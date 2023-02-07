# Ludobots 
How to reproduce my results
```
python3 search.py
```

The robot is designed to look like a puppy climbing up the stairs. 

The robot is trained to climb up as many stairs as possible. The fitness function returns the final y position of the robot, 
so the final version of the robot would have traveled the farthest in the y-direction.

Compared to the quadruped, this puppy robot has motor neurons that generate more force (max=200) so that the robot can generate 
more "bounce" to go up the stairs.

The head, ears, and tail have no mass so that they don't affect the balance of the robot.

8 different robots evolve over 8 generations, and the best performing robot becomes the final robot.

