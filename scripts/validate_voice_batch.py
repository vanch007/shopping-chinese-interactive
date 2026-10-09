"""Read back locally generated Chinese dialogue with offline Confucius ASR."""
import argparse
import csv
import difflib
import importlib.util
import json
import os
from pathlib import Path
import re
import time
import unicodedata

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'

def normalized(text):
    return ''.join(c for c in text if unicodedata.category(c)[0] in {'L', 'N'})

def distance(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        curr = [i]
        for j, y in enumerate(b, 1):
            curr.append(min(curr[-1] + 1, prev[j] + 1, prev[j-1] + (x != y)))
        prev = curr
    return prev[-1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', type=Path, action='append', required=True)
    p.add_argument('--report', type=Path, required=True)
    args = p.parse_args()
    if args.report.exists():
        raise FileExistsError(args.report)
    helper = Path('/Users/vanch/.codex/skills/asr-language-recognition/scripts/confucius_transcribe.py')
    spec = importlib.util.spec_from_file_location('local_confucius', helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    model_path = module.resolve_model()
    import mlx.core as mx
    from mlx_audio.stt.utils import load_model, load_audio
    model = load_model(str(model_path))
    cases = []
    rows = {}
    for manifest in args.manifest:
        with manifest.open() as f:
            for r in csv.DictReader(f):
                rows[r['id']] = r
    for key, row in rows.items():
        path = Path(row['output_path'])
        audio = load_audio(str(path))
        started = time.perf_counter()
        result = model.generate(audio, language='Chinese', temperature=0, max_tokens=512, chunk_duration=30.0)
        mx.synchronize()
        actual = result.text.rstrip().removesuffix('|').strip()
        expected = re.sub(r'<([^|<>]+)\|[^<>]+>', r'\1', row['text'])
        a, b = normalized(expected), normalized(actual)
        edits = distance(a, b)
        budget_hit = getattr(result, 'generation_tokens', 0) >= 512
        status = 'pass' if edits == 0 and not budget_hit else 'review'
        diff = [dict(operation=t, expected=a[x:y], actual=b[u:v]) for t,x,y,u,v in difflib.SequenceMatcher(None,a,b).get_opcodes() if t != 'equal']
        entry = dict(id=key, expected=expected, transcript=actual, status=status,
                     character_error_rate=edits/max(1,len(a)), differences=diff,
                     token_budget_reached=budget_hit, audio_seconds=int(audio.shape[0])/16000,
                     processing_seconds=time.perf_counter()-started)
        cases.append(entry)
        print(json.dumps(entry, ensure_ascii=False), flush=True)
    report = dict(model=str(model_path), status='pass' if all(c['status']=='pass' for c in cases) else 'review',
                  method='Independent ASR; punctuation ignored; no forced alignment or supplied transcript prompt.',
                  voice_similarity='pending listening review', emotion_naturalness='pending listening review', cases=cases)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__':
    main()
