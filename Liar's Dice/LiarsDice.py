from statistics import mode
import numpy as np
from numpy import random
import time
import os


names = np.array(['Ivan','Yordan','Mariya','Valeri','Iliyana','Gergana'])
all_dices = 0
play_game = True


def pause():
    time.sleep(0.7)
    
def clear_console():
    os.system('cls') 
    
    
class Player:
    
    def pl_name(self):
        name = input("Name: ")
        while not name:
            name = input("Name was not typed in. Please type in your name: ")
        return name
    
    def players_count(self):
        number_players = 0
        while True:
            try:
                while number_players < 2 or number_players > 5:
                    number_players = int(input("Type in number of players between 2 and 5: "))
                break
            except ValueError:
                print("Oops!  Something went wrong with the typed in value.  Try again...") 
        return number_players
    
    
class BotPlayer:
    
    def bot_name(self):
        global names
        
        name = random.choice(names)
        index = np.where(names == name)
        names = np.delete(names,index)
        
        return name
    
    
class InitPlayers(Player,BotPlayer):
   
    def init_players_dict(self, number_players, your_name):
        global names
        player_list = []
        player_dict = {}
        
        for i in range(number_players):
            if i == 0:
                player_list.append(your_name)
                continue
            player_list.append(self.bot_name())
            
        np.random.shuffle(player_list)
        
        for ind,x in enumerate(player_list):
            player_dict[ind] = {}
            player_dict[ind]["name"] = x
            player_dict[ind]["numberDice"] = 5
            
        return player_dict
    
    
class GameMethods:
    
    def lucky_dices(self,player_dict):
        for p_id in range(len(player_dict.items())):
            player_dict[p_id]["lucky_dices"] = list(random.choice([1,2,3,4,5,6], size=(player_dict[p_id]['numberDice'])))
      
    def check_players_bets(self,player_dict,previous_player,current_player):
        global all_dices
        count_of_num = 0
        final_arr = []
        
        for p_id in range(len(player_dict.items())):
            final_arr+=player_dict[p_id]["lucky_dices"]
            
        for el in final_arr:
            if el == int(player_dict[previous_player]["expNum"]) or el == 1:
                count_of_num += 1
                
        if count_of_num >= int(player_dict[previous_player]["expCount"]):
            player_dict[current_player]["numberDice"]-=1
            all_dices -= 1
            
            pause()
            print(final_arr)
            pause()
            print("There were", count_of_num, "x", player_dict[previous_player]["expNum"])
            pause()
            print("The bet was", player_dict[previous_player]["expCount"], "x", player_dict[previous_player]["expNum"])
            pause()
            print(player_dict[current_player]["name"], "lost a die. Dice left:", player_dict[current_player]["numberDice"])
            pause()
                 
            return True 
        else:
            player_dict[previous_player]["numberDice"]-=1
            all_dices -= 1
            
            pause()
            print(final_arr)
            pause()
            print("There were", count_of_num, "x", player_dict[previous_player]["expNum"])
            pause()
            print("The bet was", player_dict[previous_player]["expCount"], "x", player_dict[previous_player]["expNum"])
            pause()
            print(player_dict[previous_player]["name"], "lost a die. Dice left:", player_dict[previous_player]["numberDice"])
            pause()
            
            return False
                
            
