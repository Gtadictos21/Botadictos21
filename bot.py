import aiohttp
import os
import math
import asyncio
import random
import json
import time
import psutil
import hikari
import lightbulb

from colorama import Fore 
from colorama import Style
from lightbulb import commands, context
from tldextract import extract
from datetime import datetime
lista_cogs = None

# Cargamos el archivo config.json
with open("config.json") as f:
    data = json.load(f)
    token = data["discord-token"] # Token de Discord
    guild_id = data["guild"] # ID de la guild
    statuschannel = data["statuschannel"] # ID del canal de status
    partidas_channel = data["partidas-channel"] # ID del canal en el que se publican las partidas

    global bot_operators
    bot_operators = data["bot-operators"] # IDs de los operadores del bot (Acceso a cargar/descargar cogs y demas)

    global hetrix_token
    hetrix_token = data["hetrix-token"] # Token para la API de HetrixTools

    global sugchannel
    sugchannel = data["sugchannel"] # Canal de sugerencias

    global logchannel
    logchannel = data["logchannel"] # Canal de Logs

    global SteamToken
    SteamToken = data["steam-token"] # Steam API Token

    global CyberusToken
    CyberusToken = data["cyberus-token"] # Cyberus.dev API Token

# Creamos la instacia del bot, y le pasamos el token, junto con otras configuraciones.
bot = lightbulb.BotApp(
    token=token, 
    prefix="!", 
    banner=None, 
    intents=hikari.Intents.ALL, 
    default_enabled_guilds=guild_id,
    cache_settings=hikari.CacheSettings(max_messages=10000, max_dm_channel_ids=100)
)

# Cargamos todas las extensiones (cogs).
bot.load_extensions_from("./cogs", must_exist=True)

# Iniciamos aiohttp cuando se enciende el bot
@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()

# Acabamos con aiohttp cuando se apaga el bot
@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()

async def bot_status():
    while True:
        await bot.update_presence(activity=hikari.Activity(type=hikari.ActivityType.WATCHING, name="a Gtadictos 21 | Usá /ayuda"))
        await asyncio.sleep(10)
        guild = bot.cache.get_guild(guild_id)
        await bot.update_presence(activity=hikari.Activity(type=hikari.ActivityType.WATCHING, name=f"a {guild.member_count} usuarios | Usá /ayuda"))
        await asyncio.sleep(10)
        elegido_id = random.choice(list(guild.get_members()))
        username = bot.cache.get_user(elegido_id)
        await bot.update_presence(activity=hikari.Activity(type=hikari.ActivityType.WATCHING, name=f"a {username} 👀 | Usá /ayuda"))
        await asyncio.sleep(10)

