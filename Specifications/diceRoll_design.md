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
