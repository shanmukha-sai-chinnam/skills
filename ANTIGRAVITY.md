# Using Google Agent Skills with Google Antigravity

This repository provides curated, high-fidelity agent skills for Google technologies. You can integrate these skills into **Google Antigravity (AGY)** either globally, per-project, or declaratively through Nix flakes.

---

## Installation Methods

### 1. Declarative NixOS-WSL Flake (Recommended for NixOS users)

If using the [damathryxx64](https://github.com/shanmukha-sai-chinnam/damathryxx64) system flake:

```nix
# flake.nix
inputs.google-skills = {
  url = "github:shanmukha-sai-chinnam/skills";
  flake = false;
};
```

All skills are automatically managed, deduplicated, and synchronized into `~/.gemini/config/skills/` on rebuild or login via the `agent-skills-sync.service`.

### 2. Manual Global Skill Installation

To install a specific skill globally into Antigravity:

```bash
# Example: Install BigQuery Basics skill
mkdir -p ~/.gemini/config/skills/bigquery-basics
curl -fsSL https://raw.githubusercontent.com/shanmukha-sai-chinnam/skills/main/skills/cloud/bigquery-basics/SKILL.md \
  -o ~/.gemini/config/skills/bigquery-basics/SKILL.md
```

### 3. Project-Level Workspace Skill

To bundle a skill directly into your project:

```bash
mkdir -p .agents/skills/gcloud
cp -r /path/to/skills/skills/cloud/gcloud/* .agents/skills/gcloud/
```

### 4. Antigravity CLI Plugin Installation

For plugins bundling skills and MCP configs:

```bash
agy plugin install https://github.com/shanmukha-sai-chinnam/skills/plugins/<plugin-name>
```

---

## How Antigravity Discovers and Uses Skills

1. **Progressive Disclosure**: Antigravity automatically indexes skill names and triggering descriptions from `~/.gemini/config/skills/` and `.agents/skills/`.
2. **Context Preservation**: The agent only reads full `SKILL.md` content and reference guides when a matching prompt triggers the skill.
3. **Harmonious Precedence**: Project-level skills in `.agents/skills/` take precedence over global machine skills in `~/.gemini/config/skills/`.
