from re import sub
import operator


def popular_words(name, n):
    words_occurrences, top_words = {}, {}
    with open(name, encoding='utf-8') as file:
        for line in file:
            line = sub(r'[^\w\s]', '', line.strip())
            words_in_line = line.lower().strip(' ').split(' ')
            for word in words_in_line:
                if word != '':
                    if word not in words_occurrences.keys():
                        words_occurrences[word] = 1
                    else:
                        words_occurrences[word] = words_occurrences[word] + 1

    words_occurrences = dict(sorted(words_occurrences.items(), key=operator.itemgetter(1), reverse=True))

    top_word = list(words_occurrences)[0]
    top_words[top_word] = words_occurrences[top_word]
    n_top_occurrences = 1
    for word, occurrence_number in words_occurrences.items():
        if n_top_occurrences == n:
            break
        if occurrence_number in top_words.values():
            top_words[word] = occurrence_number
        else:
            top_words[word] = occurrence_number
            n_top_occurrences += 1

    return top_words


if __name__ == '__main__':
    file_name = 'potop.txt'
    print(popular_words(file_name, 3))