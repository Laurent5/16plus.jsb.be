# -*- coding: utf-8 -*- 

import os.path
import time
from copy import deepcopy

import json

from tumulus.tags import *

# Local project imports:
from config import JSON_PATH


class Profile(object):
    '''
        Handles loading and saving of user profile data.
    '''
    
    @classmethod
    def exists(identifier):
        'Returns whether or not a profile for the given user exists.'
        path = os.path.join(JSON_PATH, self.identifier + '.json')
        return os.path.isfile(path)
    
    def __init__(self, identifier):
        self.identifier = identifier
        self.load()

    def load(self):
        path = os.path.join(JSON_PATH, self.identifier + '.json')
        if os.path.isfile(path):
            self.data = json.load(open(path))
        else:
            self.data = new_profile(self.identifier)

    def update(self, new):
        for key in new:
            value = new[key].strip()
            self.update_field(key, value)

    def update_field(self, field, value):
        queue = field.split('.')
        cursor = self.data
        while len(queue) > 1:
            key = queue.pop(0)
            if key.isdigit(): 
                key = int(key)
            cursor = cursor[key]
        key = queue.pop(0)
        cursor[key] = value

    def save(self):
        # Saving copy on disk:
        path = os.path.join(JSON_PATH, self.identifier + '.json')
        if not os.path.isdir(JSON_PATH):
            os.makedirs(JSON_PATH)
        json.dump(self.data, open(path, 'w'))
        # TODO: Running copy in DB:
        #rethinkdb...


def page(user, message=None):
    '''
        Generates the profile editor page using Tumulus.
    '''

    def field(desc, path, large=False):
        'Creates the appropriate input li fields from description and dotted path.'

        # Extracting user values from the path
        # (some.key -> user['some']['key'])
        queue = path.split('.')
        value = user.data
        while queue:
            key = queue.pop(0)
            if key.isdigit():
                value = value[int(key)]
            else:
                value = value[key]

        if large:
            return li(desc, br(), textarea(value, name=path))
        else:
            return li(desc, input_(name=path, value=value))

    return html(
        head(
            meta(charset='utf-8'),
            link(rel='stylesheet', href='/static/brick-1.0beta6.byob.min.css'),
            link(rel='stylesheet', href='/static/16plus.css'),
            title('Profil JSB 16+'),
            style('x-datepicker {height: 1.5em;}', type='text/css'),
        ),

        body(
            header(
                img(src='/static/16+logo.png', alt='logo', class_='logo'),
                a(span('Retour'), href='/', class_='menu_link'),
                h1('Profil 16+'),
                div(message) if message else '',
            ),
            form(
                section(
                    input_(type='submit', value='Enregistrer'),
                ),
                section(
                    h2('Compte'),
                    ul(
                        li('Identifiant : ', user.data['account']['id']),
                        li('Date de creation : ', time.ctime(user.data['account']['stats']['creation'])),
                    ),
                ),
                section(
                    h2('Personnel'),
                    ul(
                        field('Prenom', 'personal.firstname'),
                        field('Nom de famille', 'personal.familyname'),
                        #field('Date de naissance', 'personal.birthdate'),
                        li('Date de naissance', 
                           '<x-datepicker name="personal.birthdate" value="' + \
                           user.data['personal']['birthdate'] + \
                           '"></x-datepicker>'),
                    ),
                ),
                section(
                    h2('Contact'),
                    ul(
                        field('Courriel (email)', 'contact.email'),
                        field('Telephone', 'contact.phone'),
                        field('Domicile', 'contact.domicile', large=True),
                        field('Adresse postale (si differente)', 'contact.post', large=True),
                    ),
                ),
                section(
                    h2('En cas de probleme'),
                    h3('Personne 0'),
                    ul(
                        field('Relation', 'emergency.0.relationship'),
                        field('Prenom', 'emergency.0.firstname'),
                        field('Nom de famille', 'emergency.0.familyname'),
                        field('Telephone portable', 'emergency.0.gsm'),
                        field('Telephone alternatif', 'emergency.0.phone'),
                    ),
                    h3('Personne 1'),
                    ul(
                        field('Relation', 'emergency.1.relationship'),
                        field('Prenom', 'emergency.1.firstname'),
                        field('Nom de famille', 'emergency.1.familyname'),
                        field('Telephone portable', 'emergency.1.gsm'),
                        field('Telephone alternatif', 'emergency.1.phone'),
                    ),
                ),
                section(
                    input_(type='submit', value='Enregistrer'),
                ),
                action='/profil', method='POST',
            ),
            script(src='/static/brick-1.0beta6.byob.min.js'),
        ),
    )


empty_profile = {
        'account': {
            'id': None,
            'stats': {
                'creation': None,
            },
        },
        'personal': {
            'firstname': '',
            'familyname': '',
            'birthdate': '',
        },
        'contact': {
            'email': '',
            'phone': '',
            'domicile': '',
            'post': '',
        },
        'emergency': [
            {'firstname': '',
              'familyname': '',
              'relationship': '',
              'gsm': '',
              'phone': '',
            },
            {'firstname': '',
              'familyname': '',
              'relationship': '',
              'gsm': '',
              'phone': '',
            },
        ],
    }


def new_profile(identifier):
    "Generates a new profile using the 'empty_profile' template."
    profile = deepcopy(empty_profile)
    profile['account']['id'] = identifier
    profile['account']['stats']['creation'] = time.time()
    return profile


if __name__ == '__main__':
    # Test function outputs a sample user:

    user = {
        'account': {
            'id': 'orwell@1984.apocalypse',
            'stats': {
                'creation': '1984-01-02',
            },
        },
        'personal': {
            'firstname': 'Georges',
            'familyname': 'Orwell',
            'birthdate': '1984-01-01',
        },
        'contact': {
            'email': '',
            'phone': '0486.000.002',
            'domicile': 'rue du Cinema 32',
            'post': '',
        },
        'emergency': [
            {'firstname': 'Dark',
              'familyname': 'Vador',
              'relationship': 'pere',
              'gsm': '0486.000.002',
              'phone': '020000001',
            },
            {'firstname': 'Lily',
              'familyname': 'Pad',
              'relationship': 'mere',
              'gsm': '0486.000.003',
              'phone': '020000002',
            },
        ],
    }
    print(page(user))
