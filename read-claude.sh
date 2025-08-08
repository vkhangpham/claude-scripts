#!/bin/bash

# Read Claude's output from clipboard
# Usage: ./read-claude.sh

# Get clipboard content
text=$(pbpaste)

# Read it aloud (you can change the voice)
say -v Samantha "$text"

# Optional: save to audio file
# say -v Samantha "$text" -o ~/Desktop/claude-output.aiff