var map;
function initMap() {
  map = new google.maps.Map(
    document.getElementById("map"),
    {
      center: { lat: 37.5, lng: -122.1 },
      zoom: 9,
      panControl: false,
      zoomControl: false,
      mapTypeControl: false,
      scaleControl: false,
      streetViewControl: false,
      overviewMapControl: false,
      styles: [{
        stylers: [
          { saturation: -100 }, // -100 to 100
          { gamma: 0.8 },       // 0.01 to 10.0
          { lightness: -10 }    // -100 to 100
        ]
      }]
    });

  var buildInfoWindowContent = function(crash) {
    var content = $("<div></div>"),
        victims = crash.victims.reduce(
            function(prev, curr) {
              return prev + curr.first + " " + curr.last + " (" + curr.age + "), "; 
            },
            "")
          .slice(0, -2),
        links = crash.links.reduce(
            function(prev, curr, index) {
              return prev +
                $("<a />", {
                  text: index + 1,
                  href: curr.link,
                  target: "_blank"
                }).prop("outerHTML") + 
                ", ";
            },
            "")
          .slice(0, -2),
        tags = crash.tags.reduce(
            function(prev, curr) {
            return prev + curr + ", ";
            },
            "")
          .slice(0, -2);
    content.append("<b>Victims:</b> " + victims + "<br />");
    content.append("<b>Date:</b> " + crash.date + "<br />");
    content.append("<b>Links:</b> " + links + "<br />");
    content.append("<b>Tags:</b> " + tags + "<br />");
    return content.prop("outerHTML");
  };

  // map icon 
  var icon = new google.maps.MarkerImage("static/img/dot.png", null, null,
                                         null, new google.maps.Size(11, 11));
  $.ajax({url: "/crash/all/json"})
    .done(function(crashes) {
      var infowindow = new google.maps.InfoWindow();
      for (var ii = 0; ii < crashes.length; ++ii) {
        var crash = crashes[ii],
            marker = new google.maps.Marker({
              position: { lat: crash.latitude, lng: crash.longitude },
              map: map,
              title: crash.victims[0].first,
              crash: crash,
              icon: icon
            });

        marker.addListener("click",
          (function(_map, _marker) {
              return function() { 
                infowindow.setContent(buildInfoWindowContent(this.crash));
                infowindow.open(_map, _marker);
              };
            })(map, marker));
      }
    });
}

