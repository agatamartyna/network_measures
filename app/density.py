from app.segmentise import segmentise


quadruples = {
    '\u0254\u0303w\u0303': 'OPEN_MID_ROUND_NAS_DYPH',
    '\u025B\u0303w\u0303': 'MID_OPEN_FRONT_NAS_DYPH'
}
doubles = {
    'ts': 'VS_ALV_AFF',
    't\u0255': 'VS_PAL_AFF',
    't\u0282': 'VS_POSTALV_AFF',
    'd\u0291': 'VD_PAL_AFF',
    'dz': 'VD_ALV_AFF',
    'd\u0290': 'VD_POSTALV_AFF'
}


def neighbourhood_density(word, words):
    word_items = segmentise(word)
    n = []
    for l in words:
        # this line selects item of desirable length
        if len(l[0]) - 1 <= len(word_items) <= len(l[0]) + 1:
            # for length-peers
            if len(l[0]) == len(word_items):
                segment_count = 0
                for i in range(len(l[0])):
                    if (
                            l[0][i] == word_items[i] or
                            l[0][i] == word_items[i] + 'ʲ' or
                            l[0][i] + 'ʲ' == word_items[i]
                    ):
                        pass
                    else:
                        segment_count += 1
                if segment_count == 1:
                    n.append(''.join(l[1]))
                elif l[0] == word_items and l[1] != word:
                    n.append(''.join(l[1]))
            elif len(l[0]) == len(word_items) - 1:
                flag = 0
                for i in range(len(word_items)):
                    wordie = word_items[:i] + word_items[i+1:]
                    if ''.join(l[0]) in ''.join(wordie):
                        flag = 1
                if flag == 1:
                    n.append(''.join(l[1]))

            elif len(l[0]) == len(word_items) + 1:
                flag = 0
                for i in range(len(l[0])):
                    wordie = l[0][:i] + l[0][i + 1:]
                    if ''.join(wordie) == ''.join(word_items):
                        flag = 1
                if flag == 1:
                    n.append(''.join(l[1]))

    return n
