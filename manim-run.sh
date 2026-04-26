#!/usr/bin/env bash

FILE="$1"
SCENE="$(basename "$FILE" .py)"

rm -r media/
python -m manim -pql "$FILE" "$SCENE"