import asyncio
from scadable import AsyncScadable


async def main():
    client = AsyncScadable()  # reads SCADABLE_API_KEY env var

    print("Streaming live telemetry from gateway 866f4248...\n")

    async with client.gateways.stream("866f4248-b3a4-4e04-8e76-006b5d4a011c") as stream:
        count = 0
        async for event in stream:
            print(f"Event: type={event.type}")
            devices = event.data.get("devices", {})
            for name, info in devices.items():
                print(
                    f"  [{name}] connected={info.get('connected')} protocol={info.get('protocol')}"
                )
                data = info.get("data", {})
                sample = dict(list(data.items())[:5])
                print(f"  Registers: {sample}")
            count += 1
            if count >= 3:
                break

    await client.close()
    print("\nDone!")


asyncio.run(main())
