//Declare the stations
var stations = [
      ['South Station', 42.352271 , -71.05524200000001, 1,'place-sstat'],
      ['Andrew', 42.330154, -71.057655, 2,'place-andrw'],
      ['Porter Square', 42.3884, -71.11914899999999, 3,'place-portr'],
      ['Harvard Square', 42.373362, -71.118956, 4,'place-harsq'],
      ['JFK/UMass', 42.320685, -71.052391, 5,'place-jfk'],
      ['Savin Hill', 42.31129, -71.053331, 6,'place-shmnl'],
      ['Park Street', 42.35639457, -71.0624242, 7,'place-pktrm'],
      ['Broadway', 42.342622, -71.056967, 8,'place-brdwy'],
      ['North Quincy', 42.275275, -71.029583, 9,'place-nqncy'],
      ['Shawmut', 42.29312583, -71.06573796000001, 10,'place-smmnl'],
      ['Davis', 42.39674, -71.121815, 11,'place-davis'],
      ['Alewife', 42.395428, -71.142483, 12,'place-alfcl'],
      ['Kendall/MIT', 42.36249079, -71.08617653, 13,'place-knncl'],
      ['Charles/MGH', 42.361166, -71.070628, 14,'place-chmnl'],
      ['Downtown Crossing', 42.355518, -71.060225, 15,'place-dwnxg'],
      ['Quincy Center', 42.251809, -71.005409, 16,'place-qnctr'],
      ['Quincy Adams', 42.233391, -71.007153, 17,'place-qamnl'],
      ['Ashmont', 42.284652, -71.06448899999999, 18,'place-asmnl'],
      ['Wollaston', 42.2665139, -71.0203369, 19,'place-wlsta'],
      ['Fields Corner', 42.300093, -71.061667, 20,'place-fldcr'],
      ['Central Square', 42.365486, -71.103802, 21,'place-cntsq'],
      ['Braintree', 42.2078543, -71.0011385, 22,'place-brntn']
    ]; 

// Main callback function that renders map and makes calls to other functions that: 
// 1. Renders polyline
// 2. Creates markers
// 3. Locates user via navigator geolocation object
function initMap() {
          var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 14,
            center: {lat: 42.352271, lng: -71.05524200000001},
            mapTypeId: 'terrain'
          });       
          setpolyline(map);
          setMarkers(map);
          locate_me(map);
}

// Function that locates the user
function locate_me(map) {
        // Function to determine closest station
        function get_station_distance(lat, long) {
          var closest_distance = 1000000;
          var station_distances = [];
          var closest_station = ['nowhere', 0];
          for (var i = 0; i < stations.length; i++) {
              var curr_distance = google.maps.geometry.spherical.computeDistanceBetween(new google.maps.LatLng(lat, long), new google.maps.LatLng(stations[i][1], stations[i][2]));
              if (curr_distance < closest_distance) {
                closest_distance = curr_distance;
                closest_station[0] = stations[i];
              }
            }
          closest_station[1] = (closest_distance * 0.621371 * 0.001);  
          return closest_station;
         }
        
        // Steps to determine location and add marker
        var options = {
          enableHighAccuracy: false,
          timeout: 30000,
          maximumAge: 0
          };

        // Success function implements all equatiosn related to self
        function success(position) {
              var crd = position.coords;
              lat = position.coords.latitude;
              long = position.coords.longitude;
              map.setCenter(new google.maps.LatLng(lat,long));
              var loc_marker = new google.maps.Marker({
                      position: {lat:lat,lng:long},
                      map: map,
                      title: "You're here"
              });

              // Retrieves closest station
              var closest_station = get_station_distance(lat, long);
              loc_marker.addListener('click', function() {
              // Opens infowindow for loc_marker that shows where. 
              var nearest_train = new google.maps.InfoWindow({
                  content: '<h2>Nearest station is: </h2>' + closest_station[0][0] + '<h2>Distance from you: </h2>' +'<p>' + closest_station[1] + ' miles</p>'
                });
              nearest_train.open(map,loc_marker); 
                });

              // Draws polyline between marker and closest station
              var closest_path = new google.maps.Polyline({
                path: [{lat: closest_station[0][1], lng:closest_station[0][2]},{lat:lat, lng:long}],
                geodesic: true,
                strokeColor: '#0000A0',
                strokeOpacity: 1.0,
                strokeWeight: 2
              });
              closest_path.setMap(map);
          }
          function error(err) {
              console.warn(`ERROR(${err.code}): ${err.message}`);
          }
          navigator.geolocation.getCurrentPosition(success, error, options);
}

