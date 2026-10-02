"""Run two sequences on the published PDL1 RFD3 backbone with pinned ProteinMPNN."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.request import urlopen

COMMIT = "8907e6671bfbfc92303b5f79c4b5e6ce47cdef57"
BASE = f"https://raw.githubusercontent.com/dauparas/ProteinMPNN/{COMMIT}/"
DOWNLOADS = ("protein_mpnn_run.py", "protein_mpnn_utils.py", "LICENSE", "vanilla_model_weights/v_48_020.pt")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdb", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--chain", default="A")
    parser.add_argument("--count", type=int, default=2)
    parser.add_argument("--seed", type=int, default=37)
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be positive")
    if not args.pdb.is_file():
        parser.error("PDB input not found")
    try:
        import numpy  # noqa: F401
        import torch
    except ImportError:
        parser.error("Install numpy and the CPU build of torch in the active Python environment first")
    work = args.work.resolve()
    vendor = work / "proteinmpnn"
    output = work / "outputs"
    if output.exists():
        parser.error("Output directory already exists; use a new --work to preserve earlier results")
    for name in DOWNLOADS:
        path = vendor / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            with urlopen(BASE + name, timeout=60) as response:
                path.write_bytes(response.read())
    # Upstream names targets by splitting paths on '/'; use forward slashes on Windows.
    command = [sys.executable, str(vendor / "protein_mpnn_run.py"), "--pdb_path", args.pdb.resolve().as_posix(), "--pdb_path_chains", args.chain, "--path_to_model_weights", (vendor / "vanilla_model_weights").as_posix(), "--out_folder", output.as_posix(), "--num_seq_per_target", str(args.count), "--batch_size", "1", "--sampling_temp", "0.1", "--seed", str(args.seed)]
    environment = os.environ.copy()
    environment.update(CUDA_VISIBLE_DEVICES="-1", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", PYTHONIOENCODING="utf-8")
    start = time.perf_counter()
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env=environment)
    (work / "proteinmpnn_stdout.txt").write_text(result.stdout, encoding="utf-8")
    (work / "proteinmpnn_stderr.txt").write_text(result.stderr, encoding="utf-8")
    record = {"tool": "ProteinMPNN", "upstream_commit": COMMIT, "device": "cpu", "torch_version": torch.__version__, "model_name": "v_48_020", "designed_chain": args.chain, "seed": args.seed, "temperature": 0.1, "num_sequences": args.count, "returncode": result.returncode, "elapsed_seconds": round(time.perf_counter() - start, 3), "input_sha256": hashlib.sha256(args.pdb.read_bytes()).hexdigest(), "command_arguments": command[2:], "refold_status": "not_run"}
    # Persist portable arguments without the teacher's machine paths.
    record["command_arguments"] = ["--pdb_path", args.pdb.name, "--pdb_path_chains", args.chain, "--path_to_model_weights", "proteinmpnn/vanilla_model_weights", "--out_folder", "outputs", "--num_seq_per_target", str(args.count), "--batch_size", "1", "--sampling_temp", "0.1", "--seed", str(args.seed)]
    (work / "run_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    print(f"CPU run exit={result.returncode}; output={output}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
