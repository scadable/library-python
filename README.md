# Scadable Python SDK

[![PyPi](https://img.shields.io/pypi/v/scadable)](https://pypi.org/project/scadable/)
[![Downloads](https://static.pepy.tech/badge/scadable/month)](https://pepy.tech/project/scadable)
[![Supported Versions](https://img.shields.io/pypi/pyversions/scadable.svg)](https://pypi.org/project/scadable)
[![GitHub issues](https://img.shields.io/badge/issue_tracking-github-blue.svg)](https://github.com/scadable/library-python/issues)
[![GitHub actions status](https://github.com/scadable/library-python/actions/workflows/test-project.yml/badge.svg)](https://github.com/scadable/library-python/actions/workflows/test-project.yml)

**Scadable** is the first fully container-native SCADA platform—built on Kubernetes & NATS and delivered with Python + React SDKs. Forget rigid vendor UIs: craft your own dashboards, deploy in any cloud, and scale to millions of tags in minutes.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [Support](#support)

## Overview

The Scadable Python SDK provides a simple, pythonic interface to interact with the Scadable SCADA platform. Key features include:

- **Live Telemetry Streaming**: Subscribe to real-time device data via WebSocket connections
- **Device Management**: Create and manage multiple devices within a facility
- **Flexible Connection Handling**: Built-in WebSocket support with extensible connection factory pattern
- **Async-First Design**: Fully asynchronous API using Python's `asyncio`
- **Type-Safe**: Full type hints for better IDE support and code quality

### Access & Deployment

- **PyPI Package**: Available at [pypi.org/project/scadable](https://pypi.org/project/scadable/)
- **Installation**: `pip install scadable`
- **Source Code**: [github.com/scadable/library-python](https://github.com/scadable/library-python)
- **Platform**: Requires Python 3.10 or higher
- **Dependencies**: Minimal dependencies (websockets >= 13.0)

## Installation

### Requirements

- Python 3.10 or higher
- pip package manager

### Install from PyPI

```bash
pip install scadable
```

### Install for Development

For contributing to the project, see the [CONTRIBUTING.md](CONTRIBUTING.md) guide.

## Quick Start

Here's a minimal example to get started with Scadable:

```python
import asyncio
from scadable import Facility
from scadable.connection import WebsocketConnectionFactory

# Initialize a facility with your API key
facility = Facility(
    api_key="your-api-key-here",
    connection_factory=WebsocketConnectionFactory(dest_uri="your-scadable-host.com")
)

# Create devices with live connections
devices = facility.create_many_devices(
    device_ids=["device-1", "device-2"],
    create_connection=True
)

# Subscribe to live telemetry for specific devices
@facility.live_telemetry(["device-1", "device-2"])
async def handle_telemetry(data: str):
    print(f"Received data: {data}")
    # Process your telemetry data here

# Start listening for telemetry
async def main():
    await asyncio.gather(*[device.start_live_telemetry() for device in devices])

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Concepts

### Facility

The `Facility` class is your main entry point. It represents a physical or logical facility containing multiple devices.

```python
from scadable import Facility

facility = Facility(api_key="your-api-key")
```

### Devices

Devices represent individual data sources (PLCs, sensors, controllers, etc.) within your facility.

```python
# Create a single device
device = facility.create_device("device-id-123")

# Create multiple devices
devices = facility.create_many_devices(["device-1", "device-2", "device-3"])
```

### Connections

Connections manage the communication channel between your application and the Scadable platform. The SDK provides WebSocket connections out of the box:

```python
from scadable.connection import WebsocketConnectionFactory

# Create a connection factory
factory = WebsocketConnectionFactory(
    dest_uri="scadable.example.com",
    connection_type="wss"  # or "ws" for non-secure
)

facility = Facility(api_key="your-key", connection_factory=factory)
```

### Live Telemetry

Subscribe to real-time data streams using decorators:

```python
# Subscribe to a single device
@facility.live_telemetry("device-1")
async def handler(data: str):
    print(data)

# Subscribe to multiple devices
@facility.live_telemetry(["device-1", "device-2"])
async def multi_handler(data: str):
    # This handler will receive data from both devices
    process_data(data)
```

## Usage Examples

### Example 1: Basic Telemetry Monitoring

```python
import asyncio
from scadable import Facility
from scadable.connection import WebsocketConnectionFactory

async def monitor_devices():
    # Setup
    facility = Facility(
        api_key="your-api-key",
        connection_factory=WebsocketConnectionFactory("your-host.com")
    )

    # Create devices with connections
    device = facility.create_device("sensor-001", create_connection=True)

    # Subscribe to telemetry
    @facility.live_telemetry("sensor-001")
    async def log_data(data: str):
        print(f"Sensor reading: {data}")

    # Start monitoring
    await device.start_live_telemetry()

asyncio.run(monitor_devices())
```

### Example 2: Multiple Device Management

```python
import asyncio
from scadable import Facility
from scadable.connection import WebsocketConnectionFactory

async def monitor_facility():
    facility = Facility(
        api_key="your-api-key",
        connection_factory=WebsocketConnectionFactory("your-host.com")
    )

    # Create multiple devices
    device_ids = ["plc-1", "plc-2", "sensor-1", "sensor-2"]
    devices = facility.create_many_devices(device_ids, create_connection=True)

    # Different handlers for different device groups
    @facility.live_telemetry(["plc-1", "plc-2"])
    async def handle_plc_data(data: str):
        print(f"PLC Data: {data}")

    @facility.live_telemetry(["sensor-1", "sensor-2"])
    async def handle_sensor_data(data: str):
        print(f"Sensor Data: {data}")

    # Start all connections
    await asyncio.gather(*[dev.start_live_telemetry() for dev in devices])

asyncio.run(monitor_facility())
```

### Example 3: Raw Data Processing

For advanced use cases where you need access to raw, unparsed data:

```python
device = facility.create_device("device-1", create_connection=True)

@device.raw_live_telemetry
async def handle_raw(raw_data: str):
    # Process raw data before parsing
    print(f"Raw: {raw_data}")

await device.start_live_telemetry()
```

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                        Facility                         │
│  - Manages API authentication                           │
│  - Coordinates devices and connections                  │
└────────────────┬───────────────────┬────────────────────┘
                 │                   │
        ┌────────▼────────┐  ┌───────▼──────────┐
        │ DeviceManager   │  │ ConnectionFactory │
        │ - Device CRUD   │  │ - Creates conns   │
        └────────┬────────┘  └───────┬───────────┘
                 │                   │
        ┌────────▼────────┐  ┌───────▼───────────┐
        │     Device      │  │   Connection      │
        │ - Telemetry bus │◄─┤ - WebSocket       │
        │ - Event routing │  │ - Send/Receive    │
        └─────────────────┘  └───────────────────┘
```

### Key Design Patterns

1. **Factory Pattern**: `ConnectionFactory` allows for different connection types (WebSocket, HTTP, custom)
2. **Observer Pattern**: Devices use a pub-sub bus for telemetry data distribution
3. **Async/Await**: Fully asynchronous for efficient I/O operations
4. **Decorator Pattern**: Clean syntax for subscribing to telemetry streams

### Tech Stack

- **Language**: Python 3.10+
- **Async Framework**: asyncio (standard library)
- **WebSocket Library**: websockets 13.0+
- **Type System**: Full type hints with Python's typing module

### Package Structure

```
scadable/
├── __init__.py           # Public API exports
├── facility.py           # Facility class
├── device.py             # Device and DeviceManager classes
└── connection.py         # Connection abstractions and WebSocket implementation
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development environment setup
- Code style guidelines
- Testing requirements
- Pull request process

## Support

- **Issues**: Report bugs at [github.com/scadable/library-python/issues](https://github.com/scadable/library-python/issues)
- **Discussions**: Ask questions in GitHub Discussions
- **Documentation**: Full docs at the repository

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
