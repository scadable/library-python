import pytest
import scadable
from scadable.device import DeviceManager
from .mock_connection import *


def test_init_default():
    facility = scadable.Facility("apikey")

    assert facility._api_key == "apikey"
    assert isinstance(facility.device_manager, DeviceManager)
    assert facility.connection_factory is None


def test_init_custom():
    dm = DeviceManager()
    cf = TestConnectionFactory()

    facility = scadable.Facility("apikey1", dm, cf)
    assert facility._api_key == "apikey1"
    assert facility.device_manager == dm
    assert facility.connection_factory == cf


def test_create_device_no_conn():
    facility = scadable.Facility("apikey1")

    dev = facility.create_device("abc")

    assert dev.device_id == "abc"
    assert len(facility.device_manager.devices) == 1
    assert facility.device_manager["abc"] == dev


def test_create_device_conn():
    dm = DeviceManager()
    cf = TestConnectionFactory()

    facility = scadable.Facility("apikey1", dm, cf)
    dev = facility.create_device("abc", create_connection=True)

    assert dev.connection is not None


def test_create_device_conn_no_conn():
    facility = scadable.Facility("apikey1")

    with pytest.raises(RuntimeError):
        facility.create_device("abc", create_connection=True)


def test_create_many_devices_no_conn():
    facility = scadable.Facility("apikey1")

    dev = facility.create_many_devices(["abc", "def"])

    assert len(dev) == 2
    assert dev[0].device_id == "abc"
    assert dev[1].device_id == "def"
    assert len(facility.device_manager.devices) == 2


def test_create_many_devices_conn():
    dm = DeviceManager()
    cf = TestConnectionFactory()

    facility = scadable.Facility("apikey1", dm, cf)
    dev = facility.create_many_devices(["mambo", "hachimi"], create_connection=True)

    assert len(dev) == 2
    assert dev[0].connection is not None
    assert dev[1].connection is not None


def test_create_many_devices_conn_no_conn():
    facility = scadable.Facility("teio")

    with pytest.raises(RuntimeError):
        facility.create_many_devices(["mambo", "hachimi"], create_connection=True)


def test_live_telemetry_decorator():
    dm = DeviceManager()
    cf = TestConnectionFactory()

    facility = scadable.Facility(":3", dm, cf)

    facility.create_many_devices(["mambo", "hachimi"], create_connection=True)

    @facility.live_telemetry("mambo")
    def handler(data):
        pass

    assert len(facility.device_manager["mambo"].parsed_bus) == 1
    assert len(facility.device_manager["hachimi"].parsed_bus) == 0

    @facility.live_telemetry(["mambo", "hachimi"])
    def handler1(data):
        pass

    assert len(facility.device_manager["mambo"].parsed_bus) == 2
    assert len(facility.device_manager["hachimi"].parsed_bus) == 1

    with pytest.raises(RuntimeError):
        @facility.live_telemetry(["mambo", "hachimi", "eieimun"])
        def handler2(data):
            pass
