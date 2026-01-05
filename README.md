# Vibe OS Audio System

**Research-backed frequency healing audio generation and AI music integration.**

Generate binaural beats, pure Hz tones, solfeggio frequencies, and mix them with AI-generated music at scientifically-optimized levels.

---

## Features

- **Frequency Generation** - Pure tones, binaural beats, isochronic tones
- **Research-Backed Presets** - Based on peer-reviewed studies (PubMed, PMC)
- **AI Music Integration** - Optimized prompts for Suno, Hailuo, Udio
- **Intelligent Mixing** - 5 mixing levels including subliminal
- **Professional Quality** - 48kHz, 24-bit audio output

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/vibe-os.git
cd vibe-os

# Generate a theta binaural beat (6 Hz on 432 Hz carrier)
python tools/frequency-generator-pro.py --preset theta --duration 300 --output theta.wav

# Mix AI music with healing frequency
python tools/vibe-os-mixer.py --music your_track.mp3 --frequency theta --output meditation.wav

# Get Suno/Hailuo prompt for frequency-compatible music
python tools/vibe-os-mixer.py --suno-prompt theta
```

## Tools

### frequency-generator-pro.py

Generate evidence-based healing frequencies.

```bash
# Pure 528 Hz "Love Frequency"
python tools/frequency-generator-pro.py --freq 528 --duration 300 --quality high

# Theta binaural beat for meditation
python tools/frequency-generator-pro.py --preset theta --duration 600

# All solfeggio frequencies
python tools/frequency-generator-pro.py --solfeggio all --duration 60
```

**Presets**: delta (sleep), theta (meditation), alpha (focus), beta (alertness), gamma (cognition)

### vibe-os-mixer.py

Combine AI-generated music with healing frequencies.

```bash
# Add subliminal 528 Hz to any song
python tools/vibe-os-mixer.py --music song.mp3 --hz 528 --level subliminal --output healing.wav

# Mix with binaural beat at research-optimal level
python tools/vibe-os-mixer.py --music ambient.mp3 --frequency theta --level binaural_optimal

# Get instrument recommendations
python tools/vibe-os-mixer.py --recommend theta
```

**Mixing Levels**:
| Level | Frequency dB | Description |
|-------|-------------|-------------|
| `dominant` | -3 dB | Frequency leads the mix |
| `balanced` | -6 dB | Equal presence |
| `subtle` | -12 dB | Music leads, frequency adds texture |
| `subliminal` | -24 dB | Below conscious hearing (still effective) |
| `binaural_optimal` | -9 dB | Research-optimal for entrainment |

### frequency-generator.py

Lightweight generator for basic use cases.

```bash
python tools/frequency-generator.py --freq 432 --duration 60 --output tone.wav
python tools/frequency-generator.py --binaural 432 6 --duration 300 --output binaural.wav
```

## Research Foundation

This system is built on peer-reviewed research:

### Binaural Beats (Strong Evidence)
- **PMC10198548** (2023): Systematic review of 14 studies confirmed brain entrainment
- **Scientific Reports** (Feb 2025): 80-participant EEG study confirmed gamma/attention effects
- **PMC11367212** (2024): 84-study review showing improvements in pain, sleep, mood

### 432 Hz (Moderate-Strong Evidence)
- **PubMed 31031095** (2019): Heart rate reduced by 4.79 bpm (p=0.05)
- **PubMed 35545982** (2022): Reduced stress markers in healthcare workers

### 528 Hz (Moderate Evidence)
- **SCIRP 87146** (2018): Decreased cortisol, increased oxytocin
- **2023 Study**: Anxiety reduction of 4.625 points (p=0.006)

### Subliminal Frequencies (Effective)
- **PMC10196448**: Binaural beats below conscious hearing still produce measurable effects

See [docs/frequency-healing-research.md](docs/frequency-healing-research.md) for full citations.

## AI Music Integration

### Supported Platforms

| Platform | API Status | Max Duration |
|----------|-----------|--------------|
| **MiniMax/Hailuo** | Official API | 5 minutes |
| **Suno** | Third-party | 4 minutes |
| **Udio** | Third-party | 2:10 minutes |

### Optimized Prompts

```bash
# Get Suno/Hailuo prompt for theta meditation
python tools/vibe-os-mixer.py --suno-prompt theta

# Output:
# "Ambient meditation music, 60 BPM, soft ethereal pads,
#  gentle singing bowl textures, spacious reverb, no drums,
#  D minor, peaceful and introspective, float through space"
```

### Instrument Recommendations

```bash
python tools/vibe-os-mixer.py --recommend alpha

# Best instruments: acoustic guitar, piano, light percussion, nature
# Avoid: distortion, sudden changes
# Tempo: 60-80 BPM
# Key: G major, C major
```

## Brainwave States

| State | Frequency | Carrier | Effect |
|-------|-----------|---------|--------|
| Delta | 0.5-4 Hz | 200 Hz | Deep sleep, healing |
| Theta | 4-8 Hz | 300 Hz | Meditation, creativity |
| Alpha | 8-13 Hz | 400 Hz | Relaxation, calm focus |
| Beta | 13-30 Hz | 400 Hz | Alertness, concentration |
| Gamma | 30-100 Hz | 300 Hz | Peak cognition, insight |

## Requirements

- Python 3.8+
- NumPy
- FFmpeg (optional, for MP3 support)

```bash
pip install numpy
```

## Documentation

- [Production System Guide](docs/vibe-os-production-system.md)
- [Frequency Research](docs/frequency-healing-research.md)
- [Audio Library Guide](docs/README.md)
- [Verification Report](docs/VERIFICATION_REPORT.md)

## Important Notes

1. **Headphones Required** - Binaural beats only work with headphones
2. **Minimum Duration** - 8+ minutes for brain entrainment
3. **Comfortable Volume** - ~40 dB (moderate listening level)
4. **Not Medical Advice** - Supplement, not replacement for treatment

## License

MIT License - See [LICENSE](LICENSE) for details.

---

*Part of the FrankX Superintelligent Agent System*
