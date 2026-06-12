from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, TextInput
from bot import supabase
import discord


class AddItemModal(Modal, title='新增項目'):
    name = TextInput(
        label='名稱', 
        placeholder='請輸入資源名稱', 
        min_length=1,
        max_length=100,
        required=True,
    )
    url = TextInput(
        label='連結', 
        placeholder='https://...', 
        style=discord.TextStyle.short,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            supabase.table("sourse").insert({
                "url": self.url.value, 
                "name": self.name.value, 
                "date": interaction.created_at.isoformat(timespec='milliseconds')
            }).execute()

            embed = discord.Embed(
                title="項目新增成功",
                description=f" - [{self.name.value}]({self.url.value})",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"{interaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="新增項目失敗", 
                description=f"{e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class AddCog(commands.Cog):
    """新增資源功能"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="新增項目", description="開啟表單加入新資源")
    async def add_item(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddItemModal())


async def setup(bot: commands.Bot):
    """載入此 Cog"""
    await bot.add_cog(AddCog(bot))
