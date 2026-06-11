#!/usr/bin/env python3
"""
Vibe OS MCP Server

Exposes the Vibe OS research-backed music tools to any MCP client
(Claude Code, Claude Desktop, Cursor, etc.) as structured tools:

- list_vibe_states            — the research-backed state library
- generate_vibe_prompt        — state -> optimized Suno/Hailuo/Udio prompt
- generate_transition_prompt  — ISO-principle state transitions (e.g. anxious -> calm)
- generate_custom_prompt      — custom BPM/key/mood prompt
- list_frequency_presets      — brainwave, solfeggio, and session presets with evidence notes
- design_frequency_session    — session parameters (+ optional WAV render)
- plan_session_mix            — multi-state listening session plan

The underlying logic lives in tools/*.py (research-backed, CLI-first).
This server wraps those modules without modifying them.

Run:
    pip install -r mcp-server/requirements.txt
    python mcp-server/server.py
"""

import importlib.util
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"


def _load_module(name: str, filename: str):
    """Load a hyphenated tool script as a module (tools/*.py are CLI scripts)."""
    spec = importlib.util.spec_from_file_location(name, TOOLS_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


vibe_gen = _load_module("vibe_prompt_generator", "vibe-prompt-generator.py")
freq_gen = _load_module("frequency_generator_pro", "frequency-generator-pro.py")

mcp = FastMCP("vibe-os")

STATE_CATEGORIES = {
    "energy": ["morning_energy", "high_energy", "workout"],
    "focus": ["deep_focus", "creative_flow"],
    "calm": ["relaxation", "meditation", "sleep"],
    "emotional": ["confidence", "gratitude", "emotional_release", "joy"],
    "goals": ["manifestation", "courage", "healing"],
}


def _state_or_error(state: str):
    key = state.lower().strip().replace(" ", "_").replace("-", "_")
    if key not in vibe_gen.VIBE_STATES:
        available = ", ".join(sorted(vibe_gen.VIBE_STATES))
        raise ValueError(f"Unknown state '{state}'. Available states: {available}")
    return key, vibe_gen.VIBE_STATES[key]


@mcp.tool()
def list_vibe_states() -> dict:
    """List the research-backed Vibe OS state library: every target state with its
    tempo, mode, key, instrumentation, energy, and brainwave-pairing parameters."""
    states = {}
    for key, s in vibe_gen.VIBE_STATES.items():
        category = next((c for c, ks in STATE_CATEGORIES.items() if key in ks), "other")
        states[key] = {
            "name": s.name,
            "category": category,
            "description": s.description,
            "optimal_bpm": s.optimal_bpm,
            "bpm_range": list(s.bpm_range),
            "keys": s.keys,
            "mode": s.mode,
            "instruments": s.instruments,
            "avoid_instruments": s.avoid_instruments,
            "timbre": s.timbre,
            "energy": s.energy,
            "music_styles": s.music_styles,
            "frequency_pairing": s.frequency_pairing,
        }
    return {"count": len(states), "states": states}


@mcp.tool()
def generate_vibe_prompt(state: str, with_lyrics: bool = True) -> dict:
    """Generate a research-optimized AI music prompt (Suno/Hailuo/Udio) for a target
    state, e.g. 'deep_focus', 'morning_energy', 'meditation'. Returns the music
    prompt, optional lyrics prompt, BPM, key, and frequency pairing."""
    _, s = _state_or_error(state)
    return vibe_gen.generate_full_prompt(s, include_lyrics=with_lyrics)


@mcp.tool()
def generate_transition_prompt(from_state: str, to_state: str) -> dict:
    """Generate a staged ISO-principle transition plan between emotional states
    (matching the listener's current state, then gradually shifting). Known
    transitions: anxious->calm, tired->energized, sad->hopeful, scattered->focused.
    For other pairs, to_state must be a library state; from_state is free-text
    describing the listener's current state (the ISO principle starts where the
    listener is, which need not be a library state)."""
    key = (from_state.lower().strip(), to_state.lower().strip())
    transitions = vibe_gen.STATE_TRANSITIONS
    if key in transitions:
        t = transitions[key]
        stages = []
        for i, stage in enumerate(t["stages"], 1):
            parts = [f"{stage['bpm']} BPM"]
            if stage.get("key") and stage["key"] != "varies":
                parts.append(stage["key"])
            if stage.get("texture"):
                parts.append(f"{stage['texture']} texture")
            stages.append({
                "stage": i,
                "duration": stage["duration"],
                "parameters": stage,
                "prompt_fragment": ", ".join(parts),
            })
        return {
            "from": from_state,
            "to": to_state,
            "approach": t["approach"],
            "stages": stages,
            "note": "Generate one track per stage, or use Suno Extend with these parameters per section.",
        }
    # Derive a generic plan: to_state from the library, from_state as described
    try:
        _, target = _state_or_error(to_state)
    except ValueError:
        known = ", ".join(f"{a}->{b}" for a, b in transitions)
        raise ValueError(
            f"No transition for {from_state}->{to_state} and '{to_state}' is not a "
            f"library state. Known transitions: {known}"
        )
    end = vibe_gen.generate_full_prompt(target, include_lyrics=False)
    return {
        "from": from_state,
        "to": to_state,
        "approach": "derived_two_stage",
        "stages": [
            {"stage": 1, "duration": "3min",
             "prompt_fragment": f"bridge from {from_state}: mid-tempo, {target.mode} leaning"},
            {"stage": 2, "duration": "6min", "parameters": end,
             "prompt_fragment": end["music_prompt"]},
        ],
        "note": "Derived plan (no researched transition for this pair). "
                "Start near the listener's current state per the ISO principle.",
    }


@mcp.tool()
def generate_custom_prompt(bpm: int, key: str, mood: str, with_lyrics: bool = False) -> dict:
    """Generate a custom AI music prompt from explicit parameters: BPM, musical key
    (e.g. 'D Major'), and a mood description (e.g. 'triumphant')."""
    parts = [mood, f"{bpm} BPM", key]
    mode = "major" if "major" in key.lower() else ("minor" if "minor" in key.lower() else "unspecified")
    result = {
        "music_prompt": ", ".join(parts) + ", professional production, clear mix",
        "bpm": bpm,
        "key": key,
        "mode": mode,
        "mood": mood,
    }
    if with_lyrics:
        result["lyrics_prompt"] = (
            f"Lyrics themes drawn from: {mood}. Tone matches {key} at {bpm} BPM. "
            "First person, present tense, concrete imagery."
        )
    return result


@mcp.tool()
def list_frequency_presets() -> dict:
    """List frequency-session presets: brainwave entrainment bands (delta..gamma),
    evidence-backed frequencies (432/528/40 Hz with citations), solfeggio set
    (marked anecdotal), and curated session presets."""
    freq = freq_gen
    return {
        "brainwave_bands": freq.BRAINWAVE_PRESETS,
        "evidence_based": freq.EVIDENCE_BASED,
        "solfeggio_anecdotal": {str(k): v for k, v in freq.SOLFEGGIO.items()},
        "session_presets": freq.SESSION_PRESETS,
        "evidence_note": "Solfeggio entries are anecdotal tradition; brainwave "
                         "entrainment and 432/528/40 Hz entries cite preliminary studies. "
                         "See docs/frequency-healing-research.md for sources.",
    }


@mcp.tool()
def design_frequency_session(
    session_type: str = "binaural",
    carrier_freq: float = 432.0,
    beat_freq: float = 10.0,
    duration_seconds: int = 600,
    preset: str = "",
    output_path: str = "",
) -> dict:
    """Design a frequency session (binaural beat or isochronic tone). Pass a preset
    name from list_frequency_presets (e.g. 'deep-meditation', 'stress-relief') OR
    explicit parameters. Layered presets mix a base frequency (e.g. 528 Hz) under
    the binaural beat. If output_path is set, renders a WAV file there; otherwise
    returns parameters only."""
    freq = freq_gen
    base_freq = None
    harmonics = False
    if preset:
        if preset not in freq.SESSION_PRESETS:
            raise ValueError(f"Unknown preset '{preset}'. Available: {', '.join(freq.SESSION_PRESETS)}")
        p = freq.SESSION_PRESETS[preset]
        session_type = p["type"]
        carrier_freq = float(p.get("carrier", carrier_freq))
        beat_freq = float(p.get("beat", beat_freq))
        duration_seconds = int(p.get("duration", duration_seconds))
        harmonics = bool(p.get("harmonics", False))
        if session_type == "layered":
            base_freq = float(p.get("base_freq", 528.0))

    band = next(
        (name for name, b in freq.BRAINWAVE_PRESETS.items()
         if b["range"][0] <= beat_freq <= b["range"][1]),
        "outside standard bands",
    )
    result = {
        "session_type": session_type,
        "carrier_freq_hz": carrier_freq,
        "beat_freq_hz": beat_freq,
        "brainwave_band": band,
        "duration_seconds": duration_seconds,
        "listening_note": "Binaural beats require stereo headphones; "
                          "isochronic tones work on speakers.",
    }
    if base_freq is not None:
        result["base_freq_hz"] = base_freq
    if output_path:
        config = freq.QUALITY_CONFIGS[freq.AudioQuality.HIGH]
        out = Path(output_path).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        if session_type == "isochronic":
            audio = freq.generate_isochronic(carrier_freq, beat_freq, duration_seconds,
                                             config.sample_rate)
            freq.save_wav(audio, str(out), config, stereo=False)
        else:
            left, right = freq.generate_binaural(carrier_freq, beat_freq, duration_seconds,
                                                 config.sample_rate)
            if base_freq is not None:
                if harmonics:
                    base = freq.generate_with_harmonics(base_freq, duration_seconds,
                                                        config.sample_rate, "warm")
                else:
                    base = freq.generate_sine(base_freq, duration_seconds, config.sample_rate)
                left = 0.6 * base + 0.4 * left
                right = 0.6 * base + 0.4 * right
            freq.save_wav(left, str(out), config, stereo=True, left=left, right=right)
        result["wav_file"] = str(out)
    return result


@mcp.tool()
def plan_session_mix(states: list[str], minutes_per_state: int = 10) -> dict:
    """Plan a multi-state listening session: an ordered sequence of states
    (e.g. ['relaxation', 'deep_focus']) with a generated prompt and frequency
    pairing per segment, ready for AI music generation plus frequency layering."""
    if not states:
        raise ValueError("Provide at least one state, e.g. ['deep_focus']")
    segments = []
    for i, name in enumerate(states, 1):
        _, s = _state_or_error(name)
        pkg = vibe_gen.generate_full_prompt(s, include_lyrics=False)
        segments.append({
            "segment": i,
            "state": name,
            "minutes": minutes_per_state,
            "music_prompt": pkg["music_prompt"],
            "bpm": pkg["bpm"],
            "key": pkg["key"],
            "frequency_pairing": pkg["frequency_pairing"],
        })
    return {
        "total_minutes": minutes_per_state * len(segments),
        "segments": segments,
        "mixing_note": "Crossfade 2s between segments (see tools/vibe-os-mixer.py). "
                       "Layer the paired frequency at -20 dB under the music.",
    }


if __name__ == "__main__":
    mcp.run()
