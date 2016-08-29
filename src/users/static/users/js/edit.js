/**
 * Created by stas on 30.08.16.
 */
function constructSelect() {

    $('#id_selector_row').css('display', 'block');

    $('#id_course_select option').remove();
    var count = 0;
    for (var id in courses) {
        if (!courses[id].isOnList) {
            count += 1;
            $('#id_course_select').append('<option value="' + id + '">' + courses[id].name + '</option>');
        }
    }
    if (count == 0) {
        $('#id_selector_row').css('display', 'none');
    }
}

function constructTable() {
    $('#id_course_table tr').remove();
    for (var id in courses) {
        if (courses[id].isOnList) {
            $('#id_course_table').append('<tr><td>' + courses[id].name + '</td><td><div class="text-right"><div role="button" id="remove_' + id + '"><i class="glyphicon glyphicon-remove-circle"></i></div></div></td></tr>');
            $('#remove_' + id).click(function (id) {
                thisID = $(this).attr('id').split('remove_')[1];
                courses[thisID].isOnList = false;
                constructSelect();
                constructTable();
                updateHiddenInput();
            });
        }
    }

}

function updateHiddenInput() {
    var courseList = '';
    for (var id in courses) {
        if (courses[id].isOnList) {
            if (courseList !== '') {
                courseList += '&' + String(id);
            } else {
                courseList = String(id);
            }
        }
    }
    $('#id_courses').val(courseList);
}

$('#id_course_button').click(function () {
    var id = $('#id_course_select').find(":selected").val();
    console.log(id);
    courses[id].isOnList = true;
    constructTable();
    constructSelect();
    updateHiddenInput();
});