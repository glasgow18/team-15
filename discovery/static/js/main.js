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

//
// $('modal1').modal.options.onOpenStart=clearFormData();

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