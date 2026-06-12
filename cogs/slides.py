from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, TextInput, Select, View
from bot import supabase
import discord


class ResourceTypeSelect(discord.ui.Select):
    def __init__(self, options, url_map):
        super().__init__(placeholder="請選擇資源項目...", min_values=1, max_values=1, options=options)
        self.label_map = {option.value: option.label for option in options}
        self.url_map = url_map

    async def callback(self, interaction: discord.Interaction):
        selected_value = self.values[0]
        selected_label = self.label_map.get(selected_value, "選擇項目")
        selected_url = self.url_map.get(selected_value, "")
        embed = discord.Embed(title=f"{selected_label}", description=f"[資源連結]({selected_url})", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)


class SelectView(discord.ui.View):
    def __init__(self, options, url_map):
        super().__init__()
        self.add_item(ResourceTypeSelect(options, url_map))


class Slides(commands.Cog):
    """Slide 主要功能"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ciallo", description="打招呼")
    async def greet(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Ciallo～(∠・ω< )⌒☆")

    @app_commands.command(name="查看項目", description="查看所有資源")
    async def view_items(self, interaction: discord.Interaction):
        try:
            res = supabase.table("sourse").select("*").execute()
            if not res or not res.data:
                await interaction.response.send_message("目前沒有任何資源。")
                return

            items = sorted(res.data, key=lambda item: item.get('date', ''), reverse=True)  
            total = len(items)
            item_options = []

            url_map = {}
            for idx, item in enumerate(items):
                option_value = str(item.get('id', idx))
                url_map[option_value] = item.get('url', '')
                item_options.append(
                    discord.SelectOption(
                        label=item.get('name', '無名稱')[:100],
                        description=str(item.get('date', ''))[:100],
                        value=option_value,
                    )
                )

            embed = discord.Embed(title="📚 資源列表", description=f"總共有 {total} 個項目", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, view=SelectView(item_options, url_map))
        except Exception as e:
            await interaction.response.send_message(f"查看項目失敗：{e}")


async def setup(bot: commands.Bot):
    """載入此 Cog"""
    await bot.add_cog(Slides(bot))
