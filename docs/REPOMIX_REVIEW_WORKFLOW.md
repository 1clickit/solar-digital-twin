# Repomix Review Workflow

## Purpose

Use Repomix occasionally to create a point-in-time repository snapshot
for architecture review, project understanding, and task planning.

Repomix output is temporary review material. It is not authoritative
project memory and is not a recovery backup.

## Guardrails

- GitHub repository documentation remains authoritative.
- Run from a clean working tree unless uncommitted tracked changes are intended.
- Supply only Git-tracked paths using `git ls-files`.
- Keep Repomix sensitive-data scanning enabled.
- Keep explicit exclusions as defense in depth.
- Review the generated file before uploading or sharing it.
- Write output to `/tmp`; do not commit generated snapshots.
- Use `repomix@latest` only for initial evaluation, then pin the tested version.

## Approved Initial Evaluation Command

```bash
node -e '
const major = Number(process.versions.node.split(".")[0]);
if (major < 22) {
  console.error(`Node.js 22+ required; found ${process.version}`);
  process.exit(1);
}
console.log(`Node.js ${process.version}: OK`);
' &&
git ls-files |
npx --yes repomix@latest --stdin \
  --style xml \
  --parsable-style \
  --output /tmp/solar-digital-twin-repomix.xml \
  --token-count-tree 1000 \
  --ignore '.venv/**,node_modules/**,**/__pycache__/**,.pytest_cache/**,.mypy_cache/**,.ruff_cache/**,evidence/**,reports/**,backups/**,coverage/**,htmlcov/**,dist/**,build/**,*.pyc,*.sqlite,*.sqlite3,*.db,*.log,.env,.env.*,**/secrets.yaml,**/*.pem,**/*.key,**/*.p12,**/*.pfx,repomix-output.*'

ls -lh /tmp/solar-digital-twin-repomix.xml 2>/dev/null || true

```

## Important Detail

`git ls-files` limits Repomix to tracked filenames, but it reads their
current working-tree contents. A modified tracked file can therefore
appear in the snapshot before it is committed.
