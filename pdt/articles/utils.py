import re

# text2int: converts number words to numbers
# http://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers-python

numwords = {}

units = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
    ]

tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

scales = ["hundred", "thousand", "million", "billion", "trillion"]

numwords["and"] = (1, 0)
for idx, word in enumerate(units):    numwords[word] = (1, idx)
for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

def text2int(textnum, numwords=numwords):
    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

def words2ints(s):
    words = re.findall(r'[a-zA-Z]+', s)
    seps = re.findall(r'[^a-zA-Z]+', s)
    out = []

    if seps and s.startswith(seps[0]):
        out.append(seps.pop(0))

    part, last_sep = [], ''
    while words:
        word = words.pop(0)
        # if word is 'and' but it's not between number-words, treat it normally
        if word in numwords and not (word == 'and' and not part):
            part.append(word)
            last_sep = seps.pop(0) if seps else ''
        elif part:
            part = text2int(' '.join(part))
            out.append(str(part))
            out.append(last_sep)
            part = []
            words.insert(0, word)
        else:
            out.append(word)
            if seps:
                out.append(seps.pop(0))

    # cleanup
    if part:
        part = text2int(' '.join(part))
        out.append(str(part))
        out.append(last_sep)
        words.insert(0, word)

    return ''.join(out)
