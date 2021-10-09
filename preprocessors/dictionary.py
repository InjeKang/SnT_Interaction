import pandas as pd
import re
import swifter

def user_dict_creator(dataframe):
    keywords = dataframe.word.copy()
    keywords_replaced = keywords.swifter.apply(lambda x: re.sub(" ", "-", x))
    user_dict = {
        rf"\b{word_original}\b": word_replaced for word_original, word_replaced in zip(keywords, keywords_replaced) if "-" in word_replaced
    }
    user_dict_df = pd.DataFrame(user_dict.items(), columns=["word", "word_replaced"])
    return user_dict, user_dict_df