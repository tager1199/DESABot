#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Thomas
#
# Created:     26/03/2019
# Copyright:   (c) Thomas 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import discord
import twitter
import random
import os
from os import walk
from discord.utils import get
dir_path = os.path.dirname(os.path.realpath(__file__))

#Variables that contains the user credentials to access Twitter API
t = open("TwitterSecret.txt", "r")
c = open("ConsumerSecret.txt", "r")
access_token = "3303963448-DYXKxwkKTeOZPScOBgXVGLDfrl8DR0ZQsrQvMQp"
access_token_secret =  t.read()
consumer_key = "anEmKfK4WLIW5IIPyQk7mgWLn"
consumer_secret = c.read()
pic_ext = ['.jpg','.png','.jpeg']
api = twitter.Api(consumer_key,consumer_secret,access_token,access_token_secret, tweet_mode='extended')
rate = ["Excellent Woofer", "Much Cute", "Lovely Doggo", "Thats a big ol' pupper"]

f = open("TOKEN.txt", "r")
TOKEN = f.read();

client = discord.Client()

@client.event
async def on_message(message):
    rand = random.randint(0,200)
    text = message.content.lower()
    msg = ""
    author = message.author

    await client.say('296381421457637377', enszomessage)
    await asyncio.sleep(120)

    #if message author is this bot
    if author == client.user:
        #stop the bot replying to itself
        return

    #if author is any bot
    if author.bot == True:
        #stop bot from responding
        return

    #get 20 latest tweets from @dog_feelings and add them to a dict
    t = api.GetUserTimeline(screen_name="DinosaurEarth", count=20)
    tweets = [i.AsDict() for i in t]
    if text.startswith('what was the latest tweet'):
        #get random tweet from the dict of tweets
        msg = tweets[0]['full_text']
        #send tweet as message
        await message.channel.send(msg)

@client.event
#log basic info when the bot starts running
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)