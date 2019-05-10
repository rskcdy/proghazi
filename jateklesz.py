from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import random
import os

clear = lambda: os.system('cls') # so I can clear the screen

wordsList = [] # osszes szo a fajlbol beolvasva
wordLengthList = [] # lehetseges szohosszok
hangman = [] # a megjelenitett akasztott emberek koronkent
hangmanHeigth = 23 # egy akasztottember merete

def addLength(length):                                  # elkesziti a wordlegthlistet
    global wordLengthList
    if length not in wordLengthList:
         wordLengthList.append(length)                  # ha egy adott szohossz meg nem leteik, hozzaadja a listahoz

with open('magyar_latin2.txt') as openfileobject:       # beolvassa a szotarat, elkesziti a wordlistet es abbol a wordlengtlistet
    for line in openfileobject:
        word = line.replace('\n', '')                   # sortorest torlom
        wordsList.append(word)                          # hozzaadom a szot a wordlisthez
        addLength(len(word))                            # meghivom az addLength fuggvenyt az adott szo hosszara

clear()

questions = [                                           # ez a szar csinal ilyen valasztos gecit (github copypaste)
    {
        'type': 'list',
        'name': 'level',
        'message': 'Milyen szinten szeretnél játszani?',
        'choices': ['Normál', 'Gonosz', 'Megoldhatatlan'],
        'filter': lambda val: val.lower()
    }
]

answers = prompt(questions)
difficulty = answers.get('level')                       # ezt valasztotta a juzer

hangmanPath = "hangman.txt"
if difficulty == "gonosz":
    hangmanPath = "hangmanGonosz.txt"                   # ez a sima gonoszhoz tartozo hangman fajl. A megoldhatatlan a normalhoz tartozoval jatszik, igy kevesebbet hibazhat a juzer
with open(hangmanPath) as openfileobject:               # elkesziti a hangmant
    hangmanElem = ''                                    # ideiglenes tarolo egy darab hangman allapotnak
    count = 0
    for line in openfileobject:                         # vegignezi a hangman.txt-t soronkent
        if count < hangmanHeigth:                       # ha meg nem erte el az egy allapot meretet, hozzaadja a hangmanElemhez az aktualis sort
            hangmanElem += line
            count +=1
        else:                                           # ha elerte a magassagot, a hangmanElemet a hangman elemeve teszi, ujrainditja a kovi sorral, a szamlalot visszaallitja
            hangman.append(hangmanElem)
            hangmanElem = line
            count = 1
    hangman.append(hangmanElem)                         # hozzaadja az utso hangmaallapotot
# clear()
print("Milyen hosszú legyen a szó?")
wordLength = int(input())                               # ilyen hosszu szo jatszik

while wordLength not in wordLengthList or wordLength <= 2: # ha olyan szohosszt mond. ami nincs, akkor hulye
    print('Ilyen állat márpedig nincs')
    wordLength = int(input())

display = ""                                            # a jatekpalya
lastDisplay = ""                                        # vajon mi? a legutobbi display...

for i in range(0, wordLength):                          # a display annyi vonalka legyen, ahany betus a szo
    display += "-"
lastDisplay = display

print(display)

usedWrodsList = []                                      # azok a szavak, amik olyan hosszuak, amit mondott a juzer

for item in wordsList:                                  # megcsinalja a usedwordslistet
    if len(item) == wordLength:
        usedWrodsList.append(item)

gameWord = usedWrodsList[random.randint(0, len(usedWrodsList) - 1)] # kivalasztja a szot, amit ki kell talani

finish = False      # meg nincs vege a jateknak
usedChars = []      # ebben lesznek a betuk, amiket mar tippelt
roundCount = 0      # hanyszor baszta el

def normal(gameWord):                                   # normal nehezsegi szint. kozben rajottem, hogy nem kene parameter, de mar mindegy
    global usedChars
    global display    
    for item in gameWord:                               # vegignezi a gondolt szot
        if item in usedChars:                           # ha a gondolt szo adott betuje a hasznaltak kozott van, akkor az lesz a display kovi eleme
            display += item
        else:                                           # ha nincs, akkor egy vonalka lesz a display kovi eleme
            display += "-"

