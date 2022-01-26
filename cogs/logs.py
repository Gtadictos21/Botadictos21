import hikari
import lightbulb

from bot import logchannel

from datetime import datetime

plugin = lightbulb.Plugin("Logs")

ignorelist = []

# EVENTO ELIMINAR MENSAJE
@plugin.listener(hikari.GuildMessageDeleteEvent)
async def on_message_delete(event: hikari.GuildMessageDeleteEvent) -> None:

    # Obtenemos el canal de logs
    channel = event.app.cache.get_guild_channel(logchannel)

    # Obtenemos el mensaje eliminado
    message = event.old_message

    # Puede que el mensaje no se encuentre en el caché, y si no se encuentra, modificamos el embed de otra manera dará error
    if message == None:

        embed = (
            hikari.Embed(
                title=f"Se eliminó un mensaje que no se encuentra en el cache del bot",
                colour=hikari.Colour(0xff0000),
                timestamp=datetime.now().astimezone(),
            )
            .add_field(
                name="Mensaje eliminado:",
                value="\"Desconocido\"",
                inline=False,
            )
        )

        await channel.send(embed)
        return
    
    # Verificamos si el autor es un bot
    if message.author.is_bot:
        return
    
    # Verificamos si el canal está en la lista de ignorados
    if message.channel_id in ignorelist:
        return

    # Obtenemos el canal en el cual se elimino el mensaje
    message_channel = event.app.cache.get_guild_channel(message.channel_id)

    embed = (
        hikari.Embed(
            title=f"El usuario {message.author.username} eliminó un mensaje en #{message_channel}",
            colour=hikari.Colour(0xff0000),
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            name="Mensaje eliminado:",
            value=f"\"{message.content}\"",
            inline=False,
        )
        .set_footer(
            text=f"ID del usuario: {message.author.id}",
            icon=message.author.avatar_url,
        )
        .set_thumbnail(message.author.avatar_url)
    )

    await channel.send(embed)

# EVENTO EDITAR MENSAJE
@plugin.listener(hikari.GuildMessageUpdateEvent)
async def on_message_edit(event: hikari.GuildMessageUpdateEvent) -> None:

    # Obtenemos el canal de logs
    channel = event.app.cache.get_guild_channel(logchannel)

    # Obtenemos el mensaje eliminado
    old_message = event.old_message

    # Obtenemos el nuevo mensaje
    new_message = event.message

    # Verificamos si el autor es un bot
    if event.message.author.is_bot:
        return
    
    # Verificamos si el canal está en la lista de ignorados
    if new_message.channel_id in ignorelist:
        return

    # Puede que el mensaje no se encuentre en el caché, y si no se encuentra, modificamos el embed de otra manera dará error
    if old_message == None:

        link = f'https://discord.com/channels/{event.get_guild().id}/{new_message.channel_id}/{event.message.id}'
        
        # Enviamos un embed sin el mensaje anterior
        embed = (
            hikari.Embed(
                title=f"El usuario {new_message.author.username} editó un mensaje, has click para ir al mensaje",
                url=link,
                colour=hikari.Colour(0xffff00),
                timestamp=datetime.now().astimezone(),
            )
            .add_field(
                name="Mensaje original:",
                value=f"\"Desconocido\"",
                inline=False,
            )
            .add_field(
                name="Nuevo mensaje:",
                value=f"\"{new_message.content}\"",
                inline=False,
            )
            .set_thumbnail(new_message.author.avatar_url)
        )

        await channel.send(embed)
        return

    # Obtenemos el canal en el cual se elimino el mensaje
    message_channel = event.app.cache.get_guild_channel(old_message.channel_id)
    
    link = f'https://discord.com/channels/{event.get_guild().id}/{old_message.channel_id}/{event.message.id}'

    # Enviamos un mensaje con todos los detalles
    embed = (
        hikari.Embed(
            title=f"El usuario {old_message.author.username} editó un mensaje, has click para ir al mensaje",
            url=link,
            colour=hikari.Colour(0xffff00),
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            name="Mensaje original:",
            value=f"\"{old_message.content}\"",
            inline=False,
        )
        .add_field(
            name="Nuevo mensaje:",
            value=f"\"{new_message.content}\"",
            inline=False,
        )
        .set_footer(
            text=f"ID del usuario: {old_message.author.id}",
            icon=old_message.author.avatar_url,
        )
        .set_thumbnail(old_message.author.avatar_url)
    )
    await channel.send(embed)

# EVENTO UNBAN MEMBER
@plugin.listener(hikari.BanDeleteEvent)
async def on_member_unban(event: hikari.BanDeleteEvent) -> None:

    channel = event.app.cache.get_guild_channel(logchannel)

    embed = (
        hikari.Embed(
            title=f"El usuario {event.user} ha sido desbaneado del servidor",
            colour=hikari.Colour(0x2bff00),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del usuario: {event.user.id}",
            icon=event.user.avatar_url,
        )
        .set_thumbnail(event.user.avatar_url)
    )

    await channel.send(embed)

# EVENTO DELETE CHANNEL
@plugin.listener(hikari.GuildChannelDeleteEvent)
async def on_guild_channel_delete(event: hikari.GuildChannelDeleteEvent) -> None:

    channel = event.app.cache.get_guild_channel(logchannel)

    embed = (
        hikari.Embed(
            title=f"El canal \"#{event.channel}\" ha sido eliminado",
            colour=hikari.Colour(0xff0000),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del canal: {event.channel.id}",
            icon=event.get_guild().icon_url,
        )
    )

    await channel.send(embed)

