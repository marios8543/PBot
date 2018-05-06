# PBot
Second rewrite of >PBot. Still not as good as I'd like but it's definitely better than the original and it will make supporting it in the long term easier because of the modular design and the ORM...

## Features:
- Default prefix: ">>"
- Now supports multiple servers
- Web Dashboard
- MySQL intergration with a custom ORM
- Message change logging
- Name change logging
- Warning system


## Command list:
- Channel Settings:
  - setwelcome  
  Sets the welcome message channel
  - setgoodbye  
  Sets the goodbye message channel
  - setevent  
  Sets the event channel (namechanges etc)
  - setlogging  
  Sets the message logging channel (Deletes, Edits)
  - logging [name or msg] 
  Toggles name-change/message-change logging on/off

- Admin Commands:
  - check *tag*  
  Gets some basic info of the member tagged and presents admin options (warn,softban,clear)
  - warn *tag* *reason*  
  Warns the member. Will be banned once the warn limit is reached
  - verify *tag*  
  Verifies an unverified member manually
  - clearwarnings *tag*  
  Sets a member's warning count to 0 (Independent warnings are still logged)
  - massdelete *id* *id*  
  Deletes all the messages between 2 message IDs given
  - dashboard  
  Access the dashboard for your server and change bot settings
  - softban *tag *mins*  
  Makes a member unverified for a set number of minutes (Max 60)
  - nickname *tag* *nickname*  
  Sets the nickname for a member

- Fun Commands:
  - bsf  
  Gets the current venezuelan bolivar price
  - emoji *emoji*  
  Gives an enlarged image/download link for an emoji

More coming soon...
