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
import asyncio
import twitter
import tweepy
import random
import os
import time
from os import walk
import datetime
from discord.utils import get
dir_path = os.path.dirname(os.path.realpath(__file__))

#Variables that contains the user credentials to access Twitter API
t = open("TwitterSecret.txt", "r")
c = open("ConsumerSecret.txt", "r")
access_token = "3303963448-DYXKxwkKTeOZPScOBgXVGLDfrl8DR0ZQsrQvMQp"
access_token_secret =  t.read()
consumer_key = "anEmKfK4WLIW5IIPyQk7mgWLn"
consumer_secret = c.read()
twitterapi = twitter.Api(consumer_key,consumer_secret,access_token,access_token_secret, tweet_mode='extended')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
f = open("TOKEN.txt", "r")
TOKEN = f.read();
running = False
client = discord.Client()

async def TaskLoop():
    tChannel = client.get_channel(590822617858965514)
    while(True):
        #channel = client.get_channel(520565813443559435)
        dino = api.get_user('DinosaurEarth')
        flat = api.get_user('FlatEarthOrg')
        msg = dino.screen_name + " has: " + str(dino.followers_count) + " followers!" + "\n"
        msg += flat.screen_name + " has: " + str(flat.followers_count) + " followers!" + "\n" + "***"
        if (dino.followers_count < flat.followers_count):
            msg += flat.screen_name + " has " + str(flat.followers_count - dino.followers_count) + " more followers!" + "\n" + "***"
        else:
            msg += dino.screen_name + " has " + str(dino.followers_count - flat.followers_count) + " more followers!" + "\n" + "***"

        await tChannel.send(msg)
        await asyncio.sleep(3600)


@client.event
async def on_message(message):
    global running
    if(running == False):
        client.loop.create_task(TaskLoop())
    running = True
    rand = random.randint(0,200)
    text = message.content.lower()
    msg = ""
    author = message.author

    #if message author is this bot
    if author == client.user:
        #stop the bot replying to itself
        return

    #if author is any bot
    if author.bot == True:
        #stop bot from responding
        return

    #get 20 latest tweets from dinosaur earth society and add them to a dict
    t = twitterapi.GetUserTimeline(screen_name="DinosaurEarth", count=20)
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

