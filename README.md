# Bass Line Generator

Final semestral project of first semester of uni

## Introduction

The topic of my semester project is a bassline generator. The final program is getting the chords from the internet, using the method get() from the Requests library or allowing the user to enter chords manually. The output is the bassline written in tabs on the standard output and in a file that has the name of the song and the type of the bassline in it’s name.

## Project

The whole project consists of three files. One takes care of the interaction with the
user (main.py), second one takes care of getting the chords (UrlToChords.py), and the last
one generates the bassline and writes it in a file (ChordsToNotes.py).

The first file isn’t really that interesting, it gets input from the user and based on the input, it
continues to call other functions, while informing the user about what is happening.

The second file has one interesting line of code, and otherwise is also pretty boring. The line
is : webText = requests.get(url).text.

I am communicating with a server via REST API. I’m using one of the most common HTTP
methods that is commonly used with the REST ruleset - a GET method. With it I’m creating a
HTTP request. This get() method comes from a Python Requests library. Because of the
.text, the result of this line is the content of the response in unicode.

The rest of this function pulls out the chords from the response, which is just an ordinary
while loop.

The third file handles the actual generating of basslines. It consists of many functions, a few
of them take care of basic things that aren’t specific for any bassline, like finding root notes,
deciding whether a chord is major or minor or writing the notes into actual tabs.

Other functions always relate to one bassline type. When a bassline is quite complex, there
are two functions. One for managing the chords and adding the right things to right lists and
keeping everything in check, and one for generating intervals between individual notes of the
line relative to a root note, not depending on a chord the line relates to.

**Everything about these individual functions in more detail can be found in the comments in
ChordsToNotes.py.**
