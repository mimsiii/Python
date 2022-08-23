from statistics import mode
import numpy as np
from numpy import random
import time
import os


names = np.array(['Ivan','Yordan','Mariya','Valeri','Iliyana','Gergana'])
allDices = 0
playGame = True


def pause():
    time.sleep(0.7)
    
def clear_console():
    os.system('cls') 
    
    
class Player:
    
    def plName(self):
        name = input("Name: ")
        while not name:
            name = input("Name was not typed in. Please type in your name: ")
        return name
    
    def playerCount(self):
        numberPlayers = 0
        while True:
            try:
                while numberPlayers < 2 or numberPlayers > 5:
                    numberPlayers = int(input("Type in number of players between 2 and 5: "))
                break
            except ValueError:
                print("Oops!  Something went wrong with the typed in value.  Try again...") 
        return numberPlayers
    
    
class BotPlayer:
    
    def botName(self):
        global names
        
        name = random.choice(names)
        index = np.where(names == name)
        names = np.delete(names,index)
        
        return name
    
    
class InitPlayers(Player,BotPlayer):
   
    def initPlayerDict(self, numberPlayers, yourName):
        global names
        playerList = []
        playerDict = {}
        
        for i in range(numberPlayers):
            if i == 0:
                playerList.append(yourName)
                continue
            playerList.append(self.botName())
            
        np.random.shuffle(playerList)
        
        for ind,x in enumerate(playerList):
            playerDict[ind] = {}
            playerDict[ind]["name"] = x
            playerDict[ind]["numberDice"] = 5
            
        return playerDict
    
    
class GameMethods:
    
    def luckyDices(self,playerDict):
        for p_id in range(len(playerDict.items())):
            playerDict[p_id]["luckyDices"] = list(random.choice([1,2,3,4,5,6], size=(playerDict[p_id]['numberDice'])))
      
    def checkPlayerCount(self,playerDict,previous_player,current_player):
        global allDices
        countOfNum = 0
        finalArr = []
        
        for p_id in range(len(playerDict.items())):
            finalArr+=playerDict[p_id]["luckyDices"]
            
        for el in finalArr:
            if el == int(playerDict[previous_player]["expNum"]) or el == 1:
                countOfNum += 1
                
        if countOfNum >= int(playerDict[previous_player]["expCount"]):
            playerDict[current_player]["numberDice"]-=1
            allDices -= 1
            
            pause()
            print(finalArr)
            pause()
            print("There were", countOfNum, "x", playerDict[previous_player]["expNum"])
            pause()
            print("The bet was", playerDict[previous_player]["expCount"], "x", playerDict[previous_player]["expNum"])
            pause()
            print(playerDict[current_player]["name"], "lost a die. Dice left:", playerDict[current_player]["numberDice"])
            pause()
                 
            return True 
        else:
            playerDict[previous_player]["numberDice"]-=1
            allDices -= 1
            
            pause()
            print(finalArr)
            pause()
            print("There were", countOfNum, "x", playerDict[previous_player]["expNum"])
            pause()
            print("The bet was", playerDict[previous_player]["expCount"], "x", playerDict[previous_player]["expNum"])
            pause()
            print(playerDict[previous_player]["name"], "lost a die. Dice left:", playerDict[previous_player]["numberDice"])
            pause()
            
            return False
                
            
class Game(InitPlayers, GameMethods):
    
    def __init__(self):
        self.numberPlayers = self.playerCount()
        self.yourName = self.plName()
        self.playerDict = self.initPlayerDict(self.numberPlayers, self.yourName) 
        
    def reorderDictionary(self,index):
        global playGame
        x = {}
        for p_id in range(len(self.playerDict.items())):
            current_player = index % len(self.playerDict)
            x[p_id] = self.playerDict[current_player]
            index+=1
            
        y = {}
        counter = 0
        for p_id in range(len(x.items())):
            if x[p_id]["numberDice"] != 0:
                y[counter] = x[p_id]
                counter+=1
            elif x[p_id]["name"] == self.yourName and x[p_id]["numberDice"] == 0:
                print("Game over! You lost.")
                playGame = False
                break 
            else:
                pause()
                print(x[p_id]["name"], "lost.")
                pause()
                
        return y  
          
    def plBets(self):
        global allDices
        global playGame
        
        allDices = self.numberPlayers * 5
        notFirstPlayer = False
        
        self.luckyDices(self.playerDict)
        
        while playGame:
            
            if len(self.playerDict.items()) == 1:
                pause()
                print("You won")
                break
            
            countOfPCNum = 0
            mainCountMinimum = 0
            roundOver = False
            
            pause()
            print("All dices:", allDices)
            pause()
            
            while roundOver == False:
                
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
                                
                                if self.checkPlayerCount(self.playerDict,previous_player,p_id) is True:
                                    self.playerDict = self.reorderDictionary(p_id)
                                    if playGame == False:
                                        break
                                else: 
                                    self.playerDict = self.reorderDictionary(previous_player) 
                                      
                                roundOver = True  
                                notFirstPlayer = False 
                                         
                                self.luckyDices(self.playerDict)
                                
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
                                    pause()
                                break
                            except ValueError:
                                print("Oops!  Something went wrong with the typed in value.  Try again...")
                                pause()
                        pause()
                        
                        while True:
                            try:
                                self.playerDict[p_id]["expNum"] = int(input("Number: "))
                                while self.playerDict[p_id]["expNum"] > 6 or self.playerDict[p_id]["expNum"] < 1:
                                    self.playerDict[p_id]["expNum"] = int(input("Place a number between 1 and 6: "))
                                    pause()
                                break
                            except ValueError:
                                print("Oops!  Something went wrong with the typed in value.  Try again...")
                                pause()
                                
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
                            
                            if self.checkPlayerCount(self.playerDict,previous_player,p_id) is True:
                                self.playerDict = self.reorderDictionary(p_id)
                                if playGame == False:
                                    break
                            else: 
                                self.playerDict = self.reorderDictionary(previous_player)
                                if playGame == False:
                                    break
                                
                            self.luckyDices(self.playerDict)
                            
                            notFirstPlayer = False
                            roundOver = True
                            
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
                        
clear_console()
newGame = Game()
newGame.plBets()
