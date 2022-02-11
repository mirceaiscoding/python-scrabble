replace_symbols = {
    'ă': 'a',
    'â': 'a',
    'î': 'i',
    'ș': 's',
    'ț': 't'
}

with open("resources/dictionary/loc-flexiuni-6.0.txt", 'r', encoding="utf-8") as word_base_file:
    word_base = word_base_file.read().lower()
    for k in replace_symbols.keys():
        v = replace_symbols[k]
        print (f'Replace {k} with {v}')
        word_base = word_base.replace(k, v)
    words = word_base.split("\n")
    print (f'Dictionary has {len(word_base)} words')
    words.sort()

with open("resources/dictionary/loc-flexiuni-6.0.txt", 'w', encoding="utf-8") as word_base_file:
    word_base_file.write("\n".join(words))
