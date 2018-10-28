# PBot
Second rewrite of >PBot. Still not as good as I'd like but it's definitely better than the original and it will make supporting it in the long term easier because of the modular design and the ORM...
If you want to use >PBot you can use this [invite link](https://discordapp.com/api/oauth2/authorize?client_id=381066546535202816&permissions=8&scope=bot) instead of hosting your own instance...

## Features:
- Default prefix: ">>"
- Now supports multiple servers
- Web Dashboard
- PostgreSQL intergration with a custom ORM
- Message change logging
- Name change logging
- Warning system


## Command list:
- Settings:
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
  - setmessage *see below*
    - welcome
    Sets the welcome message (Use **{member_name}** and **{server_name}** accordingly).
    - welcome_pm
    Sets the message that is sent to a member when they join the server
    Use **{member_name}** and **{server_name}** accordingly. It's good to include that they need to click on :+1: to get verified.
    - goodbye
    Sets the goodbye message (Use **{member_name}** accordingly).

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
  - vote
  Creates a poll users can vote on. Instructions in command.
    - vote kick *tag* Vote-kicks the user. Duration is 5 minutes and can't be changed.
    - vote kill Cancels the vote running in that channel. Only the vote creator and people with the Manage Messages permission use this.
  - crypto *coin* *currency*
  Gets the price of a coin in the currency specified (USD by default). Use each coin's 3/4 letter code not the name (ex. BTC instead of Bitcoin).
  - hastebin
  Creates a paste on hastebin.com
  - mcafee
  Updates you on John McAfee's ~~$500.000~~ $1.000.000 by 2020 BTC bet.
  - shibe
  Gets a random picture of a shibe.
  - cat
  Gets a random picture of a cat.
  - playing Returns the current playing status
    - submit Submits a new playing status. Playing statuses get chosen randomly every 30 minutes
  
- NSFW Commands:
  - rule34 *tag*
  Gets an image from rule34.xxx based on the tag given.
  - gelbooru *tag*
  Gets an image from gelbooru.com based on the tag given.
  - rtube *tag*
  Gets a video/thumbnail from redtube.com based on the tag given.

- Anime Commands:
  - anime search *query* Searches for the anime with the query specified
  - anime top *upcoming*,*tv*,*movie*,*airing*,*ova*,*special* Shows the top anime of given category
  - anime character *query* Searches for the anime character with the query specified
  
- [Konishi](https://github.com/konishi-project) Client (use >>konishi *subcommand*):
  - login Logs you in with your username and password and saves the session so you can use the client
  - post Make a post. It will guide you step by step.
  - feed Get a feed of recent posts.
    
More coming soon...
