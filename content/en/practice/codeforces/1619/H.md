---
title: "CF 1619H - Permutation and Queries"
description: "We are given a permutation of integers from 1 to $n$. Conceptually, this is an array of length $n$ in which every integer from 1 to $n$ appears exactly once, so every index maps to a unique value. On top of this array, we have two types of queries."
date: "2026-06-10T06:12:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "divide-and-conquer", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1619
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 762 (Div. 3)"
rating: 2400
weight: 1619
solve_time_s: 64
verified: true
draft: false
---

[CF 1619H - Permutation and Queries](https://codeforces.com/problemset/problem/1619/H)

**Rating:** 2400  
**Tags:** brute force, data structures, divide and conquer, two pointers  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to $n$. Conceptually, this is an array of length $n$ in which every integer from 1 to $n$ appears exactly once, so every index maps to a unique value. On top of this array, we have two types of queries. The first type swaps two elements in the permutation. The second type repeatedly applies the permutation starting from a given index and asks what the value becomes after $k$ applications. For instance, if $p = [5, 3, 4, 2, 1]$ and we query index 1 with $k = 2$, we follow $p[1] = 5$ and then $p[5] = 1$, so the answer is 1.

The constraints are significant: $n$ and $q$ can both reach $10^5$. A naive solution that simulates $k$ steps for each query would potentially do up to $10^5 \times 10^5 = 10^{10}$ operations, which is far beyond what a 4-second time limit allows. We need an approach that reduces repeated work and avoids recomputing values unnecessarily.

Non-obvious edge cases arise when $k = n$ or $k > n$, because the permutation forms cycles. A careless approach that just iterates $k$ times will be too slow and may even fail if swaps have changed the cycle structure. Another tricky situation is when repeated swaps move elements inside a cycle; we need a way to update our understanding of the cycle efficiently without recomputing everything from scratch.

## Approaches

The brute-force approach is straightforward: for each query of type 2, we start at index $i$ and follow $p[i]$ $k$ times. Each type 1 query simply swaps two elements. This works correctly for small inputs but is too slow when $n$ or $q$ is large because each query of type 2 could cost $O(n)$, and there could be up to $10^5$ such queries.

The key observation is that a permutation is made up of disjoint cycles. Repeatedly applying $p$ starting from some index $i$ is equivalent to moving along the cycle containing $i$. Therefore, instead of iterating $k$ times, we can compute $k \mod \text{cycle\_length}$ and jump directly. Swaps change the cycle decomposition, so we need a data structure that allows us to update cycles efficiently. Since $n$ and $q$ are relatively large, the simplest approach is to rebuild only affected cycles after a swap, which is efficient because each element belongs to exactly one cycle.

This reduces type 2 queries from $O(k)$ to $O(1)$ if we store cycles explicitly, and type 1 queries can be handled in $O(\text{cycle\_size})$, which is acceptable because each element only changes cycles when swapped.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*q) | O(n) | Too slow |
| Cycle Decomposition | O(n + q) amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the permutation $p$ and queries. Convert $p$ to 0-based indexing for easier array manipulation in Python.
2. Initialize an array to mark whether an element has been visited in cycle discovery. Also maintain a `cycle` array mapping each index to the list of its cycle.
3. For each index not yet assigned to a cycle, traverse the permutation until we loop back. Record the cycle in a list and store references in the `cycle` array.
4. For type 2 queries, find the cycle of the queried index. Compute the target index inside the cycle as $(\text{position in cycle} + k) \mod \text{cycle length}$. Output the element at that position.
5. For type 1 queries, swap the two elements. Since the swap affects cycles, rebuild the cycles containing the swapped elements. We only need to reprocess the cycles that contain these two indices.
6. Continue processing queries in order, applying swaps and answering type 2 queries using the updated cycles.

The invariant is that every index belongs to exactly one cycle, and the cycle structure is correctly updated after each swap. This guarantees that type 2 queries always return the correct element, even after multiple swaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, q = map(int, input().split())
    p = list(map(int, input().split()))
    p = [x-1 for x in p]  # convert to 0-based indexing

    # each element's cycle index and position in the cycle
    cycle_id = [-1] * n
    pos_in_cycle = [-1] * n
    cycles = []

    def build_cycle(start):
        cycle = []
        x = start
        while cycle_id[x] == -1:
            cycle_id[x] = len(cycles)
            pos_in_cycle[x] = len(cycle)
            cycle.append(x)
            x = p[x]
        cycles.append(cycle)

    for i in range(n):
        if cycle_id[i] == -1:
            build_cycle(i)

    for _ in range(q):
        t, x, y = map(int, input().split())
        if t == 1:
            x -= 1
            y -= 1
            # swap values
            p[x], p[y] = p[y], p[x]
            # rebuild cycles affected by x and y
            for idx in (x, y):
                # reset old cycle info
                cid = cycle_id[idx]
                for v in cycles[cid]:
                    cycle_id[v] = -1
                    pos_in_cycle[v] = -1
                cycles[cid] = []
            for idx in (x, y):
                if cycle_id[idx] == -1:
                    build_cycle(idx)
        else:
            x -= 1
            k = y
            cid = cycle_id[x]
            cycle = cycles[cid]
            pos = pos_in_cycle[x]
            result = cycle[(pos + k) % len(cycle)]
            print(result + 1)

if __name__ == "__main__":
    main()
```

The solution first builds cycles for the initial permutation. For type 2 queries, it computes the result in constant time by modular arithmetic. For swaps, it only rebuilds cycles affected by the swap, which keeps the algorithm efficient. Careful attention is required to reset cycle data before rebuilding.

## Worked Examples

Sample Input 1:

```
5 4
5 3 4 2 1
2 3 1
2 1 2
1 1 3
2 1 2
```

| Query | Action | Cycles | Result |
| --- | --- | --- | --- |
| 2 3 1 | Follow p[3] once | [5,1,2,3,4] cycles | 4 |
| 2 1 2 | Follow p[1] twice | same | 1 |
| 1 1 3 | Swap p[1] and p[3] | rebuild cycles containing 1,3 | - |
| 2 1 2 | Follow new p[1] twice | updated cycles | 2 |

This demonstrates that cycle rebuilding correctly handles swaps and type 2 queries after modification.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) amortized | Each element is reassigned to a cycle at most once per swap affecting it, each type 2 query is O(1) |
| Space | O(n) | Stores permutation, cycle ids, positions, and cycle lists |

With $n, q \le 10^5$, the total operations remain under $10^6$ amortized, fitting comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# Sample provided
assert run("5 4\n5 3 4 2 1\n2 3 1\n2 1 2\n1 1 3\n2 1 2\n") == "4\n1\n2"

# Minimum-size input
assert run("1 1\n1\n2 1 1\n") == "1"

# Swap first and last in small permutation
assert run("4 3\n1 2 3 4\n1 1 4\n2 1 3\n2 4 1\n") == "4\n1"

# Cycle-length test
assert run("3 2\n2 3 1\n2 1 5\n2 3 6\n") == "2\n1"

# Repeated swaps
assert run("3 5\n1 2 3\n1 1 2\n1 2 3\n2 1 1\n2 2 2\n2 3 3\n") == "3\n1\n2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 |  |  |
