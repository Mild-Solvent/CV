# Data handling rules

**Owner:** Research Ops (#data-governance) · **Last reviewed:** 2026-10

Orbit Research works with public datasets, licensed datasets and a small amount of personal data (survey responses, interview notes). These rules keep us out of trouble.

## Classification

| Level | Examples | Where it may live |
|---|---|---|
| **Public** | Published papers, our own public datasets | Anywhere |
| **Internal** | Draft analyses, unpublished results, this wiki | Google Drive, GitHub `orbit-research` org, Notion, Slack |
| **Confidential** | Licensed datasets, partner data under NDA, survey responses with names | Encrypted laptop, the `orbit-secure` GCS bucket, approved tools only |
| **Restricted** | Payroll, health data, interview recordings | People team drive only; never Slack, never AI tools |

## AI tools and data

- **Public and Internal** data may be pasted into Claude Team, Claude in Slack, Copilot and the shared API.
- **Confidential** data may go to the Anthropic API only via the `orbit-secure` workspace, which has zero-data-retention enabled. Not into chat tools.
- **Restricted** data never goes into any AI tool.

## Licensed datasets

Check the license in the dataset register (Notion) before downloading. Most licences forbid redistribution; keep copies in the `orbit-secure` bucket, not on personal drives. Delete local copies when a project ends.

## Personal data

If you collect survey or interview data: use the consent template, store responses in the `orbit-secure` bucket, and anonymise before analysis. Keep raw responses for **at most 12 months** after the project ends.

## Incidents

If data ends up somewhere it should not be (wrong Slack channel, public repo, lost laptop), post in **#data-governance within 24 hours**. Nobody gets in trouble for reporting; people do get in trouble for hiding it.

## Retention

Internal docs: keep. Confidential: review yearly. Restricted: as required by law, then delete.
