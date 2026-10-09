"""Master checked IndexTTS utterances for the standalone app."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def command(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)

def master(source, target):
    measure = command(['ffmpeg','-hide_banner','-i',str(source),'-af',
        'loudnorm=I=-18:TP=-2:LRA=7:print_format=json','-f','null','-'])
    stats = json.JSONDecoder().raw_decode(measure.stderr[measure.stderr.rfind('{'):])[0]
    filt = ('loudnorm=I=-18:TP=-2:LRA=7:linear=true:'
            f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
            f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
            f"offset={stats['target_offset']}:print_format=json")
    result = command(['ffmpeg','-hide_banner','-y','-i',str(source),'-af',filt,
        '-ac','1','-ar','24000','-c:a','libmp3lame','-b:a','64k',str(target)])
    return json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind('{'):])[0]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', type=Path, action='append', required=True)
    p.add_argument('--expected', type=Path, required=True)
    p.add_argument('--output-report', type=Path, required=True)
    args = p.parse_args()
    rows = {}
    for path in args.manifest:
        with path.open() as f:
            for row in csv.DictReader(f): rows[row['id']] = row
    with args.expected.open() as f: expected = {r['id']:r for r in csv.DictReader(f)}
    if rows.keys() != expected.keys():
        raise ValueError(f'Voice coverage mismatch: {rows.keys() ^ expected.keys()}')
    report = []
    for key, target in expected.items():
        row = rows[key]
        if row['version'] != '2.5' or row['language'] != 'zh' or row['emotion_source'] != 'manual':
            raise ValueError(f'Unexpected speech model or controls: {key}')
        spoken_text = re.sub(r'<([^|<>]+)\|[^<>]+>', r'\1', row['text'])
        if spoken_text != target['text'] or any(row[k] != target[k] for k in ['ref_audio','emotion']):
            raise ValueError(f'Voice provenance mismatch: {key}')
        source = Path(row['output_path'])
        out = ROOT/'assets/audio'/f'{key}.mp3'
        stats = master(source, out)
        report.append(dict(id=key, text=target['text'], speaker=target['speaker'],
            reference_name=Path(target['ref_audio']).name,
            reference_sha256=hashlib.sha256(Path(target['ref_audio']).read_bytes()).hexdigest(),
            emotion=target['emotion'], direction=target['direction'],
            generation_seconds=float(row['elapsed_s']), duration_seconds=float(row['duration_s']),
            sha256=hashlib.sha256(out.read_bytes()).hexdigest(), mastering=stats))
        print(f'Mastered {key}',flush=True)
    args.output_report.parent.mkdir(parents=True,exist_ok=True)
    args.output_report.write_text(json.dumps(dict(clips=report,total_generated=len(report)),ensure_ascii=False,indent=2)+'\n')
    # Keep a WAV listening reel; public files contain generated speech only.
    import numpy as np
    import soundfile as sf
    def decode(key):
        r=subprocess.run(['ffmpeg','-v','error','-i',str(ROOT/'assets/audio'/f'{key}.mp3'),
            '-f','f32le','-ar','24000','-ac','1','pipe:1'],check=True,capture_output=True)
        return np.frombuffer(r.stdout,dtype=np.float32)
    silence=np.zeros(7200,dtype=np.float32)
    full=[part for key in expected for part in (decode(key),silence)]
    sf.write(args.output_report.parent/'combined_mastered.wav',np.concatenate(full),24000)
    demo_keys=['npc_shangchang','choice_shangchang_0','reply_shangchang_0']
    demo=np.concatenate([part for key in demo_keys for part in (decode(key),silence)])
    demo_wav=args.output_report.parent/'conversation_demo.wav'
    sf.write(demo_wav,demo,24000)
    command(['ffmpeg','-v','error','-y','-i',str(demo_wav),'-c:a','libmp3lame','-b:a','96k',str(ROOT/'assets/audio/conversation_demo.mp3')])
    print(f'Mastered {len(report)} voice tracks. Run compile_final_app.py to embed them.')

if __name__ == '__main__': main()
