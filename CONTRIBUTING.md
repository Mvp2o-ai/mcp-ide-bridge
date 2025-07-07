# Contributing to MCP IDE Bridge

Thank you for your interest in contributing to MCP IDE Bridge!

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/mcp-ide-bridge.git
   cd mcp-ide-bridge
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Testing

### Running Tests

```bash
# Run the simple test
python tests/test_simple.py
```

### Writing Tests

When adding new features, please include a simple test in `tests/test_simple.py` to verify the functionality works.

## 📝 Code Standards

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and well-documented

## 🤝 How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the code standards
4. **Test your changes**: `python tests/test_simple.py`
5. **Commit your changes** with clear commit messages
6. **Push to your fork** and submit a pull request

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details** (OS, Python version, etc.)
2. **Steps to reproduce** the issue
3. **Expected vs actual behavior**
4. **Error messages** if any

## 💡 Feature Requests

When requesting features, please:

1. **Describe the use case** and problem it solves
2. **Provide examples** of how it would be used
3. **Check existing issues** to avoid duplicates

## 📚 Documentation

- **README.md** - Main project documentation
- **Code docstrings** - Function and class documentation
- **Examples** - Usage examples in `examples/` directory

## 🔒 Security

- Never commit secrets or sensitive data
- Use environment variables for configuration
- Report security issues privately to maintainers

## How to Contribute via Fork and Pull Request

1. **Fork the repository**
   - Click the 'Fork' button on GitHub and clone your fork locally.

2. **Sync with upstream**
   - Add the main repo as upstream:
     ```sh
     git remote add upstream git@github.com:Mvp2o-ai/mcp-ide-bridge.git
     ```
   - Periodically sync your fork:
     ```sh
     git fetch upstream
     git checkout main
     git merge upstream/main
     git push origin main
     ```

3. **Create a feature branch**
   - Never work directly on `main`.
   - Create a branch for your feature or fix:
     ```sh
     git checkout -b feature/short-description
     ```

4. **Commit and push your changes**
   - Commit with clear messages.
   - Push to your fork:
     ```sh
     git push --set-upstream origin feature/short-description
     ```

5. **Open a Pull Request**
   - Go to your fork on GitHub and click 'Compare & pull request'.
   - Set the base repo to `Mvp2o-ai/mcp-ide-bridge` and base branch to `main`.
   - Set the compare branch to your feature branch.
   - Fill in a descriptive title and summary.

6. **PR Etiquette**
   - Keep PRs focused and small if possible.
   - Reference related issues if applicable.
   - Be responsive to review feedback.

7. **After merge**
   - Sync your fork's main branch with upstream as above.

Thank you for contributing to open source!

---

Thank you for contributing to MCP IDE Bridge! 🚀 