# EVENTO CREATE CHANNEL
@plugin.listener(hikari.GuildChannelCreateEvent)
async def on_guild_channel_create(event: hikari.GuildChannelCreateEvent) -> None:

    channel = event.app.cache.get_guild_channel(logchannel)

    embed = (
        hikari.Embed(
            title=f"El canal \"#{event.channel}\" ha sido creado",
            colour=hikari.Colour(0x2bff00),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del canal: {event.channel.id}",
            icon=event.get_guild().icon_url,
        )
    )

    await channel.send(embed)

# EVENTO EDIT CHANNEL
@plugin.listener(hikari.GuildChannelUpdateEvent)
async def on_guild_channel_update(event: hikari.GuildChannelUpdateEvent) -> None:
    cambiadonombre = True
    cambiadoposicion = True
    cambiodeperms = True

    # Si el nombre del canal no cambió, cambiamos la variable a False
    if event.old_channel.name == event.channel.name:
        cambiadonombre = False

    # Si la posición del canal no cambió, cambiamos la variable a False
    if event.old_channel.position == event.channel.position:
        cambiadoposicion = False

    # Si las permisos del canal no cambiaron, cambiamos la variable a False
    if event.old_channel.permission_overwrites == event.channel.permission_overwrites:
        cambiodeperms = False
    
    channell = event.app.cache.get_guild_channel(logchannel)

    # Enviamos un mensaje con todos los detalles
    embed = hikari.Embed(
        title=f"Se ha editado el canal \"#{event.channel}\":", 
        colour=hikari.Colour(0xffff00),
        timestamp=datetime.now().astimezone(),
        )
    
    # Si la variable es True, enviamos el mensaje con el nombre del canal
    if cambiadonombre:
        embed.add_field(name= "Nombre anterior:" ,value=event.old_channel.name, inline=True)
        embed.add_field(name= "Nombre nuevo:" ,value=event.channel.name, inline=True)

    # Si la variable es True, enviamos el mensaje con la posición del canal
    if cambiadoposicion:
        embed.add_field(name= "Posición anterior:" ,value=event.old_channel.position+1, inline=True)
        embed.add_field(name= "Posición nueva:" ,value=event.channel.position+1, inline=True)
    
    # Si la variable es True, enviamos el mensaje con las permisos modificados del canal
    if cambiodeperms:
        for overwrite in event.channel.permission_overwrites.values():
            if overwrite.deny:
                embed.add_field(name="Permisos denegados:" ,value=f"Rol modificado: <@&{overwrite.id}> \nPermisos modificados: {overwrite.deny}", inline=False)
            
            if overwrite.allow:
                embed.add_field(name="Permisos aceptados:" ,value=f"Rol modificado: <@&{overwrite.id}> \nPermisos modificados: {overwrite.allow}", inline=False)

            if not overwrite.deny and not overwrite.allow:
                return

    if not cambiadoposicion and not cambiadonombre and not cambiodeperms:
        return

    embed.set_footer(
        text=f"ID del canal: {event.channel_id}",
        icon=event.get_guild().icon_url,
    )
    await channell.send(embed)

# EVENTO ROLE CREATE
@plugin.listener(hikari.RoleCreateEvent)
async def on_guild_role_create(event: hikari.RoleCreateEvent) -> None:
    channel = event.app.cache.get_guild_channel(logchannel)

    embed = (
        hikari.Embed(
            title=f"El rol \"{event.role}\" ha sido creado",
            colour=hikari.Colour(0xff0000),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del rol: {event.role.id}",
            icon=event.get_guild().icon_url,
        )
    )

    await channel.send(embed)

# EVENTO ROLE DELETE
@plugin.listener(hikari.RoleDeleteEvent)
async def on_guild_role_delete(event: hikari.RoleDeleteEvent) -> None:
    channel = event.app.cache.get_guild_channel(logchannel)

    embed = (
        hikari.Embed(
            title=f"El rol \"{event.role}\" ha sido eliminado",
            colour=hikari.Colour(0xff0000),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"ID del rol: {event.role.id}",
            icon=event.get_guild().icon_url,
        )
    )

    await channel.send(embed)

# EVENTO ROLE EDIT
@plugin.listener(hikari.RoleUpdateEvent)
async def on_guild_role_delete(event: hikari.RoleUpdateEvent) -> None:

    cambiadonombre = True
    cambiadoposicion = True
    cambiodeperms = True

    # Si el nombre del canal no cambió, cambiamos la variable a False
    if event.old_role.name == event.role.name:
        cambiadonombre = False

    # Si las permisos del rol no cambiaron, cambiamos la variable a False
    if event.old_role.permissions == event.role.permissions:
        cambiodeperms = False
    
    channell = event.app.cache.get_guild_channel(logchannel)

    # Enviamos un mensaje con todos los detalles
    embed = hikari.Embed(
        title=f"Se ha editado el rol \"{event.role}\":", 
        colour=hikari.Colour(0xffff00),
        timestamp=datetime.now().astimezone(),
        )
    
    # Si la variable es True, enviamos el mensaje con el nombre del rol
    if cambiadonombre:
        embed.add_field(name="Nombre anterior:" ,value=event.old_role.name, inline=True)
        embed.add_field(name="Nombre nuevo:" ,value=event.role.name, inline=True)
    
    # Si la variable es True, enviamos el mensaje con las permisos del rol
    if cambiodeperms:
        embed.add_field(name="Permisos modificados:" ,value=event.role.permissions, inline=False)
    
    if not cambiadoposicion and not cambiodeperms:
        return

    embed.set_footer(
        text=f"ID del rol: {event.role_id}",
        icon=event.app.cache.get_guild(event.guild_id).icon_url,
    )
    await channell.send(embed)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)