# Module imports
# Tweepy Module for Twitter APi
import tweepy

# Google News Module
from gnewsclient import gnewsclient

# Pandas Module
import pandas as pd

# Time Module
import time

###### Tweeter   Credentials###################
consumer_key = "cyURof8onxNo63Tdbc8d3mB4T"
consumer_secret = "JnKzJsPuLxi0Fa7BB26l7XTpwOYnoXD37Rqio0SpWsLi7QPN1n"
access_token = "1220785803078643713-9tG4OWTEa3ykTPm26l59uUd2nsYXfB"
access_token_secret = "TXpiUcgHfcBcvBpp2m9Zib0FDdZfw0ziPOyCeY27IGFJ5"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

########################################


#Translate Module
from googletrans import Translator

#Module Wikipedia
import wikipedia
# Random module
import random
# Json module
import json
# Pickle module
import pickle
# Numpy Module
import numpy as np
# Natural language tool kit module
import nltk
# Natural language tool kit stem module
from nltk.stem import WordNetLemmatizer

# Tensorflow models module to load in the model we trained
from tensorflow.keras.models import load_model

# Autocorrect -> spell check
from autocorrect import Speller


class Agent:
    """
        The class contains will contain the model that the chat bot will use to determine a response to user input.

        Attributes:
            lemmatizer (object): A wordnet lemmatizer object.
            intents (object): A JSON object containing all the structure of the neural net model.
            tags (list): A list containing all the response type tags from a pickle object.
            responses (list): A list containing all the responses from a pickle object.
            model (object): An object containing a trained model.

        Methods:
            deconstructSentence(): deconstructs sentences into their root words.
            spellCheck(): takes a sentence and corrects any spelling mistakes based on closest known word
            bagWords(): uses the deconstructed sentence to a series of words and maps it to a matching tag.
            predictResponse(): uses the chatbot model to return a response, with an associated probability.
            getResponse(): returns random bot response that has a greater probability than the minimum threshold.
            run(): runs the chatbot.
        """

    # Object constructor
    def __init__(self):
        # Create a lemmatizer object
        self.lemmatizer = WordNetLemmatizer()
        # read in intents.json file
        #path = 'P:/COSC310 - Software Engineering/Projects/Projects/Assignment3/NeuralNet_Agent/'
        file = open('intents.json')
        self.intents = json.loads(file.read())
        file.close()
        # load in the tags, and responses from the pickle files and load the saved model
        file = open('tags.pk1', 'rb')
        self.tags = pickle.load(file)
        file.close()
        file = open('responses.pk1', 'rb')
        self.responses = pickle.load(file)
        file.close()
        self.model = load_model('chatbotmodel.h5')
        self.check = Speller(lang='en')

    def spellCheck(self, sentence):
        """
        This method takes a sentence and corrects any spelling mistakes based on closest known word
        Parameters:
            sentence (str): a sentence of user input
        Returns:
            corrected (str): a spell corrected sentence
        """
        corrected = self.check(sentence)
        return corrected

    def deconstructSentence(self, sentence):
        """
        This is a methods takes sentence and deconstructs it into its words, and breaks
        each word into it's stem word.
        Parameters:
            sentence (str): a sentence from user input
        Returns:
            separatedWords (list): a list containing individual root words of a given sentence
        """
        separatedWords = nltk.word_tokenize(sentence.lower())
        # print(separatedWords)
        separatedWords = [self.lemmatizer.lemmatize(word) for word in separatedWords]
        # print(separatedWords)
        return separatedWords

    def bagWords(self, sentence):
        """
        This is a methods takes sentence and uses the deconstructSentence methods and creates a
        bag of words (the same length as the tags), that is, it constructs an array with zeros everywhere
        except where the tags matches a word from the sentence.
        Parameters:
            sentence (str): a sentence from user input
        Returns:
            bag (numpy array): an numpy array for the model
        """
        separatedWords = self.deconstructSentence(sentence)
        bag = [0] * len(self.tags)

        # each word in the list
        for word in separatedWords:
            # enumerate the list of tags
            for (i, key) in enumerate(self.tags):
                # print("This is the key:", key)
                # if a key matches a word, set the bag at the given index to 1
                if key == word:
                    bag[i] = 1
        return np.array(bag)

    def predictResponse(self, sentence):
        """
        This is a methods takes sentence and uses the bagWords methods and predicts the responses
        Parameters:
            sentence (str): a sentence from user input
        Returns:
            potentialResponses (list): a list with responses, and probability of that being the closest responses
        """
        if sentence.split(' ')[0].lower()=='tweets':
            try:
                username = sentence.split(' ')[1]
                count = 3

                tweets = []

                tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)

                tweets_list = [[tweet.text] for tweet in tweets]
                print(tweets_list)
                tweets_df = tweets_list
                # initialize an empty string
                str1 = "" 
                # traverse in the string  
                for ele in tweets_df:
                    str1 += ele[0]+'\n\n'
                print(str1)
                return str1
            except:
                return 'No user found'
        
        elif sentence.split(' ')[0].lower()=='wikipedia':
            try:
                word=sentence.split(' ')[1:]
                # initialize an empty string
                str1 = "" 
                # traverse in the string  
                for ele in word: 
                    str1 += ele  
                return wikipedia.summary(str1)
            except:
                return 'No Content found'
            
        elif sentence.split(' ')[0].lower()=='translate':
            try:
                dest=sentence.split(' ')[1]
                translator = Translator()
                word=sentence.split(' ')[2:]
                str1 = "" 
                # traverse in the string  
                for ele in word: 
                    str1 += ele  
                result = translator.translate(str1, dest=dest)
                return result.text
            except:
                return 'No translation found'
            
            
        elif sentence.split(' ')[0].lower()=='news':
            try:
                topic=sentence.split(' ')[1]
                res=sentence.split(' ')[2]
                client = gnewsclient.NewsClient( 
                                    topic=topic, 
                                    max_results=int(res))

                news_list = client.get_news()
                
                lst=[]
                for item in news_list:
                    lst.append(item['link'])
