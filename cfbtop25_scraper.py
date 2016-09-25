import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) > 2 or len(sys.argv) < 1:
    print " Usage: python cfbtop25_scraper.py [ranking poll (AP | Coaches)]\n If no argument is supplied, both poll results are displayed"
    exit()

class print_colors:
    BLUE = '\033[94m'
    RED = '\033[31m'
    ENDC = '\033[0m'

def set_up_soup():
    endpoint = "http://www.espn.com/college-football/rankings"
    doc = requests.get(endpoint)
    soup = BeautifulSoup(doc.content, "html.parser")

    return soup

def parse_html_table(list_name):
    soup = set_up_soup()
    rankings_list = []

    table_names = soup.findAll("h2", { "class" : "table-caption" })
    table_list = soup.findAll("table", { "class" : "rankings has-team-logos" })

    if list_name.lower() == "ap":
        table = table_list[0]
    if list_name.lower() == "coaches":
        table = table_list[1]

    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 5:
            rank = cells[0].find(text=True)
            team = cells[1].find(text=True)
            record = cells[2].find(text=True)
            points = cells[3].find(text=True)

            team_tuple = (str(rank), str(team), str(record), str(points))
            rankings_list.append(team_tuple)

    return rankings_list


def print_table(rankings_list):
    header = ('RK', 'TEAM', 'REC', 'PTS')
    print "{0:{1}}".format(header[0], 5) + "{0:{1}}".format(header[1], 20) + "{0:{1}}".format(header[2], 5) + header[3]
    for row in rankings_list:
        if "Boise" in row[1]:
            print "{0:{1}}".format(row[0], 5) + print_colors.BLUE + "{0:{1}}".format(row[1], 20) + print_colors.ENDC + "{0:{1}}".format(row[2], 5) + row[3]
        else:
            print "{0:{1}}".format(row[0], 5) + "{0:{1}}".format(row[1], 20) + "{0:{1}}".format(row[2], 5) + row[3]
    print "\n"
    return

if len(sys.argv) == 2:
    poll_name = sys.argv[1].lower()
    if poll_name == "ap":
        print print_colors.RED + "AP TOP 25" + print_colors.ENDC
    if poll_name == "coaches":
        print print_colors.RED + "COACHES POLL" + print_colors.ENDC
    print_table(parse_html_table(poll_name))
else:
    print print_colors.RED + "AP TOP 25" + print_colors.ENDC
    print_table(parse_html_table("ap"))
    print print_colors.RED + "COACHES POLL" + print_colors.ENDC
    print_table(parse_html_table("coaches"))
