/**
 * Created by stas on 30.08.16.
 */
String.prototype.splice = function (idx, rem, str) {
    return this.slice(0, idx) + str + this.slice(idx + Math.abs(rem));
};

function refactor_phone(val) {
    val = val.replace(/[^0-9\.]/g, '');

    if (val[0] !== '+') {
        val = '+' + val;
    }
    if (val.length >= 3) {
        val = val.splice(3, 0, ' (');
    }
    if (val.length >= 8) {
        val = val.splice(8, 0, ') ');
    }
    if (val.length >= 13) {
        val = val.splice(13, 0, ' ');
    }
    if (val.length >= 16) {
        val = val.splice(16, 0, ' ');
    }
    return val;
}

function refactor_phone_backspace(val) {
    if (val.slice(-1) === ' ') {
        val = val.substring(0, val.length - 1)
    }
    if (val.slice(-1) === ')') {
        val = val.substring(0, val.length - 1)
    }
    if (val.slice(-2) === ' (') {
        val = val.substring(0, val.length - 2)
    }
    if (val === '+') {
        val = '';
    }
    return val;
}

$('input[id$=phone]').keyup(function (e) {
    var code = e.which;
    if (code !== 8) {
        var val = this.value;
        this.value = refactor_phone(val);
    } else {
        var val = this.value;
        this.value = refactor_phone_backspace(val);
    }
});


$(document).ready(function () {
    var phones = $('input[id$=phone]');
    for (var i = 0; i < phones.length; i++) {
        if (phones[i].value !== '') {
            phones[i].value = refactor_phone(phones[i].value);
        }
    }
});