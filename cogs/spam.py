import hikari
import lightbulb
import aioredis

from bot import bot_operators
from bot import logchannel

from colorama import Fore 
from colorama import Style
from tldextract import extract
from lightbulb import commands
from datetime import datetime, timedelta, timezone

plugin = lightbulb.Plugin("Spam")

# Conexión a DB Redis (Localhost)
redis_db = aioredis.from_url("redis://localhost", decode_responses=True)

# ADD COMMAND
@plugin.command
@lightbulb.option("url", "Selecciona la url a agregar", hikari.OptionType.STRING, modifier = commands.OptionModifier.CONSUME_REST)
@lightbulb.command("add", description="¡Añade links maliciosos a la lista negra!", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def link_add(ctx):

    # Verificamos si el usuario tiene permisos para ejecutar este comando
    if ctx.member.id not in bot_operators:
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

    # Separamos el protocolo (https://, http://, etc) y dejamos solo el dominio.
    tsd, td, tsu = extract(ctx.options.url) 
    url = td + '.' + tsu

    # Hacemos un fetch a la DB de Redis y revisamos si la URL ya se encuentra en la DB
    async with redis_db.client() as conn:
        spamlist = await conn.smembers("spamlinks")

        for spam in spamlist:
            # Si la URL no se encuentra en la DB, la agregamos
            if spam not in url:
        
                await conn.sadd("spamlinks", url)
                print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El link: \"{Fore.MAGENTA}{url}{Fore.WHITE}\" ha sido agregado a la lista de spam!{Style.RESET_ALL}')

                # Enviamos un mensaje al usuario para informarle que se agrego correctamente
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

                # Enviamos un mensaje al canal de logs
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
                return

            # Si la URL se encuentra en la DB, omitimos la accion, e informamos al usuario
            else:
        
                embed = (
                    hikari.Embed(
                        title="¡Este link ya se encuentra en la lista negra!",
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

@plugin.listener(hikari.MessageCreateEvent)
async def spam(event: hikari.MessageCreateEvent) -> None:

    # Revisamos si el autor es un operador
    if event.message.author.id == bot_operators:
        return
    
    # Revisamos si el autor es el propio bot
    if event.message.author.id == plugin.bot.get_me().id:
        return
    
    # Definimos el guild, el member y message a la vez que detectamos si el mensaje es un DM o no
    try:
        guild = event.get_guild()
        member = event.message.author.id
        message = event.message.content
    except:
        return

    # Procesamos el mensaje enviado
    mensaje_procesado2 = []
    mensaje_procesado = []
    mensaje_minus = message.lower()
    mensaje_procesado1 = mensaje_minus.split("/")
    for i in mensaje_procesado1:
        i = i.split(" ")
        mensaje_procesado2.append(i)

    for sublist in mensaje_procesado2:
        for item in sublist:
            mensaje_procesado.append(item.replace("|",""))
    
    # Revisamos si el mensaje contiene "discord.gg" y un invite
    if "discord.gg" in mensaje_procesado or ("discord.com" in mensaje_procesado and mensaje_procesado[mensaje_procesado.index("discord.com")+1] == "invite"):
        
        # Hacemos una lista con todos los codigos del servidor
        codigos = []
        invitaciones = await event.app.rest.fetch_guild_invites(event.guild_id)
        for i in invitaciones:
            i = i.code
            codigos.append(i.lower())

        # Comenzamos el checkeo de "discord.gg"
        if "discord.gg" in mensaje_procesado:
            # Si el siguiente item despues de "discord.gg" en la lista de mensaje_procesado está en la lista de codigos, lo ignoramos.
            if mensaje_procesado[mensaje_procesado.index("discord.gg")+1] in codigos:
                return
            # Hacemos una excepcion si el codigo es mi vanity url
            elif mensaje_procesado[mensaje_procesado.index("discord.gg")+1] == "gtadictos21":
                return
            else:
                # Si no lo está, significa que es una invitación de otro servidor, así que avisamos al usuario y eliminamos el mensaje.
                embed = (
                    hikari.Embed(
                        title="Por favor, evitá enviar invitaciones de otros servidores de Discord",
                        description="Hacer spam está prohibido, y puede llevar a un banneo.",
                        colour=hikari.Colour(0xff0000),
                    )
                    .set_footer(
                        text="Este es un mensaje automatico, si crees que se envió por error, reportalo.",
                        icon=event.app.get_me().avatar_url,
                    )
                )
                await event.author.send(embed)

                # Eliminamos el mensaje
                await event.message.delete()

                # Enviamos un mensaje al canal de logs
                channel = event.app.cache.get_guild_channel(logchannel)
                embed = (
                    hikari.Embed(
                        title=f"El usuario {event.author} trató de enviar una invitación a otro servidor:",
                        colour=hikari.Colour(0xff6600),
                        timestamp=datetime.now().astimezone(),
                    )
                    .add_field(
                        name="Mensaje original:",
                        value=f"\"{event.message.content}\"",
                        inline=False,
                    )
                    .set_footer(
                        text=f"ID del usuario: {event.author.id}",
                        icon=event.author.avatar_url,
                    )
                    .set_thumbnail(event.author.avatar_url)
                )

                await channel.send(embed)
                return

        # Comenzamos el checkeo de "discord.com"
        if "discord.com" in mensaje_procesado:
            # Si el siguiente item despues de "invite" en la lista de mensaje_procesado está en la lista de codigos, lo ignoramos.
            if mensaje_procesado[mensaje_procesado.index("invite")+1] in codigos:
                return
            else:
                # Si no lo está, significa que es una invitación de otro servidor, así que avisamos al usuario y eliminamos el mensaje.
                embed = (
                    hikari.Embed(
                        title="Por favor, evitá enviar invitaciones de otros servidores de Discord.",
                        description="Hacer spam está prohibido, y puede llevar a un banneo.",
                        colour=hikari.Colour(0xff0000),
                    )
                    .set_footer(
                        text="Este es un mensaje automatico, si crees que se envió por error, reportalo.",
                        icon=event.app.get_me().avatar_url,
                    )
                )
                await event.author.send(embed)

                # Eliminamos el mensaje
                await event.message.delete()

                # Enviamos un mensaje al canal de logs
                channel = event.app.cache.get_guild_channel(logchannel)
                embed = (
                    hikari.Embed(
                        title=f"El usuario {event.author} trató de enviar una invitación a otro servidor:",
                        colour=hikari.Colour(0xff6600),
                        timestamp=datetime.now().astimezone(),
                    )
                    .add_field(
                        name="Mensaje original:",
                        value=f"\"{event.message.content}\"",
                        inline=False,
                    )
                    .set_footer(
                        text=f"ID del usuario: {event.author.id}",
                        icon=event.author.avatar_url,
                    )
                    .set_thumbnail(event.author.avatar_url)
                )

                await channel.send(embed)
                return

    # Hacemos un fetch a la DB de Redis y revisamos si el mensaje contiene un link que se encuentra en la spamlist
    async with redis_db.client() as conn:
        spamlist = await conn.smembers("spamlinks")
        # Convertimos el mensaje_procesado en un string
        mensaje_procesado = ' '.join([str(elem) for elem in mensaje_procesado])
        for spam in spamlist:
            if spam in mensaje_procesado:

                # Si el mensaje contiene un link, eliminamos el mensaje y silenciamos al usuario por 28 dias.
                await event.message.delete()
                tiempo = (datetime.now(timezone.utc) + timedelta(seconds=2419200)).isoformat()
                await event.app.rest.edit_member(guild=guild, user=member, communication_disabled_until=tiempo, reason=f"Spam | Silenciado por: Acción automatica")

                embed = (
                    hikari.Embed(
                        title=f"El link que acabas de enviar ({spam}) está prohibido. Por favor, comunicate con los administradores para ser desilenciado.",
                        description="Para comunicarte con los administradores, enviales un mensaje por privado.",
                        colour=hikari.Colour(0xff0000),
                    )
                    .set_footer(
                        text="Este es un mensaje automatico, si crees que se envió por error, reportalo.",
                        icon=event.app.get_me().avatar_url,
                    )
                )
                await event.author.send(embed)

                # Enviamos un mensaje al canal de logs
                channel = event.app.cache.get_guild_channel(logchannel)
                embed = (
                    hikari.Embed(
                        title=f"El usuario {event.author} envió un link engañoso y fue muteado automaticamente:",
                        colour=hikari.Colour(0xff6600),
                        timestamp=datetime.now().astimezone(),
                    )
                    .add_field(
                        name="Mensaje original:",
                        value=f"\"{event.message.content}\"",
                        inline=False,
                    )
                    .set_footer(
                        text=f"ID del usuario: {event.author.id}",
                        icon=event.author.avatar_url,
                    )
                    .set_thumbnail(event.author.avatar_url)
                )

                await channel.send(embed)
                return

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)