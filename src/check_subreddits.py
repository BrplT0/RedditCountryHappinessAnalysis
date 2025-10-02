import praw
import os
from dotenv import load_dotenv
from prawcore.exceptions import Redirect, NotFound


world = [
    "worldnews", "asktheworld"
]

north_america = [
    "usa", "canada", "mexico", "belize", "guatemala", "elsalvador", "honduras",
    "nicaragua", "costarica", "panama", "bahamas", "cuba", "haiti",
    "dominican", "jamaica", "barbados", "trinidadandtobago", "grenada"
]

south_america = [
    "brazil", "argentina", "chile", "peru", "colombia", "venezuela",
    "ecuador", "bolivia", "paraguay", "uruguay", "guyana", "suriname"
]

#r/russia is quarantined
europe = [
    "iceland", "norway", "sweden", "suomi", "denmark", "estonia", "latvia", "lithuania",
    "poland", "belarus", "ukraine", "ireland", "unitedkingdom", "luxembourg",
    "liechtenstein", "switzerland", "belgium", "germany", "czech", "hungary", "slovakia",
    "austria", "slovenia", "croatia", "serbia", "bulgaria", "romania", "moldova",
    "montenegro", "greece", "macedonia", "albania", "bosnia", "kosovo",
    "turkey", "france", "portugal", "spain", "italy", "netherlands", "malta",
    "monaco", "andorra", "cyprus"
]

asia = [
    "kazakhstan", "mongolia", "china", "iran", "iraq", "syria", "lebanon", "israel",
    "palestine", "jordan", "saudiarabia", "yemen", "oman", "uae", "qatar",
    "kuwait", "bahrain", "afghanistan", "pakistan", "india", "nepal",
    "bangladesh", "bhutan", "srilanka", "maldives", "myanmar", "thailand",
    "cambodia", "laos", "vietnam", "malaysia", "singapore", "indonesia", "timor",
    "philippines", "taiwan", "japan", "korea", "dprk", "armenia", "azerbaijan", "sakartvelo",
    "kyrgyzstan", "tajikistan", "uzbekistan", "turkmenistan", "brunei"
]

oceania = [
    "australia", "newzealand", "papuanewguinea", "fiji", "vanuatu", "samoa",
    "tonga", "solomonislands", "micronesia", "marshallislands",
    "kiribati", "palau", "nauru"
]

#No r/Chad country subreddit
africa = [
    "egypt", "libya", "tunisia", "algeria", "morocco", "westernsahara",
    "mauritania", "mali", "niger", "sudan", "southsudan",
    "ethiopia", "eritrea", "djibouti", "somalia", "kenya", "uganda",
    "rwanda", "burundi", "tanzania", "madagascar", "comoros",
    "seychelles", "mauritius", "mozambique", "zimbabwe", "zambia",
    "malawi", "angola", "namibia", "botswana", "southafrica",
    "lesotho", "swaziland","republicofcongo", "congo", "gabon", "equatorialguinea",
    "cameroon", "nigeria", "ghana", "ivorycoast", "liberia",
    "sierraleone", "guinea", "guinea_bissau", "senegal",
    "gambia", "capeverde", "burkinafaso", "benin", "togo"
]

allSubreddits = world + north_america + south_america + europe + asia + oceania + africa

subNaN = []

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("secret"),
    user_agent="happiness-analyzer/0.1"
)

print("Reddit'e bağlanıyor...\n")

for sub in allSubreddits:
    try:
        for post in reddit.subreddit(sub).hot(limit=1):
            print(f"Subreddit: r/{sub}")
            print(f"Başlık: {post.title}")
            print(f"Score: {post.score}")
            print(f"Yorumlar: {post.num_comments}")
            print("-" * 50)
    except (Redirect, NotFound):
        print(f"❌ r/{sub}: Bulunamadı")
        print("-" * 50)
        subNaN.append(sub)
        continue
    except Exception as e:
        print(f"❌ r/{sub}: Başka hata - {e}")
        print("-" * 50)
        continue

print(subNaN)