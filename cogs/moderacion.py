import hikari
import lightbulb
import random
import asyncio
import time

from bot import bot_operators
from bot import logchannel

from colorama import Fore 
from colorama import Style
from lightbulb import commands, errors
from hikari.impl import ActionRowBuilder
from datetime import datetime, timedelta, timezone

plugin = lightbulb.Plugin("Moderación")

# BAN COMMAND
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("razon", "Escribe una razón valida", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("usuario", "Seleciona a un usuario", hikari.OptionType.USER,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("ban", description="Bannea a un usuario del servidor.", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def ban(ctx):
    
    # Verificamos si el usuario seleccionado tiene permisos para ejecutar el comando
    if ctx.options.usuario.id == ctx.member.id:
        embed = (
            hikari.Embed(
                title="No puedes banearte a ti mismo.",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Verificamos si el usuario seleccionado es el propio bot
    if ctx.options.usuario.id == ctx.bot.get_me().id:
        embed = (
            hikari.Embed(
                title="¡No puedes banear al bot!",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Verificamos si el usuario seleccionado es un operador
    if ctx.options.usuario.id == bot_operators:
        embed = (
            hikari.Embed(
                title="¡No puedes banear a un operador!",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Especificamos la razón si el usuario no lo hizo
    if ctx.options.razon == None:
        reason = "La razón no ha sido especificada."
    else:
        reason = ctx.options.razon
    
    # Enviamos un mensaje al usuario baneado 
    embed = (
        hikari.Embed(
            title=f"¡Has sido baneado de {ctx.get_guild().name}!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
        )
        .set_footer(
            text=f"Baneado por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    member = ctx.options.usuario

    try:
        await member.send(embed)
    except:
        print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El usuario {member} ha sido baneado, pero no se le ha podido enviar un mensaje!{Style.RESET_ALL}')
    
    # Enviamos un mensaje al canal de logs
    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title=f"¡El usuario {member} ha sido baneado!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Baneado por: {ctx.member.display_name} | ID del usuario banneado: {member.id}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail(member.avatar_url)
    )

    await channel.send(embed=embed)

    # Enviamos un mensaje al canal en donde se ejecuto el comando
    embed = (
        hikari.Embed(
            title=f"¡El usuario {member} ha sido baneado!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
        )
        .set_footer(
            text=f"Baneado por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )
    await ctx.respond(embed)
    
    # Agregamos "Baneado por {ctx.member.display_name}" a la razón y ejecutamos el ban
    reason = reason + f" | Baneado por {ctx.member.display_name}"
    await ctx.bot.rest.ban_member(ctx.guild_id, member, reason=reason)

@ban.set_error_handler
async def handler_ban(event: lightbulb.CommandErrorEvent) -> bool:
    exc = event.exception.__cause__ or event.exception
    ctx = event.context

    # Si el usuario no tiene permiso para ejecutar el comando, retornamos el error
    if isinstance(exc, errors.MissingRequiredPermission):
        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `BAN_MEMBERS`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    return False

# KICK COMMAND
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option("razon", "Escribe una razón valida", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("usuario", "Seleciona a un usuario", hikari.OptionType.USER,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("kick", description="Expulsa a un usuario del servidor.", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def kick(ctx):

    # Verificamos si el usuario seleccionado tiene permisos para ejecutar el comando
    if ctx.options.usuario.id == ctx.member.id:
        embed = (
            hikari.Embed(
                title="No puedes expulsarte a ti mismo.",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Verificamos si el usuario seleccionado es el propio bot
    if ctx.options.usuario.id == ctx.bot.get_me().id:
        embed = (
            hikari.Embed(
                title="¡No puedes expulsar al bot!",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Verificamos si el usuario seleccionado es un operador
    if ctx.options.usuario.id == bot_operators:
        embed = (
            hikari.Embed(
                title="¡No puedes expulsar a un operador!",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Especificamos la razón si el usuario no lo hizo
    if ctx.options.razon == None:
        reason = "La razón no ha sido especificada."
    else:
        reason = ctx.options.razon
    
    # Enviamos un mensaje al usuario expulsado
    embed = (
        hikari.Embed(
            title=f"¡Has sido expulsado de {ctx.get_guild().name}!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
        )
        .set_footer(
            text=f"Expulsado por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    member = ctx.options.usuario

    try:
        await member.send(embed)
    except:
        print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El usuario {member} ha sido expulsado, pero no se le ha podido enviar un mensaje!{Style.RESET_ALL}')

    # Enviamos un mensaje al canal de logs
    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title=f"¡El usuario {member} ha sido expulsado!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Expulsado por: {ctx.member.display_name} | ID del usuario expulsado: {member.id}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail(member.avatar_url)
    )

    await channel.send(embed=embed)

    # Enviamos un mensaje al canal en donde se ejecuto el comando
    embed = (
        hikari.Embed(
            title=f"¡El usuario {member} ha sido expulsado!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
        )
        .set_footer(
            text=f"Expulsado por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )
    await ctx.respond(embed)

    # Agregamos "Expulsado por {ctx.member.display_name}" a la razón y ejecutamos la expulsion
    reason = reason + f" | Expulsado por {ctx.member.display_name}"
    await ctx.bot.rest.kick_member(ctx.guild_id, member, reason=reason)

@kick.set_error_handler
async def handler_kick(event: lightbulb.CommandErrorEvent) -> bool:
    exc = event.exception.__cause__ or event.exception
    ctx = event.context

    # Si el usuario no tiene permiso para ejecutar el comando, retornamos el error
    if isinstance(exc, errors.MissingRequiredPermission):
        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `KICK_MEMBERS`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    return False

# MUTE COMMAND
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))
@lightbulb.option("tiempo", "Selecciona el tiempo que quieres silenciar al usuario (EN SEGUNDOS)", hikari.OptionType.INTEGER,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.option("razon", "Escribe una razón valida", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST, required=False)
@lightbulb.option("usuario", "Seleciona a un usuario", hikari.OptionType.USER,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("mute", description="Silencia a un usuario", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def mute(ctx):
    
    # Verificamos si el usuario seleccionado tiene permisos para ejecutar el comando
    if ctx.options.usuario.id == ctx.member.id:
        embed = (
            hikari.Embed(
                title="No puedes silenciarte a ti mismo.",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Verificamos si el usuario seleccionado es el propio bot
    if ctx.options.usuario.id == ctx.bot.get_me().id:
        embed = (
            hikari.Embed(
                title="¡No puedes silenciar al bot!",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Verificamos si el usuario seleccionado es un operador
    if ctx.options.usuario.id == bot_operators:
        embed = (
            hikari.Embed(
                title="¡No puedes silenciar a un operador!",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Verificamos si el tiempo es valido. Debe ser entre 1 segundo, y 2419200 segundos (28 dias)
    if not 1 <= ctx.options.tiempo <= 2_419_200:
        embed = (
            hikari.Embed(
                title="El tiempo no es valido.",
                description="Por favor, selecciona un tiempo entre 1 segundo y 28 dias.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Especificamos la razón si el usuario no lo hizo
    if ctx.options.razon == None:
        reason = "La razón no ha sido especificada."
    else:
        reason = ctx.options.razon
    
    # Sumamos los segundos a la fecha actual, y la pasamos al formato ISO 8601
    tiempo = (datetime.now(timezone.utc) + timedelta(seconds=ctx.options.tiempo)).isoformat()
    dt = datetime.fromisoformat(tiempo)
    
    # Enviamos un mensaje al usuario silenciado
    embed = (
        hikari.Embed(
            title=f"¡Has sido silenciado de {ctx.get_guild().name}!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
        )
        .add_field(
            name="Serás desilenciado en:",
            value=f"<t:{int(dt.timestamp())}:R>",
            inline=False,
        )
        .set_footer(
            text=f"Silenciado por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    member = ctx.options.usuario

    try:
        await member.send(embed)
    except:
        print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El usuario {member} ha sido silenciado, pero no se le ha podido enviar un mensaje!{Style.RESET_ALL}')

    # Enviamos un mensaje al canal de logs
    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title=f"¡El usuario {member} ha sido silenciado!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            name="Tiempo:",
            value=f"<t:{int(dt.timestamp())}:R>",
            inline=False,
        )
        .set_footer(
            text=f"Silenciado por: {ctx.member.display_name} | ID del usuario silenciado: {member.id}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail(member.avatar_url)
    )

    await channel.send(embed=embed)

    # Enviamos un mensaje al canal en el que se ejecuto el comando
    embed = (
        hikari.Embed(
            title=f"¡El usuario {member} ha sido silenciado!",
            description=f"Razón: {reason}",
            colour=hikari.Colour(0xff0000),
        )
        .add_field(
            name="Tiempo:",
            value=f"<t:{int(dt.timestamp())}:R>",
            inline=False,
        )
        .set_footer(
            text=f"Silenciado por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )
    await ctx.respond(embed)

    # Agregamos "Silenciado por: {ctx.member.display_name}" a la razón, y ejecutamos el mute
    reason = reason + f" | Silenciado por: {ctx.member.display_name}"
    await member.edit(communication_disabled_until=tiempo, reason=reason)

@mute.set_error_handler
async def handler_mute(event: lightbulb.CommandErrorEvent) -> bool:
    exc = event.exception.__cause__ or event.exception
    ctx = event.context

    # Si el usuario no tiene permiso para ejecutar el comando, retornamos el error
    if isinstance(exc, errors.MissingRequiredPermission):
        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `MODERATE_MEMBERS`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    return False

# UNMUTE COMMAND
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))
@lightbulb.option("usuario", "Seleciona a un usuario", hikari.OptionType.USER,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("unmute", description="Desilencia a un usuario", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def unmute(ctx):
    
    # Verificamos si el usuario seleccionado tiene permisos para ejecutar el comando
    if ctx.options.usuario.id == ctx.member.id:
        embed = (
            hikari.Embed(
                title="No puedes desilenciarte a ti mismo.",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Verificamos si el usuario seleccionado es el propio bot
    if ctx.options.usuario.id == ctx.bot.get_me().id:
        embed = (
            hikari.Embed(
                title="¡No puedes desilenciar al bot!",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Verificamos si el usuario seleccionado es un operador
    if ctx.options.usuario.id == bot_operators:
        embed = (
            hikari.Embed(
                title="¡No puedes desilenciar a un operador!",
                description="Por favor, selecciona a un usuario valido.",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ) 
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Enviamos un mensaje al usuario desilenciado
    embed = (
        hikari.Embed(
            title=f"¡¡Has sido desilenciado de {ctx.get_guild().name}!",
            description="¡Ahora puedes hablar, e ingresar a los canales de voz!",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Desilenciado por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )

    member = ctx.options.usuario

    try:
        await member.send(embed)
    except:
        print(f'{Fore.RED}[BOT INFO]{Fore.WHITE}¡El usuario {member} ha sido desilenciado, pero no se le ha podido enviar un mensaje!{Style.RESET_ALL}')
    
    # Ejecutamos el unmute
    await member.edit(communication_disabled_until=None)

    # Enviamos un mensaje al canal de logs
    channel = ctx.bot.cache.get_guild_channel(logchannel)
    embed = (
        hikari.Embed(
            title=f"¡El usuario {member} ha sido desilenciado!",
            colour=hikari.Colour(0x2bff00),
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Desilenciado por: {ctx.member.display_name} | ID del usuario desilenciado: {member.id}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail(member.avatar_url)
    )

    await channel.send(embed=embed)

    # Enviamos un mensaje al canal en el que se ejecuto el comando
    embed = (
        hikari.Embed(
            title=f"¡El usuario {member} ha sido desilenciado!",
            colour=hikari.Colour(0x2bff00),
        )
        .set_footer(
            text=f"Desilenciado por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )
    await ctx.respond(embed)

@unmute.set_error_handler
async def handler_unmute(event: lightbulb.CommandErrorEvent) -> bool:
    exc = event.exception.__cause__ or event.exception
    ctx = event.context

    # Si el usuario no tiene permiso para ejecutar el comando, retornamos el error
    if isinstance(exc, errors.MissingRequiredPermission):
        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `MODERATE_MEMBERS`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    return False

# PURGE COMMAND
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.option("cantidad", "Escribe la cantidad de mensajes a eliminar", hikari.OptionType.INTEGER,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("purgar", description="Elimina una cantidad de mensajes del chat", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def purgar(ctx):
    
    # Verificamos si la cantidad de mensajes a eliminar es menor o igual a 0
    if ctx.options.cantidad <= 0:
        await ctx.respond("._.") # XD
        return

    # Por seguridad, limitamos la cantidad maxima de mensajes a 300 (No hay limite, pero eliminar mas de 300 mensajes es peligroso e innecesario)
    if ctx.options.cantidad >= 300:

        embed = (
            hikari.Embed(
                title="¡No puedes eliminar más de 300 mensajes!",
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
    
    # Si la cantidad de mensajes a eliminar es mayor a 50, le preguntamos al usuario si realmente quiere hacerlo.
    if ctx.options.cantidad >= 50:

        embed = (
            hikari.Embed(
                title=f"¿Estás seguro que quieres eliminar {ctx.options.cantidad} mensajes?",
                description="Haz click en el botón verde para confirmar, o en el botón rojo para cancelar.",
                colour=hikari.Colour(0x2bff00),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        # Creamos 2 botones, uno para confirmar y el otro para cancelar la acción
        row = ctx.bot.rest.build_action_row()
        row.add_button(hikari.ButtonStyle.SUCCESS, "confirmar").set_label("Confirmar").set_emoji("✅").add_to_container() # - Creating button
        row.add_button(hikari.ButtonStyle.DANGER, "cancelar").set_label("Cancelar").set_emoji("❌").add_to_container() # - Creating button

        # Enviamos el mensaje, junto con los botones
        aviso_warning = await ctx.respond(embed, component=row, flags=hikari.MessageFlag.EPHEMERAL) # - Sending message with the component
        
        # Esperamos a que el usuario haga click en un botón, si no hace click en 60 segundos, elimina el mensaje
        try:
            event = await ctx.bot.wait_for(hikari.InteractionCreateEvent, 60, lambda event: event.interaction.custom_id in ("confirmar", "cancelar")) # - Waiting for the reaction with that component
            
            # Si el usuario hizo click en el botón de confirmar, y el usuario es el mismo que ejecuto el comando, eliminamos los mensajes
            if event.interaction.custom_id == "confirmar" and event.interaction.user.id == ctx.member.id:
                
                # Intentamos eliminar los mensajes. Si falla, es porque tienen mas de 14 dias de antigüedad
                try:
                    # Hacemos un fetch de los mensajes, con el limite en la cantidad establecida, y los eliminamos.
                    delete = await ctx.app.rest.fetch_messages(ctx.get_channel()).limit(ctx.options.cantidad)
                    await ctx.app.rest.delete_messages(ctx.get_channel(), delete)

                    # Enviamos un mensaje al usuario para informarle que se eliminaron los mensajes correctamente
                    embed = (
                        hikari.Embed(
                            title=f"¡El usuario {ctx.member.display_name} mensajes!",
                            description=f"Se eliminaron {ctx.options.cantidad} mensajes en el canal <#{ctx.get_channel().id}>",
                            colour=hikari.Colour(0xff0000),
                        )
                        .set_footer(
                            text=f"Realizado por: {ctx.member.display_name}",
                            icon=ctx.member.avatar_url,
                        )
                    )
                    aviso = await ctx.respond(embed)

                    # Enviamos un mensaje al canal de logs
                    channel = ctx.bot.cache.get_guild_channel(logchannel)
                    embed = (
                        hikari.Embed(
                            title=f"¡El usuario {ctx.member.display_name} ha eliminado mensajes!",
                            description=f"Se eliminaron {ctx.options.cantidad} mensajes en el canal <#{ctx.get_channel().id}>",
                            colour=hikari.Colour(0xff0000),
                            timestamp=datetime.now().astimezone(),
                        )
                        .set_footer(
                            text=f"ID del usuario: {ctx.member.id}",
                            icon=ctx.member.avatar_url,
                        )
                        .set_thumbnail(ctx.member.avatar_url)
                    )

                    await channel.send(embed)
                    
                    # Esperamos 15 segundos, y eliminamos el mensaje
                    await asyncio.sleep(15)
                    await aviso.delete()
                
                # Enviamos un mensaje al usuario para informarle que no se pudo eliminar los mensajes
                except:
                    embed = (
                        hikari.Embed(
                            title="¡Ha ocurrido un error!",
                            description="No es posible eliminar mensajes que tienen mas de 14 dias de antigüedad",
                            colour=hikari.Colour(0xff0000),
                        )
                        .set_footer(
                            text=f"Pedido por: {ctx.member.display_name}",
                            icon=ctx.member.avatar_url,
                        )
                    )
                    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
                    return
            
            # Si el usuario hizo click en el botón de cancelar, eliminamos el mensaje de aviso
            if event.interaction.custom_id == "cancelar" and event.interaction.user.id == ctx.member.id:
                await aviso_warning.delete()
                return

        # Si no hizo click en ningún botón en 60 segundos, eliminamos el mensaje
        except asyncio.TimeoutError:
            await aviso_warning.delete()
            return
    
    # Si la cantidad es igual o menor a 50 mensajes, los eliminamos sin la confirmacion
    if ctx.options.cantidad <= 50:

        # Intentamos eliminar los mensajes. Si falla, es porque tienen mas de 14 dias de antigüedad
        try:

            # Hacemos un fetch de los mensajes, con el limite en la cantidad establecida, y los eliminamos.
            delete = await ctx.app.rest.fetch_messages(ctx.get_channel()).limit(ctx.options.cantidad)
            await ctx.app.rest.delete_messages(ctx.get_channel(), delete)

            embed = (
                hikari.Embed(
                    title=f"¡El usuario {ctx.member.display_name} mensajes!",
                    description=f"Se eliminaron {ctx.options.cantidad} mensajes en el canal <#{ctx.get_channel().id}>",
                    colour=hikari.Colour(0xff0000),
                )
                .set_footer(
                    text=f"Realizado por: {ctx.member.display_name}",
                    icon=ctx.member.avatar_url,
                )
            )
            aviso = await ctx.respond(embed)

            # Enviamos un mensaje al canal de logs
            channel = ctx.bot.cache.get_guild_channel(logchannel)
            embed = (
                hikari.Embed(
                    title=f"¡El usuario {ctx.member.display_name} ha eliminado mensajes!",
                    description=f"Se eliminaron {ctx.options.cantidad} mensajes en el canal <#{ctx.get_channel().id}>",
                    colour=hikari.Colour(0xff0000),
                    timestamp=datetime.now().astimezone(),
                )
                .set_footer(
                    text=f"ID del usuario: {ctx.member.id}",
                    icon=ctx.member.avatar_url,
                )
                .set_thumbnail(ctx.member.avatar_url)
            )

            await channel.send(embed)
            
            # Esperamos 15 segundos, y eliminamos el mensaje
            await asyncio.sleep(15)
            await aviso.delete()
        
        # Enviamos un mensaje al usuario para informarle que no se pudo eliminar los mensajes
        except:
            embed = (
                hikari.Embed(
                    title="¡Ha ocurrido un error!",
                    description="No es posible eliminar mensajes que tienen mas de 14 dias de antigüedad",
                    colour=hikari.Colour(0xff0000),
                )
                .set_footer(
                    text=f"Pedido por: {ctx.member.display_name}",
                    icon=ctx.member.avatar_url,
                )
            )
            await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
            return

@purgar.set_error_handler
async def handler_purgar(event: lightbulb.CommandErrorEvent) -> bool:
    exc = event.exception.__cause__ or event.exception
    ctx = event.context

    # Si el usuario no tiene permiso para ejecutar el comando, retornamos el error
    if isinstance(exc, errors.MissingRequiredPermission):
        embed = (
            hikari.Embed(
                title="¡No tienes permisos para utilizar este comando!",
                description="Necesitas contar con el permiso `MANAGE_GUILD`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    return False

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)