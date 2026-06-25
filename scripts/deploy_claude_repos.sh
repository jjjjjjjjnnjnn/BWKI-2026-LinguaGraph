#!/bin/bash
# Claude Repos — Global Deployment Script
# Merges all skill/agent/rule/hook repos into ~/.claude/
# Run from any directory — uses CLAUDE_REPOS path below

CLAUDE_REPOS="C:/Users/rongj/Desktop/claude-repos"
CLAUDE_DIR="$HOME/.claude"

# Ensure target directories exist
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents" "$CLAUDE_DIR/rules" "$CLAUDE_DIR/hooks" "$CLAUDE_DIR/commands"

echo "=== Deploying Claude Repos ==="
echo "Source: $CLAUDE_REPOS"
echo "Target: $CLAUDE_DIR"
echo ""

# Track what we deploy
TOTAL_SKILLS=0
TOTAL_AGENTS=0
TOTAL_RULES=0

cd "$CLAUDE_REPOS"

for repo in */; do
  repo_name=$(basename "$repo")
  echo "--- $repo_name ---"

  # Skills: copy from repo root/skills/ and repo/.claude/skills/
  for src in "$repo/skills" "$repo/.claude/skills" "$repo/commands"; do
    if [ -d "$src" ]; then
      count=$(ls "$src" 2>/dev/null | wc -l)
      if [ "$count" -gt 0 ]; then
        target="$CLAUDE_DIR/$(basename $src)"
        cp -rn "$src"/* "$target"/ 2>/dev/null
        echo "  → $(basename $src): $count items"
        [ "$(basename $src)" = "skills" ] && TOTAL_SKILLS=$((TOTAL_SKILLS + count))
        [ "$(basename $src)" = "agents" ] && TOTAL_AGENTS=$((TOTAL_AGENTS + count))
      fi
    fi
  done

  # Agents: copy from repo root/agents/ and repo/.claude/agents/
  for src in "$repo/agents" "$repo/.claude/agents"; do
    if [ -d "$src" ]; then
      count=$(ls "$src" 2>/dev/null | wc -l)
      if [ "$count" -gt 0 ]; then
        cp -rn "$src"/* "$CLAUDE_DIR/agents"/ 2>/dev/null
        echo "  → agents: $count items"
        TOTAL_AGENTS=$((TOTAL_AGENTS + count))
      fi
    fi
  done

  # Rules: copy with repo namespace to avoid conflicts
  for src in "$repo/rules" "$repo/.claude/rules"; do
    if [ -d "$src" ]; then
      count=$(ls "$src" 2>/dev/null | wc -l)
      if [ "$count" -gt 0 ]; then
        mkdir -p "$CLAUDE_DIR/rules/$repo_name"
        cp -rn "$src"/* "$CLAUDE_DIR/rules/$repo_name"/ 2>/dev/null
        echo "  → rules/$repo_name: $count items"
        TOTAL_RULES=$((TOTAL_RULES + count))
      fi
    fi
  done

  # Hooks: merge all hooks
  for src in "$repo/hooks" "$repo/.claude/hooks"; do
    if [ -d "$src" ]; then
      count=$(ls "$src" 2>/dev/null | wc -l)
      if [ "$count" -gt 0 ]; then
        cp -rn "$src"/* "$CLAUDE_DIR/hooks"/ 2>/dev/null
        echo "  → hooks: $count items"
      fi
    fi
  done

  echo ""
done

echo "=== Deployment Complete ==="
echo "Skills: $TOTAL_SKILLS items"
echo "Agents: $TOTAL_AGENTS items"
echo "Rules: $TOTAL_RULES items (namespaced)"
echo "Hooks: merged"
echo "Commands: merged"
