function selectChangeLanding(ele) {
    var field = getTupleById(ele.id)[1];
    if (ele.id == 'select-type') {
        $('#id_type_field').val(field);
    } else if (ele.id == 'select-interior') {
        $('#id_interior_field').val(field)
    }
    getTotalPriceLanding();
}

function getTotalPriceLanding() {
    var car_price = Number(getTupleById('select-type')[0]);
    var interior_price = Number(getTupleById('select-interior')[0]);
    var total_price = car_price + interior_price;
    $('#landing-submit').text("$" + total_price);
}

function selectChangeBooking(ele) {
    var field = getTupleById(ele.id)[1];
    var name = ele.id.slice(0, -1);
    var index = ele.id.slice(-1);

    if (name == 'select-type') {
        $('#id_type_field' + index).val(field);
    } else if (name == 'select-interior') {
        $('#id_interior_field' + index).val(field)
    }
    getTotalPrice();
}

function getTotalPrice() {
    var total_price = 0;
    var type_price_dict = {
        'Hatchback': 25,
        'Sedan': 29,
        'Wagon': 35,
        'SUV': 39,
        'Van': 45
    };
    var interior_price_dict = {
        'none': 0,
        'both': 19
    };
    var car_count = numberOfCars();
    for (var i = 1; i < car_count + 1; i++) {
        var type_price = type_price_dict[$('#id_type_field' + i).val()];
        var interior_price = interior_price_dict[$('#id_interior_field' + i).val()]
        var extra_dirty = $('#id_extra_dirty_field' + i).is(':checked');
        var extra_dirty_price = ((extra_dirty) ? 5 : 0);
        total_price += type_price + interior_price + extra_dirty_price;
    }
    $('#total-price').text("$" + total_price);
}

function getTupleById(id) {
    var tuple = document.getElementById(id).value.replace("$", "").split(/\s{4}/);
    tuple[1] = tuple[1].trim();
    return tuple;
}

function assignValueFromLanding() {
    $('#id_type_field1').val('Sedan');
    $('#id_interior_field1').val('both');
    getTotalPrice();
}

function addCar(btn) {
    var car_count = numberOfCars('+');
    var ele = $('#car' + car_count);
    ele.animate({height: ele.get(0).scrollHeight});
    getTotalPrice();
    if (car_count >= 5) {
        btn.style.display = 'none';
    } else {
        $('#remove_car_btn').css('display', 'inline-block');
    }
}

function removeCar(btn) {
    var ele = $('#car' + numberOfCars());
    ele.animate({height: 0});
    var car_count = numberOfCars('-');
    getTotalPrice();
    if (car_count <= 1) {
        btn.style.display = 'none';
    } else {
        $('#add_car_btn').css('display', 'inline-block');
    }
}

function numberOfCars(operation) {
    operation = operation || '';
    var ele = $('#id_car_count_field');
    var car_count = Number(ele.val());
    if (operation == '+') {
        car_count++;
    } else if (operation == '-') {
        car_count--;
    } else {
        return car_count;
    }
    ele.val(car_count);
    return car_count;
}