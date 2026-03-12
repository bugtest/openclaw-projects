---
title: /cli/cron
source: https://docs.openclaw.ai/cli/cron.md
category: tools
fetched: 2026-03-07
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.openclaw.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# cron

# `openclaw cron`

Manage cron jobs for the Gateway scheduler.

Related:

* Cron jobs: [Cron jobs](/automation/cron-jobs)

Tip: run `openclaw cron --help` for the full command surface.

Note: isolated `cron add` jobs default to `--announce` delivery. Use `--no-deliver` to keep
output internal. `--deliver` remains as a deprecated alias for `--announce`.

Note: one-shot (`--at`) jobs delete after success by default. Use `--keep-after-run` to keep them.

Note: recurring jobs now use exponential retry backoff after consecutive errors (30s → 1m → 5m → 15m → 60m), then return to normal schedule after the next successful run.

Note: retention/pruning is controlled in config:

* `cron.sessionRetention` (default `24h`) prunes completed isolated run sessions.
* `cron.runLog.maxBytes` + `cron.runLog.keepLines` prune `~/.openclaw/cron/runs/<jobId>.jsonl`.

## Common edits

Update delivery settings without changing the message:

```bash  theme={"theme":{"light":"min-light","dark":"min-dark"}}
openclaw cron edit <job-id> --announce --channel telegram --to "123456789"
```

Disable delivery for an isolated job:

```bash  theme={"theme":{"light":"min-light","dark":"min-dark"}}
openclaw cron edit <job-id> --no-deliver
```

Enable lightweight bootstrap context for an isolated job:

```bash  theme={"theme":{"light":"min-light","dark":"min-dark"}}
openclaw cron edit <job-id> --light-context
```

Announce to a specific channel:

```bash  theme={"theme":{"light":"min-light","dark":"min-dark"}}
openclaw cron edit <job-id> --announce --channel slack --to "channel:C1234567890"
```

Create an isolated job with lightweight bootstrap context:

```bash  theme={"theme":{"light":"min-light","dark":"min-dark"}}
openclaw cron add \
  --name "Lightweight morning brief" \
  --cron "0 7 * * *" \
  --session isolated \
  --message "Summarize overnight updates." \
  --light-context \
  --no-deliver
```

`--light-context` applies to isolated agent-turn jobs only. For cron runs, lightweight mode keeps bootstrap context empty instead of injecting the full workspace bootstrap set.