# Crea el loop y avisa que se encendió.
@bot.listen(hikari.StartedEvent)
async def start_event(_event: hikari.StartedEvent):
    # Iniciamos el loop de status.
    asyncio.create_task(bot_status())

    lista_cogs = [i[:-3] for i in os.listdir('./cogs') if i.endswith('.py')]

    # Imprimimos en consola algunos datos sobre el bot y el servidor.
    disco = psutil.disk_usage('/')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}¡{bot.get_me().username} se ha conectado!{Style.RESET_ALL}')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}El ID del bot es: {Fore.MAGENTA}{bot.get_me().id}{Style.RESET_ALL}')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}Bot creado por: {Fore.MAGENTA}Gtadictos21 {Fore.CYAN}&{Fore.MAGENTA} Galo223344{Style.RESET_ALL}')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}Repositorio oficial: {Fore.MAGENTA}https://gtadictos21.com/Botadictos21{Style.RESET_ALL}')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}ID de los operadores: {Fore.MAGENTA}{bot_operators}{Style.RESET_ALL}')
    print(f'{Fore.RED}[SERVER INFO]{Fore.CYAN}Uso de CPU: {Fore.MAGENTA}{psutil.cpu_percent()}%{Style.RESET_ALL}')
    print(f'{Fore.RED}[SERVER INFO]{Fore.CYAN}Uso de RAM: {Fore.MAGENTA}{math.ceil((psutil.virtual_memory()[3]/1024)/1024)}MB {Fore.CYAN}({Fore.MAGENTA}{psutil.virtual_memory()[2]}%{Fore.CYAN}){Style.RESET_ALL}')
    print(f'{Fore.RED}[SERVER INFO]{Fore.CYAN}Uso de disco: {Fore.MAGENTA}{round(math.ceil(((disco.used/1024)/1024))/1024)}GB{Fore.CYAN}/{Fore.MAGENTA}{round(math.ceil(((disco.total/1024)/1024))/1024)}GB {Fore.CYAN}({Fore.MAGENTA}{round(math.ceil(((disco.free/1024)/1024))/1024)}GB{Fore.CYAN}){Style.RESET_ALL}')
    print(f'{Fore.RED}[SERVER INFO]{Fore.CYAN}Ping: {Fore.MAGENTA}{round(bot.heartbeat_latency * 1000)}ms')

    # Enviamos un embed al canal "statuschannel".
    channel = bot.cache.get_guild_channel(statuschannel)
    start_time = time.time()
    message = await bot.rest.create_message(channel, "API ping")
    end_time = time.time()
    await message.delete()

    embed = (
        hikari.Embed(
            title=f"¡{bot.get_me().username} se ha conectado!",
            description=f"El ID del bot es: `{bot.get_me().id}`",
            timestamp=datetime.now().astimezone(),
            color=hikari.Colour(0x2bff00),
        )
        .add_field(
            name="ID de los operadores:",
            value=f"`{bot_operators[0]}`, `{bot_operators[1]}`",
            inline=False,
        )
        .add_field(
            name="Uso de CPU:",
            value=f"{psutil.cpu_percent()}%",
            inline=True,
        )
        .add_field(
            name="Uso de RAM:",
            value=f"{math.ceil((psutil.virtual_memory()[3]/1024)/1024)}MB ({psutil.virtual_memory()[2]}%)",
            inline=True,
        )
        .add_field(
            name="Uso de disco:",
            value=f"{round(math.ceil(((disco.used/1024)/1024))/1024)}GB/{round(math.ceil(((disco.total/1024)/1024))/1024)}GB ({round(math.ceil(((disco.free/1024)/1024))/1024)}GB)",
            inline=True,
        )
        .add_field(
            name="Bot ping:",
            value=f"{round(bot.heartbeat_latency * 1000)}ms",
            inline=True,
        )
        .add_field(
            name="API ping:",
            value=f"{round((end_time - start_time) * 1000)}ms",
            inline=True,
        )
        .set_thumbnail(bot.get_me().avatar_url)
    )
    await bot.cache.get_guild_channel(statuschannel).send(embed=embed)

############################################
#
#
# COMANDOS BASICOS (SPAM & PING)
#
#
############################################

