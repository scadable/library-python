# Contributing to Scadable Python SDK

Thank you for your interest in contributing to Scadable! This guide will help you get started with development, testing, and contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Architecture & Design](#architecture--design)
- [Code Style](#code-style)
- [Testing](#testing)
- [Making Contributions](#making-contributions)
- [Release Process](#release-process)

## Getting Started

Before you start, please:

1. Read the main [Organization Docs](https://github.com/scadable/.github/blob/main/CONTRIBUTING.md) for general Scadable contribution guidelines
2. Check existing [issues](https://github.com/scadable/library-python/issues) to see if your bug/feature is already being discussed
3. For major changes, open an issue first to discuss your proposed changes

## Development Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager
- git

### Clone and Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/library-python.git
   cd library-python
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv

   # On macOS/Linux
   source .venv/bin/activate

   # On Windows
   .venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

   This installs the package in editable mode along with:
   - `pytest` - Testing framework
   - `coverage` - Code coverage reporting
   - `pytest-cov` - Coverage plugin for pytest
   - `pytest-asyncio` - Async test support
   - `pre-commit` - Git hooks for code quality

4. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

   This will automatically run code style checks before each commit.

### Verify Your Setup

Run the test suite to ensure everything is working:

```bash
pytest tests
```

You should see all tests passing.

## Architecture & Design

### Overview

The Scadable Python SDK is designed with modularity, extensibility, and ease of use in mind. It follows a layered architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                    │
│              (User's Python application)                │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                      SDK Layer                          │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Facility │──│DeviceManager │  │ConnectionFactory│  │
│  └────┬─────┘  └──────┬───────┘  └────────┬────────┘  │
│       │               │                    │            │
│  ┌────▼───────────────▼────────────────────▼────────┐  │
│  │          Device (Telemetry Bus)                  │  │
│  └──────────────────────┬───────────────────────────┘  │
└─────────────────────────┼──────────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────────────┐
│                  Transport Layer                         │
│        (WebSocket Connection to Scadable Platform)       │
└──────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Facility (`facility.py`)

**Purpose**: Main entry point and orchestrator for the SDK.

**Responsibilities**:
- API key management and authentication
- Device lifecycle management (create, delete)
- Connection factory coordination
- Decorator API for telemetry subscriptions

**Key Methods**:
- `create_device()` - Creates a single device with optional connection
- `create_many_devices()` - Batch device creation
- `live_telemetry()` - Decorator for subscribing to device telemetry

**Design Pattern**: Facade pattern - provides a simplified interface to the complex subsystem of devices and connections.

#### 2. Device & DeviceManager (`device.py`)

**Device**:
- Represents a single IoT device/data source
- Manages two event buses:
  - `raw_bus`: For raw, unparsed telemetry data
  - `parsed_bus`: For parsed telemetry data
- Handles asynchronous message routing to subscribers

**DeviceManager**:
- Registry pattern for device instances
- Prevents duplicate device creation
- Provides dictionary-like access to devices

**Design Pattern**: Observer pattern - devices maintain lists of subscribers and notify them of data events.

#### 3. Connection (`connection.py`)

**Abstract Classes**:
- `Connection`: Base interface for all connection types
- `ConnectionFactory`: Abstract factory for creating connections

**Concrete Implementations**:
- `WebsocketConnection`: WebSocket-based connection implementation
- `WebsocketConnectionFactory`: Factory for WebSocket connections

**Design Pattern**:
- Abstract Factory - allows for different connection types (WebSocket, HTTP, custom)
- Strategy pattern - connection behavior can be swapped at runtime

**Extension Point**: To add a new connection type (e.g., MQTT, HTTP polling):
1. Subclass `Connection` and implement `connect()`, `send_message()`, `stop()`
2. Subclass `ConnectionFactory` and implement `create_connection()`
3. Pass your factory to `Facility(connection_factory=YourFactory())`

### Data Flow

```
1. User creates Facility with API key and ConnectionFactory
2. User calls create_device(id, create_connection=True)
3. Facility asks ConnectionFactory for a Connection
4. Connection is injected into Device
5. User decorates handler with @facility.live_telemetry("device-id")
6. Handler is added to Device's parsed_bus
7. User calls device.start_live_telemetry()
8. Connection establishes WebSocket, listens for messages
9. Messages flow: WebSocket → Device._handle_raw() → raw_bus → parsed_bus
10. All subscribed handlers are called asynchronously
```

### Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.10+ | Core implementation |
| Async Runtime | asyncio | stdlib | Asynchronous I/O |
| WebSocket Client | websockets | ≥13.0 | Real-time communication |
| Testing | pytest | latest | Unit and integration tests |
| Async Testing | pytest-asyncio | latest | Testing async code |
| Code Coverage | pytest-cov | latest | Coverage reporting |
| Linting | ruff | latest | Code quality enforcement |
| Git Hooks | pre-commit | latest | Automated checks |

### Design Principles

1. **Async-First**: All I/O operations are asynchronous for scalability
2. **Type Safety**: Full type hints throughout for better IDE support and fewer bugs
3. **Extensibility**: Abstract base classes allow for custom implementations
4. **Simplicity**: Clean decorator API hides complexity from end users
5. **Testability**: Dependency injection and abstract interfaces enable easy mocking

## Code Style

This project uses [ruff](https://github.com/astral-sh/ruff) to enforce code style and quality. Configuration is managed through [pre-commit](https://pre-commit.com/).

### Style Guidelines

- **PEP 8**: Follow Python's standard style guide
- **Type Hints**: All public APIs must have type hints
- **Docstrings**: Use Google-style docstrings for all public classes and methods
- **Line Length**: 88 characters (Black default)
- **Import Order**: stdlib → third-party → local (managed by ruff)

### Running Style Checks

**Automatic (via pre-commit hooks)**:
```bash
pre-commit install  # One-time setup
# Now checks run automatically on git commit
```

**Manual**:
```bash
# Check all files
pre-commit run --all-files

# Check only staged files
pre-commit run
```

### Example Docstring

```python
def create_device(self, device_id: str, create_connection: bool = False) -> Device:
    """
    Creates a device associated with the facility.

    Args:
        device_id: Unique identifier for the device
        create_connection: Whether to create a WebSocket connection for live telemetry

    Returns:
        The created Device instance

    Raises:
        RuntimeError: If create_connection=True but no connection factory was provided

    Example:
        >>> facility = Facility("api-key")
        >>> device = facility.create_device("sensor-001")
    """
```

## Testing

### Running Tests

**Run all tests**:
```bash
pytest tests
```

**Run with coverage**:
```bash
pytest tests --cov=scadable --cov-report=html
```

Coverage report will be available in `htmlcov/index.html`.

**Run specific test file**:
```bash
pytest tests/test_facility.py
```

**Run specific test**:
```bash
pytest tests/test_facility.py::test_create_device_no_conn
```

### Writing Tests

- **Location**: Place tests in `tests/` directory
- **Naming**: Test files must start with `test_`
- **Async Tests**: Use `async def` and `@pytest.mark.asyncio` decorator
- **Mocking**: Use `mock_connection.py` for connection mocks
- **Coverage**: Aim for >80% code coverage

**Example Test**:
```python
import pytest
from scadable import Facility

def test_create_device():
    facility = Facility("test-api-key")
    device = facility.create_device("device-1")

    assert device.device_id == "device-1"
    assert device in facility.device_manager.devices.values()

@pytest.mark.asyncio
async def test_live_telemetry():
    # Test async functionality
    facility = Facility("key", connection_factory=MockFactory())
    device = facility.create_device("dev-1", create_connection=True)

    received_data = []

    @facility.live_telemetry("dev-1")
    async def handler(data: str):
        received_data.append(data)

    # Assert handler was registered
    assert len(device.parsed_bus) == 1
```

### Test Structure

```
tests/
├── __init__.py
├── mock_connection.py        # Mock connection implementations
├── test_connection_type.py   # Connection tests
├── test_device.py            # Device and DeviceManager tests
├── test_facility.py          # Facility tests
└── test_import.py            # Import and basic smoke tests
```

## Making Contributions

### Workflow

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**:
   ```bash
   pytest tests
   pre-commit run --all-files
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

   Use conventional commits:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `refactor:` - Code refactoring
   - `chore:` - Build/tooling changes

5. **Push and create a PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

   Then create a Pull Request on GitHub.

### PR Guidelines

- **Title**: Use conventional commit format
- **Description**: Explain what changes were made and why
- **Tests**: Ensure all tests pass
- **Coverage**: Don't decrease overall code coverage
- **Documentation**: Update README.md if user-facing changes
- **Review**: Be responsive to code review feedback

### What to Contribute

**Good First Issues**:
- Documentation improvements
- Test coverage improvements
- Bug fixes
- Example code

**Feature Requests**:
- New connection types (MQTT, HTTP polling)
- Additional telemetry parsing formats
- Performance optimizations
- Developer tooling improvements

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Creating a Release

**For Maintainers Only**:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.2.3"
   ```

2. **Update CHANGELOG** (if exists) with release notes

3. **Commit changes**:
   ```bash
   git add pyproject.toml
   git commit -m "chore: bump version to 1.2.3"
   git push
   ```

4. **Create a GitHub Release**:
   - Go to [Releases](https://github.com/scadable/library-python/releases)
   - Click "Draft a new release"
   - Tag version: `v1.2.3`
   - Release title: `v1.2.3`
   - Description: Summarize changes
   - Publish release

5. **Automated deployment**:
   - GitHub Actions workflow automatically publishes to PyPI
   - Verify at [pypi.org/project/scadable](https://pypi.org/project/scadable/)

## Questions?

- **Issues**: [GitHub Issues](https://github.com/scadable/library-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/scadable/library-python/discussions)
- **Organization Docs**: [Scadable Org](https://github.com/scadable/.github)

Thank you for contributing to Scadable!
