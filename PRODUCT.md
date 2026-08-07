# Vibe OS Pack — product manifest

**Product id (agenticincome catalog):** `vibe-os-pack` · **Sold via:** Polar (agenticincome.ai) · **Status:** gated, not yet on sale

## What it is

The Vibe OS toolkit, packaged: three Claude Code skills for AI-music prompt engineering (Suno-focused), four Python audio tools, the research documentation they're built on, and runnable examples. You describe the state you want music for — focus, workout, sleep, and the rest of the state library — and the toolkit turns it into a concrete prompt (BPM, key, instrumentation, lyric guidance) plus optional tone/binaural layering for the finished audio.

## Contents (exactly these files, generated from disk)

| Path | Lines | Purpose |
|---|---|---|
| `skills/vibe-os-master.md` | 180 | The state-change system: state library, parameter mappings, workflow |
| `skills/suno-ai-mastery.md` | 531 | Suno v4.5+ platform techniques and prompt engineering |
| `skills/suno-prompt-architect.md` | 583 | Advanced Suno prompt construction for cinematic tracks |
| `tools/vibe-prompt-generator.py` | 624 | CLI: state → AI-music prompt (`--state`, `--with-lyrics`, `--json`, `--list`) |
| `tools/vibe-os-mixer.py` | 460 | CLI: layer generated music with tones/binaural beats |
| `tools/frequency-generator-pro.py` | 597 | CLI: generate pure tones and binaural-beat WAVs (`--freq`, `--preset`) |
| `tools/frequency-generator.py` | 288 | Simpler tone generator (kept for minimal setups) |
| `docs/` (7 files) | 1,905 | Whitepaper, music-psychology and frequency research with citations, production guide, quick reference, verification report |
| `examples/` (2 scripts) | 67 | End-to-end sessions: meditation session, subliminal 528 Hz layer |
| `requirements.txt` | 1 | `numpy>=1.20.0` (FFmpeg optional, for MP3) |

## Who it's for

Creators generating music with Suno (or similar) who want prompts derived from documented music-psychology parameters instead of guesswork, and a local toolchain to mix and layer the results.

## What it is NOT

- **Not medical, therapeutic, or clinical anything.** The docs cite published research on how musical parameters correlate with mood and performance; the toolkit applies those parameters to prompts and audio. No health outcomes are promised, and nothing here treats any condition.
- **Not a music generator.** It writes prompts and processes audio files; the music itself comes from your Suno (or other) account, which you pay for separately.
- **Not exclusive content.** The source is MIT-licensed and public ([frankxai/vibe-os](https://github.com/frankxai/vibe-os)). The paid product is the packaged, versioned edition delivered through checkout; buying it supports development. MIT terms apply either way.

## Packaging note (for the operator, not the buyer)

At sale time, zip the repo contents (`skills/`, `tools/`, `docs/`, `examples/`, `requirements.txt`, `README.md`, `LICENSE`, this file) as `vibe-os-pack.zip` and upload to the Polar product's File Downloads benefit. The agenticincome catalog entry stays status-gated until that upload exists.
