#!/usr/bin/env bash
# Verifier entrypoint: fail closed on deliverable + required input snapshot.
# Never resume grading against a writable live inputs directory.
set -euo pipefail

OUTPUT_DIR="${1:-/outputs}"
SNAPSHOT="${INPUT_SNAPSHOT_MANIFEST:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "${SNAPSHOT}" ]]; then
  echo "FAIL: INPUT_SNAPSHOT_MANIFEST is unset." >&2
  echo "Refusing to grade without an immutable input snapshot (no live-input fallback)." >&2
  exit 1
fi

if [[ ! -f "${SNAPSHOT}" ]]; then
  echo "FAIL: snapshot manifest missing at ${SNAPSHOT}." >&2
  echo "Refusing to grade against a live/writable inputs directory." >&2
  exit 1
fi

python3 "${SCRIPT_DIR}/check_outputs.py" "${OUTPUT_DIR}" --snapshot "${SNAPSHOT}"
