# PyGame-Simple-Particle-Flocking-Example
![Alt Text](https://media.giphy.com/media/kiImT3dXTGJgV0fXuN/giphy.gif)
# Install
- Only pygame is needed:```pip install pygame```
# Flocking
- Based on (seperation, alignment, cohesion) principles from https://en.wikipedia.org/wiki/Boids
- Key Control Parameters
  - *max_speed*
  - *neighbour_distance*
  - *desired_seperatation*
  - *desired_neighbours*
  - *seperation_weight*
  - *cohesion_weight*
  - *alignment_weight*
## Seperation
- Move away from neighbours that are too close
## Alignment
- Move towards the average heading of all neighbours
## Cohesion
- Move towards the average position of all neighbours
