#!/usr/bin/env python3
"""
Vibe Prompt Generator - Research-Backed AI Music Prompt Creation
Part of the Vibe OS System

Generates optimized prompts for Suno, Hailuo, and Udio based on:
- Psychomusicology research on tempo, mode, and emotion
- Instrument-emotion associations from timbre research
- Lyrics psychology for affirmation and state change
- Goal-specific optimization

Usage:
    python vibe-prompt-generator.py --state focus
    python vibe-prompt-generator.py --goal "morning energy" --with-lyrics
    python vibe-prompt-generator.py --from anxious --to calm
    python vibe-prompt-generator.py --custom --bpm 120 --key "D Major" --mood triumphant
"""

import argparse
import json
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# ============================================================================
# RESEARCH-BACKED STATE LIBRARY
# ============================================================================

@dataclass
class VibeState:
    name: str
    description: str
    bpm_range: Tuple[int, int]
    optimal_bpm: int
    keys: List[str]
    mode: str  # major, minor, mixed
    instruments: List[str]
    avoid_instruments: List[str]
    timbre: str  # bright, warm, soft, powerful
    energy: str  # low, medium, high, very high
    lyric_themes: List[str]
    affirmations: List[str]
    music_styles: List[str]
    frequency_pairing: Optional[str]  # brainwave state to pair with


