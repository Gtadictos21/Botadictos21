import hikari
import lightbulb
import json
import asyncio
import motor.motor_asyncio

from bot import MongoDB_URL
from bot import bot_operators
from bot import logchannel
from bot import guild_id

from colorama import Fore 
from colorama import Style
from lightbulb import commands
from datetime import datetime

plugin = lightbulb.Plugin("Spam")

@plugin.listener(hikari.MessageCreateEvent)
async def spam(event: hikari.MessageCreateEvent) -> None:

    # Revisamos si el autor es un operador
    if event.message.author.id in bot_operators:
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
        invitaciones = await event.app.rest.fetch_guild_invites(event.get_guild().id)
        for i in invitaciones:
            i = i.code
            codigos.append(i)

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
                        colour=hikari.Colour(0x3B9DFF),
                    )
                    .set_footer(
                        text="Este es un mensaje automatico, si crees que se envió por error, reportalo.",
                        icon=event.app.get_me().avatar_url,
                    )
                )
                await event.author.send(embed)
                await event.message.delete()

                channel = event.app.cache.get_guild_channel(logchannel)
                embed = (
                    hikari.Embed(
                        title=f"El usuario {event.author} trató de enviar una invitación a otro servidor:",
                        colour=hikari.Colour(0xff6600),
                        timestamp=datetime.now().astimezone(),
                    )
                    .add_field(name="Mensaje original:",
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
                await asyncio.sleep(15)
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
                        colour=hikari.Colour(0x3B9DFF),
                    )
                    .set_footer(
                        text="Este es un mensaje automatico, si crees que se envió por error, reportalo.",
                        icon=event.app.get_me().avatar_url,
                    )
                )
                await event.author.send(embed)
                await event.message.delete()

                channel = event.app.cache.get_guild_channel(logchannel)
                embed = (
                    hikari.Embed(
                        title=f"El usuario {event.author} trató de enviar una invitación a otro servidor:",
                        colour=hikari.Colour(0xff6600),
                        timestamp=datetime.now().astimezone(),
                    )
                    .add_field(name="Mensaje original:",
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
                await asyncio.sleep(15)
                return

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)