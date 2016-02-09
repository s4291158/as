var car_count = 1;

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
    }
}

function getTotalPriceLanding() {
    var car_price = Number(getTupleById('select-type')[0]);
    var interior_price = Number(getTupleById('select-interior')[0]);
    var total_price = car_price + interior_price;
    $('#landing-submit').text("$" + total_price);
}

function getTotalPrice() {
    var total_price = 0;
    for (var i = 1; i < car_count + 1; i++) {
        var car_price = Number(getTupleById('select-type' + i)[0]);
        var interior_price = Number(getTupleById('select-interior' + i)[0]);
        var extra_dirty = document.getElementById('id_extra_dirty_field' + i).checked;
        var extra_dirty_price = ((extra_dirty) ? 5 : 0);
        total_price += car_price + interior_price + extra_dirty_price;
    }
    $('#total-price').text("$" + total_price);
}

function getTupleById(id) {
    var tuple = document.getElementById(id).value.replace("$", "").split(/\s{4}/);
    tuple[1] = tuple[1].trim();
    return tuple;
}

function assignValueFromLanding() {
    $('#id_type_field1').val(getTupleById('select-type1')[1]);
    $('#id_interior_field1').val(getTupleById('select-interior1')[1]);
    getTotalPrice();
}

function addCar(btn) {
    car_count++;
    console.log(car_count);
    $('#car' + car_count).css('display', 'block');
    getTotalPrice();
    if (car_count >= 5) {
        btn.style.display = 'none';
    } else {
        $('#remove_car_btn').css('display', 'block');
    }
}

function removeCar(btn) {
    $('#car' + car_count).css('display', 'none');
    car_count--;
    console.log(car_count);
    getTotalPrice()
    if (car_count <= 1) {
        btn.style.display = 'none';
    } else {
        $('#add_car_btn').css('display', 'block');
    }
}