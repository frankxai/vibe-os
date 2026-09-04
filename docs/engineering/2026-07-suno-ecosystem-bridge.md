# Suno ↔ Ecosystem Bridge
*Architecture Proposal — Real-Time Generation Management Without a Suno API*
*July 2026 · Status: Proposed · Author: /si engineering session*

---

## Executive Summary

Frank wants the Music Intelligence System to "interconnect with Suno and live data and manage generations in real time." Suno has no public API — the ecosystem's own deferred-items ledger (`music-intelligence-systems/roadmap/DEFERRED.md`, "Suno API Integration") records this, verified as of 2026-06-22 and re-verified this session. So "real-time interconnect" cannot mean API calls. It has to mean something buildable today.

This proposal breaks the ask into five sub-capabilities, shows that three of them are already solved or solvable without touching Suno's servers, and recommends a **hybrid bridge**:

1. **vibe-os MCP** stays the prompt brain (already shipped).
2. **Claude-in-Chrome** becomes the live-generation companion — a separate Claude context running in Frank's own browser that can see and drive the Suno tab while he works.
3. **Google Drive intake folder** ("Arcanea Music — Suno Intake", already created and readable via the connected Drive MCP) is the durable capture channel: Frank exports takes, agents catalog and post-process them.
4. **Unofficial Suno API wrappers are rejected as a default** — they violate Suno's ToS and risk the account that holds the catalog. Analyzed honestly below, adopted never (as a default), revisited only if Suno ships a real API.

The result is a round trip — prompt out, audio back, learnings fed forward — that requires zero ToS violations, zero reverse engineering, and roughly one session of glue work.

---

## 1. Problem Framing — What "Real-Time Interconnect" Actually Means

"Interconnect with Suno in real time" is a compound ask. Decomposed:

| # | Sub-capability | Status | Where it runs |
|---|---------------|--------|---------------|
| C1 | **Generate state-optimized prompts** | ✅ Solved | vibe-os Python engine (25 states) + MCP server (`generate_vibe_prompt`, `generate_transition_prompt`, `generate_custom_prompt`, `recommend_state_for_goal`, …) |
| C2 | **Get prompts into Suno** | ⚠️ Manual (copy-paste) | Frank's browser — this is the Suno boundary, inbound |
| C3 | **Capture generated outputs** | ⚠️ Manual (download/export) | Frank's browser → Drive intake folder — the Suno boundary, outbound |
| C4 | **Catalog, master, sequence captured audio** | ✅ Solvable today | vibe-os tools (`vibe-os-mixer.py`, `frequency-generator-pro.py`), Drive MCP read access, ecosystem agents |
| C5 | **Feed learnings back into prompt generation** | 🔲 Not built | vibe-os repo — a take-log that biases future prompts toward what worked |

**The Suno boundary is precisely C2 and C3** — the two moments where data crosses into or out of Suno's web app. Everything on our side of that boundary (C1, C4, C5) is ordinary engineering we control. Everything at the boundary is constrained by one hard fact:

> **Suno exposes no public API.** All integrations today are copy-paste prompts or browser-based workflows. (`roadmap/DEFERRED.md`, music-intelligence-systems hub — which already names the vibe-os MCP server as the natural integration point via a future `generate_suno_track` tool when an API ships.)

So the design question is not "how do we call Suno" — it's "how do we make the two manual boundary crossings as cheap, fast, and lossless as possible, and automate everything on either side of them."

One more constraint worth stating plainly: **this headless Claude Code session cannot reach a browser.** "Claude in Chrome" (Anthropic's extension in Frank's own Chrome) is a *separate* Claude context that can see and drive a live Suno tab. Any live-loop design has to hand off to that context — it cannot run here.

---

## 2. Options Analysis — Four Bridge Strategies

### Comparison table

