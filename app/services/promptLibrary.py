

promptDict = {
            "noteTaker":
                        """You are a highly efficient and detail-oriented note-taker. Your task is to read through the following text and extract all important points, minutes, or actionable details. Respond with an organized summary which follows these guidelines
                        Guidelines:
                        Identify Key Information: Focus on the main ideas and critical details
                        Organize Logically: Group related information under appropriate headings or categories.
                        Simplify Complex Ideas: Summarize complex or cluttered sentences into simple, understandable phrases.
                        Be Concise: Use bullet points for clarity and brevity.
                        Include Context: Where necessary, provide brief context to ensure clarity.
                        Formatting: Do not acknowledge the prompt in the output. For example do not start with "I'd be happy to help you extract important points from the text!"

                        Input Text:
                        {text}

                        Summary:
                        """,


            "titlePrompt":
                        """Respond with a short title not exceeding 8 words for the following text: {text}.""",

            "tagPrompt": 
                        """Given the following text: {text}, choose the most appropriate tags from the following list: {tags}
                        
                        Guidelines:
                        Select only tags from the given choices
                        If multiple tags are relevant, choose all that apply and output them as a comma-separated list

                        Selected Tags: 

                        Example Usage 1:
                        Input Text:
                        "Today’s meeting was a bit chaotic. First, we discussed the budget for the new project but didn’t finalize anything. Sarah mentioned some issues with the timeline and requested an extension. Meanwhile, Mike brought up marketing strategies, but it was clear no one had prepared, so it was left for the next meeting. We also talked about hiring interns for the summer, but again, no decision was made. Overall, lots of ideas but not much progress."

                        AI Response (as Tag Selector):

                        Selected Tags: Work

                        Example Usage 2:

                        Input Text:
                        "Japan is a country known for its rich cultural heritage and delicious cuisine. One of the most popular dishes is sushi, which consists of vinegared rice accompanied by various ingredients such as seafood, vegetables, and occasionally tropical fruits. Sushi is often served with pickled ginger, wasabi, and soy sauce. The art of sushi-making is a revered skill in Japan, and many travelers visit the country to experience authentic sushi prepared by master chefs."

                        AI Response (as Tag Selector):

                        Selected Tags: Travel, Food
                        """
}


EXAMPLE1 = """
    Okay, so here we go. Today was... I don’t even know where to start. Like, I knew traveling on a budget would be tough,but Barcelona is testing me in ways I did NOT sign up for.

    First off, breakfast. I thought I was being clever, grabbing a €2 croissant and coffee combo from some corner café. But, surprise! The croissant was basically air wrapped in sadness, and the coffee? If you can even call it that. It tasted like regret. I miss my instant coffee back home. Who even am I?!

    Then I tried to do the whole "explore the city on foot" thing. I mean, who needs public transport when you’ve got legs, right? WRONG. My legs are now noodles, thank you very much. I walked from my hostel near La Rambla to Park Güell because, you know, Google Maps said it was only like 45 minutes. Lies. It felt like I was trekking to Mordor. And when I got there? Oh, the views are nice, sure, but they charge you to get into the cool part of the park. What?! Gaudí must be rolling in his grave. Or maybe he’s laughing. I wouldn’t blame him.

    Lunchtime was another saga. Found this “authentic” tapas bar, thinking I’d finally hit the jackpot. Nope. Paid €12 for three pieces of bread with random stuff on top. A bit of ham here, some kind of fish paste there, and... an olive. Just one. I think they expect you to cry into your plate to add salt to the flavor.

    Also, what’s with all the pickpocket warnings? I swear every two minutes someone’s yelling, “Watch your bag!” Like, I get it. I’m clutching my backpack like it’s my firstborn. Chill.

    Oh, and the Sagrada Família. It’s stunning, don’t get me wrong, but I thought, "Hey, I’ll just admire it from the outside, save some cash." Guess what? Even just standing there, I got roped into buying some cheesy souvenir from a street vendor. It’s a mini Sagrada Familia, made of plastic, and I already hate it. But it’s in my bag now, so... yay memories?

    Dinner. Oh, dinner. Supermarkets are my new best friend, apparently. Grabbed a baguette, some cheese, and a carton of wine because I’m that person now. Ate it sitting on some random bench while watching happy tourists at fancy restaurants. Honestly, though, the wine was okay. Cheap but okay. Silver lining?

    By the end of the day, I was so tired I didn’t even bother with the hostel social thing. Everyone’s out at clubs or whatever, and I’m here, in bed, writing this. My feet hurt, my wallet is crying, but hey, at least I’m in Barcelona, right? Ugh. Tomorrow better redeem itself."""



title_example="""
                        Title:
                        
                        Example Usage:
                        
                        Input Text:
                        "Today’s meeting was a bit chaotic. First, we discussed the budget for the new project but didn’t finalize anything. Sarah mentioned some issues with the timeline and requested an extension. Meanwhile, Mike brought up marketing strategies, but it was clear no one had prepared, so it was left for the next meeting. We also talked about hiring interns for the summer, but again, no decision was made. Overall, lots of ideas but not much progress."

                        AI Response (as Title Generator):

                        Title: Unproductive & Chaotic Meeting """


summary_example = """Example Usage 1:
                        Input Text:
                        "Today’s meeting was a bit chaotic. First, we discussed the budget for the new project but didn’t finalize anything. Sarah mentioned some issues with the timeline and requested an extension. Meanwhile, Mike brought up marketing strategies, but it was clear no one had prepared, so it was left for the next meeting. We also talked about hiring interns for the summer, but again, no decision was made. Overall, lots of ideas but not much progress."

                        AI Response (as Note-Taker):

                        Discussion Points:
                        - Budget for new project discussed but not finalized.
                        - Timeline issues raised by Sarah; extension requested.
                        - Marketing strategies brought up by Mike; deferred due to lack of preparation.
                        - Intern hiring discussed for summer; no decisions made.


                        Example Usage 2:

                        Input Text:
                        "Ah, Japan. I can still remember the trip like it was yesterday. What stood out the most—aside from the temples and all that history—was the food. Sushi, oh my goodness. The real deal over there is nothing like the stuff you get back home. I remember sitting at this tiny sushi bar, the chef slicing fish with this precision that felt almost meditative. There’s something so simple yet perfect about it—just vinegared rice, fresh seafood, and maybe a touch of wasabi. Oh, and they always serve it with pickled ginger and soy sauce; it’s like a little ritual. Honestly, I didn’t even like wasabi before, but something about the way they do it there just made it all click. I could feel how much respect they have for the craft. It’s not just food; it’s an art form. I think I even overheard someone say that people travel across the globe just for a plate of authentic sushi. Yeah, I totally get it now."

                        AI Response (as Note-Taker):

                        Cultural Significance:  
                        - Japan is renowned for its rich cultural heritage, including its traditional cuisine.

                        About Sushi:  
                        - Sushi is a popular dish made of vinegared rice paired with ingredients such as seafood, vegetables, or tropical fruits.  
                        - It is commonly served with pickled ginger, wasabi, and soy sauce.

                        Art of Sushi-Making:  
                        - Sushi preparation is considered a revered skill in Japan.  
                        - Master chefs dedicate years to perfecting the craft, elevating it to an art form.

                        Tourism Appeal:  
                        - Many travelers visit Japan specifically to experience authentic sushi made by expert chefs.
"""