#!/usr/bin/env python3
"""Resolve company names to their LEI and SEC CIK in one run. Python, Node.js and cURL clients for the Company KYB Lookup on Apify, pay per result.

Command-line client for the themineworks/company-identity-resolver actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/company-identity-resolver/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/company-identity-resolver"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--companies", help="Comma-separated. List of company names to resolve")
    ap.add_argument("--country-code", help="Optional: hint the country for faster LEI matching (for example US, DE, GB)")
    ap.add_argument("--include-e-d-g-a-r", action=argparse.BooleanOptionalAction, help="Look up SEC EDGAR filing status for potential US-listed companies")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.companies: run_input["companies"] = [s.strip() for s in a.companies.split(",") if s.strip()]
    if a.country_code is not None: run_input["countryCode"] = a.country_code
    if a.include_e_d_g_a_r is not None: run_input["includeEDGAR"] = a.include_e_d_g_a_r

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
