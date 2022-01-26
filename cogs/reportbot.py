import hikari
import lightbulb
import math

from lightbulb import commands
from datetime import datetime, date
from bot import SteamToken
from bot import CyberusToken

plugin = lightbulb.Plugin("ReportBot")

# STEAMINFO COMMAND
@plugin.command
@lightbulb.option("link", "Escribe el link del perfil del jugador", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("steaminfo", description="Obtiene información sobre un usuario de Steam", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def id(ctx):

    # Checkeamos si el argumento es un link valido
    if ctx.options.link.endswith("/"):
        link = ctx.options.link[:-1]

    else:
        link = ctx.options.link

    if link.startswith("https://steamcommunity.com/profiles/"):
        id64 = link.split('/')[-1]

    elif link.startswith("https://steamcommunity.com/id/"):
        SteamCustomNick = link.split('/')[-1]

        # Obtenemos el ID64 del usuario
        try:
            async with ctx.bot.d.aio_session.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={SteamToken}&vanityurl={SteamCustomNick}") as res:
                data = await res.json()
                id64 = data['response']['steamid']
        except:
            embed = (
                hikari.Embed(
                    title="¡Argumento invalido!",
                    description="El usuario/ID no existe, revisa el link.",
                    colour=hikari.Colour(0xff0000),
                )
                .set_footer(
                    text=f"Pedido por: {ctx.member.display_name}",
                    icon=ctx.member.avatar_url,
                )
            )
            await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
            return

    else:
        embed = (
            hikari.Embed(
                title="¡Argumento invalido!",
                description="Debes introducir un link valido de Steam, como por ejemplo:\n\n `https://steamcommunity.com/id/Gtadictos21`\n\n`https://steamcommunity.com/profiles/76561198393982451`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    # Obtenemos el nombre, avatar, el estado y  fecha de creación de la cuenta del usuario
    async with ctx.bot.d.aio_session.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key={SteamToken}&steamids={id64}") as res:
        data = await res.json()
        NombreJugador = data['response']['players']['player'][0]['personaname']
        AvatarJugador = data['response']['players']['player'][0]['avatarfull']
        Visibilidad = data['response']['players']['player'][0]['communityvisibilitystate']

        if Visibilidad == 3:
            CuentaCreada = data['response']['players']['player'][0]['timecreated']

            # Obtenemos las horas jugadas al CS:GO
            try:
                async with ctx.bot.d.aio_session.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={SteamToken}&steamid={id64}") as res:
                    data = await res.json()
                    HorasJugadas = data['playerstats']['stats'][2]['value']
                    HorasJugadas = f"{round(math.ceil(HorasJugadas)/3600)} horas"
            except:
                HorasJugadas = "No disponible"
    
    # Obtenemos el estado de VAC ban del usuario
    async with ctx.bot.d.aio_session.get(f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={SteamToken}&steamids={id64}") as res:
        data = await res.json()
        VACBan = data['players'][0]['VACBanned']
        CommunityBanned = data['players'][0]['CommunityBanned']
        NumberOfVACBans = data['players'][0]['NumberOfVACBans']
    
    # Obtenemos los reportes de Steamrep.com
    async with ctx.bot.d.aio_session.get(f"http://steamrep.com/api/beta4/reputation/{id64}?json=1&extended=1") as res:
        data = await res.json()
        status = data['steamrep']['flags']['status']

        if status == "exists":
            status = data['steamrep']['reputation']['full']
            reportcount = data['steamrep']['stats']['unconfirmedreports']['reportcount']
            reportlink = data['steamrep']['stats']['unconfirmedreports']['reportlink']

            if status == "":
                status = "No tiene reputación"

        else:
            status = "No disponible"
            reportcount = "No disponible"

    if VACBan == True:
        VACBan = "Si"

    if CommunityBanned == True:
        CommunityBanned = "Si"
    
    if CommunityBanned == False:
        CommunityBanned = "No"
    
    if VACBan == False:
        VACBan = "No"
    
    if Visibilidad == 1:
        Visibilidad = "Privado"

        embed = (
            hikari.Embed(
                title=f"Información sobre: {NombreJugador}",
                description=f"ID64: `{id64}`",
                colour=hikari.Colour(0xff0000),
                url=ctx.options.link,
            )
            .add_field(
                name="Estado de perfil:",
                value=Visibilidad,
            )
            .add_field(
                name="Baneos:",
                value=f"VAC: {VACBan}\n Community Ban: {CommunityBanned}\n Cantidad de Vacs: {NumberOfVACBans}",
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
            .set_thumbnail(AvatarJugador)
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)

    elif Visibilidad == 3:
        Visibilidad = "Público"
    
        embed = (
            hikari.Embed(
                title=f"Información sobre: {NombreJugador}",
                description=f"ID64: `{id64}`",
                colour=hikari.Colour(0xff0000),
                url=ctx.options.link,
            )
            .add_field(
                name="Estado de perfil:",
                value=Visibilidad,
            )
            .add_field(
                name="Cuenta creada:",
                value=f"<t:{CuentaCreada}:d> (<t:{CuentaCreada}:R>)",
            )
            .add_field(
                name="Baneos:",
                value=f"VAC: {VACBan}\n Community Ban: {CommunityBanned}\n Cantidad de Vacs: {NumberOfVACBans}",
            )
            .add_field(
                name="Horas jugadas:",
                value=HorasJugadas,
            )
            .add_field(
                name="Reportes (Steamrep.com):",
                value=f"Reputación: {status}\n Cantidad de reportes: {reportcount} reportes\n [Link de reportes]({reportlink})",
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
            .set_thumbnail(AvatarJugador)
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)

# REPORT COMMAND
@plugin.command
@lightbulb.option("link", "Escribe el link del perfil del jugador a reportar", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("report", description="Reporta a un jugador que ha usado cualquier tipo de hack", auto_defer=True)
@lightbulb.implements(commands.SlashCommand)
async def report(ctx):

    # Checkeamos si el argumento es un link valido
    if ctx.options.link.endswith("/"):
        link = ctx.options.link[:-1]

    else:
        link = ctx.options.link

    if link.startswith("https://steamcommunity.com/profiles/"):
        id64 = link.split('/')[-1]

    elif link.startswith("https://steamcommunity.com/id/"):
        SteamCustomNick = link.split('/')[-1]

        # Obtenemos el ID64 del usuario
        try:
            async with ctx.bot.d.aio_session.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={SteamToken}&vanityurl={SteamCustomNick}") as res:
                data = await res.json()
                id64 = data['response']['steamid']
        except:
            embed = (
                hikari.Embed(
                    title="¡Argumento invalido!",
                    description="El usuario/ID no existe, revisa el link.",
                    colour=hikari.Colour(0xff0000),
                )
                .set_footer(
                    text=f"Pedido por: {ctx.member.display_name}",
                    icon=ctx.member.avatar_url,
                )
            )
            await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
            return


    else:
        embed = (
            hikari.Embed(
                title="¡Argumento invalido!",
                description="Debes introducir un link valido de Steam, como por ejemplo:\n\n `https://steamcommunity.com/id/Gtadictos21`\n\n`https://steamcommunity.com/profiles/76561198393982451`",
                colour=hikari.Colour(0xff0000),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    # Accedemos a la API de Cyberus.dev y reportamos al jugador
    async with ctx.bot.d.aio_session.get(f"https://api.cyberus.dev/steam/report?token={CyberusToken}&id={id64}") as res:
        data = await res.json()
        CodigoErrorAPI = res.status
        if data['status'] == "success":
            
            # Obtenemos la informacion del jugador
            async with ctx.bot.d.aio_session.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key={SteamToken}&steamids={id64}") as res:
                data = await res.json()
                NombreJugador = data['response']['players']['player'][0]['personaname']
                AvatarJugador = data['response']['players']['player'][0]['avatarfull']

                embed = (
                    hikari.Embed(
                        title=f"¡El jugador {NombreJugador} ha sido reportado!",
                        description=f"ID64: `{id64}`\n Cantidad de reportes enviados: 50 reportes\n [Link del perfil]({link})",
                        colour=hikari.Colour(0x00ff00),
                    )
                    .set_footer(
                        text=f"Pedido por: {ctx.member.display_name}",
                        icon=ctx.member.avatar_url,
                    )
                    .set_thumbnail(AvatarJugador)
                )
                await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        
        else:
            embed = (
                hikari.Embed(
                    title=f"¡Error {CodigoErrorAPI}!",
                    description="¡No ha sido posible conectar con la API!",
                    colour=hikari.Colour(0xff0000),
                )
                .set_footer(
                    text=f"Pedido por: {ctx.member.display_name}",
                    icon=ctx.member.avatar_url,
                )
            )
            await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
            return

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)