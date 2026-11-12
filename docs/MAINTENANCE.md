# Maintenance

## Checks (run all before every change)

```bash
python3 scripts/validate.py --release        # structure, rules, manifest, plugin files, workflow map
python3 -m unittest discover -s tests        # each rule proven by breaking it, the router corpus, the usage tool
python3 scripts/route_corpus.py check        # the router corpus is well-formed
python3 skills/ns-route/scripts/ns selftest  # the usage tool behind every phase footer
```

CI runs the same commands on every push and pull request (`.github/workflows/ci.yml`).

## Rules the validator enforces

- every skill is manual-only (`disable-model-invocation: true`), has the set preflight, a `Read first:` line that includes the core, and `agents/openai.yaml` (Codex opt-out);
- `SKILL.md` is 6.5 KB or less (warning at 4.5 KB; exceptions are written in `ns-skills.json`), the core `skills/ns-route/references/core.md` is 13 KB or less: new shared rules go in a `topic-*.md` file, not the core;
- skills read each other only by relative path (`../ns-route/references/...`), never by an absolute or home path;
- Claude Code only concepts appear only in `topic-harnesses.md`;
- no em dash anywhere;
- `.claude-plugin/plugin.json`, `marketplace.json`, `ns-skills.json`, `VERSION` and the `skills/` folders agree;
- the flow call graph is acyclic, the router lists every flow, and `docs/workflow-map.html` lists the same workflows and phases as the catalog.

## Changing a workflow

After any change to a flow, a phase, a gate or a run mode that affects a workflow or a station's description, update the matching file under `skills/ns-route/references/workflows/` and the data in `docs/workflow-map.html` (and its `SYNCED` date) in the same change.

## Releasing

1. Bump the version in `VERSION`, `ns-skills.json` and `.claude-plugin/plugin.json` (the validator checks they agree).
2. Merge to the default branch with CI green.
3. Tag and publish: `git tag vX.Y.Z && git push --tags`, then `gh release create vX.Y.Z --generate-notes`.

The changelog is the generated release notes. Never edit it by hand.
