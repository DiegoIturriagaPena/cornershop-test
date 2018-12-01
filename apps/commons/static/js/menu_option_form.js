$(function () {
    // initializing formset
    $('#tbl_formset').find('tbody tr').formset({
        prefix: 'frm_menu_option',
        formCssClass: 'formset-control',
        deleteText: 'Delete',
        addText: 'Add'
    });
    $('.delete-row').css('display', 'block');
});