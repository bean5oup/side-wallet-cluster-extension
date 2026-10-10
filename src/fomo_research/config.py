import os
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE = REPO_ROOT / "data" / "research" / "fomo.sqlite3"


def load_api_key(env_file=None):
    key = os.environ.get("FOMO_API_KEY", "").strip()
    if key:
        return key

    path = Path(env_file) if env_file else REPO_ROOT / ".env"
    if path.is_file():
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() == "FOMO_API_KEY":
                key = value.strip().strip("\"'").strip()
                if key:
                    return key

    raise RuntimeError("FOMO_API_KEY is missing. Set it in .env or the process environment.")


DEFAULT_SOLANA_RPC_URL = "https://api.mainnet.solana.com"


def load_solana_rpc_url(env_file=None):
    url = os.environ.get("SOLANA_RPC_URL", "").strip()
    if not url:
        path = Path(env_file) if env_file else REPO_ROOT / ".env"
        if path.is_file():
            for raw_line in path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, value = line.split("=", 1)
                if name.strip() == "SOLANA_RPC_URL":
                    url = value.strip().strip("\"'").strip()
                    break
    if not url:
        url = DEFAULT_SOLANA_RPC_URL
    parsed = urlparse(url)
    if parsed.scheme not in ("https", "http") or not parsed.netloc:
        raise RuntimeError("SOLANA_RPC_URL must be an HTTP(S) URL.")
    return url
