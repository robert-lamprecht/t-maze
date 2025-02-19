
import serial 
ser = serial.Serial('COM3', 115200, timeout=1)


def openValve(valveID, duration):
    out = 'V,'+str(valveID)+','+str(duration)+'\n'
    ser.write(bytes(out,'utf-8'))

    data = ser.readline().decode('ascii')
    return data

trials = 20 

for trial in range(trials): 
    openValve(1,20)
    openValve(2,20)
    
print('done')