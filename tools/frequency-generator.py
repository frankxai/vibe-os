#!/usr/bin/env python3
"""
Frequency Generator - Pure Hz tone and binaural beat generator
Part of the Vibe OS Audio System

Usage:
    python frequency-generator.py --freq 528 --duration 60 --output love_frequency.wav
    python frequency-generator.py --binaural 432 438 --duration 300 --output theta_binaural.wav
    python frequency-generator.py --solfeggio all --duration 30 --output solfeggio_sequence.wav
"""

import argparse
import numpy as np
import wave
import struct
import os
from typing import List, Tuple

# Solfeggio frequencies and their properties
SOLFEGGIO_FREQUENCIES = {
    174: "Pain reduction, security",
    285: "Tissue healing, safety",
    396: "Liberation from fear, guilt",
    417: "Facilitating change, undoing situations",
    528: "Love frequency, DNA repair, miracles",
    639: "Relationships, reconnection",
    741: "Awakening intuition, expression",
    852: "Spiritual order, returning to source",
    963: "Divine consciousness, pineal activation"
}

# Common healing frequencies
HEALING_FREQUENCIES = {
    "earth": 7.83,      # Schumann resonance
    "om": 136.1,        # Om frequency
    "love": 528,        # Love/DNA repair
    "universal": 432,   # Universal tuning
    "crown": 963,       # Crown chakra
    "third_eye": 852,   # Third eye
    "throat": 741,      # Throat chakra
    "heart": 639,       # Heart chakra
    "solar": 528,       # Solar plexus
    "sacral": 417,      # Sacral chakra
    "root": 396,        # Root chakra
}

# Brainwave frequencies for binaural beats
BRAINWAVE_STATES = {
    "delta": (0.5, 4),    # Deep sleep, healing
    "theta": (4, 8),      # Meditation, creativity
    "alpha": (8, 13),     # Relaxation, calm
    "beta": (13, 30),     # Focus, alertness
    "gamma": (30, 100),   # Peak performance, insight
}


def generate_sine_wave(frequency: float, duration: float, sample_rate: int = 44100, amplitude: float = 0.5) -> np.ndarray:
    """Generate a pure sine wave at the specified frequency."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave


def generate_binaural_beat(base_freq: float, beat_freq: float, duration: float,
                           sample_rate: int = 44100, amplitude: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate binaural beats - different frequencies for left and right ear.
    The brain perceives the difference as the 'beat' frequency.

    Args:
        base_freq: Base frequency (e.g., 432 Hz)
        beat_freq: Desired brainwave frequency (e.g., 6 Hz for theta)
        duration: Duration in seconds

    Returns:
        Tuple of (left_channel, right_channel)
    """
    left_freq = base_freq
    right_freq = base_freq + beat_freq

    left = generate_sine_wave(left_freq, duration, sample_rate, amplitude)
    right = generate_sine_wave(right_freq, duration, sample_rate, amplitude)

    return left, right


def generate_isochronic_tone(frequency: float, pulse_rate: float, duration: float,
                             sample_rate: int = 44100, amplitude: float = 0.5) -> np.ndarray:
    """
    Generate isochronic tones - single tone that pulses on and off.
    Can be used with speakers (doesn't require headphones like binaural).
    """
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    carrier = amplitude * np.sin(2 * np.pi * frequency * t)

    # Create pulse envelope
    pulse = 0.5 * (1 + np.sign(np.sin(2 * np.pi * pulse_rate * t)))

    return carrier * pulse


def apply_fade(audio: np.ndarray, fade_duration: float = 2.0, sample_rate: int = 44100) -> np.ndarray:
    """Apply fade in and fade out to avoid clicks."""
    fade_samples = int(fade_duration * sample_rate)

    if len(audio) < fade_samples * 2:
        fade_samples = len(audio) // 4

    # Fade in
    fade_in = np.linspace(0, 1, fade_samples)
    audio[:fade_samples] *= fade_in

    # Fade out
    fade_out = np.linspace(1, 0, fade_samples)
    audio[-fade_samples:] *= fade_out

    return audio


def save_mono_wav(audio: np.ndarray, filename: str, sample_rate: int = 44100):
    """Save mono audio to WAV file."""
    audio = apply_fade(audio, sample_rate=sample_rate)
    audio = np.clip(audio, -1, 1)
    audio_int = (audio * 32767).astype(np.int16)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int.tobytes())

    print(f"Saved: {filename}")


def save_stereo_wav(left: np.ndarray, right: np.ndarray, filename: str, sample_rate: int = 44100):
    """Save stereo audio (for binaural beats) to WAV file."""
    left = apply_fade(left, sample_rate=sample_rate)
    right = apply_fade(right, sample_rate=sample_rate)

    left = np.clip(left, -1, 1)
    right = np.clip(right, -1, 1)

    left_int = (left * 32767).astype(np.int16)
    right_int = (right * 32767).astype(np.int16)

    # Interleave left and right channels
    stereo = np.empty((left_int.size + right_int.size,), dtype=np.int16)
    stereo[0::2] = left_int
    stereo[1::2] = right_int

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(stereo.tobytes())

    print(f"Saved: {filename}")


def generate_solfeggio_sequence(duration_per_freq: float = 30, output_dir: str = ".") -> List[str]:
    """Generate all solfeggio frequencies as separate files."""
    files = []
    for freq, description in SOLFEGGIO_FREQUENCIES.items():
        filename = os.path.join(output_dir, f"solfeggio_{freq}hz.wav")
        audio = generate_sine_wave(freq, duration_per_freq)
        save_mono_wav(audio, filename)
        print(f"  {freq} Hz - {description}")
        files.append(filename)
    return files


