#!/usr/bin/env python3
"""
Multi-Upstream Synchronization and Autonomous Rewrite Engine for Gemini & Antigravity Skills.

Tracks upstream sources:
  - Superpowers (obra/superpowers)
  - Andrej Karpathy Skills (forrestchang/andrej-karpathy-skills)
  - I Have ADHD (ayghri/i-have-adhd)

Applies automated Antigravity/Gemini conversions, purges foreign providers, and validates skills.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Terminal Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

UPSTREAMS = {
    "superpowers": {
        "remote": "upstream-superpowers",
        "url": "https://github.com/obra/superpowers.git",
        "branch": "main",
        "source_dir": "skills",
        "dest_dir": "skills/superpowers",
    },
    "karpathy": {
        "remote": "upstream-karpathy",
        "url": "https://github.com/forrestchang/andrej-karpathy-skills.git",
        "branch": "main",
        "source_dir": "skills/karpathy-guidelines",
        "dest_dir": "skills/karpathy/karpathy-guidelines",
    },
    "adhd": {
        "remote": "upstream-adhd",
        "url": "https://github.com/ayghri/i-have-adhd.git",
        "branch": "main",
        "source_dir": "skills/i-have-adhd",
        "dest_dir": "skills/adhd/i-have-adhd",
    },
}

FOREIGN_TERMS = [
    r"\bClaude Code\b",
    r"\bclaude-code\b",
    r"\bClaude Desktop\b",
    r"\bOpenCode\b",
    r"\bopencode\b",
    r"\bHermes Agent\b",
    r"\bDevin CLI\b",
    r"\bKimi Code CLI\b",
    r"\bQwen Code\b",
    r"\bclaude plugin install\b",
    r"\bCLAUDE\.md\b",
    r"\bCURSOR\.md\b",
]

INCOMPATIBLE_SUPERPOWERS_SKILLS = [
    "dispatching-parallel-agents",
    "subagent-driven-development",
]


def run_cmd(cmd, cwd=REPO_ROOT, check=True, capture=True):
    """Run shell command with error handling."""
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
        )
        return res
    except subprocess.CalledProcessError as e:
        if capture and e.stderr:
            print(f"{RED}Command failed: {' '.join(cmd)}{RESET}\n{e.stderr.strip()}", file=sys.stderr)
        raise


def ensure_remotes():
    """Ensure all required upstreams are registered as git remotes."""
    existing_remotes = run_cmd(["git", "remote"]).stdout.split()
    for name, data in UPSTREAMS.items():
        remote = data["remote"]
        if remote not in existing_remotes:
            print(f"  Adding missing remote {CYAN}{remote}{RESET} ({data['url']})...")
            run_cmd(["git", "remote", "add", remote, data["url"]])


def cmd_status():
    """Report commit status against origin and all upstreams."""
    print(f"\n{BOLD}{BLUE}Skills Hub Upstream Status Report{RESET}")
    print("═" * 65)
    ensure_remotes()

    # Origin status
    try:
        origin_diff = run_cmd(["git", "rev-list", "--left-right", "--count", "origin/main...HEAD"]).stdout.strip().split()
        behind_origin, ahead_origin = int(origin_diff[0]), int(origin_diff[1])
        print(f"Origin (origin/main): +{ahead_origin} / -{behind_origin}")
    except Exception:
        print(f"Origin (origin/main): Unable to compare")

    # Upstream status
    for name, data in UPSTREAMS.items():
        remote = data["remote"]
        branch = data["branch"]
        ref = f"{remote}/{branch}"
        try:
            diff = run_cmd(["git", "rev-list", "--left-right", "--count", f"{ref}...HEAD"]).stdout.strip().split()
            behind, ahead = int(diff[0]), int(diff[1])
            status_str = f"+{ahead} / -{behind}"
            if behind > 0:
                status_color = YELLOW
            else:
                status_color = GREEN
            print(f"Upstream {name.capitalize():<12} ({ref:<25}): {status_color}{status_str}{RESET}")
        except Exception as e:
            print(f"Upstream {name.capitalize():<12} ({ref:<25}): {RED}Not fetched or unreachable{RESET}")
    print("═" * 65 + "\n")


def cmd_fetch():
    """Fetch updates from origin and all upstreams."""
    print(f"\n{BOLD}{BLUE}Fetching all remotes...{RESET}")
    ensure_remotes()
    run_cmd(["git", "fetch", "--all", "--prune"], capture=False)
    print(f"{GREEN}✓ All remotes fetched successfully.{RESET}\n")


def cmd_rewrite():
    """Purge foreign providers and enforce Antigravity & Gemini format."""
    print(f"\n{BOLD}{BLUE}Rewriting skills for Gemini and Antigravity...{RESET}")
    
    # 1. Purge foreign files / directories
    for root, dirs, files in os.walk(REPO_ROOT, topdown=True):
        if ".git" in dirs:
            dirs.remove(".git")
        if "node_modules" in dirs:
            dirs.remove("node_modules")

        for d in list(dirs):
            if d in [".claude-plugin", ".cursor-plugin", ".codex-plugin", ".hermes-plugin", ".opencode"]:
                full_d = Path(root) / d
                shutil.rmtree(full_d, ignore_errors=True)
                dirs.remove(d)

        for f in files:
            if f in ["CLAUDE.md", "CURSOR.md", "CODEX.md", "OPENCODE.md"]:
                (Path(root) / f).unlink(missing_ok=True)

    # 2. Remove incompatible superpowers subagent skills
    for sk in INCOMPATIBLE_SUPERPOWERS_SKILLS:
        p = REPO_ROOT / "skills" / "superpowers" / sk
        if p.exists():
            shutil.rmtree(p, ignore_errors=True)

    # 3. Text sanitization across markdown and json files
    scan_exts = [".md", ".json", ".sh", ".yaml", ".yml"]
    modified_files = 0

    for ext in scan_exts:
        for p in REPO_ROOT.rglob(f"*{ext}"):
            if ".git" in p.parts or "node_modules" in p.parts:
                continue
            try:
                content = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            
            orig = content
            # Strip disable-model-invocation
            content = re.sub(r"^disable-model-invocation:\s*true\s*$\n?", "", content, flags=re.MULTILINE)
            # Rebrand providers to Antigravity & Gemini
            content = content.replace("Claude Code", "Antigravity CLI")
            content = content.replace("claude-code", "antigravity-cli")
            content = content.replace("Claude Desktop", "Antigravity IDE")
            content = content.replace("OpenCode", "Antigravity CLI")
            content = content.replace("opencode", "antigravity-cli")
            content = content.replace("Hermes Agent", "Antigravity Agent")
            content = content.replace("Devin CLI", "Antigravity CLI")
            content = content.replace("Kimi Code CLI", "Antigravity CLI")
            content = content.replace("Qwen Code", "Antigravity CLI")
            content = content.replace("claude plugin install", "agy plugin install")
            content = content.replace("CLAUDE.md", "AGENTS.md")
            content = content.replace("CURSOR.md", "AGENTS.md")

            if content != orig:
                p.write_text(content, encoding="utf-8")
                modified_files += 1

    print(f"  {GREEN}✓ Rewrote and sanitized {modified_files} files for Gemini/Antigravity.{RESET}\n")


def cmd_audit():
    """Audit all skills for frontmatter integrity and Antigravity compliance."""
    print(f"\n{BOLD}{BLUE}Auditing skills in repository...{RESET}")
    total_skills = 0
    passed = 0
    issues = []

    skills_root = REPO_ROOT / "skills"
    for path in skills_root.rglob("SKILL.md"):
        total_skills += 1
        rel = path.relative_to(REPO_ROOT)
        content = path.read_text(encoding="utf-8", errors="replace")
        
        fm = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not fm:
            issues.append(f"{RED}[MISSING FRONTMATTER]{RESET} {rel}")
            continue

        fm_text = fm.group(1)
        name_m = re.search(r"^name:\s*([^\s]+)", fm_text, re.MULTILINE)
        desc_m = re.search(r"^description:\s*(.*)", fm_text, re.MULTILINE)

        if not name_m:
            issues.append(f"{RED}[MISSING NAME]{RESET} {rel}")
        if not desc_m or not desc_m.group(1).strip():
            issues.append(f"{RED}[MISSING DESCRIPTION]{RESET} {rel}")
        else:
            passed += 1

    print(f"  Scanned {total_skills} skills.")
    if issues:
        print(f"  {YELLOW}Found {len(issues)} issue(s):{RESET}")
        for iss in issues[:10]:
            print(f"    {iss}")
        if len(issues) > 10:
            print(f"    ... and {len(issues) - 10} more.")
    else:
        print(f"  {GREEN}✓ All {passed} skills passed frontmatter integrity checks.{RESET}\n")


def cmd_sync():
    """Sync updates from upstreams into the monorepo."""
    print(f"\n{BOLD}{BLUE}Syncing upstream skill sources...{RESET}")
    cmd_fetch()

    # 1. Sync Superpowers
    try:
        upstream_files = run_cmd(["git", "ls-tree", "-r", "--name-only", "upstream-superpowers/main", "skills/"]).stdout.split()
        synced_count = 0
        for f in upstream_files:
            if not f.startswith("skills/"):
                continue
            sub_path = f[len("skills/"):]
            skill_name = sub_path.split("/")[0]
            if skill_name in INCOMPATIBLE_SUPERPOWERS_SKILLS or skill_name in ["adhd", "karpathy", "superpowers"]:
                continue
            dest_file = REPO_ROOT / "skills" / "superpowers" / sub_path
            src_content = run_cmd(["git", "show", f"upstream-superpowers/main:{f}"]).stdout
            if not dest_file.exists() or dest_file.read_text(encoding="utf-8", errors="replace") != src_content:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                dest_file.write_text(src_content, encoding="utf-8")
                synced_count += 1
        if synced_count > 0:
            print(f"  {GREEN}✓ Superpowers synced ({synced_count} files updated).{RESET}")
        else:
            print(f"  {GREEN}✓ Superpowers already up-to-date.{RESET}")
    except Exception as e:
        print(f"  {YELLOW}Superpowers sync check: {e}{RESET}")

    # 2. Sync Karpathy
    try:
        upstream_files_k = run_cmd(["git", "ls-tree", "-r", "--name-only", "upstream-karpathy/main", "skills/karpathy-guidelines/"]).stdout.split()
        synced_count_k = 0
        for f in upstream_files_k:
            sub_path = f[len("skills/karpathy-guidelines/"):] if f.startswith("skills/karpathy-guidelines/") else Path(f).name
            dest_file = REPO_ROOT / "skills" / "karpathy" / "karpathy-guidelines" / sub_path
            src_content = run_cmd(["git", "show", f"upstream-karpathy/main:{f}"]).stdout
            if not dest_file.exists() or dest_file.read_text(encoding="utf-8", errors="replace") != src_content:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                dest_file.write_text(src_content, encoding="utf-8")
                synced_count_k += 1
        if synced_count_k > 0:
            print(f"  {GREEN}✓ Karpathy guidelines synced ({synced_count_k} files updated).{RESET}")
        else:
            print(f"  {GREEN}✓ Karpathy guidelines already up-to-date.{RESET}")
    except Exception as e:
        print(f"  {YELLOW}Karpathy sync check: {e}{RESET}")

    # 3. Sync ADHD
    try:
        upstream_files_adhd = run_cmd(["git", "ls-tree", "-r", "--name-only", "upstream-adhd/main", "skills/i-have-adhd/"]).stdout.split()
        synced_count_adhd = 0
        for f in upstream_files_adhd:
            sub_path = f[len("skills/i-have-adhd/"):] if f.startswith("skills/i-have-adhd/") else Path(f).name
            dest_file = REPO_ROOT / "skills" / "adhd" / "i-have-adhd" / sub_path
            src_content = run_cmd(["git", "show", f"upstream-adhd/main:{f}"]).stdout
            if not dest_file.exists() or dest_file.read_text(encoding="utf-8", errors="replace") != src_content:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                dest_file.write_text(src_content, encoding="utf-8")
                synced_count_adhd += 1
        if synced_count_adhd > 0:
            print(f"  {GREEN}✓ i-have-adhd synced ({synced_count_adhd} files updated).{RESET}")
        else:
            print(f"  {GREEN}✓ i-have-adhd already up-to-date.{RESET}")
    except Exception as e:
        print(f"  {YELLOW}ADHD sync check: {e}{RESET}")

    # Run rewrite and audit
    cmd_rewrite()
    cmd_audit()


def cmd_daily():
    """Daily automated pipeline: sync, rewrite, audit, commit, and push."""
    print(f"\n{BOLD}{CYAN}Running Daily Upstream Sync & Verification Pipeline{RESET}\n")
    cmd_sync()
    
    # Check if working tree has changes
    status = run_cmd(["git", "status", "--porcelain"]).stdout.strip()
    if status:
        print(f"\n{BLUE}Changes detected. Committing and pushing...{RESET}")
        run_cmd(["git", "add", "-A"])
        run_cmd(["git", "commit", "-m", "chore(upstream-sync): daily sync and Gemini/Antigravity rewrite"])
        run_cmd(["git", "push", "origin", "main"])
        print(f"{GREEN}✓ Successfully synced and pushed to origin/main!{RESET}\n")
    else:
        print(f"{GREEN}✓ No upstream changes. Repository is clean and in sync.{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Skills Hub Multi-Upstream Synchronization")
    parser.add_argument("action", choices=["status", "fetch", "sync", "rewrite", "audit", "daily"], help="Action to perform")
    args = parser.parse_args()

    if args.action == "status":
        cmd_status()
    elif args.action == "fetch":
        cmd_fetch()
    elif args.action == "sync":
        cmd_sync()
    elif args.action == "rewrite":
        cmd_rewrite()
    elif args.action == "audit":
        cmd_audit()
    elif args.action == "daily":
        cmd_daily()


if __name__ == "__main__":
    main()
