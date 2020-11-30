# Lilith
Lilith is a Discord bot designed to make Dungeons &amp; Dragons easier to play and manage. It features dice rolling, initiative tracking, and compendium search functionality.

## Commands
`!help`: Shows a list of common commands, and a link to a list of all commands.  
  
`!roll [x] d [y] [+/- m]`: Rolls an `x` number of `d`-sided dice, then adds or subtracts `m` to the result.  
  
`!join [name] [i]`: Adds a combatant as `name` to the combat order with `i` for their initiative roll.  
`!delete [name]`: Deletes the combatant `name` if they exist in the combat order.  
`!begin`: Begins combat, and tags the first player in combat.  
`!next`: Moves onto the next player in combat.  
`!previous`: Moves back to the previous player in combat.  
`!end`: Ends combat, and clears the tracker of all player information.  
  
`!search [c] [name]`: Returns the search results of `name` under the category `c`.
  
