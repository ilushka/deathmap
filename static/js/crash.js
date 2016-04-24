$(document).ready(function () {
  // Victim add & delete buttons:
  $(".del-victim-btn").click(function (event) {
    event.preventDefault();
    $(this).parents(".victim-form-group").remove();
  });
  $(".add-victim-btn").first().click(function (event) {
    event.preventDefault();
    $(".victim-form-group").first().clone(true).appendTo("#victims-container");
  });

  // Tag add & delete buttons:
  $(".del-tag-btn").click(function (event) {
    event.preventDefault();
    $(this).parents(".tag-form-group").remove();
  });
  $(".add-tag-btn").first().click(function (event) {
    event.preventDefault();
    $(".tag-form-group").first().clone(true).appendTo("#tags-container");
  });

  // Link add & delete buttons:
  $(".del-link-btn").click(function (event) {
    event.preventDefault();
    $(this).parents(".link-form-group").remove();
  });
  $(".add-link-btn").first().click(function (event) {
    event.preventDefault();
    $(".link-form-group").first().clone(true).appendTo("#links-container");
  });

  // Create button:
  $("#create-crash-btn").click(function (event) {
    // Send crash data to server:
    // - Collect victim(s) data
    // - Collect tag(s) data
    // - Collect link(s) data
    // - Collect rest of crash data
    // - POST as JSON

    event.preventDefault();
    var crash = {
          victims: [],
          tags: [],
          links: []
        };

    $(".victim-form-group").each(function() {
      crash.victims.push({
        first: $(this).find(".firstname-input").first().val(),
        last: $(this).find(".lastname-input").first().val(),
        age: parseInt($(this).find(".age-input").first().val()),
      });
    });
    $(".tag-form-group").each(function() {
      crash.tags.push($(this).find(".tag-input").first().val());
    });
    $(".link-form-group").each(function() {
      crash.links.push({
        name: $(this).find(".link-name-input").first().val(),
        link: $(this).find(".link-input").first().val()
      });
    });
    crash.date = $(".date-input").first().val();
    crash.latitude = $(".latitude-input").first().val();
    crash.longitude = $(".longitude-input").first().val();
    crash.city = $(".city-input").first().val();
    crash.state = $(".state-input").first().val();
    crash.zipcode = $(".zipcode-input").first().val();

    $.ajax({
      type: "POST",
      url: window.location.pathname,
      data: JSON.stringify(crash),
      dataType: "json",
      contentType: "application/json",
      success: function() {
        alert("Sent crash data");
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Failed to send crash data " + textStatus + " " + errorThrown);
      }
    });
  });
});

var map, marker = null;
function initMap() {
  var addMarker = function(latitude, longitude) {
      if (marker != null) {
        marker.setMap(null);
      }
      marker = new google.maps.Marker({
        position: { lat: latitude, lng: longitude },
        map: map
      });
    },
    latitude, longitude,
    // create search box
    searchInput = $(".search-input").get(0),
    searchBox = new google.maps.places.SearchBox(searchInput),
    geocoder = new google.maps.Geocoder;

  // process lat & long
  latitude = parseFloat($(".latitude-input").first().val());
  longitude = parseFloat($(".longitude-input").first().val());
  if (isNaN(latitude) || isNaN(longitude)) {
    // if lat. and long. are blank then we are adding, not editing
    latitude = 37.5;
    longitude = -122.1; 
  }

  // create map
  map = new google.maps.Map(document.getElementById("map"), {
    center: {
      lat: latitude,
      lng: longitude
    },
    zoom: 14,
    panControl: false,
    zoomControl: false,
    mapTypeControl: false,
    scaleControl: false,
    streetViewControl: false,
    overviewMapControl: false
  });

  // initialize places web service
  placesService = new google.maps.places.PlacesService(map);

  // add search box listener
  searchBox.addListener("places_changed", function() {
    var places = searchBox.getPlaces();
    if (places.length != 0) {
      map.panTo(places[0].geometry.location);
    }
  });

  if (latitude != 37.5 || longitude != -122.1) {
    // add marker for edit mode
    addMarker(latitude, longitude);
  }

  // listener for clicking on map
  map.addListener('click', function(event) {
    var lat = event.latLng.lat(),
        lng = event.latLng.lng(),
        latLng = {lat: lat, lng: lng};

    $(".latitude-input").first().val(lat);
    $(".longitude-input").first().val(lng);
    addMarker(lat, lng);

    // retrieve info for the coordinates
    geocoder.geocode( {"location": latLng}, function(results, status) {
      var attrb = null,
          type = null,
          place = null,
          city = null,
          zipcode = null,
          state = null;

      if (results.length != 0) {
        place = results[0];
        for (var ii = 0; ii < place.address_components.length; ii++) {
          attrb = place.address_components[ii];
          for (var jj = 0; jj < attrb.types.length; jj++) {
            type = attrb.types[jj];

            if (!type.localeCompare("postal_code")) {
              zipcode = attrb.long_name;
            } else if (!type.localeCompare("locality")) {
              city = attrb.long_name;
            } else if (!type.localeCompare("administrative_area_level_1")) {
              state = attrb.short_name;
            } else if (!type.localeCompare("sublocality_level_1")) {
              if (city == null) {
                city = attrb.long_name;
              }
            } 

            $(".zipcode-input").first().val(zipcode);
            $(".city-input").first().val(city);
            $(".state-input").first().val(state);
          }
        }
      } // if (results.length != 0)
    });
  });
}

