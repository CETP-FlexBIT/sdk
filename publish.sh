#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./publish.sh [--npm] [--pypi] [--dry-run]

Build and publish the selected SDK packages using their current versions.

  --npm       Publish @flexbit/sdk to npm (requires npm and installed dependencies)
  --pypi      Publish flexbit-sdk to PyPI (requires uv)
  --pypy      Alias for --pypi
  --dry-run   Build and preview publishing without uploading packages
  -h, --help  Show this help

Select at least one registry. Use --npm --pypi to publish both.
Authenticate npm with npm login or your npm configuration.
Authenticate PyPI with UV_PUBLISH_TOKEN or uv's configured credentials.
EOF
}

publish_npm=false
publish_pypi=false
dry_run_args=()

for arg in "$@"; do
  case "$arg" in
    --npm) publish_npm=true ;;
    --pypi|--pypy) publish_pypi=true ;;
    --dry-run) dry_run_args=(--dry-run) ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$arg" >&2; usage >&2; exit 1 ;;
  esac
done

if ! "$publish_npm" && ! "$publish_pypi"; then
  usage >&2
  exit 1
fi

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Required command not found: %s\n' "$1" >&2
    exit 1
  fi
}

if "$publish_npm"; then require_command npm; fi
if "$publish_pypi"; then require_command uv; fi

root_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if "$publish_pypi"; then
  # Isolate this build so old distributions cannot be uploaded by accident.
  build_dir="$(mktemp -d "${TMPDIR:-/tmp}/flexbit-publish.XXXXXX")"
  trap 'rm -rf -- "$build_dir"' EXIT
  (
    cd "$root_dir/clients/python"
    uv build --no-sources --out-dir "$build_dir"
  )
fi

if "$publish_npm"; then
  (
    cd "$root_dir/clients/typescript"
    # prepublishOnly runs the TypeScript build, including during a dry run.
    npm publish --access public ${dry_run_args[@]+"${dry_run_args[@]}"}
  )
fi

if "$publish_pypi"; then
  (
    cd "$root_dir/clients/python"
    uv publish ${dry_run_args[@]+"${dry_run_args[@]}"} "$build_dir"/*.whl "$build_dir"/*.tar.gz
  )
fi
