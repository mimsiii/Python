def palfunc(palstr):
    palstr2=[]
    for s in palstr:
        if s.isalnum():
            palstr2.append(s)
    if palstr2[::-1]==palstr2:
        return True
    return False

def main():
    userValue = input("Write a word to check if it's palindromic > ")
    userValue = userValue.casefold()

    while (userValue):
        if userValue == 'exit':
            break
        else:
            print(palfunc(userValue))
            userValue = input("Write a word to check if it's palindromic or write 'exit' to close > ")
            userValue = userValue.casefold()
            
    
if __name__ == "__main__":
    main()



      

