import random

def roll(num: int = 20):
    ''' Rolls one num-sided dice.
        Inputs:     num - size of the dice to be rolled
        Outputs:    string indicating error, or result of roll '''
    
    try:
        num = int(num)
    except ValueError:
        return ["Dice needs to be a positive integer!", 0]
    if num < 1:
        return ["Dice needs to be a positive integer!", 0]
    
    res = random.randint(1, num)
    output = "**Result:** 1d" + str(num)
    if res == num:
        output += " (**" + str(res) + "**)"
    else:
        output += " (" + str(res) + ")"
    
    return [output, res]

def multiroll(q: int = 1, d: int = 20):
    ''' Rolls q d-sided dice, then adds mod.
        Inputs:     q - quantity of dice
                    d - size of the dice to be rolled
        Output:     string indicating error, or result of roll '''

    error_str = "The following must be positive integers: "
    has_error = False
    try:
        q = int(q)
    except ValueError:
        has_error = True
        error_str += "`[quantity]` "
    try:
        d = int(d)
    except ValueError:
        has_error = True
        error_str += "`[dice]` "

    if has_error:
        return [error_str, 0]
    else:
        total = 0    
        output = str(q) + "d" + str(d) + " ("

        for i in range(q):
            res = roll(d)[1]
            total += res

            if res == d:
                output += "**" + str(res) + "**"
            else:
                output += str(res)
            
            if i < q-1:
                output += ", "
            else:
                output += ")"
        
        return [output, total]

def fudgeMod(mod, fudge):
    output = ""

    try:
        mod = int(mod)
        fudge = int(mod)
    except ValueError:
        return ["Oops! Did you cast confusion? We couldn't parse your input!", True]
    
    print(mod)
    print(fudge)
    
    if fudge >= 20 + mod:
        fudge = 20 + mod
        output += "(**20**)"
    elif fudge < 1 + mod:
        fudge = 1 + mod
        output += "(1)"
    else:
        roll = fudge - mod
        output += "(" + roll + ") + " + str(mod)

    output += "+" + str(mod)

    return [output, False]

def fudge(fudge: int = 20):
    output = ""

    print(fudge)

    try:
        fudge = int(fudge)
    except ValueError:
        return ["Oops! Did you cast confusion? We couldn't parse your input!", True]
    
    if fudge >= 20:
        output += "(**20**)"
    elif fudge < 1:
        output += "(1)"
    else:
        output += "(" + str(fudge) + ")"
    
    return [output, False]