#!/bin/bash
# Example: Add subliminal 528 Hz to any song

if [ -z "$1" ]; then
    echo "Usage: ./subliminal_528hz.sh <input_song.mp3>"
    echo ""
    echo "Adds subliminal 528 Hz (Love Frequency) to any song."
    echo "The frequency is below conscious hearing but still effective."
    exit 1
fi

INPUT="$1"
OUTPUT="${INPUT%.*}_528hz_healing.wav"

echo "Adding subliminal 528 Hz to: $INPUT"
echo "Output: $OUTPUT"
echo ""

python ../tools/vibe-os-mixer.py \
    --music "$INPUT" \
    --hz 528 \
    --level subliminal \
    --output "$OUTPUT"

echo ""
echo "Done! The 528 Hz frequency is embedded at -24 dB (subliminal level)."
echo "Research shows this still produces measurable effects on stress hormones."
