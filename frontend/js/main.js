// Main callback function that renders map and makes calls to other functions that: 
// 1. Renders polyline
// 2. Creates markers
// 3. Locates user via navigator geolocation object
// var map = initMap(map)

var map;

function initMap() {
          map = new google.maps.Map(document.getElementById('map'), {
            zoom: 14,
            center: {lat: 42.352271, lng: -71.05524200000001},
            mapTypeId: 'terrain'
          });       
          // setpolyline(map);
          // setMarkers(map);
          locate_me(map);
        //   _this.data
        //   searchButton = document.getElementById('Submit')
        //   searchButton.addEventListener('click', function(map){
        //     searchJobs(map)
        //   })
        //   return(map)
}

// ******** DETERMINE CURRENT LOCATION ********

// Function that locates the user
function locate_me(map) {
        // Optional parameter for navigator.geolocation call
        var options = {
          enableHighAccuracy: false,
          timeout: 30000,
          maximumAge: 0
          };

        // Call to geolocation API to determine obtain current coordinates
        navigator.geolocation.getCurrentPosition(success, error, options);   

        // Success function implements all equations related to self
        function success(position) {
                var crd = position.coords;
                lat = position.coords.latitude;
                long = position.coords.longitude;
                map.setCenter(new google.maps.LatLng(lat,long));
                // console.log(lat, long)
                var loc_marker = new google.maps.Marker({
                        position: {lat:lat,lng:long},
                        map: map,
                        title: "You're here"
                });
              }

        // Catches errors and prints to console. 
        function error(err) {
                console.warn(`ERROR(${err.code}): ${err.message}`);
              }     
      }


// ******** MAKES API CALL BASED ON search ********

//Called when user clicks search button
function searchJobs() {
    jobTitle = d3.select("#Title").property("value");
    jobLocation = d3.select("#Location").property("value");
    jobRadius = d3.select("#SearchRadius").property("value");
    console.log(jobTitle, jobLocation, jobRadius)
    makeSeleniumCall(jobTitle, jobLocation, jobRadius)
}


// Functiont that sets the train markers
function setMarkers(map, company_data) {
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
        
        // map.setCenter(new google.maps.LatLng(company_data["center"]["Lat"],["center"]["Lng"]));
        //   num_jobs = Object.keys(company_data).length
        for (var i = 0; i < Object.keys(company_data).length; i++) {
            // console.log("Title:" + company_data[i]["Title"])
            // console.log("Lat:" + company_data[i]["Lat"], "Lng:" + company_data[i].Lng)
            var station = company_data.Title;
            var marker = new google.maps.Marker({
              position: {lat: company_data[i].Lat, lng: company_data[i].Lng},
              map: map,
            //   icon: icon,
            //   shape: shape,
              title: company_data[i].Title,
            });
            // Passed into function for closure
            pass_into_listener(company_data[i], marker);
        }
}

// Function that renders infowindow when marker is clicked
function makeSeleniumCall(jobTitle, jobLocation, jobRadius) {
    // Temp link
    var link = d3.select("#Link").property("value") + "?title=" + jobTitle + "&loc=" + jobLocation + "&rad=" + jobRadius
    // var link = "https://chicken-of-the-sea.herokuapp.com/redline/schedule.json?stop_id=" + station[4];
    var request = new XMLHttpRequest();
    request.open('GET', link, true);
    request.send();
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 201) {
            data = request.responseText;
            console.log("Got Data, now parsing")
            company_data = JSON.parse(JSON.parse(data));
            // print("Length is: " + company_data.length)
            // console.log(company_data)
            // console.log(company_data)
            // console.log(Object.keys(company_data))
            // ***** Makes call to centralize Map View
            APIkey = "***API KEY***"
            gmapsLink = "https://maps.googleapis.com/maps/api/geocode/json?address=" + jobLocation + "&key=" + APIkey
            console.log(gmapsLink)
            centralize = new XMLHttpRequest();
            centralize.open ('GET', gmapsLink, true);
            centralize.send();
            centralize.onreadystatechange =function() {
                if (centralize.readyState == 4 && centralize.status >= 200 && centralize.status < 210) {
                    mapsData = centralize.responseText;
                    console.log("Got GMaps Data!!!!, Data is:")
                    console.log(mapsData);
                    gmaps_data = JSON.parse(mapsData);
                    console.log(gmaps_data);
                    var updatedLat = gmaps_data["results"][0]['geometry']['location']["lat"];
                    var updatedLng = gmaps_data["results"][0]['geometry']['location']["lng"];
                    map.setCenter(new google.maps.LatLng(updatedLat,updatedLng));
                    map.setZoom(11);
                }
                if (centralize.readyState != 4 || (centralize.status < 200 || centralize.status > 210)) {
                    console.log(centralize.readyState, centralize.status)
                    console.log("Fetching Gmaps data...")
                }
            }
            // centerCoords =function()
            // *****

            setMarkers(map, company_data)
            // var info_w = new google.maps.InfoWindow();
            // info_w.setContent(getTimes(station_data,station[0]));
            // info_w.open(map,curr_mark);
        }
        if (request.readyState != 4 || request.status != 201) {
            console.log("Fetching data...")
            // var info_w = new google.maps.InfoWindow();
            // info_w.setContent(getTimes(station_data,station[0]));
            // info_w.open(map,curr_mark);
        }
    }
}

// Add event listener for markers
function pass_into_listener(station, marker) {
    google.maps.event.addListener(marker, 'click', function() {
    makeinfowindow(station, marker);
    });
 }

// Helper function to generate info window for marker
function makeinfowindow(station, marker) {
    var info_w = new google.maps.InfoWindow();
        var detailedInfo = '<h1><b>Posting</b>: ' + station["Title"] + '</h1>' + '<h1><b>Company<b/>: ' + station["Company"] + '</h1>'
                        + '<h1><b>Description</b>: ' + station["Description"] + '</h1>' + '<h1><b>Link<b/>: ' + station["Link"] + '</h1>';
        info_w.setContent(detailedInfo);
        // getTimes method: 
        info_w.open(map,marker);
}

// Helper function to centralize Google Maps View
// function centralize()
