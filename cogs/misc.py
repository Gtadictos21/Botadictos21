import hikari
import lightbulb
import psutil
import math
import random
import re

from bot import bot_operators
from bot import logchannel
from bot import sugchannel
from bot import hetrix_token
from bot import partidas_channel

from uptime import uptime
from colorama import Fore 
from colorama import Style
from lightbulb import commands
from datetime import datetime, date
from hikari.impl import ActionRowBuilder

plugin = lightbulb.Plugin("Misc")

# PARTIDAS COMMAND
@plugin.command
@lightbulb.option("link", "Escribe el link de la partida, para que Gtadictos21 pueda revisarla", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.option("rango", "Escribe tu rango en el CS:GO", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.option("horas", "Escribe la cantidad de horas que tienes jugando al CS:GO", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("partidas", description="¿Quieres que Gtadictos21 analice una partida tuya? ¡Este es tu comando!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def partidas(ctx):

    # Checkeamos si el link es real
    list_servicios = ["https://youtube.com", "https://drive.google.com", "https://mediafire.com", "https://mega.nz", "https://mega.io", "https://cdn.discordapp.com"]
    link = ctx.options.link
    x = re.findall(r"(?=("+'|'.join(list_servicios)+r"))", link)
    if x == []:
        embed = (
            hikari.Embed(
                title="¡El link no es valido!",
                description="Recuerda que puedes utilizar los siguientes servicios para enviar tu partida: \n\n" + '\n'.join(list_servicios),
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    embed = (
        hikari.Embed(
            title="¡Muchas gracias por enviar tu partida!",
            description="Gtadictos21 analizará tu partida en el proximo video. Recuerda que aquellos que sean [miembros](https://gtadictos21.com/miembros), tienen prioridad.",
            colour=hikari.Colour(0x00ff00),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )
    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)

    channel = ctx.bot.cache.get_guild_channel(partidas_channel)
    embed = (
        hikari.Embed(
            title=f"¡El usuario {ctx.member.display_name} ha subido su partida!",
            colour=hikari.Colour(0xff6600),
        )
        .add_field(
            name="Link:", 
            value=link,
            inline=False,
        )
        .add_field(
            name="Rango actual:",
            value=ctx.options.rango,
            inline=True,
        )
        .add_field(
            name="Horas jugadas:",
            value=ctx.options.horas,
            inline=True,
        )
        .set_thumbnail(ctx.member.avatar_url)
    )

    await channel.send(embed)

# REDES COMMAND
@plugin.command
@lightbulb.command("redes", description="¡Visita el canal de YouTube de Gtadictos21!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def redes(ctx):
    embed = (
        hikari.Embed(
            title="Todas las redes sociales de Gtadictos21:",
            description="",
            colour=hikari.Colour(0x3B9DFF),
        )
        .add_field(
            name="YouTube:",
            value="Suscribete a mi canal: [YouTube](https://youtube.com/c/Gtadictos21)",
            inline=False,
        )
        .add_field(
            name="Twitter:",
            value="Sigueme en: [Twitter](https://twitter.com/Gtadictos21)",
            inline=False,
        )
        .add_field(
            name="Steam:",
            value="Agregame de amigo en: [Steam](https://steamcommunity.com/id/Gtadictos21/)",
            inline=False,
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

# MIEMBRO COMMAND
@plugin.command
@lightbulb.command("miembro", description="¿Eres miembro del canal? ¡Conecta tu cuenta!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def miembro(ctx):
    embed = (
        hikari.Embed(
            title="¿Eres miembro del canal? Así puedes obtener el rol correspondiente:",
            description="",
            colour=hikari.Colour(0x3B9DFF),
        )
        .add_field(name="Paso 1:", 
            value="[Vincula tu cuenta de YouTube con Discord](https://gtadictos21.com/conectar-youtube). Recuerda utilizar la cuenta de YouTube con la que has comprado la membresia.", 
            inline=False,
            )
        .add_field(name="Paso 2:",
            value="Luego de vincular tu cuenta de YouTube, automaticamente recibirás el rol correspondiente. Si esto no ocurre, contactate con los <@&750491866570686535>.",
            inline=False,
            )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

# STATUS COMMAND
@plugin.command
@lightbulb.command("status", description="¡Muestra el estado de los servicios!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def status(ctx):

    # Bot Musica
    async with ctx.bot.d.aio_session.get(f"https://api.hetrixtools.com/v1/{hetrix_token}/server/stats//") as res:
        data = await res.json()
        java = data['Services'][0]['Status']
        python = data['Services'][1]['Status']
        uptime_bot = data['SystemUptime']
        try:
            if python == 'online' and java == 'online':
                bot_status = ':green_circle:'
            else:
                bot_status = ':red_circle:'
        except:
            website_status = ':red_circle:'
            uptime_bot = 0
    
    # Website
    async with ctx.bot.d.aio_session.get(f"https://api.hetrixtools.com/v1/{hetrix_token}/server/stats//") as res:
        data = await res.json()
        try:
            nginx = data['Services'][0]['Status']
            apache = data['Services'][1]['Status']
            uptime_website = data['SystemUptime']

            if nginx == 'online' and apache == 'online':
                website_status = ':green_circle:'
            else:
                website_status = ':red_circle:'
        except:
            website_status = ':red_circle:'
            uptime_website = 0

        embed = (
            hikari.Embed(
                title="Estado de los servicios:",
                description="¡Puedes revisar mas haciendo [click aquí](https://status.gtadictos21.net)!",
                colour=hikari.Colour(0x3B9DFF),
            )
            .add_field(name="Estado del bot de musica:",
                value=f"{bot_status} (Uptime: {math.ceil(uptime_bot/3600)} horas)",
                inline=False,
                )
            .add_field(name="Estado de la website:",
                value=f"{website_status} (Uptime: {math.ceil(uptime_website/3600)} horas)",
                inline=False,
                )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed)

# INVITACION COMMAND
@plugin.command
@lightbulb.command("invitacion", description="¡Invita a un amigo al servidor!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def invitacion(ctx):
    embed = (
        hikari.Embed(
            title="Has click en el botón de abajo, o utiliza el siguiente link:",
            description="https://Gtadictos21.com/discord",
            colour=hikari.Colour(0x3B9DFF),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    row = ctx.bot.rest.build_action_row()
    await ctx.respond(embed, component=row.add_button(hikari.ButtonStyle.LINK, "https://Gtadictos21.com/discord").set_label("¡Haz click aquí!").add_to_container())

# HOST COMMAND
@plugin.command
@lightbulb.command("host", description="¿Quieres saber donde está hosteado el bot?", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def host(ctx):
    embed = (
        hikari.Embed(
            title="¡Sparked Host!",
            url="https://Gtadictos21.com/sparkedhost",
            description="Este bot se encuentra hosteado en los [VPS de Sparked Host](https://billing.sparkedhost.com/cart.php?a=confproduct&i=0), ubicados en Miami, Florida.",
            colour=hikari.Colour(0x3B9DFF),
        )
        .add_field(
            name="¿Quieres saber más?",
            value="¡Usá el código `Gtadictos21` y obtené un 15% de descuento!",
            inline=False,
        )
        .set_thumbnail("https://sparkedhost.com/src/svg/favicon.png")
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    row = ctx.bot.rest.build_action_row()
    await ctx.respond(embed, component=row.add_button(hikari.ButtonStyle.LINK, "https://Gtadictos21.com/sparkedhost").set_label("Sparked Host ⚡").add_to_container())

# NOPRUEBESESTECOMANDO COMMAND
@plugin.command
@lightbulb.command("nopruebesestecomando", description="¡No pruebes este comando!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def nopruebesestecomando(ctx):
    if ctx.author.id in bot_operators:
        embed = (
            hikari.Embed(
                title="¡Hey! No puedo hacer eso",
                description="",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    embed = (
        hikari.Embed(
            title="¡Has sido troleado!",
            description="Puedes unirte [presionando aquí](https://Gtadictos21.com/discord), o usando el botón de abajo.",
            colour=hikari.Colour(0x3B9DFF),
        )
        .set_footer(
            text="Este es un mensaje automatico, si crees que se envió por error, reportalo.",
            icon=ctx.bot.get_me().avatar_url,
        )
    )
    row = ctx.bot.rest.build_action_row()
    try:
        await ctx.author.send(embed, component=row.add_button(hikari.ButtonStyle.LINK, "https://Gtadictos21.com/discord").set_label("¡Haz click aquí!").add_to_container())
    
    except:
        print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El usuario {ctx.author} ha sido trolleado, pero no se le ha podido enviar un mensaje para que re-ingrese!{Style.RESET_ALL}')

    await ctx.bot.rest.kick_member(ctx.guild_id, ctx.author)

    await ctx.respond("https://tenor.com/view/troll-troll-face-ragememe-rageface-trolling-gif-4929853")

    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title="¡Alguien fue troleado, usó /nopruebesestecomando!",
            colour=hikari.Colour(0xff6600),
            timestamp=datetime.now().astimezone(),
        )
        .add_field(name="------",
            value=f"El usuario {ctx.author.mention} usó el comando: `/nopruebesestecomando`",
            inline=False,
        )
        .set_footer(
            text=f"ID del usuario: {ctx.author.id}",
            icon=ctx.author.avatar_url,
        )
        .set_thumbnail(ctx.author.avatar_url)
    )

    await channel.send(embed=embed)

# BOTINFO COMMAND
@plugin.command
@lightbulb.command("botinfo", description="¡Muestra información acerca del bot!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def botinfo(ctx):
    embed = (
        hikari.Embed(
            title="Haz click para ver el codigo fuente",
            url="https://gtadictos21.com/Botadictos21",
            description="",
            colour=hikari.Colour(0x3B9DFF),
        )
        .add_field(name="Botadictos21 por:",
            value="<@388924384016072706>", 
            inline=True,
        )
        .add_field(name="Musicadictos21 por:",
            value="<@503739646895718401>",
            inline=True,
        )
        .add_field(name="Para el servidor:",
            value="**El Club de los 21\'s**",
            inline=True,
        )
        .add_field(name="Hosteado en:",
            value="[Sparked Host](https://gtadictos21.com/sparkedhost)",
            inline=True,
        )
        .add_field(name="CPU:",
            value=f"{psutil.cpu_percent()}%",
            inline=True,
        )
        .add_field(name="RAM:",
            value=f"{math.ceil((psutil.virtual_memory()[3]/1024)/1024)} MB ({psutil.virtual_memory()[2]}%)",
            inline=True,
        )
        .add_field(name="Disco:",
            value=f"{round(math.ceil(((psutil.disk_usage('/')[1]/1024)/1024))/1024)}GB/{round(math.ceil(((psutil.disk_usage('/')[0]/1024)/1024))/1024)}GB  ({psutil.disk_usage('/')[3]}%)",
            inline=True,
        )
        .add_field(name="Uptime:",
            value=f"{math.ceil(uptime()/3600)} horas",
            inline=True,
        )
        .set_thumbnail(ctx.bot.get_me().avatar_url)
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )
    await ctx.respond(embed)

# MEMES COMMAND
@plugin.command
@lightbulb.option("subreddit", "Escoje un subreddit", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.command("memes", description="¡Diviertete viendo memes de Reddit!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def memes(ctx):
    if ctx.options.subreddit is None:
        listsubreddit= ["memessanos", "memes", "Divertido", "dankmemes", "me_irl", "CSGOmemes"]
        sub_reddit = random.choice(listsubreddit)
        async with ctx.bot.d.aio_session.get(f"https://meme-api.herokuapp.com/gimme/{sub_reddit}") as res:
            data = await res.json()
            try:
                titulo = data['title']
                autor = data['author']
                subreddit = data['subreddit']
                url = data['url']
                nsfw = data['nsfw']
                postlink = data['postLink']
            except:
                embed = (
                    hikari.Embed(
                        title="¡Este subreddit no existe, o no tiene memes!",
                        description=f"Subreddit solicitado: r/{sub_reddit}",
                        colour=hikari.Colour(0xff0000),
                    )
                    .set_footer(
                        text=f"Pedido por: {ctx.member.display_name}",
                        icon=ctx.member.avatar_url,
                    )
                )
                await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
                return
                
            if nsfw == True:
                embed = (
                    hikari.Embed(
                        title="¡El meme no es apto para todo publico!",
                        description=f"El meme está clasificado como NSFW, y no puede ser mostrado aquí. \n ¿Te crees valiente? Puedes ver el meme [aquí]({postlink}).",
                        colour=hikari.Colour(0xff0000),
                    )
                    .set_footer(
                        text=f"Pedido por: {ctx.member.display_name}",
                        icon=ctx.member.avatar_url,
                    )
                )
                await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
                return
                

            embed = (
                hikari.Embed(
                    title=f"{titulo}",
                    description=f"Publicado por {autor} en r/{subreddit}",
                    colour=hikari.Colour(0x3B9DFF),
                    url=postlink,
                )
                .set_image(url)
                .set_footer(
                    text=f"Pedido por: {ctx.member.display_name}",
                    icon=ctx.member.avatar_url,
                )
            )
            await ctx.respond(embed)
    else:
        async with ctx.bot.d.aio_session.get(f"https://meme-api.herokuapp.com/gimme/{ctx.options.subreddit}") as res:
            data = await res.json()
            try:
                titulo = data['title']
                autor = data['author']
                subreddit = data['subreddit']
                url = data['url']
                nsfw = data['nsfw']
                postlink = data['postLink']
            except:
                embed = (
                    hikari.Embed(
                        title="¡Este subreddit no existe, o no tiene memes!",
                        description=f"Subreddit solicitado: r/{ctx.options.subreddit}",
                        colour=hikari.Colour(0xff0000),
                    )
                    .set_footer(
                        text=f"Pedido por: {ctx.member.display_name}",
                        icon=ctx.member.avatar_url,
                    )
                )
                await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
                return

            if nsfw == True:
                embed = (
                    hikari.Embed(
                        title="¡El meme no es apto para todo publico!",
                        description=f"El meme está clasificado como NSFW, y no puede ser mostrado aquí. \n  ¿Te crees valiente? Puedes ver el meme [aquí]({postlink}).",
                        colour=hikari.Colour(0xff0000),
                    )
                    .set_footer(
                        text=f"Pedido por: {ctx.member.display_name}",
                        icon=ctx.member.avatar_url,
                    )
                )
                await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
                return

            embed = (
                hikari.Embed(
                    title=f"{titulo}",
                    description=f"Publicado por {autor} en r/{subreddit}",
                    colour=hikari.Colour(0x3B9DFF),
                    url=postlink,
                )
                .set_image(url)
                .set_footer(
                    text=f"Pedido por: {ctx.member.display_name}",
                    icon=ctx.member.avatar_url,
                )
            )
            await ctx.respond(embed)

# USERINFO COMMAND
@plugin.command
@lightbulb.option("usuario", "Seleciona a un usuario", hikari.OptionType.USER,  modifier=commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.command("userinfo", description="¡Revisa la información sobre un usuario!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def userinfo(ctx):
    target_id = int(ctx.options.usuario) if ctx.options.usuario is not None else ctx.user.id
    target = ctx.get_guild().get_member(target_id)

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]

    if target.is_bot == True:
        user_bot = "Sí"
    else:
        user_bot = "No"

    if target_id == 503739646895718401 or 388924384016072706:
        valor_1 = "¿Es mi creador?"
        valor_2 = "Sí"
    else:
        valor_1 = "¿Es un bot?"
        valor_2 = user_bot

    if not target:
        embed = (
            hikari.Embed(
                title="¡Usuario no encontrado!",
                description="",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    embed = (
        hikari.Embed(
            title=f"Información del usuario: {target.display_name}",
            description=f"ID: `{target.id}`",
            colour=hikari.Colour(0x3B9DFF),
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            name=valor_1, 
            value=valor_2, 
            inline=True,
        )
        .add_field(
            name="Cuenta creada en:",
            value=f"<t:{created_at}:d> (<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            name="Se unió al servidor en:",
            value=f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
            inline=True,
        )
        .add_field(
            name="Roles:",
            value=", ".join(r.mention for r in roles),
            inline=False,
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail(target.avatar_url)
            
    )

    await ctx.respond(embed)

# AVATAR COMMAND
@plugin.command
@lightbulb.option("usuario", "Seleciona a un usuario", hikari.OptionType.USER,  modifier=commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.command("avatar", description="¡Muestra tu avatar o el avatar de otro usuario!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def avatar(ctx):
    if ctx.options.usuario == None:
        avatar = ctx.author.avatar_url
    else:
        target_id = int(ctx.options.usuario) if ctx.options.usuario is not None else ctx.user.id
        target = ctx.get_guild().get_member(target_id)
        avatar = target.avatar_url
    

    embed = (
        hikari.Embed(
            colour=hikari.Colour(0x3B9DFF),
        )
        .set_image(avatar)
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

# SAY COMMAND
@plugin.command
@lightbulb.option("texto", "Escribe el texto que quieras", hikari.OptionType.STRING, modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.option("canal", "Seleciona el canal", hikari.OptionType.CHANNEL,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("say", description="¡Habla como si fueras el bot!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def say(ctx):
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

    if len(ctx.options.texto) > 256:
        embed = (
            hikari.Embed(
                title="¡Argumento invalido!",
                description="¡El texto no puede superar los 256 caracteres!",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    embed = (
        hikari.Embed(
            title=ctx.options.texto,
            description="",
            colour=hikari.Colour(0x3B9DFF),
        )
    )
    channel = ctx.get_guild().get_channel(ctx.options.canal)
    await channel.send(embed)

    embed = (
        hikari.Embed(
            title="¡Texto enviado!",
            description="",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)

# SERVERINFO COMMAND
@plugin.command
@lightbulb.command("serverinfo", description="¡Muestra información del servidor!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def serverinfo(ctx):
    guild = ctx.get_guild()
    created_at = int(ctx.get_guild().created_at.timestamp())
    joined_at = int(ctx.get_guild().joined_at.timestamp())
    lista_bots = [member for member in ctx.bot.cache.get_members_view_for_guild(ctx.guild_id).values() if member.is_bot]
    text_channels = [channel for channel in ctx.bot.cache.get_guild_channels_view_for_guild(ctx.guild_id) if isinstance(channel, hikari.GuildTextChannel)]
    voice_channels = [channel for channel in ctx.bot.cache.get_guild_channels_view_for_guild(ctx.guild_id) if isinstance(channel, hikari.GuildVoiceChannel)]

    if ctx.get_guild().premium_tier != 1 or 2 or 3 or "TIER_1" or "TIER_2" or "TIER_3":
        premium = "0"
    else:
        premium = ctx.get_guild().premium_tier

    embed = (
        hikari.Embed(
            title=f"Información del servidor: {ctx.get_guild().name}",
            description=ctx.get_guild().description,
            colour=hikari.Colour(0x3B9DFF),
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            name="ID:",
            value=f"`{ctx.get_guild().id}`",
            inline=True,
        )
        .add_field(
            name="Dueño:",
            value=f"<@{guild.owner_id}>",
            inline=True,
        )
        .add_field(
            name="Creado en:",
            value=f"<t:{created_at}:d> (<t:{created_at}:R>)",
            inline=False,
        )
        .add_field(
            name="Miembros totales:",
            value=f"{ctx.get_guild().member_count} (Bots: {len(lista_bots)})",
            inline=True,
        )
        .add_field(
            name="Nivel de Boost:", 
            value=f"Nivel {premium} ({ctx.get_guild().premium_subscription_count} boost)", 
            inline=True,
        )
        .add_field(
            name="Canales:",
            value=f"{len(ctx.get_guild().get_channels())} (Texto: {len(text_channels)}, Voz: {len(voice_channels)})",
            inline=False,
        )
        .set_thumbnail(ctx.get_guild().icon_url)
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed)

# REGLAS COMMAND
@plugin.command
@lightbulb.option("canal", "Seleciona el canal", hikari.OptionType.CHANNEL,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("reglas", description="¡Muestra las reglas del servidor!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def reglas(ctx):
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

    embed = (
        hikari.Embed(
            title=f"Reglas del servidor: {ctx.get_guild().name}",
            description=ctx.get_guild().description,
            colour=hikari.Colour(0x3B9DFF),
        )
        .add_field(
            name="#1", 
            value="<a:Desaprobado:784983048508276787> **NO** insultar, discriminar o faltar el respeto entre los miembros/staff.", 
            inline=False ,  
        )
        .add_field(
            name="#2", 
            value="<a:Desaprobado:784983048508276787> **NO** se permiten nombres/fotos obscenas. Queda a discreción del staff decidir que se considera como obsceno.", 
            inline=False,
        )
        .add_field(
            name="#3", 
            value="<a:Desaprobado:784983048508276787> **NO** se permite el contenido +18/NSFW. Puede ser un meme cada tanto, pero no pongas una foto de tu prima.", 
            inline=False,
        )
        .add_field(
            name="#4", 
            value="<a:Desaprobado:784983048508276787> **NO** spammear otros discords ajenos a esta comunidad.", 
            inline=False,
        )
        .add_field(
            name="#5", 
            value="<a:Desaprobado:784983048508276787> **NO** spammear canales de YouTube/Twitch sin permiso.", 
            inline=False,
        )
        .add_field(
            name="#6", 
            value="<a:Desaprobado:784983048508276787> **NO** se permite **comprar o vender NADA**, ya sea una bicicleta, un falcon o, un kilito de merca. ", 
            inline=False
        )
        .add_field(
            name="#7", 
            value="<a:Desaprobado:784983048508276787> **NO** se permite hacer flood, es decir, mensajes que puedan interrumpir una conversación o molestar como, por ejemplo, enviar demasiados mensajes en muy poco tiempo.", 
            inline=False,
        )
        .add_field(
            name="#8", 
            value="<a:Desaprobado:784983048508276787> **NO** se permite hacer \"Name Boosting\", es decir, utilizar caracteres como `! & ?` para aparecer primero en las listas.", 
            inline=False,
        )
        .add_field(
            name="#9", 
            value="<a:Aprobado:784983108663246908> **USAR** los canales correspondientes, si vas a mandar un meme, mándalo a <#750496337916592199>, etc.", 
            inline=False,
        )
        .add_field(
            name="#10", 
            value="<a:Desaprobado:784983048508276787> Al entrar a un chat de voz, **NO GRITES NI SATURES EL MICROFONO**.", 
            inline=False,
        )
        .add_field(name="#11",
            value="<a:Alerta:784982996225884200> **SI USAS CHEATS/SCRIPTS, TE REGALAMOS UNAS VACACIONES PERMANENTES A UGANDA.**", 
            inline=False,
        )
        .add_field(
            name="#12", 
            value="<a:Aprobado:784983108663246908> Para conseguir el rango de <@&750492534857400321> tenes que hablar con un <@&750492134695764059> o en su defecto con un <@&750491866570686535>, ¡y sin problemas, te lo van a dar!", 
            inline=False,
        )
        .add_field(
            name="#13", 
            value="<a:Aprobado:784983108663246908> Ante cualquier duda o consulta, podes hablar con un <@&750492134695764059> o un <@&750491866570686535> y seguro te ayudan a solucionar el problema", 
            inline=False,
        )
        .add_field(
            name="Recuerda:", 
            value="<a:Aprobado:784983108663246908> Este servidor se guia por los [Términos y Condiciones de Discord](https://www.discord.com/terms) y por las [Directivas de la Comunidad](https://www.discord.com/guidelines).", 
            inline=False,
        )
        .set_footer(
            text="Nos reservamos el derecho de hacer cambios a las reglas y/o los Términos y condiciones en cualquier momento, sin previo aviso.", 
            icon=ctx.get_guild().icon_url,
        )
    )
    channel = ctx.get_guild().get_channel(ctx.options.canal)
    await channel.send(embed)

    embed = (
        hikari.Embed(
            title="Información sobre los baneos:",
            description="",
            colour=hikari.Colour(0x3B9DFF),
        )
        .add_field(
            name="¿Has sido baneado de este servidor de manera injusta? Puedes apelar aquí:", 
            value="Haz [click aquí](https://Gtadictos21.com/apelacion-ban) para rellenar el formulario de apelaciones.", 
            inline=False
        )
        .set_footer(
            text="Recuerda que nunca serás baneado si respetas nuestras reglas, así como los Términos y Condiciones de Discord.", 
            icon=ctx.get_guild().icon_url,
        )
    )

    await channel.send(embed)

    embed = (
        hikari.Embed(
            title="¡Las reglas han sido publicadas!",
            description=f"Las reglas fueron publicadas en <#{channel.id}>",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)

# SUGERENCIAS COMMAND
@plugin.command
@lightbulb.option("texto", "Escribe tu sugerencia aquí", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("sugerencia", description="¡Envia una sugerencia!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def sugerencia(ctx):

    if len(ctx.options.texto) > 4096:
        embed = (
            hikari.Embed(
                title="¡Argumento invalido!",
                description="¡El texto no puede superar los 4096 caracteres!",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    channel = ctx.bot.cache.get_guild_channel(sugchannel)

    embed = (
        hikari.Embed(
            title=f"El usuario {ctx.author} ha sugerido lo siguiente:",
            description=f"\"{ctx.options.texto}\"",
            colour=hikari.Colour(0x3B9DFF),
        )
        .add_field(
            name="¡Vota para aceptar/denegar la sugerencia!",
            value="Utiliza `✅` para aceptar o `❌` para denegar la sugerencia.",
            inline=False,
        )
        .set_footer(
            text=f"Enviado por: {ctx.author}",
            icon=ctx.author.avatar_url,
        )
        .set_thumbnail(ctx.author.avatar_url)
    )

    mnsj = await channel.send(embed)
    await mnsj.add_reaction("✅")
    await mnsj.add_reaction("❌")

    embed = (
        hikari.Embed(
            title="¡La Sugerencia fue enviada con exito!",
            description="",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Pedido por: {ctx.author}",
            icon=ctx.author.avatar_url,
        )
    )

    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)