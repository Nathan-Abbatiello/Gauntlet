import asyncio
from bleak import BleakScanner
from bleak import BleakClient

address = "34:85:18:71:74:C5" 
CHR_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"

async def scan():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

async def read_characteristic(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(CHR_UUID)
        print("characteristic: {0}".format("".join(map(str, model_number))))

async def write_characteristic(address, data:bytearray):
    async with BleakClient(address) as client:
        await client.write_gatt_char(CHR_UUID, data)
        print("written")

async def getServices(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print('service', service.handle, service.uuid, service.description)
            characteristics = service.characteristics
            for char in characteristics:
                print ('characteristics', char.handle, char.uuid, char.description, char.properties)
                descriptors = char.descriptors
                for desc in descriptors:
                    print("  descriptor", desc)

asyncio.run(scan())
asyncio.run(write_characteristic(address, b"\x11"))
asyncio.run(read_characteristic(address))
# asyncio.run(getServices(address))
