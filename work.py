import random

words = ['']
alfabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
words_file = open('words.txt', 'r', encoding="utf-8")

def init():
    for c in words_file:
        c = c.replace('\n', '')
        words.append(c)

def get_word():
    return random.choice(words)

def check_user_message(text : str):
    if len(text) != 5:
        return False
    for c in text:
        if c not in alfabet:
            return False
    return True

def get_verdict(hidden_word : str, user_word : str):
    #print(hidden_word)
    #print(user_word)
    verdict = [0 for c in range(5)]
    for i in range(len(hidden_word)):
        if hidden_word[i] == user_word[i]:
            verdict[i] = 2
        elif user_word[i] in hidden_word:
            verdict[i] = 1
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