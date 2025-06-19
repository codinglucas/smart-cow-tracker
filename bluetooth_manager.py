import asyncio
from bleak import BleakScanner
from bleak.exc import BleakError
from PyQt5.QtCore import QThread, pyqtSignal
import time
import platform

class BluetoothManager(QThread):
    connection_status = pyqtSignal(bool)
    error_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.is_connected = False
        self.loop = None
        self.bluetooth_available = self.check_bluetooth_support()

    def check_bluetooth_support(self):
        try:
            # Create a temporary event loop to check Bluetooth
            temp_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(temp_loop)
            
            # Try to create a scanner
            temp_loop.run_until_complete(BleakScanner.discover(timeout=1))
            temp_loop.close()
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if "bluetooth" in error_msg and ("adapter" in error_msg or "not found" in error_msg):
                self.error_message.emit("Bluetooth adapter not found. Please ensure your device supports Bluetooth and it is enabled.")
            else:
                self.error_message.emit(f"Bluetooth error: {str(e)}")
            return False

    async def scan_devices(self):
        if not self.bluetooth_available:
            if self.is_connected:
                self.is_connected = False
                self.connection_status.emit(False)
            time.sleep(5)  # Wait longer between checks when Bluetooth is not available
            return

        try:
            devices = await BleakScanner.discover()
            if devices:
                if not self.is_connected:
                    self.is_connected = True
                    self.connection_status.emit(True)
            else:
                if self.is_connected:
                    self.is_connected = False
                    self.connection_status.emit(False)
        except Exception as e:
            print(f"Bluetooth scan error: {e}")
            if self.is_connected:
                self.is_connected = False
                self.connection_status.emit(False)
            self.error_message.emit(f"Bluetooth scan error: {str(e)}")

    def run(self):
        if not self.bluetooth_available:
            self.error_message.emit("Bluetooth is not available on this device")
            self.connection_status.emit(False)
            return

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        while self.is_running:
            self.loop.run_until_complete(self.scan_devices())
            time.sleep(2)

    def stop(self):
        self.is_running = False
        if self.loop:
            self.loop.close()
        self.wait()