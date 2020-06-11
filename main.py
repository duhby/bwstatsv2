import bwstatscore

username= input('email: ')
password= input('password: ')
ign= input('ign: ')
rate= input('rate: ')

bwstatsbot = bwstatscore.bot_thread(username,password,ign,rate)
bwstatsbot.start()
