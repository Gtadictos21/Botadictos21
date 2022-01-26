from bot import bot
import os

# Si el archivo NO se encuentra importado, encendemos el bot. Si el OS no es Windows, utiliza uvloop para asyncio.
if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()
    bot.run()