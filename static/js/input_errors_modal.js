$(document).ready(function(){
    function showErrors(errors) {
        var $body = $('#errorModalBody').empty();
        (errors && errors.length ? errors : ['An unexpected error occurred.'])
            .forEach(function(error) { $('<p>').text(error).appendTo($body); });
        $('#errorModal').modal('show');
    }

    $('#generate-form').submit(function(event){
        event.preventDefault();

        var formData = new FormData($(this)[0]);

        $.ajax({
            type: 'POST',
            url: '/generate',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    window.location.href = '/result?id=' + encodeURIComponent(response.id);
                } else {
                    showErrors(response.errors);
                }
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                var errors = (xhr.responseJSON && xhr.responseJSON.errors) ? xhr.responseJSON.errors : null;
                if (!errors && xhr.status === 413) {
                    errors = ['File is too large. Maximum request size is 6 MB.'];
                }
                showErrors(errors);
            }
        });
    });
});
