#!/bin/bash

# Live Claude response reader
# Monitors clipboard for changes and reads them aloud

echo "Claude Live Reader started. Copy any text to hear it."
echo "Press Ctrl+C to stop."

# Store the last clipboard content
last_content=$(pbpaste)

while true; do
    # Get current clipboard content
    current_content=$(pbpaste)
    
    # Check if content changed
    if [ "$current_content" != "$last_content" ]; then
        echo "Reading new content..."
        say -v Samantha "$current_content"
        last_content="$current_content"
    fi
    
    # Check every 0.5 seconds
    sleep 0.5
done