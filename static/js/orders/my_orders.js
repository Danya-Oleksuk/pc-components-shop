document.addEventListener('DOMContentLoaded', function () {
        const buttons = document.querySelectorAll('.toggle-details');
        buttons.forEach(button => {
            button.addEventListener('click', function () {
                const orderId = this.getAttribute('data-order-id');
                const detailsRow = document.getElementById('details-' + orderId);
                detailsRow.classList.toggle('d-none');
            });
        });
    });