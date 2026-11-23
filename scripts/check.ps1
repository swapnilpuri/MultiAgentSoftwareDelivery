$ErrorActionPreference = 'Stop'
uv run --frozen python -m scripts.check
if ($LASTEXITCODE -ne 0) { throw 'Required quality gate failed' }
