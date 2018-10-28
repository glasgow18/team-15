function getLocation() {

}


var map;

function initMap() {

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: position.coords.latitude, lng: position.coords.longitude},
                zoom: 13
            });

            var mkr = new google.maps.Marker({
                position: {lat: position.coords.latitude, lng: position.coords.longitude},
                map: map,
                title: "My Location",
                icon: "/static/img/location_icon.png"
            });
        });





    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }

}
