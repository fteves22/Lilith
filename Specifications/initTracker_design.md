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
> `join(username, name, initiative)`  

This function is in charge of adding a character into the initiative order. The Dungeon Master can also add creatures in this way. It cannot be called once combat has begun via begin().  

### Parameters
- **username** (*Member*) – The *Member* that added the character to initiative.
- **name** (*str*) – A string that represents the name of the character being added to initiative.
- **initiative** (*int*) – An integer that represents the initiative roll for the character being added to initiative.  

### Raises
- **"That character already exists!"** – A character by the same name already exists in initiative.
- **"Combat has already begun!** – The `begin()` function has already been called.
- **"Initiative must be an integer!** – The given initiative parameter is not of type *int*.