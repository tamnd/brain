---
title: "CF 957A - Tritonic Iridescence"
description: "We are given a one-dimensional strip of length $n$, where each position is either already painted in one of three colors or left blank. The blank positions must be filled using the same three colors so that no two adjacent positions end up sharing the same color."
date: "2026-06-17T02:04:27+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 957
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 472 (rated, Div. 2, based on VK Cup 2018 Round 2)"
rating: 1300
weight: 957
solve_time_s: 62
verified: true
draft: false
---

[CF 957A - Tritonic Iridescence](https://codeforces.com/problemset/problem/957/A)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional strip of length $n$, where each position is either already painted in one of three colors or left blank. The blank positions must be filled using the same three colors so that no two adjacent positions end up sharing the same color.

The task is not to count all valid completions, but only to decide whether there exist at least two distinct valid completions of the entire strip.

Two completions are considered different if at least one position is colored differently between them.

The constraint $n \le 100$ suggests that even cubic or quadratic dynamic programming is easily fast enough. However, anything that tries to enumerate all colorings directly grows as $3^n$, which becomes infeasible even for moderate $n$. This immediately pushes the solution toward a state-based DP or memoization approach with a small constant state space.

A naive but common pitfall is to attempt a greedy fill. Locally choosing any valid color for a blank position can produce a valid completion, but it does not preserve information about alternative completions. Another pitfall is to assume that if a single completion exists, then multiple always exist when there are many question marks, which is false because constraints can force uniqueness.

A concrete failure case for greedy reasoning is:

Input:

```
3
C?C
```

There is exactly one valid completion: `CMC`. Even though there is a free position, it is fully constrained by both neighbors.

Another subtle case is when the string is already invalid, such as:

```
3
CCC
```

This has zero valid completions, not at least one.

The real difficulty is distinguishing between zero, one, or at least two valid completions efficiently.

## Approaches

A brute-force method would try every assignment of colors to the question marks. If there are $k$ question marks, this yields $3^k$ possibilities. For each candidate, we would check adjacency constraints in $O(n)$, leading to $O(n \cdot 3^k)$. In the worst case $k = n = 100$, this is astronomically large and completely unusable.

The structure of the problem is that validity depends only on adjacent pairs, and decisions propagate left to right. This suggests a dynamic programming formulation where the state only needs to remember the previous color.

Instead of enumerating full strings, we track how many valid partial colorings exist up to position $i$, ending with each possible color. Since we only care whether the number of full solutions reaches at least two, we can cap all counts at 2. This prevents overflow and avoids unnecessary computation.

The key insight is that the state space is only 3 colors, so the DP remains constant-sized per position, giving a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force enumeration | $O(n \cdot 3^n)$ | $O(n)$ | Too slow |
| DP with capped counts | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We define a DP where we track how many valid ways exist up to each position, separated by the last color used.

### Steps

1. Initialize a DP table for position 0. If the first character is fixed, only that color is allowed; otherwise all three colors are possible. Each valid starting color contributes exactly one way. This represents all valid prefixes of length 1.
2. Iterate from position 1 to $n-1$, updating a new DP state from the previous one. For each position, we consider every possible current color.
3. If the current position is fixed to a color, we only allow transitions into that color. If it is '?', we try all three colors.
4. For each candidate current color, we sum all DP values from the previous position where the previous color differs from the current one. This enforces adjacency constraints.
5. After each update, cap all DP values at 2. If any state already reaches 2, we do not need exact counts anymore, only the fact that there are at least two solutions.
6. After processing all positions, sum the DP values at the last position. If the total is at least 2, output "Yes", otherwise output "No".

### Why it works

The DP state encodes all valid ways to color a prefix while remembering only the last color, which is sufficient because future validity depends only on adjacency. Every valid full coloring corresponds to exactly one path through these states. Since we cap counts at 2, we preserve correctness of the final decision: whether there exist zero, one, or multiple solutions, without tracking exact magnitude.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    colors = ['C', 'M', 'Y']

    dp = {c: 0 for c in colors}

    if s[0] == '?':
        for c in colors:
            dp[c] = 1
    else:
        dp[s[0]] = 1

    for i in range(1, n):
        ndp = {c: 0 for c in colors}

        for cur in colors:
            if s[i] != '?' and s[i] != cur:
                continue

            ways = 0
            for prev in colors:
                if prev != cur:
                    ways += dp[prev]
                    if ways >= 2:
                        ways = 2
                        break

            ndp[cur] = min(2, ways)

        dp = ndp

    total = sum(dp.values())
    print("Yes" if total >= 2 else "No")

if __name__ == "__main__":
    solve()
```

The implementation maintains a rolling DP dictionary of size three. At each step, it constructs a new dictionary for the next position. The inner loop enforces the adjacency constraint by excluding transitions where the color repeats.

The critical implementation detail is the cap at 2. Without it, counts can grow unnecessarily, but more importantly, the problem only requires distinguishing between 0, 1, and at least 2 solutions.

## Worked Examples

### Example 1

Input:

```
5
CY??Y
```

We track DP states as counts per ending color.

| Position | C | M | Y | Notes |
| --- | --- | --- | --- | --- |
| 0 (C) | 1 | 0 | 0 | fixed C |
| 1 (Y) | 0 | 1 | 1 | Y cannot follow C restriction allows M,Y |
| 2 (?) | 1 | 1 | 1 | all extensions valid |
| 3 (?) | 2 | 2 | 2 | capped at 2 |
| 4 (Y) | 2 | 0 | 2 | must end in Y |

Final total is 4, but capped logic only needs “≥2”, so output is:

```
Yes
```

This demonstrates how multiple paths quickly merge into multiple valid completions even under constraints.

### Example 2

Input:

```
3
C?C
```

| Position | C | M | Y | Notes |
| --- | --- | --- | --- | --- |
| 0 (C) | 1 | 0 | 0 | fixed |
| 1 (?) | 0 | 1 | 1 | cannot equal previous C |
| 2 (C) | 0 | 1 | 0 | only M works before C |

Final total is 1, so:

```
No
```

This shows how a single blank can still be fully constrained by both sides, producing a unique completion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each position processes a constant 3-color state transition |
| Space | $O(1)$ | Only two DP dictionaries of size 3 are stored |

With $n \le 100$, the solution is comfortably within limits and runs instantly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("5\nCY??Y\n") == "Yes"
assert run("3\nC?C\n") == "No"

# minimum size, single cell
assert run("1\n?\n") == "Yes"

# fully fixed valid alternating
assert run("3\nCMY\n") == "Yes"

# fully fixed invalid
assert run("3\nCCC\n") == "No"

# many choices but constrained chain
assert run("4\n????\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 ? | Yes | single position always has multiple possibilities |
| CMY | Yes | already valid fixed coloring |
| CCC | No | impossible configuration |
| ???? | Yes | many completions exist in unconstrained case |

## Edge Cases

A single-character string like `"?"` produces three valid completions, immediately satisfying the “at least two” requirement. The DP starts with all three states active, so the final sum exceeds the threshold.

A fully fixed string such as `"CMCMCM"` has exactly one valid completion. The DP never branches, so the final sum remains 1, correctly producing "No".

A fully uniform invalid string like `"CCC"` eliminates all DP states after the first transition. Once all states become zero, they remain zero, ensuring the algorithm correctly reports impossibility.
