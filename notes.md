# Notes

## Implementing $A^{*}$
### Sacar legal movements

```{py}
    def getPossibleActions(config, walls):
        possible = []
        x, y = config.pos
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int)  > Actions.TOLERANCE):
            return [config.getDirection()]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]: possible.append(dir)

        return possible
```

This method gets called as:

```{py}
return Actions.getPossibleActions( state.getPacmanState().configuration, state.data.layout.walls )
```

#### getLegalNeighbors function
Function for looking into neighboring nodes (cells)
```{py}
    def getLegalNeighbors(position, walls):
        x,y = position
        x_int, y_int = int(x + 0.5), int(y + 0.5)
        neighbors = []
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_x = x_int + dx
            if next_x < 0 or next_x == walls.width: continue
            next_y = y_int + dy
            if next_y < 0 or next_y == walls.height: continue
            if not walls[next_x][next_y]: neighbors.append((next_x, next_y))
        return neighbors
```

#### Take a look at generateSuccessor() [./busters.py 107]
Not really necessary because A\* just gives us our next movement, but does not realize it.

