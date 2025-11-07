# Contributing Guidelines

**Repository**: Foresight Crime Prediction  
**Date**: December 2024

---

## Quick Start

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes following coding standards
4. Write/update tests
5. Commit with clear messages
6. Push and create Pull Request

---

## Development Setup

```bash
# Clone and setup
git clone https://github.com/reichert-sentinel-ai/foresight-crime-prediction.git
cd foresight-crime-prediction
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

---

## Coding Standards

- **PEP 8**: Follow Python style guide
- **Type Hints**: Use type hints
- **Docstrings**: Google-style docstrings
- **Tests**: Maintain 80%+ coverage

---

## Project-Specific Guidelines

- Maintain forecast accuracy (72.5%+)
- Ensure geospatial features work correctly
- Test with crime datasets
- Verify route optimization algorithms

---

*See [Guardian Contributing Guide](../repo-guardian/CONTRIBUTING.md) for detailed guidelines.*

