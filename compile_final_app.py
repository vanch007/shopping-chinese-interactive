"""Build the offline, single-file mobile shopping story."""
import base64
import io
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent


def encode(path, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


def script_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def build():
    venues = json.loads((ROOT / 'game_data_rich.json').read_text())
    story = json.loads((ROOT / 'story_data.json').read_text())
    required = {'sys_story', 'sys_finish', 'sys_to_map', 'sys_buy_success'}
    required.update(t['audioKey'] for t in story['topics'])
    required.update('vocab_' + t['word'] for t in story['vocab'])
    for key, venue in venues.items():
        required.update(('sys_enter_' + key, venue['npc']['audioKey']))
        for field in ('vn', 'textPy', 'explanationVi'):
            assert venue['npc'].get(field), (key, field)
        for choice in venue['npc']['choices']:
            required.update((choice['audioKey'], choice['replyAudioKey']))
            assert choice['focusItem'] in {i['id'] for i in venue['items']}
            for field in ('vn', 'py', 'explanationVi', 'replyVn', 'replyPy', 'replyExplanationVi'):
                assert choice.get(field), (key, field)
        for item in venue['items']:
            required.update(('prod_' + item['id'], item['audioKey']))
            required.update('vocab_' + tag['word'] for tag in item['vocabTags'])
            assert item.get('explanationVi'), item['id']
    missing = [key for key in required if not (ROOT / 'assets/audio' / (key + '.mp3')).is_file()]
    if missing:
        raise ValueError('Missing generated audio: ' + ', '.join(sorted(missing)))
    audio = {key: encode(ROOT / 'assets/audio' / (key + '.mp3'), 'audio/mpeg') for key in sorted(required)}
    images = {}
    for key in ['map', *venues]:
        image = Image.open(ROOT / 'assets/images/story-v2' / (key + '.png')).convert('RGB')
        assert image.height > image.width, key
        if image.width > 960:
            image = image.resize((960, round(image.height * 960 / image.width)), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        image.save(buf, format='JPEG', quality=79, optimize=True)
        images[key] = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')
    source = (ROOT / 'template_game.html').read_text()
    for placeholder, value in [('__VENUES_JSON__', venues), ('__STORY_JSON__', story),
                               ('__AUDIO_JSON__', audio), ('__IMAGES_JSON__', images)]:
        assert placeholder in source
        source = source.replace(placeholder, script_json(value))
    assert '__STORY_JSON__' not in source
    (ROOT / 'index.html').write_text(source)
    print(f'Built v{story["version"]}: {len(venues)} scenes, {len(audio)} embedded audio clips, '
          f'{len(images)} images; {len(source.encode()) / 1024 / 1024:.2f} MiB. No external runtime assets.')


if __name__ == '__main__':
    build()
