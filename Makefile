.PHONY: help install install-codex install-other list validate

SKILLS_ROOT := $(CURDIR)
CODEX_SKILLS_DIR ?= $(HOME)/.codex/skills
OTHER_AGENT_ROOTS ?= $(HOME)/.claude $(HOME)/.agents $(HOME)/.cursor

help:
	@printf '%s\n' \
		'Targets:' \
		'  make install       Copy skills to Codex and best-effort agent skill folders' \
		'  make install-codex Copy skills to ~/.codex/skills' \
		'  make install-other Best-effort copy to ~/.claude/skills, ~/.agents/skills, ~/.cursor/skills' \
		'  make list          List source skills' \
		'  make validate      Validate Codex skill metadata when validator is available'

list:
	@find "$(SKILLS_ROOT)" -mindepth 2 -maxdepth 2 -name SKILL.md -print | sed 's#/SKILL.md##' | sort

install: install-codex install-other

install-codex:
	@mkdir -p "$(CODEX_SKILLS_DIR)" 2>/dev/null || true
	@find "$(SKILLS_ROOT)" -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort | while IFS= read -r skill_md; do \
		skill_dir="$${skill_md%/SKILL.md}"; \
		skill_name="$$(basename "$$skill_dir")"; \
		dest="$(CODEX_SKILLS_DIR)/$$skill_name"; \
		printf 'Installing %s -> %s\n' "$$skill_name" "$$dest"; \
		if command -v rsync >/dev/null 2>&1; then \
			rsync -a --delete --exclude '.git' "$$skill_dir/" "$$dest/" || true; \
		else \
			rm -rf "$$dest" 2>/dev/null || true; \
			mkdir -p "$$dest" 2>/dev/null || true; \
			cp -R "$$skill_dir"/. "$$dest"/ 2>/dev/null || true; \
			rm -rf "$$dest/.git" 2>/dev/null || true; \
		fi; \
	done

install-other:
	@for root in $(OTHER_AGENT_ROOTS); do \
		if [ -d "$$root" ]; then \
			dest_root="$$root/skills"; \
			mkdir -p "$$dest_root" || true; \
			find "$(SKILLS_ROOT)" -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort | while IFS= read -r skill_md; do \
				skill_dir="$${skill_md%/SKILL.md}"; \
				skill_name="$$(basename "$$skill_dir")"; \
				dest="$$dest_root/$$skill_name"; \
				printf 'Best-effort install %s -> %s\n' "$$skill_name" "$$dest"; \
				if command -v rsync >/dev/null 2>&1; then \
					rsync -a --delete --exclude '.git' "$$skill_dir/" "$$dest/" || true; \
				else \
					rm -rf "$$dest" 2>/dev/null || true; \
					mkdir -p "$$dest" || true; \
					cp -R "$$skill_dir"/. "$$dest"/ 2>/dev/null || true; \
					rm -rf "$$dest/.git" 2>/dev/null || true; \
				fi; \
			done; \
		else \
			printf 'Skipping missing agent root: %s\n' "$$root"; \
		fi; \
	done

validate:
	@if [ -f "$(HOME)/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ]; then \
		find "$(SKILLS_ROOT)" -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort | while IFS= read -r skill_md; do \
			skill_dir="$${skill_md%/SKILL.md}"; \
			printf 'Validating %s\n' "$$skill_dir"; \
			python3 "$(HOME)/.codex/skills/.system/skill-creator/scripts/quick_validate.py" "$$skill_dir"; \
		done; \
	else \
		printf 'Codex skill validator not found; skipping.\n'; \
	fi
