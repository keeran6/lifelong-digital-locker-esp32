"""
Unit tests for BLE advertising module
Uses mocks to test without actual Bluetooth hardware
"""

import pytest
import struct
from unittest.mock import Mock, patch


# Mock MicroPython modules
class MockMicropython:
    @staticmethod
    def const(value):
        return value


@pytest.fixture(autouse=True)
def mock_micropython_modules(monkeypatch):
    """Mock MicroPython-specific modules"""
    monkeypatch.setitem(__builtins__.__dict__, 'micropython', MockMicropython())


def test_advertising_payload_with_name():
    """Test advertising payload generation with device name"""
    # Import after mocking
    from ble_advertising import advertising_payload

    # Test with string name
    payload = advertising_payload(name="TestDevice")

    assert isinstance(payload, bytearray)
    assert len(payload) > 0
    assert len(payload) <= 31  # BLE advertising payload limit

    # Check that name is encoded
    assert b"TestDevice" in bytes(payload)


def test_advertising_payload_with_services():
    """Test advertising payload with service UUIDs"""
    from ble_advertising import advertising_payload

    # Mock a 128-bit UUID (16 bytes)
    mock_uuid = Mock()
    mock_uuid.__bytes__ = Mock(return_value=b'\x00' * 16)

    payload = advertising_payload(services=[mock_uuid])

    assert isinstance(payload, bytearray)
    assert len(payload) > 0


def test_advertising_payload_size_limit():
    """Test that payload respects BLE 31-byte limit"""
    from ble_advertising import advertising_payload

    # Short name should fit
    payload = advertising_payload(name="T8")
    assert len(payload) <= 31

    # Very long name should still be created (may exceed limit)
    long_name = "A" * 50
    payload = advertising_payload(name=long_name)
    assert isinstance(payload, bytearray)


def test_advertising_payload_empty():
    """Test advertising payload with no parameters"""
    from ble_advertising import advertising_payload

    payload = advertising_payload()

    assert isinstance(payload, bytearray)
    # Should still contain flags
    assert len(payload) >= 3


def test_advertising_payload_flags():
    """Test advertising flags are correctly set"""
    from ble_advertising import advertising_payload

    payload_discoverable = advertising_payload(limited_disc=True)
    payload_normal = advertising_payload(limited_disc=False)

    # Both should have flags, but different values
    assert isinstance(payload_discoverable, bytearray)
    assert isinstance(payload_normal, bytearray)
    assert payload_discoverable != payload_normal


def test_name_encoding():
    """Test that string names are properly encoded to bytes"""
    from ble_advertising import advertising_payload

    # Test with various string types
    names = ["ASCII", "UTF-8", "Test123"]

    for name in names:
        payload = advertising_payload(name=name)
        assert isinstance(payload, bytearray)
        assert name.encode('utf-8') in bytes(payload)


def test_appearance():
    """Test advertising with appearance code"""
    from ble_advertising import advertising_payload

    appearance_code = 512  # Generic phone
    payload = advertising_payload(appearance=appearance_code)

    assert isinstance(payload, bytearray)
    assert len(payload) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
