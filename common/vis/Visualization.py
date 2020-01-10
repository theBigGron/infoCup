# import libraries
import time
import folium
import os


def create_popup(city, economy, government, hygiene, awareness, population, events):
    """
    Create outer content from html file. Parameters will set into the html file
    :param city: name from the city
    :param economy: economy from this city
    :param government: government from this city
    :param hygiene: hygiene from this city
    :param awareness: awareness from this city
    :param population: population from this city
    :param events: events will build in two other methods
    :return: html code
    """
    return open("popup_main.html").read().format(name=city,
                                                 economy=economy,
                                                 government=government,
                                                 hygiene=hygiene,
                                                 awareness=awareness,
                                                 population=population,
                                                 events=events)


def create_popup_events(infected, prevalence, since_round, event):
    """
    Create outer html content when there are events inside a city
    :param infected: infected from this city
    :param prevalence: prevalence from this city
    :param since_round: since_round from this city
    :param event: events inside this city
    :return: html code
    """
    return open("popup_events.html").read().format(infected=infected, prevalence=prevalence, since_round=since_round,
                                                   event=event)


def create_popup_event(name, infectivity, mobility, duration, lethality):
    """
    List of all events from this city
    :param name: name from this event
    :param infectivity: infectivity from this event
    :param mobility: mobility from this event
    :param duration: duration from this event
    :param lethality: lethality from this city
    :return: html code
    """
    return open("popup_event.html").read().format(name=name, infectivity=infectivity, mobility=mobility,
                                                  duration=duration, lethality=lethality)


class Visualization(object):

    def __init__(self, game_json):
        self.create_map_new(game_json)

    def create_map_new(self, game_json):
        """
        Create the html file with the map and circles
        :param game_json:
        :return:
        """
        map = folium.Map(location=[40, 0], zoom_start=3)
        cities = game_json['cities']

        for city in cities.keys():
            city_name = cities[city]['name']
            longitude = cities[city]['longitude']
            latitude = cities[city]['latitude']
            population = cities[city]['population'] * 1000
            economy = cities[city]['economy']
            government = cities[city]['government']
            hygiene = cities[city]['hygiene']
            awareness = cities[city]['awareness']
            prevalence = 0
            since_round = 0
            events = ''
            event_html = ''

            if 'events' in cities[city]:
                for event in cities[city]['events']:
                    event_type = event['type']
                    if event_type == 'outbreak':
                        event_name = event['pathogen']['name']
                        event_infectivity = event['pathogen']['infectivity']
                        event_mobility = event['pathogen']['mobility']
                        event_duration = event['pathogen']['duration']
                        event_lethality = event['pathogen']['lethality']

                        prevalence = event['prevalence']
                        since_round = event['sinceRound']

                        # TODO: Add all events. This html content is build as a string and put into
                        # the outer html code
                        event_html = create_popup_event(name=event_name, infectivity=event_infectivity,
                                                        mobility=event_mobility, duration=event_duration,
                                                        lethality=event_lethality)

                events = create_popup_events(infected=int(population * prevalence),
                                             prevalence="{0:.2f}".format(prevalence * 100),
                                             since_round=since_round, event=event_html)

            popup = create_popup(city=city_name, economy=economy, government=government, hygiene=hygiene,
                                 awareness=awareness, population=population,
                                 events=events)

            # make circle on map
            folium.Circle(location=(latitude, longitude),
                          radius=population / 40,
                          color=self.rgb2hex(64, 64, 64),
                          popup=popup,
                          fill_color=self.rgb2hex(255, 255 - (prevalence * 255), 255 - (prevalence * 255)),
                          fill=True,
                          fill_opacity=1.0).add_to(map)

        # create folder when not exists
        if not os.path.exists("html"):
            os.makedirs("html")
        map.save('html/worldMap' + str(time.time()) + '.html')

    def rgb2hex(self, r, g, b):
        """
        https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python
        :param r: red
        :param g: green
        :param b: blue
        :return: hex value
        """
        return '#{:02x}{:02x}{:02x}'.format(self.range_rgb(int(r)), self.range_rgb(int(g)), self.range_rgb(int(b)))

    @staticmethod
    def range_rgb(x):
        """
        Check the range for rgb color
        :param x: value to check the limits
        :return:
        """
        if x > 255:
            return 255
        if x < 0:
            return 0
        return x
