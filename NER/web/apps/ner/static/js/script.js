document.addEventListener('DOMContentLoaded', function() {
    // Extract the AUTH_TOKEN from the URL hash
    const token = window.location.hash.substring(1); // Remove '#' from the beginning
    // Populate the token into the form field
    const tokenField = document.getElementById('tokenField');
    const checkButton = this.getElementById('checkTokenButton');
    const processButton = this.getElementById('processButton');
    
    // Populate the token into the form field and adjust field properties if token exists
    if (token) {
        tokenField.value = token;
        checkTokenValidity(token).then(isValid => {
            if (isValid) {
                tokenField.disabled = true; // Disable the field
                checkButton.disabled = true; // Disable the field
                tokenField.classList.add('is-valid');
                processButton.classList.replace('btn-outline-secondary', 'btn-outline-dark');
                processButton.disabled = false;
                console.log('Token is valid.');
            } else {
                tokenField.classList.add('is-invalid');
                processButton.disabled = true;
                console.log('Token is invalid.');
            }
        });
    }

    checkTokenButton.addEventListener('click', function() {
        // Get the current value of the token input field
        const token = document.getElementById('tokenField').value;
        // Call the checkTokenValidity function with the token
        checkTokenValidity(token).then(isValid => {
            if (isValid) {
                if (tokenField.classList.contains('is-invalid')) {
                    tokenField.classList.replace('is-invalid', 'is-valid');
                }
                else {
                    tokenField.classList.add('is-valid');
                }
                processButton.classList.replace('btn-outline-secondary', 'btn-outline-dark');
                processButton.disabled = false;
                console.log('Token is valid.');
            } else {
                if (tokenField.classList.contains('is-valid')) {
                    tokenField.classList.replace('is-valid', 'is-invalid');
                }
                else {
                    tokenField.classList.add('is-invalid');
                }
                processButton.disabled = true;
                console.log('Token is invalid.');
            }
        });
    });

    
});

async function checkTokenValidity(token) {
    // Define the URL for the API endpoint
    const url = '/api/auth/validate_token';

    // Prepare the request body
    const requestBody = {
        token: token
    };

    try {
        // Send a POST request to the API endpoint
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        // Check if the request was successful
        if (!response.ok) {
            console.error('Error validating token:', response.statusText);
            return false; // Return false if the request failed
        }

        // Parse the JSON response
        const data = await response.json();

        if (data.status === 'valid') {
            return true; // Return true if the token is valid
        } else {
            return false; // Return false if the token is invalid
        }
    } catch (error) {
        console.error('Error:', error);
        return false; // Return false in case of any error
    }
}

