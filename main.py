import os
import string
from tokenize import Token
import discord
from discord.ext import commands
from dotenv.dotenv import LoadEnv
from youtube_search import YoutubeSearch
global Voice
global Queue 
import os


if __name__ == "__main__":
    LoadEnv()

    Voice = None
    Queue = []
    Current = None

    TOKEN = os.environ['TOKEN']
    GUILD = os.environ['GUILD']

    client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    def yt_download(url: str, name: str) -> str:
        cmd = f"/usr/bin/yt-dlp -f 140 -o ~/Documents/Python/audio-bot/audfiles/{name}.m4a {url}"
        os.system(command=cmd)
        return f"{name}.m4a"

    def yt_search(terms, max_results=1) -> str:
        print(terms)
        res = YoutubeSearch(terms, max_results=1).to_dict()
        print(res)
        return f"https://www.youtube.com{res[0]['url_suffix']}"

    def get_queue_top(name : str):
        global Queue
        global Current
        os.remove(os.getcwd() + "/" + name)
        if len(Queue) > 0:
            source = Queue[0]
            Queue = Queue[1:]
            player = Voice.play(source['s'])
        else:
            Current = None

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

    @client.command(pass_context = True)
    async def join(ctx):
        global Voice
        if ctx.author == client.user:
            return
        channel = ctx.author.voice.channel
        Voice = await channel.connect()
        await ctx.send("Joined!")

    @client.command(pass_context = True)
    async def add(ctx, *arg):
        url = yt_search(' '.join(arg))
        name = "audfiles/" + yt_download(url=url, name=''.join(arg))
        source = discord.FFmpegPCMAudio(name, executable='/usr/bin/ffmpeg')
        d = {'name' : name, 's': source}
        Queue.append(d)
        await ctx.send("Added!")

    @client.command(pass_context = True)
    async def play(ctx):
        global Queue
        global Voice
        global Current
        source = Queue[0]
        Queue = Queue[1:]
        Current = source
        player = Voice.play(source['s'], after=lambda x=None: get_queue_top(source['name']))
            

    @client.command(pass_context = True)
    async def pause(ctx):
        if Voice.is_playing():
            Voice.pause()
        else:
            await ctx.send("No SOng is playing")

    @client.command(pass_context = True)
    async def resume(ctx):
        if Voice.is_paused():
            Voice.resume()
        else:
            await ctx.send("No song is paused")

    @client.command(pass_context = True)
    async def stop(ctx):
        Voice.stop()

    @client.command(pass_context = True)
    async def search(ctx, *arg):
        term = ' '.join(arg)
        yt_search(term)

    client.run(TOKEN)