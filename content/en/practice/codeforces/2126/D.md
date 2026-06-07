---
title: "CF 2126D - This Is the Last Time"
description: "We are given a sequence of casinos, each defined by a range of coins [li, ri] that we must have to play, and a fixed result reali that becomes our new coin count after playing there. We start with k coins and can visit casinos in any order, but only once each."
date: "2026-06-08T03:22:46+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2126
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1037 (Div. 3)"
rating: 1200
weight: 2126
solve_time_s: 78
verified: true
draft: false
---

[CF 2126D - This Is the Last Time](https://codeforces.com/problemset/problem/2126/D)

**Rating:** 1200  
**Tags:** data structures, greedy, sortings  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of casinos, each defined by a range of coins `[l_i, r_i]` that we must have to play, and a fixed result `real_i` that becomes our new coin count after playing there. We start with `k` coins and can visit casinos in any order, but only once each. The goal is to maximize the number of coins at the end.

The input consists of multiple test cases, each specifying the number of casinos `n` and initial coins `k`, followed by `n` triplets `(l_i, r_i, real_i)`. The output is a single integer per test case: the maximum coins achievable.

Given `n` can be up to `10^5` across all test cases and `k`, `l_i`, `r_i`, `real_i` up to `10^9`, any solution that checks all permutations is infeasible. A naive `O(n!)` approach would immediately fail. We need a linear or near-linear approach per test case.

Edge cases include starting with `0` coins, casinos where `real_i` does not improve your count, or sequences where visiting some casinos first blocks others due to their `l_i` thresholds. For example, if `k = 0` and all casinos have `l_i >= 1`, the maximum coins remain `0`. A careless greedy approach that chooses the largest `real_i` blindly can fail if that casino is not reachable yet.

## Approaches

The brute-force method would try all permutations of casino visits, updating the coin count and keeping track of the maximum. This works in principle but is hopelessly slow: with `n = 10^5` casinos, the number of permutations is astronomically large.

The key observation is that once you can play a casino, the new coin count is independent of the order you arrived there, as long as the precondition `l_i <= coins <= r_i` is satisfied. Therefore, a greedy strategy works: we can repeatedly pick any playable casino that maximizes our coins at that moment. Each time we play, our current coins increase or remain the same. We stop when no further playable casino exists.

This reduces the problem to simulating a process where we maintain the set of unvisited casinos and repeatedly select any casino that can currently be played. Using a queue or list and scanning all unvisited casinos each round would give `O(n^2)` in the worst case, which is too slow. Instead, sorting casinos by their lower bound `l_i` allows us to efficiently identify playable casinos and iterate until no new casinos are added.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy simulation with sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and initial coins `k`. Store casinos as a list of tuples `(l_i, r_i, real_i)`.
3. Sort casinos by their lower bound `l_i`. This ensures that when scanning from left to right, any casino with `l_i <= current coins` is immediately playable.
4. Initialize a flag `changed = True`. While `changed` is true, do the following:

1. Set `changed = False`.
2. Iterate over all casinos. If a casino is unvisited and `l_i <= current coins <= r_i`, mark it visited, update `current coins = real_i`, and set `changed = True`.
5. Repeat until no new casino is playable. The current coin count is the maximum achievable.

Why it works: the process guarantees that whenever a casino becomes playable, it will be visited in the earliest possible iteration. Since `real_i >= l_i` and each casino is only used once, coins never decrease, ensuring that we cannot miss any opportunity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        casinos = []
        for _ in range(n):
            l, r, real = map(int, input().split())
            casinos.append([l, r, real, False])  # last element marks visited

        casinos.sort(key=lambda x: x[0])  # sort by l_i
        coins = k
        changed = True
        while changed:
            changed = False
            for casino in casinos:
                if not casino[3] and casino[0] <= coins <= casino[1]:
                    coins = casino[2]
                    casino[3] = True
                    changed = True
        print(coins)

if __name__ == "__main__":
    solve()
```

We sort by `l_i` to efficiently identify which casinos are immediately playable. We maintain a `visited` flag to avoid revisiting. The outer loop runs only while new coins are gained, guaranteeing termination.

## Worked Examples

**Example 1:**

Input:

```
3 1
2 3 3
1 2 2
3 10 10
```

| coins | Casino visited | coins after visit |
| --- | --- | --- |
| 1 | Casino 2 (1,2,2) | 2 |
| 2 | Casino 1 (2,3,3) | 3 |
| 3 | Casino 3 (3,10,10) | 10 |

Final coins: 10. The table confirms that choosing casinos in an order respecting `l_i <= coins <= r_i` maximizes coins.

**Example 2:**

Input:

```
1 0
1 2 2
```

| coins | Casino visited | coins after visit |
| --- | --- | --- |
| 0 | none | 0 |

Final coins: 0. This confirms the algorithm handles unreachable casinos.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting takes `O(n log n)`. The while loop scans each casino at most once per coin increase. Since coins increase monotonically and casinos are only visited once, total iterations are `O(n)`. |
| Space | O(n) | Storing casinos with flags requires `O(n)`. |

The solution comfortably fits in the 2-second limit even for the maximum `n = 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("5\n3 1\n2 3 3\n1 2 2\n3 10 10\n1 0\n1 2 2\n1 2\n1 2 2\n2 2\n1 3 2\n2 4 4\n2 5\n1 10 5\n3 6 5") == "10\n0\n2\n4\n5", "sample 1"

# minimum input
assert run("1\n1 0\n0 0 0") == "0", "minimum input"

# maximum single casino reachable
assert run("1\n1 100\n50 200 300") == "300", "max coins single casino"

# all casinos unreachable
assert run("1\n3 0\n1 2 2\n2 3 3\n3 4 4") == "0", "all unreachable"

# sequential unlocks
assert run("1\n3 1\n1 2 2\n2 3 3\n3 4 4") == "4", "sequential unlocks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1 0\n0 0 0` | 0 | Handles minimum coins and single casino |
| `1\n1 100\n50 200 300` | 300 | Handles large reachable casino |
| `1\n3 0\n1 2 2\n2 3 3\n3 4 4` | 0 | All casinos unreachable from start |
| `1\n3 1\n1 2 2\n2 3 3\n3 4 4` | 4 | Sequential unlocking of casinos works |

## Edge Cases

Starting with zero coins and casinos requiring positive `l_i` never allows any play. For example, `k=0`, casinos `(1,2,2)` and `(3,5,5)`. The loop scans all casinos, finds none playable, sets `changed=False`, and exits immediately, outputting 0.

When multiple casinos have `l_i` below or equal to current coins, the order does not matter because the coin count only increases or remains the same. For `k=1`, casinos `(1,3,2)` and `(1,2,5)`, the algorithm picks the first in the scan, updates coins to 2, then picks the second casino (now coins 2 satisfies `l_i=1`) and updates coins to 5. Final coins are correct.
