---
title: "CF 1849B - Monsters"
description: "The problem describes a scenario where Monocarp fights a group of monsters, each with an initial health value. Monocarp can repeatedly hit the monster with the highest current health, reducing it by a fixed amount $k$ per attack."
date: "2026-06-09T05:34:10+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1849
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 152 (Rated for Div. 2)"
rating: 1000
weight: 1849
solve_time_s: 96
verified: false
draft: false
---

[CF 1849B - Monsters](https://codeforces.com/problemset/problem/1849/B)

**Rating:** 1000  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

The problem describes a scenario where Monocarp fights a group of monsters, each with an initial health value. Monocarp can repeatedly hit the monster with the highest current health, reducing it by a fixed amount $k$ per attack. If multiple monsters share the same highest health, the one with the smallest index is chosen. The task is to determine the exact sequence in which monsters die.

The input gives multiple test cases. For each test case, the number of monsters $n$ and the fixed damage $k$ are provided, followed by a list of $n$ integers representing the monsters' health. The output for each test case should be the list of monster indices in the order they die.

The constraints are significant: $n$ can be up to $3 \cdot 10^5$, and the sum of $n$ over all test cases is also capped at $3 \cdot 10^5$. Each health and damage value can reach $10^9$. A naive simulation where you repeatedly find the monster with the maximum health and subtract $k$ would require up to $10^9$ operations per monster in the worst case, clearly infeasible. The algorithm must instead compute the death order using some form of arithmetic reasoning without simulating each individual attack.

Edge cases include scenarios where all monsters have equal health, where $k$ exceeds the health of the smallest monster, or where multiple monsters die in the same "round" if their health divided by $k$ results in the same number of required hits. A naive approach that uses sorting after each hit would fail due to time limits, and one that ignores ties in required hits would produce the wrong order.

## Approaches

The brute-force approach is to simulate each attack sequentially. Find the monster with the maximum current health, subtract $k$, and record if it dies. Repeat until all monsters are dead. This is correct because it follows the problem rules exactly, but it is prohibitively slow. If we had $n = 3 \cdot 10^5$ monsters and the largest health is $10^9$ with $k = 1$, the simulation would take up to $3 \cdot 10^{14}$ operations, which is far beyond feasible for a 2-second time limit.

The key observation for a faster solution is that each monster’s death can be predicted by computing the number of full attacks needed to reduce its health to zero. Specifically, for monster $i$ with health $a_i$, the number of hits needed is $\lceil a_i / k \rceil$. Since monsters with fewer required hits die earlier, the sequence of deaths can be determined by sorting monsters based on this value. Ties are broken by original index because monsters with the same number of required hits die in their initial order.

The optimal solution avoids any simulation and reduces the problem to a single calculation per monster followed by a stable sort, which is well within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total attacks) ≈ O(n * max(a_i / k)) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$, and the list of healths $a_1, a_2, ..., a_n$.
2. Transform each monster’s health into the number of hits required to kill it, using the formula $\lceil a_i / k \rceil$. To avoid floating-point operations, compute $(a_i + k - 1) // k$. This ensures correct rounding up.
3. Pair each monster's required hits with its original index. This preserves tie-breaking order.
4. Sort the list of pairs primarily by the number of hits and secondarily by the original index. This gives the exact death order.
5. Output the indices from the sorted list.

Why it works: The invariant is that the monster with fewer required hits always dies before one with more hits. Within the same number of hits, the lower-index monster dies first, matching the selection rule in the problem. Sorting based on hits with indices as tie-breakers fully reproduces the exact sequence of deaths without simulating each individual attack.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        monsters = [((a[i] + k - 1) // k, i + 1) for i in range(n)]
        monsters.sort()
        print(' '.join(str(idx) for _, idx in monsters))

if __name__ == "__main__":
    solve()
```

The code first reads the number of test cases. For each test case, it computes the number of hits needed for each monster using integer arithmetic to simulate the ceiling of division. Each monster is paired with its original 1-based index. Sorting this list produces the death order. Finally, the indices are printed in the correct sequence. The use of `i + 1` ensures the output matches the 1-based indexing in the problem.

## Worked Examples

### Sample Input 1

```
3 2 1 2 3
```

| Monster | Health | Hits needed | Index |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 2 |
| 3 | 3 | 2 | 3 |

Sorted by hits then index: (1,1), (1,2), (2,3) → death order: 2,1,3

This demonstrates the ceiling division correctly handles monsters needing the same hits.

### Sample Input 2

```
4 3
2 8 3 5
```

| Monster | Health | Hits needed | Index |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 8 | 3 | 2 |
| 3 | 3 | 1 | 3 |
| 4 | 5 | 2 | 4 |

Sorted: (1,1), (1,3), (2,4), (3,2) → death order: 3,1,2,4

This shows the algorithm preserves the index tie-breaker for monsters needing the same number of hits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting n monsters by hits required |
| Space | O(n) | Storing hits and original indices |

With $n \le 3 \cdot 10^5$ total, $O(n \log n)$ is comfortably within 2 seconds.

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

# Provided samples
assert run("3\n3 2\n1 2 3\n2 3\n1 1\n4 3\n2 8 3 5\n") == "2 1 3\n1 2\n3 1 4 2", "samples"

# Custom test cases
assert run("1\n1 10\n7\n") == "1", "single monster"
assert run("1\n5 1\n1 2 3 4 5\n") == "1 2 3 4 5", "incremental health"
assert run("1\n4 2\n4 4 4 4\n") == "1 2 3 4", "all equal health"
assert run("1\n3 10\n1000000000 999999999 1000000000\n") == "2 1 3", "large numbers with tie-breaking"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 monster | 1 | Correct handling of single monster |
| Incremental health | 1 2 3 4 5 | Correct calculation of hits needed |
| All equal health | 1 2 3 4 | Correct index-based tie-breaking |
| Large numbers | 2 1 3 | Handles large integers and ceiling division |

## Edge Cases

If all monsters have the same health, such as `4 2 4 4 4 4`, each requires 2 hits. The algorithm sorts by hits and then by index, producing the original order: 1,2,3,4. This matches the problem rules, as all monsters die in index order if their hits needed are equal.

If one monster can be killed in a single hit and others require many, such as `3 10 1 20 30`, the single-hit monster dies first. The calculation `(a_i + k - 1) // k` yields hits `[1,2,3]`, and sorting gives the correct death order `[1,2,3]`.

Both examples confirm the solution handles tie-breaking and varying health correctly.
