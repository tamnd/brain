---
title: "CF 102638D - Distributed Computing"
description: "The system is a three dimensional grid of CPUs. A working CPU can send information only in the positive direction of each axis, meaning a CPU can move to its neighbor with one coordinate increased by one. Broken CPUs do not exist in the communication graph."
date: "2026-08-02T14:46:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102638
codeforces_index: "D"
codeforces_contest_name: "Bredor contest"
rating: 0
weight: 102638
solve_time_s: 96
verified: true
draft: false
---

[CF 102638D - Distributed Computing](https://codeforces.com/problemset/problem/102638/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
# Problem Understanding

The system is a three dimensional grid of CPUs. A working CPU can send information only in the positive direction of each axis, meaning a CPU can move to its neighbor with one coordinate increased by one. Broken CPUs do not exist in the communication graph.

A working CPU is called critical when removing only that CPU destroys at least one existing communication relationship between two other CPUs. In other words, there must be some pair of working CPUs where a path existed before the removal, but every possible path used the removed CPU. The task is to count how many CPUs have this property.

The dimensions of the grid can each reach 100, so the total number of cells can reach one million. This rules out trying to run a full graph search after removing every CPU. A single breadth first search over the whole grid is already around one million operations, and repeating it for every cell would be around one trillion operations. The solution has to inspect each CPU only a constant number of times.

The main edge cases come from the fact that a CPU may look like it has several routes around it, but those routes may not exist because of the grid direction or broken CPUs. For example:

```
1 1 3
111
```

The middle CPU is critical. Removing it leaves the first CPU unable to control the third CPU. The correct output is:

```
1
```

A careless solution that only checks whether a CPU has two neighbors might miss this because there is no two dimensional detour.

Another case is:

```
1 2 2
11
11
```

The top right CPU is not critical. There are two possible ways to go from the bottom left CPU to the top right CPU before considering directions, but with the allowed directions the only meaningful question is whether another monotone route exists. The correct output is:

```
0
```

The implementation must respect the directed nature of movement instead of treating the grid as an undirected graph.

# Approaches

A direct approach would remove every working CPU one at a time and run a reachability search to find whether any communication pair disappeared. This is correct because it exactly simulates the definition of a critical CPU. However, in the largest grid there are one million CPUs. Running a search over one million nodes for each of them gives about $10^{12}$ work, which is far beyond the limit.

The key observation is that every path entering a CPU must come through one of its three possible predecessors, and every path leaving it must go through one of its three possible successors. If a CPU is critical, there must be some predecessor and successor pair where all paths between them pass through the CPU.

The distance between such a predecessor and successor is extremely small. A predecessor is one step behind the CPU and a successor is one step ahead of it. If they are on the same axis, the CPU is the only possible middle cell. If they use different axes, there is exactly one possible alternative middle cell, the corner of the small two by two by one rectangle. Checking whether that corner exists is enough.

This reduces the whole problem to checking at most nine local configurations per CPU.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nmk · nmk) | O(nmk) | Too slow |
| Optimal | O(nmk) | O(nmk) | Accepted |

# Algorithm Walkthrough

1. Store the grid of working and broken CPUs. For every working CPU, only its six neighboring positions matter because communication can enter and leave through these adjacent cells.
2. For each working CPU, collect the directions of working predecessors and working successors. A predecessor has the form one step in the negative direction of an axis, and a successor has the form one step in the positive direction.
3. Try every predecessor and successor pair. If both use the same axis, the predecessor can only reach the successor through the current CPU, so the CPU is critical.
4. If the predecessor and successor use different axes, calculate the only possible detour cell. If that cell is broken or outside the grid, the current CPU is critical. Otherwise, the detour provides another path and this pair does not prove criticality.
5. Count the CPU if at least one predecessor and successor pair proves that every path between them uses the CPU.

The reason this works is that a path entering and leaving a single CPU has a local structure. Any communication path that uses the CPU must enter from one adjacent predecessor and leave to one adjacent successor. The only possible bypass would have to fit inside the smallest rectangle connecting those two cells, and that rectangle has at most one other middle cell. Checking that cell covers every possible alternative path.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    grid = []
    for i in range(n):
        while True:
            line = input().strip()
            if line:
                break
        grid.append([list(line)])
        for _ in range(m - 1):
            grid[i].append(list(input().strip()))

    def inside(x, y, z):
        return 0 <= x < n and 0 <= y < m and 0 <= z < k

    ans = 0

    dirs = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

    for x in range(n):
        for y in range(m):
            for z in range(k):
                if grid[x][y][z] != '1':
                    continue

                prevs = []
                nexts = []

                for idx, (dx, dy, dz) in enumerate(dirs):
                    px, py, pz = x - dx, y - dy, z - dz
                    nx, ny, nz = x + dx, y + dy, z + dz

                    if inside(px, py, pz) and grid[px][py][pz] == '1':
                        prevs.append(idx)
                    if inside(nx, ny, nz) and grid[nx][ny][nz] == '1':
                        nexts.append(idx)

                critical = False

                for a in prevs:
                    if critical:
                        break
                    for b in nexts:
                        if a == b:
                            critical = True
                            break

                        dx1, dy1, dz1 = dirs[b]
                        dx2, dy2, dz2 = dirs[a]

                        cx = x - dx2 + dx1
                        cy = y - dy2 + dy1
                        cz = z - dz2 + dz1

                        if not inside(cx, cy, cz) or grid[cx][cy][cz] == '0':
                            critical = True
                            break

                if critical:
                    ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The input parser skips the empty lines separating layers. The grid is stored directly so every neighbor lookup is constant time.

