from pathlib import Path
import threading

# Shared model state for language identification.
model = None
model_lock = threading.Lock()
MODEL_PATH = Path(__file__).parent.parent / "resources" / "lid.176.bin"
