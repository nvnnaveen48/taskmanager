django.jQuery(function($) {
    // Handle CSV file upload
    $('#id_csv_file').on('change', function(e) {
        var file = e.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var text = e.target.result;
                // Accept as plain text (comma-separated) instead of JSON
                $('#id_csv_data').val(text);
            };
            reader.readAsText(file);
        }
    });

    // Handle image preview
    $('#id_image').on('change', function(e) {
        var file = e.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var preview = $('#image-preview');
                if (preview.length === 0) {
                    preview = $('<img id="image-preview" style="max-width: 200px; margin-top: 10px;">');
                    $('#id_image').after(preview);
                }
                preview.attr('src', e.target.result);
            };
            reader.readAsDataURL(file);
        }
    });

    // Add a visible paste area for images
    if ($('#id_image').length && $('#image-paste-area').length === 0) {
        $('#id_image').before('<div id="image-paste-area" style="border:2px dashed #ccc;padding:10px;text-align:center;margin-bottom:10px;">Paste image here from clipboard (Ctrl+V)</div>');
        // Add hidden input for base64 image data
        $('#id_image').before('<input type="hidden" name="pasted_image_data" id="id_pasted_image_data">');
    }
    $('#image-paste-area').on('paste', function(e) {
        var items = (e.originalEvent || e).clipboardData.items;
        for (var i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                var file = items[i].getAsFile();
                var reader = new FileReader();
                reader.onload = function(event) {
                    var preview = $('#image-preview');
                    if (preview.length === 0) {
                        preview = $('<img id="image-preview" style="max-width: 200px; margin-top: 10px;">');
                        $('#id_image').after(preview);
                    }
                    preview.attr('src', event.target.result);
                    $('#id_pasted_image_data').val(event.target.result);
                    $('#image-paste-area').after('<div class="alert alert-info mt-2">Image pasted! It will be saved when you submit the form.</div>');
                };
                reader.readAsDataURL(file);
            }
        }
    });
}); 