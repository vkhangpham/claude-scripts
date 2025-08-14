# Setup Guide

This guide will help you set up the Claude Scripts French learning toolkit using `uv` for fast Python dependency management.

## Prerequisites

- macOS (for text-to-speech features)
- Python 3.8+ 
- Terminal access

## 1. Install uv (Ultra-fast Python Package Manager)

### Option A: Using curl (Recommended)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option B: Using Homebrew
```bash
brew install uv
```

### Option C: Using pip
```bash
pip install uv
```

## 2. Clone and Setup the Project

```bash
# Clone the repository
git clone https://github.com/vkhangpham/claude-scripts.git
cd claude-scripts

# Create a virtual environment with uv
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies with uv (much faster than pip)
uv pip install rich verbecc requests beautifulsoup4
```

## 3. Make Scripts Executable

```bash
chmod +x wr cj lr wr-cj speak-fr pdf-extract
```

## 4. Add to PATH

### Option A: Add to PATH permanently (Recommended)

Add the scripts directory to your PATH in your shell configuration file:

#### For Zsh (default on macOS):
```bash
echo 'export PATH="$PATH:$(pwd)"' >> ~/.zshrc
source ~/.zshrc
```

#### For Bash:
```bash
echo 'export PATH="$PATH:$(pwd)"' >> ~/.bashrc
source ~/.bashrc
```

#### For Fish:
```bash
echo 'set -gx PATH $PATH '(pwd) >> ~/.config/fish/config.fish
source ~/.config/fish/config.fish
```

### Option B: Create symlinks (Alternative)

```bash
# Create symlinks in a directory already in PATH
sudo ln -sf "$(pwd)/wr" /usr/local/bin/wr
sudo ln -sf "$(pwd)/cj" /usr/local/bin/cj
sudo ln -sf "$(pwd)/lr" /usr/local/bin/lr
sudo ln -sf "$(pwd)/wr-cj" /usr/local/bin/wr-cj
sudo ln -sf "$(pwd)/speak-fr" /usr/local/bin/speak-fr
```

## 5. Re-source Your Shell

After modifying your shell configuration, reload it:

```bash
# For Zsh
source ~/.zshrc

# For Bash  
source ~/.bashrc

# For Fish
source ~/.config/fish/config.fish

# Or simply restart your terminal
```

## 6. Verify Installation

Test that all tools work correctly:

```bash
# Test WordReference translation
wr hello

# Test French conjugation
cj être

# Test French dictionary
lr maison

# Test text-to-speech
speak-fr "Bonjour le monde"

# Check cache status
wr --cache-stats
```

## 7. Why uv?

`uv` is significantly faster than traditional `pip` for Python package management:

- **Speed**: 10-100x faster dependency resolution and installation
- **Reliability**: Better dependency resolution with conflict detection
- **Compatibility**: Drop-in replacement for pip commands
- **Modern**: Built in Rust with modern Python packaging standards

### Performance Comparison:
```bash
# Traditional pip (slower)
pip install rich verbecc requests beautifulsoup4  # ~30-60 seconds

# With uv (faster)
uv pip install rich verbecc requests beautifulsoup4  # ~3-10 seconds
```

## 8. Troubleshooting

### Virtual Environment Issues
```bash
# If .venv activation fails, try:
deactivate  # if already in a venv
rm -rf .venv
uv venv
source .venv/bin/activate
```

### PATH Issues
```bash
# Check if tools are in PATH
which wr
which cj
which lr

# If not found, verify PATH contains the scripts directory
echo $PATH | grep claude-scripts
```

### Permission Issues
```bash
# If scripts aren't executable
chmod +x wr cj lr wr-cj speak-fr pdf-extract

# If uv installation fails
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

### macOS Speech Issues
```bash
# If speak-fr doesn't work, check available voices
say -v ?
```

## 9. Development Setup (Optional)

For development or contributing:

```bash
# Install development dependencies
uv pip install black flake8 pytest

# Run formatting
black *.py

# Run linting
flake8 *.py
```

## 10. Updating Dependencies

```bash
# Update all packages with uv
uv pip install --upgrade rich verbecc requests beautifulsoup4

# Or update specific package
uv pip install --upgrade rich
```

## Complete Workflow Example

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Setup project
git clone https://github.com/vkhangpham/claude-scripts.git
cd claude-scripts
uv venv
source .venv/bin/activate
uv pip install rich verbecc requests beautifulsoup4

# 3. Make executable and add to PATH
chmod +x wr cj lr wr-cj speak-fr pdf-extract
echo 'export PATH="$PATH:'$(pwd)'"' >> ~/.zshrc
source ~/.zshrc

# 4. Test everything works
wr bonjour
```

You're now ready to use the comprehensive French learning toolkit! 🇫🇷