def gonosz(betu):                                       # gonosz es megoldhatatlan szint
    global usedChars
    global display
    global usedWrodsList
    global wordLength
    global gameWord
    tempListCont = []                                   # amely szavakban van a tippelt betu
    tempListNotCont = []                                # amely szavakban nincs a tippelt betu
    for item in usedWrodsList:                          # itt hozza letre a fenti ket listat
        if betu in item:
            tempListCont.append(item)
        else:
            tempListNotCont.append(item)
    if len(tempListCont) <= len(tempListNotCont):       # osszehasonlitja mibol mennyi van. Ha legalabb annyi szo nem tartalmazza a betut, mint igen, akkor a juzer "rontott", ez a lista megy tovabb a jatekban
        usedWrodsList = tempListNotCont
    else:                                               # ha tobb olyan szo van, amiben van a betu, akkor azzal dolgozunk tovabb
        charCount = {}                                  # ebben a dictionaryben tarolom a szavak listait aszerint, hogy a tippelt betu hanyszor szerepel bennuk
        for item in tempListCont:                       # vegigmegy a tippelt betut tartalmazo szavak listajan
            count = item.count(betu)                    # megnezi, hanyszor van benne a tippelt betu
            if count in charCount:                      # ha mar van olyan, amiben ennyiszer van a betu, hozzaadja ezt a szot is a listahoz
                charCount[count].append(item)
            else:                                       # ha nincs, uj listat rak a dictionarybe ezzel a szammal
                charCount[count] = [item]
        maxLenthListInCharCount = []                    # ez lesz a dictionary szo listaibol a legnagyobb, ez fog tovabbmenni vizsgalatra
        keysList = list(charCount.keys())               # egy uj listaba rakom a dictionary key-it
        keysList.sort()                                 # rendezem a key-k listajat
        for key in keysList:                            # ez keresi meg azt a listat, amiben a legtobb szo van
            if len(charCount[key]) > len(maxLenthListInCharCount):
                maxLenthListInCharCount = charCount[key]
        possibleWords = {}                              # ez egy dictinary amiben tovabb fogom bontani a megmaradt szavak listajat az alapjan, hogy hol talalhato az adott szoban a tippelt betu
        for item in maxLenthListInCharCount:
            tempKey = ""                                # a possibleWords dictionary key-i a tippelt betu helyei lesznek, pl ha a k-t tippelte a juzer, az "akkor" szoban k van a 2. es 3. helyen, az ezt a szot tartalmazo lista key-ja 23
            for i in range(0,len(item)):
                if item[i] == betu:
                    tempKey += str(i)
            if tempKey in possibleWords:
                possibleWords[tempKey].append(item)
            else:
                possibleWords[tempKey] = [item]
        finalList = []                                  # ez mar a vegleges lista lesz, a szavak, amik tovabbmennek a kovetkezo korre
        keysList = list(possibleWords.keys())
        keysList.sort(reverse=True)
        for key in keysList:                            # megkeresi a legnagyobb listat a possibleWords dictionaryben
            if len(possibleWords[key]) > len(finalList):
                finalList = possibleWords[key]
        usedWrodsList = finalList                       # a finalList tovabbmegy
    gameWord = usedWrodsList[0]                         # a kiiratashoz a gameWord a usedWrodslist nulladik eleme lesz
    normal(gameWord)                                    # kiirom a normal jatek szerint, hogy hol tart emberunk

while finish == False:                                  # ez maga a jatek
    if roundCount >= len(hangman) - 1:                  # ha fel van akasztodva az ember (ha annyiszor baszta el, ahany akaszottember allapot van), kiugrik ,csokolom
        break
    clear()                                             # takaritsuk le a kepernyot minden kor elejen
    print(hangman[roundCount])                          # aktualis akasztottsagi allapot kirajzolasa
    print(display)                                      # aktualis szokitalaltsagi allapot kirajzolasa
    print(usedChars)                                    # mar tippelt betuk kiirasa
    print("Mondj egy betűt")
    nextChar = input()                                  # amit beir, azt tippeli (mivan???? ennek a kommentnek nincs ertelme)
    nextChar = nextChar.lower()                         # haaahaaaa, azt hitted nagybetuvel kibaszhatsz velem? HAT NEM
    while nextChar in usedChars or len(nextChar) != 1:  # ha ez a szerencsecsomag olyan betut ir, ami mar volt, vagy nem csak egy betut ir, akkor hulye
        if nextChar in usedChars:                       # ha mar volt, akkor csak kicsit hulye
            print("Volt már")
        else:
            print("Hülye vagy?")                        # ha nem csak egy karakter, akkor nagyon hulye
        nextChar = input()
        nextChar = nextChar.lower()
                                                        # arra nincs felkeszitve a progi, hogy ha nem betu a valasztott karakter. Persze a teljes abc-t berakhatnam egy listaba es ellenorizhetnem...
    usedChars.append(nextChar)                          # a tippelt betu bekerul a hasznaltak koze  
    display = ""                                        # lenullazza a displayt
    
    if difficulty == 'normál':                          # normal nehezseg alapjan megyunk tovabb a gondolt szoval
        normal(gameWord)
    else:                                               # ha gonosz vagy megoldhatatlan szintet valasztott a juzer, megyunk tovabb a gonosszal
        gonosz(nextChar)

    if lastDisplay == display:                          # ha nem valtozott a display, akkor a juzer nem talalt ki uj betut, azaz no a hibak szama
        roundCount += 1
    
    lastDisplay = display                               # ellenorzes utan a mostani kor lesz a legutobbi kor
    
    if display == gameWord:                             # ha kitalalta a szot, akkor vege a jateknak
        finish = True

if finish:                                              # ha kitalalassal jott ki a while-bol, akkor nyert
    print("Nyertél")
else:                                                   # ha break-kel, akkor veszitett
    print (hangman[len(hangman) - 1])
    print("Lúzer")
print(gameWord)