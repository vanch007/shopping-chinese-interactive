# -*- coding: utf-8 -*-
import os
import json
import base64
import io
from PIL import Image

base_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(base_dir, "template_game.html")
data_path = os.path.join(base_dir, "game_data_rich.json")
audio_dir = os.path.join(base_dir, "assets", "audio")
img_dir = os.path.join(base_dir, "assets", "images")
output_path = os.path.join(base_dir, "index.html")

print("1. Loading template, data, and audio...")
with open(template_path, "r", encoding="utf-8") as tf:
    tpl = tf.read()

with open(data_path, "r", encoding="utf-8") as df:
    venues = json.load(df)

for v_id, v in venues.items():
    v["bgKey"] = v_id

mlx_audio = {}
for fname in sorted(os.listdir(audio_dir)):
    if fname.endswith(".mp3") and fname != "conversation_demo.mp3":
        with open(os.path.join(audio_dir, fname), "rb") as af:
            mlx_audio[fname[:-4]] = "data:audio/mpeg;base64," + base64.b64encode(af.read()).decode("ascii")

print(f"Loaded {len(mlx_audio)} audio clips.")

required_audio = {"sys_to_map", "sys_buy_success"}
for v in venues.values():
    required_audio.add("sys_enter_" + v["id"])
    required_audio.add(v["npc"]["audioKey"])
    for field in ("vn", "explanationVi"):
        if not v["npc"].get(field):
            raise ValueError(f"Missing NPC {field} in {v['id']}")
    for choice in v["npc"]["choices"]:
        required_audio.update((choice["audioKey"], choice["replyAudioKey"]))
        for field in ("vn", "explanationVi", "replyVn", "replyExplanationVi"):
            if not choice.get(field):
                raise ValueError(f"Missing {field} in {v['id']}")
    for item in v["items"]:
        if not item.get("explanationVi"):
            raise ValueError(f"Missing product explanation in {item['id']}")
        required_audio.update(("prod_" + item["id"], item["audioKey"]))
        required_audio.update("vocab_" + tag["word"] for tag in item["vocabTags"])
required_audio.update("topic_" + str(i) for i in range(3))
missing_audio = required_audio - mlx_audio.keys()
if missing_audio:
    raise ValueError(f"Missing embedded speech: {sorted(missing_audio)}")

print("2. Compressing images...")
image_map = {
    "map": "shopping_map_bg.png",
    "shangchang": "shangchang.png",
    "yeshi": "yeshi.png",
    "chaoshi": "chaoshi.png",
    "dianzi": "dianzi.png",
    "shichang": "shichang.png",
    "xiaomaibu": "xiaomaibu.png",
    "wangzhan": "wangzhan.png"
}

b64_dict = {}
for key, fname in image_map.items():
    p = os.path.join(img_dir, fname)
    if not os.path.isfile(p):
        raise FileNotFoundError(p)
    if os.path.exists(p):
        im = Image.open(p)
        if im.width > 1200:
            ratio = 1200.0 / im.width
            im = im.resize((1200, int(im.height * ratio)), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.convert("RGB").save(buf, format="JPEG", quality=78, optimize=True)
        raw_bytes = buf.getvalue()
        b64_dict[key] = "data:image/jpeg;base64," + base64.b64encode(raw_bytes).decode("ascii")

print("3. Replacing placeholders...")
final_html = tpl.replace("__IMAGES_JSON__", json.dumps(b64_dict, ensure_ascii=False))
final_html = final_html.replace("__VENUES_JSON__", json.dumps(venues, ensure_ascii=False))
final_html = final_html.replace("__AUDIO_JSON__", json.dumps(mlx_audio, ensure_ascii=False))

with open(output_path, "w", encoding="utf-8") as out:
    out.write(final_html)

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"4. Success! Generated clean standalone index.html: {size_mb:.2f} MB")
