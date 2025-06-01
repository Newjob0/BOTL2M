import discord
from discord import app_commands
from datetime import datetime, timedelta
from dotenv import load_dotenv
from keep_alive import keep_alive
import os

load_dotenv()
keep_alive()

GUILD_ID = discord.Object(id=1378644585965682748)

boss_info = {
    "เชลทูบา": 6, "เคลซอส": 10, "บาซิลา": 4, "ชาวาน": 12,
    "รานีมีแม่มด": 6, "ทรอมบา": 7, "เฟลิส": 3, "เอนคูรา": 6,
    "ทาลาคิน": 10, "แบนด์ไลท์": 12, "ทีมีทริส": 8, "ซาร์กา": 10,
    "สตัน": 7, "เทมเพสต์": 6, "มิวแทนต์คูร์มา": 8, "คูรม่าที่ปนเปื้อน": 8,
    "คาทาน": 10, "คอร์ซาเซปต้า": 10, "มาทูรา": 6, "เบรก้า": 6,
    "บันนาโรค": 5, "เมดูซ่า": 10, "แบล็คลิลลี่": 12, "เบฮีมอธ": 9,
    "ดราก้อนบีสต์": 12, "คูม่าชั้น3": 8, "คูม่าชั้น6": 10, "คูม่าชั้น7": 10
}

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync(guild=GUILD_ID)
        print(f"✅ Logged in as {self.user}")
        print(f"🔁 Slash commands synced to guild {GUILD_ID.id}")

client = MyClient()

@app_commands.autocomplete("bossname")
@app_commands.guilds(GUILD_ID)
async def bossname_autocomplete(interaction: discord.Interaction, current: str):
    matches = [
        app_commands.Choice(name=name, value=name)
        for name in boss_info if current.lower() in name.lower()
    ]
    return matches[:25]

@app_commands.guilds(GUILD_ID)
@client.tree.command(name="บอสตาย", description="บันทึกเวลาตายของบอส แล้วคำนวณเวลาเกิดใหม่")
@app_commands.describe(bossname="เลือกชื่อบอส", death_time="เวลาตาย เช่น 14:00")
async def boss_dead(interaction: discord.Interaction, bossname: str, death_time: str):
    try:
        now = datetime.now()
        dt = datetime.strptime(death_time, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if dt < now:
            dt += timedelta(days=1)
        add_hour = boss_info.get(bossname)
        respawn = dt + timedelta(hours=add_hour)
        embed = discord.Embed(title=f"📋 บอส: {bossname}", color=0x00ff99)
        embed.add_field(name="🕓 เวลาตาย", value=death_time, inline=True)
        embed.add_field(name="⏱ เวลาคำนวณ", value=f"{add_hour} ชั่วโมง", inline=True)
        embed.add_field(name="💥 เวลาเกิดใหม่", value=respawn.strftime("%H:%M"), inline=False)
        embed.set_footer(text=f"โดย {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"❌ เกิดข้อผิดพลาด: {str(e)}", ephemeral=True)

client.run(os.getenv("DISCORD_TOKEN"))
