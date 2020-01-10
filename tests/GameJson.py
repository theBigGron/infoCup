game_json = {

    'outcome': 'pending',
    'round': 25,
    'points': 309,
    'cities': {
        'Abuja': {
            'name': 'Abuja',
            'latitude': 9.077381,
            'longitude': 7.401908,
            'population': 281,
            'connections': [
                'Accra',
                'New York City',
                'Portland'
            ],
            'events': [
                {
                    'type': 'electionsCalled',
                    'round': 9
                },
                {
                    'type': 'campaignLaunched',
                    'round': 1

                },
                {
                    'type': 'outbreak',
                    'pathogen': {
                        'name': 'Endoictus',
                        'infectivity': '-',
                        'mobility': 'o',
                        'duration': '+',
                        'lethality': '--'
                    },
                    'prevalence': 0.708185053380783,
                    'sinceRound': 21
                },
                {
                    'type': 'outbreak',
                    'pathogen': {
                        'name': 'Methanobrevibacter colferi',
                        'infectivity': 'o',
                        'mobility': '++',
                        'duration': '--',
                        'lethality': '-'
                    },
                    'prevalence': 0.412186013480783,
                    'sinceRound': 21
                },
            ],
            'economy': 'o',
            'government': '-',
            'hygiene': '-',
            'awareness': '-'
        },
        'Accra': {
            'name': 'Accra',
            'latitude': 5.602139,
            'longitude': -0.186598,
            'population': 407,
            'connections': [
                'Abuja',
                'New York City'
            ],
            'events': [
                {
                    'type': 'outbreak',
                    'pathogen': {
                        'name': 'Endoictus',
                        'infectivity': '-',
                        'mobility': 'o',
                        'duration': '+',
                        'lethality': '--'
                    },
                    'prevalence': 0.06142506142506143,
                    'sinceRound': 6
                }
            ],
            'economy': '-',
            'government': 'o',
            'hygiene': '-',
            'awareness': '-'
        },
        'Albuquerque': {
            'name': 'Albuquerque',
            'latitude': 35.086263,
            'longitude': -106.646962,
            'population': 401,
            'connections': [
                'Portland',
                'Anchorage'
            ],
            'events': [
                {
                    'type': 'outbreak',
                    'pathogen': {
                        'name': 'Endoictus',
                        'infectivity': '-',
                        'mobility': 'o',
                        'duration': '+',
                        'lethality': '--'
                    },
                    'prevalence': 0.08977556109725686,
                    'sinceRound': 7
                }
            ],
            'economy': 'o',
            'government': 'o',
            'hygiene': 'o',
            'awareness': 'o'
        },
        'Amsterdam': {
            'name': 'Amsterdam',
            'latitude': 52.367178,
            'longitude': 4.891943,
            'population': 847,
            'connections': [
                'Anchorage',
                'New York City'
            ],
            'economy': '++',
            'government': '+',
            'hygiene': '++',
            'awareness': '++'
        },
        'Anchorage': {
            'name': 'Anchorage',
            'latitude': 61.216336,
            'longitude': -149.907299,
            'population': 236,
            'connections': [
                'Andorra la Vella',
                'Abuja'
            ],
            'events': [
                {
                    'type': 'outbreak',
                    'pathogen': {
                        'name': 'Endoictus',
                        'infectivity': '-',
                        'mobility': 'o',
                        'duration': '+',
                        'lethality': '--'
                    },
                    'prevalence': 0.09745762711864407,
                    'sinceRound': 7
                },
                {
                    'type': 'influenceExerted',
                    'round': 22
                }
            ],
            'economy': 'o',
            'government': '++',
            'hygiene': '+',
            'awareness': '+'
        },
        'Andorra la Vella': {
            'name': 'Andorra la Vella',
            'latitude': 42.506548,
            'longitude': 1.521481,
            'population': 15,
            'connections': [
                'Portland',
                'Abuja'
            ],
            'events': [
                {
                    'type': 'outbreak',
                    'pathogen': {
                        'name': 'Moricillus ☠',
                        'infectivity': '-',
                        'mobility': 'o',
                        'duration': '-',
                        'lethality': '+'
                    },
                    'prevalence': 0.2,
                    'sinceRound': 20
                }
            ],
            'economy': '+',
            'government': '+',
            'hygiene': '+',
            'awareness': '+'
        },
        'New York City': {
            'name': 'New York City',
            'latitude': 40.71354,
            'longitude': -74.04286,
            'population': 8623,
            'connections': [
                'Abuja',
                'Portland'
            ],
            'events': [
                {
                    'type': 'outbreak',
                    'pathogen': {
                        'name': 'Endoictus',
                        'infectivity': '-',
                        'mobility': 'o',
                        'duration': '+',
                        'lethality': '--'
                    },

                    'prevalence': 0.9641656036182303,
                    'sinceRound': 2
                },
                {
                    'type': 'quarantine',
                    'sinceRound': 7,
                    'untilRound': 9
                },

                {
                    'type': 'airportClosed',
                    'sinceRound': 5,
                    'untilRound': 7
                }
            ],
            'economy': 'o',
            'government': 'o',
            'hygiene': 'o',
            'awareness': 'o'
        },
        'Portland': {
            'name': 'Portland',
            'latitude': 45.501254,
            'longitude': -122.67562,
            'population': 648,
            'connections': [
                'New York City',
                'Abuja',
                'Andorra la Vella'
            ],
            'events': [
                {
                    'type': 'outbreak',
                    'pathogen': {
                        'name': 'Azmodeus',
                        'infectivity': 'o',
                        'mobility': 'o',
                        'duration': 'o',
                        'lethality': 'o'
                    },
                    'prevalence': 0.7330246913580247,
                    'sinceRound': 2
                },
                {
                    'type': 'hygienicMeasuresApplied',
                    'round': 3
                }
            ],
            'economy': '+',
            'government': '+',
            'hygiene': '++',
            'awareness': '++'
        }},
    'events': [
        {
            'type': 'pathogenEncountered',
            'pathogen': {
                'name': 'Endoictus',
                'infectivity': '-',
                'mobility': 'o',
                'duration': '+',
                'lethality': '--'
            },
            'round': 1
        },
        {
            'type': 'pathogenEncountered',
            'pathogen': {
                'name': 'Moricillus ☠',
                'infectivity': '-',
                'mobility': 'o',
                'duration': '-',
                'lethality': '+'
            },
            'round': 1
        },
        {
            'type': 'pathogenEncountered',
            'pathogen': {
                'name': 'Admiral Trips',
                'infectivity': '++',
                'mobility': '+',
                'duration': '-',
                'lethality': '++'
            },
            'round': 1
        },
        {
            'type': 'vaccineInDevelopment',
            'pathogen': {
                'name': 'Phagum vidiianum',
                'infectivity': 'o',
                'mobility': 'o',
                'duration': '+',
                'lethality': '+'
            },
            'sinceRound': 5,
            'untilRound': 11
        },
        {
            'type': 'vaccineAvailable',
            'pathogen': {
                'name': 'Procrastinalgia',
                'infectivity': '-',
                'mobility': '--',
                'duration': '++',
                'lethality': '--'
            },
            'sinceRound': 11
        },
        {
            'type': 'vaccineAvailable',
            'pathogen': {
                'name': 'Methanobrevibacter colferi',
                'infectivity': 'o',
                'mobility': '++',
                'duration': '--',
                'lethality': '-'
            },
            'sinceRound': 11
        },
        {
            'type': 'medicationInDevelopment',
            'pathogen': {
                'name': 'Admiral Trips',
                'infectivity': '++',
                'mobility': '+',
                'duration': '-',
                'lethality': '++'
            },
            'sinceRound': 5,
            'untilRound': 8
        },
        {
            'type': 'medicationAvailable',
            'pathogen': {
                'name': 'Methanobrevibacter colferi',
                'infectivity': 'o',
                'mobility': '++',
                'duration': '--',
                'lethality': '-'
            },
            'sinceRound': 8
        },
        {
            'type': 'largeScalePanic',
            'sinceRound': 16
        }
    ]
}

