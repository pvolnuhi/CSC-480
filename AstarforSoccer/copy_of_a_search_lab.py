# -*- coding: utf-8 -*-
"""Copy of A* Search Lab

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C9K3HWig1y7x26r25LYaZYd_AkC-iIpC

## A* Search
A* search is an informed search algorithm that acheives better performance than other best-first approaches by using a heuristic funciton to guide its search. In this lab, you will apply A* Search to the problem of goal scoring in robotic soccer. The goal is to plan an attacking path.

## Part 1: Define the Field
In this part, the field must be defined. We will represent the field as a 2 dimensional numpy array. A numpy array is like a python array, but it can be transformed using cpython code, which makes it faster for vector transformations. Coordinates on this field will be represtented as python tuples. This class exposes functions to change ball and player positions.
"""

import numpy as np 
import copy

class Field:

  def __init__(self, width=24, length=36, attacker='left'):
    self.width = width
    self.length = length
    self.attacker = attacker
    self.ball = None
    self.kicks = []
    self.players = {}
    self.field = \
      np.vstack((
        np.full((max(1, width // 5), length), '_', dtype=str),
        np.hstack((
          np.full((width - 2 * max(1, width // 5), 1), 'G', dtype=str),
          np.full((width - 2 * max(1, width // 5), length - 2), '_', dtype=str),
          np.full((width - 2 * max(1, width // 5), 1), 'G', dtype=str)
        )),
      np.full((max(1, width // 5), length), '_', dtype=str),
      ))
    self.init_ball()
    self.init_players()

  def init_ball(self):
    self.set_ball((self.width // 2, self.length // 2))

  def get_ball(self):
    return self.ball

  def set_ball(self, position):
    if self.ball:
      self.field[self.ball[0]][self.ball[1]] = '_'
    self.ball = position
    self.field[position[0], position[1]] = 'B'

  def init_players(self):     
    self.set_player('1', (self.width // 4, self.length // 2 - 1))
    self.set_player('3', (3 * self.width // 4, self.length // 2 - 1))
    self.set_player('4', (self.width // 4, self.length // 2 + 1))
    self.set_player('6', (3 * self.width // 4, self.length // 2 + 1))
    if self.attacker == 'left':
      self.set_player('5', (self.width // 2, 
                            self.length // 2 + 1 + self.length // 10))
      self.set_player('2', (self.width // 2, self.length // 2 - 1))
    else:
      self.set_player('5', (self.width // 2, self.length // 2 + 1))
      self.set_player('2', (self.width // 2, 
                            self.length // 2 - 1 - self.length // 10))

  def get_players(team='left'):
    if team == 'left':
      return {p: self.players[p] for p in self.players if int(p) < 4}
    else:
      return {p: self.players[p] for p in self.players if int(p) > 3}

  def set_player(self, player, position):
    if player in self.players:
      x, y = self.players[player]
      self.field[x][y] = '_'
    self.players[player] = position
    self.field[position[0]][position[1]] = player

  def is_open(self, position):
    return self.field[position[0], position[1]] == '_' or \
    self.field[position[0], position[1]] == 'G'

  def get_goal(self, side='right'):
    if side == 'left':
      return [(x, 0) for x in 
              range(self.width // 5 + 1, 
                    self.width - 2 * max(1, self.width // 5)
              )]
    else:
      return [(x, self.length - 1) for x in 
              range(self.width // 5 + 1, 
                    self.width - 2 * max(1, self.width // 5)
              )]

  def execute_kick(self, kick):
    new = copy.deepcopy(self)
    new.kicks.append(kick)
    new.set_ball(kick.end)
    return new
  
  def __str__(self):
    return '\n'.join([' '.join(row) for row in self.field]) 

  def __repr__(self):
        return "Field(val={})".format(self.field)

myField = Field()
print(myField)

"""## Part 2: Generate Potential Kicks
Now that we have defined the field, we need to define possible kicks.

### Aside: Distance

When modeling the kick, we need to understand what measure of distance will be used. The two most simple ideas of distance are Manhattan Distance and Euclidian Distance. Manhattan distance measures the number of moves in a 2D grid, while euclidian distance is a measure of the straight line between two points on a grid. Manhattan distance is computationally cheaper, so on low power systems it is a much better solution. However, since the lab is running on a cloud instance, euclidian distance will be a better option due to the accuracy increase.
"""

import math, random
def manhattan_distance(p1, p2):
  return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def euclidian_distance(p1, p2):
  return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

points = [((random.randint(0, 1000), random.randint(0,1000)), 
           (random.randint(0, 1000), random.randint(0,1000))) \
         for i in range(10000)]
import time
t0 = time.process_time()
distances_m = [manhattan_distance(p1, p2) for p1, p2 in points]
print("Computation time (manhattan):", time.process_time() - t0)
t0 = time.process_time()
distances_e = [euclidian_distance(p1, p2) for p1, p2 in points]
print("Computation time (euclidian):", time.process_time() - t0)
error = sum([abs(m - e) / (e + 0.01) for m, e in zip(distances_m, distances_e)]) / len(points)
print("Distance average percent difference:", error)

"""### Possible Kicks 

To generate possible kicks, we will define a max kick radius and generate all possible ball positions within that radius
"""

class Kick:
  def __init__(self, start, end, dist):
    self.start = start
    self.end = end
    self.dist = dist
  
  def __str__(self):
    return '\n'.join("%s: %s" % item for item in [("Start", self.start), ("End", self.end), ("Dist", self.dist)])

def get_potential_kicks(field, radius=8, distance=euclidian_distance):
  kicks = []
  for x in range(max(field.ball[0] - radius, 0), 
                 min(field.ball[0] + radius, field.width)):
    for y in range(max(field.ball[1] - radius, 0),
                   min(field.ball[1] + radius, field.length)):
      d = distance(field.ball, (x, y))
      if d <= radius and field.is_open((x, y)):
        kicks.append(Kick(field.ball, (x, y), d))
  return kicks



myField = Field()
myKick = random.choice(get_potential_kicks(myField))
myKickedField = myField.execute_kick(myKick)
print(myField)
print(myKickedField)

"""## Part 3: Define Cost
Here is where your work begins. In order to decide which kick is optimal, we need a way of judging the quality of a kick. In this section, you will define a cost function, which should be a lower number if the kick is of higher quality. 

In this case, we will use the time it takes for the kick to complete as a measure of quality. This can be done by creating a physics model of the ball traveling accross the grass. An introduction of physics is out of scope for this assignment, so I will define an extremely basic kicking definition based on the assumption that the ball moves at a constant speed, when in actuality, the ball moves with a constant acceleration. Feel free to improve upon this model for your submission for bonus points.

$$ ballTravelTime = \frac{kickLength}{ballSpeed} $$

The cost function should return an real number > 0, based on the inputs provided
"""

def cost(field, distance_function=euclidian_distance, robot_speed=1, ball_speed=4):
  return sum([distance_function(kick.start, kick.end) for kick in field.kicks])

print("Cost before Kick:", cost(myField))
print("Cost after Kick:", cost(myKickedField))

"""Part 4: Define Heuristic

As you know from A* search, the heuristic function causes it to be a large improvement from uninformed search methods like Dijkstra's Algorithm. As you have learned, the heuristic must be both admissable and consistent. 

We want the heuristic function to estimate the time it takes for the ball to enter the net. A naive approach would be to use the distance to the goal and convert it to time. Apply the search to see why this is a poor heuristic
"""

def heuristic(field, distance_function=euclidian_distance, robot_speed=1, ball_speed=4):
  
  return min([distance_function(field.ball, x) / ball_speed for x in field.get_goal()])

print(heuristic(myField))
print(heuristic(myKickedField))

"""## Part 5: Apply A* search"""

import queue
from itertools import count

def compute_strategy(field, get_potential_kicks, distance_function, find_cost, find_heuristic):
    last_explored = field
    explored = {}
    explored[str(field)] = last_explored
    last_explored_val = find_cost(last_explored, distance_function) + find_heuristic(last_explored, distance_function)
    frontier = queue.PriorityQueue()
    unique = count()
    frontier.put((last_explored_val, next(unique), last_explored))
    while(not frontier.empty()):
        if (min([distance_function(last_explored.ball, x) 
                 for x in last_explored.get_goal()]) == 0):
            print("Goal Reached")
            return last_explored.kicks
        for kick in get_potential_kicks(last_explored):
            new_field = last_explored.execute_kick(kick)
            value = find_cost(new_field, distance_function) + find_heuristic(new_field, distance_function)
            if ((str(new_field) not in explored) or \
                (value < cost(explored[str(new_field)], distance_function) + \
                 find_heuristic(explored[str(new_field)], distance_function))):
                  frontier.put((value, next(unique), new_field))
                  explored[str(new_field)] = new_field
        last_explored_cost, _, last_explored = frontier.get()
        #print(last_explored)
    return last_explored.kicks

strategy = compute_strategy(Field(), get_potential_kicks, euclidian_distance, cost, heuristic)

myField = Field()
for k in strategy:
  print(myField)
  myField = myField.execute_kick(k)
print(myField)
