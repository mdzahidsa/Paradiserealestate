
function initAutoComplete(){
    initialize();
    myMap();
}
let autocomplete;

function initialize(){
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: {'country': ['in','qa','ie','ae']},
        })
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
    
}

function myMap(){
    var defaultLatLng = { lat: 51.508742, lng: -0.120850 }; // Default coordinates
    var mapProp = {
      center: defaultLatLng,
      zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    var latitude = parseFloat(document.getElementById("latitude").value);
    var longitude = parseFloat(document.getElementById("longitude").value);

    if (!isNaN(latitude) && !isNaN(longitude)) {
      var markerLatLng = { lat: latitude, lng: longitude };
      var marker = new google.maps.Marker({
        position: markerLatLng,
        map: map,
      });

      map.setCenter(markerLatLng);
      map.setZoom(18);
    }
  }

  // Call the initMap function when the page loads
  google.maps.event.addDomListener(window, "load", initMap);

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
   //     console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
   // console.log(place);
   var geocoder = new google.maps.Geocoder()
   var address = document.getElementById('id_address').value
   geocoder.geocode({'address': address}, function(results, status){
       // console.log('results=>',results)
      //  console.log('status=>',status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

           // console.log('lat=>', latitude);
          //  console.log('long=>', longitude);
          $('#id_latitude').val(latitude);
          $('#id_longitude').val(longitude);
          $('#id_address').val(address);
        }
   });
   //address components loop
   for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            //get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            //get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            //get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }
            else
            {
                $('#id_pin_code').val("");   
            }

        }
   }

   console.log(place.address_components);


}

