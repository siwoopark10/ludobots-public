# Ludobots
## Teaser:


## Video: https://youtu.be/JifEDfGnvVI

### Credits
My work projects for the evolutionary robotics project - Ludobots, based completely in the subreddit [r/ludobots](https://www.reddit.com/r/ludobots/).  
Final Project for CS 396/496 Aritificial Life.

### How to reproduce my work
```
python3 search.py
```
This python script creates a parallel hill climber that evolves a robot that moves forward the fastest. After a series of evolutions, the results, including fitness curves, successful mutations, and best fitness of each parallel hill climber, are saved in the `results` directory.

Currently, this script creates 10 parallel hill climbers with 10 random seeds. Each parallel hill climber has a population size of 10 and simulates each population over 500 generations. Thus, 500 * 10 * 10 = 50,000 simulations.  
You can change the number of hill climbers being created in `search.py`.  
You can edit the population size and number of generations in `constants.py`.  

## The World
<img src="https://user-images.githubusercontent.com/57846202/225165716-6da3286e-5193-43b4-b67a-e6408ffa9182.jpg" width="350" height="280">  
The arena/world is an open field that expands in the x, y, and z direction. Our robot is placed in the middle of the world.  


A force of **gravity** pulls down every object to ground level. Our robot cannot go underground (z < 0).  

There is **friction** between our robot and the ground, which allows our robot to move around the world.  
 
 ## The Body
 
**Genotype: directed graph**  

<img src="https://user-images.githubusercontent.com/57846202/225164698-658bf49e-4fd1-4139-af99-d7f754fbb68d.jpg" width="400" height="300">

We first start with a torso link. This link is connected to another torso link, which starts off a body segment. A body segment consists of
- a torso link
- two arms
- two legs

The left and right side are symmetrical to each other. So if one side has an arm, the other side is guaranteed to have an arm of the same size.
66.6 percent of the time a body segment will have two arms. Half of those body segments with arms will have two legs (33.3 percent).

**Torso** links are connected along the y-axis, and each of them has a random dimension of range [(0,1), (0,1), (0,0.3)]. This would most likely create a flatter rectangle, preventing the body of our robot from being too fat vertically.

Both **arms** and **legs** have a random of range [(0,1), (0,1), (0,0.5)]. The range of the z dimension is greater than that of a torso link in order to allow our robot to have longer limbs, which is what we usually observe in the natural world.

**Phenotype: 3D model**  


A phenotype of a body segment would look like this 3D model:  
<img src="https://user-images.githubusercontent.com/57846202/225169438-4515add6-b9a5-4384-b601-318cb222df9a.jpg" width="350" height="300">  

Each body segment looks like either one of these three 3D models:

- no limbs, two arms, two legs

<img src="https://user-images.githubusercontent.com/57846202/222006572-d1383b73-2d17-4bed-a20a-2919b30460ee.jpg" width="150" height="100"><img src="https://user-images.githubusercontent.com/57846202/222006598-41cce254-ad5f-4738-9d81-d444180a572a.jpg" height="100" width="150"><img src="https://user-images.githubusercontent.com/57846202/222006614-9c600284-d660-4c38-a0f8-e3282f237cf5.jpg" height="100" width="120">

### Links and Joints Positioning

A link is connected to another links through joints. Each torso link is connected in the y-direction with the joint being placed in the middle of the intersection of the two faces.

<img src="https://user-images.githubusercontent.com/57846202/221871750-2e387886-0d08-4ac6-8da5-c2dcba6fb66e.jpg" width="180" height="160">

The links for the body segment (torso, arms, legs) are connected in a slightly more complex manner.

<img src="https://user-images.githubusercontent.com/57846202/225164699-caa43187-d24f-4893-b78a-bcf8555026c8.jpg" width="600" height="250">

One thing to note is that all joints rotate around the x axis in order to promote movement along the y-axis.

## The Brain

The Brain consists of:
- Motor Neurons
- Sensor Neurons
- Synapses

<img src="https://user-images.githubusercontent.com/57846202/225164695-257be63e-e99d-4e90-af9e-6a51fe5eebb0.jpg" width="350" height="250">

For every joint that exists in our robot, there is a **motor neuron** that facilitates the movement of those joints.  
Each joint in the diagram above is assigned a motor neuron.

**Sensor neurons** randomly placed in torso links and limb links. The probability that a torso link has a sensor is 50%, where as it is 70% for the arms and legs. The links with sensors are indicated with the color "Green" in the simulation, and the rest of them are "Cyan" (blue in the diagram above).

<img src="https://user-images.githubusercontent.com/57846202/225164697-265a5613-8788-4487-bf65-983d8eee2668.jpg" width="450" height="250">

**Synapses** determine the relationship between the motor neurons and the sensor neurons. Whenever a link with a sensor neuron senses a touch (in our simulation, contact with the ground), a message is sent to all the motor neurons. The **weight** of the synapse determine how much each motor neuron reacts to the message, which influences how much the joint rotates. The weights are randomly assigned at the beginning of the simulation.

This diagram is a 3D model of how synapses work with motor neuron and sensor neurons.

<img src='https://user-images.githubusercontent.com/57846202/222050989-49951c4a-82ff-4013-b4a5-7b8f50aed337.jpg' width="200" height="160">

## Code

All of the code for a single run of simulation is done in `solutions.py`. The world is created by `Create_World`. The main body of the robot is built through `Create_Body` and the neurons are set in `Create_Brain`. I created an helper function `_Create_Limbs` to help me loop through to create the arms and legs. `Initialize_fields` initializes the sizes of all the torso and limb links as well as the weights of each synapse.


## Evolution
The creature evolves through mutations which can be divided into 4 main types (2 body and 2 brain): Generating or deleting limbs, changing the size of the links, changing synapse weight, and changing sensor placement

- Changing synapse weight

<img src="https://user-images.githubusercontent.com/57846202/222008211-3cdeb1a3-836c-468a-8366-2a226a23ba44.jpg" width="260" height="180">

Since we know the dimentions of `self.weights`, we can replace one of the values to a random value between -1 and 1.

- Generating or deleting links (either torso or limbs)

<img src="https://user-images.githubusercontent.com/57846202/222008184-7e966f82-7fcd-4549-94b5-dbdc06f36d9e.jpg" width="300" height="160">

- Changing the size of the links (either torso or limbs)

<img src="https://user-images.githubusercontent.com/57846202/222009293-b4aa71e0-83f1-4b6d-bec4-6acf0a0c9f8b.jpg" width="300" height="160">

- Changing sensor placement (either torso and limbs)

<img src="https://user-images.githubusercontent.com/57846202/222009114-b903d26b-88e6-4865-a3ac-25a8d1db6f64.jpg" width="220" height="180">

In each evolution, one of these 7 mutations happen. 

### Fitness function
The robot in this assignment is trying to optimize for how far it can crawl in the *positive y-direction*. Thus, the fitness function prefers creatures that end up with the greatest y-position by the time the simulation terminates.

### Parallel Hill Climber
Parallel Hill Climber allows us to simulatenously train and evolve different robots so that I can start off on various starting points. Each robot in the population evolves over several generations. The population size and the number of generations can be modified in the `constants.py` file. The main functionality of this method is to create a **child** robot from a copy of a **parent** robot, and to generate *mutations* in the child robot to see if it outperforms the parent. If the child robot performs better (*better fitness*), we overwrite the parent robot with the child and continue to evolve and mutate until we reach the maximum number of generations. Thus, the fitness of each robot should monotonously increase over time.



## Results

The results of the simulations are all stored in the `results` directory. 
This is a fitness curve for the best fitness among all the populations for each PHC across 500 generations.
![PHC Fitness Curves](https://github.com/siwoopark10/ludobots-public/blob/main/results/phc_fitness_curve.png)

I kept track of all the mutations that led to an improved fitness for each PHC. The graphs looked similar across all random seeds.
![Mutation](https://github.com/siwoopark10/ludobots-public/blob/main/results/seed_6/mutation_count.png)
![Mutation](https://github.com/siwoopark10/ludobots-public/blob/main/results/seed_8/mutation_count.png)

Synapse weight and link size mutations were always the top two leading mutations, and the other mutations had similar counts when considering the other mutation graphs in different seeds.

Let's look deeper into the population with the highest fitness. 
![Seed 8 Fitness Curve](https://github.com/siwoopark10/ludobots-public/blob/main/results/seed_8/fitness_curve_per_population_8.png)

We can see that Population 1 of seed 8 had an impressive fitness of over 7.
Generation 1  
![ezgif com-video-to-gif (1)](https://user-images.githubusercontent.com/57846202/225186015-6d79af7c-0270-4c8e-bf2f-8de6c884db56.gif)

Generation 100  
![ezgif com-video-to-gif (2)](https://user-images.githubusercontent.com/57846202/225186139-97b58564-c74b-433b-89b7-cb77997a78e7.gif)

Generation 500  
![ezgif com-video-to-gif](https://user-images.githubusercontent.com/57846202/225185780-1000afc3-3e13-48ac-a714-41e4d59c72bd.gif)








