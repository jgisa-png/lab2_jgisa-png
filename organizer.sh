#!/bin/bash

# Configuration variables
SOURCE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

if [ ! -f "$SOURCE" ]; then
    echo "Error: '$SOURCE' was NOT found in $(pwd)."
    echo "Hint: run this script from the folder that contains '$SOURCE'."
    exit 1
fi

if [ ! -s "$SOURCE" ]; then
    echo "Warning: '$SOURCE' is empty. Archiving it anyway."
fi

mkdir -p "$ARCHIVE_DIR"

DEST="$ARCHIVE_DIR/grades_${TIMESTAMP}.csv"
COUNTER=1
while [ -e "$DEST" ]; do
    DEST="$ARCHIVE_DIR/grades_${TIMESTAMP}_${COUNTER}.csv"
    ((COUNTER++))
done

if mv "$SOURCE" "$DEST"; then
    echo "Archived '$SOURCE' -> '$DEST'"
    echo "[$TIMESTAMP] Archived '$SOURCE' -> '$DEST'" >> "$LOG_FILE"
    # Create a fresh empty file for the next batch
    : > "$SOURCE"
else
    echo "Error: could not move '$SOURCE' to '$DEST'."
    echo "[$TIMESTAMP] ERROR moving '$SOURCE' to '$DEST'" >> "$LOG_FILE"
    exit 1
fi
