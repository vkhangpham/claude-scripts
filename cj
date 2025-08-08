#!/bin/bash
# French Conjugation CLI wrapper
script_dir="$(dirname "$0")"
exec python "$script_dir/french-conjugator-verbecc.py" "$@"