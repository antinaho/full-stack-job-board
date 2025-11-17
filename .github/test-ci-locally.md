# Testing CI Workflow Locally

You can test the GitHub Actions workflow locally before pushing to GitHub using [act](https://github.com/nektos/act).

## Install act

### macOS
```bash
brew install act
```

### Linux
```bash
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Windows
```bash
choco install act-cli
```

## Run the CI Workflow Locally

```bash
# Run the default workflow
act

# Run the CI workflow specifically
act -W .github/workflows/ci.yml

# Run only the test job
act -j test

# Run with verbose output
act -v

# List all workflows and jobs
act -l
```

## Notes

- act uses Docker to simulate GitHub Actions runners
- PostgreSQL service container will be started automatically
- First run will download the Ubuntu runner image (~1GB)
- Subsequent runs will be much faster

## Limitations

- Some GitHub-specific features may not work identically
- Secrets and environment variables need to be configured
- Service containers work but may behave slightly differently

## Alternative: Just Run Tests Normally

For most cases, you can simply run tests locally as usual:

```bash
# Start the database
docker compose up db

# Run tests in another terminal
uv run pytest backend/tests/ -v
```

This is often faster and more reliable than simulating the full CI environment.
