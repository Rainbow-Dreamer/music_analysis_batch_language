key_header = 'key: '


def grammar_translate(current):
    global key_header
    result = ''
    interval = 1
    comments = ''
    show_bar = 'T'
    bar_line_character = '|'
    arrow_character = '→ '
    show_chord_analysis = 'T'
    if current[:2] == 'k.':
        current_key = current[2:]
        result += f'{key_header}{current_key}'
        return result
    elif current[:2] == 'k!':
        new_key_header = current[2:]
        if new_key_header:
            key_header = new_key_header
        return
    parts = current.split('$')
    length = len(parts)
    if length == 1:
        bar_chords = parts[0]
        chord_degrees = '.'
    elif length == 2:
        bar_chords, chord_degrees = parts
    elif length > 2:
        bar_chords, chord_degrees = parts[:2]
        other_parts = parts[2:]
        for each in other_parts:
            flag = each[:2]
            content = each[2:]
            if flag == 'i=':
                try:
                    interval = int(content)
                except:
                    pass
            elif flag == 'c=':
                comments = content
            elif flag == 'b=':
                show_bar = content
            elif flag == 's=':
                if content.split():
                    bar_line_character = content
            elif flag == 'a=':
                if content:
                    arrow_character = content
            elif each[:3] == 'ca=':
                show_chord_analysis = each[3:]
    else:
        return
    bar_chords_split = bar_chords.split(';')
    if show_bar == 'T':
        bar_num = bar_chords_split[0]
        current_chords = bar_chords_split[1:]
        result += f'{bar_num}\n'
    else:
        current_chords = bar_chords_split
    current_play = False
    current_play_num = 0
    for i in range(len(current_chords)):
        each = current_chords[i]
        if each:
            if each[0] == '!':
                current_play = True
                current_play_num = i
                current_chords[i] = each[1:]
    if chord_degrees in ['.', '~', '']:
        show_chord_analysis = 'F'
    chord_degrees = chord_degrees.split(';')

    current_bar_chords = []
    current_bar_chords_degree = []
    degree_inds = []
    chord_inds = []
    current_chord_num = len(current_chords)
    chord_degrees_num = len(chord_degrees)
    for k in range(current_chord_num):
        chord_name = current_chords[k]
        if current_play and k == current_play_num:
            chord_name = arrow_character + chord_name
        result += f'{chord_name}{" "*interval}{bar_line_character}{" "*interval}'
    if current_chord_num == 0:
        return
    bar_line_character_len = len(bar_line_character)
    recent_line = result[result.rfind('\n') + 1:]
    result = result[:(-2 * interval - bar_line_character_len)]
    if show_chord_analysis == 'T':
        result += '\n'
        for current_ind in range(chord_degrees_num):
            chord_degree = chord_degrees[current_ind]
            if current_ind == 0:
                inds = 0
                if current_play and current_play_num == 0:
                    inds += len(arrow_character)
                result += ' ' * inds + chord_degree
                chord_inds = [
                    j + interval + bar_line_character_len
                    for j in range(len(recent_line))
                    if recent_line[j:j + bar_line_character_len] ==
                    bar_line_character
                ]
                if current_play and current_play_num != 0:
                    chord_inds[current_play_num - 1] += 2
            else:
                inds = chord_inds[current_ind - 1]
                last_degree = chord_degrees[current_ind - 1]
                last_degree_len = len(last_degree)
                last_chord = current_chords[current_ind - 1]
                result += ' ' * (inds - degree_inds[-1] -
                                 last_degree_len) + chord_degree
            degree_inds.append(inds)
    if comments:
        comments = comments.replace('\\n', '\n')
        result += f'\n{comments}'
    return result


def whole_translate(text, interval=2):
    results = [grammar_translate(i) if i else '' for i in text.split('\n')]
    results = [i for i in results if i is not None]
    return '\n'.join(results)
