import serial
import time
import numpy as np
import json
import datetime




animaldict = {
    'BFL4': {
        'F,1':'right(V2)',
        'F,2':'right(V2)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
    },
    'BHH6': {
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
        
    },
     'BHH2': {
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
     },
     
    'BHH3': {
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)',
        'F,4':'right(V2)'
        },
    'BHH4': {
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)',
        'F,4':'right(V2)'
        },
    'BFL5': {
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'       
    },
    'BFL3': {
        'F,1':'right(V2)',
        'F,2':'right(V2)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'      
    
    },
    'BFL2': {
        'F,1':'left(V1)',
        'F,2':'left(V1)',
        'F,3':'left(V1)',
        'F,4':'right(V2)'
        },
    'BFL1': {
        'F,1':'left(V1)',
        'F,2':'left(V1)',
        'F,3':'left(V1)',
        'F,4':'right(V2)',
        },
     'BDY2': {
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
        },
    'BDY4': {
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        # 'F,3':'right(V2)',
        # 'F,4':'left(V1)'
        },
    'BDY5': {
        'F,1':'left(V1)',
        'F,2':'right(V2)'
        # 'F,3':'left(V1)', 
        # 'F,4':'right(V2)'
        },
    'BFZ1': {
        'F,1':'left(V1)',
        'F,2':'left(V1)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
        },
    'BFZ2': {
        'F,1':'left(V1)',
        'F,2':'left(V1)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
        },
    'BFZ3': {
        'F,1':'left(V1)',
        'F,2':'left(V1)', 
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
        },
    'BEB5': {#BEBs are modified for I/S
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
        },
     'BEB2': {
        'F,1':'right(V2)',
        'F,2':'right(V2)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
        },
     'BEB3': {
        'F,1':'left(V1)',
        'F,2':'left(V1)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
        },
     'BEB4': {
        'F,1':'left(V1)',
        'F,2':'left(V1)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
        },        
     
    'BCU1': {
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
        },
    'BCU4': {
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)', 
        'F,4':'left(V1)'
        },
    'BCU5': {
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
    },
    'BDE1': {
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'     
    },
    'BBC6': {
       'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
    },
    'BBN1': {
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
    },
    'BBN2': {
       'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
    },
    'BBN6': {
       'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
    },
    'BDB3': {
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
        },
    'BDC5': {
        'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)', 
        'F,4':'left(V1)'
        },
    'BDB5': {
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
    },
    'BDB4': {
       'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
    },
    'BDB1': {
       'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
    },
    'BDC3': {
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
    },
    'BDC4': {
       'F,1':'right(V2)',
        'F,2':'left(V1)',
        'F,3':'right(V2)',
        'F,4':'left(V1)'
    },
    'BDB2': {
       'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'  

    },
    'TEST': {#same as BBC1, BBN1, and BBN6
        'F,1':'left(V1)',
        'F,2':'right(V2)',
        'F,3':'left(V1)', 
        'F,4':'right(V2)'
    }
}


#floor_level = ser.readline().decode('ascii')
# is not none stamnet will check is there is a value assined to a vaiable
#print('initializing')
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)
print('Loading......')

def floorLevel(level):
    out = 'F,'+str(level)+'\n'
    ser.write(bytes(out,'utf-8'))
    time.sleep(0.01)
    data = ser.readline().decode('ascii')
    return data
def initialize():
    out = 'Z'
    ser.write(bytes(out, 'utf-8'))
    time.sleep(0.01)
    door_stat(1,0)

    time.sleep(0.01)
    door_stat(2,0)
    time.sleep(0.01)
    door_stat(3,0)
    time.sleep(0.01)
    door_stat(4,0)

    global MazeTexture
    global coneHeight_1
    global coneHeight_2

    global gratings_floor1
    global gratings_floor2
    global texture_foor_g_3
    global texture_foor_g_4
    
    while True:
        MazeTexture = input('What is the texture? R/S(rough vs smooth) or I/S (Intermediate rough texture vs smooth) or C (rough vs smooth for CNO experiment) or G(direction gratings) or S(smooth only): ')
        if MazeTexture not in ['R/S','I/S','C','G', 'S','G+R/S']:
            print('not a texture')
        else:
            break

    while True:
        if MazeTexture == 'I/S':
            coneHeight_1 = input('what is cone height 1(floor1 texture)?')
            coneHeight_2 = input('what is cone height 2(floor2 texture)?')
            break
        elif MazeTexture == 'G':
            gratings_floor1 = input('what is orientation for floor1 ?')
            gratings_floor2 = input('what is orientation for floor2 ?')
            coneHeight_1 = '1.5'
            coneHeight_2 = '1.5'
            texture_foor_g_3 = 'NA'
            texture_foor_g_4 = 'NA'
            break

            
              
        else:
            coneHeight_1 = '1.5'
            coneHeight_2 = '1.5'
      
            
            break
        

    global mouseID
    while True:
        mouseID = input('enter mouse ID: ')
        if mouseID not in animaldict.keys():
            print('not a real ID')
        else:
            break
     
    
    while True: 
       out4 =  ser.readline().decode('ascii')
       out2 = 'E,0\n'
       if out4 == out2: 
           break 

       ser.reset_input_buffer()

    numTrials = int(input('enter number of trials'))
    return numTrials

