import serial
import time
# import tkinter as tk

# window = tk.Tk()

# greeting = tk.Label(text='Maze GUI')



# valveButton = tk.Button(
#     text="Open Valve",
#     width=25,
#     height=5,
#     bg='red',
#     fg='white')

# greeting.pack()
# valveButton.pack()
# window.mainloop()



ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)

def write_read(x):
    ser.write(bytes(x, 'utf-8'))
    time.sleep(0.01)
    data = ser.readline().decode('ascii')
    return data

def openValve(valveID, duration):
    out = 'V,'+valveID+','+duration+'\n'
    ser.write(bytes(out, 'utf-8'))
    time.sleep(0.01)
    data = ser.readline().decode('ascii')
    return data


while (True):
    num = input("Enter a string: ")+'\n' # Taking input from user
    value = write_read(num)
    print(value) # printing the value