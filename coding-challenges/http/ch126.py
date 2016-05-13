import ringzer

# get SCOWL from <http://wordlist.aspell.net>
# /xxx/scowl/mk-list english 80 > english.dat
WORDMAP, WORDSET = {}, set()
for line in file('../../scowl/english.dat'):
    word = line.strip()
    WORDMAP[''.join(sorted(word))] = word
    WORDSET.add(word)

def chall_func(words_str):
    result = []
    for word in words_str.split(','):
        if word in WORDSET:
            result.append(word)
        else:
            idx = ''.join(sorted(word))
            if idx in WORDMAP:
                result.append(WORDMAP[idx])
    return ','.join(result)

ringzer.Challenge(126, chall_func, chall_repeat = 10)
