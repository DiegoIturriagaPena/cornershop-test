$(function () {
    // initializing formset
    $('#tbl_formset').find('tbody tr').formset({
        prefix: 'frm_option_dish',
        formCssClass: 'formset-control',
        deleteText: 'Delete',
        addText: 'Add'
    });
    $('.delete-row').css('display', 'block');
});