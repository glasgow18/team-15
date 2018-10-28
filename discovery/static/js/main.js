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
});

var getSearchResponse = function () {

    var selectActivity = parseInt($('#selectActivity').val());
    var selectCategory = parseInt($('#selectCategory').val());

    var toSend = {'activity': selectActivity, 'category': selectCategory};
    console.log(toSend);
    $.ajax({
        url: "/api/search/",
        type: "POST",
        data: toSend
    }).done(function(data) {
        console.log(data);
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