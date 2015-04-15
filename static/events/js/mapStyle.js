var miniMarker = {url: '../img/icons/mini_marker.png',
                    /*size: new google.maps.Size(20,32),
				  /*size: new google.maps.Size(36, 46)
				  /*origin: new google.maps.Point(0,0),
				  anchor: new google.maps.Point(0, 32)*/
				  };
var bigMarker = {url: 'pngs/marker.png'};
	  			  
			  
var featureOpts = [
  {
    "featureType": "poi",
    "elementType": "geometry",
    "stylers": [
      { "color": "#e4e2dd" }
    ]
  },{
    "featureType": "poi",
    "elementType": "labels.icon",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "landscape",
    "stylers": [
      { "color": "#e4e2dd" }
    ]
  },{
    "featureType": "administrative",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      { "color": "#a1a1a1" }
    ]
  },{
    "featureType": "road.highway",
    "elementType": "labels.text.stroke",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "road.highway",
    "elementType": "labels.text.fill",
    "stylers": [
      { "color": "#000000" }
    ]
  },{
    "featureType": "road.highway",
    "elementType": "labels.icon",
    "stylers": [
      { "gamma": 0.01 }
    ]
  },{
    "featureType": "road.arterial",
    "elementType": "geometry",
    "stylers": [
      { "color": "#bababa" }
    ]
  },{
    "featureType": "road.arterial",
    "elementType": "labels.text.stroke",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "road.arterial",
    "elementType": "labels.text.fill",
    "stylers": [
      { "color": "#000000" }
    ]
  },{
    "featureType": "road.arterial",
    "elementType": "labels.icon",
    "stylers": [
      { "color": "#626262" }
    ]
  },{
    "featureType": "road.local",
    "elementType": "geometry",
    "stylers": [
      { "color": "#b4b4b4" }
    ]
  },{
    "featureType": "road.local",
    "elementType": "labels.text.stroke",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "road.local",
    "elementType": "labels.text.fill",
    "stylers": [
      { "color": "#000000" }
    ]
  },{
    "featureType": "road.local",
    "elementType": "labels.icon",
    "stylers": [
      { "color": "#5f5f61" }
    ]
  },{
    "featureType": "transit.line",
    "stylers": [
      { "color": "#808080" }
    ]
  },{
    "featureType": "transit.station.bus",
    "stylers": [
      { "gamma": 0.01 }
    ]
  },{
    "featureType": "transit.station.rail",
    "stylers": [
      { "gamma": 0.01 }
    ]
  },{
    "featureType": "transit.station.airport",
    "stylers": [
      { "gamma": 0.01 }
    ]
  },{
    "featureType": "water",
    "stylers": [
      { "color": "#f7f7f9" }
    ]
  },{
    "featureType": "poi.park",
    "elementType": "labels.text",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "poi.place_of_worship",
    "elementType": "labels.text",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "poi.government",
    "elementType": "labels.text.stroke",
    "stylers": [
      { "color": "#008080" },
      { "visibility": "off" }
    ]
  },{
    "featureType": "poi.school",
    "elementType": "labels.text",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "poi.business",
    "elementType": "labels.text",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "poi.medical",
    "elementType": "labels.text",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "road.highway",
    "elementType": "labels.icon",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "road.arterial",
    "elementType": "labels.icon",
    "stylers": [
      { "visibility": "off" }
    ]
  },{
    "featureType": "transit.station.airport",
    "stylers": [
      { "visibility": "off" }
    ]
  }
  ]