VIBE_STATES: Dict[str, VibeState] = {
    # ========== ENERGY STATES ==========
    "morning_energy": VibeState(
        name="Morning Energy",
        description="Energizing wake-up music to start the day with positivity",
        bpm_range=(110, 130),
        optimal_bpm=120,
        keys=["G Major", "D Major", "A Major"],
        mode="major",
        instruments=["acoustic guitar", "piano", "light percussion", "strings"],
        avoid_instruments=["heavy bass", "distorted guitar", "aggressive drums"],
        timbre="bright",
        energy="medium-high",
        lyric_themes=["new beginnings", "possibility", "gratitude", "rising sun", "fresh start"],
        affirmations=[
            "Today is full of possibility",
            "I rise with energy and purpose",
            "Every morning is a new beginning",
            "I am ready for whatever comes"
        ],
        music_styles=["indie folk", "acoustic pop", "uplifting acoustic", "morning acoustic"],
        frequency_pairing="alpha"
    ),

    "high_energy": VibeState(
        name="High Energy",
        description="Peak energy for workouts, challenges, and maximum drive",
        bpm_range=(140, 170),
        optimal_bpm=150,
        keys=["E Major", "D Major", "B Major"],
        mode="major",
        instruments=["driving drums", "synth bass", "power chords", "brass"],
        avoid_instruments=["soft piano", "acoustic guitar", "ambient pads"],
        timbre="powerful",
        energy="very high",
        lyric_themes=["power", "unstoppable", "warrior", "victory", "strength"],
        affirmations=[
            "I am unstoppable",
            "Nothing can hold me back",
            "I have limitless power within",
            "I push through every barrier"
        ],
        music_styles=["electronic", "EDM", "power pop", "workout anthem", "epic"],
        frequency_pairing="beta"
    ),

    "workout": VibeState(
        name="Workout Power",
        description="Optimal exercise music based on sports psychology research",
        bpm_range=(130, 160),
        optimal_bpm=145,  # Research ceiling effect
        keys=["D Major", "E Major", "G Major"],
        mode="major",
        instruments=["driving drums", "synth", "bass", "electronic elements"],
        avoid_instruments=["ballad piano", "soft strings", "ambient"],
        timbre="bright",
        energy="high",
        lyric_themes=["strength", "endurance", "pushing limits", "victory", "power"],
        affirmations=[
            "I am getting stronger",
            "Pain is temporary, glory is forever",
            "I can do one more",
            "My body is powerful"
        ],
        music_styles=["workout EDM", "power pop", "hip hop beats", "electronic anthem"],
        frequency_pairing="beta"
    ),

    # ========== FOCUS STATES ==========
    "deep_focus": VibeState(
        name="Deep Focus",
        description="Sustained concentration for knowledge work and study",
        bpm_range=(80, 100),
        optimal_bpm=90,
        keys=["C Major", "G Major", "F Major"],
        mode="major",
        instruments=["ambient synth pads", "soft piano", "minimal percussion", "nature sounds"],
        avoid_instruments=["vocals", "complex drums", "brass", "heavy bass"],
        timbre="warm",
        energy="low-medium",
        lyric_themes=[],  # Instrumental preferred for focus
        affirmations=[],
        music_styles=["lo-fi", "ambient", "study music", "concentration", "minimal"],
        frequency_pairing="alpha"
    ),

    "creative_flow": VibeState(
        name="Creative Flow",
        description="Inspiration and creative exploration",
        bpm_range=(90, 115),
        optimal_bpm=100,
        keys=["A Major", "E Major", "D Major"],
        mode="major",
        instruments=["piano", "strings", "light electronic", "acoustic guitar", "bells"],
        avoid_instruments=["aggressive drums", "distortion", "heavy bass"],
        timbre="bright",
        energy="medium",
        lyric_themes=["imagination", "possibility", "creation", "vision", "dreams"],
        affirmations=[
            "Ideas flow through me effortlessly",
            "I am a channel for creativity",
            "My imagination knows no bounds",
            "Every creation is a gift"
        ],
        music_styles=["cinematic", "inspirational", "neoclassical", "ambient pop"],
        frequency_pairing="theta"
    ),

    # ========== CALM STATES ==========
    "relaxation": VibeState(
        name="Deep Relaxation",
        description="Stress relief and nervous system regulation",
        bpm_range=(60, 80),
        optimal_bpm=70,
        keys=["F Major", "C Major", "G Major"],
        mode="major",
        instruments=["soft piano", "strings", "ambient pads", "nature sounds", "harp"],
        avoid_instruments=["drums", "bass", "brass", "electronic"],
        timbre="soft",
        energy="low",
        lyric_themes=["peace", "safety", "letting go", "breath", "stillness"],
        affirmations=[
            "I release all tension",
            "I am safe and at peace",
            "With every breath I relax deeper",
            "Calm flows through me"
        ],
        music_styles=["ambient", "spa", "meditation", "new age", "peaceful piano"],
        frequency_pairing="alpha"
    ),

    "meditation": VibeState(
        name="Meditation",
        description="Deep meditative states and mindfulness",
        bpm_range=(50, 70),
        optimal_bpm=60,
        keys=["D Minor", "A Minor", "F Major"],
        mode="mixed",
        instruments=["singing bowls", "ambient drones", "soft pads", "nature sounds", "flute"],
        avoid_instruments=["drums", "guitar", "bass", "brass"],
        timbre="soft",
        energy="very low",
        lyric_themes=["presence", "breath", "awareness", "stillness", "being"],
        affirmations=[
            "I am present in this moment",
            "I observe without judgment",
            "Peace is my natural state",
            "I am connected to all that is"
        ],
        music_styles=["meditation", "ambient", "drone", "tibetan", "zen"],
        frequency_pairing="theta"
    ),

    "sleep": VibeState(
        name="Sleep Preparation",
        description="Wind-down music for restful sleep",
        bpm_range=(40, 60),
        optimal_bpm=50,
        keys=["D Minor", "A Minor", "F Major"],
        mode="minor",
        instruments=["very soft piano", "ambient drones", "nature sounds", "minimal strings"],
        avoid_instruments=["any percussion", "brass", "electronic", "vocals"],
        timbre="soft",
        energy="very low",
        lyric_themes=["rest", "surrender", "dreams", "night", "peace"],
        affirmations=[
            "I surrender to rest",
            "Sleep comes easily to me",
            "I release this day with gratitude",
            "My body knows how to heal"
        ],
        music_styles=["sleep ambient", "dark ambient", "drone", "ASMR music"],
        frequency_pairing="delta"
    ),

    # ========== EMOTIONAL STATES ==========
    "confidence": VibeState(
        name="Confidence Boost",
        description="Build self-assurance and personal power",
        bpm_range=(115, 140),
        optimal_bpm=128,
        keys=["D Major", "A Major", "E Major"],
        mode="major",
        instruments=["piano", "brass", "strings", "drums", "synth"],
        avoid_instruments=["soft acoustic", "ambient"],
        timbre="powerful",
        energy="high",
        lyric_themes=["power", "self-belief", "capability", "rising", "unstoppable"],
        affirmations=[
            "I am worthy of success",
            "I believe in myself completely",
            "I walk with confidence",
            "My presence is powerful"
        ],
        music_styles=["anthemic", "power ballad", "inspirational pop", "epic orchestral"],
        frequency_pairing="beta"
    ),

    "gratitude": VibeState(
        name="Gratitude",
        description="Cultivate appreciation and positive reflection",
        bpm_range=(80, 100),
        optimal_bpm=90,
        keys=["G Major", "C Major", "F Major"],
        mode="major",
        instruments=["acoustic guitar", "piano", "soft strings", "light percussion"],
        avoid_instruments=["electronic", "heavy drums", "bass"],
        timbre="warm",
        energy="medium",
        lyric_themes=["thankfulness", "blessings", "abundance", "appreciation", "love"],
        affirmations=[
            "I am grateful for this moment",
            "Abundance flows to me",
            "I appreciate all that I have",
            "My life is full of blessings"
        ],
        music_styles=["acoustic folk", "indie folk", "soft pop", "worship"],
        frequency_pairing="alpha"
    ),

    "emotional_release": VibeState(
        name="Emotional Release",
        description="Process and release difficult emotions safely",
        bpm_range=(60, 85),
        optimal_bpm=72,
        keys=["A Minor", "E Minor", "D Minor"],
        mode="minor",
        instruments=["piano", "strings", "cello", "soft vocals"],
        avoid_instruments=["electronic", "drums", "brass"],
        timbre="warm",
        energy="low-medium",
        lyric_themes=["letting go", "feeling", "acceptance", "healing", "tears"],
        affirmations=[
            "It is safe to feel",
            "I release what no longer serves me",
            "My emotions are valid",
            "Healing happens through feeling"
        ],
        music_styles=["sad piano", "emotional ballad", "ambient", "cinematic sad"],
        frequency_pairing="theta"
    ),

    "joy": VibeState(
        name="Pure Joy",
        description="Celebrate and amplify happiness",
        bpm_range=(120, 145),
        optimal_bpm=130,
        keys=["D Major", "G Major", "A Major"],
        mode="major",
        instruments=["bright piano", "acoustic guitar", "strings", "light percussion", "claps"],
        avoid_instruments=["minor sounds", "drones", "heavy bass"],
        timbre="bright",
        energy="high",
        lyric_themes=["happiness", "celebration", "freedom", "dancing", "love"],
        affirmations=[
            "Joy is my natural state",
            "I celebrate this moment",
            "Happiness flows through me",
            "Life is beautiful"
        ],
        music_styles=["uplifting pop", "indie dance", "feel-good", "celebration"],
        frequency_pairing="gamma"
    ),

    # ========== GOAL STATES ==========
    "manifestation": VibeState(
        name="Manifestation",
        description="Visualize and attract desired outcomes",
        bpm_range=(90, 110),
        optimal_bpm=100,
        keys=["E Major", "A Major", "D Major"],
        mode="major",
        instruments=["ethereal synths", "strings", "piano", "bells", "soft vocals"],
        avoid_instruments=["aggressive drums", "distortion"],
        timbre="bright",
        energy="medium",
        lyric_themes=["dreams", "vision", "attraction", "becoming", "possibility"],
        affirmations=[
            "I am becoming who I'm meant to be",
            "My dreams are manifesting",
            "I attract what I focus on",
            "The universe supports my vision"
        ],
        music_styles=["cinematic", "inspirational", "ethereal pop", "new age"],
        frequency_pairing="alpha"
    ),

    "courage": VibeState(
        name="Courage",
        description="Face fears and take bold action",
        bpm_range=(100, 130),
        optimal_bpm=115,
        keys=["D Major", "G Major", "C Major"],
        mode="major",
        instruments=["drums", "strings", "brass", "piano", "choir"],
        avoid_instruments=["soft ambient", "minimal"],
        timbre="powerful",
        energy="high",
        lyric_themes=["bravery", "facing fears", "rising", "warrior", "strength"],
        affirmations=[
            "I face my fears with courage",
            "I am braver than I know",
            "Fear does not control me",
            "I take bold action"
        ],
        music_styles=["epic", "cinematic", "orchestral", "heroic"],
        frequency_pairing="beta"
    ),

    "healing": VibeState(
        name="Healing",
        description="Support physical and emotional healing",
        bpm_range=(55, 75),
        optimal_bpm=65,
        keys=["F Major", "C Major", "G Major"],
        mode="major",
        instruments=["singing bowls", "soft piano", "harp", "nature sounds", "strings"],
        avoid_instruments=["drums", "bass", "electronic", "brass"],
        timbre="soft",
        energy="low",
        lyric_themes=["healing", "wholeness", "restoration", "love", "light"],
        affirmations=[
            "My body knows how to heal",
            "Healing energy flows through me",
            "I am whole and complete",
            "Love heals all wounds"
        ],
        music_styles=["healing ambient", "spa", "sound healing", "peaceful"],
        frequency_pairing="theta"
    ),
}

