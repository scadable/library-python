# Scadable Python SDK

[![PyPi](https://img.shields.io/pypi/v/scadable)](https://pypi.org/project/scadable/)
[![Downloads](https://static.pepy.tech/badge/scadable/month)](https://pepy.tech/project/scadable)
[![Supported Versions](https://img.shields.io/pypi/pyversions/scadable.svg)](https://pypi.org/project/scadable)
[![GitHub actions status](https://github.com/scadable/library-python/actions/workflows/test-project.yml/badge.svg)](https://github.com/scadable/library-python/actions/workflows/test-project.yml)

The official Python SDK for the [Scadable](https://scadable.com) IoT platform. Check gateway status, list devices, and stream live telemetry in 3 lines of code.

## Install

```bash
pip install scadable
```

## Quick Start

```python
from scadable import Scadable

client = Scadable(api_key="sk_live_...")

# List gateways
for gw in client.gateways.list():
    print(f"{gw.name}: {gw.status}")

# Get gateway detail
gw = client.gateways.get("gateway-id")
print(gw.name, gw.status)

# List devices on a gateway
for device in client.gateways.devices("gateway-id"):
    print(f"{device.name} [{device.status}]")
```

## Stream Live Telemetry

```python
import asyncio
from scadable import AsyncScadable

async def main():
    client = AsyncScadable(api_key="sk_live_...")

    async with client.gateways.stream("gateway-id") as stream:
        async for event in stream:
            print(event.type, event.data)

asyncio.run(main())
```

## Authentication

Pass your API key directly or set it as an environment variable:

```python
# Direct
client = Scadable(api_key="sk_live_...")

# Environment variable
# export SCADABLE_API_KEY=sk_live_...
client = Scadable()
```

API keys are created in the [Scadable Dashboard](https://dashboard.scadable.com) under project settings.

## Error Handling

```python
from scadable import Scadable, AuthenticationError, NotFoundError

client = Scadable(api_key="sk_live_...")

try:
    gw = client.gateways.get("bad-id")
except NotFoundError:
    print("Gateway not found")
except AuthenticationError:
    print("Invalid API key")
```

## Requirements

- Python 3.10+
- Dependencies: `httpx`, `pydantic`, `websockets`

## License

Apache 2.0
