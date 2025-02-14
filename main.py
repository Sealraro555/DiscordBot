import discord
from discord.ext import commands
import os, random
import requests
import webserver

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'He iniciado sesión como {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def presentate(ctx):
    await ctx.send(f'Mucho gusto, me presento. Soy un bot de Discord de nombre, {bot.user}!')

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('pato')
async def pato(ctx):
    '''The duck command returns the photo of the duck'''
    print('hello')
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def animales(ctx):
    animales = os.listdir('animales')
    with open(f'animales/{random.choice(animales)}', 'rb') as f:
            picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def palomas(ctx):
    palomas = os.listdir('palomas')
    with open(f'palomas/{random.choice(palomas)}', 'rb') as f:
            picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def gorriones(ctx):
    gorriones = os.listdir('gorriones')
    with open(f'gorriones/{random.choice(gorriones)}', 'rb') as f:
            picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def pokemon(ctx,arg):
    try:
        pokemon = arg.split(" ",1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/"+pokemon)
        if result.text == "Not Found":
            await ctx.send("Creo que ese pokemon no existe :/")
        else:
            image_url = result.json()["sprites"]["front_default"]
            print(image_url)
            await ctx.send(image_url)
    except Exception as e:
        print("Error:", e)
@pokemon.error
async def error_type(ctx,error):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.send("Pero no me has mencionado ningun pokemon >:(")

@bot.command()
async def limpiar(ctx):
    await ctx.channel.purge()
    await ctx.send("He limpiado el chat de esos molestos mensajes", delete_after = 3)

@bot.command()
async def sumar(ctx, left: int, right: int):
    await ctx.send(left + right)
    print('En base a los números que me diste, he realizado esta suma')

@bot.command()
async def restar(ctx, left: int, right: int):
    await ctx.send(left - right)
    print('En base a los números que me diste, he realizado esta resta')

@bot.command()
async def multiplicar(ctx, left: int, right: int):
    await ctx.send(left * right)
    print('En base a los números que me diste, he realizado esta multiplicación')

@bot.command()
async def dividir(ctx, left: int, right: int):
    await ctx.send(left / right)
    print('En base a los números que me diste, he realizado esta división')

# Tablero de 3 en raya
board = [' ' for _ in range(9)]
current_player = 'X'

def print_board():
    return f"""
    {board[0]}      | {board[1]}    | {board[2]}
    ------------------------------------------------------
    {board[3]}      | {board[4]}    | {board[5]}
    ------------------------------------------------------
    {board[6]}      | {board[7]}    | {board[8]}
    """

def check_winner(player):
    win_conditions = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]],
    ]
    return [player, player, player] in win_conditions

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='tresenraya')
async def tresenraya(ctx):
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    await ctx.send(f'Juego de 3 en raya iniciado!\n{print_board()}')

@bot.command(name='colocar')
async def colocar(ctx, pos: int):
    global board, current_player
    if pos < 1 or pos > 9:
        await ctx.send('Posición inválida. Por favor elige un número entre 1 y 9.')
        return

    if board[pos - 1] == ' ':
        board[pos - 1] = current_player
        if check_winner(current_player):
            await ctx.send(f'Jugador {current_player} ha ganado!\n{print_board()}')
            board = [' ' for _ in range(9)]
        elif ' ' not in board:
            await ctx.send(f'Es un empate!\n{print_board()}')
            board = [' ' for _ in range(9)]
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            await ctx.send(f'{print_board()}\nTurno del jugador {current_player}')
    else:
        await ctx.send('Movimiento inválido, esa posición ya está ocupada.')

palabras = ["python", "discord", "programacion", "computadora", "juego"]

# Diccionario para almacenar el estado del juego por cada canal
juegos = {}

@bot.command()
async def ahorcado(ctx):
    """Inicia un juego del ahorcado."""
    if ctx.channel.id in juegos:
        await ctx.send("Ya hay un juego en curso en este canal. ¡Intenta adivinar!")
        return

    palabra_secreta = random.choice(palabras)
    letras_adivinadas = set()
    intentos_restantes = 6
    juegos[ctx.channel.id] = {
        "palabra": palabra_secreta,
        "letras": letras_adivinadas,
        "intentos": intentos_restantes
    }

    await ctx.send(f"¡Comienza el juego del ahorcado!\n{mostrar_palabra(palabra_secreta, letras_adivinadas)}\nIntentos restantes: {intentos_restantes}")

def mostrar_palabra(palabra, letras_adivinadas):
    """Muestra la palabra con las letras adivinadas y guiones bajos para las letras no adivinadas."""
    return " ".join([letra if letra in letras_adivinadas else "_" for letra in palabra])

@bot.command()
async def letra(ctx, letra: str):
    """Intenta adivinar una letra."""
    if ctx.channel.id not in juegos:
        await ctx.send("No hay ningún juego en curso en este canal. ¡Inicia uno con !ahorcado!")
        return

    juego = juegos[ctx.channel.id]
    palabra_secreta = juego["palabra"]
    letras_adivinadas = juego["letras"]
    intentos_restantes = juego["intentos"]

    if len(letra) != 1 or not letra.isalpha():
        await ctx.send("Por favor, introduce una sola letra válida.")
        return

    letra = letra.lower()

    if letra in letras_adivinadas:
        await ctx.send("Ya has intentado esa letra.")
        return

    letras_adivinadas.add(letra)

    if letra in palabra_secreta:
        await ctx.send(f"¡Correcto! La letra '{letra}' está en la palabra.")
    else:
        intentos_restantes -= 1
        await ctx.send(f"Incorrecto. La letra '{letra}' no está en la palabra. Intentos restantes: {intentos_restantes}")

    juego["letras"] = letras_adivinadas
    juego["intentos"] = intentos_restantes

    palabra_mostrada = mostrar_palabra(palabra_secreta, letras_adivinadas)
    await ctx.send(palabra_mostrada)

    if "_" not in palabra_mostrada:
        await ctx.send(f"¡Felicidades! Has adivinado la palabra: {palabra_secreta}")
        del juegos[ctx.channel.id]
        return

    if intentos_restantes <= 0:
        await ctx.send(f"¡Te has quedado sin intentos! La palabra era: {palabra_secreta}")
        del juegos[ctx.channel.id]
        return

@bot.command()
async def rendirse(ctx):
    """Termina el juego actual."""
    if ctx.channel.id not in juegos:
        await ctx.send("No hay ningún juego en curso en este canal.")
        return

    palabra_secreta = juegos[ctx.channel.id]["palabra"]
    await ctx.send(f"El juego ha terminado. La palabra era: {palabra_secreta}")
    del juegos[ctx.channel.id]

webserver.keep_alive()
bot.run(DISCORD_TOKEN)
