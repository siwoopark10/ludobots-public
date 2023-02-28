# Ludobots
How to reproduce my results
```
python3 search.py
```

The creature has a spine like the one used in assignment 6, but now it has arms and leg that 

Generates a kinematic chain (a jointed, motorized, innervated, sensorized snake) with a:

 - random number (between 4 and 10) of

 - randomly shaped links (cube dimensions range from 0 to 1) with

 - random sensor placement along the chain.
 
 - Links with and without sensors are colored green and blue, respectively.
 
 ## Structure
 The vertabrae extend in the y-direction, and each vertabrae link has a random dimension [(0,1), (0,1), (0,0.3)]. The height was intentially set to a lower value to provide more balance to the creature. The number of links in the vertabrae is randomly chosen between 3 and 8. 
 
<img src="https://user-images.githubusercontent.com/57846202/221871750-2e387886-0d08-4ac6-8da5-c2dcba6fb66e.jpg" width="120" height="120">

We initially start with an absolute positioning for a link and a joint

<img src="https://user-images.githubusercontent.com/57846202/221871752-9a090dc3-1ef1-4df4-b7b0-961435029ed9.jpg" width="150" height="120">
<img src="https://user-images.githubusercontent.com/57846202/221871753-2f06334f-32a0-480f-af71-15362c753944.jpg" width="150" height="120">

The next joint points to the center of the link's bottom right edge. This can be calculated by adding 1/2 of the link's y-size, subtracting 1/2 of z-size, and adding 1/2 of x-size. The center position of the next link (the arm) is going to be on the same z as the joint but to the right by 1/2 of its x-size.

<img src="https://user-images.githubusercontent.com/57846202/221871755-d47436d7-7b62-4e6f-bf5a-f7296d4a053a.jpg" width="150" height="120">
<img src="https://user-images.githubusercontent.com/57846202/221871758-0727fe8d-80be-41f7-88a7-c8df092b6223.jpg" width="160" height="100">

The next joint which is relative to the previous joint is located at the center of the bottom surface. The position of the next link (leg) is 1/2 of its z-size down, but the same x and y. Now we have created a connected arm and leg.

The left size is basically the same as the right size but the x-values are filpped.

The main body of the robot is built through **Create_Body** and the neurons are set in **Create_Brain**.
I created an helper function **Create_Limbs** to help me loop through to create the arms and legs. 
One shoftcut I took was to keep the size of the arms and legs smaller than the main vertebrae link so that there aren't any unpleasing overlaps between the limbs. The joint axes were also determined carefully to allow forward and backward movement for the robot creature.

Before each simulation is run, I intitialize the necessary weights, such as synapse weights, random size of links, and the positioning of sensor neurons.

## Evolution
The creature evolves through mutations which can be divided into 4 main types:
- Generating or deleting limbs
- Changing synapse weight
- Changing sensor placement
- Changing the size of the links

In each evolution, any of these 4 mutations could happen. 

### Parallel Hill Climber
Parallel Hill Climber allows us to simulatenously train and evolve different robots so that I can start off on various starting points. Each robot in the population evolves over several generations. The population size and the number of generations can be modified in the `constants.py` file. The main loop of this method is to create a child robot from a copy of a parent robot, and to generate mutations in the child robot to see if it outperforms the parent with the modifications. If the child robot performs better, we overwrite the parent robot with the child and continue to evolve and mutate until we reach the maximum number of generations.

### Fitness function
The robot in this assignment is trying to optimize for how far it can crawl in the positive y-direction. Thus, the fitness function prefers creatures that end up with the greatest y-position by the time simulation terminates.
