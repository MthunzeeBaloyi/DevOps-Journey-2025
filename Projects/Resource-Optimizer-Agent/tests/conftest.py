import sys
from pathlib import Path
# Add the project root to sys.path so `import src` works during pytest runs.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
