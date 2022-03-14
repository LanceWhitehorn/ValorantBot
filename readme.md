# Valorant Bot

Having picked up Valorant during the COVID lockdown, I decided to create a custom bot for my Valorant Discord server. I coded the bot in Python which I currently continue to host  on Heroku.

## Features
| Name | Command | Description
| :--- | :------ | :----------
| Agent roles reaction | !agentRoles | Assigns the user to the agent-specific roles they choose.
| Mains | !mains [agent] | Lists all users who main the specified agent.
| Roulette | !roulette [n] | Lists `n` random agents.
| Squad | !squad | Creates a virtual lobby which users can join and leave.
| Music player | Basic music player with play, pause, resume, stop, leave functions.
| Clear | !clear [n] | Clears the last `n` messages.
| Log files | | Logs members that join/leave, reacts for a role, attempts using admin commands.
