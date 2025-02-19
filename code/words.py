import os

class Words:
    def __init__(self, stopwords_path='../data/StopWords', positive_path='../data/MasterDictionary/positive-words.txt',
                 negative_path='../data/MasterDictionary/negative-words.txt'):
        self.stopwords_path = stopwords_path
        self.positive_path = positive_path
        self.negative_path = negative_path

    def get_all_stopwords(self) -> set:
        """Return set of all stopwords from files"""
        txt_files = [f for f in os.listdir(self.stopwords_path) if f.endswith('.txt')]
        stopword_set = set()
        
        for txt_file in txt_files:
            file_path = os.path.join(self.stopwords_path, txt_file)
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read().lower().splitlines()
                # remove and append roman numerals as all caps
                romans = None
                for index, word in enumerate(content):
                    if '| roman numerals' in word:
                        romans = content[index:]
                        romans = [roman.split('|')[0].strip() for roman in romans]
                        romans = [roman.upper() if len(roman) > 1 else roman for roman in romans]
                        break
                content = [stopword.split('|')[0].strip() for stopword in content]
                if romans:
                    content = content[:index] + romans
                content = set(content)
            stopword_set = stopword_set | content
        
        return stopword_set

    def get_sentiment_words(self, sentiment: str) -> set:
        """Return set of all words with the positive or negative sentiment from file"""
        sentiments = {
            "positive": self.positive_path,
            "negative": self.negative_path
        }

        if sentiment not in sentiments:
            raise ValueError("Sentiment must be 'positive' or 'negative'")
        else:
            with open(sentiments[sentiment], 'r', encoding='latin-1') as file:
                content = file.read().lower().splitlines()
                _words = set(content)

        stopwords = self.get_all_stopwords()
        _words = _words - stopwords

        return _words
