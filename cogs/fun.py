import hikari
import lightbulb
import random
import asyncio

from lightbulb import commands

plugin = lightbulb.Plugin("Misc")

# pitos = ["8=D", "8==D", "8===D", "8====D", "8=====D", "8======D", "8=======D", "8============D"]
respuestas = ["Si", "No", "Quizás", "Pregunta mas tarde", "Oops! Mi CPU se calentó demasiado", "Se amable la proxima vez", "No lo sé", "Utiliza `/nopruebesestecomando` y averigualo", "Preguntale a <@388924384016072706>", "Creo que no te gustará la respuesta..."]

@lightbulb.command("fun", "¡Este comando es divertido!", auto_defer=True)
@lightbulb.implements(commands.SlashCommandGroup)
async def fun(ctx):
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

# BANANA COMMAND
@fun.child
@lightbulb.command("banana", "¿Cuanto mide tu banana?", auto_defer=True)
@lightbulb.implements(commands.SlashSubCommand)
async def fun_banana(ctx):
    random.seed(ctx.author.id)
    await ctx.respond(f"La banana de {ctx.author.mention} mide: `8{'='*random.randint(1,15)}D`")

# CHICAHOT COMMAND
@fun.child
@lightbulb.command("chicahot", "¿Estas caliente?")
@lightbulb.implements(commands.SlashSubCommand)
async def fun_chicahot(ctx):
    pensando = await ctx.respond(f"Buscando ubicación de {ctx.author.mention}...")
    await asyncio.sleep(random.randint(3, 6))
    pensando2 = await pensando.edit("[7.49%] Revisando las imagenes del satelite...")
    await asyncio.sleep(random.randint(3, 6))
    pensando3 = await pensando2.edit("[15.20%] No se han encontrado resultados...")
    await asyncio.sleep(random.randint(3, 6))
    pensando4 = await pensando3.edit("[26.46%] Revisando la base de datos...")
    await asyncio.sleep(random.randint(3, 6))
    pensando5 = await pensando4.edit("[33.91%] La base de datos solo contiene la ubicación de <@503739646895718401>")
    await asyncio.sleep(random.randint(3, 6))
    pensando6 = await pensando5.edit(f"[47.00%] Revisando en la carpeta 'Fotos de {ctx.author.mention}'...")
    await asyncio.sleep(random.randint(3, 6))
    pensando7 = await pensando6.edit("[54.00%] Buscando entre 250.000 archivos...")
    await asyncio.sleep(random.randint(3, 6))
    pensando8 = await pensando7.edit("[68.88%] ¡Vaya! No hay nada aquí tampoco....")
    await asyncio.sleep(random.randint(3, 6))
    pensando9 = await pensando8.edit(f"[79.04%] ¡Hackeando mensajes privados de {ctx.author.mention}...")
    await asyncio.sleep(random.randint(3, 6))
    pensando10 = await pensando9.edit(f"[84.98%] Accediendo a la webcam de {ctx.author.mention}...")
    await asyncio.sleep(random.randint(3, 6))
    pensando11 = await pensando10.edit(f"[97.73%] Interesante...")
    await asyncio.sleep(random.randint(3, 6))
    pensando12 = await pensando11.edit("[99.99%] ¡Encontré la chica mas caliente en todo internet!")
    await asyncio.sleep(random.randint(3, 6))
    embed = (
        hikari.Embed(
            title="¡Aldo está caliente y está a 3 KM de tu casa!",
            description="No pierdas tiempo, ve a visitarlo",
            colour=hikari.Colour(0x3B9DFF),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail("./media/aldo.jpg")
    )
    await pensando12.edit(embed)

# 8 BALL COMMAND
@fun.child
@lightbulb.option("pregunta", "¡Escribe la pregunta que quieres hacerle!", hikari.OptionType.STRING,  modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("8ball", "¿No sabes la respuesta a alguna pregunta? ¡Preguntale al bot!", auto_defer=True)
@lightbulb.implements(commands.SlashSubCommand)
async def fun_magicball(ctx):
    embed = (
        hikari.Embed(
            title="La bola magica dice:",
            description="",
            colour=hikari.Colour(0x3B9DFF),
        )
        .add_field(
            name="Pregunta:",
            value=f"\"{ctx.options.pregunta}\"",
            inline=False,
        )
        .add_field(
            name="Respuesta:",
            value=f"\"{random.choice(respuestas)}\"",
            inline=False,
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )
    await ctx.respond(embed)

# LOLIS COMMAND
@fun.child
@lightbulb.command("lolis", "¿Quieres ver una foto de un loli?", auto_defer=True)
@lightbulb.implements(commands.SlashSubCommand)
async def fun_lolis(ctx):
    embed = (
        hikari.Embed(
            title="¡CONTENIDO PROHIBIDO!",
            description="¡Este contenido se encuentra bloqueado, y has sido automaticamente reportado a los administradores!",
            colour=hikari.Colour(0xff0000),
        )
        .set_footer(
            text=f"Pedido por: {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
    )
    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)

# NAVIDAD COMMAND
@fun.child
@lightbulb.command("navidad", "¿Cuantos dias quedan para que sea navidad?", auto_defer=True)
@lightbulb.implements(commands.SlashSubCommand)
async def fun_navidad(ctx):
    async with ctx.bot.d.aio_session.get("https://christmas-days.anvil.app/_/api/get_days") as res:
        data = await res.json()
        days = data['Days to Christmas']

        if days == 0:
            title = "¡Jo jo jo! Feliz navidad"
            description = "¡Hoy es navidad, ve y disfruta de este dia!"
            colour = 0xFF0000
        elif days == 1:
            title = "¡Un dia mas!"
            description = "¡Queda un dia para que sea navidad!"
            colour = 0x3B9DFF
        elif days == 2:
            title = "¡Dos dias para navidad!"
            description = "¡Quedan dos dias para que sea navidad!"
            colour = 0x3B9DFF
        else:
            title = "¡Aún no es navidad... pero falta poco!"
            description = f"Faltan {days} dias para que comience la navidad"
            colour = 0x3B9DFF
        
        embed = (
            hikari.Embed(
                title=title,
                description=description,
                colour=hikari.Colour(colour),
            )
            .set_footer(
                text=f"Pedido por: {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
        )

    await ctx.respond(embed)
    
plugin.command(fun)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)