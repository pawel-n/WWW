from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from obwody.models import *
import re
import requests


def get_locations(link):
    content = requests \
        .get("http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/" + link) \
        .content.decode('utf-8')
    return BeautifulSoup(content) \
        .select("#s0 tbody a")


def is_gmina(link):
    """ Gminy rozpoznajemy po linku. Trzeba zaifować miasto Warszawę, bo ma dzielnice"""
    link_warszawa = '146501.htm'
    return re.match(r'[0-9]{6}.htm', link) and (not (re.match(r'[0-9]{4}(00).htm', link) or link == link_warszawa))


class Command(BaseCommand):
    help = 'Clears and imports the voting data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing the database...')
        Obwód.objects.all().delete()
        Gmina.objects.all().delete()
        self.stdout.write('Done.')

        self.get_poll_data("index.htm")

    def get_poll_data(self, link):
        self.stdout.write('Scraping ' + link)
        for potential_gmina in get_locations(link):
            pg_link = potential_gmina.attrs['href']

            if is_gmina(pg_link):
                self.stdout.write('Added gmina ' + potential_gmina.string + ' with obwóds:')
                gmina = Gmina(name=potential_gmina.string)
                gmina.save()

                for obwód in get_locations(pg_link):
                    self.stdout.write(' * ' + obwód.string)
                    Obwód(name=obwód.string, gmina=gmina).save()
            else:
                self.get_poll_data(pg_link)
