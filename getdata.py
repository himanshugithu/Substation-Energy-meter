import struct
from pymodbus.client import ModbusSerialClient as ModbusClient
import time
from om2m import create_cin

def read_modbus_values(slave_id):
    client = ModbusClient(
        port="/dev/ttyUSB0",  # Adjust to your serial port
        baudrate=9600,
        parity='E',
        stopbits=1,
        bytesize=8,
        timeout=1
    )
    try:
        client.connect()

        # Helper function to read and parse register values
        def read_register(address, count=2):
            result = client.read_holding_registers(address=address, count=count, slave=slave_id)
            if not result.isError():
                registers = result.registers
                return struct.unpack('>f', struct.pack('>HH', registers[1], registers[0]))[0]
            return None

        vll = read_register(132)
        voltage = read_register(140)
        current = read_register(148)
        frequency = read_register(156)
        power = read_register(100)
        power_factor = read_register(116)
        energy_received = read_register(158)

        return vll, voltage, current, frequency, power, energy_received, power_factor
    finally:
        client.close()

_url = "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-EM/EM-CR-SB00-00/Data"

if __name__ == "__main__":
    meter_ids = [1, 2, 3, 4, 5]  # List of meter IDs

    while True:
        timestamp = int(time.time())  # Generate a single timestamp for all meters
        all_meter_data = [timestamp]  # Start the list with the timestamp

        for meter_id in meter_ids:
            print(f"Reading data from Meter ID: {meter_id}")
            vll, voltage, current, frequency, power, energy_received, power_factor = read_modbus_values(meter_id)

            # Ensure all values are numeric
            vll = round(vll, 3) if vll is not None else 0.0
            voltage = round(voltage, 3) if voltage is not None else 0.0
            current = round(current, 3) if current is not None else 0.0
            frequency = round(frequency, 3) if frequency is not None else 0.0
            power = round(power, 3) if power is not None else 0.0
            power_factor = round(power_factor, 3) if power_factor is not None else 0.0
            energy_received = round(energy_received, 3) if energy_received is not None else 0.0

            # Add meter data directly to the consolidated list
            all_meter_data.extend([
                vll, voltage, current, frequency, power, power_factor, energy_received
            ])

            print(f"Meter ID {meter_id} Data:")
            print([vll, voltage, current, frequency, power, power_factor, energy_received])

        # Send the consolidated data for all meters
        try:
            print("Sending consolidated data for all meters...")
            print(all_meter_data)  # Debug print for verification
            print(len(all_meter_data))
            create_cin(_url,all_meter_data)  # Convert the list to a string for transmission
            
        except Exception as e:
            print(f"Error sending consolidated data: {e}")

        print("Waiting before next read cycle...")
        time.sleep(60)
