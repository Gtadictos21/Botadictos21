import aiohttp
import os
import math
import asyncio
import random
import json
import time
import pytz
import psutil
import hikari
import lightbulb

from colorama import Fore 
from colorama import Style
import motor.motor_asyncio
from lightbulb import commands, context
from tldextract import extract
from datetime import datetime

# Cargamos el archivo config.json
with open("config.json") as f:
    data = json.load(f)
    token = data["discord-token"] # Token de Discord
    MongoDB_URL = data["Mongodb"] # URL para conectarse a la base de datos de MongoDB
    guild_id = data["guild"] # ID de la guild
    statuschannel = data["statuschannel"] # ID del canal de status

    global bot_operators
    bot_operators = data["bot-operators"] # IDs de los operadores del bot (Acceso a cargar/descargar cogs y demas)

    global hetrix_token
    hetrix_token = data["hetrix-token"] # Token para la API de HetrixTools

    global sugchannel
    sugchannel = data["sugchannel"] # Canal de sugerencias

    global logchannel
    logchannel = data["logchannel"] # Canal de Logs

# Configuramos e iniciamos MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MongoDB_URL)
print(f'{Fore.RED}[MONGODB INFO]{Fore.CYAN}¡La base de datos se ha conectado!{Style.RESET_ALL}')
db = client['bot']
spamlist = db['spamlist']

# Zona horaria
tz = pytz.timezone('America/Argentina/Buenos_Aires')

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

# Cambios de status cada 10 segundos
@bot.listen()
async def on_bot_started(event: hikari.StartingEvent):
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
        async with bot.d.aio_session.get("https://christmas-days.anvil.app/_/api/get_days") as res:
            data = await res.json()
            days = data['Days to Christmas']
            await bot.update_presence(activity=hikari.Activity(type=hikari.ActivityType.WATCHING, name=f"a 🎅 ¡Solo {days} dias para navidad!"))
            await asyncio.sleep(10)

