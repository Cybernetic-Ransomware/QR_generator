$(document).ready(function(){
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
                    window.location.href = '/result';
                } else {
                    $('#errorModalBody').empty();
                    response.errors.forEach(function(error) {
                        $('#errorModalBody').append('<p>' + error + '</p>');
                    });
                    $('#errorModal').modal('show');
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});
