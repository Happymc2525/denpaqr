import discord
from discord import Option
from discord.ui import Button, Select, View
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
    # QRコードを生成する非同期関数
    async def generate_qr(generate_random=True):
        # `generate_random` が True の場合はランダムな文字列を生成
        if generate_random:
            qr_data = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        else:
            # data が指定されている場合、そのデータをQRコードに使用
            qr_data = data or ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        # QRコードを生成してファイルに保存
        img = qrcode.make(qr_data)
        img.save("qr.png")
        # 生成したQRコードのデータを返す
        return qr_data

    # 初期のQRコードを生成
    qr_data = await generate_qr(generate_random=False)  # 最初のQRコードではdataを使用

    # QRコードの再生成ボタンのビュー
    class QRButtonView(View):
        @discord.ui.button(label="再生成", style=discord.ButtonStyle.primary)
        async def regenerate(self, button: Button, interaction: discord.Interaction):
            # 再生成時はdataを無視してランダムな文字列でQRコードを生成
            new_data = await generate_qr(generate_random=True)  # `generate_random=True` でランダムなデータ生成
            # 新しいQRコード画像ファイルを作成
            file = discord.File("qr.png", filename="qr.png")
            # 最初のメッセージを更新（画像を新しいものに差し替える）
            # 既存の画像を削除するためにattachmentsを空にして、新しい画像をfilesに渡す
            await interaction.response.edit_message(content=new_data, attachments=[], files=[file])

    # 初回のQRコードと再生成ボタンを表示
    msg = await ctx.respond(content=qr_data, file=discord.File("qr.png"), view=QRButtonView())


@bot.slash_command(description="QRコード生成(プライベート)")
async def sqr(
    ctx: discord.ApplicationContext,
    data: Option(str, required=False, description="データ指定")
):
    # QRコードを生成する非同期関数
    async def generate_qr(generate_random=True):
        # `generate_random` が True の場合はランダムな文字列を生成
        if generate_random:
            qr_data = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        else:
            # data が指定されている場合、そのデータをQRコードに使用
            qr_data = data or ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        # QRコードを生成してファイルに保存
        img = qrcode.make(qr_data)
        img.save("qr.png")
        # 生成したQRコードのデータを返す
        return qr_data

    # 初期のQRコードを生成
    qr_data = await generate_qr(generate_random=False)  # 最初のQRコードではdataを使用

    # QRコードの再生成ボタンのビュー
    class QRButtonView(View):
        @discord.ui.button(label="再生成", style=discord.ButtonStyle.primary)
        async def regenerate(self, button: Button, interaction: discord.Interaction):
            # 再生成時はdataを無視してランダムな文字列でQRコードを生成
            new_data = await generate_qr(generate_random=True)  # `generate_random=True` でランダムなデータ生成
            # 新しいQRコード画像ファイルを作成
            file = discord.File("qr.png", filename="qr.png")
            # 最初のメッセージを更新（画像を新しいものに差し替える）
            # 既存の画像を削除するためにattachmentsを空にして、新しい画像をfilesに渡す
            await interaction.response.edit_message(content=new_data, attachments=[], files=[file])

    # 初回のQRコードと再生成ボタンを表示、ephemeralでコマンド使用者にのみ表示
    msg = await ctx.respond(content=qr_data, file=discord.File("qr.png"), view=QRButtonView(), ephemeral=True)

bot.run(TOKEN)