For each cell, `prevs` and `nexts` contain only the working neighbors that can participate in a communication path through the cell. There are never more than three of each, so the nested check performs at most nine iterations.

The detour calculation is the subtle part. Suppose the predecessor direction is the x axis and the successor direction is the y axis. The only alternative route must move in y first and then x, so it passes through the opposite corner. The formula computes exactly that corner. There is no need for a search because the coordinate difference between the predecessor and successor is only two unit moves.

# Worked Examples

For the full three by three by three cube, consider a middle CPU.

| Current CPU | Predecessor direction | Successor direction | Alternative cell | Result |
| --- | --- | --- | --- | --- |
| (2,2,2) | x | x | none | Critical |
| (2,2,2) | x | y | (2,1,2) | Not enough to prove critical |

The CPU has pairs on the same axis, such as the CPU before it and the CPU after it along the x direction. Removing it blocks that straight communication path. Repeating this reasoning marks every non corner CPU as critical.

For a line of three CPUs:

```
1 1 1
```

the trace is:

| Current CPU | Predecessors | Successors | Decision |
| --- | --- | --- | --- |
| First | none | middle | Not critical |
| Middle | first | last | Critical |
| Last | middle | none | Not critical |

The example shows why endpoints cannot be counted. A critical CPU needs both a source side and a destination side that lose communication.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nmk) | Every CPU checks a constant number of neighbors and pairs. |
| Space | O(nmk) | The grid itself is stored. |

The largest possible grid contains one million cells. The algorithm performs only a small fixed amount of work per cell, so it fits the intended limits.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().splitlines()
    sys.stdin = old

    it = iter(data)
    n, m, k = map(int, next(it).split())
    grid = []
    for _ in range(n):
        while True:
            s = next(it)
            if s:
                break
        grid.append([list(s)])
        for _ in range(m - 1):
            grid[-1].append(list(next(it)))

    def inside(x, y, z):
        return 0 <= x < n and 0 <= y < m and 0 <= z < k

    dirs = [(1,0,0),(0,1,0),(0,0,1)]
    ans = 0

    for x in range(n):
        for y in range(m):
            for z in range(k):
                if grid[x][y][z] != '1':
                    continue
                p = []
                q = []
                for i, (dx,dy,dz) in enumerate(dirs):
                    if inside(x-dx,y-dy,z-dz) and grid[x-dx][y-dy][z-dz]=='1':
                        p.append(i)
                    if inside(x+dx,y+dy,z+dz) and grid[x+dx][y+dy][z+dz]=='1':
                        q.append(i)
                ok = False
                for a in p:
                    for b in q:
                        if a == b:
                            ok = True
                        else:
                            dx1,dy1,dz1 = dirs[b]
                            dx2,dy2,dz2 = dirs[a]
                            cx,cy,cz = x-dx2+dx1, y-dy2+dy1, z-dz2+dz1
                            if not inside(cx,cy,cz) or grid[cx][cy][cz]=='0':
                                ok = True
                        if ok:
                            break
                    if ok:
                        break
                ans += ok
    return str(ans) + "\n"

assert run("""1 1 3
111
""") == "1\n", "line middle"

assert run("""3 3 3
111
111
111
111
111
111
111
111
111
""") == "19\n", "full cube"

assert run("""1 1 10
0101010101
""") == "0\n", "isolated CPUs"

assert run("""1 1 1
1
""") == "0\n", "single CPU"

assert run("""1 2 2
11
11
""") == "0\n", "small square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three CPUs in a line | 1 | Middle cell separator detection |
| Full 3D cube | 19 | Dense grid behavior |
| Alternating working cells | 0 | No communication paths |
| One CPU | 0 | Minimum size boundary |
| Two by two layer | 0 | Detour handling |

# Edge Cases

For a straight line:

```
1 1 3
111
```

the middle CPU has one predecessor and one successor on the same axis. The algorithm sees that there is no possible detour cell and counts it.

For a single isolated working CPU:

```
1 1 1
1
```

there are no predecessors or successors. Since no communication relationship can be broken, the algorithm leaves the answer unchanged.

For alternating cells:

```
1 1 10
0101010101
```

every working CPU lacks the required neighboring pair. The algorithm never finds a predecessor and successor combination, so the output remains zero.

For a dense cube, every internal CPU has at least one straight predecessor successor pair. The algorithm does not need to inspect the whole graph, because the local straight path is already enough to prove criticality.
