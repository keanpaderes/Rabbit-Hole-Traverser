from bs4 import BeautifulSoup
import json
import requests
import sys

# The original end of tweet
# rabbit_hole_end = "/TylerAdobe/status/936369543919702016"

# Initialization
root = "https://twitter.com"
if(len(sys.argv) == 2):
    verbose = True
    url = sys.argv[1].replace(root, "")
elif(len(sys.argv) == 3):
    verbose = sys.argv[1] == "true"
    url = sys.argv[2].replace(root, "")
else:
    print("Error in running the script! Please follow the syntax: `python rabbit_hole_traverser <is_verbose> <starting_tweet_url>`")
    sys.exit()
    
rabbit_hole_start = root + url
rabbit_hole_level = 1
headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
is_it_the_light = False
is_premature = False

# While loop
while not is_it_the_light:
    req_url = root + url
    req = requests.get(req_url, headers = headers)
    soup = BeautifulSoup(req.text, "html.parser")

    is_protected_timeline = soup.find_all("div", class_="ProtectedTimeline")

    if(len(is_protected_timeline) > 0):
        is_premature = True
        is_it_the_light = True
    else:
        tweet_details = soup.find_all("div", class_="permalink-tweet")[0]
        parsed_json_details = json.loads(tweet_details.get("data-reply-to-users-json"))[0]
        current_user = parsed_json_details["name"] + " @" + parsed_json_details["screen_name"]
        if verbose:
            print("Rabbit hole user: " + current_user + " | level: " + str(rabbit_hole_level))

        quote_tweet_container = tweet_details.find_all("div", class_="QuoteTweet-container")
        if quote_tweet_container:
            quote_tweet_link = quote_tweet_container[0].find_all("a", class_="QuoteTweet-link")[0]
            url = quote_tweet_link.get("href")
            rabbit_hole_level = rabbit_hole_level + 1
        else:
            is_it_the_light = True

if not is_premature:
    print("Your tweet (\'" + rabbit_hole_start + "\') will take you " + str(rabbit_hole_level) + " tweets to reach the light if you go down that rabbit hole. (" + root + url + ")")
else:
    print("Your tweet (\'" + rabbit_hole_start + "\') encountered a quote of a protected account at level " + str(rabbit_hole_level) + ".")
