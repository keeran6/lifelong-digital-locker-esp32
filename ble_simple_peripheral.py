"""
Simple BLE Peripheral for ESP32 MicroPython
Simplified BLE UART service implementation
"""

import bluetooth
from ble_advertising import advertising_payload
from micropython import const
import struct

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


class BLESimplePeripheral:
    def __init__(self, name="T8-Lock"):
        try:
            self._ble = bluetooth.BLE()
            self._ble.active(True)
            self._ble.irq(self._irq)
            ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
            self._connections = set()
            self._write_callback = None
            self.device_name = name
            self.service_uuid = _UART_UUID
            self._advertise()
        except Exception as e:
            print(f"BT: Init error: {e}")
            raise

    def _irq(self, event, data):
        # Track connections with error handling
        try:
            if event == _IRQ_CENTRAL_CONNECT:
                conn_handle, _, _ = data
                print("BT: Device connected")
                self._connections.add(conn_handle)
            elif event == _IRQ_CENTRAL_DISCONNECT:
                conn_handle, _, _ = data
                print("BT: Device disconnected")
                self._connections.discard(conn_handle)  # Use discard instead of remove
                self._advertise()
            elif event == _IRQ_GATTS_WRITE:
                conn_handle, value_handle = data
                if value_handle == self._handle_rx and self._write_callback:
                    try:
                        value = self._ble.gatts_read(value_handle)
                        if value:  # Only call callback if we got valid data
                            self._write_callback(value)
                    except Exception as e:
                        print(f"BT: Callback error: {e}")
        except Exception as e:
            print(f"BT: IRQ error (event={event}): {e}")

    def send(self, data):
        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, (bytes, bytearray)):
            data = str(data).encode('utf-8')

        # Make a copy of connections to avoid modification during iteration
        connections_copy = list(self._connections)
        for conn_handle in connections_copy:
            try:
                self._ble.gatts_notify(conn_handle, self._handle_tx, data)
            except Exception as e:
                print(f"BT: Send error on handle {conn_handle}: {e}")
                # Remove invalid connection
                try:
                    self._connections.discard(conn_handle)
                except:
                    pass

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        try:
            print("BT: Advertising with two payloads......")
            adv_data = advertising_payload(name=self.device_name)
            resp_data = advertising_payload(services=[self.service_uuid])
            if len(adv_data) <= 31 and len(resp_data) <= 31:
                print(f"BT: Advertising (Adv Len: {len(adv_data)}, Resp Len: {len(resp_data)})")
                # Pass BOTH payloads to the gap_advertise function
                if self._ble and hasattr(self._ble, 'gap_advertise'):
                    self._ble.gap_advertise(interval_us, adv_data=adv_data, resp_data=resp_data)
            else:
                # This should ideally not happen now
                print(f"Error: Payloads still too long. Adv len: {len(adv_data)}, Resp len: {len(resp_data)}")
        except Exception as e:
            print(f"BT: Advertise error: {e}")

    def on_write(self, callback):
        self._write_callback = callback
