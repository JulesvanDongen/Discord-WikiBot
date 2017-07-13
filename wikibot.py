import constants
import discord
import logging
import asyncio
import command
import sys

assert sys.version_info >= (3,5)

logging.basicConfig(level=logging.INFO)

client = discord.Client()

dict = command.commandDict

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
	if message.content.startswith(command.commandchar):
		splitmessage = message.content[len(command.commandchar):].split(' ', 1)
		try:
			cmd = dict[splitmessage[0]]
			
			if cmd is not None:
				args = ''
				if (len(splitmessage) > 1):
					args = splitmessage[1]
					
				await cmd.execute(client, message, args)
		except KeyError:
			print('KeyError caught during on_message')
			
client.run(constants.token)