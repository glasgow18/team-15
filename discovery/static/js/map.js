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
        });
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }

}
