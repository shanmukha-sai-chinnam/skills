# Google Agent Skills for Antigravity

Repository guidelines for Google Antigravity (AGY) agents navigating this collection of official Google product and service skills.

---

## Operating Guidelines

1. **Progressive Skill Loading**:
   - Skills are located in `skills/<category>/<skill-name>/SKILL.md` (e.g. `skills/cloud/`, `skills/ads/`, `skills/developers/`).
   - Load only the specific skill relevant to the user's current task to avoid exhausting the context window.
   - Respect frontmatter triggers (`description`) to decide relevance.

2. **Safety-Critical Operations (gcloud, IAM, Cloud Storage)**:
   - Always run syntax help (e.g., `gcloud help <leaf-command>`) before proposing non-trivial commands.
   - For destructive operations (e.g. `delete`, IAM policy drops), always request explicit user confirmation.
   - Use dry-run flags (`--dry-run`, `--validate-only`) where available.
   - Use data reduction flags (`--limit`, `--filter`, `--format`) on all list queries.

3. **Multi-Platform Integration**:
   - In Antigravity workspaces, individual skills can be symlinked or copied into `.agents/skills/<skill-name>/` or globally in `~/.gemini/config/skills/<skill-name>/`.
