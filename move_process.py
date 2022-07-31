import math
import random
from operator import itemgetter
from typing import List, Dict

def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict],
    possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]
    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    neck = my_body[1]

    if len(possible_moves) == 1:
        return possible_moves
    if neck["x"] < my_head["x"] and "left" in possible_moves:  # my neck is left of my head
      possible_moves.remove("left")
    elif neck["x"] > my_head["x"] and "right" in possible_moves:  # my neck is right of my head
      possible_moves.remove("right")
    elif neck["y"] < my_head["y"] and "down" in possible_moves:  # my neck is below my head
      possible_moves.remove("down")
    elif neck["y"] > my_head["y"] and "up" in possible_moves:  # my neck is above my head
      possible_moves.remove("up")

    return possible_moves

def avoid_walls(board_width: int, my_head: Dict[str, int],
possible_moves: List[str]) -> List[str]:
    x_walls_start = 0
    x_walls_end = board_width - 1
    y_walls_start = 0
    y_walls_end = board_width - 1

    if (my_head["x"] == x_walls_start) and "left" in possible_moves:
      possible_moves.remove("left")
    if my_head["y"] == y_walls_start and "down" in possible_moves:
      possible_moves.remove("down")
    if my_head["y"] == y_walls_end and "up" in possible_moves:
        possible_moves.remove("up")
    if my_head["x"] == x_walls_end and "right" in possible_moves:
      possible_moves.remove("right")

    return possible_moves

def food_moves(food_location: Dict[str, int],my_head: Dict[str, int], possible_moves: List[str]):
  print(f"Food: {food_location}")
  # Sort list of food x'y
  head_x = my_head["x"]
  head_y = my_head["y"]
  for location in food_location:
    dist = math.sqrt( (head_x - location["x"])**2 + (head_y - location["y"])**2 )
    location["dist"] = dist
  print(f"Unsorted food: {food_location}")
  sorted_food_locations = sorted(food_location, key=itemgetter('dist'))

  print(f"Sorted Food: {sorted_food_locations}")

  food_moves = []
  for food in sorted_food_locations:
    # Add a direction to a list for each food item
    # The closest food is first in the list
    x_diff = food["x"] - my_head["x"]
    y_diff = food["y"] - my_head["y"]

    if x_diff > 0:
      food_moves.append("right")
    elif x_diff < 0:
      food_moves.append("left")
    elif y_diff > 0:
      food_moves.append("up")
    elif y_diff < 0:
      food_moves.append("down")
   
    return food_moves
      

def move_x(x_diff, possible_moves: List[str]):
  if x_diff > 0 and "left" in possible_moves:
    possible_moves.remove("left")
  else:
    possible_moves.remove("right")

def move_y(y_diff, possible_moves: List[str]):
  if y_diff > 0 and "down" in possible_moves:
    possible_moves.remove("down")
  else:
    possible_moves.remove("up")


def move_it(data: dict) ->str:
  my_head = data["you"]["head"]
  my_body = data["you"]["body"]
  board = data["board"]
  
  # print(f"All board data this turn: {data}")
  print(f"My Battlesnakes head this turn is: {my_head}")
  print(f"My Battlesnakes body this turn is: {my_body}")
  possible_moves = ["up", "down", "left", "right"]

  # Don't allow your Battlesnake to move back in on it's own neck
  possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
  print(f"Possible moves after neck: {possible_moves}")

  possible_moves = avoid_walls(board["width"], my_head, possible_moves)
  print(f"Possible moves after wall: {possible_moves}")

  if len(possible_moves) == 1:
    return possible_moves[0]
  
  build_snake_moves(data, possible_moves)
  print(f"Possible moves after snake moves: {possible_moves}")

  if len(possible_moves) == 1:
    return possible_moves[0]

 
  food_directions = food_moves(data["board"]["food"], my_head, possible_moves)
  print(f"food_directions: {food_directions}")

  if food_directions:
    for direction in food_directions:
      if direction in possible_moves:
        print(f"MOVE for food: {direction}")
        return direction

  move = random.choice(possible_moves)
  print(f"MOVE: {move}")
  return move

def is_risky_move(board: dict, my_head: dict, my_snake_id: str):
  x_walls_start = 0
  x_walls_end = board["width"] - 1
  y_walls_start = 0
  y_walls_end = board["height"] - 1
  print("In risky moves function")
  print(f"My head: {my_head}")
  print(f"Wall: x start:{x_walls_start}, x end:{x_walls_end}, y start: {y_walls_start}, y end: {y_walls_end}")

  for enemy in board["snakes"]:
    if my_snake_id == enemy["id"]:
      continue

    # Is my head next to a wall
    if my_head["x"] == x_walls_start:
      #Left edge of board, can only move up or down
      #Check up and down for enemies causing trap
      # enemy y values 1 down and 1 across from my_head
      enemy_body_part_down = {"x":my_head['x'] + 1, "y":my_head["y"] - 1}
      for part in enemy["body"]:
        if part == enemy_body_part_down:
          #go the other direction
          return "up"
        else:
          return "down"

    if my_head["y"] == y_walls_start:
      # Bottom edge of board
      enemy_body_part_left = {"x":my_head['x'] - 1, "y":my_head["y"] + 1}

      for part in enemy["body"]:
        if part == enemy_body_part_left:
          #go the other direction
          return "right"
        else:
          return "left"
   
    if my_head["y"] == y_walls_end:
      #Top edge of board, can only go left or right
      #Check left and right for enemies causing trap
      # enemy y values 1 down and 1 across from my_head
      enemy_body_part_left = {"x":my_head['x'] - 1, "y":my_head["y"] - 1}

      for part in enemy["body"]:
        if part == enemy_body_part_left:
          #go the other direction
          return "right"
        else:
          return "left"
            
    if my_head["x"] == x_walls_end:
      # Right edge of board
      enemy_body_part_down = {"x":my_head['x'] - 1, "y":my_head["y"] - 1}

      for part in enemy["body"]:
        if part == enemy_body_part_down:
          #go the other direction
          return "up"
        else:
          return "down"
  return None

