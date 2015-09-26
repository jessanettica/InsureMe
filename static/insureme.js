////////////////////////////////////////////////////
// Event Listeners

$('.distance').on('input', syncDistanceValues);
$('#search-btn').on('click', postLocation);


////////////////////////////////////////////////////
// Goople Maps Autocomplete 

var address = document.getElementById('address');
var options = {
    types: ['address'] 
};
// Add autocomplete to the text boxes
var autocomplete_address = new google.maps.places.Autocomplete(address, options);


////////////////////////////////////////////////////
// Functions

function syncDistanceValues(evt) {
    var value = $(this).val();
    $('.distance').val(value);
}

function postLocation() {

    var locationData = {
        address: $('#address').val(),
        radius: $('#distance').val()
    };

    $.post('/locate', locationData, function(response) {

    	// This is where we update the D3

    });
}