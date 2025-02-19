import pandas as pd
import requests
from bs4 import BeautifulSoup
from text_analyzer import TextAnalyzer


def scrape_article(URL: str):
    """Scrape article data from URL. Return title, text, and title + text."""
    try:
        # extract url and parse using BeautifulSoup
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        # get title for article
        title = soup.title.string.replace(" - Blackcoffer Insights", "")
        if not title.endswith("."):
            title += "."
        # in case the article does not exist
        if "Page not found" in title:
            return pd.NA, pd.NA

        else:
            # find main content text id
            content = soup.find_all("div", class_="td-post-content")[0]
            # Find and remove the specified <pre> tag
            pre_tag = content.find('pre', class_='wp-block-preformatted')
            if pre_tag:
                pre_tag.extract()
            # get text of html
            text = content.get_text()
            return title, text
    except Exception as e:
        print(f"Error processing URL: {URL}")
        print(e)
        return pd.NA, pd.NA


def get_ouptut_df_calcs(df_output: pd.DataFrame, text_list: list) -> pd.DataFrame:
    """Return output dataframe with calculations"""
    positive_scores, negative_scores, polarity_scores, subjectivity_scores, avg_sentence_lengths, percentage_of_complex_words_list, fog_indexes, avg_words_per_sentence_list, complex_word_counts, word_counts, syllables_per_word_list, pronoun_counts, avg_word_lengths = [], [], [], [], [], [], [], [], [], [], [], [], []

    for text in text_list:

            if pd.isna(text):
                positive_scores.append(pd.NA)
                negative_scores.append(pd.NA)
                polarity_scores.append(pd.NA)
                subjectivity_scores.append(pd.NA)
                avg_sentence_lengths.append(pd.NA)
                percentage_of_complex_words_list.append(pd.NA)
                fog_indexes.append(pd.NA)
                avg_words_per_sentence_list.append(pd.NA)
                complex_word_counts.append(pd.NA)
                word_counts.append(pd.NA)
                syllables_per_word_list.append(pd.NA)
                pronoun_counts.append(pd.NA)
                avg_word_lengths.append(pd.NA)

            else:
                text_analyzer = TextAnalyzer(text=text)

                positive_scores.append(text_analyzer.positive_score)
                negative_scores.append(text_analyzer.negative_score)
                polarity_scores.append(text_analyzer.polarity_score)
                subjectivity_scores.append(text_analyzer.subjectivity_score)
                avg_sentence_lengths.append(text_analyzer.avg_sentence_length)
                percentage_of_complex_words_list.append(text_analyzer.percentage_complex_words)
                fog_indexes.append(text_analyzer.fog_index)
                avg_words_per_sentence_list.append(text_analyzer.avg_words_per_sentence)
                complex_word_counts.append(text_analyzer.num_complex_words)
                word_counts.append(text_analyzer.num_words)
                syllables_per_word_list.append(text_analyzer.syllables_per_word)
                pronoun_counts.append(text_analyzer.pronoun_count)
                avg_word_lengths.append(text_analyzer.avg_word_length)

    df_output["POSITIVE SCORE"] = positive_scores
    df_output["NEGATIVE SCORE"] = negative_scores
    df_output["POLARITY SCORE"] = polarity_scores
    df_output["SUBJECTIVITY SCORE"] = subjectivity_scores
    df_output["AVG SENTENCE LENGTH"] = avg_sentence_lengths
    df_output["PERCENTAGE OF COMPLEX WORDS"] = percentage_of_complex_words_list
    df_output["FOG INDEX"] = fog_indexes
    df_output["AVG NUMBER OF WORDS PER SENTENCE"] = avg_words_per_sentence_list
    df_output["COMPLEX WORD COUNT"] = complex_word_counts
    df_output["WORD COUNT"] = word_counts
    df_output["SYLLABLE PER WORD"] = syllables_per_word_list
    df_output["PERSONAL PRONOUNS"] = pronoun_counts
    df_output["AVG WORD LENGTH"] = avg_word_lengths

    return df_output


def main():

    df = pd.read_excel("../data/Input.xlsx")
    df_output = pd.read_excel("../data/Output Data Structure.xlsx")

    titles, texts = [], []

    # loop to run all articles
    for i in range(len(df)):
        # get article URL
        URL = df.URL[i]

        title, text = scrape_article(URL)

        titles.append(title)
        texts.append(text)

    # add lists as df columns
    df["TITLE"] = titles
    df["TEXT"] = texts
    df["FULL_TEXT"] = df.TITLE + ' ' + df.TEXT

    df_output = get_ouptut_df_calcs(df_output, df.FULL_TEXT.tolist())

    df_output.to_csv("../output.csv", index=False)


if __name__ == "__main__":
    main()