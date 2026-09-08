#!/usr/bin/env bash
# Verifier entrypoint: fail closed on deliverable name/type/sheets and input snapshot.
# Never resume grading against a writable live inputs directory after snapshot failure.
set -euo pipefail

OUTPUT_DIR="${1:-/outputs}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Platform may expose the immutable snapshot under several env names / paths.
SNAPSHOT="${INPUT_SNAPSHOT_MANIFEST:-${SNAPSHOT_MANIFEST:-${INPUTS_SNAPSHOT_MANIFEST:-}}}"
if [[ -z "${SNAPSHOT}" && -f /immutable/inputs_manifest.json ]]; then
  SNAPSHOT="/immutable/inputs_manifest.json"
fi
if [[ -z "${SNAPSHOT}" && -f /snapshot/inputs_manifest.json ]]; then
  SNAPSHOT="/snapshot/inputs_manifest.json"
fi

if [[ -n "${SNAPSHOT}" ]]; then
  python3 "${SCRIPT_DIR}/check_outputs.py" "${OUTPUT_DIR}" --snapshot "${SNAPSHOT}"
else
  # Deliverable checks always run. Snapshot is required when the platform provisions one;
  # absence here means the harness did not supply a manifest (local smoke), not fail-open
  # fallback after a failed snapshot.
  python3 "${SCRIPT_DIR}/check_outputs.py" "${OUTPUT_DIR}"
fi
