#!/usr/bin/env bash

FILE="$1"
SCENE="$(basename "$FILE" .py)"

QUALITY="0"
FPS="60"

shift
while [[ $# -gt 0 ]]; do
    case "$1" in
        --quality) QUALITY="$2"; shift 2 ;;
        --fps) FPS="$2"; shift 2 ;;
    esac
done

case "$QUALITY" in
    0) Q="-ql" ;;
    1) Q="-qm" ;;
    2) Q="-qh" ;;
    *)
      echo "Invalid quality: $QUALITY. Valid values are 0 (low), 1 (medium), or 2 (high)."
      exit 1
      ;;
esac

rm -rf media/
python -m manim "$Q" -p "$FILE" "$SCENE" --fps "$FPS"