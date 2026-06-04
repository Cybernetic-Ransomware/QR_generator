function clearFileInput() {
    var fileInput = document.getElementById('image');
    fileInput.value = '';
    fileInput.dispatchEvent(new Event('change'));
}
