# Vibe OS Production System
*Complete Guide to AI-Assisted Music Production with Tones and Binaural Beats*
*January 2025*

---

## System Overview

The Vibe OS Production System combines:
1. **Frequency Generation** - Pure tones, binaural beats, and isochronic tones
2. **AI Music Generation** - Suno, Hailuo/MiniMax, Udio APIs
3. **Intelligent Mixing** - Preset level blending
4. **Agent Orchestration** - Specialized agents for each phase

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIBE OS PRODUCTION PIPELINE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   SONIC     │    │  FREQUENCY  │    │    SONIC    │        │
│  │  ARCHITECT  │ →  │  ENGINEER   │ →  │  ALCHEMIST  │        │
│  │             │    │             │    │             │        │
│  │ AI Music    │    │ Hz Tones    │    │ Mix & Master│        │
│  │ Prompts     │    │ Binaural    │    │ Levels      │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│        ↓                  ↓                  ↓                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │ Suno/Hailuo │    │ frequency-  │    │ vibe-os-    │        │
│  │ /Udio API   │    │ generator-  │    │ mixer.py    │        │
│  │             │    │ pro.py      │    │             │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│        ↓                  ↓                  ↓                 │
│        └──────────────────┴──────────────────┘                 │
│                          ↓                                     │
│                  ┌─────────────┐                               │
│                  │ FINAL       │                               │
│                  │ MIXED AUDIO │                               │
│                  │ (WAV/MP3)   │                               │
│                  └─────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Available Tools

### 1. frequency-generator-pro.py
**Location**: `~/.claude/tools/frequency-generator-pro.py`
**Purpose**: Generate pure tones, binaural beats, isochronic tones

```bash
# Pure 432 Hz tone
python frequency-generator-pro.py --freq 432 --duration 180 --quality high

# Theta binaural beat
python frequency-generator-pro.py --binaural 432 6 --duration 300 --quality high

# Research-backed preset
python frequency-generator-pro.py --preset theta --duration 600 --output theta_session.wav
```

### 2. vibe-os-mixer.py
**Location**: `~/.claude/tools/vibe-os-mixer.py`
**Purpose**: Combine AI music with tones and binaural beats

```bash
# Mix music with theta binaural
python vibe-os-mixer.py --music track.mp3 --frequency theta --output meditation.wav

# Low-level 528 Hz layer in any song
python vibe-os-mixer.py --music song.mp3 --hz 528 --level subliminal --output toned.wav

# Get Suno prompt for frequency-compatible music
python vibe-os-mixer.py --suno-prompt theta

# View instrument recommendations
python vibe-os-mixer.py --recommend alpha
```

---

## AI Music APIs

### Option 1: MiniMax/Hailuo (Recommended)
**Status**: Official API available
**Best For**: Full compositions with vocals, up to 5 minutes

```
API: platform.minimax.io
Features:
- Music 2.0 (October 2025): Full songs with vocals
- Supports all genres
- Duets and a cappella
- Multi-instrument control
- Free tier available (3 songs)
```

### Option 2: Suno (Third-Party)
**Status**: No official API, third-party options
**Best For**: Quick generation, diverse styles

```
Third-Party APIs:
- sunoapi.org - Stable, affordable
- gcui-art/suno-api (GitHub) - Self-hosted
- aimlapi.com - Multi-model platform

Models: V4, V4.5, V5 (Pro tier)
```

### Option 3: Udio
**Status**: Third-party APIs
**Best For**: Complex instrumental arrangements

```
Third-Party APIs:
- musicapi.ai - Full feature access
- udioapi.pro - Budget option

Models: V1.0, V1.5, V1.5 Allegro
Output: 320kbps MP3
```

---

## Mixing Levels (Research-Based)

| Level | Music dB | Freq dB | Use Case |
|-------|----------|---------|----------|
| `dominant` | -6 | -3 | Frequency meditation, tone focus |
| `balanced` | -3 | -6 | Equal music/frequency experience |
| `subtle` | 0 | -12 | Music-forward with frequency texture |
| `subliminal` | 0 | -24 | Frequency layer intended to sit below conscious hearing |
| `binaural_optimal` | -3 | -9 | Preset used in these workflows (not an established optimum) |

### Research Notes

**Subliminal level**: one cited study (PMC10196448) reports effects from binaural beats presented below conscious hearing. That is a single report, and it does not remove placebo as an explanation.

**Volume**: the cited studies used about 40 dB, a comfortable listening level.

**Duration**: the cited sources used sessions of 8 minutes or more, so the workflows below use that as a minimum.

---

## Instrument Recommendations

### For Theta (4-8 Hz) - Meditation
```
Best: singing bowls, ambient pads, soft strings, flute
Avoid: drums, bass-heavy, fast tempo
Tempo: 50-70 BPM
Key: D minor, F major
```

### For Alpha (8-13 Hz) - Focus
```
Best: acoustic guitar, piano, light percussion, nature
Avoid: distortion, sudden changes
Tempo: 60-80 BPM
Key: G major, C major
```

### For Delta (0.5-4 Hz) - Sleep
```
Best: deep drones, whale sounds, very slow strings, rain
Avoid: any sudden sounds, high frequencies
Tempo: 40-60 BPM or beatless
Key: Low register, minimal movement
```

