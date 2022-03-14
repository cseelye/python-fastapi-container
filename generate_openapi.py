from fastapi.openapi.utils import get_openapi
import argparse
import json
import os
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create OpenAPI document from FastAPI service code")
    parser.add_argument("-d", "--app-dir", default=".", help="directory the FastAPI service is in")
    parser.add_argument("-o", "--out-dir", default="doc", help="subdirectory to write the OpenAPI file into")
    args = parser.parse_args()

    app_dir = Path(args.app_dir)
    os.chdir(app_dir)
    from app.main import app

    out_dir = app_dir / "doc"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "openapi.json", "w", encoding="utf-8") as f:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
            ),
            f,
        )
