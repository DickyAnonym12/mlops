import json, os, re
from pathlib import Path
import lmstudio as lms

IMAGE = Path("data/raw/nota.png")
MODEL = os.environ["LM_STUDIO_MODEL"]
image = lms.prepare_image(str(IMAGE))
model = lms.llm(MODEL)
chat = lms.Chat()
chat.add_user_message(
  "Baca nota. Ekstrak merchant, tanggal, item, subtotal, pajak, dan total. "
  "Keluarkan JSON valid. Jika pajak tidak terlihat, isi 0. Jangan mengarang.",
  images=[image],
)
prediction = model.respond(chat)

raw = prediction.content.strip()
raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
result = json.loads(raw)

Path("reports/receipt.json").write_text(
  json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(json.dumps(result, indent=2, ensure_ascii=False))
