import numpy as np

all_tags = ['Work', 'Reflection', 'Food', 'Travel']
all_titles = ['Working from Home', 'Working from Work', 'Depression', 'Ending Things', 'Another Day', 'Racism']

def get_title_summary_tags_from_transcription(transcription):
    """
    Recieved the text from the audio note made by the user. Uses ollama along with llama3.2:3b to format the text 
    using a formatting prompt template to capture all the key points summarizing the important aspects of the text and 
    then returns the formatted text.
    Prompt should be such that the key points are captured in the summary and are easy to retrieve when doing retrieval using an 
    embedding model
    """
    
    formatted_text = ollama.generate(model='llama3.2:3b', prompt=promptDict['noteTaker'].format(text=text))['response']
    title = ollama.generate(model='llama3.2:3b', prompt=promptDict['titlePrompt'].format(text=text))['response']
    tag = ollama.generate(model='llama3.2:3b', prompt=promptDict['tagPrompt'].format(text=text, tags=tags))['response']

    # Extract tags using regex
    tag_list = [x for x in re.findall(r'\b\w+\b', tag) if x in tags]

    return title, formatted_text, tag_list



