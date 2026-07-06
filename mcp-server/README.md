# Vibe OS MCP Server

Exposes the Vibe OS research-backed music tools to any MCP client — Claude Code, Claude Desktop, Cursor, or anything speaking the Model Context Protocol.

## Tools

| Tool | What it does |
|---|---|
| `list_vibe_states` | The 25-state research-backed library (BPM, key, mode, instruments, energy, brainwave pairing) |
| `generate_vibe_prompt` | State → optimized Suno/Hailuo/Udio prompt (+ optional lyrics prompt) |
| `generate_transition_prompt` | ISO-principle staged transitions (anxious→calm, tired→energized, sad→hopeful, scattered→focused, plus derived plans) |
| `generate_custom_prompt` | Explicit BPM/key/mood → prompt |
| `list_frequency_presets` | Brainwave bands, evidence-backed frequencies (432/528/40 Hz with citations), solfeggio (marked anecdotal), curated session presets |
| `design_frequency_session` | Session parameters — and a rendered 24-bit WAV if you pass `output_path` |
| `plan_session_mix` | Multi-state listening session plan with per-segment prompts and frequency pairings |
| `compare_vibe_states` | Side-by-side diff of two states — BPM, key, mode, timbre, energy, and instrumentation differences |
| `recommend_state_for_goal` | Free-text goal → top 3 ranked states via deterministic keyword overlap (no LLM/network calls) |

## Install

```bash
pip install -r mcp-server/requirements.txt
```

## Register the server

### Claude Code (project scope — already configured via `.mcp.json` in this repo)

```bash
claude mcp add vibe-os -- python3 mcp-server/server.py
```

### Claude Desktop / Cursor

```json
{
  "mcpServers": {
    "vibe-os": {
      "command": "python3",
      "args": ["/absolute/path/to/vibe-os/mcp-server/server.py"]
    }
  }
}
```

## Example session

> "Put me in deep focus for the next hour."

The client calls `generate_vibe_prompt("deep_focus")` → you get a research-tuned Suno prompt (90 BPM, C Major, soft piano + ambient pads, no vocals) plus the alpha-band pairing → `design_frequency_session(session_type="binaural", carrier_freq=400, beat_freq=10, duration_seconds=3600, output_path="focus.wav")` renders the layer.

## Design notes

- The server **wraps** `tools/*.py` without modifying them — the research logic stays CLI-first and independently usable.
- Tool scripts have hyphenated filenames, so the server loads them via `importlib` rather than imports. Don't rename the scripts; the README and examples document their CLI usage.
- Evidence framing is preserved: solfeggio output is explicitly marked anecdotal; binaural/entrainment and 432/528/40 Hz entries carry their citations from `docs/frequency-healing-research.md`.

---

Part of the [Music Intelligence System](https://github.com/frankxai/music-intelligence-systems) ecosystem.
