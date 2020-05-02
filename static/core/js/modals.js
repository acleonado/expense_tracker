(function($) {
    $('#AddAccountModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var id = button.data('id')

    var modal = $(this)
    modal.find('.user-id').val(id)
    })
})(jQuery);