# ![Bot-logo](https://user-images.githubusercontent.com/83682754/142743615-fbe1fc17-3015-4b1f-974b-34eb35e67a67.png) Botadictos21 (Beta Testing):

### Bot creado por [Gtadictos21](https://github.com/Gtadictos21) y [Galo](https://github.com/Galo223344) para el servidor de Discord: [El Club De Los 21's](https://gtadictos21.com/discord)

Estado del proyecto: [En desarollo](https://discord.gg/XEVxMVWHTE) - Fecha final estipulada: Febrero 2022

Este bot se beneficia de [Hikari](https://www.hikari-py.dev/) y [Lightbulb](https://hikari-lightbulb.readthedocs.io/en/latest/), dos librerias que se encuentran en constante crecimiento.

## Instalar dependencias:
¡Este bot requiere [Python versión: 3.9.x](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu), y pip!

```bash
$ pip install -r requirements.txt
```

**Ademas, es necesario contar con una base de datos MongoDB para poder utilizar muchas de las funciones del bot. Puedes obtener una base de datos gratuita [aquí](https://www.mongodb.com/es/cloud/atlas/register).**

## Iniciar el bot:

```bash
$ python3 -OO -m main

# El parametro -OO optimiza el inicio del bot
```

## Configuraciones:

1. Abrir archivo **"config.json"** y agregar el token de Discord, el ID de la guild, los IDs de los canales y opcionalmente, una API key de [HetrixTools](https://hetrixtools.com/).
3. Cambiar los emojis customizados por los tuyos o unos no customizados en los cogs.
4. Agregar tu propia clave API de youtube en **YTconfig.yml** (Las instrucciónes para conseguír esta clave están en el [repositorio original](https://github.com/Amethyst93/Discord-YouTube-Notifier), o simplemente podés borrar todo lo relacionado a YouTube.)
5. Utilizando los comandos "/sugchannel", "/logchannel", "/gvchannel" e "/init" deberás configurar tu servidor.

## Próximos cambios:
- [x] ~~Añadir MongoDB (Base de datos principal)~~
- [ ] Añadir mas cogs (Misc, Spam, Moderación, YT, Levels, Reminder, Welcome, Reacción, Temp, Logs)
- [ ] Añadir funciones extras
- [ ] Añadir Dockerfile y Docker-Compose.yml para poder dockerizar el bot
- [ ] Crear un dashboard web para revisar los niveles (PHP, HTML & CSS)
- Y mas...

## Créditos:

* Youtube cog sacado de este [repositorio de GitHub](https://github.com/Amethyst93/Discord-YouTube-Notifier) y modificado por mi mismo (Convertido a cog, arreglo de bugs y otros cambios varios)

* Levels cog sacado de este [hilo de Stackoverflow](https://stackoverflow.com/questions/62042331/how-to-create-a-leveling-system-with-discord-py-with-python) (La cantidad de experiencia dada fue modificada, y se realizaron otros cambios varios)

* Ranking cog sacado de este [hilo de Stackoverflow](https://stackoverflow.com/questions/61996040/discord-py-rank-command) (Arreglo de bugs y estilizado)

* Muchas gracias a la comunidad de Hikari por resolver nuestras dudas :)

## Aviso:

**Eres libre de copiar, modificar y hacer lo que quieras con este código, siempre y cuando, no sea malicioso.**

_Ultima actualización: 21/11/2021 por: Julián M. (Gtadictos21)_
