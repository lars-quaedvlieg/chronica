document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('input[name="filter"]');
    const searchBar = document.getElementById('search-bar');
    const notesContainer = document.getElementById('notes-container');

    // Get notes data from the script tag
    const notesData = document.getElementById('notes-data').textContent;
    const notes = JSON.parse(notesData);

    // Function to group notes by different time periods
    function groupNotesByFilter(notes, filter) {
        const groupedNotes = {};

        notes.forEach(note => {
            const noteDate = new Date(note.datetime);
            let groupKey;

            if (filter === 'month') {
                groupKey = noteDate.toLocaleString('default', { month: 'long', year: 'numeric' });
            } else if (filter === 'week') {
                const startOfYear = new Date(noteDate.getFullYear(), 0, 1);
                const weekNumber = Math.ceil((((noteDate - startOfYear) / 86400000) + startOfYear.getDay() + 1) / 7);
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

        let hasNotes = false; // Track if there are any notes to display

        for (const [groupKey, notes] of Object.entries(groupedNotes)) {
            if (notes.length === 0) continue; // Skip categories without notes

            hasNotes = true; // Found notes to display
            const groupSection = document.createElement('div');
            groupSection.classList.add('mb-4');

            // Add group label (month, week, year)
            const groupLabel = document.createElement('h3');
            groupLabel.classList.add('month-label', 'mb-3');
            groupLabel.textContent = groupKey;
            groupSection.appendChild(groupLabel);

            // Create a grid for the notes in this group
            const notesGrid = document.createElement('div');
            notesGrid.classList.add('row', 'g-4'); // Bootstrap row with gutter for spacing

            notes.forEach(note => {
                const noteCardContainer = document.createElement('div');
                noteCardContainer.classList.add('col-lg-4', 'col-md-6', 'col-sm-12', 'mb-4'); // Responsive column sizes

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

                // Append tags
                const tagsContainer = document.createElement('div');
                tagsContainer.classList.add('mb-2');
                note.tags.forEach(tag => {
                    const tagBadge = document.createElement('span');
                    tagBadge.classList.add('badge', 'badge-primary', 'mr-1');
                    tagBadge.textContent = tag;
                    tagsContainer.appendChild(tagBadge);
                });

                // View Note Button
                const viewNoteButton = document.createElement('a');
                viewNoteButton.classList.add('btn', 'btn-primary', 'mt-3');
                viewNoteButton.href = `/view_entry/${note.id}`;
                viewNoteButton.textContent = 'View Note';

                // Append content to card body
                cardBody.appendChild(cardTitle);
                cardBody.appendChild(tagsContainer);
                cardBody.appendChild(cardDatetime);
                cardBody.appendChild(viewNoteButton);

                // Append card body to card
                card.appendChild(cardBody);

                // Append card to note card container
                noteCardContainer.appendChild(card);

                // Add card to grid
                notesGrid.appendChild(noteCardContainer);
            });

            // Add notes grid to the group section
            groupSection.appendChild(notesGrid);

            // Append group section to the container
            notesContainer.appendChild(groupSection);
        }

        // Display a message if no notes are found
        if (!hasNotes) {
            const noResultsMessage = document.createElement('p');
            noResultsMessage.textContent = 'No notes match your search.';
            noResultsMessage.classList.add('no-results-message', 'text-center', 'mt-4');
            notesContainer.appendChild(noResultsMessage);
        }
    }

    // Initial render grouped by month
    let currentFilter = 'month';
    const groupedNotes = groupNotesByFilter(notes, currentFilter);
    renderNotes(groupedNotes);

    // Event Listener for Filter Buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            currentFilter = event.target.value;
            const groupedNotes = groupNotesByFilter(notes, currentFilter);
            renderNotes(groupedNotes);
        });
    });

    // Event Listener for Search Bar
    searchBar.addEventListener('input', () => {
        const searchQuery = searchBar.value.toLowerCase();
        const filteredNotes = notes.filter(note =>
            note.title.toLowerCase().includes(searchQuery)
        );
        const groupedNotes = groupNotesByFilter(filteredNotes, currentFilter);
        renderNotes(groupedNotes);
    });
});
