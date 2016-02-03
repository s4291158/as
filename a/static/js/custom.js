getTotalPrice();

function selectChange(ele) {
    var field = getTupleById(ele.id)[1];

    if (ele.id == 'select-type') {
        $('#id_type').val(field);
    } else if (ele.id == 'select-interior') {
        $('#id_interior').val(field)
    }
    getTotalPrice();
}

function getTotalPrice() {
    var price = Number(getTupleById('select-interior')[0]);
    price += Number(getTupleById('select-type')[0]);
    $('#landing_submit').text("$" + price);
}

function getTupleById(id) {
    var tuple = document.getElementById(id).value.replace("$", "").split(/\s{3}/);
    return tuple;
}

