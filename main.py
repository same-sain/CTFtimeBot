import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
from datetime import datetime, timedelta
import time
import asyncio
from config import load_config
from constants import Token, GUILD_ID 


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

def create_ctf_embed(info):
    def format_ctf_time(iso_time: str):
        dt = datetime.fromisoformat(iso_time.replace('Z', "+00:00"))
        dt_th = dt + timedelta(hours=7)
        return dt_th.strftime("%d/%m/%Y %H:%M")
    
    start_time = format_ctf_time(info['start'])
    finish_time = format_ctf_time(info['finish'])

    embed = discord.Embed(
        title=info['title'],
        url=info['url'],
        description=info['description'],
        color=discord.Color.dark_red()
    )
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7nr78opGAJ7CSFEOM6JccyZhPElGrmeIFOA&s")
    embed.add_field(name="date", value=f'start: {start_time}\nFinish: {finish_time}', inline=False)

    duration = info.get('duration', {})
    days = duration.get('days', 0)
    hours = duration.get('hours', 0)
    
    if days <= 0:
        embed.add_field(name="duration", value=f"{hours} hour", inline=True)
    else:
        embed.add_field(name="duration", value=f"{days} day {hours} hours", inline=True)

    embed.add_field(name='Format', value=info['format'], inline=True)
    embed.add_field(name="onsite", value=info['onsite'], inline=True)
    embed.add_field(name="weight", value=info['weight'], inline=True)

    if info['restrictions'] == "Individual":
        embed.add_field(name='restrictions', value=f"{info['restrictions']}", inline=True)
    else:
        embed.add_field(name='restrictions', value=f"{info['restrictions']} {info['participants']} team will participate", inline=True)

    embed.set_footer(text=f"CTF ID: {info['id']}") 
    
    if info.get('organizers'):
        embed.set_author(name=info['organizers'][0]['name'], url=info['url'], icon_url=info.get('logo'))
        
    return embed

client.create_ctf_embed = create_ctf_embed

@client.tree.command(name="clearsyn", description="⚠️ Clear all global and guild commands.")
async def clear_syn(interaction: discord.Interaction):
    
    await interaction.response.defer(ephemeral=True)
    
    client.tree.clear_commands(guild=None)
    await client.tree.sync()
    
    if GUILD_ID:
        client.tree.clear_commands(guild=discord.Object(id=GUILD_ID))
        await client.tree.sync(guild=discord.Object(id=GUILD_ID))
    
    await interaction.followup.send("✅ ล้าง Global และ Guild Application Commands ทั้งหมดเรียบร้อยแล้ว! โปรดรอ 1-2 นาทีเพื่อให้ Discord อัปเดต", ephemeral=True)

@tasks.loop(seconds=60)
async def check_time_loop():
    now_str = datetime.now().strftime("%H:%M")
    config = load_config()

    if not config.get('time') or now_str != config['time']:
        return

    now_ts = int(time.time())
    config_time = config['time']
    one_week_later = now_ts + 7 * 24 * 60 * 60
    
    limit = config.get('limit', 10) 
    response = requests.get(f"https://ctftime.org/api/v1/events/?limit={limit}&start={now_ts}&finish={one_week_later}")
    CTFtimedata = response.json()

    channel_id = config.get('channel_id')
    channel = client.get_channel(channel_id)
    
    if len(config_time) == 4 and config_time[1] == ':':
        config_time = f"0{config_time}"
    if now_str != config_time: 
        return
    if not channel:
        print(f"Error: Channel with ID {channel_id} not found or inaccessible.")
        return

    notify_roles_ids = config.get('notify_roles', [])
    
    mention_list = []
    
    guild = client.get_guild(channel.guild.id) if channel and channel.guild else None
    everyone_role_id = guild.default_role.id if guild else None

    for role_id in notify_roles_ids:
        if role_id == everyone_role_id: 
            mention_list.append("@everyone")
        else:
            mention_list.append(f"<@&{role_id}>")
            
    mention_roles_string = " ".join(mention_list) 
    
    mention_message = f"🔔 แจ้งเตือน CTF time\n{mention_roles_string}\n" 

    await channel.send(mention_message)
    
    for info in CTFtimedata:
        if 'id' not in info:
            continue
            
        embed = create_ctf_embed(info)
        await channel.send(embed=embed)


@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        error_message = "❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้ (สิทธิ์ถูกจำกัดไว้สำหรับคนที่มี Admin/Manage Guild Perms หรือ Role ผู้ดูแลที่ถูกตั้งค่าไว้)"
        if interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)
        return

    print(f"App Command Error: {error}")



@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')

    if not check_time_loop.is_running():
        check_time_loop.start()
        print('Time loop started')

    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')

async def main():
    async with client:
        await client.load_extension("cogs.configuration") 
        await client.load_extension("cogs.subscribe") 
        await client.load_extension("cogs.search")
        await client.start(Token)



asyncio.run(main())