| | (a) Manual export → Drive intake | (b) Claude-in-Chrome companion | (c) Unofficial Suno API wrapper | (d) Local watch-folder daemon |
|---|---|---|---|---|
| **What it unlocks** | Durable capture + agent-side catalog/master/sequence (C3, C4) | Live loop: prompt insertion, generation monitoring, metadata scraping from Frank's own tab (C2, C3 partially) | Full programmatic C2+C3 — submit jobs, poll status, download audio | Zero-click C3: Suno downloads land in ecosystem automatically |
| **Cost / effort** | ~Zero — folder exists, Drive MCP connected, works today | Low — session playbook + prompt-handoff format; no code on Suno's side | Medium — pick/pin a wrapper, host it, maintain against breakage | Low-medium — small daemon (watchdog + rclone/Drive sync) on Frank's machine |
| **Risk** | None (Frank's own exports, own Drive) | Low — Frank's own logged-in browser, human-in-the-loop, ordinary web use | **High — violates Suno ToS; plausible account ban; the 12k+ catalog account is the blast radius** | Low — local file ops only; fragile only to Suno's download naming |
| **Token efficiency** | Good — agents read files on demand, batch-friendly | Moderate — vision/DOM interaction in the Chrome context burns tokens per action; fine for a session, wasteful for bulk | Best (if it worked) — structured JSON, no vision | Good — metadata extracted locally, agents see clean manifests |
| **Durability** | High — Drive + MCP are stable, boring infrastructure | Medium — depends on Suno's UI and the extension; playbooks need occasional updating | **Low — breaks whenever Suno changes internal endpoints; wrappers are perpetually chasing** | High for the daemon; medium for filename-parsing heuristics |
| **Real-time?** | No — minutes-later capture | **Yes — this is the only real-time option that exists** | Yes, but at unacceptable risk | Near-real-time (seconds after download) |
| **Verdict** | **Keep — durable capture backbone** | **Adopt — the live creative loop** | **Reject as default — document as contingency only** | **Adopt in Next phase — removes the export chore** |

### (a) Manual export → Drive intake folder — what exists now

Frank generates in Suno, downloads or exports takes to the Drive folder **"Arcanea Music — Suno Intake"** (folder id `1iF8qP5m31K6X7WfbCof6dOBQdlfes-aB`). The Google Drive MCP is connected and verified working this session — Claude can search and read the folder directly. From there, agents can catalog takes, run `vibe-os-mixer.py` frequency layering, plan sequences with `plan_session_mix`, and write take-logs.

Honest assessment: this is not real-time and it puts a chore on Frank (download → upload). But it is the only channel in this design that produces *durable, agent-readable artifacts*, and it costs nothing to keep. Every other option feeds it rather than replacing it.

### (b) Claude-in-Chrome browser companion — the live loop

Anthropic's Claude-in-Chrome extension runs in Frank's own browser, sees the live Suno tab, and can interact with it — as Frank, in Frank's logged-in session, with Frank watching. That's a categorically different risk posture from a reverse-engineered API: it's a human's assistant operating a web app the way a human does, not a bot impersonating the client.

What the companion can do in a live session:

- Take a prompt pack generated by vibe-os (via this repo's MCP tools) and paste prompts into Suno's create form.
- Watch generations complete and read titles, style strings, and durations off the page.
- Capture Frank's verbal verdicts ("take 2 is the keeper") into a session log.
- Nudge Frank to export keepers to the Drive intake folder — closing the loop to channel (a).

What it cannot do: run headless, run unattended, or run from this Claude Code session. It's a *companion for Frank's generation sessions*, not a background service. Its durability depends on Suno's UI staying roughly stable — acceptable, because the playbook is prose, not brittle selectors, and a UI change degrades to "Frank pastes manually" rather than breaking anything.

The engineering deliverable here is not code. It's a **handoff contract**: a prompt-pack file format that this session's agents write and the Chrome context reads, plus a session-log format flowing the other way.

### (c) Unofficial Suno API wrapper — honest risk assessment

Reverse-engineered Suno clients exist on GitHub and npm. They work by replaying Suno's private web-client endpoints with Frank's session cookies. Technically they would give us everything: programmatic submission, status polling, direct audio download, structured metadata.

The case against, plainly:

1. **ToS violation.** Suno's terms prohibit automated access outside official channels. This isn't a gray area.
2. **Ban blast radius.** The account at risk is the one holding Frank's entire generation history and active subscription. Losing it costs vastly more than any automation saves.
3. **Perpetual breakage.** Private endpoints change without notice. Wrapper maintainers chase; we'd be chasing the chasers.
4. **It poisons the well.** If Suno ships a real API (the DEFERRED.md unlock condition), an account previously flagged for automation is exactly the account you don't want to be holding.

The case for, honestly: it's the only path to *unattended* generation — batch-producing a 25-state session library overnight, say. If that ever becomes the dominant need, the risk-managed version is a **separate, disposable Suno account** used only for wrapper experiments, never the main catalog account. Even then: recommend against until the value of unattended batching is demonstrated with real demand, not speculation.

**Recommendation: rejected as a default. Documented as a contingency with an explicit precondition (separate account + demonstrated batch need + Frank's sign-off).**

### (d) Local watch-folder daemon — automating the capture chore

A small daemon on Frank's machine (Python `watchdog` or even just Drive for Desktop pointed at the browser download directory) that:

1. Watches the folder where Suno downloads land.
2. Detects new audio files, extracts what metadata the filename/tags carry.
3. Writes a manifest entry (JSON: filename, timestamp, inferred prompt/state if the session log provides it).
4. Syncs file + manifest into the Drive intake folder (or a local mirror the agents read).

This turns C3 from "Frank remembers to upload" into "Frank clicks Download and walks away." It composes with (a) — same destination, less friction — and with (b) — the Chrome session log supplies the prompt↔file linkage the filename alone can't. Risks are minor: filename conventions drift, and the daemon is one more process on Frank's machine. Cheapest version: skip custom code entirely and let **Drive for Desktop sync the download directory**, with a periodic agent pass that manifests whatever arrived. Start there; write the daemon only if the naive version leaks metadata we need.

---

## 3. Recommended Architecture — The Hybrid Bridge

Adopt **(a) + (b) + (d)**, in that order of standing: Drive intake is the durable spine, Claude-in-Chrome is the live loop, the watch-folder is the friction remover. vibe-os MCP remains the single prompt brain feeding all of it. Wrapper (c) stays on the shelf with its preconditions written down.

```
                         FRANK'S MACHINE / BROWSER                         CLOUD
        ┌──────────────────────────────────────────────────┐   ┌────────────────────────┐
        │                                                  │   │                        │
  ┌─────┴──────┐   prompt pack    ┌─────────────────┐      │   │   ┌────────────────┐   │
  │  vibe-os   │  (files / MCP)   │ Claude-in-Chrome │ paste│   │   │     SUNO       │   │
  │ MCP server ├─────────────────►│  (live session   ├──────┼───┼──►│   (web app,    │   │
  │ 25 states  │                  │   companion)     │      │   │   │    NO API)     │   │
  │ 9+ tools   │                  └────────┬─────────┘      │   │   └───────┬────────┘   │
  └─────▲──────┘                           │ session log    │   │           │ Frank      │
        │                                  │ (takes, verdicts)  │           │ downloads/ │
        │ C5: take-log biases             ▼                 │   │           │ exports    │
        │ future prompts          ┌─────────────────┐       │   │           ▼            │
  ┌─────┴──────┐                  │  download dir   │       │   │   ┌────────────────┐   │
  │  take-log  │◄─────────────────┤  + watch-folder ├───────┼───┼──►│  Drive intake  │   │
  │ (manifest  │   manifests      │  sync (Drive    │  sync │   │   │ "Arcanea Music │   │
  │  + verdicts)│                 │  for Desktop)   │       │   │   │ — Suno Intake" │   │
  └─────▲──────┘                  └─────────────────┘       │   │   └───────┬────────┘   │
        │                                                   │   │           │            │
        └───────────────────────────────────────────────────┼───┼───────────┘            │
                       headless Claude Code session         │   │  Drive MCP (read/search│
                       catalogs, masters (vibe-os-mixer),   │   │  — verified working)   │
                       sequences (plan_session_mix)         │   └────────────────────────┘
        └──────────────────────────────────────────────────┘

  Round trip: state intent → vibe-os prompt → Chrome companion pastes → Suno generates
  → Frank keeps/kills → download → watch-folder/Drive → headless agents catalog + master
  → take-log updates → next session's prompts are better. The only human-mandatory steps
  are the two boundary crossings (paste-confirm and download) plus taste itself.
```

### The handoff contract (the one thing to actually specify)

Two small file formats make the three channels compose. Both live in the Drive intake folder (or a `sessions/` subfolder) so every context — Chrome, headless, Frank's phone — reads the same source of truth:

- **Prompt pack** (`session-YYYY-MM-DD.prompts.json`): ordered list of `{state, prompt, lyrics_guidance, frequency_pairing, intent_note}` — exactly what `generate_vibe_prompt` already emits, batched.
- **Take log** (`session-YYYY-MM-DD.takes.json`): per generation, `{prompt_ref, suno_title, verdict: keep|kill|rework, notes, filename}` — written by the Chrome companion during the session, enriched by the watch-folder manifest after.

C5 (the learning loop) is then a plain read: before generating the next pack, the prompt agent reads recent take logs and biases toward the styles, BPMs, and phrasings that earned `keep`.

---

## 4. Real-Time Generation Management UX — A Day in the Loop

What "manage generations in real time" concretely looks like, given the boundary:

**Before the session (headless, async — this kind of Claude Code session):**
Frank says "I want a 3-track morning arc: wake → focus → flow." Agents call `recommend_state_for_goal` / `generate_transition_prompt`, consult the take-log for what's worked, and write a prompt pack to the intake folder. Frank gets a link, not a wall of text.

**During the session (Frank + Claude-in-Chrome, real-time):**
Frank opens Suno and the prompt pack side by side. The Chrome companion pastes prompt 1, Frank hits Create. While Suno renders, the companion queues prompt 2 and logs the take metadata as results appear. Frank listens and says "first one's the keeper, second's too bright." The companion records the verdicts and reminds him to download keepers. Frank stays in the creative seat the whole time — the companion handles clipboard, bookkeeping, and memory, which is exactly the drudgery that breaks flow.

**After the session (headless, async):**
Downloads sync to the intake folder. Agents manifest the new files, pair them with take-log entries, run `vibe-os-mixer.py` to layer binaural/solfeggio frequencies per the state spec, assemble session sequences via `plan_session_mix`, and update the take-log. Next week's prompts start from evidence.

**Division of labor, stated once:** Frank does taste, clicks Create, and clicks Download. Suno does rendering. Everything else — prompt science, bookkeeping, capture, mastering, sequencing, learning — is agent work. "Real time" lives entirely in the middle block, and only the Chrome context can deliver it.

---

## 5. Phased Build Plan

### Now (this week — no unblock condition; everything already exists)

- **Ships:** Prompt-pack and take-log JSON formats (spec + one example of each, written to the Drive intake folder). A short Chrome-companion session playbook (prose, in this repo under `docs/engineering/`). First end-to-end manual run: pack → Suno → export → Drive → agent catalog pass.
- **Proves:** The round trip works with zero new infrastructure.

### Next (unblock: one successful manual round trip + Frank confirms the loop feels right)

- **Ships:** Watch-folder capture — Drive for Desktop sync of the Suno download directory (or a small watchdog daemon if metadata leaks), plus an agent manifest pass that reconciles new audio against take logs. Take-log-aware prompt generation: the prompt agent reads verdicts before writing the next pack. Optional: a `log_suno_take` / `read_take_log` tool pair on the vibe-os MCP server so any MCP client can query the loop's state.
- **Proves:** Capture is zero-chore and prompts measurably improve (keep-rate per session is the metric — tracked in the take-log itself, not claimed).

### Later (each item gated on an explicit external unblock)

- **`generate_suno_track` MCP tool** — gated on **Suno shipping a public API**, exactly as `music-intelligence-systems/roadmap/DEFERRED.md` already records. The vibe-os MCP server is the designated integration point; the prompt-pack format becomes the request schema for free.
- **Unattended batch generation via wrapper (contingency (c))** — gated on *all three*: demonstrated demand for overnight batching, a separate disposable Suno account, and Frank's explicit sign-off on the ToS trade. Default answer stays no.
- **Catalog-scale integration** — wiring take-logs into the wider Music Intelligence System hub (12k+ catalog indexing, release pipeline) once the per-session loop is stable. Tie-in point: the hub's `ECOSYSTEM.md` map.

---

## 6. Open Questions — Needs Frank or External Input

1. **Drive folder layout:** Flat intake folder, or `sessions/YYYY-MM-DD/` subfolders per generation session? (Affects the manifest pass; cheap to decide, annoying to migrate.)
2. **Chrome companion appetite:** How much should the companion *do* in the Suno tab — paste-only, or also click Create? Paste-only keeps Frank as the actor for every generation-spending action; recommend starting there and letting Frank loosen it.
3. **Verdict vocabulary:** Is `keep | kill | rework` enough, or does Frank want a richer scale (e.g., keeper-for-release vs. keeper-for-personal-use)? The take-log schema should freeze early.
4. **Watch-folder host:** Which machine actually runs the sync — the Windows box with the existing scheduled-task infrastructure, or wherever Frank generates? (Determines whether we reuse Drive for Desktop or write the daemon.)
5. **Disposable-account contingency:** Does Frank want the wrapper contingency researched and shelf-ready (account created, wrapper pinned, never run), or left entirely cold until demand shows up? Recommend cold.
6. **Suno API watch:** Who/what monitors for a public Suno API announcement so the Later phase unblocks promptly? (Candidate: the existing research-scan cadence in the FrankX ecosystem; needs a one-line addition, not new machinery.)

---

*Part of the [Music Intelligence System](https://github.com/frankxai/music-intelligence-systems). Companion to `roadmap/DEFERRED.md` (Suno API Integration) in the hub repo.*
