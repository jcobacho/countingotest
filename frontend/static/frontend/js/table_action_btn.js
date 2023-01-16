// Select all delete buttons
const actionButtons = document.querySelectorAll('[data-action="buttons"]');

actionButtons.forEach(d => {
    // Delete button on click
    d.addEventListener('click', function (e) {
        e.preventDefault();
        const alert_msg = d.dataset.message || "Are you sure you want to delete this item ?";
        const icon = d.dataset.icon || "warning";
        const url = d.dataset.href;
        const confirm_btn = d.dataset.confirmbtn || "btn fw-bold btn-danger";
        const cancel_btn = d.dataset.cancelbtn || "btn fw-bold btn-active-light-primary";
        const method = d.dataset.method || "DELETE";
        const confirm_btn_text = d.dataset.confirmbtntext || "Yes, delete!";

        Swal.fire({
            text: alert_msg,
            icon: icon,
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: confirm_btn_text,
            cancelButtonText: "No, cancel",
            customClass: {
                confirmButton: confirm_btn,
                cancelButton: cancel_btn
            }
        }).then(function (result) {
            if (result.value && url) {

                fetch(url, {
                    method: method, headers: {
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

