import os
import sys
import tempfile
from pathlib import Path

# Garante que a raiz do projeto esteja no path dos testes
PROJETO = Path(__file__).resolve().parent.parent
if str(PROJETO) not in sys.path:
    sys.path.insert(0, str(PROJETO))

# Usa um banco temporário isolado antes de importar os models
_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_db_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"

from models.db import Base, engine  # noqa: E402


def pytest_sessionstart():
    Base.metadata.create_all(engine)


def pytest_sessionfinish():
    os.remove(_db_path)
