function selectChangeLanding(ele) {
    selectChange(ele);
    getTotalPriceLanding();
}

function selectChangeBooking(ele) {
    selectChange(ele)
    getTotalPrice();
}

function selectChange(ele) {
    var field = getTupleById(ele.id)[1];

    if (ele.id == 'select-type') {
        $('#id_type_field').val(field);
    } else if (ele.id == 'select-interior') {
        $('#id_interior_field').val(field)
    } else if (ele.id == 'select-extra-dirty') {
        if (field == 'Yes') {
            $('#id_extra_dirty_field').val('True')
        } else if (field == 'No') {
            $('#id_extra_dirty_field').val('False')
        }
    }
}

function getTotalPriceLanding() {
    var car_price = Number(getTupleById('select-type')[0]);
    var interior_price = Number(getTupleById('select-interior')[0]);
    var total_price = car_price + interior_price;
    $('#landing-submit').text("$" + total_price);
}

function getTotalPrice() {
    var car_price = Number(getTupleById('select-type')[0]);
    var interior_price = Number(getTupleById('select-interior')[0]);
    var extra_dirty_price = Number(getTupleById('select-extra-dirty')[0]);
    var total_price = car_price + interior_price + extra_dirty_price;
    $('#total-price').text("$" + total_price);
}

function getTupleById(id) {
    var tuple = document.getElementById(id).value.replace("$", "").split(/\s{4}/);
    tuple[1] = tuple[1].trim();
    return tuple;
}

function assignValueFromLanding() {
    $('#id_type_field').val(getTupleById('select-type')[1]);
    $('#id_interior_field').val(getTupleById('select-interior')[1])
    getTotalPrice();
}
