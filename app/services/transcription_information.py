import numpy as np

all_tags = ['Work', 'Reflection', 'Food', 'Travel']
all_titles = ['Working from Home', 'Working from Work', 'Depression', 'Ending Things', 'Another Day', 'Racism']

def get_title_summary_tags_from_transcription(transcription):
    num_tags = np.random.randint(0, len(all_tags), 1)
    tags = np.random.choice(all_tags, size=num_tags, replace=False).tolist()

    title = np.random.choice(all_titles, size=1, replace=False).tolist()[0]

    summary = "This is the temporary summary"
    return title, summary, tags