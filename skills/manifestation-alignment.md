# Manifestation Alignment Skill
*Vibe OS for the grounded manifestation practice*

## Overview

You map a person's **goal** to the **state** that goal needs from them, then hand off to the Vibe OS engine to build the track that sets it. This is the bridge between Vibe OS (a state engine) and a grounded manifestation practice (imagination + attention + action). The honest framing: the emotional state you carry changes what you actually do — and music is the fastest reliable lever for state. This is the deliberate version of "raise your vibration," with zero mysticism.

## When to use

Someone wants music to align with a goal, to "get in the right state" before working toward something, or to support a manifestation / visualization / Reality Architect session.

## The mapping

Goals don't need a vibe — the *work the goal requires* does. Translate goal → state → Vibe OS dials.

| If the goal needs… | Target state | Vibe OS state preset | Dials |
|--------------------|-------------|----------------------|-------|
| Clarity to define the vision | Focused calm | `deep_focus` / `creative_flow` | 80–100 BPM · major · instrumental |
| To feel the outcome as real | Steady confidence | `confidence` | 115–140 BPM · major · warm pads |
| To create / render the vision | Creative flow | `creative_flow` | 90–115 BPM · major · piano/strings |
| Energy to ship | Bold energy | `high_energy` / `morning_energy` | 110–170 BPM · major · driving |
| To notice openings (attention) | Open awareness | `relaxation` (light) | 60–80 BPM · major · ambient |
| Recovery / processing a setback | Emotional release | `emotional_release` / `healing` | 55–85 BPM · minor→major · strings |

## Steps

1. **Name the goal and the move.** Ask what they're working toward and which part they're on (defining it, feeling it, building it, shipping it).
2. **Pick the target state** from the table. If they're currently in a *different* state (anxious before a confidence session), apply the **ISO principle**: start the track nearer where they are, then transition toward the target.
3. **Hand off to the engine.** Generate the prompt with the Vibe OS master skill or:
   ```bash
   python tools/vibe-prompt-generator.py --state <preset> --with-lyrics
   ```
4. **Set the ritual.** Tell them to start the track at the top of the work block and begin the work *inside* the state — not to listen passively first.

## The wider loop

This skill is the state-setting step of a larger grounded practice:

- **Vision + feeling** → the imagination rep (see `awesome-manifestation-skills/manifestation-session`).
- **State** → this skill.
- **Attention + action** → act on what surfaces; log it.
- **Render + ship** → use generative AI to make the vision real (the Reality Architect loop).

References: the [Reality Architect method](https://github.com/frankxai/realityarchitect) (architect your state *before* your systems), [awesome-manifestation-skills](https://github.com/frankxai/awesome-manifestation-skills), and the full hub at [frankx.ai/manifestation](https://frankx.ai/manifestation).

## Boundaries

- State is an input to action, not a substitute for it. Don't imply the track does the work.
- Keep frequency/binaural claims as a soft add-on; the reliable levers are tempo, mode, and lyric.
