import os
import json

alphabet_list = ['ա', 'բ', 'գ', 'դ', 'ե', 'զ', 'է', 'ը', 'թ', 'ժ', 'ի', 'լ', 'խ', 'ծ', 'կ', 'հ', 'ձ', 'ղ', 'ճ', 'մ',
                 'յ', 'ն', 'շ', 'ո', 'չ', 'պ', 'ջ', 'ռ', 'ս', 'վ', 'տ', 'ր', 'ց', 'ւ', 'փ', 'ք', 'և', 'օ', 'ֆ', 'Ա',
                 'Բ', 'և', 'Ս', 'Դ', 'Է', 'Ե', 'Ֆ', 'Գ', 'Հ', 'Ի', 'Ժ', 'Ճ', 'Ջ', 'Չ', 'Լ', 'Մ', 'Ն', 'Օ', 'Ո', 'Ւ',
                 'Փ', 'Պ', 'Ր', 'Ռ', 'Վ', 'Յ', 'Զ', 'Ը', 'Թ', 'Տ', 'Ղ', 'Խ', 'Կ', 'Ք', 'Շ', 'Ձ', 'Ծ', 'Ց']


def distance(a: str, b: str) -> int:
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    array = [[i] for i in range(m + 1)]
    array[0] = list(range(n + 1))
    for i in range(1, m + 1):
        for j in range(n):
            if b[i - 1] != a[j]:
                array[i].append(min(array[i - 1][j] + 1, array[i - 1][j + 1] + 1, array[i][j] + 1))
            else:
                array[i].append(min(array[i - 1][j], array[i - 1][j + 1] + 1, array[i][j] + 1))
    return array.pop().pop()


def soundex(string: str) -> tuple:
    encoding_table = {'Ա': 0, 'Բ': 1, 'ԵՒ': 1, 'Ս': 2, 'Դ': 3, 'Է': 0, 'Ե': 0, 'Ֆ': 1, 'Գ': 2, 'Հ': 0, 'Ի': 0, 'Ժ': 2,
                      'Ճ': 2, 'Ջ': 2, 'Չ': 2, 'Լ': 4, 'Մ': 5, 'Ն': 5, 'Օ': 0, 'Ո': 0, 'Ւ': 0, 'Փ': 1, 'Պ': 1, 'Ր': 6,
                      'Ռ': 6, 'Վ': 1, 'Յ': 0, 'Զ': 2, 'Ը': 0, 'Թ': 3, 'Տ': 3, 'Ղ': 6, 'Խ': 6, 'Կ': 2, 'Ք': 2, 'Շ': 2,
                      'Ձ': 3, 'Ծ': 3, 'Ց': 3, ' ': 0}
    encode = ''.join([str(encoding_table[i.upper()]) for i in string[1:] if i != "\r"]).strip('0')
    encode_soundex = '000'
    count = 0
    flag = False
    i = 0
    for i in encode:
        if count == 3:
            break
        if i != '0':
            if encode_soundex[count - 1] != i or flag:
                encode_soundex = encode_soundex.replace('0', i, 1)
                count += 1
                flag = False
        else:
            flag = True

    return ''.join([string[0].upper(), encode_soundex]), True if encode and i == encode[-1] else False


def create_soundex_file():
    soundex_dict = {}
    with open(os.path.normpath('encyclopedia.text'), 'rb') as f:
        for line in f:
            line = line.decode().rstrip('\n')
            try:
                soundex_encrypt = soundex(line)
            except KeyError as e:
                print(e)
            line = line.replace('\r', '')
            if not soundex_dict.get(soundex_encrypt[0]):
                soundex_dict.update({f'{soundex_encrypt[0]}': [line]})
            else:
                if line not in soundex_dict.get(soundex_encrypt[0]):
                    soundex_dict.get(soundex_encrypt[0]).append(line)
    json.dump(soundex_dict, open(os.path.normpath('soundexFile.text'), 'w'))


def is_valid(inputStr: str) -> bool:
    if not len(inputStr) > 31:
        for el in inputStr:
            if el not in alphabet_list:
                print(f'InputError: {el} is not a letter')
                break
        else:
            return True
    else:
        print('InputError: The input string is not a word')
    return False


if __name__ == '__main__':
    print("1. Levenshtein \n2. Soundex \n3. Spell correction")
    inputType = input("Type 1, 2 or 3: ").strip()

    if inputType == '1':
        firstString = input('First string: ')
        secondString = input('Second string: ')
        distance = distance(firstString, secondString)
        print(f'Levenshtein distance for "{firstString}" and "{secondString}" is {distance}')
    elif inputType == '2':
        inputString = input('Input string: ').strip()
        if is_valid(inputString):
            soundexCode = soundex(inputString)
            print(f'Soundex code for "{inputString}" is {soundexCode[0]}')
    elif inputType == '3':
        word = input('Write misspelled word:')
        dictionary = json.load(open(os.path.normpath('soundexFile.text'), 'rb'))
        if is_valid(word):
            optionsList = []
            soundexCode, info = soundex(word)
            if info:
                options = []
                for ind in range(0, 7):
                    soundexCode = f'{soundexCode[:-1]}{ind}'
                    options_ = dictionary.get(soundexCode)
                    if options_:
                        options += options_
            else:
                options = dictionary.get(soundexCode)
            if options:
                for item in options:
                    distanceOptions = distance(word, item)
                    if distanceOptions < 3:
                        optionsList.append(item.strip('\r'))
                if optionsList:
                    print('Possible options: ', ', '.join(optionsList))
                else:
                    print('did not find possible options')
            else:
                print('did not find possible options')
    else:
        print(f'TypeError: Type 1, 2 or 3 not \'{inputType}\'')