"""
List for cities, city_names and diseases
"""

cities = [
    {
        'city_name': 'Abuja',
        'population': 0.003635781911257835,
        'amount_connections': 0.25,
        'connected_city_population': 0.014492887749530323,
        'economy': 0.5,
        'government': 0.25,
        'hygiene': 0.25,
        'awareness': 0.25,
        'anti-vaccinationism': 0
    },
    {
        'city_name': 'Accra',
        'population': 0.0021074314060163597,
        'amount_connections': 0.25,
        'connected_city_population': 0.011011791832315094,
        'economy': 0.25,
        'government': 0.5,
        'hygiene': 0.25,
        'awareness': 0.25,
        'anti-vaccinationism': 0
    },
    {
        'city_name': 'Albuquerque',
        'population': 0.0012031132869980473,
        'amount_connections': 0.1,
        'connected_city_population': 0.004329885730679785,
        'economy': 0.5,
        'government': 0.5,
        'hygiene': 0.5,
        'awareness': 0.5,
        'anti-vaccinationism': 0
    },
    {
        'city_name': 'Amsterdam',
        'population': 0.0011422965713915525,
        'amount_connections': 0.3,
        'connected_city_population': 0.01724814938700717,
        'economy': 1,
        'government': 0.75,
        'hygiene': 1,
        'awareness': 1,
        'anti-vaccinationism': 0
    },
    {
        'city_name': 'Anchorage',
        'population': 0.0005328073128134209,
        'amount_connections': 0.3,
        'connected_city_population': 0.02165339496093848,
        'economy': 0.75,
        'government': 1,
        'hygiene': 0.75,
        'awareness': 0.75,
        'anti-vaccinationism': 0
    },
    {
        'city_name': 'Andorra la Vella',
        'population': 2.9086255290062682e-05,
        'amount_connections': 0.0,
        'connected_city_population': 0.0,
        'economy': 0.75,
        'government': 0.75,
        'hygiene': 0.75,
        'awareness': 0.75,
        'anti-vaccinationism': 0
    },
    {
        'city_name': 'New York City',
        'population': 0.011400489971191386,
        'amount_connections': 0.4,
        'connected_city_population': 0.07359880270396406,
        'economy': 0.5,
        'government': 0.5,
        'hygiene': 0.5,
        'awareness': 0.5,
        'anti-vaccinationism': 0
    },
    {
        'city_name': 'Portland',
        'population': 0.0008567224285436644,
        'amount_connections': 0.15,
        'connected_city_population': 0.011300010180189352,
        'economy': 0.75,
        'government': 0.75,
        'hygiene': 1,
        'awareness': 1,
        'anti-vaccinationism': 0
    }
]

city_names = {"Abuja", "Accra", "Albuquerque", "Amsterdam", "Anchorage", "Andorra la Vella", "New York City",
              "Portland"}

diseases = [{'id': 0, 'name': 'Endoictus', 'vaccine_available_or_in_development': 0,
             'medication_available_or_in_development': 0, 'duration': 0.75, 'lethality': 0,
             'infectivity': 0.25, 'mobility': 0.5, 'world_prevalence': 0.7503054634316635},
            {'id': 1, 'name': 'Moricillus ☠', 'vaccine_available_or_in_development': 0,
             'medication_available_or_in_development': 0, 'duration': 0.25, 'lethality': 0.75,
             'infectivity': 0.25, 'mobility': 0.5, 'world_prevalence': 0.00026182579856868566},
            {'id': 2, 'name': 'Admiral Trips', 'vaccine_available_or_in_development': 0,
             'medication_available_or_in_development': 1, 'duration': 0.25, 'lethality': 1, 'infectivity': 1,
             'mobility': 0.75, 'world_prevalence': 0.0}]
