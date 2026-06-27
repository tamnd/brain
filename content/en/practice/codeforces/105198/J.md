---
title: "CF 105198J - Monke, Potato and Their Knight Game"
description: "The board is infinite, so the only information that matters is the relative position between the starting square and the chosen destination square. For every test case, we are given two coordinates for the knight's initial position and two coordinates for the target position."
date: "2026-06-27T03:00:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105198
codeforces_index: "J"
codeforces_contest_name: "ShellBeeHaken Presents Intra SUST Programming Contest 2024 - Replay"
rating: 0
weight: 105198
solve_time_s: 65
verified: false
draft: false
---

[CF 105198J - Monke, Potato and Their Knight Game](https://codeforces.com/problemset/problem/105198/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** no  

## Solution
## Problem Understanding

The board is infinite, so the only information that matters is the relative position between the starting square and the chosen destination square. For every test case, we are given two coordinates for the knight's initial position and two coordinates for the target position. We need decide whether there exists a way for the knight to reach the target using an odd number of knight moves. If such a path exists, the winner is Monke. Otherwise, Potato wins.

The coordinates can be as large as $10^6$, and the number of test cases can reach $10^5$. This immediately rules out any simulation that explores the board, because even a small breadth-first search around one position would visit many squares and repeating that process $10^5$ times would exceed the available operations. We need a constant time observation that works directly from the coordinates.

The tricky part is that the board is infinite, so a naive approach might try to reason about the shortest knight path or build a search graph. The answer does not depend on the exact distance. It depends only on the coloring property of the knight graph.

A common mistake is to only check whether the target is reachable in one move. For example, the input `1 1 4 5` is a case where the target is not one knight move away, but the answer is still Monke because the knight can reach it in an odd number of moves. Another mistake is assuming that reaching a square in an even number of moves means an odd route might also exist. For `1 1 1 3`, the coordinate color is the same, so every possible route has even length. The correct output is `Potato`.

## Approaches

The direct brute-force solution would be to perform a graph search from the starting square. Each square is a node, and every knight move creates an edge. A breadth-first search can find the shortest distance to the destination, and if that distance is odd, Monke wins. Since a shortest path in an unweighted graph is found by BFS, this approach is correct.

The problem is the size of the graph. Even though we only need one destination, a BFS on an infinite board may have to examine a large number of squares. With $10^5$ test cases, any search-based method is impossible. In the worst case, if a search visits $K$ squares per test case, the total work becomes $O(10^5K)$, which is far beyond the limit.

The key observation comes from looking at the color of a chessboard square. A square can be colored by the parity of $x+y$. Every knight move changes $x+y$ by an odd amount because the move changes one coordinate by 1 and the other by 2. Adding those changes always gives an odd value. As a result, every knight move changes the color of the square.

This means the knight graph is bipartite. A path with an odd number of moves must end on the opposite color, and a path with an even number of moves must end on the same color. The remaining question is whether every opposite-colored square is reachable. The knight can reach every square on an infinite board, so color difference is the only condition that matters.

The brute-force works because it directly follows the graph definition, but fails because the graph is too large. The coloring property compresses the entire graph into a single parity check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(K)$ per test case, where $K$ is the number of explored squares | $O(K)$ | Too slow |
| Optimal | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the color of the starting square using $(x_1+y_1)\bmod 2$. The exact value of the sum is not needed, only whether it is odd or even, because the chessboard coloring repeats every two squares.
2. Compute the color of the destination square using $(x_2+y_2)\bmod 2$. This gives the color class where the knight must finish.
3. Compare the two colors. If they are different, the knight must have made an odd number of moves, so print `Monke`. If they are the same, every possible path has even length, so print `Potato`.

Why it works: every knight move switches the parity of $x+y$. After one move the color is flipped, after two moves it is restored, and this continues for all path lengths. The destination color completely determines the parity of every possible path length to that square. Since all squares are reachable on the infinite knight board, opposite colors correspond exactly to positions reachable in an odd number of moves.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        x1, y1, x2, y2 = map(int, input().split())

        if (x1 + y1) % 2 != (x2 + y2) % 2:
            ans.append("Monke")
        else:
            ans.append("Potato")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is processed one test case at a time, which keeps the memory usage constant even when there are many cases. The program only stores the output strings before printing them together, avoiding the overhead of many individual output operations.

The expression `(x1 + y1) % 2` is the entire core of the solution. Since only parity matters, the large coordinate values do not create any difficulty. Python integers also avoid overflow concerns, although the maximum possible sum here is already small enough for standard integer types in other languages.

The comparison is done directly between the two square colors. There is no need to calculate a distance, generate knight moves, or handle special coordinate cases because the infinite board removes boundary effects.

## Worked Examples

Using the sample cases:

| Start | Target | Start parity | Target parity | Result |
| --- | --- | --- | --- | --- |
| (1,1) | (4,5) | 0 | 1 | Monke |
| (100,2) | (9,11) | 0 | 0 | Potato |
| (1,1) | (1,2) | 0 | 1 | Monke |

The first case demonstrates that the answer is not about being one knight move away. The colors differ, so some odd-length route exists.

The second case shows that squares with the same color cannot be connected by an odd number of moves. Every knight move flips color, so returning to the same color requires an even number of flips.

The third case is the simplest opposite-color case. The knight may need several moves, but the parity condition guarantees the existence of an odd-length path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case requires only four additions and a parity comparison. |
| Space | $O(t)$ | The output list stores one answer per test case. |

With $t$ up to $10^5$, the linear running time is easily within the limit. The algorithm does not depend on the coordinate size or require any additional data structures.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        x1, y1, x2, y2 = map(int, input().split())
        if (x1 + y1) % 2 != (x2 + y2) % 2:
            ans.append("Monke")
        else:
            ans.append("Potato")

    return "\n".join(ans)

# provided sample
assert solution("""3
1 1 4 5
100 2 9 11
1 1 1 2
""") == """Monke
Potato
Monke""", "sample"

# minimum-size style case: same square
assert solution("""1
1 1 1 1
""") == "Potato", "same square"

# boundary values
assert solution("""1
1000000 1000000 1 2
""") == "Monke", "large coordinates"

# same color but far apart
assert solution("""1
1 1 1000000 1000000
""") == "Potato", "same parity"

# opposite color adjacent coordinates
assert solution("""1
999999 1000000 1000000 1000000
""") == "Monke", "parity difference"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 4 5` | `Monke` | Checks that the algorithm is not limited to one knight move. |
| `1 1 1 1` | `Potato` | Checks the zero-move case where the square color is unchanged. |
| `1000000 1000000 1 2` | `Monke` | Checks maximum coordinate handling. |
| `1 1 1000000 1000000` | `Potato` | Checks that same-color distant squares are rejected. |
| `999999 1000000 1000000 1000000` | `Monke` | Checks a boundary parity difference case. |

## Edge Cases

For the case `1 1 1 1`, both squares have parity $(1+1)\bmod 2=0$. The algorithm compares equal colors and outputs `Potato`. A careless implementation that assumes zero moves count as a valid odd path would incorrectly print `Monke`.

For the case `1 1 1 3`, both squares also have even parity. The knight cannot arrive in an odd number of moves because every move flips color, and an odd number of flips cannot return to the original color. The algorithm immediately detects equal parity and outputs `Potato`.

For the case `1000000 1000000 1 2`, the starting square has parity $0$, while the destination has parity $1$. The values are large, but only the last bit of the coordinate sum matters. The algorithm finds different colors and outputs `Monke` without any dependence on the board size.
