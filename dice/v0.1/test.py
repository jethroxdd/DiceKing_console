import random
import dices
from entity import Entity
import copy
import enemies
from systems import RoundSystem
from room import NewDiceRoom, EventRoom, StoreRoom
from color import *

def main():
    initial_dices = copy.deepcopy(random.sample(dices.ALL, 6))
    player = Entity("Player", 100, initial_dices)
    player.gold = 10  # Starting gold
    
    weak_enemies = [enemies.rat, enemies.goblin, enemies.slime]

    for stage in range(1, 10):
        print(f"\n=== STAGE {stage} ===")
        
        # Generate rooms with store chance
        num_rooms = random.randint(2, 3)
        rooms = []
        for _ in range(num_rooms):
            if random.random() < 0.3:  # 30% chance for store
                rooms.append(StoreRoom())
            else:
                rooms.append(random.choice([NewDiceRoom, EventRoom])())
        
        # Choose room
        print(f"{YELLOW}Gold: {player.gold}{RESET}")
        print("Choose a room:")
        for i, room in enumerate(rooms):
            print(f"{i+1}) {room.description}")
        
        while True:
            choice = input(f"Enter choice (1-{num_rooms}): ")
            if choice.isdigit() and 1 <= int(choice) <= num_rooms:
                rooms[int(choice)-1].enter(player)
                break
            print("Invalid choice!")

        # Combat phase
        enemy = copy.deepcopy(random.choice(weak_enemies))
        print(f"\n{RED}Encountered {enemy.name}!{RESET}")
        enemy.setTarget(player)
        player.setTarget(enemy)
        
        game = RoundSystem(player, enemy)
        game.start()
        
        if player.isDead:
            print("Game Over!")
            return
        
        # Gold reward
        gold_earned = random.randint(10, 20)
        player.gold += gold_earned
        print(f"\n{YELLOW}Acquired {gold_earned} gold! Total: {player.gold}{RESET}")

    # Final boss
    print("\n=== FINAL BOSS ===")
    boss = copy.deepcopy(enemies.dragon)
    player.setTarget(boss)
    boss.setTarget(player)
    
    final_game = RoundSystem(player, boss)
    final_game.start()

if __name__ == "__main__":
    main()