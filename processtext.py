import re

def get_words(file_name):
    words_file = open(file_name, 'r', encoding="utf8")
    text = words_file.read()
    words = text.split(" ")
def process_words(words):
    word_dict = {}
    for index,word in enumerate(words):
        unvocalized_word = re.sub(r'[ְֱִֵֶַָֹֻּ]', '', word, flags=re.IGNORECASE)
        fully_unvocalized_word = re.sub(r'[שׁשׂ]', 'ש', unvocalized_word, flags=re.IGNORECASE)
        if fully_unvocalized_word in word_dict.keys():
            word_dict[fully_unvocalized_word][1] += 1
            tzurot_dict = word_dict[fully_unvocalized_word][0]
            if tzurot_dict is None:
                word_dict[fully_unvocalized_word][0] = {}
                word_dict[fully_unvocalized_word][0][word] = list()
                word_dict[fully_unvocalized_word][0][word].append(index)
            else:
                if word in word_dict[fully_unvocalized_word][0].keys():
                    word_dict[fully_unvocalized_word][0][word].append(index)
                else:
                    word_dict[fully_unvocalized_word][0][word] = list()
                    word_dict[fully_unvocalized_word][0][word].append(index)
        else:
            word_dict[fully_unvocalized_word] = list()
            word_dict[fully_unvocalized_word].append({word: [index]})
            word_dict[fully_unvocalized_word].append(1)
    return word_dict

def generate_suggestions(tzurah_family):
    ordered_tzurot = dict(sorted(tzurah_family[0].items(), key=lambda kv: len(kv[1]), reverse=True))
    most_common = next(iter(ordered_tzurot))
    ordered_tzurot.pop(most_common)
    if((len(tzurah_family[0][most_common]) * 1.5) > tzurah_family[1]):
        suggestions = {'best_guess': most_common, 'fixes': ordered_tzurot}
        return suggestions

def compile_suggestions(corpus):
    corpus_words = get_words(corpus)
    tzurot_hash = process_words(corpus_words)
    suggestions = []
    for tzurah_index in tzurot_hash:
        tzurah_family = tzurot_hash[tzurah_index]
        suspicious_tzurot = generate_suggestions(tzurah_family)  
        if suspicious_tzurot is not None:
            suggestions.append(suspicious_tzurot)
    return {'words': corpus_words, 'suggestions': suggestions}