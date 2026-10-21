# Requesting API credits and AI tool budget

**Owner:** AI Enablement (#ai-tools) · **Last reviewed:** 2026-10

Orbit Research pays for the AI tools staff use for work. This doc covers how to get access and what the limits are.

## Default access (no request needed)

Every employee gets, on day one:

- A **Claude Team** seat (chat, projects, Claude in Slack).
- A **GitHub Copilot** seat.
- A shared **Anthropic API key** for the `orbit-shared` workspace, capped at **USD 100 per person per month**. Keys are in 1Password under "AI / shared API keys".

## Requesting more

If you expect to spend more than USD 100 in a month (for example running an evaluation across thousands of prompts), post in **#ai-tools** with:

1. What you are running and roughly how many tokens or calls.
2. Which model(s).
3. The expected cost. A rule of thumb: Claude Opus 5.5 costs about **USD 4 per million input tokens and USD 20 per million output tokens**; Sonnet 5.5 is roughly half; Haiku 5.5 is about 20 times cheaper than Opus.

Requests up to **USD 1,000 per month** are approved by the AI Enablement lead, usually within one working day. Above that, the Research Director approves. Approved budgets get their own API key and workspace so spend is tracked per project.

## Rules

- Never put a company API key in a public repo, a notebook you share externally, or a personal machine without disk encryption.
- Rotate a key immediately in #ai-tools if you think it leaked.
- Do not use personal API keys for work; we cannot reimburse them.
- Check the monthly usage dashboard (linked in #ai-tools channel topic) before launching a large run.

## Other tools

Requests for tools we do not already pay for (new coding agents, transcription, image models) go through the same #ai-tools post. We trial new tools for **30 days** before committing to annual seats.
