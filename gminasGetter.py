# Encoding: utf-8
import requests
import django
import re
from bs4 import BeautifulSoup

__author__ = 'fc346868'


linkWarszawa = '146501.htm'
gminas = []
komisjas = []


def get_locations(link):
        page = requests.get("http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/" + link)
        p_text = page.content.decode('utf-8')
        p_text_soup = BeautifulSoup(p_text)
        return p_text_soup.select("#s0 tbody a")


def is_gmina(link):
    """ Gminy rozpoznajemy po linku. Trzeba zaifować miasto Warszawę, bo ma dzielnice"""
    return re.match(r'[0-9]{6}.htm', link) and (not (re.match(r'[0-9]{4}(00).htm', link) or link == linkWarszawa))


def get_poll_data(link):
    locations = get_locations(link)
    if is_gmina(link):
        for new_komisja in locations:
            komisjas.append(new_komisja.string)
    else:
        for potential_gmina in locations:
            pg_link = potential_gmina.attrs['href']
            if is_gmina(pg_link):
                gminas.append(potential_gmina.string)
            get_poll_data(pg_link)

get_poll_data("index.htm")

print "gmin: ", len(gminas)
print "komisji: ", len(komisjas)

for gmina in gminas:
    print gmina.encode('utf-8')
for komisja in komisjas:
    print komisja.encode('utf-8')