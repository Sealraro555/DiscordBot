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


webserver.keep_alive()
bot.run(DISCORD_TOKEN)