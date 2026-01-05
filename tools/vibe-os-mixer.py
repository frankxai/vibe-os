#!/usr/bin/env python3
"""
Vibe OS Audio Mixer - Research-Based Frequency + Music Integration System
Part of the Vibe OS Audio System

Combines AI-generated music (Suno/Hailuo/Udio) with healing frequencies
at research-backed levels for maximum therapeutic impact.

Research Sources:
- PMC10196448: Binaural beats effective at 40 dB (comfortable listening)
- Frontiers 2023: Carrier 200-900 Hz optimal for entrainment
- PMC11367212: Subliminal frequencies still produce effects
- University of Pavia: 432 Hz reduces heart rate by 4.79 bpm

Usage:
    python vibe-os-mixer.py --music track.mp3 --frequency theta --output mixed.wav
    python vibe-os-mixer.py --music ambient.wav --binaural 432 6 --level subtle --output meditation.wav
    python vibe-os-mixer.py --music song.mp3 --hz 528 --level subliminal --output healing.wav
"""

import argparse
import numpy as np
import wave
import subprocess
import os
import tempfile
from typing import Tuple, Optional
import struct

# ============================================================================
# RESEARCH-BACKED MIXING LEVELS
# ============================================================================

MIXING_LEVELS = {
    "dominant": {
        "music_db": -6,      # Music at -6 dB
        "frequency_db": -3,   # Frequency dominant at -3 dB
        "description": "Frequency is clearly audible, leads the mix"
    },
    "balanced": {
        "music_db": -3,       # Music at -3 dB
        "frequency_db": -6,   # Frequency at -6 dB
        "description": "Equal presence of music and frequency"
    },
    "subtle": {
        "music_db": 0,        # Music at 0 dB (full)
        "frequency_db": -12,  # Frequency subtle at -12 dB
        "description": "Music leads, frequency adds texture"
    },
    "subliminal": {
        "music_db": 0,        # Music at 0 dB
        "frequency_db": -24,  # Frequency below conscious threshold
        "description": "Frequency below conscious hearing but still effective (per research)"
    },
    "binaural_optimal": {
        "music_db": -3,       # Music slightly reduced
        "frequency_db": -9,   # Binaural at ~40 dB equivalent
        "description": "Research-optimal level for binaural entrainment"
    }
}

# ============================================================================
# OPTIMAL INSTRUMENT PAIRINGS (Research-derived)
# ============================================================================

INSTRUMENT_RECOMMENDATIONS = {
    "theta": {
        "best_instruments": ["singing bowls", "ambient pads", "soft strings", "flute"],
        "avoid": ["drums", "bass-heavy", "fast tempo"],
        "tempo_range": "50-70 BPM",
        "key_suggestion": "D minor, F major (calming)"
    },
    "alpha": {
        "best_instruments": ["acoustic guitar", "piano", "light percussion", "nature sounds"],
        "avoid": ["distortion", "sudden changes"],
        "tempo_range": "60-80 BPM",
        "key_suggestion": "G major, C major (peaceful)"
    },
    "delta": {
        "best_instruments": ["deep drones", "whale sounds", "very slow strings", "rain"],
        "avoid": ["any sudden sounds", "high frequencies"],
        "tempo_range": "40-60 BPM or beatless",
        "key_suggestion": "Low register, minimal harmonic movement"
    },
    "gamma": {
        "best_instruments": ["bright synths", "crystal bowls", "bells", "light electronic"],
        "avoid": ["muddy sounds", "heavy compression"],
        "tempo_range": "80-120 BPM",
        "key_suggestion": "E major, A major (uplifting)"
    },
    "432hz": {
        "best_instruments": ["strings", "piano", "singing bowls", "choir"],
        "avoid": ["harsh digital sounds"],
        "tempo_range": "Any",
        "key_suggestion": "Natural tuning, avoid tritones"
    },
    "528hz": {
        "best_instruments": ["crystal singing bowl", "harp", "soft vocals", "nature"],
        "avoid": ["dissonance", "aggressive sounds"],
        "tempo_range": "60-90 BPM",
        "key_suggestion": "C major (528 Hz = C5 in Solfeggio)"
    }
}

# ============================================================================
# BRAINWAVE PRESETS
# ============================================================================

