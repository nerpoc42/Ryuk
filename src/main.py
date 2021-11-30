import os
from random import randint

import sys
import discord
from discord.ext import tasks
from food import get_food

from settings import settings
from io import StringIO
from contextlib import redirect_stdout
import re
import tempfile
import time
import subprocess

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

def exec_code(orig, code, stream):
	z = re.search('(```)([^\s]*)', orig)
	if not z or not z.groups() or not z.groups()[1]:
		lang = "python"
	else:
		lang = z.groups()[1].lower()
	
	if lang == "python" or lang == "py":
		try:
			exec(code)
		except Exception as e:
			print(e)
	elif lang == "c":
		with open('./comp_code/code.c', 'w') as fp:
			fp.write(code)
		val = subprocess.run('g++ -o ./comp_code/res_c ./comp_code/code.c; ./comp_code/res_c', shell=True, capture_output=True)
		if val.stderr:
			print(val.stderr.decode("utf-8"))
		elif val.stdout:
			print(val.stdout.decode("utf-8"))
	elif lang == "cpp" or lang == "c++":
		with open('./comp_code/code.cpp', 'w') as fp:
			fp.write(code)
		val = subprocess.run('g++ -o ./comp_code/res_cpp ./comp_code/code.cpp; ./comp_code/res_cpp', shell=True, capture_output=True)
		if val.stderr:
			print(val.stderr.decode("utf-8"))
		elif val.stdout:
			print(val.stdout.decode("utf-8"))
		
	else:
		print("Nepažįstu šitos kalbos")

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	content = message.content.lower()

	if message.content.startswith('$'):
		await message.channel.send('No')
		# text = re.sub('```[^\s]*', '', message.content)[1:].lstrip()
		
		# stream = StringIO()
		# with redirect_stdout(stream):
		# 	exec_code(message.content, text, stream)
			
		# res = stream.getvalue()
		# if res:
		# 	await message.channel.send(content=res)
		return

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
		return
	

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

