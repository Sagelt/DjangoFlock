function decimal_to_minutes(min) {
    var min = min * 60;
    if (min < 10) {
        min = "0" + min;
    }
    return min;
}
function split_hours_and_minutes(time) {
    var h = parseInt(time);
    var m = time - h;
    return Array(h, m);
}
function format_time(hour) {
    if (hour < 12) {
        minute = decimal_to_minutes(hour - parseInt(hour));
        hour = parseInt(hour);
        return hour + ":" + minute + "am";
    } else {
        hour = hour - 12;
        minute = decimal_to_minutes(hour - parseInt(hour));
        hour = parseInt(hour);
        if (hour == 0) {
            hour = 12;
        }
        return hour + ":" + minute + "pm";
    }
}
function set_amount_and_hidden_fields() {
	var start = new Date($('#id_day').val().split('-'));
	var start_time = parseFloat($("#duration").slider("values", 0));
	var start_hours_minutes = split_hours_and_minutes(start_time);
	start.setHours(start_hours_minutes[0]);
	start.setMinutes(start_hours_minutes[1] * 60);
	var start_total = $("#id_day").val() + " " + start.getHours() + ":";
	var start_min = start.getMinutes();
	if (start_min < 10) {
		start_min = "0" + start_min;
	}
	start_total += start_min;
	$("#id_start").val(start_total);

	var end = new Date($('#id_day').val().split('-'));
	var end_time = parseFloat($("#duration").slider("values", 1));
	var end_hours_minutes = split_hours_and_minutes(end_time);
	end.setHours(end_hours_minutes[0]);
	end.setMinutes(end_hours_minutes[1] * 60);
	var end_total = $("#id_day").val() + " " + end.getHours() + ":";
	var end_min = end.getMinutes();
	if (end_min < 10) {
		end_min = "0" + end_min;
	}
	end_total += end_min;
	$("#id_end").val(end_total);
	
	$("#amount").text(format_time($("#duration").slider("values", 0)) + " to " + format_time($("#duration").slider("values", 1)) + " (" + (end_time - start_time) + " hours).");
}
$(function(){
	$('#id_start, #id_end').hide()
    $('#id_day').datepicker({
        dateFormat: 'yy-mm-dd',
        defaultDate: 0
    });
	$('#id_day').datepicker("setDate", new Date($("#id_day").val()));
    $('#duration').slider({
        range: true,
        min: 0,
        max: 24,
        values: [14, 16],
        step: 0.5,
        slide: set_amount_and_hidden_fields
    });
    set_amount_and_hidden_fields();
});