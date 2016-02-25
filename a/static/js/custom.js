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
    var landing_submit = $('#landing-submit');
    if (landing_submit.length) {
        var type_price = type_price_dict[$('#id_type_field').val()];
        var interior_price = interior_price_dict[$('#id_interior_field').val()];
        total_price += type_price + interior_price;
        landing_submit.text('$' + total_price);
    } else {
        var car_count = numberOfCars();
        for (var i = 1; i < car_count + 1; i++) {
            type_price = type_price_dict[$('#id_type_field' + i).val()];
            interior_price = interior_price_dict[$('#id_interior_field' + i).val()];
            var extra_dirty = $('#id_extra_dirty_field' + i).is(':checked');
            var extra_dirty_price = ((extra_dirty) ? 5 : 0);
            total_price += type_price + interior_price + extra_dirty_price;
        }
        $('#total-price').text('$' + total_price);
    }

}

function assignInitialValues(initial_type_choice, initial_interior_choice) {
    if (initial_type_choice) {
        $('#id_type_field1').val(initial_type_choice);
    }
    if (initial_interior_choice) {
        $('#id_interior_field1').val(initial_interior_choice);
    }
    var car_count = numberOfCars();
    for (var i = 1; i < car_count + 1; i++) {
        $('#car' + i).css('height', 'auto');
    }
    if (car_count > 1) {
        $('#remove_car_btn').css('display', 'inline-block');
    } else if (car_count >= 5) {
        $('#add_car_btn').style.display = 'none';
    }
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

$('.admin-change-role-btn').click(function () {
    $('#id_role_field').val(this.text.toLowerCase());
    var form = $('#admin-change-role-form');
    form.submit();
    //var posting = $.post(form.attr('action'), form.serialize(), function (data) {
    //    if (data.role == 'washer') {
    //        alert('washer');
    //        $('#admin-washer-selector').text('>');
    //        $('#admin-washee-selector').text('');
    //    } else if (data.role == 'washee') {
    //        alert('washee');
    //        $('#admin-washer-selector').text('');
    //        $('#admin-washee-selector').text('>');
    //    }
    //});
});