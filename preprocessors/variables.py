import re
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS

# Patterns
pat_authors = re.compile(r"\[(.+?)\]")

# Patterns (stopwords)
# pat_pos = re.compile(r"NN[S|P|PS]{0,}|JJ[R|S]{0,}|PR\w{0,}|RB[R|S]{0,}|VB[D|G|N|P|Z]{0,}")
pat_pos = re.compile(r"NN[S|P|PS]{0,}|JJ[R|S]{0,}")
pat_stopwords = re.compile(r"|".join(list(map(lambda x: r"\b"+rf"{x}"+r"\b", STOP_WORDS))))
pat_punc_replace = re.compile(r"[\-\/\(\)\;\.\,\&]")
pat_punc_remove = re.compile(r"[^(a-zA-Z\d\s)]")
pat_tags = re.compile(r"\<(.+?)\>")
pat_paths = re.compile(r".+\/[a-zA-Z0-9]+")
pat_emails = re.compile(r".+\@")
pat_whitespaces = re.compile(r"\s{2,}")
