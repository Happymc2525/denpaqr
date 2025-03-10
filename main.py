import discord
from discord import Option
import random
import string
import qrcode

TOKEN = 'ここにBotトークン'
bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} 起動しました")

@bot.slash_command(description="QRコード生成")
async def qr(
  ctx: discord.ApplicationContext,
  data: Option(str, required=False, description="データ指定")
):
  data = data or (''.join(random.choices(string.ascii_letters + string.digits, k=16)))
  img = qrcode.make(data)
  img.save('qr.png')
  await ctx.respond(f'{data}', file=discord.File('qr.png'))

@bot.slash_command(description="QRコード生成(プライベート)")
async def sqr(
  ctx: discord.ApplicationContext,
  data: Option(str, required=False, description="データ指定")
):
  data = data or (''.join(random.choices(string.ascii_letters + string.digits, k=16)))
  img = qrcode.make(data)
  img.save('qr.png')
  await ctx.respond(f'{data}', file=discord.File('qr.png'), ephemeral=True)

bot.run(TOKEN)
