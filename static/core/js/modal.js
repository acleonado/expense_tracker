(function($) {
    $('#deleteAccountModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var id = button.data('id')
    var name = button.data('name')

    var modal = $(this)
        modal.find('.account-id').val(id)
        modal.find('.modal-body').text('Are you sure you want to delete ' + name + ' Account?')
    })

    $('#deleteAccountTransactionModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var id = button.data('id')
    
        var modal = $(this)
            modal.find('.acct-trans-id').val(id)
            modal.find('.modal-body').text('Are you sure you want to delete Transaction # ' + id + '?')
        })
})(jQuery);