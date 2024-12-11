import qrcode
import io
from fastapi.responses import StreamingResponse

def get_qrcode(content: str):
    qr_code = qrcode.make(content)
    buffer = io.BytesIO()
    qr_code.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")