// Function that sets the polyline
function setpolyline (map) {
          // Script for the polyline
          var flightPlanCoordinates = [
            {lat: stations[11][1], lng: stations[11][2]}, {lat: stations[10][1], lng: stations[10][2]}, {lat: stations[2][1], lng: stations[2][2]},
            {lat: stations[3][1], lng: stations[3][2]}, {lat: stations[20][1], lng: stations[20][2]}, {lat: stations[12][1], lng: stations[12][2]},
            {lat: stations[13][1], lng: stations[13][2]}, {lat: stations[6][1], lng: stations[6][2]}, {lat: stations[14][1], lng: stations[14][2]},
            {lat: stations[0][1], lng: stations[0][2]}, {lat: stations[7][1], lng: stations[7][2]}, {lat: stations[1][1], lng: stations[1][2]},
            {lat: stations[4][1], lng: stations[4][2]},
            // Up to JFK/UMASS
            {lat: stations[8][1], lng: stations[8][2]}, {lat: stations[18][1], lng: stations[18][2]}, {lat: stations[15][1], lng: stations[15][2]},
            {lat: stations[16][1], lng: stations[16][2]}, {lat: stations[21][1], lng: stations[21][2]},
            // Going back up to JFK UMASS
            {lat: stations[16][1], lng: stations[16][2]}, {lat: stations[15][1], lng: stations[15][2]}, {lat: stations[18][1], lng: stations[18][2]},
            {lat: stations[8][1], lng: stations[8][2]}, {lat: stations[4][1], lng: stations[4][2]},

            // End of one fork
            {lat: stations[5][1], lng: stations[5][2]}, {lat: stations[19][1], lng: stations[19][2]}, {lat: stations[9][1], lng: stations[9][2]},
            {lat: stations[17][1], lng: stations[17][2]},
          ];

          var flightPath = new google.maps.Polyline({
            path: flightPlanCoordinates,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2
          });

          flightPath.setMap(map);
}


// Functiont that sets the train markers
function setMarkers(map) {
          var icon = {
              url: "MBTA.png",
              scaledSize: new google.maps.Size(20, 20), 
              origin: new google.maps.Point(0,0),
              anchor: new google.maps.Point(0,0) 
          };
          var shape = {
            coords: [1, 1, 1, 20, 18, 20, 18, 1],
            type: 'poly'
          };
          for (var i = 0; i < stations.length; i++) {
            var station = stations[i];
            var marker = new google.maps.Marker({
              position: {lat: station[1], lng: station[2]},
              map: map,
              icon: icon,
              shape: shape,
              title: station[0],
              zIndex: station[3]
            });
            // Passed into function for closure
            pass_into_listener(station, marker);
          }
}

// Function that renders infowindow when marker is clicked
function makeinfowindow(station, curr_mark) {
          var link = "https://chicken-of-the-sea.herokuapp.com/redline/schedule.json?stop_id=" + station[4];
          var request = new XMLHttpRequest();
          request.open('GET', link, true);
          request.send();
          request.onreadystatechange = function() {
              if (request.readyState == 4 && request.status == 200) {
                  data = request.responseText;
                  station_data = JSON.parse(data);
                  var info_w = new google.maps.InfoWindow();
                  info_w.setContent(getTimes(station_data,station[0]));
                  info_w.open(map,curr_mark);
              }
          }
}

function pass_into_listener(station, marker) {
          google.maps.event.addListener(marker, 'click', function() {
          makeinfowindow(station, marker);
          });
 }

function getTimes(station_data, station_name) {
          var time = '<h1>Sorry, station data not available </h1>';
          // Checks for wollaston edge case: 
          if (station_data.data.length == 0) {
            return time;
          }
          // gets 4 latest schedules
          var arrive;
          var depart;
          var trains = [[0,0],[0,0],['TBD','TBD'],['TBD','TBD']];
          var direction = ['Unavailable', 'Unavailable', 'Unavailable', 'Unavailable'];
          for (var i = 0; i < 4; i++) {
            if (i == station_data.data.length) {
              break;
            }
            else {
              arrive = station_data.data[i].attributes.arrival_time;
              depart = station_data.data[i].attributes.departure_time;
              if (arrive != null && depart != null) {
                arrive = arrive.substring(11,16);
                trains[i][0] = arrive;
                depart = depart.substring(11,16);
                trains[i][1] = depart;
              }
              else if (arrive == null && depart != null) {
                trains[i][0] = 'Not available';
                depart = depart.substring(11,16);
                trains[i][1] = depart;
              }
              else if (depart == null && arrive != null) {
                arrive = arrive.substring(11,16);
                trains[i][0] = arrive;
                trains[i][1] = 'Not available';
              }  
              else {
                  trains[i][0] = 'Not available'; 
                  trains[i][1] = 'Not available'; 
              }
            }
          }
          for (var i = 0; i < 4; i++) {
            if (station_data.data[i].attributes.direction_id == '0')
              direction[i] = 'Southbound (to Ashmont/Braintree)';
            else 
              direction[i] = 'Northbound (to Alewife)';
          }
          time = '<h1> Station: ' + station_name + '</h1>' + '<table>' + '<tr>' + '<th> Arrival time</th>' + '<th> Departure time</th>' + '<th> Direction</th>' + '</tr>' +
                '<tr>' + '<td>' + trains[0][0] + '</td>' + '<td>' + trains[0][1] + '</td>' + '<td>' + direction[0] + '</td>' + 
                '<tr>' + '<td>' + trains[1][0] + '</td>' + '<td>' + trains[1][1] + '</td>' + '<td>' + direction[1] + '</td>' + 
                '<tr>' + '<td>' + trains[2][0] + '</td>' + '<td>' + trains[2][1] + '</td>' + '<td>' + direction[2] + '</td>' + 
                '<tr>' + '<td>' + trains[3][0] + '</td>' + '<td>' + trains[3][1] + '</td>' + '<td>' + direction[3] + '</td>' + '</table>';
          return time;
}





