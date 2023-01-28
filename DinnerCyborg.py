from collections import Counter

import spacy

from responses import blank_spot, responses
from user_functions import (compare_overlap, compute_similarity, extract_nouns,
                            pos_tag, preprocess)

word2vec = spacy.load('en')

exit_commands = ("quit", "goodbye", "exit", "no")

class ChatBot:
    
    def make_exit(self, user_message):
        for o in exit_commands:
            if o in user_message:
                print("goodbye!")
                return True 

    def chat(self):
        user_message = input("Hola! What is to your gusto? ")
        while not self.make_exit(user_message):
            self.respond(user_message)


    def find_intent_match(self, responses, user_message):
        bow_user_message = Counter(preprocess(user_message))
        processed_responses = [Counter(preprocess(r)) for r in responses]
        similarity_list = [compare_overlap(doc, bow_user_message) for doc in processed_responses]   
        response_index = similarity_list.index(max(similarity_list))
        return responses[response_index]

    def find_entities(self, user_message):
        message_nouns = extract_nouns(pos_tag(preprocess(user_message)))
        tokens = word2vec(" ".join(message_nouns))
        category = word2vec(blank_spot)
        word2vec_result = compute_similarity(tokens, category)
        word2vec_result.sort(key=lambda x: x[2])
        if len(word2vec_result) > 0:
            return word2vec_result[-1][0]
        else:
            return blank_spot

    def respond(self, user_message):
        best_response = self.find_intent_match(responses, user_message)
        entity = self.find_entities(user_message)
        print(best_response.format(entity))
        input_message = input("Anything más? ")
        return input_message

#call .chat() method below:
chatBotInstance = ChatBot()
chatBotInstance.chat()




