import wikipediaapi
import wikipedia
import re

wiki = wikipediaapi.Wikipedia(user_agent = '412 Project', language = 'en')

test = wikipedia.page("Not Like Us")
##text = test.text

infobox_start = test.content.find("{{Infobox")
infobox_end = test.content.find("}}", infobox_start)

infobox = test.content[infobox_start:infobox_end+2]

producer_match = re.search(r"producer\s*=\s*(.*)", infobox, re.IGNORECASE)
if producer_match:
    producer = producer_match.group(1).strip()
    print(producer)
    