# ============================================================================
# STATE TRANSITIONS (ISO PRINCIPLE)
# ============================================================================

STATE_TRANSITIONS = {
    ("anxious", "calm"): {
        "approach": "iso_principle",
        "stages": [
            {"bpm": 110, "key": "A Minor", "duration": "2min"},
            {"bpm": 90, "key": "D Minor", "duration": "2min"},
            {"bpm": 75, "key": "G Major", "duration": "2min"},
            {"bpm": 65, "key": "F Major", "duration": "4min"}
        ]
    },
    ("tired", "energized"): {
        "approach": "gradual_build",
        "stages": [
            {"bpm": 80, "key": "G Major", "duration": "2min"},
            {"bpm": 100, "key": "D Major", "duration": "2min"},
            {"bpm": 120, "key": "A Major", "duration": "3min"},
            {"bpm": 140, "key": "E Major", "duration": "3min"}
        ]
    },
    ("sad", "hopeful"): {
        "approach": "iso_principle",
        "stages": [
            {"bpm": 65, "key": "A Minor", "duration": "3min"},
            {"bpm": 75, "key": "E Minor", "duration": "2min"},
            {"bpm": 85, "key": "C Major", "duration": "3min"},
            {"bpm": 95, "key": "G Major", "duration": "2min"}
        ]
    },
    ("scattered", "focused"): {
        "approach": "simplification",
        "stages": [
            {"bpm": 100, "key": "varies", "texture": "complex", "duration": "2min"},
            {"bpm": 95, "key": "G Major", "texture": "medium", "duration": "2min"},
            {"bpm": 90, "key": "C Major", "texture": "simple", "duration": "6min"}
        ]
    }
}

