function autoresizeTextarea(textarea) {
    textarea.style.height = 'auto'; // Reset the height
    textarea.style.height = textarea.scrollHeight + 'px'; // Set the height
  }

// Adjust the textarea on load
document.addEventListener('DOMContentLoaded', function() {
  const textarea = document.getElementById('content');
  autoresizeTextarea(textarea);

  // Adjust the textarea on input
  document.getElementById('content').addEventListener('input', function() {
    autoresizeTextarea(this);
  });
});

