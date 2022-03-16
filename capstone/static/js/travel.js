// Flatpickr "datepicker"
flatpickr("#datepicker", {
    minDate: new Date(),
    dateFormat: "Y-m-d",
    });


$(document).ready(function(){
    $('select').on('change', function(event ) {
        //restore previously selected value
        var prevValue = $(this).data('previous');
        $('select').not(this).find('option[value="'+prevValue+'"]').show();
        //hide option selected                
        var value = $(this).val();
        //update previously selected data
        $(this).data('previous',value);
        $('select').not(this).find('option[value="'+value+'"]').hide();
    });
});

// Get csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function getTime() {
    console.log(csrftoken)
    // Get values from date / destination / departure
    var departureDay = document.getElementById("datepicker").value

    var e = document.getElementById("jsDestination");
    var destination = e.options[e.selectedIndex].text;

    var e2 = document.getElementById("jsDeparture");
    var departure = e2.options[e2.selectedIndex].text;

    // Check if inputs are selected
    if(destination != "Select Destination" && departureDay != "Select Date" && departure != "Select Departure") {

    // Reset error message
    document.getElementById('noTrips').innerHTML = '';

        // Fetch Time
        fetch('get/time', {
    method: 'PUT',
    headers: { 
        'Content-Type': 'application/json',
        "X-CSRFToken": csrftoken }
    ,
    body: JSON.stringify({
        destination: destination,
        departure: departure,
        departureDay: departureDay,
    })
})

    .then(res => res.json())
    .then(data => {

    // If there are no trips available on that day sent a message to user
    if(data.error){
        document.getElementById('noTrips').innerHTML = data.error;
        document.getElementById('noTrips').style.color = "red";
        document.getElementById('noTrips').style.fontSize = "small";
    }

    // Reset time select tag
    document.getElementById('RouteTimes').innerHTML = '<option selected disabled>Choose Time of Departure</option>';

    // Iterate through data and apend each time in the time select tag
    let i = 0
    for(i; i<=data.length; i++){
        const times = document.createElement('option');
        times.innerHTML = data[i].departureTime.slice(0, -3);
        document.getElementById("RouteTimes").append(times)
    }
    
    })
    .catch(error => console.error('Unable to get items.', error));

    }
};

function enableBtn() {
    document.getElementById("submitBtn").disabled = false;
}