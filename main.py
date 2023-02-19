from pprint import pprint

from bs4 import BeautifulSoup
import requests

from tinydb import TinyDB

db = TinyDB('english_call_this_soccer_ptdrr.json', indent=4, encoding='utf-8')
JOUEURS = db.table('joueurs')


def get_link_saison(URL="https://www.psg.fr/equipes/equipe-premiere/effectif", choice_saison: str = "2018"):
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    effectif_filter_by_saison = soup.find('div', class_='select select--inline filter-bar__dropdown')

    # recuperer la balise qui contient les saisons
    select_option = effectif_filter_by_saison.find('select')
    all_option = select_option.findAll('option')

    # Mettre tous les liens dans un tableau
    LINKS = [link_saison['value'] for link_saison in all_option]

    # recuperer les infos des joueurs
    PLAYERS = []

    for link in LINKS:
        r = requests.get(link)
        # Filtrer par date
        if choice_saison in link:
            print(f'Recuperation des données en {choice_saison}..')
            soup = BeautifulSoup(r.content, 'html.parser')

            # si cette balise ne contient pas  d'enfants ca veut dire pas de donner
            player_data = soup.find('div', class_='container player-list')
            if player_data:
                all_player = soup.findAll('a', class_='player-card player-card--with-stats player-card--firstTeam')
                [PLAYERS.append(player['href']) for player in all_player]
                print(f'Recuperation des joueurs terminés...')
            else:
                print('Donées indisponible sur le site...')

    # recuperer les infos des joueurs
    for player in PLAYERS:
        r = requests.get(player)
        soup = BeautifulSoup(r.content, 'html.parser')

        name_player = soup.find('h2', class_='player-profile-details__title u-hidden-mobile').span.text
        naissance = soup.findAll('dd')[1].text
        nationality = soup.findAll('dd')[2].text
        profil = soup.findAll('dd')[3].text
        dexterite = soup.findAll('dd')[4].text
        au_club_depuis = soup.findAll('dd')[5].text
        position = soup.findAll('dd')[-1].text
        description = soup.find('div', class_='player-profile-details__bio')

        if description is not None:
            description = description.p.text
            if description is None:
                description = str(description)

        JOUEURS.insert({'nom': name_player, 'naissance': naissance.strip().replace('        ', '').replace('\n', ''),
                        'nationalite': nationality.strip(), 'profil': profil,
                        'dexterite': dexterite,
                        'position': position,
                        'au_club_depuis': au_club_depuis.strip(),
                        'description': description
                        })
        pprint('Creation de la base de donnée...')
    pprint('La base de donnée est créé avec success')


get_link_saison(choice_saison="2022")

# LES SAISON :
# 2015/16
# 2016/17
# 2017/18
# 2018/19
# 2019/20
# 2020/21
# 2021/22
# 2022/23