@bot.command
@lightbulb.command("ping", description="¡Revisa la latencia del bot!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def ping(ctx):

    # API ping
    start_time = time.time()
    message = await bot.cache.get_guild_channel(logchannel).send("API ping")
    end_time = time.time()
    await message.delete()

    # Report bot ping
    start_time_api = time.time()
    async with ctx.bot.d.aio_session.get("https://api.cyberus.dev/ping") as res:
        end_time_api = time.time()

    embed = (
        hikari.Embed(
            color=hikari.Colour(0x3B9DFF),
        )
        .add_field(
            name="Bot ping:",
            value=f"{round(bot.heartbeat_latency * 1000)}ms",
            inline=True,
        )
        .add_field(
            name="API ping:",
            value=f"{round((end_time - start_time) * 1000)}ms",
            inline=True,
        )
        .add_field(
            name="Report Bot ping:",
            value=f"{round((end_time_api - start_time_api) * 1000)}ms",
            inline=False,
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

############################################
#
#
# COGS
#
#
############################################

@bot.command
@lightbulb.option("extension", "¡Selecciona la extension a cargar!", hikari.OptionType.STRING, modifier = commands.OptionModifier.CONSUME_REST, choices=lista_cogs)
@lightbulb.command("load", description="¡Carga una extension!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def load(ctx):
    if ctx.author.id not in bot_operators:

        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `BOT_OPERATOR`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    try:
        lista_cogs = [i[:-3] for i in os.listdir('./cogs') if i.endswith('.py')]
        bot.load_extensions(f"cogs.{ctx.options.extension}")
    except Exception as err:
        embed = (
            hikari.Embed(
                title="¡Ha ocurrido un error!",
                description=err,
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El cog \"{ctx.options.extension}\" se ha cargado!{Style.RESET_ALL}')

    embed = (
        hikari.Embed(
            title=f"¡El cog \"{ctx.options.extension}\" se ha cargado!",
            description="",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title="Un operador ha cargado una extensión:",
            description=f"El operador {ctx.author.mention} ha cargado el cog **{ctx.options.extension}**",
            colour=hikari.Colour(0xff6600),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del usuario: {ctx.author.id}",
            icon=ctx.author.avatar_url,
        )
        .set_thumbnail(ctx.author.avatar_url)
    )

    await channel.send(embed=embed)

@bot.command
@lightbulb.option("extension", "¡Selecciona la extension a descargar!", hikari.OptionType.STRING, modifier = commands.OptionModifier.CONSUME_REST, choices=lista_cogs)
@lightbulb.command("unload", description="¡Descarga una extension!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def unload(ctx):
    if ctx.author.id not in bot_operators:

        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `BOT_OPERATOR`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    try:
        lista_cogs = [i[:-3] for i in os.listdir('./cogs') if i.endswith('.py')]
        bot.unload_extensions(f"cogs.{ctx.options.extension}")
    except Exception as err:
        embed = (
            hikari.Embed(
                title="¡Ha ocurrido un error!",
                description=err,
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El cog \"{ctx.options.extension}\" se ha descargado!{Style.RESET_ALL}')

    embed = (
        hikari.Embed(
            title=f"¡El cog \"{ctx.options.extension}\" se ha descargado!",
            description="",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title="Un operador ha cargado una extensión:",
            description=f"El operador {ctx.author.mention} ha descargado el cog **{ctx.options.extension}**",
            colour=hikari.Colour(0xff6600),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del usuario: {ctx.author.id}",
            icon=ctx.author.avatar_url,
        )
        .set_thumbnail(ctx.author.avatar_url)
    )

    await channel.send(embed=embed)

@lightbulb.command("reload", "¡Recarga una extension!", auto_defer=True)
@lightbulb.implements(commands.SlashCommandGroup)
async def reload(ctx):
    embed =(
        hikari.Embed(
            title="¡Vaya! Esto es incomodo...",
            description="Este mensaje no deberia haber aparecido, por favor, reportalo.",
            colour=hikari.Colour(0xff0000),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)

@reload.child
@lightbulb.command("all", "¡Recarga todas las extensiones!", auto_defer=True)
@lightbulb.implements(commands.SlashSubCommand)
async def reload_all(ctx):
    if ctx.author.id not in bot_operators:

        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `BOT_OPERATOR`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    try:
        lista_cogs = [i[:-3] for i in os.listdir('./cogs') if i.endswith('.py')]
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.reload_extensions(f"cogs.{filename[:-3]}")
    except Exception as err:
        embed = (
            hikari.Embed(
                title="¡Ha ocurrido un error!",
                description=err,
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡Todos los cogs han sido recargados!{Style.RESET_ALL}')

    embed = (
        hikari.Embed(
            title=f"¡Todas las extensiones han sido recargadas!",
            description="",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title="Un operador ha recargado todas las extensiones",
            description=f"El operador {ctx.author.mention} ha recargado todas las extensiones",
            colour=hikari.Colour(0xff6600),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del usuario: {ctx.author.id}",
            icon=ctx.author.avatar_url,
        )
        .set_thumbnail(ctx.author.avatar_url)
    )

    await channel.send(embed=embed)

@reload.child
@lightbulb.option("extension", "¡Selecciona la extensión a recargar!", choices=lista_cogs)
@lightbulb.command("one", "¡Recarga una extensión!", auto_defer=True)
@lightbulb.implements(commands.SlashSubCommand)
async def reload_one(ctx):
    if ctx.author.id not in bot_operators:

        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `BOT_OPERATOR`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    try:
        lista_cogs = [i[:-3] for i in os.listdir('./cogs') if i.endswith('.py')]
        bot.reload_extensions(f"cogs.{ctx.options.extension}")
    except Exception as err:
        embed = (
            hikari.Embed(
                title="¡Ha ocurrido un error!",
                description=err,
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El cog \"{ctx.options.extension}\" se ha recargado!{Style.RESET_ALL}')

    embed = (
        hikari.Embed(
            title=f"¡El cog \"{ctx.options.extension}\" se ha recargado!",
            description="",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title="Un operador ha recargado una extensión:",
            description=f"El operador {ctx.author.mention} ha recargado el cog **{ctx.options.extension}**",
            colour=hikari.Colour(0xff6600),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del usuario: {ctx.author.id}",
            icon=ctx.author.avatar_url,
        )
        .set_thumbnail(ctx.author.avatar_url)
    )

    await channel.send(embed=embed)

bot.command(reload)