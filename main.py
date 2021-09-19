import os
import random
import discord
import youtube_dl
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

##################################
#     Discord slash commands     #
##################################

from discord_slash import SlashCommand, SlashContext, ComponentContext
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle


###################
#     Buttons     #
###################

@client.command(aliases=['s'])
async def squad(ctx:SlashContext):
    buttons = [
        create_button(style=ButtonStyle.green, label='Join', custom_id='join'),
        create_button(style=ButtonStyle.blue, label='Leave', custom_id='leave')
    ]
    action_row = create_actionrow(*buttons)
    embed = discord.Embed(title='Squad', description=f'{ctx.author.name}', color=0xF4F4F4)
    message = await ctx.send(embed=embed)
    await ctx.send(content='Options:', components=[action_row])
    temp = [ctx.author.name]
    while True:
        button_ctx: ComponentContext = await manage_components.wait_for_component(client, components=action_row)
        await button_ctx.edit_origin(content='Options:')
        user = button_ctx.author.name
        if button_ctx.custom_id=='join' and user not in temp:
            if len(temp) != 1:
                temp.append(user)
            else:
               await ctx.send('Full squad!') 
        if button_ctx.custom_id=='leave' and user in temp:
            temp.remove(user)
        new_embed = discord.Embed(title='Squad', description=', '.join(temp), color=0xF4F4F4)
        await message.edit(embed=new_embed)


#################
#     Setup     #
#################

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
async def agentSelect(ctx):
    message = await ctx.fetch_message('888372589116928060')
    emojis = ['astra', 'breach', 'brimstone', 'cypher', 'jett', 'kayo', 'killjoy', 'omen', 'phoenix', 'raze', 'reyna', 'sage', 'skye', 'sova', 'viper', 'yoru']
    guild = discord.utils.find(lambda g: g.id==ctx.guild.id, client.guilds)
    for agent in emojis:
        emoji = discord.utils.get(guild.emojis, name=agent)
        await message.add_reaction(emoji)


##########################
#     Agent Roulette     #
##########################

@client.command(aliases=['r'], help='(Takes an integer n, default n=1) Randomly selects n agents')
async def roulette(ctx, number:int=1):
    if number <= 5:
        agents = ['astra', 'breach', 'brimstone', 'cypher', 'jett', 'kayo', 'killjoy', 'omen', 'phoenix', 'raze', 'reyna', 'sage', 'skye', 'sova', 'viper', 'yoru']
        chosen = []
        while len(chosen) < number:
            idx = random.randint(0, 15)
            agent = agents[idx].capitalize()
            if agent not in chosen:
                chosen.append(agent)
        desc = ', '.join(chosen)
        embed = discord.Embed(title='Agent Roulette', description=desc, color=0xF4F4F4)
        await ctx.send(embed=embed)
#       await ctx.send('Agent(s): ' + desc)
    else:
        await ctx.send('You can\'t select more than 5 agents!')


############################
#     Agent Main Users     #
############################

@client.command(help='Lists users that main the specified agent')
async def mains(ctx, agent:str):
    agent = agent.capitalize()
    guild = discord.utils.find(lambda g: g.id==ctx.guild.id, client.guilds)
    role = discord.utils.get(guild.roles, name=agent)
    users = []
    for member in guild.members:
        if role in member.roles:
            users.append(member.name)
    desc = ', '.join(users)
    embed = discord.Embed(title=agent+' Mains', description=desc, color=0xF4F4F4)
    await ctx.send(embed=embed)


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