### For Gamma (30-100 Hz) - Cognition
```
Best: bright synths, crystal bowls, bells, light electronic
Avoid: muddy sounds, heavy compression
Tempo: 80-120 BPM
Key: E major, A major
```

### For 432 Hz - Universal Calm
```
Best: strings, piano, singing bowls, choir
Avoid: harsh digital sounds
Tempo: Any
Key: Natural tuning
```

### For 528 Hz - Love frequency (traditional name)
```
Best: crystal singing bowl, harp, soft vocals, nature
Avoid: dissonance, aggressive sounds
Tempo: 60-90 BPM
Key: C major (528 Hz = C5)
```

---

## Suno/Hailuo Prompt Templates

### Theta Meditation
```
Ambient meditation music, 60 BPM, soft ethereal pads,
gentle singing bowl textures, spacious reverb, no drums,
D minor, peaceful and introspective, float through space
```

### Alpha Focus
```
Relaxing acoustic instrumental, 70 BPM, soft piano and
gentle guitar, nature sounds, calming and peaceful, G major,
light atmospheric textures, mindfulness background
```

### Delta Sleep
```
Deep sleep ambient drone, 50 BPM, very low frequencies,
ocean waves, distant whale sounds, extremely peaceful,
minimal harmonic movement, sleep inducing, dark ambient
```

### Gamma Performance
```
Uplifting electronic ambient, 100 BPM, bright crystalline
synths, subtle energy, clarity and focus, E major,
inspiring and awakening, light percussion
```

### 528 Hz Healing
```
528 Hz love frequency music, healing ambient,
crystal singing bowls in C, soft harp arpeggios,
heart opening, gentle nature sounds, deeply peaceful
```

---

## Agent Roles

### Sonic Architect
**Trigger**: "sonic architect", "suno prompt", "music for meditation"
**Role**: Designs AI music prompts optimized for frequency integration

### Frequency Engineer
**Trigger**: "hz", "binaural", "solfeggio", "healing frequency"
**Role**: Generates tones using frequency-generator-pro.py

### Sonic Alchemist
**Trigger**: "mix", "layer", "combine", "subliminal"
**Role**: Combines music + frequencies at preset levels

### Music API Integrator
**Trigger**: "suno api", "hailuo api", "generate music"
**Role**: Handles API integration with music services

### Vibe Architect
**Trigger**: "vibe os", "session design", "mood arc"
**Role**: Plans complete session structure and flow

### Vibe Creator
**Trigger**: "create vibe", "meditation track"
**Role**: Executes the full production workflow

---

## Example Workflows

### Workflow 1: Meditation Track (Automated)

```bash
# 1. Generate frequency component
python frequency-generator-pro.py --preset theta --duration 600 --output theta_tone.wav

# 2. Get optimal Suno prompt
python vibe-os-mixer.py --suno-prompt theta
# → Use output to generate track via Suno/Hailuo

# 3. Mix together
python vibe-os-mixer.py --music suno_track.mp3 --frequency theta \
  --level binaural_optimal --output final_meditation.wav
```

### Workflow 2: Low-level tone layer (any song)

```bash
# Add a low-level 528 Hz layer to any existing song
python vibe-os-mixer.py --music favorite_song.mp3 --hz 528 \
  --level subliminal --output toned_version.wav
```

### Workflow 3: Full Production Session

```bash
# 1. Design session (Sonic Architect)
#    - Choose brainwave target (theta for meditation)
#    - Get instrument recommendations
python vibe-os-mixer.py --recommend theta

# 2. Generate AI music (Music API Integrator)
#    - Use Suno/Hailuo with optimized prompt
#    - Download track

# 3. Generate frequency (Frequency Engineer)
python frequency-generator-pro.py --binaural 432 6 \
  --duration 600 --quality high --output theta_binaural.wav

# 4. Mix final output (Sonic Alchemist)
python vibe-os-mixer.py --music ai_ambient.mp3 \
  --binaural 432 6 --level binaural_optimal \
  --output final_session.wav

# 5. Verify quality (all agents)
#    - Check frequency accuracy via FFT
#    - Confirm stereo separation for binaural
#    - Test with headphones
```

---

## Quality Checklist

- [ ] Frequency accuracy verified (FFT analysis)
- [ ] Stereo separation confirmed for binaural files
- [ ] Headphones tested for binaural effect
- [ ] Duration is 8+ minutes (the minimum used in the cited sources)
- [ ] Volume comfortable (~40 dB equivalent)
- [ ] No clipping in mixed output
- [ ] Fade in/out applied (no clicks)
- [ ] File format: 48kHz, 24-bit WAV

---

## Research Sources

1. **PMC10198548** - Binaural beats systematic review (14 studies)
2. **PMC10196448** - Binaural beats presented below conscious hearing (single report)
3. **PubMed 31031095** - 432 Hz vs 440 Hz: heart rate 4.79 bpm lower (p = 0.05)
4. **PubMed 35545982** - 432 Hz vs 440 Hz in healthcare workers (COVID nurse study)
5. **SCIRP 87146** - 528 Hz: cortisol lower, oxytocin higher after 5 min (preliminary)
6. **Frontiers 2023** - Carrier-frequency range reported for entrainment (200-900 Hz)
7. **Scientific Reports 2025** - 40 Hz gamma beat improved attention in one study

Full research summary: [`frequency-healing-research.md`](frequency-healing-research.md)

---

*Part of the Vibe OS System - FrankX Superintelligent Agent System*
