from aiohttp import web
from discord.ext import commands, tasks
import os
import aiohttp
import pickle
import asyncio

app = web.Application()
routes = web.RouteTableDef()

def setup(bot):
    bot.add_cog(Webserver(bot))

class Webserver(commands.Cog):
    def __init__(self, bot):
        self.labs = {}
        self.mins = []
        self.bot = bot
        self.web_server.start()
        self.pull_labs.start()

        try:
            labt = pickle.load( open( "./persistence/labs.p", "rb" ) )
            self.labs = labt[0]
            self.mins = labt[1]
            print("Labs successfully loaded.")
        except:
            print("No labs to load")

        @routes.post('/curtin_lab_ingest')
        async def cli_post(request):
            data = await request.json()
            mini = 1000
            for room in [218,219,220,221,232]:
                for row in range(1,7):
                    for column in "abcd":
                        for row in range(1,7):
                            host = "lab{}-{}0{}.cs.curtin.edu.au.".format(room,column,row)
                            users = -1 #Get users for this host
                            self.labs[host] = users
                            if (users>-1 and users < mini):
                                mini = users
                                mins = []
                            if (users == mini):
                                mins.append(host)
            self.mins = mins
            max = -1
            for lab in sorted(self.labs,key=self.labs.get):
                if self.labs[lab] > max:
                    max = self.labs[lab]
            if max != -1:
                print("Saving up machines to file", flush=True)
                pickle.dump( (self.labs,self.mins), open ("./persistence/labs.p", "wb" ) )
            if self.bot:
                if self.bot.eloop:
                    self.bot.eloop.create_task(self.bot.updatePMsg())
            return 200

        self.webserver_port = os.environ.get('PORT', 8010)
        app.add_routes(routes)
    
    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host='0.0.0.0', port=self.webserver_port)
        await site.start()
    
    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=60)
    async def pull_labs(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://35.189.5.47/machineList.txt') as resp:
                data = await resp.text()
                print(data)
                return
                mini = 1000
                for room in [218,219,220,221,232]:
                    for row in range(1,7):
                        for column in "abcd":
                            for row in range(1,7):
                                host = "lab{}-{}0{}.cs.curtin.edu.au.".format(room,column,row)
                                users = -1 #Get users for this host
                                self.labs[host] = users
                                if (users>-1 and users < mini):
                                    mini = users
                                    mins = []
                                if (users == mini):
                                    mins.append(host)
                self.mins = mins
                max = -1
                for lab in sorted(self.labs,key=self.labs.get):
                    if self.labs[lab] > max:
                        max = self.labs[lab]
                if max != -1:
                    print("Saving up machines to file", flush=True)
                    pickle.dump( (self.labs,self.mins), open ("./persistence/labs.p", "wb" ) )
                if self.bot:
                    if self.bot.eloop:
                        self.bot.eloop.create_task(self.bot.updatePMsg())
