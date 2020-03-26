# Pacman
Simulation for Pacman game. 

To create enviroment:

```
pip install -r requirements.txt
```


### Usage
```
usage: run.py [-h] [--level N]

Process some integers.

optional arguments:
  -h, --help  show this help message and exit
  --level N   choose the level ['bfs', 'dfs', 'A_star', 'greedy', '0', '1',
              '2', '3', '4', '5']
```

# Algorithms
To check algorithms *BDS*, *DFS*, *A\** and *Greedy*:
```
python run.py --level=bfs
python run.py --level=dfs
python run.py --level=A_star
python run.py --level=greedy
```

To check the *MiniMax* algorithm, you can choose one of the 6 levels [0, 1, 2, 3, 4, 5], for example:
```
python run.py --level=2
```
