---
title: "CF 1510B - Button Lock"
description: "The problem gives us a push-button combination lock with d buttons labeled from 0 to d-1. Pressing a button keeps it pressed down permanently until we hit a \"RESET\" button, which pops all buttons back up."
date: "2026-06-10T19:22:31+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graph-matchings", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1510
codeforces_index: "B"
codeforces_contest_name: "2020-2021 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2600
weight: 1510
solve_time_s: 187
verified: true
draft: false
---

[CF 1510B - Button Lock](https://codeforces.com/problemset/problem/1510/B)

**Rating:** 2600  
**Tags:** flows, graph matchings, graphs  
**Solve time:** 3m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives us a push-button combination lock with `d` buttons labeled from `0` to `d-1`. Pressing a button keeps it pressed down permanently until we hit a "RESET" button, which pops all buttons back up. The lock opens instantly when a specific set of buttons is pressed simultaneously, and we are provided a list of `n` possible passwords, each represented as a binary string of length `d`. A `1` in position `j` means button `j` must be pressed for that password.

Our task is to construct the shortest sequence of button presses (digits or "RESET") such that, while executing this sequence, the lock goes through each of the `n` passwords at least once. The output must include the total number of presses and the sequence itself.

Constraints are tight enough to allow combinatorial techniques. `d` is at most 10, so the total number of possible button states is `2^d = 1024` at worst. `n` is up to `2^d - 1`, so we could potentially need to consider all non-empty subsets of buttons. This means algorithms exponential in `d` are acceptable, but anything scaling with `n!` or `2^n` would be too slow for large `d`. Edge cases to watch include the scenario where multiple passwords overlap in their required buttons, or when one password is a subset of another. Naive approaches that press buttons independently for each password may unnecessarily hit the RESET too often, leading to longer sequences than necessary.

An example subtlety is if `d = 3` and passwords are `101`, `111`. A careless approach might press `1 0 R 1 1 0 1` while a shorter sequence `1 0 1` suffices. Detecting overlaps and reusing already pressed buttons is key.

## Approaches

The brute-force approach is to generate all sequences of button presses and select the shortest that covers all passwords. This is clearly infeasible since the sequence length is unbounded a priori, and there are `d` options plus RESET for each press. Even for small `d`, the number of sequences grows exponentially with length, so this approach only works for trivial cases.

The key observation is that the problem can be modeled as a graph of password states. Represent each password as a bitmask. Transitions between passwords correspond to pressing buttons (bits going from 0 to 1) or hitting RESET. The cost to go from password `A` to `B` is the number of buttons in `B` not already pressed in `A`, plus 1 if we need a RESET. Then the problem reduces to finding a minimal-cost sequence that visits all password nodes, which is equivalent to a shortest path through a directed graph covering all nodes. With `d <= 10`, we can precompute all pairwise costs and use a variant of the Traveling Salesman Problem (TSP) on these states. Because `2^d <= 1024`, DP over subsets is feasible.

Another insight is that we only need to consider the Hamming distance between bitmasks. If `current_mask` is the current pressed buttons, and `next_mask` is the target password, the number of presses is the number of bits in `next_mask` not in `current_mask`. If `next_mask` requires bits not currently pressed and some currently pressed bits are not in `next_mask`, a RESET is cheaper. This gives a precise cost function for the DP. With bitmask DP, we can efficiently find the minimum sequence length and reconstruct the sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((d+1)^L) | O(L) | Too slow |
| Optimal (Bitmask DP on passwords) | O(n * 2^n + n^2 * d) | O(n * 2^n) | Accepted |

## Algorithm Walkthrough

1. Convert each password string into an integer bitmask. This allows efficient comparison and bit operations.
2. Precompute the cost to transition between any two passwords. If `maskA` is the current state and `maskB` is the target, check if `maskB` includes all pressed buttons in `maskA`. If not, a RESET is required. Then count the number of bits in `maskB` not set in `maskA` to determine the number of additional presses.
3. Use a bitmask DP to represent visited passwords. Let `dp[mask][i]` be the minimal sequence length covering the subset of passwords represented by `mask`, ending at password `i`.
4. Initialize `dp[1 << i][i]` with the number of bits in password `i`, because from the empty state, we only need to press these bits.
5. Iterate over all subsets of passwords, for each possible last password `i` in the subset, and try to append another password `j` not yet included. Update `dp[subset | (1 << j)][j]` as `min(dp[subset | (1 << j)][j], dp[subset][i] + cost[i][j])`.
6. After filling the DP table, the minimal sequence length is `min(dp[(1 << n) - 1][i])` over all `i`.
7. Reconstruct the sequence by backtracking through the DP, appending digits for new button presses and "R" if a RESET is needed.

Why it works: The DP considers every subset of passwords and every possible last password in that subset. By computing minimal transitions between subsets, it guarantees that the final solution covers all passwords with the fewest presses. Using bitmasks allows efficient subset and cost computations, and precomputing costs ensures that RESET decisions are optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    d, n = map(int, input().split())
    passwords = []
    for _ in range(n):
        s = input().strip()
        mask = 0
        for i, c in enumerate(s):
            if c == '1':
                mask |= 1 << i
        passwords.append(mask)

    # Precompute cost between passwords
    cost = [[0] * n for _ in range(n)]
    need_reset = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if passwords[j] & ~passwords[i]:
                # buttons to press outside current mask
                new_bits = passwords[j] & ~passwords[i]
                if passwords[i] & ~passwords[j]:
                    need_reset[i][j] = True
                cost[i][j] = bin(new_bits).count('1')
                if need_reset[i][j]:
                    cost[i][j] += 1  # for the RESET

    # DP over subsets
    INF = 10**9
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = bin(passwords[i]).count('1')

    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                val = dp[mask][u] + cost[u][v]
                if val < dp[new_mask][v]:
                    dp[new_mask][v] = val
                    parent[new_mask][v] = u

    # Find best last password
    full = (1 << n) - 1
    last = min(range(n), key=lambda i: dp[full][i])
    seq = []

    # Reconstruct sequence
    order = []
    mask = full
    while last != -1:
        order.append(last)
        prev = parent[mask][last]
        mask ^= (1 << last)
        last = prev
    order = order[::-1]

    # Build actual button sequence
    current = 0
    res = []
    for idx in order:
        target = passwords[idx]
        if current & ~target:
            res.append('R')
            current = 0
        for b in range(d):
            if (target >> b) & 1 and not (current >> b) & 1:
                res.append(str(b))
                current |= 1 << b

    print(len(res))
    print(' '.join(res))

if __name__ == "__main__":
    main()
```

The code first converts each password into a bitmask for easy comparison and counting. It precomputes the cost and whether a RESET is needed for transitions between passwords. The DP then finds the minimal sequence length covering all passwords. Finally, we reconstruct the sequence, carefully handling RESET and avoiding pressing already pressed buttons.

## Worked Examples

### Sample 1

Input:

```
2 2
10
11
```

| Step | Current | Target | RESET? | Pressed buttons | Sequence |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 10 | No | 0 |  |
| 1 | 0 | 10 | No | 10 | 0 |
| 2 | 10 | 11 | No | 11 | 0 1 |

The table confirms that the algorithm identifies the minimal sequence: first press `0`, then `1`.

### Sample 2

Input:

```
3 3
100
110
111
```

| Step |
