import os
import discord
from discord.ext import commands
from discord import app_commands
import requests

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def obter_emoji_clima(condicao: str) -> str:
    emojis = {
        "thunderstorm": "⛈️",
        "drizzle": "🌦️",
        "rain": "🌧️",
        "snow": "❄️",
        "mist": "🌫️",
        "fog": "🌫️",
        "clear": "☀️",
        "clouds": "☁️",
    }
    for chave, emoji in emojis.items():
        if chave in condicao.lower():
            return emoji
    return "🌡️"


class Clima(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="clima",
        description="Mostra o clima de uma cidade (precisa de chave OpenWeather).",
    )
    @app_commands.describe(cidade="O nome da cidade, ex: São Paulo")
    async def clima(self, interaction: discord.Interaction, cidade: str):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            await interaction.response.send_message(
                "⚠️ O comando `/clima` ainda não está configurado.\n"
                "O administrador precisa adicionar `OPENWEATHER_API_KEY` no arquivo `.env` "
                "(chave gratuita em https://openweathermap.org/api).",
                ephemeral=True,
            )
            return

        await interaction.response.defer()
        try:
            resposta = requests.get(
                OPENWEATHER_URL,
                params={
                    "q": cidade,
                    "appid": api_key,
                    "units": "metric",
                    "lang": "pt_br",
                },
                timeout=10,
            )
            if resposta.status_code == 404:
                await interaction.followup.send(
                    f"❌ Cidade **{cidade}** não encontrada.", ephemeral=True
                )
                return
            resposta.raise_for_status()
            dados = resposta.json()

            clima_info = dados["weather"][0]
            temperatura = dados["main"]["temp"]
            sensacao = dados["main"]["feels_like"]
            umidade = dados["main"]["humidity"]
            vento = dados["wind"]["speed"]
            nome = dados["name"]
            pais = dados["sys"]["country"]

            embed = discord.Embed(
                title=f"{obter_emoji_clima(clima_info['main'])} Clima em {nome} ({pais})",
                description=clima_info["description"].capitalize(),
                color=discord.Color.blue(),
            )
            embed.add_field(name="🌡️ Temperatura", value=f"**{temperatura:.1f}°C**", inline=True)
            embed.add_field(name="🤔 Sensação", value=f"{sensacao:.1f}°C", inline=True)
            embed.add_field(name="💧 Umidade", value=f"{umidade}%", inline=True)
            embed.add_field(name="💨 Vento", value=f"{vento} m/s", inline=True)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"Erro no /clima: {e}")
            await interaction.followup.send(
                "❌ Erro ao buscar o clima. Tente novamente mais tarde.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Clima(bot))