BRAINWAVE_PRESETS = {
    "delta": {"beat": 2, "carrier": 200, "effect": "Deep sleep, healing"},
    "theta": {"beat": 6, "carrier": 300, "effect": "Meditation, creativity"},
    "alpha": {"beat": 10, "carrier": 400, "effect": "Relaxation, calm focus"},
    "beta": {"beat": 18, "carrier": 400, "effect": "Focus, alertness"},
    "gamma": {"beat": 40, "carrier": 300, "effect": "Peak cognition, insight"},
    "schumann": {"beat": 7.83, "carrier": 432, "effect": "Earth grounding, theta state"}
}


def db_to_amplitude(db: float) -> float:
    """Convert decibels to amplitude multiplier."""
    return 10 ** (db / 20)


def read_audio_file(filepath: str) -> Tuple[np.ndarray, int, int]:
    """
    Read audio file (WAV or MP3) and return numpy array.
    Returns: (audio_data, sample_rate, channels)
    """
    # Check if file is MP3, convert if necessary
    if filepath.lower().endswith('.mp3'):
        # Convert MP3 to WAV using ffmpeg
        temp_wav = tempfile.mktemp(suffix='.wav')
        try:
            subprocess.run([
                'ffmpeg', '-i', filepath, '-acodec', 'pcm_s16le',
                '-ar', '48000', '-ac', '2', '-y', temp_wav
            ], check=True, capture_output=True)
            filepath = temp_wav
        except subprocess.CalledProcessError as e:
            print(f"Error converting MP3: {e}")
            raise

    with wave.open(filepath, 'r') as wav:
        sample_rate = wav.getframerate()
        channels = wav.getnchannels()
        n_frames = wav.getnframes()
        sample_width = wav.getsampwidth()

        raw = wav.readframes(n_frames)

        if sample_width == 2:
            audio = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
            audio /= 32768.0
        elif sample_width == 3:
            # 24-bit
            audio = np.zeros(n_frames * channels, dtype=np.float64)
            for i in range(n_frames * channels):
                audio[i] = int.from_bytes(raw[i*3:(i+1)*3], 'little', signed=True)
            audio /= 8388608.0
        else:
            audio = np.frombuffer(raw, dtype=np.int32).astype(np.float64)
            audio /= 2147483648.0

        # Reshape for stereo
        if channels == 2:
            audio = audio.reshape(-1, 2)

        return audio, sample_rate, channels


def generate_binaural_beat(duration: float, base_freq: float, beat_freq: float,
                           sample_rate: int = 48000) -> Tuple[np.ndarray, np.ndarray]:
    """Generate binaural beat tones."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + beat_freq) * t)
    return left, right


def generate_pure_tone(duration: float, frequency: float,
                       sample_rate: int = 48000) -> np.ndarray:
    """Generate pure sine wave tone."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * frequency * t)


