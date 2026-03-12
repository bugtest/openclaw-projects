---
title: /cli/health
source: https://docs.openclaw.ai/cli/health.md
category: tools
fetched: 2026-03-07
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.openclaw.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# health

# `openclaw health`

Fetch health from the running Gateway.

```bash  theme={"theme":{"light":"min-light","dark":"min-dark"}}
openclaw health
openclaw health --json
openclaw health --verbose
```

Notes:

* `--verbose` runs live probes and prints per-account timings when multiple accounts are configured.
* Output includes per-agent session stores when multiple agents are configured.
