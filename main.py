import tweepy
from time import sleep
from random import shuffle
from os import environ as env
import traceback

keys = [env.get("UNFBOT_TWITTER_API_KEY"), env.get("UNFBOT_TWITTER_API_KEY_SECRET")]
tokens = [env.get("UNFBOT_TWITTER_API_TOKEN"), env.get("UNFBOT_TWITTER_API_TOKEN_SECRET")]

auth = tweepy.OAuthHandler(keys[0], keys[1])
auth.set_access_token(tokens[0], tokens[1])
api = tweepy.API(auth)

def get_followers(screen_name):
    if (api.get_user(screen_name).protected) == False:
        print("pegando os seguidores de @{}...".format(screen_name))
        ids = list()
        for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
            ids.extend(page)
            sleep(60)
        return ids
    else:
        print("impossivel pegar os seguidores de @{}, conta privada".format(screen_name))
        return []

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
        suspcont = 0
        for follower in oldf:
            if follower not in newf:
                try:
                    unfs.append("@{}".format(api.get_user(int(follower)).screen_name))
                except:
                    suspcont += 1
        if suspcont>0:
            unfs.append("[{} contas suspensas]".format(suspcont))
        if (api.get_user(idbf).protected):
            text = "Sua conta está privada, considere despriva-la."
        else:
            text = "Ninguém deixou de te seguir" if len(unfs)==0 else ("{} pessoas deixaram de te seguir:\n{}".format(len(unfs), "\n".join(unfs)))
        api.send_direct_message(recipient_id=int(idbf), text=text) if len(text)<=10000 else (api.send_direct_message(recipient_id=int(idbf), text="ow na moral vc ta quebrando o bot, não é culpa minha vc ter tanto seguidor assimkk"))
    except Exception as err:
        print(err)
        print(traceback.format_exc())
