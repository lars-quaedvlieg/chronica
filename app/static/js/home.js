document.addEventListener('DOMContentLoaded', async function () {
    const wordcloudImage = document.getElementById('wordcloud-image');

    try {
        // Fetch the wordcloud image from the backend
        const response = await fetch('/wordcloud');
        console.log(response);

        if (response.ok) {
            // Get the blob data and create an object URL to display the image
            const blob = await response.blob();
            // Set the image URL to the wordcloud image element
            wordcloudImage.src = URL.createObjectURL(blob);
        } else {
            console.error('Failed to load wordcloud image:', response.statusText);
            wordcloudImage.alt = 'There is not enough data for the world cloud to be generated';
        }
    } catch (error) {
        console.error('Error fetching wordcloud image:', error);
        wordcloudImage.alt = 'There is not enough data for the world cloud to be generated';
    }
});