# Inicia el loop, e informa por la consola que el bot se encendio.
@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent)-> None:
    asyncio.create_task(on_bot_started(event))
    disco = psutil.disk_usage('/')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}¡{bot.get_me().username} se ha conectado!{Style.RESET_ALL}')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}El ID del bot es: {Fore.MAGENTA}{bot.get_me().id}{Style.RESET_ALL}')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}Bot creado por: {Fore.MAGENTA}Gtadictos21 {Fore.CYAN}&{Fore.MAGENTA} Galo223344{Style.RESET_ALL}')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}Repositorio oficial: {Fore.MAGENTA}https://github.com/galo223344/Botadictos21{Style.RESET_ALL}')
    print(f'{Fore.RED}[BOT INFO]{Fore.CYAN}ID de los operadores: {Fore.MAGENTA}{bot_operators}{Style.RESET_ALL}')
    print(f'{Fore.RED}[SERVER INFO]{Fore.CYAN}Uso de CPU: {Fore.MAGENTA}{psutil.cpu_percent()}%{Style.RESET_ALL}')
    print(f'{Fore.RED}[SERVER INFO]{Fore.CYAN}Uso de RAM: {Fore.MAGENTA}{math.ceil((psutil.virtual_memory()[3]/1024)/1024)}MB {Fore.CYAN}({Fore.MAGENTA}{psutil.virtual_memory()[2]}%{Fore.CYAN}){Style.RESET_ALL}')
    print(f'{Fore.RED}[SERVER INFO]{Fore.CYAN}Uso de disco: {Fore.MAGENTA}{round(math.ceil(((disco.used/1024)/1024))/1024)}GB{Fore.CYAN}/{Fore.MAGENTA}{round(math.ceil(((disco.total/1024)/1024))/1024)}GB {Fore.CYAN}({Fore.MAGENTA}{round(math.ceil(((disco.free/1024)/1024))/1024)}GB{Fore.CYAN}){Style.RESET_ALL}')
    print(f'{Fore.RED}[SERVER INFO]{Fore.CYAN}Ping: {Fore.MAGENTA}{round(bot.heartbeat_latency * 1000)}ms')

    start_time = time.time()
    message = await bot.cache.get_guild_channel(statuschannel).send("API ping")
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
@lightbulb.command("ping", description="¡Revisa la latencia del bot!")
@lightbulb.implements(commands.SlashCommand)
async def ping(ctx):
    start_time = time.time()
    message = await bot.cache.get_guild_channel(logchannel).send("API ping")
    end_time = time.time()
    await message.delete()

    embed = (
        hikari.Embed(
            color=hikari.Colour(0x3B9DFF),
        )
        .add_field(
            name="Bot ping:",
            value=f"{round(bot.heartbeat_latency * 1000)}ms",
            inline=False,
        )
        .add_field(
            name="API ping:",
            value=f"{round((end_time - start_time) * 1000)}ms",
            inline=False,
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

@bot.command
@lightbulb.option("link", "Selecciona el link a agregar", hikari.OptionType.STRING, modifier = commands.OptionModifier.CONSUME_REST)
@lightbulb.command("add", description="¡Añade links maliciosos a la lista negra!")
@lightbulb.implements(commands.SlashCommand)
async def add(ctx):
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

    tsd, td, tsu = extract(ctx.options.link) 
    url = td + '.' + tsu

    try:
        fecha = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")

        spamurl = {
        "_id": url,
        "autor": ctx.author.id,
        "fecha": fecha
        }

        await spamlist.insert_one(spamurl)
        print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El link: \"{Fore.MAGENTA}{url}{Fore.WHITE}\" ha sido agregado a la lista de spam!{Style.RESET_ALL}')
        
        embed = (
            hikari.Embed(
                title="¡El link fue agregado a la lista de spam!",
                description=f"Link agregado: \"{url}\"",
                colour=hikari.Colour(0x2bff00),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed)

        bot.reload_extensions("cogs.spam")
        print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El cog \"spam\" se ha recargado, ya que se ha utilizado el comando \"/add\"!{Style.RESET_ALL}')

        channel = ctx.bot.cache.get_guild_channel(logchannel)
        embed = (
            hikari.Embed(
                title=f"¡El administrador {ctx.author.username} agregó un nuevo link a la lista de spam:",
                description = f"Link agregado: \"{url}\"",
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
    
    except:
        encontrado = spamlist.find({},{'_id': url, 'autor': 1, 'fecha': 1, })
        for data in await encontrado.to_list(length=100):
            x = json.dumps(data)
            y = json.loads(x)
            author = y["autor"]
            date = y["fecha"]
        
        embed = (
            hikari.Embed(
                title="¡Este link ya se encuentra en la lista negra!",
                description=f"El administrador <@{author}> agregó el link el dia: {date}",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

############################################
#
#
# COGS
#
#
############################################

@bot.command
@lightbulb.option("extension", "¡Selecciona la extension a cargar!", hikari.OptionType.STRING, modifier = commands.OptionModifier.CONSUME_REST)
@lightbulb.command("load", description="¡Carga una extension!")
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
@lightbulb.option("extension", "¡Selecciona la extension a cargar!", hikari.OptionType.STRING, modifier = commands.OptionModifier.CONSUME_REST)
@lightbulb.command("unload", description="¡Descarga una extension!")
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

@bot.command
@lightbulb.option("all", "¡Recarga todas las extensiones!", hikari.OptionType.STRING, modifier = commands.OptionModifier.CONSUME_REST, choices=["all"], required = False)
@lightbulb.option("extension", "¡Selecciona la extension a recargar!", hikari.OptionType.STRING, modifier = commands.OptionModifier.CONSUME_REST, required = False)
@lightbulb.command("reload", description="¡Recarga una extension!")
@lightbulb.implements(commands.SlashCommand)
async def reload(ctx):
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
    
    if ctx.options.extension == None and ctx.options.all == None:

        embed = (
            hikari.Embed(
                title="¡Argumento invalido!",
                description="Debes especificar la extensión que deseas recargar",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    if ctx.options.all:

        try:
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
    
    else:
        try:
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