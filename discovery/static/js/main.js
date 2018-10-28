// template card
var cardHtml = `
<div class="col s12 m12 l6 container-col">
<a href="#CardDetails" class="modal-trigger">
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

document.addEventListener('DOMContentLoaded', function () {
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
});

$("#CardDetails").click(function (){

});

var getSearchResponse = function () {

    var numItems = 0;

    var selectActivity = parseInt($('#selectActivity').val());
    var selectCategory = parseInt($('#selectCategory').val());

    if(selectCategory == NaN && selectActivity == NaN){
        document.getElementById("cardCount").innerHTML = "Rows:"+ numItems;
        $.get('/api/locations', function (data, status) {
        for (let i = 0; i < data.length; i++) {
            var item = data[i];
            var cardWrapper = $("#CardWrapper");
            var curCard = cardHtml.replace("%TITLE%", item.name)
            curCard = curCard.replace("%DESC%", item.description)
            $(cardWrapper).append(curCard.replace("%POSS_ACT%", item.possibleActivities))
        }
        return;
    })
    }

    var toSend = {'activity': selectActivity, 'category': selectCategory};
    $.ajax({
        url: "/api/search/",
        type: "POST",
        data: toSend
    }).done(function(data) {
        console.log(data);
        if(data.length>0) {
            document.getElementById("CardWrapper").innerHTML = "";
            numItems=0;
            for (let i = 0; i < data.length; i++) {
                console.log(data[i])
                var item = data[i];
                var cardWrapper = $("#CardWrapper");
                var curCard = cardHtml.replace("%TITLE%", item.name)
                curCard = curCard.replace("%DESC%", item.description)
                $(cardWrapper).append(curCard.replace("%POSS_ACT%", item.possibleActivities))
                numItems++;
            }
        }
    });
};

$(document).ready(function () {
    $('select').formSelect();


    $('select').change(function() {
        getSearchResponse();



    });

    $('#submitLocationForm').click(function () {
        console.log(getFormData($("#locationForm")));
    });
    $('#submitActivityForm').click(function () {
        console.log(getFormData($("#activityForm")));
    });
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

$(document).ready(function () {
    $.get('/api/locations', function (data, status) {
        for (let i = 0; i < data.length; i++) {
            var item = data[i];
            var cardWrapper = $("#CardWrapper");
            var curCard = cardHtml.replace("%TITLE%", item.name)
            curCard = curCard.replace("%DESC%", item.description)
            $(cardWrapper).append(curCard.replace("%POSS_ACT%", item.possibleActivities))
        }
    })


    $('#addActivity').click(function() {
        $('#modal1').modal('open');
    });

    $('#addLocation').click(function() {
        $('#modal2').modal('open');
    });

    $('#btnViewMap').click(function() {
       $('#CardWrapper').hide();
       $('#map').show();
    });

});
