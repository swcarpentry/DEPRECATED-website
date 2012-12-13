for x in range(1, GRID_WIDTH-1):
  for y in range(1, GRID_HEIGHT-1):
    if (density[x-1][y] > density_threshold) or \
       (density[x+1][y] > density_threshold):
      if (flow[x][y-1] < flow_threshold) or\
         (flow[x][y+1] < flow_threshold):
        temp = (density[x-1][y] + density[x+1][y]) / 2
        if abs(temp - density[x][y]) > update_threshold:
          density[x][y] = temp
