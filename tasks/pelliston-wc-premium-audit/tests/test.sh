#!/usr/bin/env bash
# Verifier entrypoint: fail closed on deliverable name/type/sheets and optional input snapshot.
set -euo pipefail

OUTPUT_DIR="${1:-/outputs}"
SNAPSHOT="${INPUT_SNAPSHOT_MANIFEST:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${SNAPSHOT}" ]]; then
  python3 "${SCRIPT_DIR}/check_outputs.py" "${OUTPUT_DIR}" --snapshot "${SNAPSHOT}"
else
  # Deliverable checks always run; snapshot required when platform provides it.
  python3 "${SCRIPT_DIR}/check_outputs.py" "${OUTPUT_DIR}"
fi
