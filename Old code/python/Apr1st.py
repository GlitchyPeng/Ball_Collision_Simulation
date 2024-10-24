import itertools

def is_valid(grid):
  """
  Checks if the given grid is valid, i.e., no rectangle has four vertices of the same color.
  """
  for i in range(6):
    for j in range(6):
      for k in range(i + 1, 6):
        for l in range(j + 1, 6):
          if grid[i][j] == grid[i][l] == grid[k][j] == grid[k][l]:
            return False
  return True

def main():
  """
  Tries all possible arrangements of yellow and pink dots in a 4x6 grid and prints a solution if one exists.
  """
  for arrangement in itertools.product(['Y', 'P'], repeat=36):
    grid = [list(arrangement[i:i+6]) for i in range(0, 36, 6)]
    if is_valid(grid):
      print("Solution found:")
      for row in grid:
        print(' '.join(row))
      
  else:
    print("No solution found.")

if __name__ == "__main__":
  main()
