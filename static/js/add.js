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
    latitude,
    longitude;

  latitude = parseFloat($(".latitude-input").first().val());
  longitude = parseFloat($(".longitude-input").first().val());
  if (isNaN(latitude) || isNaN(longitude)) {
    // if lat. and long. are blank then we are adding, not editing
    latitude = 37.5;
    longitude = -122.1; 
  }

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

  if (latitude != 37.5 || longitude != -122.1) {
    // add marker for edit mode
    addMarker(latitude, longitude);
  }

  map.addListener('click', function(event) {
    $(".latitude-input").first().val(event.latLng.lat());
    $(".longitude-input").first().val(event.latLng.lng());
    addMarker(event.latLng.lat(), event.latLng.lng());
  });
}

