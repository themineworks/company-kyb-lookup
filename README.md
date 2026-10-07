# Company KYB Lookup: LEI, EU & SEC EDGAR Verify

KYB lookup for a list of company names. Returns the GLEIF LEI, legal name, entity status and an EU headquarters flag, plus the SEC EDGAR CIK when the filer name matches. Pair it with the EU VAT Validator for VAT checks. No API key required.

**Run it on Apify:** [apify.com/themineworks/company-identity-resolver](https://apify.com/themineworks/company-identity-resolver)
**Docs, FAQ and pricing:** [themineworks.com/actors/company-identity-resolver](https://themineworks.com/actors/company-identity-resolver/)

**Price:** From $2.50 per 1,000 companies on Apify's higher plans ($5.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Resolve company names to LEI and SEC CIK
* GLEIF and SEC EDGAR in one run
* Flags EU-headquartered entities for a VAT check
* Returns null rather than a wrong CIK
* Counterparty and supplier verification

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/company-identity-resolver").call(run_input={
    "companies": [
        "Apple Inc",
        "Volkswagen AG"
    ],
    "countryCode": "US"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/company-identity-resolver').call({
    "companies": [
        "Apple Inc",
        "Volkswagen AG"
    ],
    "countryCode": "US"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~company-identity-resolver/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companies": ["Apple Inc", "Volkswagen AG"], "countryCode": "US"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 company_kyb_lookup.py --token YOUR_APIFY_TOKEN --companies "Apple Inc,Volkswagen AG" --country-code "US"
node company_kyb_lookup.mjs --token YOUR_APIFY_TOKEN --companies "Apple Inc,Volkswagen AG" --country-code "US"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `companies` | array |  | List of company names to resolve |
| `countryCode` | string |  | Optional: hint the country for faster LEI matching (for example US, DE, GB) |
| `includeEDGAR` | boolean | `true` | Look up SEC EDGAR filing status for potential US-listed companies |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `query_name` | string | Company name as provided in the input |
| `lei` | string | Legal Entity Identifier (LEI) from GLEIF |
| `lei_status` | string | LEI registration status (ISSUED, LAPSED, etc.) |
| `legal_name` | string | Official legal name from GLEIF |
| `country` | string | Country of headquarters (ISO 2-letter code) |
| `entity_status` | string | Entity status from GLEIF (ACTIVE, INACTIVE, etc.) |
| `is_eu_registered` | boolean | Whether the entity is registered in an EU member state |
| `edgar_cik` | string | SEC EDGAR Central Index Key if the company is US-listed |
| `edgar_name` | string | Company name as it appears in SEC EDGAR |
| `resolved` | boolean | Whether at least one identifier (LEI or EDGAR CIK) was found |
| `scraped_at` | string | ISO timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/company-identity-resolver
```

## FAQ

### How much does the Company KYB Lookup cost?

From $2.50 per 1,000 companies on Apify's higher plans ($5.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [GST Taxpayer Lookup](https://themineworks.com/actors/gst-taxpayer-lookup/): Verify any Indian GSTIN against the official GST portal
* [World Bank Trade Scraper](https://themineworks.com/actors/global-trade-data/): Imports and exports by country and product, from World Bank WITS
* [SEC EDGAR Filings](https://themineworks.com/actors/sec-edgar-filings/): Structured SEC filings ready for AI and RAG pipelines

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
