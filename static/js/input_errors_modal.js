document.addEventListener('DOMContentLoaded', function () {
    var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));

    function showErrors(errors) {
        var body = document.getElementById('errorModalBody');
        body.innerHTML = '';
        (errors && errors.length ? errors : ['An unexpected error occurred.'])
            .forEach(function (error) {
                var p = document.createElement('p');
                p.textContent = error;
                body.appendChild(p);
            });
        errorModal.show();
    }

    document.getElementById('generate-form').addEventListener('submit', function (event) {
        event.preventDefault();

        fetch('/generate', { method: 'POST', body: new FormData(this) })
            .then(function (response) {
                return response.json().then(function (data) {
                    if (data.success) {
                        window.location.href = '/result?id=' + encodeURIComponent(data.id);
                    } else {
                        showErrors(data.errors);
                    }
                });
            })
            .catch(function (err) {
                console.error(err);
                showErrors(null);
            });
    });
});
