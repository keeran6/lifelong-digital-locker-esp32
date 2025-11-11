"""
Unit tests for BLE Simple Peripheral module
Uses mocks to simulate Bluetooth functionality
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call


# Mock MicroPython modules
class MockBluetooth:
    class BLE:
        def __init__(self):
            self.active_state = False
            self.irq_handler = None
            self.services = []

        def active(self, state=None):
            if state is not None:
                self.active_state = state
            return self.active_state

        def irq(self, handler):
            self.irq_handler = handler

        def gatts_register_services(self, services):
            self.services = services
            # Return mock handles
            return [[(1, 2)]]

        def gatts_notify(self, conn_handle, value_handle, data):
            pass

        def gatts_read(self, value_handle):
            return b"test_data"

        def gap_advertise(self, interval, adv_data=None, resp_data=None):
            pass

    class UUID:
        def __init__(self, uuid_str):
            self.uuid_str = uuid_str

        def __bytes__(self):
            return b'\x00' * 16


@pytest.fixture
def mock_bluetooth(monkeypatch):
    """Mock bluetooth module"""
    bluetooth_mock = MockBluetooth()
    monkeypatch.setattr('bluetooth.BLE', bluetooth_mock.BLE)
    monkeypatch.setattr('bluetooth.UUID', bluetooth_mock.UUID)
    return bluetooth_mock


@pytest.fixture
def mock_advertising(monkeypatch):
    """Mock advertising module"""
    mock_adv = Mock(return_value=bytearray(b'\x00' * 10))
    monkeypatch.setattr('ble_advertising.advertising_payload', mock_adv)
    return mock_adv


def test_ble_peripheral_init(mock_bluetooth, mock_advertising):
    """Test BLE peripheral initialization"""
    from ble_simple_peripheral import BLESimplePeripheral

    # Should initialize without errors
    peripheral = BLESimplePeripheral(name="TestDevice")

    assert peripheral is not None
    assert peripheral.device_name == "TestDevice"
    assert len(peripheral._connections) == 0


def test_ble_peripheral_init_error(monkeypatch):
    """Test BLE peripheral initialization error handling"""
    # Mock BLE to raise exception
    mock_ble = Mock(side_effect=Exception("BLE init failed"))
    monkeypatch.setattr('bluetooth.BLE', mock_ble)

    from ble_simple_peripheral import BLESimplePeripheral

    with pytest.raises(Exception):
        BLESimplePeripheral(name="TestDevice")


def test_send_string_data(mock_bluetooth, mock_advertising):
    """Test sending string data (should convert to bytes)"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")
    peripheral._connections.add(1)

    # Mock gatts_notify
    peripheral._ble.gatts_notify = Mock()

    # Send string
    peripheral.send("Hello World")

    # Should have called gatts_notify with bytes
    peripheral._ble.gatts_notify.assert_called_once()
    call_args = peripheral._ble.gatts_notify.call_args
    assert isinstance(call_args[0][2], bytes)


def test_send_bytes_data(mock_bluetooth, mock_advertising):
    """Test sending bytes data"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")
    peripheral._connections.add(1)

    peripheral._ble.gatts_notify = Mock()

    # Send bytes
    test_data = b"Binary data"
    peripheral.send(test_data)

    peripheral._ble.gatts_notify.assert_called_once()
    call_args = peripheral._ble.gatts_notify.call_args
    assert call_args[0][2] == test_data


def test_send_to_multiple_connections(mock_bluetooth, mock_advertising):
    """Test sending data to multiple connections"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")
    peripheral._connections.add(1)
    peripheral._connections.add(2)
    peripheral._connections.add(3)

    peripheral._ble.gatts_notify = Mock()

    peripheral.send("Test")

    # Should be called for each connection
    assert peripheral._ble.gatts_notify.call_count == 3


def test_send_error_handling(mock_bluetooth, mock_advertising):
    """Test error handling when sending fails"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")
    peripheral._connections.add(1)

    # Mock send to raise exception
    peripheral._ble.gatts_notify = Mock(side_effect=Exception("Send failed"))

    # Should not raise exception (error handled internally)
    peripheral.send("Test")

    # Connection should be removed after error
    assert len(peripheral._connections) == 0


def test_is_connected(mock_bluetooth, mock_advertising):
    """Test connection status check"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")

    assert peripheral.is_connected() is False

    peripheral._connections.add(1)
    assert peripheral.is_connected() is True

    peripheral._connections.clear()
    assert peripheral.is_connected() is False


def test_on_write_callback(mock_bluetooth, mock_advertising):
    """Test setting write callback"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")

    callback = Mock()
    peripheral.on_write(callback)

    assert peripheral._write_callback == callback


def test_irq_connect_event(mock_bluetooth, mock_advertising):
    """Test IRQ handler for connection event"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")

    # Simulate connection event (event=1)
    peripheral._irq(1, (123, None, None))

    assert 123 in peripheral._connections


def test_irq_disconnect_event(mock_bluetooth, mock_advertising):
    """Test IRQ handler for disconnection event"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")
    peripheral._connections.add(123)

    # Mock advertise
    peripheral._advertise = Mock()

    # Simulate disconnect event (event=2)
    peripheral._irq(2, (123, None, None))

    assert 123 not in peripheral._connections
    peripheral._advertise.assert_called_once()


def test_irq_write_event_with_callback(mock_bluetooth, mock_advertising):
    """Test IRQ handler for write event with callback"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")

    callback = Mock()
    peripheral.on_write(callback)

    # Simulate write event (event=3)
    peripheral._irq(3, (123, 2))  # 2 is RX handle

    callback.assert_called_once()


def test_irq_error_handling(mock_bluetooth, mock_advertising):
    """Test IRQ error handling"""
    from ble_simple_peripheral import BLESimplePeripheral

    peripheral = BLESimplePeripheral(name="TestDevice")

    # Simulate event with invalid data (should not crash)
    peripheral._irq(999, None)

    # Should handle gracefully
    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
