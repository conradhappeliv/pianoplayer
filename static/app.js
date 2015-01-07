var playsong = function(element) {
    $.post('start', {"filename": element.innerHTML});
}

$('#start').click(function() {
    $.post('start');
});

$('#stop').click(function() {
    $.post('stop');
});

$(document).ready(function() {
    $.get('getlist', function(data) {
        for(var i = 0; i < data.length; i++) {
            $('#list').prepend('<div class="row"><a href="#" onclick="playsong(this)">'+ data[i] +'</a></div>');
        }
    });
})