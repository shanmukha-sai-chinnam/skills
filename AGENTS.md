# Google Agent Skills: Agent Operational Guide

Universal guidelines for coding agents (Google Antigravity, Claude Code, Codex, Cursor, and Herdr-managed agents) utilizing skills from this repository.

---

## Skill Architecture

- **Path Structure**: `skills/<category>/<skill-name>/SKILL.md`
- **Categories**:
  - `cloud`: Google Cloud Platform (Compute, GKE, BigQuery, Storage, Networking, IAM, Cloud Run, Cloud Logging).
  - `ads`: Google Ads API, Google Mobile Ads SDK, IMA SDK.
  - `analytics`: Google Analytics Admin & Data APIs.
  - `developers`: Google Developer Knowledge retrieval and skill discovery.
  - `identity`: DPoP adoption and token authentication.

## Execution Directives

1. **Precision & Data Reduction**: When querying Google Cloud services via CLI or MCP, always apply filtering and projection (`--filter`, `--format`, `--limit`).
2. **Deterministic Validation**: Verify syntax with leaf-level help commands rather than guessing flags or subcommands.
3. **Safe Execution**: Never run destructive deletions or policy modifications autonomously without user review.