def check_for_enemies(my_snake_id: str, other_snakes: list, my_head_key: str, my_snake: dict, possible_moves: List[str], remove_direction: str, dir_val: int):
  move_removed = False
  my_head = my_snake["head"]


  head_other_key = "x" if my_head_key == "y" else "y"
  next_head_val = my_head[my_head_key] + dir_val

  for snake in other_snakes:
    if my_snake_id == snake["id"]:
      continue
  
    counter = 0
    for part in snake["body"]:
      if my_head[head_other_key] == part[head_other_key] and (next_head_val == part[my_head_key] or (next_head_val + dir_val) == part[my_head_key]):
        # Check if this part is the enemy head
        # if (part == snake["head"]) and (my_snake["length"] <= snake["length"]):
            #attack
          # return

        possible_moves.remove(remove_direction)
        move_removed = True
        break
      counter += 1

    # Check enemy head loaction and body length, avoid if not strong enough
    if my_snake["length"] <= snake["length"]:
      enemy_head = snake["head"]
    
      if next_head_val == enemy_head[my_head_key] and my_head[head_other_key] - 1 == enemy_head[head_other_key]:
        possible_moves.remove(remove_direction)
        break
  
      if next_head_val == enemy_head[my_head_key] and my_head[head_other_key] + 1 == enemy_head[head_other_key]:
        possible_moves.remove(remove_direction)
        break
      
      if next_head_val == enemy_head[my_head_key] and my_head[head_other_key] + 1 == enemy_head[head_other_key]:
        possible_moves.remove(remove_direction)
        break 
      
    if move_removed:
      break

  print(f"Possible moves after enemies: {possible_moves}")

def check_for_own_body(my_body: list, my_head_key: str, my_head: dict, possible_moves: List[str], remove_direction: str, dir_val: int):
  counter = 0
  body_part_counter = 0
  move_removed = False

  head_other_key = "x" if my_head_key == "y" else "y"
  next_head_val = my_head[my_head_key] + dir_val

  for part in my_body:

    #Ignore head and neck as they are done already
    if body_part_counter < 2:
      body_part_counter += 1
      continue

    if my_head[head_other_key] == part[head_other_key] and (next_head_val == part[my_head_key] or (next_head_val + dir_val) == part[my_head_key]):
      possible_moves.remove(remove_direction)
      print(f"Removed: {remove_direction}")
      move_removed = True
      break
    counter += 1
  return move_removed
  
def build_snake_moves(data: dict, possible_moves: List[str]):
  print(f"build_snake_moves - Possible moves: {possible_moves}")
  my_snake_id = data["you"]["id"]
  my_snake = data["you"]
  food = data["board"]["food"]
  head = data["you"]["head"]
  my_body = data["you"]["body"]
  other_snakes = data["board"]["snakes"]

  if len(food) > 0:
    sorted_food_locations = sorted(food, key=itemgetter('x'))
    sorted(sorted_food_locations, key=itemgetter('y'))

  # for each possible move direction detect food, enemy or self
  for direction in list(possible_moves):
    counter = 0
    move_removed = False
    print(f"Possible moves for direction:{direction} {possible_moves}")

    if direction == "down":
      #down is a y direction
      hy = head["y"]

      # Any own body in this direction
      move_removed = check_for_own_body(my_body, "y", head, possible_moves, "down", -1)
      if move_removed:
        continue

      # Any enemies in this direction
      check_for_enemies(my_snake_id, other_snakes,"y", my_snake, possible_moves, "down", -1)
      
    if direction == "up":
      #up is a y direction
      hy = head["y"]
      # Any own body in this direction
      move_removed = check_for_own_body(my_body, "y", head, possible_moves, "up", 1)

      if move_removed:
        continue

      # Any enemies in this direction
      check_for_enemies(my_snake_id, other_snakes,"y", my_snake, possible_moves, "up", 1)
   
    if direction == "left":
      #left is an x direction
      hx = head["x"]
      # Any own body in this direction
      move_removed = check_for_own_body(my_body, "x", head, possible_moves, "left", -1)

      if move_removed:
        continue

      # Any enemies in this direction
      check_for_enemies(my_snake_id, other_snakes,"x", my_snake, possible_moves, "left", -1)

    if direction == "right":
      #right is an x direction
      hx = head["x"]
      # Any own body in this direction
      move_removed = check_for_own_body(my_body, "x", head, possible_moves, "right", 1)
      if move_removed:
        continue

      # Any enemies in this direction      
      check_for_enemies(my_snake_id, other_snakes,"x", my_snake, possible_moves, "right", 1)

  risky_direction = is_risky_move(data["board"], head, my_snake_id)
  print(f"Risky direction: {risky_direction}")
  if risky_direction and risky_direction in possible_moves:
    possible_moves.remove(risky_direction)
                   