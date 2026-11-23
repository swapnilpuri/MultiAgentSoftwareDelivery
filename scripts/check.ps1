$ErrorActionPreference = 'Stop'
function Invoke-Check([scriptblock]$Command) {
    & $Command
    if ($LASTEXITCODE -ne 0) { throw "Quality gate failed: $Command" }
}
Invoke-Check { uv run --frozen python scripts/validate_standards.py }
Invoke-Check { uv run --frozen ruff check . }
Invoke-Check { uv run --frozen ruff format --check . }
Invoke-Check { uv run --frozen mypy }
Invoke-Check { uv run --frozen pytest -q }
Invoke-Check { uv run --frozen python scripts/scan_secrets.py }
Invoke-Check { uv run --frozen pip-audit }
$npmCommand = if ($IsWindows) { 'npm.cmd' } else { 'npm' }
foreach ($gate in @('lint', 'typecheck', 'format:check', 'test', 'build')) {
    Invoke-Check { & $npmCommand --prefix apps/web run $gate }
}
Invoke-Check { & $npmCommand --prefix apps/web audit --audit-level=low }
