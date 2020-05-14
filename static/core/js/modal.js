
(function($) {
    $('#deleteAccountModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var id = button.data('id')
        var name = button.data('name')

        var modal = $(this)
            modal.find('.account-id').val(id)
            modal.find('.modal-body').text('Are you sure you want to delete ' + name + ' Account?')
            console.log('hello')
        })

    $('#deleteAccountTransactionModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var id = button.data('id')
    
        var modal = $(this)
            modal.find('.acct-trans-id').val(id)
            modal.find('.modal-body').text('Are you sure you want to delete Account Transaction # ' + id + '?')
        })
        
    $('#cancelTransferModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var id = button.data('id')

        var modal = $(this)
            modal.find('.make-transf-id').val(id)
            modal.find('.modal-body').text('Are you sure you want to cancel Transfer Transaction # ' + id + '?')
    })
    

    
})(jQuery);

$(function () {
    $('#editAccountModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var id = button.data('id')
        var name = button.data('name')
        var balance = button.data('balance')
        
        var modal = $(this)
            modal.find('.account-id').val(id)
            modal.find('.account-name').val(name)
            modal.find('.account-balance').val(balance)
    })

    $('#editBudgetModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var id = button.data('id')
        var name = button.data('name')
        
        var modal = $(this)
            modal.find('.budget-id').val(id)
            modal.find('.budget-name').val(name)
    })

    $('#deleteBudgetModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var id = button.data('id')
        var name = button.data('name')

        var modal = $(this)
            modal.find('.budget-id').val(id)
            modal.find('.modal-body').text('Are you sure you want to delete your ' + name + ' Budget?')
        })
});