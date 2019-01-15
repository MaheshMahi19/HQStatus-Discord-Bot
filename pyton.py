import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from hq_api import HQApi as hq
from dateutil import parser
from pytz import timezone
from datetime import datetime

api = hq("Place your Bearer token Here")
#note: Game time was in GMT
#If u want to convert use pytz and datetime libs
print(api.get_show())
client = commands.Bot(command_prefix="..")
@client.event
async def on_ready():
    print("Bot is logged on ",client.user.name)
    print("With user id",client.user.id)
    print("----------------------------")

@client.command(pass_context=True,no_pm=True)
async def hqstats(ctx, user:str ):
    searchuname = api.search(user)
    unamedata = searchuname['data']
    if not unamedata:
        embed = discord.Embed(title="HQ's Profile Error", description="Got an Error By HQ's server",color = discord.Colour.magenta())
        embed.add_field(name="The Name u entered",value=str(user),inline=False)
        embed.add_field(name="What is Error",value="No username Found",inline=False)
        embed.set_footer(text="Mahesh")
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Error.svg/2000px-Error.svg.png")
        await client.say(embed=embed)
    else:
        nexts = unamedata[0]
        idu = nexts['userId']
        details = api.get_user(idu)
        embed = discord.Embed(title="HQ Status of "+user,description="Status of your HQ's Profile",colour=discord.Colour.red())
        embed.set_author(name="HQ's Details",icon_url="https://i.ytimg.com/vi/6GjaUu9tOaA/maxresdefault.jpg")
        embed.set_footer(text="Mahesh")
        img=details['avatarUrl']
        embed.set_thumbnail(url=img)
        embed.add_field(name="HQ's Username",value='__'+details['username']+'__',inline=True)
        embed.add_field(name="HQ's UserId", value='__'+str(details['userId'])+'__',inline=True)
        embed.add_field(name="Your's Refferal Url", value='__'+details['referralUrl']+'__',inline=True)
        embed.add_field(name="Total Games Played", value='__'+str(details['gamesPlayed'])+'__',inline=False)
        embed.add_field(name="TotalWins", value='__'+details['leaderboard']['alltime']['total']+'__',inline=True)
        embed.add_field(name="Weekly Total", value='__'+details['leaderboard']['weekly']['total']+'__',inline=True)
        embed.add_field(name="All Time Rank", value='__'+str(details['leaderboard']['alltime']['rank'])+'__',inline=True)
        embed.add_field(name="Weekly Rank", value='__'+str(details['leaderboard']['rank'])+'__',inline=True)
        embed.add_field(name="Unclaimed Money", value='__'+details['leaderboard']['unclaimed']+'__',inline=False)
        embed.add_field(name="Total Achievments Count", value='__'+str(details['achievementCount'])+'__',inline=True)
        embed.add_field(name="Your's High Score", value='__'+str(details['highScore'])+'__',inline=True)
        point = details['seasonXp']
        points = point[0]
        total =points['currentPoints']+points['remainingPoints']
        embed.add_field(name="This Season XP", value='__'+str(points['currentPoints'])+"/"+str(total)+'__',inline=False)
        embed.add_field(name="Current Level", value='__'+str(points['currentLevel']['level'])+'__',inline=False)
        embed.add_field(name="Any Refferals", value='__'+str(points['quotas']['currentReferrals'])+'__',inline=False)
        original_date = parser.parse(details['created'])
        creates = original_date.strftime("%a %d %b %Y, %H:%M:%S GMT")
        embed.add_field(name="Account Created At", value='__'+str(creates)+'__',inline=False)
        
   
    
        await client.say(embed=embed)

@client.command(pass_context=True,no_pm=True)
async def hqgame(ctx):
    x = api.get_show()
    y = x['upcoming']
    z = y[0]
    original_date = parser.parse(str(z['time']))
    showd = original_date.strftime("%a %d %b %Y, %H:%M:%S GMT")
    embed = discord.Embed(title="Next HQ's Details",description="Details About HQ's Next Game",colour=discord.Colour.dark_gold())
    embed.add_field(name="Next HQ Type",value = str(z['showType'] + z['gameType']))
    embed.add_field(name="Next HQ's Prize", value=z['prize'])
    embed.add_field(name="Game Time", value=showd)
    embed.set_thumbnail(url="https://i.ytimg.com/vi/6GjaUu9tOaA/maxresdefault.jpg")
    await client.say(embed=embed)
client.run('NTE2OTYwNjE3NTI1OTM2MTQ4.DvZqlg.zp-YITA-q-0eOk5AYpQEL329z5w')
