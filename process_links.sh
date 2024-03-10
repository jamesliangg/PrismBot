#!/bin/bash

# Read each line from resources.md
while IFS= read -r line; do
    # Pass the line as an argument to your Python script
    python chat.py "$line"
done < resources.md
