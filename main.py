import tweepy
from time import sleep

consumer_key = "kA7btSPyTtXD1WeLKkpTjgbRl"
api_secret = "J7UVenQKCu6Z1Eay11Jn4V9uRLPDCTF6OI6PByIAcwXuVYW9lK"
access_token = "1252349748964667392-jKSDT6RSx6uUy7cKrHFGkehex1nB65"
access_token_secret = "WXe3Ot5fDd71vxitZ6gclRyJMRDHUQV70DxPq17r1YIoV"
auth = tweepy.OAuthHandler(consumer_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_followers(screen_name):
    if (api.get_user(screen_name).protected) == False:
        ids = list()
        for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
            ids.extend(page)
        return ids
    else:
        print("impossivel pegar os tweets de @{}, conta privada".format(screen_name))
        return []

for idbf in get_followers(api.me().screen_name):
    try:
        oldf = open("./followers/{}.txt".format(idbf), 'r').read().strip("\n").split("\n")
    except:
        pass
    newf = open("./followers/{}.txt".format(idbf), '+w')
    for idff in get_followers(api.get_user(idbf).screen_name):
        newf.write("{}\n".format(idff))
    newf.close()
    newf = open("./followers/{}.txt".format(idbf), 'r').read()
    unfs = list()
    try:
        for follower in oldf:
            if follower not in newf:
                try:
                    unfs.append(api.get_user(int(follower)).screen_name)
                except:
                    unfs.append("[conta suspensa]")
        text = "Ninguém deixou de te seguir" if len(unfs)==0 else ("{} pessoas deixaram de te seguir:\n{}".format(len(unfs), "\n".join(unfs)))
        api.send_direct_message(recipient_id=int(idbf), text=text)
    except:
        pass
