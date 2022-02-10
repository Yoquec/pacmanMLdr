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

#### Take a look at generateSuccessor() [./busters.py 107]
Not really necessary because A* just gives us our next movement, but does not realize it.

