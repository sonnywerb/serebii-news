import re
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# parse the daily news
# home_url = "https://www.serebii.net/"
# response = requests.get(home_url)

# if response.status_code == 200:
#     page = BeautifulSoup(response.content, 'html.parser')

#     post = page.find("div", class_="post")
#     headline = post.find("h2")
#     date = headline.find("a").get("id")
#     sub_categories = post.find_all("div", class_="subcat")
#     print(date + " - " + headline.string)

#     for subcat in sub_categories:
#         games_department = subcat.find('h3', string="In The Games Department")
#         if games_department:
#             game = subcat.find("p", class_="title").string
#             # if game == "Pokémon Scarlet & Violet":
#             if game == "Pokémon Masters EX":
#                 info = subcat.find("p", class_=lambda x: x is None).text
#                 print(("============================================="))
#                 print(games_department.string)
#                 print(game)
#                 print("News Info: " + info)
# else:
#     print("Unable to send GET request")

# time.sleep(30);

# parse tera raid database
tera_raid_url = "https://www.serebii.net/scarletviolet/teraraidbattleevents.shtml"
response = requests.get(tera_raid_url)

if response.status_code == 200:
    page = BeautifulSoup(response.content, 'html.parser')
    main_tag = page.find("main")

    tera_raids_table = main_tag.find("table")
    #extract the raid pokemon name
    event_name = tera_raids_table.find("h2")
    tera_raid_content = tera_raids_table.find("td", class_="foocontent")

    # extract the dates
    dates = tera_raid_content.find("b", string="Global:").next_sibling.strip()
    # removes st, nd, rd, or th after the date
    date_string_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', dates)
    start_date_str, end_date_str = date_string_cleaned.split(" - ")

    date_format = "%B %d %Y"

    # convert dates to datetime objects
    start_date = datetime.strptime(start_date_str + " 2024", date_format)
    end_date = datetime.strptime(end_date_str, date_format)
    
    current_date = datetime.now();

    # check if current_date falls within the date ranges
    if start_date <= current_date <= end_date:
        print("Event: " + event_name.string)
        print("Dates: " + dates)

time.sleep(30)

# parse distributions










