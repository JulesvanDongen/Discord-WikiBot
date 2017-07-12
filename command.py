import abc
import discord
import asyncio
import wikipedia

class Command:
	__metaclass__ = abc.ABCMeta
	
	@abc.abstractmethod
	def help(self):
		"""This method implements the returning help documentation for help command"""
		return
	
	@abc.abstractmethod
	async def execute(self, client, message, arg):
		"""Calling this command executes the command, the command creates implements its own use"""
		return
		
	@abc.abstractmethod
	def names(self):
		"""This method should return an array of names which are used to execute the command"""
		return

class HelpCommand(Command):
	def help(self):
		return 'Display this help message'
		
	async def execute(self, client, message, arg):
		title = 'The commands for WikiBot:\n'
		
		content = ''
		
		for command in commands: 
			for name in command.names():
				content += '!'
				content += name
				content += ' '
			content += '\t'
			content += command.help() 
			content += '\n'
		
		emb = discord.Embed(title=title, description=content)
			
		await client.send_message(message.channel, embed=emb)
		
	def names(self):
		return ['help']
		
class WikiCommand(Command):
	def help(self):
		return 'Searches Wikipedia for an article'
		
	async def execute(self, client, message, arg):
		tmp = await client.send_message(message.channel, 'Searching Wikipedia...')
		try:
			page = wikipedia.page(arg)
			
			summ = page.summary[:page.summary[:2000].rfind('\n')]
			emb = discord.Embed(title=page.title, description=summ, url=page.url)
			
			if len(page.images) > 0:
				emb.thumbnail.url = page.images[0]
				emb.thumbnail.width = 25
				emb.thumbnail.height = 25                                                  
			
			await client.send_message(message.channel, embed=emb)
			
			await client.delete_message(tmp)
		except wikipedia.exceptions.DisambiguationError as de:
			title = arg
			title += ' may refer to:\n'
			
			content = ''
		
			for option in de.options:
				if not(option.startswith('All pages with a title containing') or option.startswith('All pages beginning with')):
					content += option
					content += '\n'
					
			emb = discord.Embed(title=de.title, description=content)
			await client.delete_message(tmp)
			await client.send_message(message.channel, embed=emb)
		except wikipedia.exceptions.PageError as pe:
			string = 'WikiBot could not find a page for \''
			string += arg
			string += '\''
			
			await client.edit_message(tmp, string)
	def names(self):
		return ['wiki']
		
		
class CleanCommand(Command):
	def help(self):
		return 'Cleans the chat of the commands. This requires the Manage Messages permission.'
		
	async def execute(self, client, message, arg):
	
		def delete_all(message):
			return message.author == client.user or delete_commands(message)
				
		def delete_commands(message):
			try:
				return (message.content.startswith('!') and commandDict[message.content[1:].split(' ', 1)[0]] is not None)
			except KeyError:
				return False
				
		try:
			if arg.startswith('all'):
				print('everything will be deleted')
				deleted = await client.purge_from(message.channel, check=delete_all)
			else:
				print('only inputs are deleted')
				deleted = await client.purge_from(message.channel, check=delete_commands)
		except discord.Forbidden as forbidden:
			await client.send_message(message.channel, 'Could not delete the data, possibly because of not having enough permissions')
	
	def names(self):
		return ['clean']
		
commands = [HelpCommand(), WikiCommand(), CleanCommand()]
commandDict = {}

for command in commands:
	for name in command.names():
		commandDict[name] = command