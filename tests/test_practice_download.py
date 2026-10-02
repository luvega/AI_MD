import hashlib
import importlib.util
import io
import json
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "chapters/shared/assets/get-practice.py"
spec = importlib.util.spec_from_file_location("practice_download", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fake_site(monkeypatch):
    payloads = {"chapter-03/input.pdb": b"ATOM input", "chapter-04/run.py": b"print('ready')"}
    rows = [{"chapter": int(path[8:10]), "relative_path": path.replace("/", "/assets/", 1), "url_path": path,
             "sha256": hashlib.sha256(data).hexdigest()} for path, data in payloads.items()]
    manifest = {"dependencies": {"4": [3]}, "files": rows}
    payloads["shared/practice-downloads.json"] = json.dumps(manifest).encode()
    monkeypatch.setattr(module, "urlopen", lambda request, timeout: io.BytesIO(payloads[request.full_url.removeprefix("https://test/assets/")]))


def test_download_includes_inputs_and_preserves_modified_files(tmp_path, monkeypatch):
    fake_site(monkeypatch)
    assert module.download(4, tmp_path, "https://test/assets/") == 2
    assert (tmp_path / "chapter-03/assets/input.pdb").read_bytes() == b"ATOM input"
    assert module.download(4, tmp_path, "https://test/assets/") == 2
    (tmp_path / "chapter-04/assets/run.py").write_text("my edits")
    with pytest.raises(FileExistsError):
        module.download(4, tmp_path, "https://test/assets/")


def test_download_checks_bytes_before_writing(tmp_path, monkeypatch):
    manifest = {"files": [{"chapter": 1, "relative_path": "chapter-01/assets/input.txt",
                          "url_path": "chapter-01/input.txt", "sha256": "0" * 64}]}
    monkeypatch.setattr(module, "urlopen", lambda request, timeout: io.BytesIO(json.dumps(manifest).encode() if request.full_url.endswith("json") else b"changed"))
    with pytest.raises(ValueError, match="checksum"):
        module.download(1, tmp_path, "https://test/assets/")
    assert not (tmp_path / "chapter-01/assets/input.txt").exists()