def lickSpout():

    out1 = 'L,1,1'
    ser.write(bytes(out1, 'utf-8'))
    time.sleep(0.01)
    out2 = 'L,2,1'
    ser.write(bytes(out2, 'UTF-8'))
    time.sleep(0.01)
    out = 'E,0\n'
    while True: 
        data = ser.readline().decode('ascii')
        #print(repr(data))
        if data == out:
            ser.reset_input_buffer()
            break 



def openValve(valveID, duration):
    out = 'V,'+str(valveID)+','+str(duration)+'\n'
    ser.write(bytes(out,'utf-8'))
    time.sleep(0.01)
    data = ser.readline().decode('ascii')
    return data


def readStatus():
    out = 'S'
    ser.write(bytes(out, 'utf-8'))
    time.sleep(0.01)
    data = ser.readline().decode('ascii')
    # print(repr(data))
    return data

def door_stat(doorID, open_close):
    out = 'D,'+str(doorID)+ ',' +str(open_close)+ '\n'
    ser.write(bytes(out, 'utf-8'))
    time.sleep(0.01)
    data = ser.readline().decode('ascii')
    return data

def openDoor():
    door_stat(1,1)

    door_stat(2,1 )



      


def runTrial (savefile, numTrials, rewardBeforeLick=False,  valveOpenTime=50, lickUntilCorrect=False, biasCorrection=False):
    trials = numTrials
    on_trial = 0 
    correct_trials = 0
    right_correct_trials = 0
    left_correct_trials = 0
    previousDirections = []
    dataLoaded = False
    if biasCorrection: 
        try:
            with open("D:\TMAZE_DATA\data_BHH4_20241121_113812.json",'r') as file:
                data = json.load(file)
                dataLoaded = True
            if mouseID in data:
                list_of_licks = []
                for key, trial in enumerate(data[mouseID]):
                    for directions in trial:
                        licks = data[mouseID][trial]['lick']
                        list_of_licks.append(licks)

                    last_10_lick = list_of_licks[-10:]
                    print(last_10_lick)
                    num_of_right = 0
                for right in last_10_lick:
                    if right == 'right(V2)':
                        num_of_right += 1
                if num_of_right / 10 > 0.8:
                    rightProb = 1
                elif num_of_right / 10 < 0.2:
                    rightProb = 0
                else:
                    rightProb = 0.5
            else:
                print('MOUSEID not in JSON data, wrong file?')
        except FileNotFoundError:
            print(f"MouseID {mouseID} not found in the JSON data. Setting rightProb to 0.5.")
            rightProb = 0.5        
    else:
        rightProb=0.5        
    
    
   


    for trial in range(trials):
        trial_time = time.localtime()
        on_trial = int(on_trial) + 1 
        start_time = time.time()
        incorrectFlag=False
        try:  
            with open(savefile,'r') as file: 
                data = json.load(file)
        except:
            data = {}
        try: 
            last_key = list(data[mouseID].keys())[-1]
            trial_number = data[mouseID][last_key]['trial_number']
        except: 
            trial_number = 0
        current_trial = 1 + int(trial_number)
        trial_key = 'trial' + str(current_trial)
        
        print(previousDirections)
        print('The number of right decisions:',np.sum(np.array(previousDirections) == 'right(V2)'))
        print('The number of left decisions:',np.sum(np.array(previousDirections) == 'left(V1)'))
        if biasCorrection:
            if len(previousDirections) > 10:
                if np.sum(np.array(previousDirections[-10:]) == 'right(V2)')/10 > 0.8:
                    rightProb = 0.0
                elif np.sum(np.array(previousDirections[-10:]) == 'right(V2)')/10 < 0.2:
                    rightProb = 1.0
                else:
                    rightProb = 0.5
            elif dataLoaded:
                last10 = np.append(last_10_lick,previousDirections)
                last10 = last10[-10:]
                if np.sum(last10 == 'right(V2)')/10 > 0.8:
                    rightProb = 0.0
                elif np.sum(last10 == 'right(V2)')/10 < 0.2:
                    rightProb = 1.0
                else:
                    rightProb = 0.5
            else:
                rightProb = 0.5
                
        print('rightProb', rightProb)
        
        rightFloors = []
        leftFloors = []
        for key in animaldict[mouseID].keys():
            if animaldict[mouseID][key] == 'right(V2)':
                rightFloors.append(int(key[-1]))
            else:
                leftFloors.append(int(key[-1]))
        print('right floors',rightFloors)
        print('left floors',leftFloors)
        
        if np.random.binomial(1,rightProb): ### if right
             floorInd = np.random.randint(0,len(rightFloors)) ## create an index for rightFloors
             floor = rightFloors[floorInd]
             print('CorrectValve: right')
        else: ## if left
             floorInd = np.random.randint(0,len(leftFloors)) ## create an index for leftFloors
             floor = leftFloors[floorInd]
             print('CorrectValve: left')
        

        floorLevel(floor)
        while True: 
            serial_output4 = ser.readline().decode('ascii')
            out6 = 'E,0\n'
            if serial_output4 == out6: 
               break 



        openDoor()
        out = 'A2\n'
        while True: 
            ser1 = ser.readline().decode('ascii') 
            if ser1 == out: 
                door_stat(1,0)
                door_stat(2,0)
                start_time = time.time()
                break 
        print("A2 triggered")

        ser.reset_input_buffer()
        serOutput = readStatus()
        # print(serOutput)
        floor1 = 'F,1' in serOutput
        floor2 = 'F,2' in serOutput
        floor3 = 'F,3' in serOutput
        floor4 = 'F,4' in serOutput
        if floor1: 
            current_floor = 'F,1'
        elif floor2:
            current_floor = 'F,2'
        elif floor3:
            current_floor = 'F,3'
        elif floor4:
            current_floor = 'F,4'
        print(F'the current floor is {current_floor}')

        
        if rewardBeforeLick:
            if animaldict[mouseID][current_floor] == 'right(V2)':
                print('dispensing reward on right valve (V2)')
                openValve(2,valveOpenTime)
            elif animaldict[mouseID][current_floor] == 'left(V1)':
                print('dispensing reward on left valve (V1)')
                openValve(1,valveOpenTime)

        right_lick = False  
        left_lick = False
        out2 = 'L2\n'
        out1 = 'L1\n'
        time.sleep(0.01)

        firstLickOccurred = False
        lickDirection = False
        #logic for openning correct valve 
        while True:
            break_loop = False 
            serial_output2 = ser.readline().decode('ascii')
            #print(serial_output2)
            if serial_output2 == out2:
                left_lick = True
                right_lick = False
                lickDirection = 'left(V1)'

            elif serial_output2 == out1:
                right_lick = True
                left_lick = False
                lickDirection = 'right(V2)'

            if (lickDirection != False) and (firstLickOccurred == False):
                firstLickDirection = lickDirection[:]
                previousDirections.append(lickDirection)
                #print('here3')
                firstLickOccurred = True
            print(left_lick,right_lick,'waiting for lick ----------')
            #print('left lick:',left_lick,'right lick:',right_lick)
            if serial_output2 == out1 or serial_output2 == out2:
                if animaldict[mouseID][current_floor] == lickDirection:
                    if right_lick:
                        if not rewardBeforeLick:
                            newtrials = 20
                            for trial in range(newtrials): 
                                openValve(2,valveOpenTime)
                        if not incorrectFlag:
                            decision = 'correct'
                            right_correct_trials += 1
                            correct_trials += 1
                            print('right valve open; {} trials correct'.format(correct_trials))
                            print('{} right correct decisions'.format(right_correct_trials))
                        end_time = time.time()
                        break_loop = True
                        door_stat(3,1)
                        time.sleep(0.1)
                        door_stat(4,1)
                        #decision = 'correct'
                    elif left_lick:
                        if not rewardBeforeLick:
                            newtrials = 20
                            for trial in range(newtrials): 
                                openValve(1,valveOpenTime)
                        if not incorrectFlag:
                            decision ='correct'
                            left_correct_trials += 1
                            correct_trials += 1
                            print('left valve open; {} trials correct'.format(correct_trials))
                            print('{} left correct decisions'.format(left_correct_trials))
                    
                        end_time = time.time()
                        break_loop = True 
                        door_stat(3,1)
                        time.sleep(0.1)
                        door_stat(4,1)
                        end_time = time.time()
                if animaldict[mouseID][current_floor] != lickDirection:
                    decision = 'incorrect'
                    print('{}, {} correct trials'.format(decision, correct_trials))      
                    incorrectFlag = True
                    if not lickUntilCorrect:
                        door_stat(3,1)
                        time.sleep(0.1)
                        door_stat(4,1)
                        end_time = time.time()
                        break
            if break_loop: 
                incorrectFlag=False
                break 




        time_for_trial = int(end_time) - int(start_time)

        if mouseID not in data: 
            data[mouseID] = {}
            data[mouseID][trial_key] = {'MazeTexture':MazeTexture,'rewardBefLick': rewardBeforeLick,'lickUntilCorrect': lickUntilCorrect,'decision': decision, 'floorID': current_floor,
                                        'time_for_trial': time_for_trial,'valve':floor, 'lick': firstLickDirection,
                                        'trial_number': current_trial, 'trial_time': trial_time,
                                        'right_probability': rightProb,'rewardAmount(ms)': valveOpenTime,'BiasCorrection(T/F)':biasCorrection,'coneHeight_1(floor1)': coneHeight_1,'coneHeight_2(floor2)': coneHeight_2}
        elif mouseID in data:
            data[mouseID][trial_key] = {'MazeTexture':MazeTexture,'rewardBefLick': rewardBeforeLick,'lickUntilCorrect': lickUntilCorrect,'decision': decision, 'floorID': current_floor,
                                        'time_for_trial': time_for_trial,'valve':floor, 'lick': firstLickDirection,
                                        'trial_number': current_trial, 'trial_time': trial_time,
                                        'right_probability': rightProb,'rewardAmount(ms)': valveOpenTime,'BiasCorrection(T/F)':biasCorrection,'coneHeight_1(floor1)': coneHeight_1,'coneHeight_2(floor2)': coneHeight_2}
        sorted_items = sorted(data[mouseID].items(), key=lambda x: x[1]["trial_number"])
        data[mouseID] = {k: v for k, v in sorted_items}

        with open(savefile, 'w') as file: 
            json.dump(data, file, indent = 4)





        if on_trial == trials: 
            return
        else: 
            pass







        print('Trail number:', on_trial)

        out = 'A1\n'
        while True: 
            ser1 = ser.readline().decode('ascii') 
            if ser1 == out: 
                door_stat(3,0)
                door_stat(4,0)
                start_time = time.time()
                break


    
    out = 'A1\n'
    while True: 
        ser1 = ser.readline().decode('ascii') 
        if ser1 == out: 
            door_stat(3,0)
            door_stat(4,0)
            start_time = time.time()
            break 


numTrials = initialize()
currentTime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
data_file_name = 'D:/TMAZE_DATA/data_{0}_{1}.json'.format(mouseID,currentTime)
lickSpout()
lickUntilCorrect=input('LickUntillCorrect? T/F [case sensitive]: ')
lickUntilCorrect_bool=lickUntilCorrect=='T'
rewardBefLick = input('Reward before lick? T/F [case sensitive]: ')
rewardBefLick_bool = rewardBefLick == 'T'
valveOpenTime = int(input('Valve open time (ms): '))
biasCorrection =input('do you want to correct for bias? T/F [case sensitive]')
biasCorrection_bool = biasCorrection =='T'
runTrial(data_file_name, numTrials, rewardBeforeLick=rewardBefLick_bool, valveOpenTime=valveOpenTime,lickUntilCorrect=lickUntilCorrect_bool,biasCorrection=biasCorrection_bool)
out = 'A1\n'
while True: 
    ser1 = ser.readline().decode('ascii') 
    if ser1 == out: 
        door_stat(3,0)
        door_stat(4,0)
        start_time = time.time()
        break 
print(mouseID, 'Session {} Finished'.format(datetime.datetime.now().isoformat()))
