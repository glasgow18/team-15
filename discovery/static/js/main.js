// template card
var cardHtml = `
  <a href="#CardDetails" class="modal-trigger">
        <div class="row">
            <div class="col s12 m6">
                    <div class="card white">
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
            </div>
        </div>
    </a>
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
});

$(document).ready(function () {
    $('#submitLocationForm').click(function () {
        console.log(getFormData($("#locationForm")));
    });
});

$(document).ready(function () {
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
});
