import serial 
import time
ser = serial.Serial('COM3', 115200, timeout=1)


def openValve(valveID, duration):
    out = 'V,'+str(valveID)+','+str(duration)+'\n'
    ser.write(bytes(out,'utf-8'))

    data = ser.readline().decode('ascii')
    return data

trials =20

#pre-traial water testing
# for trial in range(trials): 
#     openValve(1,1000)
#     openValve(2,50)
    

#lick amount calculation
for trial in range(trials): 
    openValve(1,5 )
    openValve(2, 5)
    

print('done')