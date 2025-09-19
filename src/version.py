from pathlib import Path

def get_version():
    try:
        version_file = Path(__file__).parent.parent / "VERSION"
        return version_file.read_text().strip()
    except:
        return "1.0.0.dev"