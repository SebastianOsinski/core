from serial import Serial
import asyncio

CONST_ON = b"\xA0\x01\x01\xA2"
CONST_OFF = b"\xA0\x01\x00\xA1"


class GarageRemote:
    def __init__(self, serialPort, pressTime):
        self.serial = Serial(serialPort)
        self.pressTime = pressTime

    async def press(self):
        self.serial.write(CONST_ON)

        await asyncio.sleep(self.pressTime)

        self.serial.write(CONST_OFF)
