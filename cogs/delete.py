from discord.ext import commands
from discord import app_commands
from discord.ui import Select, Button, View
from bot import supabase
import discord


class DeleteSelect(discord.ui.Select):
    def __init__(self, options, id_map, items):
        super().__init__(placeholder="選擇要刪除的項目", min_values=1, max_values=min(len(options), 25), options=options)
        self.id_map = id_map
        self.items = items
        self.deleted_items = []

    async def callback(self, interaction: discord.Interaction):
        selected_ids = self.values
        self.deleted_items = []
        
        for selected_id in selected_ids:
            item = self.id_map.get(selected_id)
            if item:
                try:
                    supabase.table("sourse").delete().eq("id", selected_id).execute()
                    self.deleted_items.append(item)
                except Exception:
                    pass

        names_text = "、".join([item["name"] for item in self.deleted_items]) if self.deleted_items else "(沒有刪除項目)"
        embed = discord.Embed(
            title="刪除完成",
            description=f"已刪除項目: {names_text}",
            color=discord.Color.red()
        )
        embed.set_footer(text="按下方還原按鈕可復原被刪除的項目")
        await interaction.response.edit_message(embed=embed, view=RestoreView(self.deleted_items))


class RestoreButton(discord.ui.Button):
    def __init__(self, deleted_items):
        super().__init__(label="還原", style=discord.ButtonStyle.success)
        self.deleted_items = deleted_items

    async def callback(self, interaction: discord.Interaction):
        if not self.deleted_items:
            await interaction.response.edit_message(content="沒有項目可還原", embed=None, view=None)
            return

        restored_names = []
        for item in self.deleted_items:
            try:
                supabase.table("sourse").insert({
                    "url": item.get("url"),
                    "name": item.get("name"),
                    "date": item.get("date")
                }).execute()
                restored_names.append(item["name"])
            except Exception:
                pass

        names_text = "、".join(restored_names) if restored_names else "(沒有還原項目)"
        embed = discord.Embed(
            title="還原完成",
            description=f"已還原項目: {names_text}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=None)


class RestoreView(discord.ui.View):
    def __init__(self, deleted_items):
        super().__init__()
        self.add_item(RestoreButton(deleted_items))


class DeleteView(discord.ui.View):
    def __init__(self, options, id_map, items):
        super().__init__()
        self.add_item(DeleteSelect(options, id_map, items))


class DeleteCog(commands.Cog):
    """刪除資源功能"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="刪除項目", description="刪除資源項目")
    async def delete_items(self, interaction: discord.Interaction):
        try:
            res = supabase.table("sourse").select("*").execute()
            if not res or not res.data:
                await interaction.response.send_message("目前沒有任何資源可刪除。")
                return

            items = sorted(res.data, key=lambda item: item.get('date', ''), reverse=True)
            options = []
            id_map = {}
            for idx, item in enumerate(items):
                option_value = str(item.get('id', idx))
                id_map[option_value] = item
                options.append(
                    discord.SelectOption(
                        label=item.get('name', '無名稱')[:100],
                        description=str(item.get('date', ''))[:100],
                        value=option_value,
                    )
                )

            embed = discord.Embed(
                title="刪除資源項目",
                description="請選擇要刪除的項目（可多選）",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, view=DeleteView(options, id_map, items))
        except Exception as e:
            await interaction.response.send_message(f"刪除項目失敗：{e}")


async def setup(bot: commands.Bot):
    """載入此 Cog"""
    await bot.add_cog(DeleteCog(bot))
