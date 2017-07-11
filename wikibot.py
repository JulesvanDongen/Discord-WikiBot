import logging

logging.basicConfig(level=logging.INFO)

import constants
import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
	if message.content.startswith('!wiki'):
		print('message sent') # do things
	elif message.content.startswith('!help'):
		



client.run(constants.token)