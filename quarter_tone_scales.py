import math
import numpy as np
from scipy.io.wavfile import write

def triangle(t):
    if t < 0:
        return -triangle(-t)
    t = t % 1
    if t < 0.25:
        return t*4
    elif t < 0.75:
        return 2 - t*4
    else:
        return t*4 - 4

# Utility stuff
flatsharp = ['bb', 'db', 'b', 'd', '', 'ⱡ', '#', '#ⱡ', 'x']
halftones = {
    'Lydian': [4, 4, 4, 2, 4, 4, 2], 'Mixolydian': [4, 4, 2, 4, 4, 2, 4], 'Aeolian': [4, 2, 4, 4, 2, 4, 4], 'Locrian': [2, 4, 4, 2, 4, 4, 4], 'Ionian': [4, 4, 2, 4, 4, 4, 2], 'Dorian': [4, 2, 4, 4, 4, 2, 4], 'Phrygian': [2, 4, 4, 4, 2, 4, 4],
    'Ionadian': [2, 4, 2, 4, 4, 4, 4], 'Bocrian': [4, 2, 4, 4, 4, 4, 2], 'Mixolythian': [2, 4, 4, 4, 4, 2, 4], 'Larian': [4, 4, 4, 4, 2, 4, 2], 'Lythian': [4, 4, 4, 2, 4, 2, 4], 'Stydian': [4, 4, 2, 4, 2, 4, 4], 'Lorian': [4, 2, 4, 2, 4, 4, 4],
    'Aeroptian': [4, 4, 4, 4, 2, 2, 4], 'Phryrian': [4, 4, 4, 2, 2, 4, 4], 'Gothian': [4, 4, 2, 2, 4, 4, 4], 'Storian': [4, 2, 2, 4, 4, 4, 4], 'Pyptian': [2, 2, 4, 4, 4, 4, 4], 'Thydian': [2, 4, 4, 4, 4, 4, 2], 'Aeolynian': [4, 4, 4, 4, 4, 2, 2]
}
major = [0, 4, 8, 10, 14, 18, 22]

modeclasses = {710: 'Quintal', 722: 'Melodic', 726: 'Whole',
    692: 'Quintal 5th', 691: 'Quintal 2nd = Whole 5th = Q-M 1st', 637: 'Quintal 6th = Melodic 5th = M-W 1st',
    715: 'Melodic 2nd = Whole 6th = Q-W 1st', 695: 'Melodic 6th',
    723: 'Whole 2nd',
    716: 'Q-M 4th', 709: 'Q-M 5th', 689: 'Q-M 6th = Q-W 5th = M-W 3rd', 698: 'Q-M 7th', 671: 'Q-M 2nd', 697: 'Q-M 3rd = Q-W 4th = M-W 2nd',
    718: 'Q-W 7th', 707: 'Q-W 2nd', 700: 'Q-W 3rd', 699: 'Q-W 6th',
    724: 'M-W 4th', 721: 'M-W 5th', 713: 'M-W 6th', 717: 'M-W 7th'
    }
    
solfege = ['do', 're', 'mi', 'fa', 'so', 'la', 'ti']

alternate_names = {125: ['Major'], 80: ['Minor', 'Natural Minor'], 145: ['Acoustic', 'Overtone', 'Lydian Dominant'], 6: ['Altered'], 76: ['Half Diminished'], 157: ['Lydian Augmented'], 116: ['Major Locrian'], 85: ['Melodic Minor'], 20: ['Neapolitan Major'], 120: ['Aeolian Dominant', 'Melodic Major', 'Hindu'], 35: ['Bayati'], 124: ['Jiharkah'], 32: ['Husayni \'Ushyaran'], 98: ['Rast'], 36: ['"Rattlesnake"']}

# Enumerate all of them!
scales = []

for halfFlat1 in range(7):
    for halfFlat2 in range(halfFlat1, 7):
        for halfFlat3 in range(halfFlat2, 7):
            for halfFlat4 in range(halfFlat3, 7):
                if halfFlat1 == halfFlat3 or halfFlat2 == halfFlat4:
                    continue
                scale = [4, 4, 4, 4, 4, 4, 4]
                scale[halfFlat1] -= 1
                scale[halfFlat2] -= 1
                scale[halfFlat3] -= 1
                scale[halfFlat4] -= 1
                scales += [scale]
                
