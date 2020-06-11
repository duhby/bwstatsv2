import bwstatscore

username= input('email: ')
password= input('password: ')
ign= input('ign: ')
rate= input('rate: ')
whitelist = input('whitelist: [y/N]' )

if whitelist.lower() == "y":
  whitelist = True
else:
  whitelist = False

bwstatsbot = bwstatscore.bot_thread(username,password,ign,rate,whitelist)
bwstatsbot.start()
