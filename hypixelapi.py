import json
import requests

##=============[setting]========================================
keys=["e973092a-your-key-here-09e69ffbeefb",
      "d66d46a8-your-key-here-65ed0498c06e"]

api_timeout = 3  #default 3 seconds

##==============================================================

key_dis=-1
def nextKey():
    global key_dis
    key_dis+=1
    return keys[key_dis%len(keys)]

def readbw(data,agu):
    try: datareturn = data["stats"]["Bedwars"][agu]
    except Exception:
        try: datareturn = data["achievements"][agu]
        except Exception: datareturn=-1
    return(datareturn)

def getStats(data,modeID):
    modes=["overall","eight_one","eight_two","four_three","four_four","two_four"]
    modeDisplay=["OA","Solo","Double","3S","4S","4v4"]
    modeDisplayLong=["OVERALL","SOLO","DOUBLES","3v3v3v3","4v4v4v4","4v4"]

    if modeID not in range(6): return({"error":"Invalid mode ID"})
    mode=modes[modeID]
    if mode == modes[0]: mode=""
    else: mode=mode+"_"
    bwpar= ["bedwars_level",
            f"{mode}winstreak",
            f"{mode}beds_broken_bedwars",
            f"{mode}beds_lost_bedwars",
            f"{mode}final_kills_bedwars",
            f"{mode}final_deaths_bedwars",
            f"{mode}losses_bedwars",
            f"{mode}wins_bedwars",]

    bwcode=["level",
            "ws",
            "beds_broken",
            "beds_lost",
            "final_kills",
            "final_deaths",
            "losses",
            "wins",]
    from math import ceil, log10, floor
    def round_sig(x, sig=2): return round(x, sig-int(floor(log10(abs(x))))-1)
    bwout={}
    bwdata={bwcode[x]:readbw(data,bwpar[x]) for x in range(len(bwpar))}
    bwout["username"] = data["displayname"]
    bwout["lv"] =       bwdata["level"]
    bwout["ws"] =       max(bwdata["ws"],0)

    bwdata["away"]=0
    if bwdata["final_kills"]<=0:    bwout["fkdr"]=0.00
    elif bwdata["final_deaths"]<=0: bwout["fkdr"]=bwdata["final_kills"]
    else:                           bwout["fkdr"]=int((bwdata["final_kills"]/bwdata["final_deaths"])*10)/10
    bwout["away"]=max(ceil(bwout["fkdr"]+10e-10)*bwdata["final_deaths"]-bwdata["final_kills"],0)
    bwout["nextfkdr"]=ceil(bwout["fkdr"]+10e-10)

    if bwdata["wins"]<=0:           bwout["wr"]="0%"
    elif bwdata["losses"]<=0:       bwout["wr"]="100%"
    else:                           bwout["wr"]=str(int(bwdata["wins"]/(bwdata["losses"]+bwdata["wins"])*100))+"%"

    if bwdata["beds_broken"]<=0:    bwout["bblr"]=0
    elif bwdata["beds_lost"]<=0:    bwout["bblr"]=bwdata["beds_broken"]
    else:                           bwout["bblr"]=round(bwdata["beds_broken"]/bwdata["beds_lost"],1)

    bwout["fkdrperfkill"]="n/a"
    if bwdata["final_kills"]>0 and bwdata["final_deaths"]>0:
        fkdr=bwdata["final_kills"]/bwdata["final_deaths"]
        fkdrf=(bwdata["final_kills"]+1)/bwdata["final_deaths"]
        bwout["fkdrperfkill"]=round_sig(fkdrf-fkdr,3)

    bwout["mode"]=modeDisplay[modeID]
    bwout["modelong"]=modeDisplayLong[modeID]
    return(bwout)


def getPlayer(username,apikey="n/a"):
    if apikey == "n/a": apikey = nextKey()
    try:
        response = requests.get("https://api.hypixel.net/player?key={}&name={}".format(apikey,username), timeout=api_timeout)
    except Exception:
        print("API timeout!")
        out={}
        out["msgsetting"] = False
        out["info"]=["Timeout!","Try again later"]
        out["stats"]=[[""],[""],[""],[""],[""],[""],[""],[""],[""],[""]]
        return(out)
    try:
        player = response.json()
        mode = uuid = channel = ""

        if not player["success"]:
            print("Key error :",apikey)
            return({})
        if "player" in player:
            player = player["player"]
            if player == None:
                player = {}
        if "uuid" in player:
            if "displayname" in player: username = player["displayname"]
            if "uuid" in player: uuid = player["uuid"]
            if "channel" in player:
                if player["channel"] == "PARTY" :
                    channel = "(P)"
            if "mostRecentGameType" in player: mode = player["mostRecentGameType"]
        else: player["displayname"]=username
        msgsetting = False
        try:
            if player["settings"]["privateMessagePrivacy"] == "NONE":
                msgsetting = True
        except Exception:
            pass
        out={}
        out["msgsetting"] = msgsetting
        out["info"]=[username,channel]
        out["stats"]=[getStats(player,x) for x in range(6)]
        return(out)
    except Exception as error_code:
        print("something went wrong!",error_code)
        out={}
        out["msgsetting"] = False
        out["info"]=["Timeout!","Try again later"]
        out["stats"]=[[""],[""],[""],[""],[""],[""],[""],[""],[""],[""]]
        return(out)

def convert(x,mode=0,formatMode=""):
    try:
        info=x["info"]
        stats=x["stats"][mode]
        modeDisplayLong=["OVERALL","SOLO","DOUBLES","3v3v3v3","4v4v4v4","4v4"]
        mainbody = ""
        optional = ""
        mode = modeDisplayLong[mode]

        if stats["lv"] == -1:
            if formatMode=="msg":
                mainbody = info[0]+f'-(Nicked?)(No-data)(mode={mode})'
            elif formatMode=="party":
                mainbody = info[0]+f'-(Nicked?)(No-data)(mode={mode})'
        else:
            if formatMode=="msg":
                mainbody = "[{}✫]{}{}  FKDR:{}  WR:{}  WS:{}  BBLR:{}".format(stats["lv"],info[0],info[1],stats["fkdr"],stats["wr"],stats["ws"],stats["bblr"])
            elif formatMode=="party":
                mainbody = "[{:3d}✫]{:<12} FKDR:{} WR:{} WS:{} BBLR:{}".format(stats["lv"],info[0][:12],stats["fkdr"],stats["wr"],stats["ws"],stats["bblr"])
            optional = "{} Finals till {} FKDR.".format(stats["away"],stats["nextfkdr"])

        return({"main":mainbody,"optional":optional,"mode":mode})
    except Exception as errcode:
        return({"main":"Something went wrong. Please try again in a bit!","optional":"Error","mode":"Error"})
