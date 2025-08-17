import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

MAX_ITERATION = 1_000_000

class Person:
    capacity: int
    current_capacity: int
    recharge: int
    name: str
    is_dead: bool
    died_on: int
    
    def __init__(self, capacity, recharge, name = None):
        self.capacity = capacity
        self.current_capacity = capacity
        self.recharge = recharge
        self.name = f"{self.capacity}-{self.recharge}" if name == None else name
        self.is_dead = False
        
    def iterate(self, number):
        if (self.is_dead): return
        
        if (is_prime(number)):
            self.current_capacity = min(self.current_capacity + self.recharge, self.capacity)
        else:
            self.current_capacity -= 1
        
        if (self.current_capacity <= 0 or number >= MAX_ITERATION): 
            # print(f"\tPLayer {self.__repr__()} died on {number}")
            self.is_dead = True
            self.died_on = number
    
    def __str__(self): return self.name
    
    def __repr__(self): return f"{self.capacity}-{self.recharge}[{self.current_capacity}]"

def is_prime(n: int) -> bool:
    root = n ** 0.5
    
    if (n <= 1): return False
    for i in range(2, int(root) + 1):
        if (n % i == 0): return False
    return True

def any_alive(arr):
    for player in arr:
        if (not player.is_dead): return True
    return False
    
def main():
    # Settings
    min_capacity = 1
    max_capacity = 100
    min_recharge = -1
    max_recharge = 100
    
    # Create players
    players = []    
    for cap in range(min_capacity, max_capacity + 1):
        for recharge in range(min_recharge, max_recharge + 1):
            players.append(Person(cap, recharge))


    # PLay the game
    num = 1
    while (any_alive(players)):
        if (num % 100 == 0): print(f"Checking {num}")
        
        for player in players:
            player.iterate(num)  
        num += 1     
        
    create_heatmap(players)
        

def create_heatmap(players, save_as = None):
    lookup = {(player.capacity, player.recharge): player.died_on for player in players}
    
    # Get grid size
    row_max = max(player.capacity for player in players)
    col_max = max(player.recharge for player in players)
    row_min = min(player.capacity for player in players)
    col_min = min(player.recharge for player in players)
    row_total = row_max - row_min + 1
    col_total = col_max - col_min + 1
    
    # Fill array
    grid = np.full((row_total, col_total), np.nan)
    for player in players:
        grid[player.capacity - row_min, player.recharge - col_min] = player.died_on
        
    plt.imshow(grid,
               cmap="viridis",
               origin="lower",
               extent=[row_min, row_max + 1, col_min, col_max + 1],
               aspect="auto")
    plt.colorbar(label="lasted")
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.xlabel("Capacity")
    plt.ylabel("Recharge rate")
    plt.title("Deaths of players")
    plt.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    main()