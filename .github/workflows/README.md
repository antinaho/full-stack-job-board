# GitHub Actions CI/CD

This directory contains GitHub Actions workflow configurations for automated testing and continuous integration.

## Workflows

### CI Workflow (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger via GitHub UI (workflow_dispatch)

**What it does:**
1. **Sets up environment**: Ubuntu latest with Python 3.12
2. **Spins up PostgreSQL**: Creates a test database using PostgreSQL 16
3. **Installs dependencies**: Uses `uv` package manager for fast, reliable installs
4. **Runs tests**: Executes all pytest tests in `backend/tests/`

**PostgreSQL Test Database:**
- User: `postgres`
- Password: `postgres`
- Database: `testdb`
- Port: `5432`

## How to Use

### Viewing Test Results

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Select the workflow run you want to view
4. Click on the "Run Tests" job to see detailed output

### Manual Trigger

1. Go to the "Actions" tab
2. Select "CI" workflow from the left sidebar
3. Click "Run workflow" button
4. Select the branch and click "Run workflow"

### Adding a Status Badge

Add this to your README.md to show build status:

```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your actual GitHub username and repository name.

## Customization

### Adding More Python Versions

To test against multiple Python versions, modify the workflow:

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12', '3.13']

steps:
  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

### Adding Code Coverage

To add code coverage reporting:

1. Install pytest-cov:
   ```bash
   uv add pytest-cov --dev
   ```

2. Modify the test step:
   ```yaml
   - name: Run pytest with coverage
     run: uv run pytest backend/tests/ --cov=backend --cov-report=xml
   ```

3. Upload coverage to Codecov (optional):
   ```yaml
   - name: Upload coverage to Codecov
     uses: codecov/codecov-action@v4
     with:
       file: ./coverage.xml
   ```

### Adding Linting

To add code quality checks, create a new job in `ci.yml`:

```yaml
  lint:
    name: Lint Code
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run ruff check backend/
```

## Troubleshooting

### Tests fail in CI but pass locally

- Check environment variables are set correctly in the workflow
- Verify PostgreSQL connection settings match
- Check Python version matches between local and CI
- Review the full test output in the Actions tab

### Slow workflow runs

- Enable caching (already enabled with `enable-cache: true`)
- Use `uv sync --frozen` to avoid resolving dependencies
- Consider running only changed tests for pull requests

### Database connection errors

- Ensure PostgreSQL service is healthy before running tests
- Check port conflicts (PostgreSQL uses 5432)
- Verify connection string format matches psycopg3 syntax

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [uv Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
