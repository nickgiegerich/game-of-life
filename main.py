import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

st.write(""" # Conway's Game of Life

The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970.[1] 
It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by
creating an initial configuration and observing how it evolves. It is Turing complete and can simulate a universal constructor or any other Turing machine.

<https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life>

### rules: 
- Any live cell with two or three live neighbours survives.
- Any dead cell with three live neighbours becomes a live cell.
- All other live cells die in the next generation. Similarly, all other dead cells stay dead.
""")

N = 100
frame = 100

ON = 255
OFF = 0
vals = [ON, OFF]

# INPUTS 
input_grid = st.number_input('Enter a grid size', min_value=8, max_value=None, value=100, step=5)  # grid size
frame_input = st.number_input('Change amount of frames', min_value=100, max_value=None, step=50)  # frames

if input_grid:
    N = input_grid
    
if frame_input:
    frame = frame_input

def randomGrid(N):
    """ returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N,N)


def update_grid(img, grid, N):

    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):

            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            
            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img

def animate(i):  # update the y values (every 1000ms)
    update_grid(img, grid, N)
    the_plot.pyplot(plt)


grid = randomGrid(N)
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest')
the_plot = st.pyplot(plt)

for i in range(frame):
    animate(i)
    # time.sleep(0.001)