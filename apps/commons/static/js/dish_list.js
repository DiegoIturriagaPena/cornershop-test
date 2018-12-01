$(function () {

    $selectGroup = $('#select-group');
    $selectOrder = $('#select-order');
    $button = $('button.btn-primary');

    $selectGroup.on('change', function () {
        submitButton();
    });

    $selectOrder.on('change', function () {
        submitButton();
    });

    function submitButton() {
        $button.attr('clicked', true);
        $button.unbind('click').click();
    }

});