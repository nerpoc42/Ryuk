import os
from random import randint

import sys
import discord
from discord.ext import tasks
from food import get_food

from settings import settings

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print("Bot is ready to serve:")
	print(f"{client.user.name}#{client.user.discriminator}")
	print(f"Bot ID: {client.user.id}")
	print("----------------------------------")
	
	if settings['food_channel_id']:
		print("Starting delivery service")
		food_delivery.start()
	else:
		print("No food channel given, skipping work", file=sys.stderr)


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	content = message.content.lower()

	if 'labas' in content:
		# food_link = get_food()
		# try:
		# 	await message.channel.send(content=food_link)
		# 	await message.channel.send(content="Valgyk tortilija")
		# except:		
		#  	await message.channel.send('Kas mane per idiotas sukodavo')
		await message.channel.send(content='Labas')
	

@tasks.loop(hours=5)
async def food_delivery():
	print("Preparing food")
	food_link = get_food()
	if not food_link:
		print("Failed to find food", file=sys.stderr)
		return
	else:
		print(f"Got food: {food_link}")
	
	channel = client.get_channel(settings['food_channel_id'])
	if not channel:
		print("Failed to find customer channel", file=sys.stderr)
		return
	
	found = None
	async for message in channel.history(limit=200):
		if message.author == client.user:
			found = message
			break
	if found: # Has previous message
		try:
			print(f"Editing food menu: {found.id}")
			await message.edit(content=food_link)
		except discord.Forbidden as e:
			print(e, file=sys.stderr)
	else: # Has to send a new one
		try:
			message = await channel.send(content=food_link)
			print(f"Sending new food menu: {message.id}")
		except discord.Forbidden as e:
			print(e, file=sys.stderr)
	print("----------------------------------")

client.run(settings['bot_token'])