# ============================================================================
# PROMPT GENERATION
# ============================================================================

def generate_suno_prompt(state: VibeState, include_lyrics: bool = True) -> str:
    """Generate optimized Suno/Hailuo prompt for a state."""

    # Select random elements from the state
    key = random.choice(state.keys)
    style = random.choice(state.music_styles)
    instruments = random.sample(state.instruments, min(3, len(state.instruments)))

    # Build the prompt
    prompt_parts = [
        f"{style}",
        f"{state.optimal_bpm} BPM",
        f"{key}",
        f"{', '.join(instruments)}",
    ]

    # Add timbre description
    timbre_map = {
        "bright": "bright and uplifting",
        "warm": "warm and comforting",
        "soft": "soft and gentle",
        "powerful": "powerful and driving"
    }
    prompt_parts.append(timbre_map.get(state.timbre, state.timbre))

    # Add energy description
    energy_map = {
        "very low": "very peaceful, minimal",
        "low": "calm and relaxed",
        "low-medium": "gently flowing",
        "medium": "balanced energy",
        "medium-high": "building momentum",
        "high": "energetic and driving",
        "very high": "explosive energy, intense"
    }
    prompt_parts.append(energy_map.get(state.energy, ""))

    # Add avoid instructions
    if state.avoid_instruments:
        prompt_parts.append(f"no {', '.join(state.avoid_instruments[:2])}")

    prompt = ", ".join([p for p in prompt_parts if p])

    return prompt


def generate_lyrics_prompt(state: VibeState) -> str:
    """Generate lyrics prompt based on state themes and affirmations."""

    themes = random.sample(state.lyric_themes, min(3, len(state.lyric_themes)))

    if state.affirmations:
        affirmation = random.choice(state.affirmations)
        return f"""Lyrics themes: {', '.join(themes)}
Core message: {affirmation}
Tone: {state.timbre}, {state.energy} energy
Style: {random.choice(state.music_styles)}"""
    else:
        return f"Instrumental - no lyrics (optimal for {state.name})"


