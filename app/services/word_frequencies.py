import json
import os
import re
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

from app.routes.new_entry import NOTES_DIR

WORDCLOUD_PATH = 'static/wordcloud/wordcloud.png'

stopwords = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'can', "can't", 'cannot', 'could', "couldn't",
    'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during',
    'each',
    'few', 'for', 'from', 'further',
    'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's",
    'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself',
    'let', "let's", 'like', 'yeah', 'uh', 'something',
    'me', 'more', 'most', "mustn't", 'my', 'myself',
    'no', 'nor', 'not',
    'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such',
    'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up',
    'very', 'don', 'right', 'left',
    'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't",
    'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'
}

def generate_word_frequencies():
    """
    Generate word frequencies from the summaries of all notes.

    Returns:
        list: A list of [word, frequency] pairs sorted by frequency.
    """
    word_counter = Counter()

    # Iterate through all the notes and accumulate words from summaries
    for note_id in os.listdir(NOTES_DIR):
        note_path = os.path.join(NOTES_DIR, note_id, f"data.json")
        if os.path.isfile(note_path):
            with open(note_path, 'r') as note_file:
                note_data = json.load(note_file)
                summary = note_data.get('transcription', "")

                # Normalize and clean the text
                words = re.findall(r'\b\w+\b', summary.lower())
                word_counter.update([word for word in words if word not in stopwords.union(set(STOPWORDS)) and len(word) > 2])

    # Convert counter to a list of [word, frequency] pairs, sorted by frequency
    return word_counter


def generate_wordcloud():
    """
    Generate a word cloud from the summaries of all notes and save it as an image.

    Returns:
        str: Path to the saved word cloud image.
    """
    # Generate word frequencies from summaries
    word_frequencies = generate_word_frequencies()

    # Create a WordCloud instance
    wordcloud = WordCloud(width=800, height=400, background_color="rgba(255, 255, 255, 0)", mode="RGBA", colormap='viridis')

    # Generate the word cloud using word frequencies
    wordcloud.generate_from_frequencies(word_frequencies)

    # Save the word cloud image
    if not os.path.exists(os.path.dirname('app/' + WORDCLOUD_PATH)):
        os.makedirs(os.path.dirname('app/' + WORDCLOUD_PATH))

    wordcloud.to_file('app/' + WORDCLOUD_PATH)

    return WORDCLOUD_PATH