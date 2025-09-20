from .device import DeviceManager, Device
from .connection import ConnectionFactory


class Facility:
    """
    A class to manage everything related to a Facility

    Instance attributes:
        device_manager: DeviceManager, a default one is created if not specified
        connection_factory: ConnectionFactory that is used to init long lived connections (e.g. websockets) for live telemetry
    """

    def __init__(
        self,
        api_key: str,
        device_manager: DeviceManager | None = None,
        connection_factory: ConnectionFactory | None = None,
    ):
        """
        Initializes the Facility Class

        :param api_key: API Key associated with the facility
        :param device_manager: Optional if you want to specify your own device manager, default is created
        :param connection_factory: Optional if you want to specify your own connection factory, otherwise none is specified
        """
        self._api_key = api_key

        if device_manager:
            self.device_manager = device_manager
        else:
            self.device_manager = DeviceManager()

        if connection_factory:
            self.connection_factory = connection_factory
        else:
            self.connection_factory = None

    def create_device(self, device_id: str, create_connection=False) -> Device:
        """
        Creates a device associated with the factory

        :param device_id: Device id to be created
        :param create_connection: Whether to create a connection for each device to be used in live telemetry, default is False
        :return: Created device
        """
        if create_connection:
            if self.connection_factory:
                conn = self.connection_factory.create_connection(
                    api_key=self._api_key, device_id=device_id
                )
            else:
                raise RuntimeError(
                    "Facility was never initialized with a connection factory"
                )
        else:
            conn = None

        return self.device_manager.create_device(device_id, conn)

    def create_many_devices(
        self, device_ids: list[str], create_connection=False
    ) -> list[Device]:
        """
        Creates many devices associated with the factory

        :param device_ids: List of device ids to be created
        :param create_connection: Whether to create a connection for each device to be used in live telemetry, default is False
        :return: List of created devices
        """
        return [
            self.create_device(device_id=i, create_connection=create_connection)
            for i in device_ids
        ]

    def live_telemetry(self, device_ids: list[str] | str):
        """
        Decorator to register a function with device id(s)

        :param device_ids: Single device (str) or multiple devices list(str)
        :return: Function
        """
        if isinstance(device_ids, str):
            device_ids = [device_ids]

        def decorator(subscriber):
            if not (
                error_device_ids := [
                    i for i in device_ids if i not in self.device_manager
                ]
            ):
                for d_id in device_ids:
                    self.device_manager[d_id].live_telemetry(subscriber=subscriber)
            else:
                raise RuntimeError(
                    f"Device ids: {error_device_ids} were not found in device manager"
                )

            return subscriber

        return decorator
