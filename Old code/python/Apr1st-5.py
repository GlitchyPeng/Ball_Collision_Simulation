Last login: Tue Apr  9 13:09:16 on ttys001
(base) stanleypeng@StevendeMacBook-Pro ~ % vim Apr1st-5.py
(base) stanleypeng@StevendeMacBook-Pro ~ % cd coding
(base) stanleypeng@StevendeMacBook-Pro coding % cd python
(base) stanleypeng@StevendeMacBook-Pro python % vim Apr1st-5.py
(base) stanleypeng@StevendeMacBook-Pro python % vim Apr1st-4.py
(base) stanleypeng@StevendeMacBook-Pro python % vim Apr1st.py  

















      for k in range(i + 1, 3):
        for l in range(j + 1, 6):
          if grid[i][j] == grid[i][l] == grid[k][j] == grid[k][l]:
            return False
  return True

def main():
  """
  Tries all possible arrangements of yellow and pink dots in a 4x6 grid and prints a solution if one exists.
  """
  for arrangement in itertools.product(['Y', 'P'], repeat=18):
    grid = [list(arrangement[i:i+6]) for i in range(0, 18, 6)]
    if is_valid(grid):
      print("Solution found:")
      for row in grid:
        print(' '.join(row))
      break
  else:
    print("No solution found.")

if __name__ == "__main__":
  main()


