# Saylog Design Skills Repository Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the three Dou-product-dependent skills into `saylog-design-skills`, remove them from `agent-skills`, and document installation and external private dependencies in both repositories.

**Architecture:** Preserve each skill directory as a self-contained unit under `saylog-design-skills/skills/`. Keep the general-purpose skills in `agent-skills` and remove only the moved entries from its README. The new README is the source of truth for private installation and product-repository access requirements.

**Tech Stack:** Git repositories, Markdown, `npx skills` CLI, shell-based file and link verification.

## Global Constraints

- Move exactly `dou-product-design`, `dou-uxui-issues`, and `manual-authoring`, including every nested file.
- Do not modify or delete any other skill in `agent-skills`.
- Do not fetch, modify, or commit changes to external product repositories.
- Use SSH installation examples for the private repository.
- State that `npx skills add` does not automatically install or authenticate external private repositories referenced by a skill.
- Keep the existing MIT license in `agent-skills`; add an MIT license file to `saylog-design-skills` only if the target repository does not already have one.

---

### Task 1: Move the three dependent skill directories

**Files:**
- Move from `/Users/initred/Code/agent-skills/skills/dou-product-design/` to `/Users/initred/Code/saylog-design-skills/skills/dou-product-design/`
- Move from `/Users/initred/Code/agent-skills/skills/dou-uxui-issues/` to `/Users/initred/Code/saylog-design-skills/skills/dou-uxui-issues/`
- Move from `/Users/initred/Code/agent-skills/skills/manual-authoring/` to `/Users/initred/Code/saylog-design-skills/skills/manual-authoring/`

**Interfaces:**
- Produces the three complete skill directories in the private repository.
- Leaves all other `agent-skills/skills/*` directories untouched.

- [ ] **Step 1: Create the target skill parent directory**

Run:

```bash
mkdir -p /Users/initred/Code/saylog-design-skills/skills
```

- [ ] **Step 2: Move each exact directory**

Run:

```bash
mv /Users/initred/Code/agent-skills/skills/dou-product-design /Users/initred/Code/saylog-design-skills/skills/
mv /Users/initred/Code/agent-skills/skills/dou-uxui-issues /Users/initred/Code/saylog-design-skills/skills/
mv /Users/initred/Code/agent-skills/skills/manual-authoring /Users/initred/Code/saylog-design-skills/skills/
```

- [ ] **Step 3: Verify the move before documentation edits**

Run:

```bash
test -f /Users/initred/Code/saylog-design-skills/skills/dou-product-design/SKILL.md
test -f /Users/initred/Code/saylog-design-skills/skills/dou-uxui-issues/SKILL.md
test -f /Users/initred/Code/saylog-design-skills/skills/manual-authoring/SKILL.md
test ! -e /Users/initred/Code/agent-skills/skills/dou-product-design
test ! -e /Users/initred/Code/agent-skills/skills/dou-uxui-issues
test ! -e /Users/initred/Code/agent-skills/skills/manual-authoring
```

Expected: all six tests exit successfully.

### Task 2: Update the original repository README

**Files:**
- Modify: `/Users/initred/Code/agent-skills/README.md`

**Interfaces:**
- Produces a README whose skill catalog contains only skills still present in `agent-skills`.

- [ ] **Step 1: Remove the three moved skill rows**

Delete the `dou-product-design`, `dou-uxui-issues`, and `manual-authoring` rows from the catalog. Remove the associated `douinc/agent-skills@...` install examples for those skills and leave the rest of the catalog unchanged.

- [ ] **Step 2: Check for stale source links**

Run:

```bash
rg -n 'dou-product-design|dou-uxui-issues|manual-authoring|agent-skills@' /Users/initred/Code/agent-skills/README.md
```

Expected: only the generic `douinc/agent-skills@<skill-name>` installation pattern and entries for skills that remain in the source repository are present; no moved-skill path or row remains.

### Task 3: Write the private repository README

**Files:**
- Create: `/Users/initred/Code/saylog-design-skills/README.md`

**Interfaces:**
- Documents direct installation from `douinc/saylog-design-skills`.
- Documents the `dou-product-design` → `dou-uxui-issues` relationship.
- Documents external product-repository permissions for all three skills.

- [ ] **Step 1: Add repository purpose and access requirements**

Explain that the repository is private and users must have GitHub read access. Show the reliable SSH form:

```bash
npx skills add git@github.com:douinc/saylog-design-skills.git --skill <skill-name>
```

Also show the shorthand form requested by the repository’s existing conventions, with a note that the user’s GitHub authentication must already be able to clone the private repository.

- [ ] **Step 2: Add the skill catalog and dependency table**

Describe each skill and list the required private repositories or local product files. Explicitly state that skill installation does not automatically fetch or authenticate those external dependencies.

- [ ] **Step 3: Add usage, structure, contribution, and license sections**

Document the `skills/<skill-name>/SKILL.md` layout, how to add or update a skill, and the MIT license.

### Task 4: Verify repository integrity and documentation

**Files:**
- Test: both repository working trees and Markdown references

- [ ] **Step 1: Compare moved file manifests**

Run:

```bash
find /Users/initred/Code/saylog-design-skills/skills/dou-product-design /Users/initred/Code/saylog-design-skills/skills/dou-uxui-issues /Users/initred/Code/saylog-design-skills/skills/manual-authoring -type f | sort
```

Confirm that all files observed in the source before migration are present in the target.

- [ ] **Step 2: Validate Markdown and whitespace**

Run:

```bash
git -C /Users/initred/Code/agent-skills diff --check
git -C /Users/initred/Code/saylog-design-skills diff --check
```

Expected: no output and exit code 0.

- [ ] **Step 3: Verify stale references and Git status**

Run:

```bash
rg -n 'skills/(dou-product-design|dou-uxui-issues|manual-authoring)|agent-skills@(dou-product-design|dou-uxui-issues|manual-authoring)' /Users/initred/Code/agent-skills/README.md
git -C /Users/initred/Code/agent-skills status --short
git -C /Users/initred/Code/saylog-design-skills status --short
```

Expected: the first command returns no matches; Git status shows only the three source deletions, source README change, target skill files, target README, and the already committed design/plan documents.
