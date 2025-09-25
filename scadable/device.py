import asyncio
from typing import Callable, Awaitable, Any
from .connection import Connection


class DeviceManager:
    """
    A class to manage created Devices

    Instance attributes:
        devices: dict that maps deviceid->Device
    """

    def __init__(self):
        self.devices: dict[str, Device] = {}

    def __getitem__(self, device_id: str) -> "Device":
        """
        Returns a device from a device id

        :param device_id: device id
        :return: Device with associated device id
        """
        return self.devices[device_id]

    def __contains__(self, device_id):
        """
        Returns whether device id is created

        :param device_id: device id
        :return: If device id is created
        """
        return device_id in self.devices

    def create_device(self, device_id: str, connection: Connection | None) -> "Device":
        """
        Creates a device if not already created, otherwise return the already created one

        :param device_id: ID of the device we connect to
        :param connection: The connection that should be used for live_telemetry
        :return: Created device
        """
        if device_id in self.devices:
            device = self.devices[device_id]
        else:
            device = Device(device_id=device_id, connection=connection)
            self.devices[device_id] = device

        return device

    def remove_device(self, device_id: str):
        """
        Removes a device from our manager

        :param device_id: Device Id to remove
        :return:
        """
        if device_id in self.devices:
            device = self.devices[device_id]  # noqa
            # TODO: figure out what to do here
            del self.devices[device_id]


class Device:
    """
    A class that represents a single device

    Instance attributes:
        connection: connection that the device will read messages from
        device_id: device id of the device
        raw_bus: set of subscribed handlers that will be called when receiving a raw response
        parsed_bus: set of subscribed handlers that will be called after parsing a response
    """

    def __init__(self, device_id: str, connection: Connection | None):
        self.connection = connection
        self.device_id = device_id

        # Bus that contains all functions that handle raw data
        self.raw_bus: set[Callable[[str], Awaitable[Any]]] = set()
        # Bus that contains all functions that handle parsed data
        self.parsed_bus: set[Callable[[str], Awaitable[Any]]] = set()

    def raw_live_telemetry(self, subscriber: Callable[[str], Awaitable]):
        """
        Decorator that adds a function to our bus
        Throws an error if no connection was specified

        :param subscriber: Function that subscribes to raw data
        :return: subscriber
        """
        if not self.connection:
            raise RuntimeError(
                f"No connection was specified for device {self.device_id}"
            )

        self.raw_bus.add(subscriber)
        return subscriber

    def live_telemetry(self, subscriber: Callable[[str], Awaitable]):
        """
        Decorator that adds a function to our bus
        Throws an error if no connection was specified

        :param subscriber: Function that subscribes to raw data
        :return: subscriber
        """
        if not self.connection:
            raise RuntimeError(
                f"No connection was specified for device {self.device_id}"
            )

        self.parsed_bus.add(subscriber)
        return subscriber

    async def _handle_raw(self, data: str):
        """
        Internal method to parse raw data and send it to a different bus
        :param data: raw data that was received by the connection
        :return: None
        """
        await asyncio.gather(*[s(data) for s in self.raw_bus])
        # TODO: parse data
        await asyncio.gather(*[s(data) for s in self.parsed_bus])

    async def start_live_telemetry(self):
        """
        Starts the connection to the server to receive live telemetry for this particular device
        This function is called when we want to initialize a connection to a single device

        :return: None
        """
        if self.connection:
            await self.connection.connect(self._handle_raw)
        else:
            raise RuntimeError(
                f"No connection was specified for device {self.device_id}"
            )