# Find averages of each pair
average_list = [[] for i in range(len(scales))]
scale_names = ['?' for i in range(len(scales))]

htkeys = list(halftones.keys())
for i in range(len(htkeys)-1, -1, -1):
    for j in range(i, -1, -1):
        ht1 = htkeys[i]
        ht2 = htkeys[j]
        s1 = halftones[ht1]
        s2 = halftones[ht2]
        s3 = [(s1[k] + s2[k]) // 2 for k in range(7)]
        if ht1 == ht2:
            scale_names[scales.index(s3)] = ht1
        else:
            scale_names[scales.index(s3)] = ht2 + '-' + ht1
        average_list[scales.index(s3)] = [ht2 + '-' + ht1] + average_list[scales.index(s3)]
        
# Find scale squares
squares = []
for i in range(len(scales)):
    if 3 in scales[i]:
        continue
    for j in range(i+1, len(scales)):
        if 3 in scales[j]:
            continue
        scale_notes1 = [sum(scales[i][:k]) for k in range(7)]
        scale_notes2 = [sum(scales[j][:k]) for k in range(7)]
        sameness = [(1 if scale_notes1[k] == scale_notes2[k] else 0) for k in range(7)]
        commonalities = sum(sameness)
        if commonalities == 5:
            if sameness[sameness.index(0)+1] == 0 or (sameness[0] == 0 and sameness[6] == 0):
                continue
            square = []
            for k in range(1, 7):
                if scale_notes1[k] == scale_notes2[k]:
                    square += [[k, scale_notes1[k] - major[k]]]
            if square not in squares:
                squares += [square]

def getScaleIndex(st):
    st = st.lower()
    ind = -1
    try:
        ind = int(st)
    except ValueError:
        # Try to find by name!
        for i in range(len(scales)):
            if scale_names[i].lower() == st or st in [s.lower() for s in average_list[i]] or (i in alternate_names and st in [s.lower() for s in alternate_names[i]]):
                ind = i
                break
        if ind == -1:
            print('Unknown scale name')
            return -1
    if ind < 0 or ind >= len(scales):
        print('Index out of range')
        return -1
    return ind

while True:
    cmd = input('> ')
    cmd = cmd.strip().split(' ')
    
    if cmd[0] == 'quit':
        break
    elif cmd[0] == 'scale':
        ind = getScaleIndex(' '.join(cmd[1:]))
        if ind < 0:
            continue
        scale = scales[ind]
        scale_notes = [sum(scale[:i]) for i in range(7)]
        if ind in alternate_names:
            print('SCALE', ind, '-', scale_names[ind], '(' + ' / '.join(alternate_names[ind]) + ')')
        else:
            print('SCALE', ind, '-', scale_names[ind])
        print('Scale:', scale)
        print('On C:', 'C' + flatsharp[scale_notes[0]+4], 'D' + flatsharp[scale_notes[1]], 'E' + flatsharp[scale_notes[2]-4], 'F' + flatsharp[scale_notes[3]-6], 'G' + flatsharp[scale_notes[4]-10], 'A' + flatsharp[scale_notes[5]-14], 'B' + flatsharp[scale_notes[6]-18])
        print('Average of:', average_list[ind])
        print('Brightness:', sum([scale_notes[i] - major[i] for i in range(7)]))
    elif cmd[0] == 'modes':
        ind = getScaleIndex(' '.join(cmd[1:]))
        if ind < 0:
            continue
        scale = scales[ind]
        
        maxsum = 0
        for i in range(7):
            thissum = 243*(scale[0]-2) + 81*(scale[1]-2) + 27*(scale[2]-2) + 9*(scale[3]-2) + 3*(scale[4]-2) + (scale[5]-2)
            if thissum > maxsum:
                maxsum = thissum
            scale = scale[1:] + scale[:1]
        print('MODE CLASS', maxsum, '-', modeclasses[maxsum])
        
        for i in range(7):
            scale_notes = [sum(scale[:i]) for i in range(7)]
            print('Mode', str(i+1) + ':', scale, '-', str(scales.index(scale)) + ',', scale_names[scales.index(scale)], '(brightness', str(sum([scale_notes[i] - major[i] for i in range(7)])) + ')')
            scale = scale[1:] + scale[:1]
    elif cmd[0] == 'search':
        toFind = []
        for word in cmd[1:]:
            sf = word[:2]
            if sf not in solfege:
                continue
            degree = solfege.index(sf)
            acc = word[2:]
            if acc == '':
                acc = 0
            try:
                acc = int(acc)
            except ValueError:
                continue
            toFind += [[degree, acc]]
        for scale in scales:
            scale_notes = [sum(scale[:i]) for i in range(7)]
            diffs = [scale_notes[i] - major[i] for i in range(7)]
            works = True
            for t in toFind:
                if diffs[t[0]] != t[1]:
                    works = False
                    break
            if not works:
                continue
            
            print(scale, '-', str(scales.index(scale)) + ',', scale_names[scales.index(scale)], '(brightness', str(sum([scale_notes[i] - major[i] for i in range(7)])) + ')')
    elif cmd[0] == 'squares':
        ind = getScaleIndex(' '.join(cmd[1:]))
        if ind < 0:
            continue
        scale = scales[ind]
        scale_notes = [sum(scale[:i]) for i in range(7)]
        diffs = [scale_notes[i] - major[i] for i in range(7)]

        for square in squares:
            works = True
            for t in square:
                if diffs[t[0]] != t[1]:
                    works = False
                    break
            if not works:
                continue
                
            squarestr = ''
            for i in range(len(square)):
                if i > 0:
                    squarestr += ' '
                squarestr += solfege[square[i][0]]
                squarestr += str(square[i][1])
            print(squarestr)
    elif cmd[0] == 'allsquares':
        for square in squares:
            squarestr = ''
            for i in range(len(square)):
                if i > 0:
                    squarestr += ' '
                squarestr += solfege[square[i][0]]
                squarestr += str(square[i][1])
            print(squarestr)
    elif cmd[0] == 'alterations':
        ind = getScaleIndex(' '.join(cmd[1:]))
        if ind < 0:
            continue
        scale = scales[ind]
        scale_notes = [sum(scale[:i]) for i in range(7)]
        for alt in range(-2, 3):
            if alt == 0:
                continue
            for degree in range(7):
                sn2 = scale_notes.copy()
                sn2[degree] += alt
                if degree == 0:
                    for i in range(1, 7):
                        sn2[i] -= sn2[0]
                    sn2[0] = 0
                for io in range(len(scales)):
                    s_other = scales[io]
                    sn_other = [sum(s_other[:i]) for i in range(7)]
                    if sn_other == sn2:
                        print(['Lower', 'Half-lower', '', 'Half-raise', 'Raise'][alt+2], 'degree', (degree+1), 'to get', scale_names[io])
    elif cmd[0] == 'wavfile':
        ind = getScaleIndex(' '.join(cmd[1:]))
        if ind < 0:
            continue
        scale = scales[ind]
        scale_notes = [sum(scale[:i]) for i in range(7)]
        scale_notes += [24]
        updown = [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0]
        
        samples = []
        for i in range(len(updown)):
            this_note = scale_notes[updown[i]]
            this_freq = (440 * math.pow(2, -3/4)) * math.pow(2, this_note/24)
            for sampind in range(22050): # 1/2 second
                sample = triangle(sampind / 44100 * this_freq)
                sample *= math.pow(2, -sampind / 20000)
                if sampind > 21609: # 1/100 second from the end
                    sample *= 1 - (sampind - 21609) / 441
                samples += [sample]
        
        scaled = np.int16(np.array(samples) * 32767)
        write(str(ind) + ' - ' + scale_names[ind] + '.wav', 44100, scaled)
    elif cmd[0] == 'help':
        print('List of available commands:')
        print('quit: Quit')
        print('scale [scale]: Look up a scale')
        print('modes [scale]: List the modes of a scale')
        print('search [notes]: Search for scales with certain scale degrees altered certain ways, e.g. "search mi-1" finds scales where mi is lowered one quarter tone')
        print('squares [scale]: List scale squares containing a scale')
        print('allsquares: List all of the scale squares recognized by the database')
        print('alterations [scale]: List new scales made from a scale by altering one of the pitches')
        print('wavfile [scale]: Create a WAV file of a scale')
        print('help: Display this help text')
    else:
        print('Unknown command')