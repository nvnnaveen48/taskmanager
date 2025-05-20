document.addEventListener('DOMContentLoaded', function() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        const container = input.parentElement;
        const pasteArea = document.createElement('div');
        pasteArea.className = 'paste-area';
        pasteArea.innerHTML = '<p>Or paste image here (Ctrl+V)</p>';
        container.appendChild(pasteArea);

        pasteArea.addEventListener('paste', function(e) {
            const items = (e.clipboardData || e.originalEvent.clipboardData).items;
            
            for (let i = 0; i < items.length; i++) {
                if (items[i].type.indexOf('image') !== -1) {
                    const blob = items[i].getAsFile();
                    const file = new File([blob], 'pasted-image.png', { type: 'image/png' });
                    
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    input.files = dataTransfer.files;
                    
                    // Trigger change event
                    const event = new Event('change', { bubbles: true });
                    input.dispatchEvent(event);
                    break;
                }
            }
        });
    });
}); 