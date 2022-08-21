from statistics import mode
import numpy as np
from numpy import random
import time
import os

playGame = True
names = np.array(['Ivan','Yordan','Mariya','Valeri','Iliyana','Gergana'])
allDices = 0
countOfNum = 0

def pause():
    time.sleep(0.7)
    
def clear_console():
    os.system('cls')  
      
class Game():
    def __init__(self,numberPlayers):
        self.numberPlayers = numberPlayers -1 
        self.playerList = []
        self.playerDict = {}
           
    def pcName(self):
        global names
        self.name = random.choice(names)
        index = np.where(names == self.name)
        names = np.delete(names,index)
        return self.name
    
    def initPlayers(self):
        global allDices
        global names
        for i in range(self.numberPlayers):
            if i == 0:
                self.name = input("Name: ")
                while self.name == '':
                    self.name = input("Name was not typed in. Please type in your name: ")
                self.playerList.append(str(self.name))
                self.yourName = self.name
            self.name = self.pcName()
            self.playerList.append(str(self.name))
        np.random.shuffle(self.playerList)
        allDices = numberPlayers*5
        n = 0
        for x in self.playerList:
            self.playerDict[n] = {}
            self.playerDict[n]["name"] = x
            self.playerDict[n]["numberDice"] = 5 
            n += 1 
    
    def luckyDices(self):
        self.finalArr = []
        self.expNumb = 0
        self.expCount = 0
        for p_id in range(len(self.playerDict.items())):
            self.playerDict[p_id]["luckyDices"] = list(random.choice([1,2,3,4,5,6], size=(self.playerDict[p_id]['numberDice'])))
            self.finalArr+=self.playerDict[p_id]["luckyDices"]
      
    def checkPlayerCount(self,p_id):
        global allDices
        global countOfNum
        for el in self.finalArr:
            if el == int(self.playerDict[p_id]["expNum"]) or el == 1:
                countOfNum += 1
        if countOfNum >= int(self.playerDict[p_id]["expCount"]):
            return True
        else:
            self.playerDict[p_id]["numberDice"]-=1
            allDices -= 1
            pause()
            print("There were", countOfNum, "x", self.playerDict[p_id]["expNum"])
            pause()
            print("The bet was", self.playerDict[p_id]["expCount"], "x", self.playerDict[p_id]["expNum"])
            pause()
            print(self.playerDict[p_id]["name"], "lost a die. Dice left:",self.playerDict[p_id]["numberDice"])
            pause()            
            
    def reorderDictionary(self,index):
        x = {}
        for el in range(len(self.playerDict.items())):
            current_player = index % len(self.playerDict)
            x[el] = self.playerDict[current_player]
            index+=1
        return x  
            
    def plBets(self):
        global playGame
        global allDices
        global countOfNum
        notFirstPlayer = False
        allDices = 0
        self.initPlayers()
        self.luckyDices()
        while playGame:
            countOfPCNum = 0
            mainCountMinimum = 0
            roundOver = False
            print("All dices:",allDices)
            pause()
            if len(self.playerDict.items()) == 1:
                pause()
                print("You won")
                playGame = False
            while roundOver == False:
                countOfNum = 0 
                for p_id in range(len(self.playerDict.items())):
                    self.playerDict[p_id]["callALiar"] = ''
                    previous_player = (p_id - 1) % len(self.playerDict)
                    if self.playerDict[p_id]["name"] == self.yourName:
                        print("Your lucky dices:", self.playerDict[p_id]["luckyDices"])
                        if notFirstPlayer:
                            pause()
                            if input("Type in 'y' to call previous player a liar or press enter to continue: ") == 'y':
                                pause()
                                print(self.playerDict[p_id]["name"],"calls",self.playerDict[previous_player]["name"],"a liar.")
                                pause()
                                print(self.finalArr)
                                roundOver = True
                                if self.checkPlayerCount(previous_player) == True:
                                    self.playerDict[p_id]["numberDice"]-=1
                                    allDices -= 1
                                    if self.playerDict[p_id]["numberDice"] == 0:
                                        print("Game over! You lost.")
                                        playGame = False
                                        break
                                    pause()
                                    print("There were", countOfNum, "x", self.playerDict[previous_player]["expNum"])
                                    pause()
                                    print(self.playerDict[p_id]["name"], "lost a die. Dice left:",self.playerDict[p_id]["numberDice"])
                                    self.playerDict = self.reorderDictionary(p_id)
                                else:
                                    self.playerDict = self.reorderDictionary(previous_player)
                                    x = {}
                                    counter = 0
                                    for p_id in range(len(self.playerDict.items())):
                                        if self.playerDict[p_id]["numberDice"] != 0:
                                            x[counter] = self.playerDict[p_id]
                                            counter+=1
                                    self.playerDict = x               
                                self.luckyDices()
                                notFirstPlayer = False
                                pause()
                                input("Press enter to continue to next round.")
                                clear_console()
                                print("Next round starts...")
                                pause()
                                pause()
                                clear_console()
                                break
                            notFirstPlayer = True
                        pause()
                        while True:
                            try:
                                self.playerDict[p_id]["expCount"] = int(input("Expected count of number: "))
                                while self.playerDict[p_id]["expCount"] <= mainCountMinimum:
                                    self.playerDict[p_id]["expCount"] = int(input("Place a count grater than the previous: "))
                                break
                            except ValueError:
                                print("Oops!  Something went wrong with the typed in value.  Try again...")
                        pause()
                        while True:
                            try:
                                self.playerDict[p_id]["expNum"] = int(input("Number: "))
                                while self.playerDict[p_id]["expNum"] > 6 or self.playerDict[p_id]["expNum"] < 1:
                                    self.playerDict[p_id]["expNum"] = int(input("Place a number between 1 and 6: "))
                                break
                            except ValueError:
                                print("Oops!  Something went wrong with the typed in value.  Try again...")
                        mainCountMinimum = int(self.playerDict[p_id]["expCount"])
                        pause()
                    else:
                        self.playerDict[p_id]["expNum"] = mode(self.playerDict[p_id]["luckyDices"])
                        if notFirstPlayer: 
                            self.playerDict[p_id]["callALiar"] = random.choice(['y','n'], p=(0.4,0.6), size=(1))
                        for num in self.playerDict[p_id]["luckyDices"]:
                            if num == self.playerDict[p_id]["expNum"] or num == 1:
                                countOfPCNum += 1
                        if countOfPCNum >= mainCountMinimum:
                            self.playerDict[p_id]["expCount"] = int(random.choice([countOfPCNum+1, countOfPCNum+2], size = (1)))
                        else:
                            self.playerDict[p_id]["expCount"] = int(random.choice([mainCountMinimum+1, mainCountMinimum+2], size = (1)))
                            if self.playerDict[p_id]["expCount"] >= allDices-1:
                                self.playerDict[p_id]["callALiar"] = 'y'
                        mainCountMinimum = int(self.playerDict[p_id]["expCount"])
                        if self.playerDict[p_id]["callALiar"] == 'y':
                            print(self.playerDict[p_id]["name"],"calls",self.playerDict[previous_player]["name"],"a liar.")
                            pause()
                            print(self.finalArr)
                            roundOver = True
                            if self.checkPlayerCount(previous_player) == True:
                                self.playerDict[p_id]["numberDice"]-=1
                                allDices -= 1
                                pause()
                                print("There were", countOfNum, "x", self.playerDict[previous_player]["expNum"])
                                pause()
                                print("The bet was", self.playerDict[previous_player]["expCount"], "x", self.playerDict[previous_player]["expNum"])
                                pause()
                                print(self.playerDict[p_id]["name"], "lost a die. Dice left:",self.playerDict[p_id]["numberDice"])
                                pause()
                                self.playerDict = self.reorderDictionary(p_id)
                                x = {}
                                counter = 0
                                for p_id in range(len(self.playerDict.items())):
                                    if self.playerDict[p_id]["numberDice"] != 0:
                                        x[counter] = self.playerDict[p_id]
                                        counter+=1
                                self.playerDict = x
                            else:
                                self.playerDict = self.reorderDictionary(previous_player)
                                x = {}
                                counter = 0
                                for p_id in range(len(self.playerDict.items())):
                                    if self.playerDict[p_id]["numberDice"] != 0:
                                        x[counter] = self.playerDict[p_id]
                                        counter+=1
                                self.playerDict = x
                            self.luckyDices()
                            notFirstPlayer = False
                            input("Press enter to continue to next round.")
                            clear_console()
                            print("Next round starts...")
                            pause()
                            pause()
                            clear_console()
                            pause()
                            break
                        notFirstPlayer = True
                        print(self.playerDict[p_id]["name"],"expects there are",self.playerDict[p_id]["expCount"],"x",self.playerDict[p_id]["expNum"])
                        pause()
                            
numberPlayers = 0

clear_console()
print("Game starts")  
clear_console() 
     
while True:
    try:
        while numberPlayers < 2 or numberPlayers > 5:
            numberPlayers = int(input("Type in number of players between 2 and 5: "))
        break
    except ValueError:
        print("Oops!  Something went wrong with the typed in value.  Try again...") 
        
pause()
newGame = Game(numberPlayers)
newGame.plBets()