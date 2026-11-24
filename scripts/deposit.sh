#!/usr/bin/env bash
# Run the deposit yourself, with your own token.
#
#   ./scripts/deposit.sh sandbox            # check the token against the sandbox
#   ./scripts/deposit.sh sandbox --publish  # actually deposit
#
# The token is read from ~/.hermes/cofre/zenodo.env and never echoed. This wrapper exists so the
# credentialed step can be run by the account holder, while the agent verifies the result afterwards
# through the public API.
set -euo pipefail

ENVFILE="${HOME}/.hermes/cofre/zenodo.env"
TARGET="${1:-sandbox}"

case "$TARGET" in
  sandbox)    VAR=ZENODO_SANDBOX_TOKEN; BASE=https://sandbox.zenodo.org/api ;;
  production) VAR=ZENODO_TOKEN;         BASE=https://zenodo.org/api ;;
  *) echo "usage: $0 {sandbox|production} [--publish]" >&2; exit 2 ;;
esac

[ -f "$ENVFILE" ] || { echo "missing $ENVFILE" >&2; exit 2; }
# shellcheck disable=SC1090
set -a; . "$ENVFILE"; set +a

if [ -z "${!VAR:-}" ]; then
  echo "error: $VAR is empty in $ENVFILE" >&2
  exit 2
fi

cd "$(dirname "$0")/.."

python3 - "$VAR" "$BASE" <<'PY'
import os, sys
import requests
var, base = sys.argv[1], sys.argv[2]
tok = os.environ.get(var, "")
r = requests.get(f"{base}/deposit/depositions",
                 headers={"Authorization": f"Bearer {tok}"}, timeout=30)
print(f"authentication against {base}: HTTP {r.status_code}")
if r.status_code == 401:
    print("  -> token invalid for this environment. Sandbox and production tokens are separate.",
          file=sys.stderr)
    sys.exit(3)
if r.status_code >= 400:
    print(f"  -> {r.text[:200]}", file=sys.stderr)
    sys.exit(3)
print(f"  ok, {len(r.json())} existing deposition(s) visible")
PY

if [ "${2:-}" = "--publish" ]; then
  python3 scripts/deposit_skills.py --env "$TARGET" --publish --include-collection
else
  echo
  echo "token works. re-run with --publish to deposit:"
  echo "  ./scripts/deposit.sh $TARGET --publish"
fi
