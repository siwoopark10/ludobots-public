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
 The torso extend in the y-direction, and each torso link has a random dimension [(0,1), (0,1), (0,0.3)]. The height was intentially set to a lower value to provide more balance to the creature. The number of links in the torso is randomly chosen between 3 and 8. For simiplicity sake, the sizes of every link will be [1,1,1] even though I limited the z-size of the torso to be 0.3 and that of the limbs to be 0.5.
 
<img src="https://user-images.githubusercontent.com/57846202/221871750-2e387886-0d08-4ac6-8da5-c2dcba6fb66e.jpg" width="120" height="120">


The main body of the robot is built through **Create_Body** and the neurons are set in **Create_Brain**.
I created an helper function **Create_Limbs** to help me loop through to create the arms and legs.

Each torso link has:
- no limbs
<img src="https://user-images.githubusercontent.com/57846202/222006572-d1383b73-2d17-4bed-a20a-2919b30460ee.jpg" width="150" height="100">

- two arms

<img src="https://user-images.githubusercontent.com/57846202/222006598-41cce254-ad5f-4738-9d81-d444180a572a.jpg" height="100" width="120">


- or two arms and legs

<img src="https://user-images.githubusercontent.com/57846202/222006614-9c600284-d660-4c38-a0f8-e3282f237cf5.jpg" height="100" width="120">

### Links and Joints Positioning

We initially start with an absolute positioning for a link and a joint. The joint is placed on the center of the surface facing the positive y-direction.

<img src="https://user-images.githubusercontent.com/57846202/221871752-9a090dc3-1ef1-4df4-b7b0-961435029ed9.jpg" width="150" height="120">

The next joint points to the center of the link's bottom right edge. This can be calculated by adding 1/2 of the link's y-size, subtracting 1/2 of z-size, and adding 1/2 of x-size. The center position of the next link (the arm) is going to be on the same z as the joint but to the right by 1/2 of its x-size.

<img src="https://user-images.githubusercontent.com/57846202/221871755-d47436d7-7b62-4e6f-bf5a-f7296d4a053a.jpg" width="150" height="120">
<img src="https://user-images.githubusercontent.com/57846202/221871758-0727fe8d-80be-41f7-88a7-c8df092b6223.jpg" width="160" height="100">

The next joint which is relative to the previous joint is located at the center of the bottom surface. The position of the next link (leg) is 1/2 of its z-size down, but the same x and y. Now we have created a connected arm and leg.

<img src="https://user-images.githubusercontent.com/57846202/222007345-e31886f0-cc9a-4584-8fad-bb762c19cd50.jpg" width="150" height="140">


The left size is basically the same as the right size but the x-values are filpped.

<img src="https://user-images.githubusercontent.com/57846202/222007372-c08244d4-6723-414d-b9a5-47d11385f055.jpg" width="150" height="200">

One shoftcut I took was to keep the size of the arms and legs smaller than the torso link so that there aren't any unpleasing overlaps between the limbs. The joint axes were also determined carefully to allow forward and backward movement for the robot creature. (jointAxis = "1 0 0")

### Initializing fields

Before each simulation is run, I intitialize the necessary weights, such as synapse weights, random size of links, and the positioning of sensor links.

**Sensor Links**: Sensor links are represented with the color green and each link has a 70 percent probability that it will be a sensor link.

**Synapse Weights**: A synapse is send from a sensor link to every motor joint.
Rows = Number of sensors
Columns = Number of joints (every joint is a motor joint)
Each synapse weight is randomly sampled between -1 and 1.

**Link Sizes**: I randomly determined the number of torso links to be a number between 4 and 10. I can create a list of random sizes that correspond to each link size. Whenever I loop through each index of the torso, I randomly generate a number between 0 and 3.
0 -> No limbs
1 -> Two Arms
2,3 -> Two Arms and Legs
The left and right are symmetrical, so I generate one size for two limbs. I increaesed the probability of generating more limbs to give the robot more mobility. The sizes of the limbs are stored in a list of lists.

## Evolution
The creature evolves through mutations which can be divided into 4 main types (2 body and 2 brain):
- Generating or deleting limbs

<img src="https://user-images.githubusercontent.com/57846202/222008184-7e966f82-7fcd-4549-94b5-dbdc06f36d9e.jpg" width="160" height="100">

- Changing the size of the links

<img src="https://user-images.githubusercontent.com/57846202/222009293-b4aa71e0-83f1-4b6d-bec4-6acf0a0c9f8b.jpg" width="160" height="100">

- Changing synapse weight

<img src="https://user-images.githubusercontent.com/57846202/222008211-3cdeb1a3-836c-468a-8366-2a226a23ba44.jpg" width="160" height="100">


- Changing sensor placement

<img src="https://user-images.githubusercontent.com/57846202/222009114-b903d26b-88e6-4865-a3ac-25a8d1db6f64.jpg" width="160" height="100">


In each evolution, any of these 4 mutations could happen. 

### Parallel Hill Climber
Parallel Hill Climber allows us to simulatenously train and evolve different robots so that I can start off on various starting points. Each robot in the population evolves over several generations. The population size and the number of generations can be modified in the `constants.py` file. The main functionality of this method is to create a child robot from a copy of a parent robot, and to generate mutations in the child robot to see if it outperforms the parent. If the child robot performs better, we overwrite the parent robot with the child and continue to evolve and mutate until we reach the maximum number of generations.

### Fitness function
The robot in this assignment is trying to optimize for how far it can crawl in the positive y-direction. Thus, the fitness function prefers creatures that end up with the greatest y-position by the time the simulation terminates.

### Fitness Curves
The fitness improvement for population size = 5 and number of generations = 25 with 5 random seeds.
<img src="https://user-images.githubusercontent.com/57846202/222009906-44811364-cbbf-44a0-8992-bbeb3d189397.png" width="160" height="120">

