import requests

class SearchForChords:
    def FindChords(url):
        '''
        This function is making a HTTP request to an URL pieced together from the information given by the user.
        The request is made by the Python Requests library's function GET. Because of the .text, the request
        returns the content of the response in unicode and saves it to a variable webText.

        Then the function separates the chords from the html document, now saved in webText, and appends them to
        a list of chords.

        inputs: url address

        outputs: list of chords
        '''
        webText = requests.get(url).text

        chords = []

        chordLenght = 2
        
        # Goes through the webText and retrieves anything that is written in superscript...
        while 0 < chordLenght < 15:       
            x = webText.find("<sup>")
            webText = webText[x+5:]
            chordLenght = webText.find("</sup>")
            chords.append(webText[:chordLenght])

        chords.pop()
        return chords

    def EnterChords():
        # This function allows the user to manually enter chords.
        print("----------\nWrite a chord, press enter, repeat.\nTo remove a chord, write: 'remove'\nTo end, write: 'end'")
        userInp = "X"
        chords = []

        while userInp != "end":
            userInp = input()
            if userInp == "remove":
                if chords != []:
                    chords.pop()
            else:
                chords.append(userInp)
            
        chords.pop()
        return (chords)

    def GetChords(song_input : str):
        '''
        This function calls a function that sends HTTP requests, if none of the requests have positive response,
        returns empty list of chords.
        '''
        song_list = song_input.split()

        song = ""
        for word in song_list:
            song = song + word + "-"

        song = song[:-1]
        
        url = "https://www.chords-and-tabs.net/song/name/" + song

        chords = SearchForChords.FindChords(url)
        if chords == []:
            print("Song not found, searching for another version...")

        for i in range(1,25):
            if chords != []:
                break
            chords = SearchForChords.FindChords(url + "-" + str(i))

        return chords, song
