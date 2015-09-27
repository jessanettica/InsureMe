////////////////////////////////////////////////////
// Event Listeners

$('.distance').on('input', syncDistanceValues);
$('#search-btn').on('click', postLocation);
$(document).ready(autocomplete);

////////////////////////////////////////////////////
// Functions

function syncDistanceValues() {
    var value = $(this).val();
    $('span.distance').text(value);
}

function postLocation() {

    var locationData = {
        address: $('#address').val(),
        radius: $('#distance').val()
    };

    $.ajax({
        url: '/locate',
        method: 'POST',
        data: locationData,
        success: getD3,
        error: function () { alert("An Error Occurred in postLocation") }
    });

}


function getD3() {

    $.ajax({
        url: '/get_d3',
        error: function() { alert( "An Error Occurred in getD3" ); }
    });

}


////////////////////////////////////////////////////
// Goople Maps Autocomplete 


function autocomplete() {
    var address = document.getElementById('address');
    var options = {
        types: ['address'] 
    };
    // Add autocomplete to the text boxes
    var autocomplete_address = new google.maps.places.Autocomplete(address, options);
}
