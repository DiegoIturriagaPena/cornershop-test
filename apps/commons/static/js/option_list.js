$(function () {

    $selectMenu = $('#select-menu');
    $button = $('button.btn-primary');

    $selectMenu.on('change', function () {
        submitButton();
    });

    function submitButton() {
        $button.attr('clicked', true);
        $button.unbind('click').click();
    }

});