def generate_full_prompt(state: VibeState, include_lyrics: bool = True) -> dict:
    """Generate complete prompt package."""

    music_prompt = generate_suno_prompt(state, include_lyrics)
    lyrics_prompt = generate_lyrics_prompt(state) if include_lyrics else None

    # Frequency pairing recommendation
    freq_info = None
    if state.frequency_pairing:
        freq_map = {
            "delta": "2 Hz binaural (deep sleep)",
            "theta": "6 Hz binaural (meditation)",
            "alpha": "10 Hz binaural (calm focus)",
            "beta": "18 Hz binaural (alertness)",
            "gamma": "40 Hz binaural (peak cognition)"
        }
        freq_info = freq_map.get(state.frequency_pairing)

    return {
        "state": state.name,
        "description": state.description,
        "music_prompt": music_prompt,
        "lyrics_prompt": lyrics_prompt,
        "bpm": state.optimal_bpm,
        "key": random.choice(state.keys),
        "frequency_pairing": freq_info,
        "recommended_duration": "3-10 minutes"
    }


def list_states():
    """List all available states."""
    print("\n" + "="*60)
    print("VIBE OS STATE LIBRARY")
    print("="*60 + "\n")

    categories = {
        "Energy": ["morning_energy", "high_energy", "workout"],
        "Focus": ["deep_focus", "creative_flow"],
        "Calm": ["relaxation", "meditation", "sleep"],
        "Emotional": ["confidence", "gratitude", "emotional_release", "joy"],
        "Goals": ["manifestation", "courage", "healing"]
    }

    for category, states in categories.items():
        print(f"\n### {category.upper()} ###")
        for state_key in states:
            state = VIBE_STATES[state_key]
            print(f"  {state_key:20} - {state.description}")

    print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Vibe Prompt Generator - Research-Backed AI Music Prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get prompt for a specific state
  python vibe-prompt-generator.py --state focus

  # State with lyrics
  python vibe-prompt-generator.py --state confidence --with-lyrics

  # State transition (anxious to calm)
  python vibe-prompt-generator.py --from anxious --to calm

  # List all available states
  python vibe-prompt-generator.py --list

  # Custom prompt
  python vibe-prompt-generator.py --custom --bpm 120 --key "D Major" --mood triumphant

Available States:
  morning_energy, high_energy, workout, deep_focus, creative_flow,
  relaxation, meditation, sleep, confidence, gratitude, emotional_release,
  joy, manifestation, courage, healing
"""
    )

    parser.add_argument("--state", "-s", type=str, help="Target emotional state")
    parser.add_argument("--with-lyrics", "-l", action="store_true", help="Include lyrics prompt")
    parser.add_argument("--from", dest="from_state", type=str, help="Starting emotional state")
    parser.add_argument("--to", type=str, help="Target emotional state")
    parser.add_argument("--list", action="store_true", help="List all available states")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--custom", action="store_true", help="Custom prompt mode")
    parser.add_argument("--bpm", type=int, help="Custom BPM")
    parser.add_argument("--key", type=str, help="Custom key (e.g., 'D Major')")
    parser.add_argument("--mood", type=str, help="Custom mood description")

    args = parser.parse_args()

    if args.list:
        list_states()
        return

    if args.state:
        state_key = args.state.lower().replace(" ", "_").replace("-", "_")
        if state_key not in VIBE_STATES:
            print(f"Unknown state: {args.state}")
            print("Use --list to see available states")
            return

        state = VIBE_STATES[state_key]
        result = generate_full_prompt(state, args.with_lyrics)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"VIBE: {result['state'].upper()}")
            print(f"{'='*60}")
            print(f"\n{result['description']}\n")
            print(f"--- SUNO/HAILUO PROMPT ---")
            print(result['music_prompt'])
            if result['lyrics_prompt']:
                print(f"\n--- LYRICS GUIDANCE ---")
                print(result['lyrics_prompt'])
            print(f"\n--- PARAMETERS ---")
            print(f"BPM: {result['bpm']}")
            print(f"Key: {result['key']}")
            if result['frequency_pairing']:
                print(f"Frequency Pairing: {result['frequency_pairing']}")
            print(f"{'='*60}\n")

    elif args.from_state and args.to:
        print("\n[State transition prompts - coming in v2.0]")
        print(f"From: {args.from_state} → To: {args.to}")
        print("Use the ISO Principle: start with music matching current state,")
        print("then gradually shift tempo, mode, and energy toward target state.\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
