---
title: "CF 985A - Chess Placing"
description: "We are given a line of length $n$, where $n$ is even, and each position is either empty or contains exactly one chess piece. The board is colored in an alternating pattern starting with black at position 1, so positions look like B, W, B, W, and so on."
date: "2026-06-17T00:55:25+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 985
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 44 (Rated for Div. 2)"
rating: 1100
weight: 985
solve_time_s: 65
verified: true
draft: false
---

[CF 985A - Chess Placing](https://codeforces.com/problemset/problem/985/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of length $n$, where $n$ is even, and each position is either empty or contains exactly one chess piece. The board is colored in an alternating pattern starting with black at position 1, so positions look like B, W, B, W, and so on.

All pieces must be moved so that in the end they occupy only cells of a single color, either all black cells or all white cells. A move consists of shifting one piece by exactly one step left or right into an empty cell, and pieces cannot overlap or leave the board.

The goal is to minimize the total number of such single-step moves needed to achieve a configuration where all pieces sit only on cells of one chosen color.

The input size is small, with $n \le 100$, so even quadratic or cubic solutions are easily fast enough. That means we can afford to simulate movements or compute costs directly for each candidate target configuration without worrying about optimization tricks like prefix preprocessing or greedy heuristics being mandatory for performance reasons.

A subtle edge case arises from the fact that we are not told which color is optimal. A naive approach might assume black or white without checking both, which can fail. For example, if pieces are mostly aligned with white cells but slightly closer to black cells, the wrong assumption leads to a higher total cost.

Another pitfall is trying to simulate movements step by step. Since pieces block each other during movement, naive simulation can incorrectly estimate costs because intermediate states matter if handled incorrectly. The correct solution avoids simulation entirely and works with direct positional cost reasoning.

## Approaches

A brute-force interpretation would be to simulate all possible sequences of moves until all pieces land on valid target cells of either color. This would involve exploring all ways to assign pieces to target cells and then simulating shortest movement sequences under collision constraints. Even with $k$ pieces, the number of assignments alone is $O(k!)$, and each simulation requires at least linear time to resolve collisions. This quickly becomes infeasible even for moderate $k$.

The key simplification is to notice that the pieces do not interact in a way that changes the total cost if we fix their final destinations. Since each move is just shifting a piece by one position into an empty slot, and we only care about final occupied positions, the problem reduces to assigning each piece to a target cell of the chosen color and computing the sum of distances.

Once we fix a color, say black, we extract all black positions on the board. Then the problem becomes matching the current piece positions to a subset of these cells. The optimal assignment is achieved by sorting both lists and pairing them in order. This works because in a 1D line, the minimum sum of absolute differences matching is always obtained by sorted pairing.

We compute this cost for black cells and again for white cells, then take the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all moves) | Exponential | O(k!) | Too slow |
| Optimal (sort and pair) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Extract the positions of all pieces into a list.
2. Build two target lists: one containing all black positions and one containing all white positions.
3. For each target list, compute the cost of matching pieces to targets.
4. To compute matching cost, sort both the piece positions and the target positions.
5. Pair elements in sorted order and sum absolute differences.
6. Take the minimum of the two computed costs and output it.

The key idea in pairing step is that sorting ensures that large positions are matched with large positions and small with small, preventing unnecessary long jumps caused by crossing assignments.

### Why it works

The correctness relies on a standard property of optimal assignment on a line: the minimum sum of absolute differences between two equal-sized sets is achieved by sorting both and matching in order. Any crossing assignment can be improved by swapping endpoints, which strictly reduces or preserves total distance. Since both color choices reduce to this matching problem, evaluating both and taking the minimum guarantees global optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
pieces = list(map(int, input().split()))

# build black and white positions (1-indexed board)
black = []
white = []

for i in range(1, n + 1):
    if i % 2 == 1:
        black.append(i)
    else:
        white.append(i)

