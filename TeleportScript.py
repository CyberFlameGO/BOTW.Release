try:
    import pymem
except:
    from pip._internal import main as pip
    pip(['install', '--user', 'pymem'])

from pymem import Pymem
from datetime import datetime
from pymem import pattern
import struct

def Log(Mensaje, valor = "", tipo = ""):
    hora = datetime.now()
    print(hora.strftime("%H:%M:%S") + ":", Mensaje, valor)
    if tipo == "Error":
        input("Press Enter to continue.")
        exit()

def ConectarConCemu():
    try:
        pm = Pymem("Cemu.exe")
        base_address = pm.base_address

        static = pm.read_ulonglong(base_address + 0x12D8788)

        Log("Connection with Cemu successful.")

    except:
        Log("Cemu.exe does not exist. Please open the emulator.", tipo="Error")
        pm = 0
        static = 0

    return pm, static

def PatternScan(pm, static, patron, multiple=False):
    memory_end = static + 0x50000000
    region = static

    if not multiple:

        address = None

        while address == None and region < memory_end:
            region, address = pattern.scan_pattern_page(pm.process_handle, region, patron)

        if address == None:
            Log("Address not found.", tipo="Error")
    else:

        address = []
        result = []

        while region < memory_end:
            region, result = pattern.scan_pattern_page(pm.process_handle, region, patron, return_multiple=multiple)
        
            if result != None:
                for i in range(len(result)):
                    address.append(result[i])

        if address == None:
            Log("Address not found.")            

    return address

def from_bigEndianFloat(value):
    value = struct.pack('<f', value)
    value = int.from_bytes(value, 'big')
    return value

patron2 = rb".\xff\xff\xff\xf1\x3f...\x80\x00..\x11...\x10\xdf..\x00\x00\x00\x01\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3f\x80"

pm, static = ConectarConCemu()

PositionAddress = PatternScan(pm, static, patron2) + 0xD5

SavedPositions = {
    "Great Plateau Battle Royale Platform": [-885.676758, 590.46582, 1765.28833]
}

print("Select the position you want to teleport to:")

counter = 0

for place in SavedPositions:
    print(f"({counter}) {place}")
    counter += 1

while(True):
    number = int(input("Input: "))

    PositionToWrite = list(SavedPositions.values())[number]

    for i in range(3):
        pm.write_uint(PositionAddress + (0x4 * i), from_bigEndianFloat(PositionToWrite[i]))
