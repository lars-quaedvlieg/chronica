document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('input[name="filter"]');
    const searchBar = document.getElementById('search-bar');
    const notesContainer = document.getElementById('notes-container');
    const tagsContainer = document.getElementById('available-tags');
    const searchButton = document.getElementById('search-button');

    Date.prototype.getWeek = function () {
        var onejan = new Date(this.getFullYear(), 0, 1);
        var today = new Date(this.getFullYear(), this.getMonth(), this.getDate());
        var dayOfYear = ((today - onejan + 86400000) / 86400000);
        return Math.ceil(dayOfYear / 7)
    };

    // Get notes data from the script tag
    const notesData = document.getElementById('notes-data').textContent;
    const notes = JSON.parse(notesData);

    // Get all available tags from the script tag
    const tagsData = document.getElementById('tags-data').textContent;
    const tags = JSON.parse(tagsData);

    const tagColors = {};

    // Function to generate random pastel color for tags
    function getRandomColor() {
        const letters = 'BCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * letters.length)];
        }
        return color;
    }

    // Assign random colors to each unique tag
    tags.forEach(tag => {
        tagColors[tag] = getRandomColor();
    });

    // Render available tags
    function renderAvailableTags() {
        tagsContainer.innerHTML = ''; // Clear existing tags
        tags.forEach(tag => {
            const tagBadge = document.createElement('span');
            tagBadge.classList.add('badge', 'tag-badge');
            tagBadge.textContent = tag;
            tagBadge.style.backgroundColor = tagColors[tag];
            tagBadge.addEventListener('click', () => {
                filterNotesByTag(tag);
            });
            tagsContainer.appendChild(tagBadge);
        });
    }

    // Function to group notes by different time periods
    function groupNotesByFilter(notes, filter) {
        const groupedNotes = {};

        notes.forEach(note => {
            const noteDate = new Date(note.datetime);
            let groupKey;

            if (filter === 'month') {
                groupKey = noteDate.toLocaleString('default', { month: 'long', year: 'numeric' });
            } else if (filter === 'week') {
                const weekNumber = noteDate.getWeek();
                groupKey = `Week ${weekNumber}, ${noteDate.getFullYear()}`;
            } else if (filter === 'year') {
                groupKey = noteDate.getFullYear().toString();
            }

            if (!groupedNotes[groupKey]) {
                groupedNotes[groupKey] = [];
            }
            groupedNotes[groupKey].push(note);
        });

        // Sort group keys in descending order (latest first)
        const sortedGroupedNotes = {};
        Object.keys(groupedNotes)
            .sort((a, b) => {
                const aDate = new Date(groupedNotes[a][0].datetime);
                const bDate = new Date(groupedNotes[b][0].datetime);
                return bDate - aDate;
            })
            .forEach(key => {
                groupedNotes[key].sort((a, b) => new Date(b.datetime) - new Date(a.datetime));
                sortedGroupedNotes[key] = groupedNotes[key];
            });

        return sortedGroupedNotes;
    }

    function renderNotes(groupedNotes) {
        notesContainer.innerHTML = ''; // Clear previous content

        let hasNotes = false;

        for (const [groupKey, notes] of Object.entries(groupedNotes)) {
            if (notes.length === 0) continue;

            hasNotes = true;
            const groupSection = document.createElement('div');
            groupSection.classList.add('mb-4');

            // Add group label (month, week, year)
            const groupLabel = document.createElement('h3');
            groupLabel.classList.add('month-label', 'mb-3');
            groupLabel.textContent = groupKey;
            groupSection.appendChild(groupLabel);

            // Create a grid for the notes in this group
            const notesGrid = document.createElement('div');
            notesGrid.classList.add('row', 'g-4');

            notes.forEach(note => {
                const noteCardContainer = document.createElement('div');
                noteCardContainer.classList.add('col-lg-4', 'col-md-6', 'col-sm-12', 'mb-4');

                const card = document.createElement('div');
                card.classList.add('card', 'shadow-sm', 'h-100');
                card.setAttribute('data-id', note.id);
                card.setAttribute('data-datetime', note.datetime);
                card.style.transition = 'transform 0.2s ease, box-shadow 0.2s ease';

                card.addEventListener('mouseover', () => {
                    card.style.transform = 'translateY(-5px)';
                    card.style.boxShadow = '0 8px 15px rgba(0, 0, 0, 0.1)';
                });

                card.addEventListener('mouseout', () => {
                    card.style.transform = 'translateY(0)';
                    card.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.05)';
                });

                const cardBody = document.createElement('div');
                cardBody.classList.add('card-body');

                const cardTitle = document.createElement('h5');
                cardTitle.classList.add('card-title');
                cardTitle.textContent = note.title;

                const cardDatetime = document.createElement('p');
                cardDatetime.classList.add('card-text');
                cardDatetime.innerHTML = `<small class="text-muted">${note.datetime}</small>`;

                const tagsContainer = document.createElement('div');
                tagsContainer.classList.add('mb-2');
                note.tags.forEach(tag => {
                    const tagBadge = document.createElement('span');
                    tagBadge.classList.add('badge', 'tag-badge');
                    tagBadge.textContent = tag;
                    tagBadge.style.backgroundColor = tagColors[tag];
                    tagsContainer.appendChild(tagBadge);
                });

                const viewNoteButton = document.createElement('a');
                viewNoteButton.classList.add('btn', 'btn-primary', 'mt-3');
                viewNoteButton.href = `/view_entry/${note.id}`;
                viewNoteButton.textContent = 'View Note';

                cardBody.appendChild(cardTitle);
                cardBody.appendChild(tagsContainer);
                cardBody.appendChild(cardDatetime);
                cardBody.appendChild(viewNoteButton);

                card.appendChild(cardBody);
                noteCardContainer.appendChild(card);
                notesGrid.appendChild(noteCardContainer);
            });

            groupSection.appendChild(notesGrid);
            notesContainer.appendChild(groupSection);
        }

        if (!hasNotes) {
            const noResultsMessage = document.createElement('p');
            noResultsMessage.textContent = 'No notes match your search.';
            noResultsMessage.classList.add('no-results-message', 'text-center', 'mt-4');
            notesContainer.appendChild(noResultsMessage);
        }
    }

    function filterNotesByTag(tag) {
        const filteredNotes = notes.filter(note => note.tags.includes(tag));
        const groupedNotes = groupNotesByFilter(filteredNotes, currentFilter);
        renderNotes(groupedNotes);
    }

    // Initial render
    let currentFilter = 'month';
    const groupedNotes = groupNotesByFilter(notes, currentFilter);
    renderNotes(groupedNotes);
    renderAvailableTags();

    // Trigger search with semantic approach
    async function triggerSearch() {
        const query = searchBar.value.trim();

        // Clear the summary for a new search
        displaySummary('');

        try {
            const response = await fetch('/note_gallery/semantic_search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            if (response.ok) {
                const data = await response.json();

                // Validate data.notes before rendering
                if (data && Array.isArray(data.notes)) {
                    const groupedNotes = groupNotesByFilter(data.notes, currentFilter);
                    renderNotes(groupedNotes);
                } else {
                    console.error('Invalid response structure:', data);
                    alert('Invalid response received from server.');
                }
            } else {
                console.error('Failed to fetch notes: ', response.status, response.statusText);
                alert('Failed to fetch search results. Please try again.');
            }
        } catch (error) {
            console.error('Error with semantic search:', error);
            alert('An error occurred while performing the search.');
        }
    }

    // Event Listener for Search Button
    searchButton.addEventListener('click', triggerSearch);

    // Event Listener for Enter Key Press in Search Bar
    searchBar.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            triggerSearch();
        }
    });


    // Event Listeners
    // Event Listener for Ask Button
    document.getElementById('ask-button').addEventListener('click', triggerAsk);

    // Event Listeners for Filter Buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            // Update the current filter based on the selected radio button
            currentFilter = event.target.value;

            // Group and render the notes based on the updated filter
            const groupedNotes = groupNotesByFilter(notes, currentFilter);
            renderNotes(groupedNotes);
        });
    });


    async function triggerAsk() {
        const query = searchBar.value.trim();

        try {
            const response = await fetch('/note_gallery/rag_summary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            if (response.ok) {
                const data = await response.json();

                if (data && Array.isArray(data.relevant_notes)) {
                    if (data.summary) {
                        displaySummary(data.summary); // Display the new summary
                        const groupedNotes = groupNotesByFilter(data.relevant_notes, currentFilter);
                        renderNotes(groupedNotes);
                    }
                    else {
                        displaySummary('');
                    }
                } else {
                    console.error('Invalid response structure:', data);
                    alert('Invalid response received from server.');
                }
            } else {
                console.error('Failed to fetch RAG summary: ', response.status, response.statusText);
                alert('Failed to fetch Ask results. Please try again.');
            }
        } catch (error) {
            console.error('Error with Ask functionality:', error);
            alert('An error occurred while processing the Ask request.');
        }
    }

    function displaySummary(summaryText) {
        let summaryContainer = document.getElementById('summary-container');

        // Create the summary container if it doesn't exist
        if (!summaryContainer) {
            summaryContainer = document.createElement('div');
            summaryContainer.id = 'summary-container';
            summaryContainer.classList.add('summary-container');
            const container = document.querySelector('.container');
            container.insertBefore(summaryContainer, notesContainer);
        }

        // Update the summary content or hide the box if the summary is empty
        if (summaryText) {
            summaryContainer.innerHTML = summaryText;  // Use innerHTML to render HTML content
            summaryContainer.classList.add('fade-in');
            summaryContainer.style.display = 'block';  // Ensure it is visible
        } else {
            summaryContainer.style.display = 'none';  // Hide the box if no summary
        }
    }

});
