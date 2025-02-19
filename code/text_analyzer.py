from nltk.tokenize import word_tokenize, sent_tokenize, SyllableTokenizer
import re
import warnings
from words import Words


class TextAnalyzer:
    """A class to analyze article text"""

    def __init__(self, text) -> None:
        self.text = text
        self.tokens_clean = self.clean_tokens()
        self.tokens = self.remove_stopwords()
        self.calculate_metrics()


    def get_tokens(self) -> list:
        """Get tokens from text"""
        # Remove newline characters and non-breaking spaces
        text = re.sub(r'\n|(\xa0)', ' ', self.text)
        # remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        # Tokenize the text into sentences
        self.sentences = sent_tokenize(text)
        # Replace punctuation with a space
        text = re.sub(r'[^\w\s]', ' ', text)
        # remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        # Tokenize the text into words/tokens
        tokens = word_tokenize(text)
        return tokens
    

    def clean_tokens(self) -> list:
        """
        If the length of the word is 1, i want to lower it.
        If the length of the word is more than 1 and it is all caps, I do not want to lower it.
        If the length of the word is more than 1 and only the first letter is caps, I want to lower it.
        """
        tokens = self.get_tokens()
        processed_words = []
        for word in tokens:
            if len(word) == 1:
                processed_words.append(word.lower())
            elif len(word) > 1 and word.isupper():
                processed_words.append(word)
            elif len(word) > 1 and word[0].isupper() and word[1:].islower():
                processed_words.append(word.lower())
            else:
                processed_words.append(word)
        return processed_words
    

    def remove_stopwords(self) -> list:
        """Get all stopwords and remove them from tokens"""
        words = Words()
        stopwords = words.get_all_stopwords()
        tokens = [token for token in self.tokens_clean if token not in stopwords]
        return tokens
    

    def get_pronoun_count(self) -> int:
        pronouns = {"i":0, "we":0, "my":0, "ours":0, "us":0}
        for pronoun in pronouns:
            pronouns[pronoun] += self.tokens_clean.count(pronoun)
        pronoun_count = sum(pronouns.values())
        return pronoun_count


    def average_word_length_calc(self) -> float:
        total_characters = sum(len(word) for word in self.tokens_clean)
        total_words = len(self.tokens_clean)
        return total_characters / total_words if total_words > 0 else 0
    

    def nsyl(self, word: str) -> int:
        """Count number of syllables in word"""
        try:
            word = int(word)
            return 1
        except ValueError:
            tokenizer = SyllableTokenizer()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                return len(tokenizer.tokenize(word))


    def count_complex_words(self) -> int:
        """Complex words are with more than 2 syllables. Return number of complex words"""
        complex_word_count = sum(1 for word in self.tokens if self.nsyl(word) > 2)
        return complex_word_count


    def nsyl_per_word(self) -> float:
        """Syllables per word"""
        nsyl_total = sum(self.nsyl(word) for word in self.tokens)
        total_words = len(self.tokens)
        return nsyl_total / total_words if total_words > 0 else 0
    

    def calculate_metrics(self) -> None:
        """Calculate the required metrics"""
        self.pronoun_count = self.get_pronoun_count()
        self.avg_word_length = self.average_word_length_calc()
        
        words = Words()
        positive_words = words.get_sentiment_words("positive")
        negative_words = words.get_sentiment_words("negative")

        self.positive_score = sum(1 for word in self.tokens if word in positive_words)
        self.negative_score = sum(1 for word in self.tokens if word in negative_words)
        self.polarity_score = (self.positive_score - self.negative_score) / ((self.positive_score + self.negative_score) + 0.000001)

        self.num_sentences = len(self.sentences)
        self.num_words = len(self.tokens)

        self.num_complex_words = self.count_complex_words()
        self.syllables_per_word = self.nsyl_per_word()

        self.subjectivity_score = (self.positive_score + self.negative_score) / (self.num_words + 0.000001)
        self.avg_sentence_length = self.num_words / self.num_sentences
        self.percentage_complex_words = (self.num_complex_words / self.num_words) * 100
        self.fog_index = 0.4 * (self.avg_sentence_length + self.percentage_complex_words)
        self.avg_words_per_sentence = self.num_words / self.num_sentences