def cost(targets):
    if len(targets) != len(pieces):
        return float('inf')
    pieces_sorted = sorted(pieces)
    targets_sorted = sorted(targets)
    return sum(abs(p - t) for p, t in zip(pieces_sorted, targets_sorted))

print(min(cost(black), cost(white)))
```

The implementation first collects all piece positions. It then constructs the two possible destination sets based on board coloring. The helper function computes the matching cost using sorted pairing.

A subtle point is ensuring the counts match: only one color has exactly $n/2$ cells, but the number of pieces is guaranteed to match one of the two color classes, so we guard the other case by returning infinity.

## Worked Examples

### Example 1

Input:

```
6
1 2 6
```

Black positions: [1, 3, 5]

White positions: [2, 4, 6]

#### Matching to black

| Step | Pieces sorted | Targets sorted | Pairing | Cost |
| --- | --- | --- | --- | --- |
| 1 | [1,2,6] | [1,3,5] | (1,1),(2,3),(6,5) | 0 + 1 + 1 = 2 |

#### Matching to white

| Step | Pieces sorted | Targets sorted | Pairing | Cost |
| --- | --- | --- | --- | --- |
| 1 | [1,2,6] | [2,4,6] | (1,2),(2,4),(6,6) | 1 + 2 + 0 = 3 |

Minimum is 2.

This confirms that evaluating both color choices is necessary because the better option is not always obvious from initial positions.

### Example 2

Input:

```
4
1 3
```

Black positions: [1, 3]

White positions: [2, 4]

#### Matching to black

| Step | Pieces sorted | Targets sorted | Pairing | Cost |
| --- | --- | --- | --- | --- |
| 1 | [1,3] | [1,3] | (1,1),(3,3) | 0 |

#### Matching to white

| Step | Pieces sorted | Targets sorted | Pairing | Cost |
| --- | --- | --- | --- | --- |
| 1 | [1,3] | [2,4] | (1,2),(3,4) | 1 + 1 = 2 |

Minimum is 0.

This shows that even if both configurations are valid, one can already be optimal without any movement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting piece positions and targets dominates computation |
| Space | $O(n)$ | storing positions of pieces and two color classes |

The constraints $n \le 100$ make this solution extremely safe, with sorting and linear scans running instantly.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    n = int(input())
    pieces = list(map(int, input().split()))

    black, white = [], []
    for i in range(1, n + 1):
        if i % 2:
            black.append(i)
        else:
            white.append(i)

    def cost(targets):
        if len(targets) != len(pieces):
            return float('inf')
        a = sorted(pieces)
        b = sorted(targets)
        return sum(abs(x - y) for x, y in zip(a, b))

    print(min(cost(black), cost(white)))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("6\n1 2 6\n") == "2"

# minimum input
assert run("2\n1\n") == "0"

# already optimal on black
assert run("4\n1 3\n") == "0"

# needs movement
assert run("4\n1 2\n") == "1"

# worst spread
assert run("6\n1 6\n") in ["2", "2"]

# symmetric case
assert run("8\n1 3 5 7\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2, 1 | 0 | minimal edge case |
| 4, 1 3 | 0 | already aligned configuration |
| 4, 1 2 | 1 | single-move adjustment |
| 6, 1 6 | 2 | long-distance movement |
| 8, 1 3 5 7 | 0 | perfect black alignment |

## Edge Cases

A key edge case is when all pieces already lie on one color. For input:

```
4
1 3
```

the black cells are exactly the occupied ones. The algorithm computes zero cost because sorted pairing matches identical positions.

Another edge case is when pieces are concentrated on the wrong parity. For:

```
4
2 4
```

black targets are [1,3]. Sorting gives pairing (2,1),(4,3) resulting in cost 2. White targets are [2,4], giving cost 0. The algorithm correctly selects the white configuration because it evaluates both possibilities symmetrically and does not assume parity alignment.

A third edge case is uneven initial spacing. Even if pieces are far apart, sorting-based matching ensures that no crossing assignment artificially inflates cost, since each piece is paired with its nearest structural target in order rather than greedily choosing locally closest positions.
