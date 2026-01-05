#!/bin/bash
# Example: Generate a complete meditation session

# Configuration
OUTPUT_DIR="./output"
DURATION=600  # 10 minutes

mkdir -p "$OUTPUT_DIR"

echo "=== Vibe OS Meditation Session Generator ==="
echo ""

# Step 1: Generate theta binaural beat
echo "Step 1: Generating theta binaural beat..."
python ../tools/frequency-generator-pro.py \
    --preset theta \
    --duration $DURATION \
    --quality high \
    --output "$OUTPUT_DIR/theta_tone.wav"

# Step 2: Show recommended Suno prompt
echo ""
echo "Step 2: Recommended Suno/Hailuo prompt for theta-compatible music:"
echo "------------------------------------------------------------"
python ../tools/vibe-os-mixer.py --suno-prompt theta
echo "------------------------------------------------------------"
echo ""
echo "Generate music using the prompt above via Suno, Hailuo, or Udio"
echo "Save the track as: $OUTPUT_DIR/ai_music.mp3"
echo ""

# Step 3: Instructions for mixing
echo "Step 3: Once you have the AI music, mix with:"
echo "python ../tools/vibe-os-mixer.py \\"
echo "    --music $OUTPUT_DIR/ai_music.mp3 \\"
echo "    --frequency theta \\"
echo "    --level binaural_optimal \\"
echo "    --output $OUTPUT_DIR/final_meditation.wav"
echo ""
echo "Done! Use headphones for binaural beats to work."
