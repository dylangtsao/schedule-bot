import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pytz


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')
bot.classes = []
bot.reminders = []


@bot.command()
async def hello(ctx):
  await ctx.send("hello " + ctx.author.display_name + "! Welcome to the SOSP test server.")

@bot.command()
async def addClass(ctx, *, item):
  in_list = False
  it1, it2 = item.split(",")
  for (key,value) in bot.classes: 
    if (key == it1):
      await ctx.send(item + " already in list!")
      in_list = True;
  if (in_list == False):
    bot.classes.append([it1, calculateGrade(it2)])
    await ctx.send(it1 + " added!")
    print(bot.classes)
    
@bot.command()
async def removeClass(ctx, *, item):
  in_list = False
  for (key,value) in bot.classes:
    if (key == item):
      bot.classes.remove([key, value])
      await ctx.send(item + " removed!")
      in_list = True;
  if (in_list == False):
    await ctx.send("You are not registered for " + item)
  print(bot.classes)

@bot.command()
async def addReminder(ctx, *, item):
  bot.reminders.append(item)
  await ctx.send(item + " added to Reminders!")
  print(bot.reminders)

@bot.command()
async def classes(ctx): 
    to_string = "Classes"
    if len(bot.classes) == 0:
        await ctx.send("No classes avaliable")
    else:
      column_headers = ['Class','Grade']
      row_headers = []
      for (key,value) in bot.classes:
        row_headers.append("")
      fig,ax = plt.subplots()
      ax.set_axis_off()
      table = ax.table(cellText=bot.classes,
                        rowLabels=row_headers,
                        rowLoc='right',
                        colLabels=column_headers,
                        loc= 'center',
                        )
      plt.savefig(fname='plot',
                  bbox_inches='tight',
                  facecolor='dimgrey',
                  cellColours='dimgrey')
      await ctx.send(file=discord.File('plot.png'))

    

@bot.command()
async def removeReminder(ctx, *, item):
  in_list = False
  for r in bot.reminders:
    if (r == item):
      bot.reminders.remove(item)
      await ctx.send(item + " removed from Reminders")
      in_list = True
  if (in_list == False):
    await ctx.send(item + " is not a Reminder")
  
  print(bot.reminders)

@bot.command()
async def reminders(ctx):
  if (len(bot.reminders) != 0):
    to_string = ""
    count = 1
    for r in bot.reminders:
      to_string += f'{str(count)}. {r}\n'
      count += 1
      print(to_string)
    await ctx.send(to_string)
  else:
    tz_CA = pytz.timezone('America/Los_Angeles') 
    datetime_CA = datetime.now(tz_CA)
    await ctx.send("You have no reminders as of: " + datetime_CA.strftime("%H:%M:%S"))

def calculateGrade(it2):
    grade = 0.0
    if it2 == 'A+' or it2 == 'A':
        grade = 4.0
    elif it2 == 'A-':
        grade = 3.7
    elif it2 == 'B+':
        grade = 3.3
    elif it2 == 'B':
        grade = 3.0
    return grade

@bot.command()
async def changeGrade(ctx, *, item):
    it1, it2 = item.split(",")
    grade = calculateGrade(it2)
    changed = False
    for (key, value) in bot.classes:
        if key == it1: 
            value = grade
            await ctx.send(f"Grade for {it1} changed to {str(value)}") 
            changed = True
            break
    if (changed == False):
        await ctx.send("Invalid class")
    print(value)

@bot.command()
async def gpa(ctx):
    add = 0
    count = 0
    for (key, value) in bot.classes:
        if value != 0.0:
            add += value
            count+=1
    if (len(bot.classes) != 0):
      gpa = add/count
      print(gpa)
      await ctx.send('GPA: %.2f' %gpa)
    else:
      await ctx.send("0 Classes Inputted")

bot.run(TOKEN)
