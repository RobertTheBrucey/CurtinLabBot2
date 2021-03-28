if __name__ == '__main__':
    import discord
    import botClient as bc
    from config import getToken,getCreds
    import sys
    import logging
    import datetime
    import time
    from discord.ext import commands

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='./persistence/discord'+str(datetime.datetime.now())+'.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    if len(sys.argv) < 2:
        configfile = "./persistence/config.ini"
    else:
        configfile = sys.argv[1]

    try:
        getToken(filename=configfile)
    except:
        print("Config file invalid, creating a new one")
        base = "[token]\n\
token=\n\n\
[logging]\n\
logfile="
        file = open("config.ini", "w")
        file.write(base)
        file.close()
        exit()

    """ Setup """
    client = bc.BotClient(configfile)
    client.run(getToken(filename=configfile))
