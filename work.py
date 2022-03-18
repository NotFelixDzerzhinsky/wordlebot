import random
import requests

words = ['']
words_for_find = set()
alfabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
words_file = open('russian_words.txt', 'r', encoding="utf-8")

def init():
    for c in words_file:
        c = c.replace('\n', '')
        if len(c) == 5:
            words.append(c)
            words_for_find.add(c)

def get_word():
    return random.choice(words)

def check_user_message(text : str):
    for c in text:
        if c not in alfabet:
            return False
    if text not in words_for_find:
        return False
    return True

def get_verdict(hidden_word : str, user_word : str):
    count_letters = dict()
    verdict = [0 for c in range(5)]
    for i in range(len(hidden_word)):
        if hidden_word[i] not in count_letters:
            count_letters[hidden_word[i]] = 0
        count_letters[hidden_word[i]] += 1
    
    for i in range(len(hidden_word)):
        if hidden_word[i] == user_word[i]:
            verdict[i] = 2
            count_letters[user_word[i]] -= 1

    for i in range(len(hidden_word)):
        if verdict[i] == 0 and user_word[i] in count_letters and count_letters[user_word[i]] > 0:
            verdict[i] = 1
            count_letters[user_word[i]] -= 1

    str_verdict = ""
    for c in verdict:
        str_verdict += str(c)
    return str_verdict

def transform_verdict(verdict : str):
    result = ""
    for c in verdict:
        if c == '0':
            result += '⬛️'
        elif c == '1':
            result += '🟨'
        elif c == '2':
            result += '🟩'
        else:
            print("Something went wrong")

    return result

# 0  1  2
# ⬛️🟨🟩