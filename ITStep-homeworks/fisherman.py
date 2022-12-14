# 3 fishermen caught X amount of fish. 
# The first one threw one out of the batch since he couldn't split the amount evenly in 3 and took a third of the fish.
# Later the 2-nd fisherman split them, threw one fish out since he couldn't evenly split the amount in 3 and took 1/3.
# Later again the 3-rd fisherman threw one fish out, split the amount into 3 and took 1/3. 
# After the 3-rd fisherman took his share the remaining fish was 6. How many fish was there at the begining(X)?

### 25 -> 24 -> 16 -> 15 -> 10 -> 9 -> 6

def find_fishes(fisherman, fishes):
    for fisher_man in range(fisherman):
        fishes = fishes + (fishes / (fisherman - 1)) + 1 
    return int(fishes)