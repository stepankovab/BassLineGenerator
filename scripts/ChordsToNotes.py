import random

#changes note letter to a number
rootNotes = {"C":8,"D":10,"E":0,"F":1,"G":3,"A":5,"B":7}

#intervals between notes (scale patterns) when using major or minor scale
minor = [0,2,3,5,7,8,10]
major = [0,2,4,5,7,9,11]

#what to press on the bass neck
whatToWrite = [["-","-","-","0"],
["-","-","-","1"],["-","-","-","2"],["-","-","-","3"],
["-","-","-","4"],["-","-","0","-"],["-","-","1","-"],
["-","-","2","-"],["-","-","3","-"],["-","-","4","-"],
["-","0","-","-"],["-","1","-","-"],["-","2","-","-"],
["-","3","-","-"],["-","4","-","-"],["-","5","-","-"],
["1","-","-","-"],["2","-","-","-"],["3","-","-","-"],
["4","-","-","-"],["5","-","-","-"],["6","-","-","-"],
["7","-","-","-"],["8","-","-","-"]]

def WriteTabs(notesToPrint : list, chordsAbove : str, f):
    '''
    This function prints the final result both on the stdout and in a file

    input:
    list of lists in which are saved the tabs
    string in which are saved the song chords with correct spaces
    empty file with an assign name

    output:
    prints chords and tabs in correct formating
    '''

    # Cycles so it will be in lines, 80 character each
    cycles = (len(notesToPrint)//80) +1
    x = 0
    y = min(80,len(notesToPrint))

    # Makes five lines
    for cycle in range(cycles):
        lines = [chordsAbove[x:y], "", "", "", ""]
        for note in notesToPrint[x:y]:
            for i in range(4):
                lines[i+1] += note[i]

        # Adds the lines
        for i in range(5):
            print(lines[i])
            f.write(lines[i] + "\n")  

        print("")  
        f.write("\n")   

        # Makes new interval, from which I take chords and tabs
        x += 80
        y = min((y+80), len(notesToPrint))

    

def FindRootNotes(songChords : list):
    '''
    This function:
    sorts out anything that isn't recognised as a chord
    assigns a correct number to a chord, depending on the root note of the chord

    input:
    song chords from the internet

    output:
    songChords - all the correct chords for the song
    roots - corresponding root numbers with the same indexing as in songChords
    '''
    # Holds rootnotes as a number
    roots = []

    # Holds index numbers of things that shouldn't be in songChords
    chordsToRemove = []

    for i in range(len(songChords)):
        chord = songChords[i]

        # Checks if the chord consists of two chords (root is always from the second one)
        try:
            chordStart = chord.index("/") +1
            chord = chord[chordStart:]
        except:
            pass

        # Gets the assigned number of a first letter of the chord
        root = rootNotes.get(chord[0].upper())

        # If the letter/character can't be converted to a number, remove 
        if root == None:
            chordsToRemove.append(i)
            continue

        # finds if the root is actually a half note up or down or not
        try:
            halfTone = chord[1]
            if halfTone == "#":
                root = (root + 1) % 12
            if halfTone == "b":
                root = (root - 1) % 12
        except:
            pass

        roots.append(root)

    # Removes 'not chords' from the list of chords
    for i in chordsToRemove[::-1]:
        songChords.pop(i)

    return roots, songChords


def IsMajorOrMinor(chord : str):
    '''
    finds out if the chord is major or minor

    input: a chord that im currently working on
    
    output: returns the correct scale pattern
    '''

    # Checks if the chord consists of two chords
    try:
        chordStart = chord.index("/") +1
        chord = chord[chordStart:]
    except:
        pass

    chordLen = len(chord)

    # Checks for half tones and sets n (on which position to look for major/minor notation)
    n = 1
    if chordLen > 1:
        if (chord[1] == "#" or chord[1] == "b") and chordLen > 2:
            n = 2
        else:
            n = 1

    if chordLen >= 4:
        if chord[n] == "m" and chord[n+1] != "a": # Is not xxMaj as in major
            return minor
    elif 2 <= chordLen <= 3:
        if chord[n] == "m":
            return minor
    return major


def BasicBass(songChords : list, f):
    '''
    This function generates tabs for the most common bassline that can be found in music.
    It composes of roots and their fifths. 

    input: list of chords from the internet, file to which I will write tabs

    output: returns the original chords with correct spaces and bassline written in tabs.
    With these parameters, the function calls another function to print these in a correct formating.
    '''
    roots, songChords = FindRootNotes(songChords)
    notesToPrint = []
    chordsAbove = ""

    for i in range(len(roots)):
        # Adds chords and spaces
        chordsAbove += songChords[i] + (10 - len(songChords[i])) * " "
        for j in (0,7,0,7): #Intervals
            notesToPrint.append(whatToWrite[(roots[i] + j) % 24])
            notesToPrint.append(["-","-","-","-"])
        for i in range(2):
            notesToPrint.append(["-","-","-","-"])

    WriteTabs(notesToPrint, chordsAbove, f)




def GenerateWalkBass(chordMood, nextRoot, upDownNow):
    '''
    This function generates intervals between notes for walking bassline, a bassline that 
    can be typically found in jazz.

    Depending on if the bassline is going up or down, it randomly chooses the next possible note, and if the next sequence is
    going to be ascending or descending, while checking the tone distance between the first note of the next chord root.

    If the distance is short enough, the function will generate chromatic passing notes and transition into the next root.

    There is a 20% chance that there will be one extra note for flavour.

    input: A scale that fits to this chord, root note of the next chord, if the bassline is ascending or descending

    output: returns a walking bassline for one chord written in intervals counting from the root note, the number of generated
    notes, and if the next chord will have ascending or descending bassline
    '''
    numberOfNotes = 4

    # Depending on the distance of the roots, chooses if the next sequence will be ascending or descending
    if upDownNow == 0:
        secondInterval = random.choice([1,1,1,2,2,2,3,3])
        third = chordMood[random.randint(secondInterval + 1, 6)]
        if nextRoot > 8:
            upDownNext = 0
        else:
            upDownNext = 12
    else:
        secondInterval = random.choice([4,4,4,5,6])
        third = chordMood[random.randint(1, secondInterval - 1)]
        if nextRoot < 4:
            upDownNext = 12
        else:
            upDownNext = 0
    
    nextRoot += upDownNext
    second = chordMood[secondInterval]

    # Makes chromatic notes if possible
    if abs(second - nextRoot) == 3:
        third = second + ((nextRoot - second) // 3)

    if abs(third - nextRoot) == 2:
        fourth = (third + nextRoot) // 2

    # If chromatic notes are not possible
    else:
        if third == nextRoot:
            fourth = (third - 1) % 24

        else:
            if (((third + nextRoot) // 2) % 12) in chordMood:
                fourth = (third + nextRoot) // 2
            else:
                fourth = ((third + nextRoot) // 2) + random.choice([-1,1])

        # Fifth for flavour and randomness
        if random.randint(0,100) < 10:
            numberOfNotes = 5

    walkBass = [upDownNow, second, third, fourth]

    if numberOfNotes == 5:
        walkBass.append(random.choice([fourth -1, third, second, upDownNow]))

    
    return walkBass, numberOfNotes, upDownNext



def WalkingBass(songChords : list, f):
    '''
    This function manages everything related to generating a walking bassline except
    generating the actuall intervals, that can be converted into notes and tabs.
    For the generating it calls function GenerateWalkBass()

    input: list of chords from the internet, file to which I will write tabs

    output: returns the original chords with correct spaces and bassline written in tabs.
    With these parameters, the function calls another function to print these in a correct formating.
    '''
    notesToPrint = []
    roots, songChords = FindRootNotes(songChords)
    chordsAbove = ""

    upDownNext = 0

    for i in range(len(roots)):

        chordsAbove += songChords[i] + (8 - len(songChords[i])) * " "
        chordMood = IsMajorOrMinor(songChords[i])

        # Finds next root note in context of the current chord, if it doesn't exist, sets current as next
        try:
            nextRoot = roots[i + 1] - roots[i]
        except:
            nextRoot = 0

        # generates intervals
        walkBass, numberOfNotes, upDownNext = GenerateWalkBass(chordMood, nextRoot, upDownNext)

        # changes intervals to tabs
        for j in range(4):
            notesToPrint.append(whatToWrite[roots[i] + walkBass[j]])

            if numberOfNotes == 5 and j == 2:
                notesToPrint.append(whatToWrite[roots[i] + walkBass[4]])
            else:
                notesToPrint.append(["-","-","-","-"])

    WriteTabs(notesToPrint, chordsAbove, f)


    
def GenerateRollBass(chordMood):
    '''
    This function generates intervals between notes for rock and roll bassline.

    The third note is always fixed on the third of the corresponding scale. Some other notes are randomly chosen
    from a list of possible notes that fit into the bassline and depending on this choice, one of three scenarios
    is followed for the fifth, sixth and seventh note.

    This function only generates the intervals between notes and doesn't know which chord it is currently working on.

    input: A scale of a current chord

    output: returns a rock and roll bassline for one chord written in intervals counting from the root note
    '''
    third = chordMood[2]

    second = random.choice([0,0,12])
    fourth = random.choice([third,third,5,7])
    if fourth == third:
        fifth = 7
        sixth = 7
        seventh = third
    elif fourth == 7:
        fifth = 10
        sixth = 10
        seventh = 9     
    else:
        fifth = 6
        sixth = 7
        seventh = 10

    eighth = random.choice([0,7,12,12,12])

    rollBass = [0,second,third,fourth,fifth,sixth,seventh,eighth]

    return rollBass

def RockAndRollBass(songChords : list, f):
    '''
    This function manages everything related to generating a rock and roll bassline except
    generating the actuall intervals, that can be converted into notes and tabs.

    For the generating it calls function GenerateRollBass() and uses these intervals combined with
    the root note of a current chord to get the final notes.

    input: list of chords from the internet, file to which I will write tabs

    output: returns the original chords with correct spaces and bassline written in tabs.
    With these parameters, the function calls another function to print these in a correct formating.
    '''
    notesToPrint = []
    roots, songChords = FindRootNotes(songChords)
    chordsAbove = ""


    for i in range(len(roots)):

        chordsAbove += songChords[i] + (16 - len(songChords[i])) * " "
        chordMood = IsMajorOrMinor(songChords[i])
        # generates intervals
        rollBass = GenerateRollBass(chordMood)

        for j in range(8):
            # changes intervals to tabs
            notesToPrint.append(whatToWrite[roots[i] + rollBass[j]])
            notesToPrint.append(["-","-","-","-"])


    WriteTabs(notesToPrint, chordsAbove, f)

def DustPart1(notesToPrint : list, whatToWrite : list, roots : list, i : int):
    '''
    First part of the 'Another One Bites The Dust' cycle
    '''
    notesToPrint.append(whatToWrite[(roots[i] + 5) % 24])
    notesToPrint.append(whatToWrite[(roots[i] + 3) % 24])
    for k in range(3):
        notesToPrint.append(whatToWrite[roots[i]])
        for l in range(3):
            notesToPrint.append(["-","-","-","-"])
    for m in range(2):
        notesToPrint.append(["-","-","-","-"])

def DustPart2(notesToPrint : list, whatToWrite : list, roots : list, i : int):
    '''
    Second part of the 'Another One Bites The Dust' cycle
    '''
    for j in (-1,-1,0,0,-1,0,-1,3,-1,0,5,-1,-1,-1,-1,-1,):
        if j == -1:
            notesToPrint.append(["-","-","-","-"])
        else:
            notesToPrint.append(whatToWrite[(roots[i] + j) % 24])

def BitesTheDustBass(songChords : list, f):
    '''
    This function is more of a fun interesting idea, then an actual bassline generator.
    It writes tabs for a bassline from a song 'Another One Bites The Dust' by Queen, but fitting 
    to chords of any other song.

    Depending on how quickly are the chords in the song switching, one cycle lasts over either one or
    two chords.

    input: list of chords from the internet, file to which I will write tabs

    output: returns the original chords with correct spaces and bassline written in tabs.
    With these parameters, the function calls another function to print these in a correct formating.
    '''
    roots, songChords = FindRootNotes(songChords)
    notesToPrint = []
    chordsAbove = ""

    quickSwith = input("----------\nAre the chords in the song switching quickly? [y]/n ").lower()
    print()

    # one cycle for chord
    if quickSwith == "y":
        for i in range(len(roots)):
            chordsAbove += songChords[i] + (16 - len(songChords[i])) * " "
            if i % 2 == 0:
                DustPart1(notesToPrint, whatToWrite, roots, i)
            else:
                DustPart2(notesToPrint, whatToWrite, roots, i)
    # two cycles for chord
    else:
        for i in range(len(roots)):
            chordsAbove += songChords[i] + (32 - len(songChords[i])) * " "
            DustPart1(notesToPrint, whatToWrite, roots, i)
            DustPart2(notesToPrint, whatToWrite, roots, i)

    WriteTabs(notesToPrint, chordsAbove, f)


def BillieJean(songChords : list, f):
    '''
    This function is also more of a fun bonus function. It writes tabs for the iconic 'Billie Jean'
    bassline, over chords of any song.

    input: list of chords from the internet, file to which I will write tabs

    output: returns the original chords with correct spaces and bassline written in tabs.
    With these parameters, the function calls another function to print these in a correct formating.
    '''
    roots, songChords = FindRootNotes(songChords)
    notesToPrint = []
    chordsAbove = ""

    for i in range(len(roots)):
        chordsAbove += songChords[i] + (16 - len(songChords[i])) * " "

        # if the deepest note isn't playable on the bass, shift the whole thing up
        shifting = 0
        if roots[i] < 5:
            shifting = 12

        for j in (2,-3,0,2,0,-3,-5,-3):
                notesToPrint.append(whatToWrite[(roots[i] + j + shifting) % 24])
                notesToPrint.append(["-","-","-","-"])
        
    WriteTabs(notesToPrint, chordsAbove, f)