def generate_chakra_meditation(duration_per_chakra: float = 60, output_file: str = "chakra_meditation.wav"):
    """Generate a full chakra meditation sequence (root to crown)."""
    chakra_sequence = [396, 417, 528, 639, 741, 852, 963]

    full_audio = np.array([])
    for freq in chakra_sequence:
        audio = generate_sine_wave(freq, duration_per_chakra)
        audio = apply_fade(audio, fade_duration=3.0)
        full_audio = np.concatenate([full_audio, audio])

    save_mono_wav(full_audio, output_file)
    total_duration = len(chakra_sequence) * duration_per_chakra
    print(f"Created {total_duration/60:.1f} minute chakra meditation")


def main():
    parser = argparse.ArgumentParser(
        description="Frequency Generator - Create pure Hz tones and binaural beats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single frequency (528 Hz love frequency, 5 minutes)
  python frequency-generator.py --freq 528 --duration 300 --output love_528hz.wav

  # Binaural beat for theta meditation (6 Hz beat on 432 Hz carrier)
  python frequency-generator.py --binaural 432 6 --duration 600 --output theta_meditation.wav

  # Isochronic tone for focus (10 Hz alpha on 528 Hz)
  python frequency-generator.py --isochronic 528 10 --duration 300 --output focus_isochronic.wav

  # All solfeggio frequencies
  python frequency-generator.py --solfeggio all --duration 60

  # Full chakra meditation sequence
  python frequency-generator.py --chakra --duration 60

  # List all available frequencies
  python frequency-generator.py --list

Healing Frequencies:
  174 Hz - Pain reduction       528 Hz - Love/DNA repair
  285 Hz - Tissue healing       639 Hz - Relationships
  396 Hz - Liberation           741 Hz - Intuition
  417 Hz - Change               852 Hz - Spiritual order
  432 Hz - Universal            963 Hz - Divine consciousness
"""
    )

    parser.add_argument("--freq", "-f", type=float, help="Single frequency in Hz")
    parser.add_argument("--binaural", "-b", nargs=2, type=float, metavar=("BASE", "BEAT"),
                        help="Binaural beat: base frequency and beat frequency")
    parser.add_argument("--isochronic", "-i", nargs=2, type=float, metavar=("FREQ", "PULSE"),
                        help="Isochronic tone: frequency and pulse rate")
    parser.add_argument("--solfeggio", "-s", choices=["all"] + [str(f) for f in SOLFEGGIO_FREQUENCIES.keys()],
                        help="Generate solfeggio frequency(s)")
    parser.add_argument("--chakra", "-c", action="store_true", help="Generate full chakra meditation")
    parser.add_argument("--duration", "-d", type=float, default=60, help="Duration in seconds (default: 60)")
    parser.add_argument("--output", "-o", type=str, default="output.wav", help="Output filename")
    parser.add_argument("--list", "-l", action="store_true", help="List all available frequencies")
    parser.add_argument("--amplitude", "-a", type=float, default=0.5, help="Amplitude 0-1 (default: 0.5)")

    args = parser.parse_args()

    if args.list:
        print("\n=== SOLFEGGIO FREQUENCIES ===")
        for freq, desc in SOLFEGGIO_FREQUENCIES.items():
            print(f"  {freq:>4} Hz - {desc}")

        print("\n=== HEALING FREQUENCIES ===")
        for name, freq in HEALING_FREQUENCIES.items():
            print(f"  {name:>10}: {freq:>6.2f} Hz")

        print("\n=== BRAINWAVE STATES (for binaural beats) ===")
        for state, (low, high) in BRAINWAVE_STATES.items():
            print(f"  {state:>6}: {low:>4.1f} - {high:>5.1f} Hz")
        return

    if args.freq:
        print(f"Generating {args.freq} Hz tone for {args.duration} seconds...")
        audio = generate_sine_wave(args.freq, args.duration, amplitude=args.amplitude)
        save_mono_wav(audio, args.output)

    elif args.binaural:
        base_freq, beat_freq = args.binaural
        print(f"Generating binaural beat: {base_freq} Hz base, {beat_freq} Hz beat for {args.duration} seconds...")
        print(f"  Left ear: {base_freq} Hz")
        print(f"  Right ear: {base_freq + beat_freq} Hz")
        print(f"  Perceived beat: {beat_freq} Hz")
        left, right = generate_binaural_beat(base_freq, beat_freq, args.duration, amplitude=args.amplitude)
        save_stereo_wav(left, right, args.output)

    elif args.isochronic:
        freq, pulse = args.isochronic
        print(f"Generating isochronic tone: {freq} Hz at {pulse} Hz pulse for {args.duration} seconds...")
        audio = generate_isochronic_tone(freq, pulse, args.duration, amplitude=args.amplitude)
        save_mono_wav(audio, args.output)

    elif args.solfeggio:
        if args.solfeggio == "all":
            print("Generating all solfeggio frequencies...")
            generate_solfeggio_sequence(args.duration)
        else:
            freq = int(args.solfeggio)
            print(f"Generating solfeggio {freq} Hz - {SOLFEGGIO_FREQUENCIES[freq]}...")
            audio = generate_sine_wave(freq, args.duration, amplitude=args.amplitude)
            save_mono_wav(audio, args.output)

    elif args.chakra:
        print("Generating full chakra meditation sequence...")
        generate_chakra_meditation(args.duration, args.output)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
