import os
import pickle
import random


def read_data_from_folder(folder_path):
    all_text = ''
    for file in os.listdir(path=folder_path):
        if file.endswith('.txt'):
            with open(file, encoding='ANSI') as f:
                my_text = f.read()
            all_text += my_text
    return all_text


def make_dict(data):
    dict_of_words = {}
    words = data.split(' ')
    index = 2

    dict_of_words['Beginning'] = {}
    dict_of_words['Beginning'].update({words[0]: 1})

    for word in words[2:]:
        word_low = word.lower()
        key = ' '.join(words[index - 1: index]).lower()
        if key in dict_of_words:
            if key.endswith('.') or key.endswith('!') or key.endswith('?') or key.endswith('...'):
                if 'Ending' in dict_of_words[key]:
                    dict_of_words[key]['Ending'] += 1
                else:
                    dict_of_words[key].update({'Ending': 1})

                if word in dict_of_words['Beginning']:
                    dict_of_words['Beginning'][word] += 1
                else:
                    dict_of_words['Beginning'].update({word: 1})
            else:
                if word_low in dict_of_words[key]:
                    dict_of_words[key][word_low] += 1
                else:
                    dict_of_words[key].update({word_low: 1})
        else:
            if key.endswith('.') or key.endswith('!') or key.endswith('?') or key.endswith('...'):
                dict_of_words[key] = {}
                dict_of_words[key].update({'Ending': 1})
            else:
                dict_of_words[key] = {}
                dict_of_words[key].update({word_low: 1})
        index += 1

    return dict_of_words


def download_dict(my_dict, file_name):
    with open(file_name, 'wb') as out:
        pickle.dump(my_dict, out)


def dictionary(file_name):
    with open(file_name, 'rb') as inp:
        loaded_dict = pickle.load(inp)
    return loaded_dict


def make_text(my_dict, text_length):
    my_values = []
    my_weights = []
    for k, v in my_dict['Beginning'].items():
        my_values.append(k)
        my_weights.append(v)
    first_word = random.choices(my_values, weights=my_weights)
    text = ''.join(first_word) + ' '
    prefix = ''.join(first_word)

    for i in range(text_length):
        try:
            my_values = []
            my_weights = []
            if prefix == 'Beginning':
                for k, v in my_dict['Beginning'].items():
                    my_values.append(k)
                    my_weights.append(v)
            else:
                for k, v in my_dict[prefix.lower()].items():
                    my_values.append(k)
                    my_weights.append(v)
            new_word = ''.join(random.choices(my_values, weights=my_weights))
            if new_word == 'Ending':
                prefix = 'Beginning'
            else:
                text += new_word + ' '
                prefix = new_word

        except KeyError:
            return text

    return text


my_dictionary = make_dict(read_data_from_folder('C:\Александра\Прога\генератор текстов\тексты'))
download_dict(my_dictionary, 'C:\Александра\Прога\генератор текстов\dictionary.txt')
print(make_text(dictionary('C:\Александра\Прога\генератор текстов\dictionary.txt'), 1000))
