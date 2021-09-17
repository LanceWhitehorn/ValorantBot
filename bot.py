import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    print(f'{member.name} has joined the server!')
    await member.send(f'Hi {member.name}, welcome to my Discord server!')
    
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 888331814471602207:
        guild = discord.utils.find(lambda g: g.id==payload.guild_id, client.guilds)
        role_name = payload.emoji.name.capitalize()
        role = discord.utils.get(guild.roles, name=role_name)    
        if role is not None:
            member = discord.utils.find(lambda m: m.id==payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('Member added to', role_name)
            else:
                print('Member not found')
        else:
            print('Role not found')

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 888331814471602207:
        guild = discord.utils.find(lambda g: g.id==payload.guild_id, client.guilds)
        role_name = payload.emoji.name.capitalize()
        role = discord.utils.get(guild.roles, name=role_name)    
        if role is not None:
            member = discord.utils.find(lambda m: m.id==payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print('Member removed from', role_name)
            else:
                print('Member not found')
        else:
            print('Role not found')
            
@client.event
async def on_command_error(ctx  , error):
    if isinstance(error, commands.CommandNotFound):
        print(error)

@client.command()
async def hello(ctx):
    await ctx.send('Hello')

@client.command(aliases=['q'])
async def quit(ctx):
    print(f'{client.user.name} has disconnected')
    await ctx.send(f'{client.user.name} has disconnected')
    await client.close()

client.run(TOKEN)