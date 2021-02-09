import serial.tools.list_ports
import serial
import struct

def checkPacemakerDevice():
    for comport in serial.tools.list_ports.comports():
        if (comport.pid == 14155 and comport.vid == 1155): #vendor and product ID for given pacemaker device
            return comport.device
            #print(comport.device)
    return False

def sendSerialInfo(fnCode, user):
    output = []
    modeVal = 0
    rateAdaptive = 0

    modes = {"AOO": 1, "VOO": 2, "AAI": 3, "VVI": 4, "DOO": 5, "AOOR": 6, "VOOR": 7, "AAIR": 8, "VVIR": 9, "DOOR": 10}
    for key in modes:
        if key == user['Mode']:
            if (modes[key] > 5):
                modeVal = modes[key] - 5
                rateAdaptive = 1
            else:
                modeVal = modes[key]

    atrDutyCycle = int(float(user['AA'])/5*100)
    ventDutyCycle = int(float(user['VA'])/5*100)
    apw = int(user['APW'])

    output.append((fnCode).to_bytes(1, byteorder="big"))
    output.append((modeVal).to_bytes(1, byteorder="big"))
    output.append((rateAdaptive).to_bytes(1, byteorder="big"))
    output.append((atrDutyCycle).to_bytes(1, byteorder="big"))
    output.append((ventDutyCycle).to_bytes(1, byteorder="big"))
    output.append((apw).to_bytes(1, byteorder="big"))
    output.append((int(user['VPW'])).to_bytes(1, byteorder="big"))
    output.append((int(user['LRL'])).to_bytes(1, byteorder="big"))
    output.append((int(user['URL'])).to_bytes(1, byteorder="big"))
    output.append((int(user['ARP'])).to_bytes(2, byteorder="big"))
    output.append((int(user['VRP'])).to_bytes(2, byteorder="big"))
    output.append((int(user['FAVD'])).to_bytes(2, byteorder="big"))
    output.append((int(user['RF'])).to_bytes(1, byteorder="big"))
    output.append((int(user['ReactTime'])).to_bytes(1, byteorder="big"))
    output.append((int(user['RecovTime'])).to_bytes(1, byteorder="big"))
    output.append((int(user['MSR'])).to_bytes(1, byteorder="big"))

    ser = serial.Serial(port=checkPacemakerDevice(), baudrate=115200)
    transmittedData = bytearray(b''.join(output))

    ser.write(transmittedData)