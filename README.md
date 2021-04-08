# Random-Walk
A random walk simulator. The user can create a 'drunks' that will walk on a 'map' for a chosen amount of steps. The position and path of these drunks can be plotted.  
There are 4 types of drunks to choose from: four-directions, four-direction-north-biased, any-direction and any-direction-any-length.
- Four-directions - His steps have length 1 and can be in any of the four cardinal directions. The probability of each direction is uniform.
- Four-direction-north-biased - Steps in any of the four cardinal direction with equal probability, but his steps south have length 0.9 and his steps north 1.1, while east and west steps remain with length 1.
- Any-direction - Steps of length 1 but can move in any direction. Uniform distribution.
- Any-direction-any-length - Any length steps and any direction. Uniform distribution.  
The are also 3 different maps: plane, torus and portals.
- Plane - An infinite cartesian plane.
- Torus - We use the non-isomorphic plane representation of the torus as a rectangle. It is a pacman map, where if you go to one of the edges you end up in the opposite edge.
- Portals - An infinite plane that contains portals that teleport the drunks to a different location.
