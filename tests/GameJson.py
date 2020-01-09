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