#                     print("Title : ", item['title'])
#                     print("Link : ", item['link'])
#                     print("")
                str1 = "" 
                # traverse in the string  
                for ele in lst: 
                    str1 += ele+'\n\n'
                return str1
            
            except:
                return 'No News Found'
            
            
            
            
        bow = self.bagWords(sentence)
        predictionModel = self.model.predict(np.array([bow]))[0]
        # Specify the error threshold
        ERROR_THRESHOLD = 0.25
        predictedResponses = [[i, r] for i, r in enumerate(predictionModel) if r > ERROR_THRESHOLD]

        predictedResponses.sort(key=lambda x: x[1], reverse=True)
        potentialReponses = []
        for r in predictedResponses:
            potentialReponses.append({'intent': self.responses[r[0]], 'probability': str(r[1])})
        # print(potentialReponses)
        return potentialReponses

    def getResponse(self, userSentence):
        """
        This is a methods takes the user input, retrieves the tags from the JSON
        and checks if it matches the tags from intents list and chooses a random response
        (of the appropriate responses) to return to the user
        Parameters:
            userSentence (list): a sentence from user input
        Returns:
            idealResponse (list): a randomly selected response to the user input
        """
        try:
            tag = userSentence[0]['intent']
            intents = self.intents['intents']
            for group in intents:
                if group['tag'] == tag:
                    idealResponse = random.choice(group['responses'])
                    break
            return idealResponse
        except:
            return userSentence

    def run(self):
        """
        This methods receives user input, and uses the predictResponse methods to determine what the user's intention
        is, then uses the getResponse methods to determine an ideal response to return.
        """
        print("Welcome, we are here to help you with your computer issues. Please type \"Hello\" "
              "or the type of issue you are having, to begin.")
        while True:
            userInput = input("Enter text: ")
            correctedInput = self.spellCheck(userInput)
            print(correctedInput)

            if correctedInput.lower() == 'quit':
                break
            intentions = self.predictResponse(correctedInput)
            botResponse = self.getResponse(intentions)
            print("Agent: " + botResponse)


# run the chat bot
def main():
    chatBot = Agent()
    chatBot.run()


if __name__ == '__main__':
    main()
