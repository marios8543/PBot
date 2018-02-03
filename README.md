# PBot
The rewrite of the original Implying_Pbot

## Features:
- Default prefix: ">>"
- Now supports multiple servers
- Web Dashboard
- MySQL intergration
- Message change logging
- Name change logging
- Warning system

## Command list:
- setwelcome
Sets the welcome message channel
- setgoodbye
Sets the goodbye message channel
- setevent
Sets the event channel (namechanges etc)
- setlogging
Sets the message logging channel (Deletes, Edits)
- logging
Toggles logging on/off
- check *tag*
Gets some basic info of the member tagged
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
- bsf
Gets the current venezuelan bolivar price
- emoji *emoji*
Gives an enlarged image/download link for an emoji

More coming soon...
