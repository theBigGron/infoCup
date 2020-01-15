var map, cityCircle, hello;
var circleMap, last_data;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: {lat: -33.865427, lng: 151.196123},
        mapTypeId: 'terrain'
    });

    // Create a <script> tag and set the USGS URL as the source.
    var script = document.createElement('script');

    // This example uses a local copy of the GeoJSON stored at
    // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
    /*
    script.src = 'https://developers.google.com/maps/documentation/javascript/examples/json/earthquake_GeoJSONP.js';
    document.getElementsByTagName('head')[0].appendChild(script);
*/
    map.data.setStyle(function (feature) {
        var magnitude = feature.getProperty('mag');
        return {
            icon: getCircle(magnitude)
        };
    });

    $(document).ready(function () {
        refresh = function () {
            $.ajax({
                // Get the current host, e. i. "hostname:port" format to dynamically change get_game_json base url
                url: "http://" + window.location.host + "/get_game_json",
                dataType: "json",
                async: true,
                cache: false,
                success: async function (data) {
                    // _.isEqual from source:
                    // chovy's comment on accepted solution from
                    // https://stackoverflow.com/questions/201183/how-to-determine-equality-for-two-javascript-objects
                    if (data === null || _.isEqual(last_data, data)) {
                        await sleep(10000);
                    } else {
                        printCities(data);
                        last_data = data;
                    }
                    await sleep(2000);
                    refresh();
                },
                fail: function (jqxhr, textStatus, error) {
                    var err = textStatus + ", " + error;
                    console.log("Request Failed: " + err);
                }
            });
        };
        refresh();
    });
}

// Source: https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function generateGeoJSONCircle(center, radius, numSides) {

    var points = [],
        degreeStep = 360 / numSides;

    for (var i = 0; i < numSides; i++) {
        var gpos = google.maps.geometry.spherical.computeOffset(center, radius, degreeStep * i);
        points.push([gpos.lng(), gpos.lat()]);
    }

    // Duplicate the last point to close the geojson ring
    points.push(points[0]);

    return {
        type: 'Polygon',
        coordinates: [points]
    };
}

function printCities(game_json) {
    var city;
    if (circleMap === undefined) {
        circleMap = new Map();
        for (city in game_json['cities']) {
            if (Object.prototype.hasOwnProperty.call(game_json['cities'], city)) {
                cityCircle = addCircle(game_json['cities'][city]);
                circleMap[city] = cityCircle;
            }
        }
    } else {
        for (city in game_json['cities']) {
            if (Object.prototype.hasOwnProperty.call(game_json['cities'], city)) {
                cityCircle = circleMap[city];
                updateCircle(cityCircle, game_json['cities'][city]);
            }
        }
    }
}

function addCircle(city) {
    // Add the circle for this city to the map.
    var city_prevalence = 0;
    if (city.prevalence !== undefined) {
        city_prevalence = city.prevalence;
    }
    cityCircle = new google.maps.Circle({
        strokeColor: rgbToHex(64, 64, 64),
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: rgbToHex(255, 255 - (city_prevalence * 255), 255 - (city_prevalence * 255)),
        fillOpacity: 0.35,
        map: map,
        center: {lat: city.latitude, lng: city.longitude},
        radius: city.population * 40,
        draggable: false
    });

    return cityCircle;
}

function updateCircle(cityCircle, city) {
    var city_prevalence = 0;
    if (city.prevalence !== undefined) {
        city_prevalence = city.prevalence;
    }
    cityCircle.setOptions({
        fillColor: rgbToHex(255, 255 - (city_prevalence * 255), 255 - (city_prevalence * 255))
    });
    cityCircle.setRadius(city.population * 40);
}

function getCircle(magnitude) {
    return {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: 'red',
        fillOpacity: .2,
        scale: Math.pow(2, magnitude) / 2,
        strokeColor: 'white',
        strokeWeight: .5
    };
}

function eqfeed_callback(results) {
    map.data.addGeoJson(results);
}

// Source: https://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
function rgbToHex(r, g, b) {
    return "#" + ((1 << 24) + (range_rgb(r) << 16) + (range_rgb(g) << 8) + range_rgb(b)).toString(16).slice(1);
}

function range_rgb(x) {
    if (x > 255) {
        return 255;
    }
    if (x < 0) {
        return 0;
    }
    return x;
}