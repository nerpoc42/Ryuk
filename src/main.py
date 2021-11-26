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

	global prev_food_link
	prev_food_link = read_food()
	print(f"Last food link: {prev_food_link}")

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

	if 'maist' in content:
		await message.channel.trigger_typing()
		print("----------------------------------")
		print("Preparing food")
		food_link = get_food()
	
		if not food_link:
			print("Failed to find food", file=sys.stderr)
			return
		else:
			print(f"Got food: {food_link}")

		global prev_food_link
		if prev_food_link == food_link:
			print("Forcing new food menu")

		try:
			message = await message.channel.send(content=food_link)
			prev_food_link = food_link
			save_food(food_link)
			print(f"Served new food menu: {message.id}")
		except discord.Forbidden as e:
			print(e, file=sys.stderr)
	

@tasks.loop(hours=1)
async def food_delivery():
	
	channel = client.get_channel(settings['food_channel_id'])
	if not channel:
		print("Failed to find customer channel", file=sys.stderr)
		return
	else:
		await channel.trigger_typing()
		print("----------------------------------")
		print("Preparing food")
		food_link = get_food()
	
		if not food_link:
			print("Failed to find food", file=sys.stderr)
			return
		else:
			print(f"Got food: {food_link}")

		global prev_food_link
		if prev_food_link == food_link:
			print("Previous and current food matches, skipping")
			return
		else:
			try:
				message = await channel.send(content=food_link)
				prev_food_link = food_link
				save_food(food_link)
				print(f"Served new food menu: {message.id}")
			except discord.Forbidden as e:
				print(e, file=sys.stderr)

def save_food(food_link):
	try:
		with open(settings['food_cache_file'], "w") as f:
			f.write(food_link)
	except Exception as e:
		print(e, file=sys.stderr)

def read_food():
	res = None
	try:
		with open(settings['food_cache_file'], "r") as f:
			res = f.read().rstrip()
		return res
	except Exception as e:
		print(e, file=sys.stderr)
		return None

client.run(settings['bot_token'])

