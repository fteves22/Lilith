import random

def roll(num: int = 20):
    ''' Rolls one num-sided dice.
        Inputs:     num - size of the dice to be rolled
        Outputs:    string indicating error, or result of roll '''
    
    try:
        num = int(num)
    except ValueError:
        return ["Dice needs to be a positive integer!", 0, True]
    if num < 1:
        return ["Dice needs to be a positive integer!", 0, True]
    
    res = random.randint(1, num)
    output = "**Result:** 1d" + str(num)
    if res == num:
        output += " (**" + str(res) + "**)"
    else:
        output += " (" + str(res) + ")"
    
    return [output, res, False]

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
        return [error_str, 0, True]
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
        
        return [output, total, False]

def rollAdv(adv, mod = 0):
    try:
        mod = int(mod)
    except ValueError:
        return ["⚠️ To roll with advantage, your input must be of the form: `+/- [mod]`.", 0, True]
    
    r1 = roll()[1]
    r2 = roll()[1]

    # Bold if Nat 20
    if r1 == 20:
        r1_str = "**" + str(r1) + "**"
        r2_str = str(r2)
    elif r2 == 20:
        r1_str = str(r1)
        r2_str = "**" + str(r2) + "**"
    else:
        r1_str = str(r1)
        r2_str = str(r2)
    
    if adv == True:
        if max(r1, r2) == r1:
            output = "**Result:** 1d20 (" + r1_str + ", ~~" + r2_str + "~~) "
            total = r1 + mod
        else:
            output = "**Result:** 1d20 (~~" + r1_str + "~~, " + r2_str + ") "
            total = r2 + mod
    else:
        if min(r1, r2) == r1:
            output = "**Result:** 1d20 (" + r1_str + ", ~~" + r2_str + "~~) "
            total = r1 + mod
        else:
            output = "**Result:** 1d20 (~~" + r1_str + "~~, " + r2_str + ") "
            total = r2 + mod
    
    if mod > 0:
        output += "+ " + str(mod)
    elif mod < 0:
        output += "- " + str(mod)
    else:
        pass

    return [output, total, False]
    

def fudgeMod(mod, fudge):
    ''' Fudges a 1d20 + mod roll.
        Inputs:     mod - modifier
                    fudge - total fudge roll
        Output:     string indicating error, or result of roll '''

    output = ""

    try:
        mod = int(mod)
        fudge = int(fudge)
    except ValueError:
        return ["Oops! Did you cast confusion? We couldn't parse your input!", 0, True]
    
    if fudge >= 20 + mod:
        fudge = 20 + mod
        output += "(**20**)"
    elif fudge < 1 + mod:
        fudge = 1 + mod
        output += "(1)"
    else:
        roll = fudge - mod
        output += "(" + str(roll) + ")"

    if mod > 0:
        output += " + " + str(mod)
    elif mod < 0:
        output += " - " + str(-mod)

    return [output, fudge, False]

def fudge(fudge: int = 20):
    ''' Fudges a 1d20 roll.
        Inputs:     fudge - total fudge roll
        Output:     string indicating error, or result of roll '''
    output = ""

    try:
        fudge = int(fudge)
    except ValueError:
        return ["Oops! Did you cast confusion? We couldn't parse your input!", 0, True]
    
    if fudge >= 20:
        fudge = 20
        output += "(**20**)"
    elif fudge < 1:
        fudge = 1
        output += "(1)"
    else:
        output += "(" + str(fudge) + ")"
    
    return [output, fudge, False]

# HELPER FUNCTIONS
def splitMe(arg):
    ''' HELPER FUNCTION: To split tuples into roll chunks. '''

    arg = "".join(arg)
    splitPlus = " + ".join(arg.split('+'))
    fullSplit = " - ".join(splitPlus.split('-')).split()

    return fullSplit

def complexRoll(arg):
    ''' HELPER FUNCTION: To parse complex rolls. '''

    arg = splitMe(arg)

    output = "**Result:** "
    total = 0
    is_subtract = False
    has_error = False

    # Handle each rolling chunk in the params.
    for i in range(len(arg)):
        # In the form [quantity]d[dice]
        if "d" in arg[i]:
            params = arg[i].split("d")
            q = params[0]
            d = params[1]

            if q == '':
                q = '1'

            res = multiroll(q, d)
            if res[2]:
                has_error = True
            
            if res[1] != 0:
                output += res[0]

                if is_subtract:
                    total -= res[1]
                else:
                    total += res[1]
            else:
                output = "Oops! Did you cast confusion? We couldn't parse your input!\n" + res[0]
                return [output, total, has_error]
        elif arg[i] == "+":
            output += " + "
            is_subtract = False
        elif arg[i] == "-":
            output += " - "
            is_subtract = True
        # It's a modifier.
        else:
            try:
                res = int(arg[i])
            except ValueError:
                output = "Oops! Did you cast confusion? We couldn't parse your input!"
                return [output, total, has_error]
            
            if res < 0:
                output += " - " + str(-res)
            else:
                output += arg[i]
            
            if is_subtract:
                    total -= res
            else:
                total += res
        
    return [output, total, has_error]