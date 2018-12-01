$(function () {
    var $btnShowModal = $('#btn-show-modal');
    var $orderId = $btnShowModal.attr('data-order-id');

    $btnShowModal.on('click', function () {
        swal({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, change it',
            cancelButtonText: 'No, cancel!',
            confirmButtonClass: 'btn btn-success',
            cancelButtonClass: 'btn btn-danger',
            showCloseButton: true,
            buttonsStyling: true,
            reverseButtons: true
        }).then((result => {
            if (result.value) {
                var url = '/api/order/update/';
                var data = {
                    pk: $orderId,
                    csrfmiddlewaretoken: Cookies.get('csrftoken')
                };
                $.post(url, data)
                    .done(function (data) {
                        swal(
                            'Updated!',
                            'The order has been updated.',
                            'success',
                        );
                        $('.panel-footer').hide();
                        setTimeout(function(){
                            location.reload();
                        }, 1000);

                    })
                    .fail(function (response) {
                        console.error(response);
                    })
                    .always(function () {
                        console.log("The request are done !!!");
                    });
            }
        }))

    });
});