def generate_isochronic_tone(duration: float, frequency: float, pulse_rate: float,
                             sample_rate: int = 48000) -> np.ndarray:
    """Generate isochronic (pulsing) tone."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    carrier = np.sin(2 * np.pi * frequency * t)
    # Smooth pulse envelope using raised cosine
    pulse = 0.5 * (1 + np.cos(2 * np.pi * pulse_rate * t - np.pi))
    return carrier * pulse


def apply_crossfade(audio: np.ndarray, fade_duration: float = 2.0,
                    sample_rate: int = 48000) -> np.ndarray:
    """Apply fade in and fade out."""
    fade_samples = int(fade_duration * sample_rate)

    if len(audio) < fade_samples * 2:
        fade_samples = len(audio) // 4

    # Handle both mono and stereo
    if audio.ndim == 1:
        fade_in = np.linspace(0, 1, fade_samples)
        audio[:fade_samples] *= fade_in
        fade_out = np.linspace(1, 0, fade_samples)
        audio[-fade_samples:] *= fade_out
    else:
        fade_in = np.linspace(0, 1, fade_samples).reshape(-1, 1)
        audio[:fade_samples] *= fade_in
        fade_out = np.linspace(1, 0, fade_samples).reshape(-1, 1)
        audio[-fade_samples:] *= fade_out

    return audio


def mix_audio(music: np.ndarray, frequency_left: np.ndarray, frequency_right: np.ndarray,
              music_db: float, frequency_db: float) -> np.ndarray:
    """
    Mix music with frequency tones at specified dB levels.
    """
    music_amp = db_to_amplitude(music_db)
    freq_amp = db_to_amplitude(frequency_db)

    # Ensure same length
    min_len = min(len(music), len(frequency_left))

    if music.ndim == 1:
        # Mono music - make stereo
        music_stereo = np.column_stack([music[:min_len], music[:min_len]])
    else:
        music_stereo = music[:min_len]

    freq_stereo = np.column_stack([frequency_left[:min_len], frequency_right[:min_len]])

    # Mix with levels
    mixed = (music_stereo * music_amp) + (freq_stereo * freq_amp)

    # Normalize to prevent clipping
    max_val = np.max(np.abs(mixed))
    if max_val > 0.99:
        mixed = mixed * 0.99 / max_val

    return mixed


def save_wav(audio: np.ndarray, filepath: str, sample_rate: int = 48000):
    """Save audio to WAV file (16-bit for compatibility and speed)."""
    # Ensure stereo
    if audio.ndim == 1:
        audio = np.column_stack([audio, audio])

    # Apply final fade
    audio = apply_crossfade(audio, sample_rate=sample_rate)

    # Clip and convert to 16-bit
    audio = np.clip(audio, -1, 1)
    audio_16bit = (audio * 32767).astype(np.int16)

    # Interleave stereo channels
    interleaved = audio_16bit.flatten()

    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        wav.writeframes(interleaved.tobytes())

    print(f"Saved: {filepath}")


def get_suno_prompt_for_frequency(frequency_type: str) -> str:
    """
    Generate an optimal Suno prompt for music that complements specific frequencies.
    """
    prompts = {
        "theta": """Ambient meditation music, 60 BPM, soft ethereal pads,
        gentle singing bowl textures, spacious reverb, no drums,
        D minor, peaceful and introspective, float through space""",

        "alpha": """Relaxing acoustic instrumental, 70 BPM, soft piano and
        gentle guitar, nature sounds, calming and peaceful, G major,
        light atmospheric textures, mindfulness background""",

        "delta": """Deep sleep ambient drone, 50 BPM, very low frequencies,
        ocean waves, distant whale sounds, extremely peaceful,
        minimal harmonic movement, sleep inducing, dark ambient""",

        "gamma": """Uplifting electronic ambient, 100 BPM, bright crystalline
        synths, subtle energy, clarity and focus, E major,
        inspiring and awakening, light percussion""",

        "432hz": """432 Hz tuned meditation music, soft strings and
        singing bowls, natural tuning, peaceful choir harmonies,
        grounding and centering, cosmic ambient""",

        "528hz": """528 Hz love frequency music, healing ambient,
        crystal singing bowls in C, soft harp arpeggios,
        heart opening, gentle nature sounds, deeply peaceful"""
    }

    return prompts.get(frequency_type, prompts["theta"])


def print_recommendations(frequency_type: str):
    """Print instrument and mixing recommendations."""
    rec = INSTRUMENT_RECOMMENDATIONS.get(frequency_type, INSTRUMENT_RECOMMENDATIONS["theta"])

    print(f"\n{'='*60}")
    print(f"RECOMMENDATIONS FOR {frequency_type.upper()} FREQUENCY MUSIC")
    print(f"{'='*60}")
    print(f"\nBest instruments: {', '.join(rec['best_instruments'])}")
    print(f"Avoid: {', '.join(rec['avoid'])}")
    print(f"Tempo range: {rec['tempo_range']}")
    print(f"Key suggestion: {rec['key_suggestion']}")

    print(f"\n--- Suno/Hailuo Prompt ---")
    print(get_suno_prompt_for_frequency(frequency_type))
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Vibe OS Audio Mixer - Research-Based Frequency + Music Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mix music with theta binaural beat
  python vibe-os-mixer.py --music ambient.mp3 --frequency theta --output meditation.wav

  # Custom binaural beat at subtle level
  python vibe-os-mixer.py --music track.wav --binaural 432 6 --level subtle --output mixed.wav

  # Add subliminal 528 Hz to any song
  python vibe-os-mixer.py --music song.mp3 --hz 528 --level subliminal --output healing.wav

  # Get recommendations for creating frequency-compatible music
  python vibe-os-mixer.py --recommend theta

  # Generate Suno prompt for frequency-compatible music
  python vibe-os-mixer.py --suno-prompt gamma

Mixing Levels:
  dominant     - Frequency leads (-3 dB freq, -6 dB music)
  balanced     - Equal presence (-6 dB freq, -3 dB music)
  subtle       - Music leads, frequency adds texture (-12 dB freq)
  subliminal   - Frequency below conscious hearing (-24 dB freq) - still effective per research
  binaural_optimal - Research-optimal for entrainment (-9 dB freq)
"""
    )

    parser.add_argument("--music", "-m", type=str, help="Input music file (WAV or MP3)")
    parser.add_argument("--frequency", "-f", choices=list(BRAINWAVE_PRESETS.keys()),
                        help="Brainwave preset (theta, alpha, delta, beta, gamma, schumann)")
    parser.add_argument("--binaural", "-b", nargs=2, type=float, metavar=("CARRIER", "BEAT"),
                        help="Custom binaural beat (carrier Hz, beat Hz)")
    parser.add_argument("--hz", type=float, help="Single frequency in Hz (pure tone)")
    parser.add_argument("--isochronic", "-i", nargs=2, type=float, metavar=("FREQ", "PULSE"),
                        help="Isochronic tone (frequency Hz, pulse rate Hz)")
    parser.add_argument("--level", "-l", choices=list(MIXING_LEVELS.keys()),
                        default="binaural_optimal",
                        help="Mixing level preset (default: binaural_optimal)")
    parser.add_argument("--output", "-o", type=str, default="mixed_output.wav",
                        help="Output filename")
    parser.add_argument("--recommend", "-r", choices=list(INSTRUMENT_RECOMMENDATIONS.keys()),
                        help="Show instrument recommendations for frequency type")
    parser.add_argument("--suno-prompt", "-s", choices=list(INSTRUMENT_RECOMMENDATIONS.keys()),
                        help="Generate Suno/Hailuo prompt for frequency-compatible music")
    parser.add_argument("--list-levels", action="store_true",
                        help="List all mixing level presets")

    args = parser.parse_args()

    # Handle info commands
    if args.list_levels:
        print("\n=== MIXING LEVELS ===\n")
        for name, level in MIXING_LEVELS.items():
            print(f"{name:20} Music: {level['music_db']:+3} dB | Freq: {level['frequency_db']:+3} dB")
            print(f"{'':20} {level['description']}\n")
        return

    if args.recommend:
        print_recommendations(args.recommend)
        return

    if args.suno_prompt:
        print(f"\n=== SUNO/HAILUO PROMPT FOR {args.suno_prompt.upper()} ===\n")
        print(get_suno_prompt_for_frequency(args.suno_prompt))
        print_recommendations(args.suno_prompt)
        return

    # Require music file for mixing
    if not args.music:
        parser.print_help()
        return

    # Load music
    print(f"Loading music: {args.music}")
    music, sample_rate, channels = read_audio_file(args.music)
    duration = len(music) / sample_rate
    print(f"  Duration: {duration:.1f}s, Sample rate: {sample_rate} Hz, Channels: {channels}")

    # Generate frequency component
    if args.frequency:
        preset = BRAINWAVE_PRESETS[args.frequency]
        print(f"Using preset: {args.frequency}")
        print(f"  Carrier: {preset['carrier']} Hz, Beat: {preset['beat']} Hz")
        print(f"  Effect: {preset['effect']}")
        freq_left, freq_right = generate_binaural_beat(
            duration, preset['carrier'], preset['beat'], sample_rate
        )
    elif args.binaural:
        carrier, beat = args.binaural
        print(f"Custom binaural: {carrier} Hz carrier, {beat} Hz beat")
        freq_left, freq_right = generate_binaural_beat(duration, carrier, beat, sample_rate)
    elif args.hz:
        print(f"Pure tone: {args.hz} Hz")
        tone = generate_pure_tone(duration, args.hz, sample_rate)
        freq_left = freq_right = tone
    elif args.isochronic:
        freq, pulse = args.isochronic
        print(f"Isochronic: {freq} Hz at {pulse} Hz pulse")
        tone = generate_isochronic_tone(duration, freq, pulse, sample_rate)
        freq_left = freq_right = tone
    else:
        print("Error: Must specify --frequency, --binaural, --hz, or --isochronic")
        return

    # Get mixing levels
    level = MIXING_LEVELS[args.level]
    print(f"\nMixing level: {args.level}")
    print(f"  Music: {level['music_db']} dB, Frequency: {level['frequency_db']} dB")
    print(f"  {level['description']}")

    # Flatten music if stereo for mixing
    if music.ndim == 2:
        music_flat = music[:, 0]  # Use left channel
    else:
        music_flat = music

    # Mix
    print("\nMixing audio...")
    mixed = mix_audio(music_flat, freq_left, freq_right,
                      level['music_db'], level['frequency_db'])

    # Save
    save_wav(mixed, args.output, sample_rate)
    print(f"\nOutput: {args.output}")
    print(f"Duration: {duration/60:.1f} minutes")

    # Print usage tip
    if "binaural" in args.level or args.frequency or args.binaural:
        print("\n⚠️  IMPORTANT: Use headphones for binaural beats to work!")


if __name__ == "__main__":
    main()
