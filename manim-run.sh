#!/usr/bin/env bash

FILE="$1"
SCENE="$(basename "$FILE" .py)"

python -m manim -pql "$FILE" "$SCENE"