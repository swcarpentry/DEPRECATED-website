for x in grid_interior(GRID_WIDTH):
  for y in grid_interior(GRID_HEIGHT):
    if (density[x-1][y] > density_threshold) or \
       (density[x+1][y] > density_threshold):
      if (flow[x][y-1] > flow_threshold) or\
         (flow[x][y+1] > flow_threshold):
        temp = (density[x-1][y] + density[x+1][y]) / 2
        if abs(temp - density[x][y]) > update_threshold:
          density[x][y] = temp
