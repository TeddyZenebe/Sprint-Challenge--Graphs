from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']

def backtrack_path(graph, player):
    # Create an empty queue
    q = Queue()
 
    # Add a PATH TO the starting vertex_id to the queue
    q.enqueue( [(player.current_room.id, None)] )
    #Create an empty set
    visited = set()
    # While the queue is not empty
    while q.size() > 0:
        #Dequeue the first path
        path = q.dequeue()
        # grab the last vertex from the path
        v = path[-1][0]
        # check if it's the target
        if '?' in graph[v].values():
            # if so, return the path
            return [i[1] for i in path[1:]]
        if v not in visited:
            visited.add(v)
            for key, val in graph[v].items():
                # make a copy of the path before adding
                path_copy = path.copy()
                # print(f"Path copy: {path_copy}")
                path_copy.append((val, key))
                q.enqueue(path_copy)
traversal_path = []
opposites = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
previous_room = [None]
room_queue = {}#{0:[n,e,s]
visited = {}#{0:0}
#function that append all possible exit direction for each room 
def check_direction(roomId):
    directions = []
    if 'n' in room_graph[roomId][1].keys():
        directions.append('n')
    if 'e' in room_graph[roomId][1].keys():
        directions.append('e')
    if 's' in room_graph[roomId][1].keys():
        directions.append('s')
    if 'w' in room_graph[roomId][1].keys():
        directions.append('w')
    return directions
#check the number of rooms visited and loop until they equal to the available rooms (or all visited)
while len(visited) < len(room_graph):
    room_id = player.current_room.id
    if room_id not in room_queue:
        visited[room_id] = room_id #{0:0}
        room_queue[room_id] = check_direction(room_id)
    
    if len(room_queue[room_id]) < 1:
        previous_direction = previous_room.pop()
        traversal_path.append(previous_direction)
        player.travel(previous_direction)
    #check the path is avalilabe 
    #assign the next path/direction and the room
    else:
        next_direction = room_queue[room_id].pop(0)#n
        traversal_path.append(next_direction)#[n]
        previous_room.append(opposites[next_direction])#
        player.travel(next_direction)
# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
