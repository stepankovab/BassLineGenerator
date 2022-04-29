from scripts/UrlToChords import SearchForChords
from scripts/ChordsToNotes import BasicBass, WalkingBass, RockAndRollBass, BitesTheDustBass, BillieJean

def CreateAFile(nameTogether, style):
    f = open("{}-{}.txt".format(nameTogether, style), "w+")
    return f

def SameSongGoAgain(f):
    input("-----------\npress enter to continue...\n")
    if input("-----------\nDo you want to generate a different bassline for this song? [y]/n ").lower() == "y":
        print()
        f.close()
        return "0"
    else:
        return "1"

print("----------\nHave you ever wanted to be able to hear your favourite pop/rock song with a funky jazzy bassline?")
cont = input("[y]/n ").lower()
if cont == "y":

    while cont == "y":
        print("----------\nGreat! First, I would like to know something about the song...")
        songChords = []

        while songChords == []:
            song = input("Artist: ").lower() + " " + input("Song name: ").lower()
            songChords, nameTogether = SearchForChords.GetChords(song)
            if songChords == []:
                manuallyOrNot = input("----------\nSong not found. Do you want to:\n [1] write chords manually?\
                    \n [2] correct the spelling or pick a different song\n(if you don't choose, i will choose for you)\n 1/[2] ").lower()
                if manuallyOrNot == "1":
                    songChords = SearchForChords.EnterChords()

        chooseStyle = None
        print("----------\nOk, and now the important part.")

        while chooseStyle not in ["1", "2", "3", "4","5"]:
            chooseStyle = input("What kind of bassline do you think would fit this song the best?\
                \n [1] the boring fifths and fourths\
                \n [2] the well-known jazzy walking bassline\
                \n [3] the funky rock and roll bassline\
                \n [4] Billie Jean\
                \n [5] tu. tu. tu. tudu tu taa du tu. Tadu *repeat*\
                \nChoose a number: ")
            print()
            if chooseStyle == "1":
                f = CreateAFile(nameTogether, "basic")
                BasicBass(songChords,f)
                chooseStyle = SameSongGoAgain(f)
            elif chooseStyle == "2":
                f = CreateAFile(nameTogether, "walking")
                WalkingBass(songChords,f)
                chooseStyle = SameSongGoAgain(f)
            elif chooseStyle == "3":
                f = CreateAFile(nameTogether, "rock-and-roll")
                RockAndRollBass(songChords,f)
                chooseStyle = SameSongGoAgain(f)
            elif chooseStyle == "4":
                f = CreateAFile(nameTogether, "billie-jean")
                BillieJean(songChords,f)
                chooseStyle = SameSongGoAgain(f)
            elif chooseStyle == "5":
                f = CreateAFile(nameTogether, "bites-the-dust")
                BitesTheDustBass(songChords,f)
                chooseStyle = SameSongGoAgain(f)
            else:
                print("----------\nThat isn't a valid choice of bassline, please type a number from 1 to 4 and hit enter.")
        
        f.close()
        cont = input("-----------\nDo you want to try it again with a different song? [y]/n ")
        
    print("-----------\nThank you for using my program!")
        
else:
    print("I'm sorry to hear that, but it's actually your loss :).")

