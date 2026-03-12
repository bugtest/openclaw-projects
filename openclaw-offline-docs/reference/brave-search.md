---
title: /brave-search
source: https://docs.openclaw.ai/brave-search.md
category: reference
fetched: 2026-03-07
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.openclaw.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Brave Search

# Brave Search API

OpenClaw supports Brave Search as a web search provider for `web_search`.

## Get an API key

1. Create a Brave Search API account at [https://brave.com/search/api/](https://brave.com/search/api/)
2. In the dashboard, choose the **Data for Search** plan and generate an API key.
3. Store the key in config (recommended) or set `BRAVE_API_KEY` in the Gateway environment.

## Config example

```json5  theme={"theme":{"light":"min-light","dark":"min-dark"}}
{
  tools: {
    web: {
      search: {
        provider: "brave",
        apiKey: "BRAVE_API_KEY_HERE",
        maxResults: 5,
        timeoutSeconds: 30,
      },
    },
  },
}
```

## Tool parameters

| Parameter     | Description                                                         |
| ------------- | ------------------------------------------------------------------- |
| `query`       | Search query (required)                                             |
| `count`       | Number of results to return (1-10, default: 5)                      |
| `country`     | 2-letter ISO country code (e.g., "US", "DE")                        |
| `language`    | ISO 639-1 language code for search results (e.g., "en", "de", "fr") |
| `ui_lang`     | ISO language code for UI elements                                   |
| `freshness`   | Time filter: `day` (24h), `week`, `month`, or `year`                |
| `date_after`  | Only results published after this date (YYYY-MM-DD)                 |
| `date_before` | Only results published before this date (YYYY-MM-DD)                |

**Examples:**

```javascript  theme={"theme":{"light":"min-light","dark":"min-dark"}}
// Country and language-specific search
await web_search({
  query: "renewable energy",
  country: "DE",
  language: "de",
});

// Recent results (past week)
await web_search({
  query: "AI news",
  freshness: "week",
});

// Date range search
await web_search({
  query: "AI developments",
  date_after: "2024-01-01",
  date_before: "2024-06-30",
});
```

## Notes

* The Data for AI plan is **not** compatible with `web_search`.
* Brave provides paid plans; check the Brave API portal for current limits.
* Brave Terms include restrictions on some AI-related uses of Search Results. Review the Brave Terms of Service and confirm your intended use is compliant. For legal questions, consult your counsel.
* Results are cached for 15 minutes by default (configurable via `cacheTtlMinutes`).

See [Web tools](/tools/web) for the full web\_search configuration.
