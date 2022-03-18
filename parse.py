# Create txt file of russian words

'''
import requests
response = requests.get('https://raw.githubusercontent.com/danakt/russian-words/master/russian.txt')

text = response.content.decode('cp1251')

with open('russian.txt', 'wb') as ru:
    ru.write(text.encode('utf-8'))
'''

not_parse = open("notparsewords.txt", "r", encoding="utf-8")
parse = open("guess_words.txt", "w", encoding="utf-8")

for line in not_parse:
    count = 0
    current_word = ''
    last = ''
    for c in line:
        #print(c)
        if c == '\t' and last != ' ' and last != '\t':
            count += 1
            if count == 2 and len(current_word) == 5:
                parse.write(current_word + '\n')
                print(current_word)
            current_word = ''
        elif c == ' ' and last != ' ' and last != '\t':
            count += 1
            if count == 2 and len(current_word) == 5:
                parse.write(current_word + '\n')
                print(current_word)
            current_word = ''
        elif c != ' ' and c != '\t':
            current_word += c
        last = c


