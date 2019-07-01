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
t = open("/home/pi/Desktop/DESABot/TwitterSecret.txt", "r")
c = open("/home/pi/Desktop/DESABot/ConsumerSecret.txt", "r")
access_token = "3303963448-DYXKxwkKTeOZPScOBgXVGLDfrl8DR0ZQsrQvMQp"
access_token_secret =  t.read()
consumer_key = "anEmKfK4WLIW5IIPyQk7mgWLn"
consumer_secret = c.read()
twitterapi = twitter.Api(consumer_key,consumer_secret,access_token,access_token_secret, tweet_mode='extended')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
f = open("/home/pi/Desktop/DESABot/TOKEN.txt", "r")
TOKEN = f.read();
running = False
first = True
dino = api.get_user('DinosaurEarth')
flat = api.get_user('FlatEarthOrg')
lastDiff = 0
client = discord.Client()

async def TaskLoop():
    global first
    global lastDiff
    global dino
    global flat
    reps = 0
    dinoOrig = dino.followers_count
    flatOrig = flat.followers_count
    tChannel = client.get_channel(590822617858965514)
    while(True):
        dino = api.get_user('DinosaurEarth')
        flat = api.get_user('FlatEarthOrg')
        #channel = client.get_channel(520565813443559435)
        dinoGain = dino.followers_count - dinoOrig
        flatGain = flat.followers_count - flatOrig

        msg = dino.screen_name + " has: " + str(dino.followers_count) + " followers!" + "\n"
        msg += flat.screen_name + " has: " + str(flat.followers_count) + " followers!" + "\n" + "***"
        if (dino.followers_count < flat.followers_count):
            msg += flat.screen_name + " has " + str(flat.followers_count - dino.followers_count) + " more followers!" + "***" + "\n"
        else:
            msg += dino.screen_name + " has " + str(dino.followers_count - flat.followers_count) + " more followers!" + "***" + "\n"
        percent = (float(dino.followers_count/flat.followers_count))*100
        percent = round(percent,2)
        msg += "***" + dino.screen_name +  " has: " + str(percent) + "% of " + flat.screen_name + "'s followers!" + "***"  + "\n"
        diff = flat.followers_count - dino.followers_count
        if (reps%24 == 0):
            lastDiff = diff
        if lastDiff != 0:
            msg += dino.screen_name + " has gained on " + flat.screen_name + " by " + str(lastDiff - diff) + " followers!" + "\n"
        
        if (reps < 24):
            days = 1
        else:
            days = int(reps/24)
            
        dinoAv = dinoGain/days
        flatAv = flatGain/days    
        
        if (dinoGain > flatGain):
            msg += "At this rate " + dino.screen_name + " will reach "
            if dino.followers_count < flat.followers_count*0.5:
                msg += "50% of " + flat.screen_name + " in "
                perc = 0.5
            elif dino.followers_count < flat.followers_count*0.6:
                msg += "60% of " + flat.screen_name + " in "
                perc = 0.6
            elif dino.followers_count < flat.followers_count*0.7:
                msg += "70% of " + flat.screen_name + " in "
                perc = 0.7
            elif dino.followers_count < flat.followers_count*0.8:
                msg += "80% of " + flat.screen_name + " in "
                perc = 0.8
            elif dino.followers_count < flat.followers_count*0.9:
                msg += "90% of " + flat.screen_name + " in "
                perc = 0.9
            elif dino.followers_count < flat.followers_count:
                msg += "100% of " + flat.screen_name + " in "
                perc = 1
                
            overtake = ((perc*flatOrig)-dinoOrig)/(dinoAv-(perc*flatAv))    
                
            msg += str(round(overtake,2)) + " days!!\n"  

        
        if (percent == 50 or percent == 60 or percent == 70 or percent == 80 or percent == 90 or percent == 100):
            msg += "\nCheck out <https://www.dinosaurearthsociety.com/livecount/> for an easter egg"
        currentDT = datetime.datetime.now()
        msg += "\n\nLast updated at: " + str(currentDT.hour) + ":"+ str(currentDT.minute) + " GMT/BST"
        
        if (reps%24 == 0):
            m = await tChannel.send(msg)
            lastDiff = diff
        else:
            await m.edit(content = msg)
        reps += 1
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
        #await message.add_reaction(":roger:398715448859951104")
        return

    #if author is any bot
    if author.bot == True:
        #stop bot from responding
        return
    
    #if str(message.author) in ["tinyman1199#6969"]:
        #await message.add_reaction(r":roger:398715448859951104")
    
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

