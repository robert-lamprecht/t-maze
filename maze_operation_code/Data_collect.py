import json 
#Correctness Rate
filePath = "D:\\TMAZE_DATA\\data_BCU5_20240422_150150.json"
with open(filePath, 'r') as file:
    data = json.load(file) 

num_correct = 0 
num_incorrect = 0
for value in data.values():
    for key, v in value.items(): 
        x = v['decision']
        if x == 'correct': 
            num_correct += 1 
        elif x == 'incorrect': 
            num_incorrect += 1 

rewardAmount=[]
for rewardAmount in data.values():
    rewardAmount=v['rewardAmount(ms)']

#Bias Checking
num_right = 0 
num_left = 0
for value in data.values():
    for key, v in value.items(): 
        x = v['lick']
        if x == 'right(V2)': 
            num_right += 1 
        elif x == 'left(V1)': 
            num_left += 1 

right_bias = num_right / (num_right + num_left)
left_bias = num_left / (num_right + num_left)

biasR = right_bias > 0.8
biasL = left_bias > 0.8

print('the amount of reward each trial for this session is:', rewardAmount, '(ms)')
print(f'the number of correct trials is {num_correct}')
print(f'the number of incorrect trials is {num_incorrect}')

#print(f'the number of right trials is {num_right}')
#print(f'the number of left trials is {num_left}')
#print(f'bias rate(right) is {right_bias}')
#print(f'bias rate(left) is {left_bias}')
#print(f'The bias is (right: {biasR}, left: {biasL})')

if biasR:
    print('This session is biased, please apply bias correcting function (right)')
elif biasL:
    print('This session is biased, please apply bias correcting function (left)')
else:
    print('No need to apply bias correcting function')