class Game(InitPlayers, GameMethods):
    
    def __init__(self):
        self.number_players = self.players_count()
        self.your_name = self.pl_name()
        self.player_dict = self.init_players_dict(self.number_players, self.your_name) 
        
    def reorder_dictionary(self,index):
        global play_game
        x = {}
        for p_id in range(len(self.player_dict.items())):
            current_player = index % len(self.player_dict)
            x[p_id] = self.player_dict[current_player]
            index+=1
            
        y = {}
        counter = 0
        for p_id in range(len(x.items())):
            if x[p_id]["numberDice"] != 0:
                y[counter] = x[p_id]
                counter+=1
            elif x[p_id]["name"] == self.your_name and x[p_id]["numberDice"] == 0:
                print("Game over! You lost.")
                play_game = False
                break 
            else:
                pause()
                print(x[p_id]["name"], "lost.")
                pause()
                
        return y  
          
    def pl_bets(self):
        global all_dices
        global play_game
        
        all_dices = self.number_players * 5
        not_first_player = False
        
        self.lucky_dices(self.player_dict)
        
        while play_game:
            
            if len(self.player_dict.items()) == 1:
                pause()
                print("You won")
                break
            
            count_of_pc_num = 0
            main_count_minimum = 0
            round_over = False
            
            pause()
            print("All dice:", all_dices)
            pause()
            
            while round_over == False:
                
                for p_id in range(len(self.player_dict.items())):
                    self.player_dict[p_id]["callALiar"] = ''
                    previous_player = (p_id - 1) % len(self.player_dict)
                    
                    if self.player_dict[p_id]["name"] == self.your_name:
                        print("Your lucky dices:", self.player_dict[p_id]["lucky_dices"])
                        
                        if not_first_player:
                            pause()
                            
                            if input("Type in 'y' to call previous player a liar or press enter to continue: ") == 'y':
                                pause()
                                print(self.player_dict[p_id]["name"],"calls",self.player_dict[previous_player]["name"],"a liar.")
                                
                                if self.check_players_bets(self.player_dict,previous_player,p_id) is True:
                                    self.player_dict = self.reorder_dictionary(p_id)
                                    if play_game == False:
                                        break
                                else: 
                                    self.player_dict = self.reorder_dictionary(previous_player) 
                                      
                                round_over = True  
                                not_first_player = False 
                                         
                                self.lucky_dices(self.player_dict)
                                
                                pause()
                                input("Press enter to continue to next round.")
                                clear_console()
                                print("Next round starts...")
                                pause()
                                pause()
                                clear_console()
                                
                                break
                            
                            not_first_player = True
                        pause()
                        
                        while True:
                            try:
                                self.player_dict[p_id]["expCount"] = int(input("Expected count of number: "))
                                while self.player_dict[p_id]["expCount"] <= main_count_minimum:
                                    self.player_dict[p_id]["expCount"] = int(input("Place a count grater than the previous: "))
                                    pause()
                                break
                            except ValueError:
                                print("Oops!  Something went wrong with the typed in value.  Try again...")
                                pause()
                        pause()
                        
                        while True:
                            try:
                                self.player_dict[p_id]["expNum"] = int(input("Number: "))
                                while self.player_dict[p_id]["expNum"] > 6 or self.player_dict[p_id]["expNum"] < 1:
                                    self.player_dict[p_id]["expNum"] = int(input("Place a number between 1 and 6: "))
                                    pause()
                                break
                            except ValueError:
                                print("Oops!  Something went wrong with the typed in value.  Try again...")
                                pause()
                                
                        main_count_minimum = int(self.player_dict[p_id]["expCount"])
                        pause()
                        
                    else:
                        self.player_dict[p_id]["expNum"] = mode(self.player_dict[p_id]["lucky_dices"])
                        
                        if not_first_player: 
                            self.player_dict[p_id]["callALiar"] = random.choice(['y','n'], p=(0.4,0.6), size=(1))
                            
                        for num in self.player_dict[p_id]["lucky_dices"]:
                            if num == self.player_dict[p_id]["expNum"] or num == 1:
                                count_of_pc_num += 1
                                
                        if count_of_pc_num >= main_count_minimum:
                            self.player_dict[p_id]["expCount"] = int(random.choice([count_of_pc_num+1, count_of_pc_num+2], size = (1)))
                        else:
                            self.player_dict[p_id]["expCount"] = int(random.choice([main_count_minimum+1, main_count_minimum+2], size = (1)))
                            if self.player_dict[p_id]["expCount"] >= all_dices-1:
                                self.player_dict[p_id]["callALiar"] = 'y'
                                
                        main_count_minimum = int(self.player_dict[p_id]["expCount"])
                        
                        if self.player_dict[p_id]["callALiar"] == 'y':
                            print(self.player_dict[p_id]["name"],"calls",self.player_dict[previous_player]["name"],"a liar.")
                            
                            if self.check_players_bets(self.player_dict,previous_player,p_id) is True:
                                self.player_dict = self.reorder_dictionary(p_id)
                                if play_game == False:
                                    break
                            else: 
                                self.player_dict = self.reorder_dictionary(previous_player)
                                if play_game == False:
                                    break
                                
                            self.lucky_dices(self.player_dict)
                            
                            not_first_player = False
                            round_over = True
                            
                            input("Press enter to continue to next round.")
                            clear_console()
                            print("Next round starts...")
                            pause()
                            pause()
                            clear_console()
                            pause()
                            
                            break
                        
                        not_first_player = True
                        
                        print(self.player_dict[p_id]["name"],"expects there are",self.player_dict[p_id]["expCount"],"x",self.player_dict[p_id]["expNum"])
                        pause()
                        
clear_console()
new_game = Game()
new_game.pl_bets()
