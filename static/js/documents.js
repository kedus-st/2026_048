document.addEventListener("DOMContentLoaded", function() {
    var docs = JSON.parse(document.getElementById("docs_context_elem").getAttribute("data"));

    const categories = document.querySelectorAll('.category');
    const contentContainer = document.getElementById('content_panel');
    const expandableItemTemplate = document.getElementById('expandable-item-template');

    function fetchSecureURL(blobName) {
        return fetch(`/get-sas-token/?blob_name=${blobName}`)
            .then(response => response.json())
            .then(data => {
                if (data.url) {
                    return data.url;
                } else {
                    throw new Error('Failed to fetch url');
                }
            });
    }

    categories.forEach(category => {
        category.addEventListener('click', function() {
            if (!contentContainer.classList.contains('active')) {
                contentContainer.classList.add('active');
            }
            const categoryName = this.querySelector('h2').textContent;
            contentContainer.innerHTML = '';

            const title = document.createElement('h1');
            title.textContent = categoryName;
            contentContainer.appendChild(title);

            // Get the corresponding collapsible items for the clicked category
            const itemsContainerId = categoryName.toLowerCase().replace(/\s+/g, '_') + '_items';
            const collapsibleItemsContainer = document.getElementById(itemsContainerId);
            if (collapsibleItemsContainer) {
                // Clone and customize the expandable item template for each item
                const expandableItems = collapsibleItemsContainer.querySelectorAll('.expandable-item');
                expandableItems.forEach(item => {
                    const itemName = item.getAttribute('name');
                    const itemDocs = docs.filter(doc => doc.type === itemName); // Filter documents based on type
                    const itemClone = expandableItemTemplate.content.cloneNode(true);
                    const form = itemClone.querySelector('form');
                    const hiddenInput = itemClone.querySelector('input[type="hidden"]');
                    const uploadButton = itemClone.querySelector('.upload-button');
                    const selectField = itemClone.querySelector('.document-dropdown');
                    const documentLink = itemClone.querySelector('.document-link');

                    // Set form ID, hidden input ID, and value dynamically
                    form.id = itemName.toLowerCase().replace(/\s+/g, '_') + '_form';
                    hiddenInput.id = itemName.toLowerCase().replace(/\s+/g, '_') + '_type';
                    hiddenInput.value = itemName;
                    uploadButton.setAttribute('form', itemName.toLowerCase().replace(/\s+/g, '_') + '_form');
                    itemClone.querySelector('.document-name').textContent = item.textContent;

                    // Add empty default option to select field
                    const defaultOption = document.createElement('option');
                    defaultOption.value = '';
                    defaultOption.textContent = '';
                    selectField.appendChild(defaultOption);

                    // Populate select field with options based on filtered documents
                    itemDocs.forEach(doc => {
                        const option = document.createElement('option');
                        option.value = doc.id; 
                        option.textContent = doc.name;
                        selectField.appendChild(option);
                    });

                    // Event listener to update link when an option is selected
                    selectField.addEventListener('change', function() {
                        const selectedOption = selectField.options[selectField.selectedIndex];
                        if (selectedOption.value !== '') {
                            fetchSecureURL(PROJECT_NAME +'/management/docs/' + selectedOption.textContent).then(url=>{
                                documentLink.href = url;
                                documentLink.style.display = 'inline'; 
                            });
                        } else {
                            documentLink.style.display = 'none'; 
                        }
                    });

                    contentContainer.appendChild(itemClone);
                });
            } else {
                console.error('Collapsible items container not found for category: ' + categoryName);
            }
        });
    });
});
