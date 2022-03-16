// Disable submit button
document.getElementById("seatButton").disabled = true;

function saveSeat(button) {
    if(
        // Reset button color on click
        button.style.backgroundColor == "aqua"){
        button.style.backgroundColor = "";
        document.getElementById(`${button.innerHTML}`).remove();

        // Change price
        document.getElementById("ticketsPrice").innerHTML -= 15;

        // Disable submit button
        if(document.getElementById("hiddenTickets").innerHTML == ''){
            document.getElementById("seatButton").disabled = true;
        }
    }else{
        // Change button color on click
        button.style.backgroundColor = "aqua";

        // Create a hidden input for seats
        const tickets =document.createElement('input');
        tickets.type = "hidden";
        tickets.value = button.innerHTML;
        tickets.id = tickets.value;
        // Set the name of hidden input
        tickets.name = button.innerHTML;
        document.getElementById("hiddenTickets").append(tickets)

        // Change price
        let parse = document.getElementById("ticketsPrice").innerHTML
        let parsed = parseInt(parse) + 15;
        document.getElementById("ticketsPrice").innerHTML = parsed;
        
        // Enable submit button
        document.getElementById("seatButton").disabled = false;
    }
}