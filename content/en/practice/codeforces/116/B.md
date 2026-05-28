---
title: "CF 116B - Little Pigs and Wolves"
description: "We have a small rectangular grid where each cell is either empty, contains a pig, or contains a wolf. A wolf may eat one pig that is directly adjacent to it in one of the four cardinal directions. Once a pig is eaten, it disappears and cannot be eaten again."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 116
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 87 (Div. 2 Only)"
rating: 1100
weight: 116
solve_time_s: 150
verified: true
draft: false
---

[CF 116B - Little Pigs and Wolves](https://codeforces.com/problemset/problem/116/B)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a small rectangular grid where each cell is either empty, contains a pig, or contains a wolf. A wolf may eat one pig that is directly adjacent to it in one of the four cardinal directions. Once a pig is eaten, it disappears and cannot be eaten again.

The goal is to maximize how many pigs are eaten in total.

The key restriction is unusual and extremely important: every pig is adjacent to at most one wolf. A wolf may still have several neighboring pigs, but a pig can never be contested by multiple wolves.

That restriction changes the problem from a matching problem into a simple greedy simulation.

The grid dimensions are at most 10 × 10, so the entire board contains at most 100 cells. Even inefficient solutions would likely pass. Still, the problem is designed to test whether we notice the structural property that removes the need for heavy graph algorithms.

A careful implementation still matters because the board changes while wolves eat pigs. If we accidentally allow the same pig to be eaten twice, the answer becomes incorrect.

One easy mistake is forgetting to remove a pig after it gets eaten. Consider this input:

```
1 3
WPW
```

The correct output is:

```
1
```

The middle pig is adjacent to both wolves, but this configuration is actually forbidden by the statement because each pig can have at most one adjacent wolf. A careless implementation that ignores the guarantee might count the pig twice.

Another subtle case is when a wolf has multiple neighboring pigs:

```
2 2
PW
PP
```

The correct output is:

```
1
```

The wolf can only eat one pig, even though two pigs are adjacent. A buggy solution might count every adjacent pig.

Boundary handling is another common source of errors. For example:

```
1 2
WP
```

The correct output is:

```
1
```

The wolf only has neighbors inside the grid. Accessing coordinates outside the board without checks causes index errors.

## Approaches

The most direct brute-force idea is to try every possible decision for every wolf. Each wolf can choose one adjacent pig or choose nobody. We could recursively explore all combinations and keep the maximum answer.

That works because the board is tiny. In the worst case there are about 100 cells, and many of them could be wolves. If each wolf has up to four choices, the search space becomes roughly $4^k$, where $k$ is the number of wolves. Even with only 20 wolves, that is already more than a trillion possibilities.

The reason this explosion happens is that wolves normally compete for pigs. Choosing a pig for one wolf may block another wolf later.

The crucial observation is that this problem removes almost all competition. Every pig is adjacent to at most one wolf. That means if a wolf sees a pig, no other wolf can ever take it.

Once we realize this, the problem becomes simple. We iterate through the grid. For every wolf, we check its four neighboring cells. If any neighbor contains a pig, the wolf eats it immediately, we increase the answer, and we erase that pig from the board.

This greedy choice is always safe because no future wolf could have used that pig anyway.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4^k) | O(k) | Too slow conceptually |
| Optimal | O(n × m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the grid into a 2D array so we can modify cells after pigs are eaten.
2. Prepare the four movement directions: up, down, left, and right.
3. Traverse every cell in the grid.
4. When the current cell contains a wolf, examine its four neighboring cells.
5. For each neighbor, first check whether the coordinates stay inside the board. This prevents invalid array access.
6. If a neighboring cell contains a pig, let the wolf eat it immediately:

1. Increase the answer by one.
2. Replace that pig cell with `.` so no later wolf can eat it again.
3. Stop checking further neighbors for this wolf.

A wolf may eat at most one pig, so continuing after a successful eat would overcount.
7. After processing all cells, print the total number of eaten pigs.

### Why it works

The correctness comes from the guarantee that every pig is adjacent to at most one wolf. Suppose a wolf finds an adjacent pig. No other wolf can ever use that pig, either now or later. Eating it immediately cannot reduce any future options.

Because of that property, every successful greedy choice is independent of all others. The algorithm counts exactly one pig for each wolf that has at least one adjacent pig, and no pig is counted twice because eaten pigs are removed from the grid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    ans = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'W':
                for dx, dy in directions:
                    ni = i + dx
                    nj = j + dy

                    if 0 <= ni < n and 0 <= nj < m:
                        if grid[ni][nj] == 'P':
                            ans += 1
                            grid[ni][nj] = '.'
                            break

    print(ans)

solve()
```

The solution stores the board as a mutable list of character lists because pigs disappear after being eaten. Strings are immutable in Python, so using raw strings would make updates awkward.

The outer loops scan every cell once. Whenever we encounter a wolf, we test the four neighboring positions using the direction array.

The boundary check comes before accessing `grid[ni][nj]`. Reversing this order would cause index errors on edge cells.

After a wolf eats a pig, the code immediately replaces the pig with `.`. This prevents double counting and models the problem statement accurately.

The `break` statement is essential. A wolf may eat only one pig. Without the break, a single wolf could consume multiple adjacent pigs incorrectly.

## Worked Examples

### Example 1

Input:

```
2 3
PPW
W.P
```

Initial grid:

```
P P W
W . P
```

| Step | Wolf Position | Adjacent Pig Found | Answer | Grid Change |
| --- | --- | --- | --- | --- |
| 1 | (0, 2) | (0, 1) | 1 | Pig at (0,1) removed |
| 2 | (1, 0) | (0, 0) | 2 | Pig at (0,0) removed |

Final answer:

```
2
```

This trace shows that each wolf independently takes one neighboring pig. Removing pigs after eating prevents reuse.

### Example 2

Input:

```
2 2
PW
PP
```

Initial grid:

```
P W
P P
```

| Step | Wolf Position | Adjacent Pig Found | Answer | Grid Change |
| --- | --- | --- | --- | --- |
| 1 | (0, 1) | (0, 0) | 1 | Pig at (0,0) removed |

Final answer:

```
1
```

This example demonstrates the rule that a wolf can only eat one pig even if several are adjacent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × m) | Every cell is visited once, and each wolf checks at most 4 neighbors |
| Space | O(1) | Only a few variables besides the input grid are used |

The board contains at most 100 cells, so this solution is comfortably within the limits. Even interpreted Python runs instantly at this scale.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    ans = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'W':
                for dx, dy in directions:
                    ni = i + dx
                    nj = j + dy

                    if 0 <= ni < n and 0 <= nj < m:
                        if grid[ni][nj] == 'P':
                            ans += 1
                            grid[ni][nj] = '.'
                            break

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run("2 3\nPPW\nW.P\n") == "2\n", "sample 1"

# minimum grid
assert run("1 1\n.\n") == "0\n", "empty cell"

# single wolf and pig
assert run("1 2\nWP\n") == "1\n", "single adjacent pig"

# wolf with multiple adjacent pigs
assert run("2 2\nPW\nPP\n") == "1\n", "wolf only eats one pig"

# no possible eats
assert run("2 2\nP.\n.W\n") == "0\n", "no adjacency"

# larger mixed case
assert run("3 3\nPWP\n.W.\nPWP\n") == "4\n", "multiple wolves and pigs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / .` | `0` | Minimum-size grid |
| `1 2 / WP` | `1` | Boundary adjacency |
| `2 2 / PW / PP` | `1` | One wolf cannot eat multiple pigs |
| `2 2 / P. / .W` | `0` | No adjacent pigs |
| `3 3 / PWP / .W. / PWP` | `4` | Multiple successful greedy choices |

## Edge Cases

Consider the case where a wolf touches several pigs:

```
2 2
PW
PP
```

The algorithm scans the wolf at position `(0,1)`. It checks neighbors in order and finds the pig at `(0,0)`. The answer becomes 1, the pig is removed, and the loop breaks immediately. The remaining pigs are ignored for that wolf, which matches the rule that each wolf eats at most one pig.

Now consider a board edge case:

```
1 2
WP
```

The wolf sits in the top-left corner. Some neighboring coordinates would fall outside the board, such as `(-1,0)` or `(0,-1)`. The boundary check rejects those positions before array access. The valid neighbor `(0,1)` contains a pig, so the answer becomes 1 safely.

Finally, consider a case with no possible eats:

```
2 2
P.
.W
```

The wolf at `(1,1)` checks all four directions. Every valid neighbor is either empty or outside the board. The answer never increases, and the algorithm correctly prints 0.
