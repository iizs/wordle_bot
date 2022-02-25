
def match(word, mask_word, mask):
    for i in range(len(mask_word)):
        if mask[i] == '🟩':
            if mask_word[i] != word[i]:
                return False
            mask_word = mask_word[0:i] + ' ' + mask_word[i + 1:]
            word = word[0:i] + ' ' + word[i + 1:]
            mask = mask[0:i] + ' ' + mask[i + 1:]

    for i in range(len(mask_word)):
        if mask_word[i] == ' ':
            continue
        if mask[i] == '🟨':
            found = False
            for j in range(len(word)):
                if i == j:
                    # This should be '🟩' not '🟨'
                    continue
                if mask_word[i] == word[j]:
                    mask_word = mask_word[0:i] + ' ' + mask_word[i + 1:]
                    word = word[0:j] + ' ' + word[j + 1:]
                    mask = mask[0:i] + ' ' + mask[i + 1:]
                    found = True
                    break
            if not found:
                return False

    for i in range(len(mask_word)):
        if mask_word[i] == ' ':
            continue
        if mask[i] == '⬛':
            if word.__contains__(mask_word[i]):
                return False
    return True


def mark(answer, guess):
    m = '⬛⬛⬛⬛⬛'
    for i in range(len(answer)):
        if answer[i] == guess[i]:
            m = m[0:i] + '🟩' + m[i + 1:]
            answer = answer[0:i] + ' ' + answer[i + 1:]
            guess = guess[0:i] + ' ' + guess[i + 1:]
    for i in range(len(guess)):
        if guess[i] == ' ':
            continue
        for j in range(len(answer)):
            if answer[j] == guess[i]:
                m = m[0:i] + '🟨' + m[i + 1:]
                answer = answer[0:j] + ' ' + answer[j + 1:]
    return m
