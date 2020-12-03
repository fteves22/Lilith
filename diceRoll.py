import random

def roll(num: int = 20):
    ''' Rolls one num-sided dice.
        Inputs:     num - size of the dice to be rolled
        Outputs:    string indicating error, or result of roll '''
    
    try:
        num = int(num)
    except ValueError:
        return "Dice needs to be a positive integer!"
    if num < 1:
        return "Dice needs to be a positive integer!"
    
    res = random.randint(1, num)
    if res == num:
        return "**Result:** 1d" + str(num) + " **" + str(res) + "**"
    else:
        return "**Result:** 1d" + str(num) + " (" + str(res) + ")"

