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

 // Flatpickr "datepicker"
 flatpickr("#datepicker", {
    minDate: new Date(),
    dateFormat: "Y, m, d",
    });

flatpickr("#timepicker", {
enableTime: true,
noCalendar: true,
dateFormat: "H:i",
time_24hr: true
});