// template card
var cardHtml = `
<div class="col s12 m12 l6 container-col">
<a href="#CardDetails" class="modal-trigger" data-location="%DATALOCATION%">
    <div class="card white place-card">
        <div class="card-content black-text">
            <span id="loc_name" class="card-title">%TITLE%</span>
            <p>%DESC%</p>
        </div>
        <div class="card-action">
            <div>
                <div>%POSS_ACT%</div>
            </div>

        </div>
    </div>
</a>
</div>
`;

var currentItems = [];
var currentlySelected = null;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


var getSearchBarResponse = function () {
    var searchBox = document.getElementById('search');
    var filter = {'filter': searchBox.value}
    var numItems = 0;
    if (searchBox.value == "") {
        get_original_card_data()
        return
    }
    $.ajax({
        url: "/api/search_bar/",
        type: "POST",
        data: filter
    }).done(function (data) {
        if (data.length > 0) {
            numItems = data.length;
            generate_card_data(data)
        }
        else {
            get_original_card_data()
        }
        $('#selectActivity').val("")
        $("#selectActivity").formSelect()
        $('#selectCategory').val("")
        $("#selectCategory").formSelect()
        document.getElementById("cardCount").innerHTML = "Rows Returned : " + numItems;
    });
};


var getSearchResponse = function () {
    var numItems = 0;

    var selectActivity = parseInt($('#selectActivity').val());
    var selectCategory = parseInt($('#selectCategory').val());
    if ($('#selectActivity').val() == "" && $('#selectCategory').val() == "") {
        get_original_card_data()
        return
    }
    var toSend = {'activity': selectActivity, 'category': selectCategory};
    $.ajax({
        url: "/api/search/",
        type: "POST",
        data: toSend
    }).done(function (data) {
        console.log(data);
        if (data.length > 0) {
            numItems = data.length;
            generate_card_data(data)
        }
        else {
            get_original_card_data()
        }
        document.getElementById("cardCount").innerHTML = "Rows Returned : " + numItems;
    });
};


$(document).ready(function () {

    $('#submitComment').click(function () {
        var locationId = currentlySelected.name;
        $.ajax({
            url: "/api/createcomment/",
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({'name': currentlySelected.name, comment: $('#comment-body').val()})
        }).done(function (data) {
            for (let i = 0; i < data.length; i++) {
                console.log(data[i]['content']);
                $('.comments-list').append("<p>" + data[i]['content'] + "</p>");

            }
        });
    });

    var elems = document.querySelectorAll('.modal');
    M.Modal.init(elems, {
        onOpenStart: function () {
            clearFormData();
        },
        onCloseEnd: function () {
            console.log("same");
        }
    });
    var card = document.querySelectorAll('.CardWrapper');
    M.Modal.init(card, {})


    var fab = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(fab, {});

    $('select').formSelect();


    $('select').change(function () {
        getSearchResponse();
    });

    $('#submitLocationForm').click(function () {
        formData = getFormData($("#locationForm"));
        csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        var numItems = 0;

        $.ajax({
            url: "/api/locations/",
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(formData)
        }).done(function (data) {
            console.log(data);
            if (data.length > 0) {
                numItems = data.length;
                generate_card_data(data)
            }
            else {
                get_original_card_data()
            }
            document.getElementById("cardCount").innerHTML = "Rows Returned : " + numItems;
        });
        console.log(formData)
    });


    $('#submitActivityForm').click(function () {
        console.log(getFormData($("#activityForm")));
    });

    $('#search').keypress(function (e) {
        var key = e.which;
        if (key == 13)  // the enter key code
        {
            getSearchBarResponse();
        }
    });


    get_original_card_data();

    $('#addActivity').click(function () {
        $('#modal1').modal('open');
    });

    $('#addLocation').click(function () {
        $('#modal2').modal('open');
    });

    $('#btnViewMap').click(function () {
        $('#CardWrapper').hide();
        $('#map').show();

        for (let i = 0; i < currentItems.length; i++) {

            let item = currentItems[i];
            if (item.hasOwnProperty('lat') && item.hasOwnProperty('long')) {
                if (item.lat !== null && item.lat !== null && item.long !== null && item.lat !== null) {
                    var marker = new google.maps.Marker({
                        position: {lat: item.lat, lng: item.long},
                        map: map,
                        title: item.name
                    });

                }
            }
        }
    });

    $('#btnViewList').click(function () {
        $('#CardWrapper').show();
        $('#map').hide();
    })


});


function getFormData($form) {
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function clearFormData() {
    $('form').trigger("reset");
}

// Gets location data from backend and displays it in cards
var generate_card_data = function (data) {
    document.getElementById("CardWrapper").innerHTML = "";
    for (let i = 0; i < data.length; i++) {
        var item = data[i];
        var cardWrapper = $("#CardWrapper");
        var curCard = cardHtml.replace("%TITLE%", item.name);
        curCard = curCard.replace("%DESC%", item.description);
        curCard = curCard.replace("%DATALOCATION%", escape(JSON.stringify(item)));
        $(cardWrapper).append(curCard.replace("%POSS_ACT%", item.possibleActivities))
        currentItems.push(item);

    }

    $('.modal-trigger').click(function () {
        var encodedData = $(this).data("location");
        if (encodedData !== null && encodedData !== undefined) {
            var locationData = JSON.parse(unescape(encodedData));

            $('#location-card-title').text(locationData.name);
            $('#location-card-description').text(locationData.description);
            $('#location-activities').text(locationData.possibleActivities)
            currentlySelected = locationData;
            $.ajax({
                url: "/api/locationcomments/",
                type: "POST",
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({'location': locationData.name})
            }).done(function (data) {
                $('.comments-list').empty();
                for (let i = 0; i < data.length; i++) {
                    console.log(data[i]['content']);
                    $('.comments-list').append("<p>" + data[i]['content'] + "</p>");

                }
            });

        }

    });
};

var get_original_card_data = function () {
    $.get('/api/locations', function (data, status) {
        generate_card_data(data)
    })
    document.getElementById("cardCount").innerHTML = ""
};

