from pathlib import Path
import sys
import qrcode

def generate_qr(text: str, filename: str = "", save_dir: str = "") -> str:
    filename = filename.strip() if filename.strip() else "qrcode"
    if not filename.endswith(".png"):
        filename += ".png"

    if save_dir and Path(save_dir).exists():
        target_dir = Path(save_dir)
    else:
        if getattr(sys, "frozen", False):
            target_dir = Path(sys.executable).parent
        else:
            target_dir = Path(__file__).resolve().parent.parent

    save_path = target_dir / filename

    img = qrcode.make(text)
    img.save(str(save_path))

    return str(save_path)