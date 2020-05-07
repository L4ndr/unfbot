import tweepy
from time import sleep
from random import shuffle
import credentials

keys, tokens = credentials.api()

auth = tweepy.OAuthHandler(keys[0], keys[1])
auth.set_access_token(tokens[0], tokens[1])
api = tweepy.API(auth)

def get_followers(screen_name):
    if (api.get_user(screen_name).protected) == False:
        ids = list()
        for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
            ids.extend(page)
            sleep(60)
        return ids
    else:
        print("impossivel pegar os seguidores de @{}, conta privada".format(screen_name))
        return ["Sua conta está privada, considere despriva-la."]

idsbf = get_followers(api.me().screen_name) #idsbf = ids dos seguidores do bot
shuffle(idsbf)

for idbf in idsbf:
    try:
        oldf = open("./followers/{}.txt".format(idbf), 'r').read().strip("\n").split("\n")
    except:
        pass
    newf = open("./followers/{}.txt".format(idbf), '+w')
    for idff in get_followers(api.get_user(idbf).screen_name): #idff = id do seguidor do seguidor
        newf.write("{}\n".format(idff))
    newf.close()
    newf = open("./followers/{}.txt".format(idbf), 'r').read()
    unfs = list()
    try:
        for follower in oldf:
            if follower not in newf:
                try:
                    unfs.append("@{}".format(api.get_user(int(follower)).screen_name))
                except:
                    unfs.append("[conta suspensa]")
        text = "Ninguém deixou de te seguir" if len(unfs)==0 else ("{} pessoas deixaram de te seguir:\n{}".format(len(unfs), "\n".join(unfs)))
        api.send_direct_message(recipient_id=int(idbf), text=text)
    except:
        pass