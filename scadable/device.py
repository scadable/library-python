import asyncio
from typing import Callable, Awaitable, Any
from scadable.connection import ConnectionFactory, Connection


class DeviceManager:
    """
    A class to manage created Devices

    Instance attributes:
        connection_factory: Connection Factory
        devices: dict that maps deviceid->Device
    """

    def __init__(self, connection_factory: ConnectionFactory):
        self.connection_factory = connection_factory
        self.devices: dict[str, Device] = {}

    def create_device(
        self, api_key: str, device_id: str, create_connection: bool = False
    ):
        """
        Creates a device if not already created, otherwise return the already created one

        :param api_key: API key to be used to create the device
        :param device_id: ID of the device we connect to
        :param create_connection: Whether or not to create a connection (to be used with live telemetry), defaults to False
        :return: Created device
        """
        if device_id in self.devices:
            device = self.devices[device_id]
        else:
            conn = (
                self.connection_factory.create_connection(
                    api_key=api_key, device_id=device_id
                )
                if create_connection
                else None
            )
            device = Device(device_id=device_id, connection=conn)
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
    """

    def __init__(self, device_id: str, connection: Connection | None):
        self.connection = connection
        self.device_id = device_id

        # Bus that contains all functions that handle raw data
        self.raw_bus: set[Callable[[str], Awaitable[Any]]] = set()

    def raw_live_telemetry(self, subscriber: Callable[[str], Awaitable]):
        """
        Decorator that adds a function to our bus
        :param subscriber: Function that subscribes to raw data
        :return: subscriber
        """
        self.raw_bus.add(subscriber)
        return subscriber

    async def _handle_raw(self, data: str):
        """
        Internal method to prase raw data and send it to a different bus
        :param data: raw data that was received by the connection
        :return: None
        """
        await asyncio.gather(*[s(data) for s in self.raw_bus])

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
