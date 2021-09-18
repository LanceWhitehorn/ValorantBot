import os
import random
import discord
import youtube_dl
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)


#########################
#     Role Reaction     #
#########################

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    print(f'{member.name} has joined the server!')
    await member.send(f'Hi {member.name}, <#887372328143552572> to our friendly Valorant server!')
    
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 888372589116928060:
        guild = discord.utils.find(lambda g: g.id==payload.guild_id, client.guilds)
        role_name = payload.emoji.name.capitalize()
        role = discord.utils.get(guild.roles, name=role_name)    
        if role is not None:
            member = discord.utils.find(lambda m: m.id==payload.user_id, guild.members)
            if member is not None:
                if member.id != 835802124117475348:
                    await member.add_roles(role)
                    print(f'{member.name}  added to', role_name)
                else:
                    print('ValorantBot reaction for', role_name)
            else:
                print(f'{member.name}  not found')
        else:
            print('Role not found')

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 888372589116928060:
        guild = discord.utils.find(lambda g: g.id==payload.guild_id, client.guilds)
        role_name = payload.emoji.name.capitalize()
        role = discord.utils.get(guild.roles, name=role_name)    
        if role is not None:
            member = discord.utils.find(lambda m: m.id==payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f'{member.name} removed from', role_name)
            else:
                print(f'{member.name} not found')
        else:
            print('Role not found')

@commands.has_role('Admin')            
@client.command(hidden=True)
async def roles(ctx):
    message = await ctx.fetch_message('888372589116928060')
    emojis = ['astra', 'breach', 'brimstone', 'cypher', 'jett', 'kayo', 'killjoy', 'omen', 'phoenix', 'raze', 'reyna', 'sage', 'skye', 'sova', 'viper', 'yoru']
    guild = discord.utils.find(lambda g: g.id==ctx.guild.id, client.guilds)
    for agent in emojis:
        emoji = discord.utils.get(guild.emojis, name=agent)
        await message.add_reaction(emoji)


##########################
#     Agent Roulette     #
##########################

@client.command(aliases=['r'], help='(Takes an integer n) Randomly selects n agents')
async def roulette(ctx, number:int):
    if number <= 5:
        agents = ['astra', 'breach', 'brimstone', 'cypher', 'jett', 'kayo', 'killjoy', 'omen', 'phoenix', 'raze', 'reyna', 'sage', 'skye', 'sova', 'viper', 'yoru']
        chosen = []
        while len(chosen) < number:
            idx = random.randint(0, 15)
            agent = agents[idx].capitalize()
            if agent not in chosen:
                chosen.append(agent)
        desc = ', '.join(chosen)
        embed = discord.Embed(title='Agents', description=desc, color=0xF4F4F4)
        await ctx.send(embed=embed)
#       await ctx.send('Agent(s): ' + desc)
    else:
        await ctx.send('You can\'t select more than 5 agents!')


#################
#     Music     #
#################  
      
@client.command(help='Play song (only accepts YouTube URLs atm)')
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='comms')
    try:
        await voiceChannel.connect()
    except:
        pass
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command(help='Disconnect ValorantBot from vc')
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command(help='Pause the current song')
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@client.command(help='Resume the current song')
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@client.command(help='Stop the song')
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
client.run(TOKEN)


#####################
#     Workspace     #
#####################

#@client.event
#async def on_command_error(ctx  , error):
#    if isinstance(error, commands.CommandNotFound):
#        print(error)

#@client.command(aliases=['q'])
#async def quit(ctx):
#    print(f'{client.user.name} has disconnected')
#    await ctx.send(f'{client.user.name} has disconnected')
#    await client.close()