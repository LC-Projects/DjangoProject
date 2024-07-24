document.addEventListener('DOMContentLoaded', function () {
    const dropdownSelected = document.querySelector('.dropdown-selected');
    const dropdownOptions = document.querySelector('.dropdown-options');
    const hiddenInput = document.getElementById('id_language');

    // Function to update the dropdown based on the hidden input's value
    function updateDropdownSelection() {
        document.querySelectorAll('.dropdown-option').forEach(option => {
            if (option.dataset.value === hiddenInput.value) {
                // Copy the entire HTML content, including the flag
                dropdownSelected.innerHTML = option.innerHTML;
                dropdownSelected.dataset.value = option.dataset.value;
            }
        });
    }

    // Initial update of the dropdown to reflect the hidden input's value
    updateDropdownSelection();

    // Toggle dropdown options visibility
    dropdownSelected.addEventListener('click', function () {
        dropdownOptions.classList.toggle('hidden');
    });

    // Update selected item, hide options, and update hidden input when an option is clicked
    document.querySelectorAll('.dropdown-option').forEach(option => {
        option.addEventListener('click', function () {
            // Copy the entire HTML content, including the flag
            dropdownSelected.innerHTML = this.innerHTML;
            dropdownSelected.dataset.value = this.dataset.value;
            dropdownOptions.classList.add('hidden');

            // Update the hidden input's value
            hiddenInput.value = this.dataset.value;
        });
    });

    // Optional: Hide dropdown options when clicking outside
    document.addEventListener('click', function (e) {
        if (!dropdownSelected.contains(e.target) && !dropdownOptions.contains(e.target)) {
            dropdownOptions.classList.add('hidden');
        }
    });
});