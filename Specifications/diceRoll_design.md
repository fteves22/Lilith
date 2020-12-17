# Dice Rolling

## Purpose
The purpose of this module is to cover the dice rolling requirements for common TTRPG games. The bot will be able to use this module to roll any number of any sided dice and add modifiers to them, roll with advantage or disadvantage, and fudge rolls.  

## Functions
```python
roll(num: int = 20)
```  

This funciton rolls one `num`-sided die.   

#### Parameters
- **num** (*int*, Optional) – An integer representing the size of the dice to be rolled.

#### Returns
```python
[output, res, error]
```  
- **output** (*str*) – A string representing the roll output or the error message.
- **res** (*int*) – An integer representing the roll result.
- **error** (*bool*) – A boolean indicating whether an error was raised.  

#### Logic
```python
try:
    num = int(num)
except:
    throw error
if num < 1:
    throw error

result = randint(1, num)
output = "**Result:** 1d" + num
if res == num:
    # Bold
    output = output + " (**" + res + "**)"
else:
    # Not bold
    output = output + " (" + res + ")"

return [output, res, False]
```  

#### Raises
- **"Dice needs to be a positive integer!"** – `num` cannot be casted as an integer, or is less than 1.  

---

```python
multiroll(q: int = 1, d: int = 20)
```  

This function rolls `q` `d`-sided dice, then adds `mod`.  

#### Parameters
- **q** (*int*, Optional) – An integer representing dice quantity.
- **d** (*int*, Optional) – An integer representing the size of the dice to be rolled.  

#### Returns
```python
[output, res, error]
```  
- **output** (*str*) – A string representing the roll output or the error message.
- **res** (*int*) – An integer representing the roll result.
- **error** (*bool*) – A boolean indicating whether an error was raised.  

#### Logic
```python
error_str = "The following must be positive integers: "
has_error = False

# Make sure q and d are integers.
try:
    q = int(q)
except:
    error_str = error_str + "[quantity]"
try:
    d = int(d)
except:
    error_str = error_str + "[dice]"

if has_error:
    # This error will return the error_str.
    throw error
else:
    total = 0
    output = q + "d" + d + " ("

    for i in range(q):
        res = roll(d)[1]
        total += res

            if res == d:
                output += "**" + res + "**"
            else:
                output += res
            
            if i < q-1:
                output += ", "
            else:
                output += ")"
        
        return [output, total, False]
```  

#### Raises
- **"The following must be positive integers: [quantity]"** – `quantity` cannot be cast as an integer.
- **"The following must be positive integers: [dice]"** – `dice` cannot be cast as an integer.
- **"The following must be positive integers: [quantity] [dice]"** – `quantity` and `dice` cannot be cast as integers.  

---

```python
rollAdv(adv, mod = 0)
```  

This function rolls two 20-sided dice, and keeps the higher result if `adv` is True and the lower result if `adv` is False.  

#### Parameters
- **adv** (*bool*) – A boolean indicating whether you're rolling at advantage.
- **mod** (*int*) – An integer representing the modifier to be added to the roll result.  

#### Returns


#### Logic
```python
# advantage_err: An error mesage for advantage.
# disadvantage_err: An error message for disadvantage.
# gen_err: A general error message.

try:
    mod = int(mod)
except:
    if adv:
        return [advantage_err, 0, True]
    elif not adv:
        return [disadvantage_err, 0, True]
    else:
        return [gen_err, 0, True]

r1 = roll()[1]
r2 = roll()[1]

# Bold if 20
r1_str = str(r1)
r2_str = str(r2)

if adv:
    if max(r1, r2) == r1:
        output = "**Result:** 1d20 (" + r1_str + ", ~~" + r2_str + "~~)"
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
    output += "+ " + mod
elif mod < 0:
    output += "- " + -mod
else:
    pass

return [output, total, False]
```

#### Raises
- **"⚠️ To roll with advantage, your input must be of the form: `adv +/- [mod]`."** – `adv` is True and `mod` cannot be cast as an integer.
- **"⚠️ To roll with disadvantage, your input must be of the form: `dis +/- [mod]`."** – `adv` is False and `mod` cannot be cast as an integer.
- **"Oops! Something went wrong."** – `adv` is not a bool.
