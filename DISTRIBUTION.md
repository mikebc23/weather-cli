# Distribution Guide for weather-cli

This guide explains how to publish weather-cli to PyPI and Homebrew.

## 🎯 Quick Summary

**For users to install:**

```bash
# Option 1: PyPI (works everywhere)
pip install cr-mb-weather-cli

# Option 2: Homebrew (macOS)
brew install weather-cli
```

Both will provide the `weather` command globally.

## 📦 Publishing to PyPI

### Prerequisites

1. Create accounts:
   - [PyPI Account](https://pypi.org/account/register/)
   - [TestPyPI Account](https://test.pypi.org/account/register/) (for testing)

2. Set up authentication:

   ```bash
   pip install twine
   # Configure ~/.pypirc with your credentials
   ```

### Build and Upload

1. **Build the package:**

   ```bash
   ./scripts/build-pypi.sh
   ```

2. **Test on TestPyPI first:**

   ```bash
   twine upload --repository testpypi dist/*
   pip install --index-url https://test.pypi.org/simple/ cr-mb-weather-cli
   weather --help  # Test it works
   ```

3. **Upload to PyPI:**

   ```bash
   twine upload dist/*
   ```

4. **Verify installation:**

   ```bash
   pip install cr-mb-weather-cli
   weather "New York"  # Should work!
   ```

## 🍺 Publishing to Homebrew

### Method 1: Homebrew Core (Official)

1. **After PyPI is live**, create a PR to [homebrew-core](https://github.com/Homebrew/homebrew-core)
2. Use our formula template in `homebrew/weather-cli.rb`
3. Update the SHA256 hash after PyPI upload
4. Follow [Homebrew's contribution guidelines](https://docs.brew.sh/Formula-Cookbook)

### Method 2: Custom Tap (Easier)

1. **Create your own tap:**

   ```bash
   # Create a new repo: homebrew-tap
   git clone https://github.com/mikebc23/homebrew-tap
   mkdir -p Formula
   cp homebrew/weather-cli.rb Formula/
   git add . && git commit -m "Add weather-cli formula"
   git push origin main
   ```

2. **Users install with:**

   ```bash
   brew tap mikebc23/tap
   brew install weather-cli
   ```

## 🔍 Testing Your Distribution

### Test PyPI Package

```bash
# Create fresh virtual environment
python -m venv test-env
source test-env/bin/activate
pip install cr-mb-weather-cli
weather --help
weather "London"
deactivate
```

### Test Homebrew Formula

```bash
# Test locally first
brew install --build-from-source homebrew/weather-cli.rb
weather --help
brew uninstall weather-cli
```

## 📈 Release Process

1. **Update version** in `setup.py` and `pyproject.toml`
2. **Update CHANGELOG.md** with new features
3. **Create GitHub release** with tag (e.g., `v1.0.1`)
4. **Build and upload to PyPI**
5. **Update Homebrew formula** with new version/hash
6. **Test installations**

## 🎉 After Publishing

Your users can now install with:

```bash
# Python users
pip install cr-mb-weather-cli

# macOS users
brew install weather-cli

# Both get the same `weather` command
weather "Tokyo" --hourly --format visual
```

## 📊 Monitoring

- **PyPI Downloads:** https://pypistats.org/packages/cr-mb-weather-cli
- **GitHub Stats:** Stars, forks, issues
- **Homebrew Stats:** `brew info weather-cli`

## 🔧 Maintenance

- **Dependencies:** Keep `requests` and `urllib3` updated
- **Python versions:** Test against new Python releases
- **Security:** Monitor for vulnerabilities
- **Features:** Gather user feedback for improvements
