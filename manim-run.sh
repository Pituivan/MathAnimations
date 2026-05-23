#!/usr/bin/env bash

FILE="$1"
SCENE="$(basename "$FILE" .py)"

rm -rf media/
python -m manim -pql "$FILE" "$SCENE"