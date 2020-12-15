# Initiative Tracker

## Purpose
The purpose of this module is to cover the initiative tracking requirements for common TTRPG games. The bot will be able to use this module to add characters to the initiative tracker using a user-provided initiative value, display the initiative order to the text channel, keep track of rounds and the current turn, and end combat by clearing the initiative tracker. This module will be a class; the bot interface will store instances of this class, allowing persistent storage of the tracker information.  

## Class Attributes
**trackerInfo**  
A three-dimensional array arranged so `trackerInfo[i][0]` holds the usernames, `trackerInfo[i][1]` holds the character names, and `trackerInfo[i][2]` holds the initiative values. (Given `i` is some non-negative integer.)  

**currentPlayer**  
An integer representing the index in `trackerInfo` that holds the current player's information. This is updated each time `next()` is called.  

**rounds**  
An integer representing the number of combat rounds. This is updated when `currentPlayer` loops around `trackerInfo`, so that `currentPlayer` is once again 0.

## Functions
```python
printTracker()
```  

This function displays the current initiative.

#### Logic
```python
if trackerInfo == []:
  throw error
else:
  current = 0
  toPrint = ""
  for data in trackerInfo:
    if current == currentPlayer:
      # Bold
      toPrint = toPrint + "**" + str(data[2]) + ": " + data[1] + "**"
    else:
      # Not bold
      toPrint = toPrint + str(data[2]) + ": " + data[1]
    
    current = current + 1
  
  if rounds == 0:
    print(toPrint)
  else:
    print(toPrint)
    print(name + ", it's your turn!")
```

---

```python
join(username, name, initiative)
```

This function is in charge of adding a character into the initiative order. The Dungeon Master can also add creatures in this way. It cannot be called once combat has begun via `begin()`.  

#### Parameters
- **username** (*Member*) – The *Member* that added the character to initiative.
- **name** (*str*) – A string that represents the name of the character being added to initiative.
- **initiative** (*int*) – An integer that represents the initiative roll for the character being added to initiative.  

#### Logic
```python
# Check that name doesn't exist yet.
for data in trackerInfo:
  if name == data[1]:
    throw error

try:
  initiative = int(initiative)
except:
  throw error

# Check if currentPlayer gets bumped down.
if initiative > trackerInfo[currentPlayer][2]:
  currentPlayer = currentPlayer + 1

trackerInfo.append([username, name, initiative])
printTracker()
```

#### Raises
- **"That character already exists!"** – A character by the same name already exists in initiative.
- **"Combat has already begun!** – The `begin()` function has already been called.
- **"Initiative must be an integer!** – The given initiative parameter is not of type *int*.

---

```python
kill(name)
```

This function deletes the combatant in initiative with `name` if they exist in `trackerInfo`.  

#### Parameters
- **name** (*str*) – A string that represents the name of the character being deleted from initiative.  

#### Logic
```python
count = 0
for data in trackerInfo:
  # Find the character to remove.
  if name == data[1]:
    # Check if currentPlayer gets bumped up.
    if count < currentPlayer:
      currentPlayer = currentPlayer - 1
    trackerInfo.pop(count)      
    printTracker()
  else:
    count = count + 1
# Combatant with that name wasn't found.
throw error
```

#### Raises
- **"`name` does not exist."** – A combatant with the user-given name does not exist in initiative.

---

```python
begin()
```

This function marks the start of combat. Once it has been called, characters can no longer join combat.  

#### Logic
```python
# Check that initiative hasn't already begun.
if rounds != 0:
  throw error
# Check that there are at least 2 combatants.
elif len(trackerInfo) < 2:
  throw error
else:
  rounds = 1
  printTracker()
```

#### Raises
- **"Combat has already begun! Use `end` to clear the initiative tracker."** – There is still combatants in initiative, and `rounds` isn't 0.
- **"At least two combatants required!"** – There are less than two combatants added to initative.

---

```python
end()
```  

This function marks the end of combat. Once it has been called, all combatants are cleared from initiative and relevant attributes are reset.

#### Logic
```python
trackerInfo.clear()
currentPlayer = 0
rounds = 0
```

---

```python
next()
```   

This function moves `currentPlayer` to the next combatant in initiative.

#### Logic
```python
# Check if combat has begun.
if rounds == 0:
  throw error
# Check if currentPlayer is at the end of initiative.
elif currentPlayer + 1 == len(trackerInfo):
  currentPlayer = 0
  inc_round()
else:
  currentPlayer = currentPlayer + 1

printTracker()
```

#### Raises
- **"Combat hasn't begun yet! Use `begin` to begin combat."** – The `begin()` function hasn't been called yet.

---

```python
prev()
```  

This function moves `currentPlayer` to the previous combatant in initiative.  

#### Logic
```python
# Check if combat has begun.
if rounds == 0:
  throw error
# Check if currentPlayer is at the beginning of initiative.
elif currentPlayer - 1 == 0:
  currentPlayer = len(trackerInfo) - 1
  dec_round()
else:
  currentPlayer = currentPlayer - 1

printTracker()
```  

#### Raises
- **"Combat hasn't begun yet! Use `begin` to begin combat."** – The `begin()` function hasn't been called yet.

### Helper Functions
```python
inc_round()
```  

This function increments `rounds` by 1.

#### Logic
```python
rounds = rounds + 1
```

---

```python
dec_round()
```  

This function decrements `rounds` by 1.

#### Logic
```python
if rounds - 1 == 0:
  rounds = 1
else:
  rounds = rounds - 1
```

---

```python
sortTrackerInfo()
```  

This function sorts `trackerInfo` by initiative roll in descending order.

#### Logic
```python
trackerInfo = sorted(trackerInfo, key = lambda x:x[2], reverse = True)
```
