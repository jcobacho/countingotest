// Select all delete buttons
const deleteButtons = document.querySelectorAll('[data-action="delete_row"]');

deleteButtons.forEach(d => {
    // Delete button on click
    d.addEventListener('click', function (e) {
        e.preventDefault();
        const delete_url = d.dataset.href;

        Swal.fire({
            text: "Are you sure you want to delete this item ?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, delete!",
            cancelButtonText: "No, cancel",
            customClass: {
                confirmButton: "btn fw-bold btn-danger",
                cancelButton: "btn fw-bold btn-active-light-primary"
            }
        }).then(function (result) {
            if (result.value && delete_url) {

                fetch(delete_url, {
                    method: 'DELETE', headers: {
                        'Content-type': 'application/json; charset=UTF-8'
                    }
                })
                    .then(function (resp) {
                        window.location.reload();
                    })
                    .catch(errorMsg => {
                        console.log(errorMsg);
                    });
            }
        });
    })
});