async function processAndDisplay() {
    // Get the text from the input field
    const text = document.getElementById('textInput').value;
    const token = document.getElementById('tokenField').value;
    const inputForm = document.getElementById('textProcessForm');
    const nerForm = document.getElementById('nerForm');
    const processButton = document.getElementById('loadingIndicator');

    processButton.classList.remove("invisible");

    // Ensure the token is present
    if (!token) {
        console.error('Token is missing.');
        return;
    }

    // Send a request to the FastAPI endpoint
    const response = await fetch('/api/ner/process-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, // Use the token from the form
        },
        body: JSON.stringify({ text: text }),
    });

    // Check if the request was successful
    if (!response.ok) {
        console.error('Error processing text:', response.statusText);
        return;
    }

    // Parse the JSON response
    const data = await response.json();

    const container = document.getElementById('result');
    // Function to highlight all spans with matching entity IDs
    const highlightEntitySpans = (entityIds, highlight) => {
        entityIds.split(',').forEach(id => {
            const spans = container.querySelectorAll(`span[data-entity="${id}"]`);
            spans.forEach(span => {
                if (highlight) {
                    span.classList.add('highlight');
                } else {
                    span.classList.remove('highlight');
                }
            });
        });
    };

    // Function to handle hover start
    const handleHoverStart = (event) => {
        const entityIds = event.target.getAttribute('data-entity');
        if (entityIds) {
            highlightEntitySpans(entityIds, true);
        }
    };

    // Function to handle hover end
    const handleHoverEnd = (event) => {
        const entityIds = event.target.getAttribute('data-entity');
        if (entityIds) {
            highlightEntitySpans(entityIds, false);
        }
    };

    // Function to handle click
    const handleClick = (event) => {
        console.log('Entity IDs:', event.target.getAttribute('data-entity'));
    };
    
    // Function to handle click
    const handleDelete = (event) => {
          var target = event.target;
          var parent = target.parentElement;//parent of "target"
        	const entityIds = parent.getAttribute('data-entity');
        	// Assuming all entity classes are prefixed with 'ent-'
          const entityClasses = parent.className.split(" ").filter(c => c.startsWith('ent-'));
          entityClasses.forEach(ec => parent.classList.remove(ec));

          // Clear the 'data-entity' attribute
          parent.removeAttribute('data-entity');
          parent.classList.remove('highlight');
          if (entityIds) {
              highlightEntitySpans(entityIds, false);
          }
    };

    // Create spans for each token and attach events
    data.tokens.forEach(token => {
        const span = document.createElement('span');
        span.textContent = data.text.substring(token.start, token.end) + " ";
        span.setAttribute('data-id', token.id);
        span.setAttribute('data-start', token.start);
        span.setAttribute('data-end', token.end);

        // Create remove button
        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'x';
        removeBtn.setAttribute('class', 'remove-btn');
        removeBtn.onclick = handleDelete; 
        
        // Attach hover events
        span.addEventListener('mouseenter', handleHoverStart);
        span.addEventListener('mouseleave', handleHoverEnd);

        // Attach click event
        span.addEventListener('click', handleClick);
        
        span.appendChild(removeBtn); // Add remove button to the span
        container.appendChild(span);
    });

    // Step 2: Mark entities on tokens
    data.ents.forEach((entity, entityIndex) => {
        for (let tokenId = 0; tokenId < data.tokens.length; tokenId++) {
            const token = data.tokens[tokenId];
            if (token.start >= entity.start && token.end <= entity.end) {
                // This token is part of the current entity
                let span = container.querySelector(`span[data-id="${token.id}"]`);
                if (span) {
                    span.classList.add(`ent-${entity.label}`);
                    let existingEntities = span.getAttribute('data-entity');
                    let newEntities = existingEntities ? `${existingEntities},${entity.id}` : `${entity.id}`;
                    span.setAttribute('data-entity', newEntities);
                }
            }
        }
    });

    function generateOverview(matches) {
        let outputHtml = '<br>';
        // Removed colorIndex since we're using specific colors for each category
    
        for (const category in matches.entities) { // Ensure to access matches.entities
            outputHtml += `<b>${category.replace('_', ' ')}</b>`; // Format category names
            outputHtml += '<div class="match-list">';
            matches.entities[category].forEach(item => {
                // Use the category to dynamically create the variable name
                outputHtml += `<div class="match ent-${category}" >${item}</div>`;
            });
            outputHtml += '</div>';
            // No need to increment colorIndex
        }
    
        // Display the JSON output in a new section of the HTML
        const overviewDiv = document.getElementById('overview');
        overviewDiv.innerHTML = outputHtml;

        const downloadButton = document.createElement('button');
        downloadButton.textContent = '💾 Download JSON';
        downloadButton.setAttribute('class', 'btn btn-outline-dark');
        overviewDiv.prepend(downloadButton);

        // Set up the download action for the button
        downloadButton.addEventListener('click', () => {
            const jsonData = JSON.stringify(matches.entities, null, 2); // Pretty print the JSON
            const blob = new Blob([jsonData], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.setAttribute('href', url);
            a.setAttribute('download', 'entities.json');
            a.click();
            URL.revokeObjectURL(url); // Clean up the URL object
        });
    }

    generateOverview(data);



    // Hide loading indicator
    processButton.classList.add("invisible");
    inputForm.classList.add("invisible");
    nerForm.classList.remove("invisible");
}
