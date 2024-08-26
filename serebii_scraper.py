import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

current_date = datetime.now();
sv_news, tera_raids, event_distributions = [], [], []

# parse the daily news
home_url = "https://www.serebii.net/"
response = requests.get(home_url)

if response.status_code == 200:
    page = BeautifulSoup(response.content, 'html.parser')

    post = page.find("div", class_="post")
    headline = post.find("h2")
    date = headline.find("a").get("id")
    sub_categories = post.find_all("div", class_="subcat")

    for subcat in sub_categories:
        games_department = subcat.find('h3', string="In The Games Department")
        if games_department:
            game = subcat.find("p", class_="title").string
            if game == "Pokémon Scarlet & Violet":
                news_info = subcat.find("p", class_=lambda x: x is None).text
                news_data = {
                    "department": games_department.string,
                    "game": game,
                    "news-info": news_info
                }
                sv_news.append(news_data)
else:
    print("Error getting Serebii news.")

# time.sleep(5);

# parse tera raid database
tera_raid_url = "https://www.serebii.net/scarletviolet/teraraidbattleevents.shtml"
response = requests.get(tera_raid_url)

if response.status_code == 200:
    page = BeautifulSoup(response.content, 'html.parser')
    main_tag = page.find("main")

    tera_raids_table = main_tag.find("table")
    #extract the raid pokemon name
    raid_poke = tera_raids_table.find("h2")
    tera_raid_content = tera_raids_table.find("td", class_="foocontent")

    # extract the dates
    dates = tera_raid_content.find("b", string="Global:").next_sibling.strip()
    # removes st, nd, rd, or th after the date
    date_string_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', dates)
    raid_start_date_str, raid_end_date_str = date_string_cleaned.split(" - ")

    raid_date_format = "%B %d %Y"

    # convert dates to datetime objects
    raid_start_date = datetime.strptime(raid_start_date_str + " " + str(current_date.year), raid_date_format)
    raid_end_date = datetime.strptime(raid_end_date_str, raid_date_format)


    # check if current_date falls within the date ranges
    if raid_start_date <= current_date <= raid_end_date:
        formatted_raid_start_date = raid_start_date.strftime("%B %d %Y")
        formatted_raid_end_date = raid_end_date.strftime("%B %d %Y")
        date_range = str(formatted_raid_start_date) + " - " + str(formatted_raid_end_date)
        tera_raid_data = {
            "raid_poke": raid_poke.string,
            "dates": date_range
        }
        tera_raids.append(tera_raid_data)
else:
    print("Error accessing tera raid battle events.")

# time.sleep(5)

# parse distributions
dist_url_template = "https://www.serebii.net/events/{}.shtml"
distribution_url = dist_url_template.format(current_date.year)
response = requests.get(distribution_url)

if response.status_code == 200:
    page = BeautifulSoup(response.content, 'html.parser')
    eventpoke_list = page.find_all("table", class_="eventpoke")

    for eventpoke in eventpoke_list:
        # check if they're Global or NA
        desc_type_loc_row = eventpoke.find("tr").find_next_sibling();
        desc_type_loc_info = desc_type_loc_row.find("tr").find_next_sibling();
        description = desc_type_loc_info.find_all("td")[0].string
        location = desc_type_loc_info.find_all("td")[2].string
        if location != "Global":
            if location != "North America":
                continue

        # get the event pokemon's name
        a_tag = eventpoke.find("a")
        href = a_tag['href']
        match = re.search(r'pokedex-sv/([^/]+)/?', href)
        pokemon_name = ""
        if match:
            pokemon_name = match.group(1).capitalize()
        
        date_table = eventpoke.find("table", class_="date");
        dist_start_date_str = date_table.find_all("td")[2].string.strip();
        dist_end_date_str = date_table.find_all("td")[3].string.strip();

        # convert from str to datetime objects
        dist_date_format = "%d %B %Y"
        dist_start_date = datetime.strptime(dist_start_date_str, dist_date_format)
        end_date = True
        try :
            dist_end_date = datetime.strptime(dist_end_date_str, dist_date_format)
        except ValueError: # error occurs because end date is "No End Date"
            dist_end_date = dist_end_date_str
            end_date = False

        if end_date:
            if dist_start_date <= current_date <= dist_end_date:
                date_range = dist_start_date_str + " - " + dist_end_date_str
                # current_distributions.append((pokemon_name, date_range))
                dist_data = {
                    'pokemon': pokemon_name,
                    'dates': date_range,
                    'description': description
                }
                event_distributions.append(dist_data)
        else:
            if dist_start_date <= current_date:
                date_range = dist_start_date_str + " - " + dist_end_date_str
                dist_data = {
                    'pokemon': pokemon_name,
                    'dates': date_range,
                    'description': description
                }
                event_distributions.append(dist_data)
else:
    print("Error getting distribution page")
