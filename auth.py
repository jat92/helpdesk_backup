from requests.auth import HTTPBasicAuth
import os
import sys
from json import load
from pathlib import Path

secrets_file=Path(os.getenv("SECRETS_FILE", "/var/tmp/secrets.json"))
if not secrets_file.exists():
    print(f"Cant read secrets file {secrets_file}")
    sys.exit(1)

secrets=None
with open(secrets_file, 'r', encoding="utf8") as f:
    secrets = load(f)

api_key=os.getenv("FS_API_KEY",None)
if not api_key and "FS_API_KEY" not in secrets:
    print("Cant auth to the Freashservice API, missing API Key")
    sys.exit(1)
if not api_key:
    api_key=secrets["FS_API_KEY"]

db_connection_str="sqlite:///test_db.db"
if "DB_PASSWORD" in secrets:
    db_connection_str=f"postgresql+psycopg2://{secrets['DB_USER']}:{secrets['DB_PASSWORD']}@localhost:5432/fs_backup"

http_auth = HTTPBasicAuth(api_key, '')
