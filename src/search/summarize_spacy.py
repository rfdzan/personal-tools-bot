from heapq import nlargest

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.language import Language
from spacy.tokens import Token
from spacy.tokens.doc import Doc

stopword = list(STOP_WORDS)
nlp: Language = spacy.load(str("en_core_web_sm"))


async def tokenize_word(docx) -> list[str]:
    # token.text = tokenize, and convert to string.
    # allows for string methods to be applied to it
    mytoken = [token.text.lower() for token in docx]
    return mytoken


async def tokenize_sentence(docx: Doc) -> list[str]:
    list_of_sentence = [sent.text.lower() for sent in docx.sents]
    return list_of_sentence


async def remove_stopwords(docx: Doc) -> list[Token]:
    filter_stopword = []
    for word in docx:
        text_token = word.text
        if text_token not in stopword:
            filter_stopword.append(word)
    return filter_stopword


async def get_word_frequency(filter_stopword: list) -> dict[str, int]:
    word_frequency: dict[str, int] = {}
    for word in filter_stopword:
        text_token = word.text
        if text_token not in word_frequency.keys():
            word_frequency[text_token] = 1
        else:
            word_frequency[text_token] += 1
    return word_frequency


async def get_word_weights(word_frequency: dict[str, int]) -> dict[str, float]:
    word_max_freq = max(word_frequency.values())
    weighted_words = {}
    for word in word_frequency.keys():
        if word_frequency.get(word) is not None:
            weighted_words[word] = (
                word_frequency.get(word) / word_max_freq
            )  # division elapsed time is pretty awful
    return weighted_words


async def rank_score_sents(docx: Doc, weighted_words: dict[str, str]) -> dict[str, str]:
    score: dict[str, str] = {}
    sents_list = await tokenize_sentence(docx)
    words_list = await tokenize_word(docx)
    for sent in sents_list:
        for word in words_list:
            if word in weighted_words.keys() and sent not in score.keys():
                score[sent] = weighted_words[word]
            elif word in weighted_words.keys() and sent in score.keys():
                score[sent] += weighted_words[word]
    return score


async def nlargest_summary(score: dict, x_largest: int) -> list:
    nlargest_summary = nlargest(x_largest, score, key=score.__getitem__)
    return nlargest_summary


async def main(text):
    docx: Doc = nlp(text)
    filtered_stopwords = await remove_stopwords(docx)
    word_freq = await get_word_frequency(filtered_stopwords)
    weighted_words = await get_word_weights(word_freq)
    score = await rank_score_sents(docx, weighted_words)
    prelim_summary = await nlargest_summary(score, 6)
    return " ".join(prelim_summary)
