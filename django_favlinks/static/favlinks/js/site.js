function resetForm(formId, form_action, action) {
    const modal_form = document.getElementById(formId);
    const modal_form_title = modal_form.querySelector('.modal-title');
    const modal_submit_button = modal_form.querySelector('.modal-footer button[type="submit"]');

    modal_form.action = "";
    modal_form.reset();
    modal_form.action = form_action;
    if (action === 'edit') {
        modal_form_title.textContent = 'Edit bookmark';
        modal_submit_button.textContent = 'Update bookmark';
    } else {
        modal_form_title.textContent = 'Add New bookmark';
        modal_submit_button.textContent = 'Save bookmark';
    }
}

function populateForm(data) {
    var form = document.querySelector('#bookmarkModal form');
    for (const key in data) {
        var input = form.querySelector(`[name="${key}"]`); // Select input based on name attribute
        if (input && key !== "screenshot") {
            if (input.type === "checkbox") {
                input.checked = data[key]; // Set checked property for checkboxes
            } else {
                        input.value = data[key];
            }
        }
    }
};


document.addEventListener('DOMContentLoaded', (event) => {

    //const editButtons = document.querySelectorAll('#editBookmarkButton');
    const addButtons = document.querySelectorAll('#addBookmarkButton');


    /* Add event listener to the add button */
    addButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            resetForm('bookmarkForm', this.getAttribute("data-bs-url"), "add");
        });
    });

    /* Add event listener to the delete buttons */
    var deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var itemId = this.getAttribute('data-bookmark-id'); // Get the item ID from the data attribute
            var actionUrl = `${itemId}/delete/`; // Construct the URL for form submission
            
            // Set the action attribute of the form inside the delete modal
            var form = document.querySelector('#deleteItemModal form');
            form.setAttribute('action', actionUrl);
            
            // Show the modal
            var deleteModal = document.querySelector('#deleteItemModal');
            var modal = new bootstrap.Modal(deleteModal); // Bootstrap 5 modal instance
            modal.show();
        });
    });


        /* Add event listener to the publish buttons */
        var publishButtons = document.querySelectorAll('.publish-btn');
        publishButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                var itemId = this.getAttribute('data-bookmark-id'); // Get the item ID from the data attribute
                var actionUrl = `${itemId}/publish/`; // Construct the URL for form submission
                
                // Set the action attribute of the form inside the delete modal
                var form = document.querySelector('#publishItemModal form');
                form.setAttribute('action', actionUrl);
                
                // Show the modal
                var publishModal = document.querySelector('#publishItemModal');
                var modal = new bootstrap.Modal(publishModal); // Bootstrap 5 modal instance
                modal.show();
            });
        });
    

    // Add event listeners to edit buttons
    const editButtons = document.querySelectorAll('.edit-btn');

    editButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var itemId = this.getAttribute('data-bookmark-id'); // Get the item ID
            var url = `/api/favlinks/bookmarks/${itemId}/`; // Endpoint that returns item details as JSON
            
            fetch(url)
            .then(response => response.json())
            .then(data => {
                // reset the form
                resetForm('bookmarkForm', `/favlinks/${itemId}/update/`, "edit");
                // Populate the form fields
                console.log("data: ",data);
                populateForm(data);

                const bookmarkForm = document.getElementById('bookmarkForm');
                
                // Show the modal
                var itemModal = new bootstrap.Modal(document.getElementById('bookmarkModal'));
                itemModal.show();
            })
            .catch(error => console.error('Error fetching item details:', error));
        });
    });


    /* 
    Add event listener to tags, clicking a tag adds a filter,
    if the URL already has a filter, it appends the tag filter to the URL
     */
    const tagLinks = document.querySelectorAll('.tag');
    tagLinks.forEach(function(tag) {
        tag.addEventListener('click', function() {
            var tagId = this.getAttribute('data-tag-name');
        
            // Get the current URL
            var currentUrl = new URL(window.location.href);
        
            // Get the URLSearchParams object
            var params = new URLSearchParams(currentUrl.search);
        
            // Add the new query parameter if it doesn't exist already
            if (!params.getAll('q').includes(tagId)) {
                params.append('q', tagId); // Use .set() to add or update the parameter
            }
        
            // Construct the new URL with updated parameters
            currentUrl.search = params.toString();
        
            // Redirect to the new URL
            window.location.href = currentUrl.toString();
        });    });


});          
