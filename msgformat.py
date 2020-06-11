## --------in hypixelapi.py--------------
## def convert(x,mode=0,formatMode=""):
##    return({"main":mainbody,"optional":optional,"mode":mode})
import random

def insertNoBreak(msg):
    #return(msg.replace(" ","‾"))
    return(msg.replace(" ","┈"))

def insertInvis(msg,n):
    for i in range(n):
        randomPos=random.randint(0,len(msg)-1)
        invischar="⛬⛫⛭⛮⛶"
        msg=msg[:randomPos]+invischar[random.randint(0,len(invischar)-1)]+msg[randomPos:]
    return(msg)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield(l[i:i+n])

# ================[SETTINGS]================
bots=["bwstatsv2"] # add your bot here
announcement="[bruh]" # add your announcement here
# ==========================================

def promote():
  return(f'Made with <3 from FatDubs') # change this if u want

class formats:
    def __init__(self, bot_ign, party_max=12):
        self.bot_ign = bot_ign
        self.party_max = party_max

    def msg(self, raw,nextfkdr=False):
        modeLabel=f"[{raw['mode']}]"
        pack=[]
        pack.append(promote())
        pack.append( f"{modeLabel:-^51}" )
        if nextfkdr: pack.append( insertNoBreak("       "+raw['optional']) )
        pack.append( insertNoBreak(raw['main']) )
        pack.append( f"{announcement:-^51}" )
        return(insertInvis(" ".join(pack),35))

    def party(self, raws, mode):
        modeDisplay=["OVERALL","SOLO","DOUBLES","3v3v3v3","4v4v4v4","4v4"]
        blocks = chunks(raws,4)
        for block in blocks:
            pack=[]
            pack.append(promote())
            pack.append(f'[{modeDisplay[mode]}]')
            for line in block: pack.append(insertNoBreak(line))
            if len(" ".join(pack))<200:
                yield(insertInvis(" ".join(pack),40))
            else:
                yield(" ".join(pack))
        if announcement!="":
            yield(announcement)

    def wrong_syntax(self):
        pack=[]
        link=[]
        pack.append(promote())
        pack.append(insertNoBreak(f'Use "/msg {self.bot_ign} username" for overall stats'))
        pack.append("                       v v v v v v v v v v v v v v v v")
        link = f' https://hastebin.com/irekakelaq.rb'
        return(insertInvis(" ".join(pack),20)+link)

    def party_too_large(self):
        pack=[]
        pack.append(f'max party size is {self.party_max}!!')
        return(insertInvis(" ".join(pack),30))

    def party_mode(self,mode):
        modeDisplay=["OVERALL","SOLO","DOUBLES","3v3v3v3","4v4v4v4","4v4"]
        return(insertInvis(insertNoBreak(f"Got it! Next time you invite me I will show {modeDisplay[mode]} stats."),10))

    def overload(self):
        pack=[]
        pack.append(promote())
        pack.append(insertNoBreak("I'm currently under heavy load? hmm try again later ig lol"))
        pack.append("_"*50)
        return(insertInvis(" ".join(pack),40))

    def msgsendtomin(self):
        temp = bots[random.randint(0,len(bots)-1)]
        if temp!=self.bot_ign:
            return(insertInvis(f"-> Alternative Bot:. {temp} | Main Bot:. bwstats",10))
        return(None)
