import struct
from pymodbus.client import ModbusSerialClient as ModbusClient
import time
from om2m import create_cin
def read_modbus_values():
    print("....")	
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

        vll_result = client.read_holding_registers(address=132, count=2, slave=2)
        if not vll_result.isError():
            vll_registers = vll_result.registers
            vll = struct.unpack('>f', struct.pack('>HH', vll_registers[1], vll_registers[0]))[0]
        else:
            vll = None

        # Read voltage from register 40141 (address 140)
        voltage_result = client.read_holding_registers(address=140, count=2, slave=2)
        if not voltage_result.isError():
            voltage_registers = voltage_result.registers
            voltage = struct.unpack('>f', struct.pack('>HH', voltage_registers[1], voltage_registers[0]))[0]
        else:
            voltage = None

        # Read current from register 40149 (address 148)
        current_result = client.read_holding_registers(address=148, count=2, slave=1)
        if not current_result.isError():
            current_registers = current_result.registers
            current = struct.unpack('>f', struct.pack('>HH', current_registers[1], current_registers[0]))[0]
        else:
            current = None
 
 
        # Read frequency from register 40157 (address 156)
        frequency_result = client.read_holding_registers(address=156, count=2, slave=1)
        if not frequency_result.isError():
            frequency_registers = frequency_result.registers
            frequency = struct.unpack('>f', struct.pack('>HH', frequency_registers[1], frequency_registers[0]))[0]
        else:
            frequency = None

        # Read total power from register 40101 (address 100)
        power_result = client.read_holding_registers(address=100, count=2, slave=1)
        if not power_result.isError():
            power_registers = power_result.registers
            power = struct.unpack('>f', struct.pack('>HH', power_registers[1], power_registers[0]))[0]
        else:
            power = None

        # Read Power Factor from register 40117 (address 116)
        pf_result = client.read_holding_registers(address=116, count=2, slave=1)
        if not pf_result.isError():
            pf_registers = pf_result.registers
            power_factor = struct.unpack('>f', struct.pack('>HH', pf_registers[1], pf_registers[0]))[0]
        else:
            power_factor = None

        # Read Energy (Wh Received) from register 40159 (address 158)
        energy_received_result = client.read_holding_registers(address=158, count=2, slave=1)
        if not energy_received_result.isError():
            energy_received_registers = energy_received_result.registers
            energy_received = struct.unpack('>f', struct.pack('>HH', energy_received_registers[1], energy_received_registers[0]))[0]
        else:
            energy_received = None

        return  vll, voltage, current, frequency, power, energy_received, power_factor
    finally:
        client.close()
       
_url = f"http://dev-onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-EM/EM-CR-SB00-02/Data"
if __name__ == "__main__":
    while True:
        
        vll,voltage, current, frequency, power, energy_received, power_factor = read_modbus_values()
        vll = round(vll, 3) if vll is not None else 0.00
        voltage = round(voltage, 3) if voltage is not None else 0.00
        current = round(current, 3) if current is not None else 0.00
        frequency = round(frequency, 3) if frequency is not None else 0.00
        power = round(power, 3) if power is not None else 0.00
        power_factor = round(power_factor, 3) if power_factor is not None else 0.00
        energy_received = round(energy_received, 3) if energy_received is not None else 0.00
        if None not in [voltage, current, frequency, power, power_factor, energy_received]:
            print(f"vll : {round(vll, 3)}\nVoltage : {round(voltage, 3)}\nCurrent : {round(current, 3)},\nFrequency : {round(frequency, 3)}, \nTotal Power : {round(power, 3)},\nPower factor : {round(power_factor, 3)},\nenergy_received : {round(energy_received, 3)}")
            data = (f"[{int(time.time())},{round(vll, 3)},{round(voltage, 3)},{round(current, 3)},{round(frequency, 3)},{round(power, 3)},{round(power_factor, 3)},{round(energy_received, 3)}]")
            try:
                print("send successful")
                create_cin(_url,data)
            except Exception as e:
                print(e)   
        else:
            print("Error reading Modbus values")
        time.sleep(60)