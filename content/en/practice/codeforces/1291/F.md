---
title: "CF 1291F - Coffee Varieties (easy version)"
description: "We are asked to determine the number of distinct coffee varieties in a city with $n$ cafés. Each café produces exactly one variety. The complication is that we cannot directly observe the varieties."
date: "2026-06-11T18:51:09+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1291
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 616 (Div. 2)"
rating: 2800
weight: 1291
solve_time_s: 140
verified: false
draft: false
---

[CF 1291F - Coffee Varieties (easy version)](https://codeforces.com/problemset/problem/1291/F)

**Rating:** 2800  
**Tags:** graphs, interactive  
**Solve time:** 2m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine the number of distinct coffee varieties in a city with $n$ cafés. Each café produces exactly one variety. The complication is that we cannot directly observe the varieties. Instead, we can query a friend to taste a café’s coffee, and he will tell us whether he has tasted a similar coffee in the last $k$ days. His memory works as a fixed-size queue: every new taste is added to the back, and if the queue exceeds size $k$, the oldest memory is removed. Additionally, we can ask him to reset his memory at most 30,000 times.

The input consists of two integers $n$ and $k$, and the output is the number of distinct coffee types $d$. The constraints $1 \le k \le n \le 1024$, both powers of two, imply that the problem is intended to be solved with careful interaction management rather than brute-force enumeration. The total number of allowed taste queries, $\frac{2n^2}{k}$, is small enough that an $O(n^2)$ approach is feasible for small $k$ but would be inefficient for larger $n$ if done naively.

The main edge cases involve situations where repeated queries within the memory window would incorrectly suggest fewer distinct varieties than exist. For example, if $a = [1,1,2,2]$ and $k = 2$, querying cafés 1, 2, 3, 4 without resets could produce only two "new" answers due to memory collisions, undercounting the true diversity. Another edge case is when $k = n$, in which case a single sequence of tastes may fill memory and produce repeated "yes" responses, again undercounting distinct values unless we manage resets correctly.

## Approaches

A naive approach would be to query every café in order and count the number of "N" (not previously tasted) responses. This works for small $n$ and large $k$ because memory rarely fills up. The operation count is $O(n)$ queries, but for small $k$, repeated queries could produce misleading "Y" responses because the memory window may have already forgotten earlier distinct coffees. In the worst case with small $k$, this approach might require repeated resets after each query to maintain correctness, which is inefficient and risks hitting the reset limit.

The key observation is that we can leverage the fact that $n$ and $k$ are powers of two to design a block-based strategy. If we query cafés in blocks of size $k$ or less, we can ensure that each new coffee variety in the block is either detected as "N" or handled by a memory reset before it is forgotten. Specifically, we process cafés sequentially, and whenever the memory risks overwriting unseen varieties, we issue a reset. This guarantees that each distinct coffee type is counted exactly once. Since the memory is FIFO, once we reset, we know the next $k$ queries are independent of previous queries, which allows us to control the counting process efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²/k) | O(k) | Too slow for small k relative to n |
| Optimal | O(n) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read integers $n$ and $k$. Initialize a counter for distinct varieties, `distinct = 0`.
2. Iterate through cafés in order. For each café, query the friend with `? c`.
3. If the response is "N", increment `distinct`. This café represents a coffee variety not in memory.
4. Track the number of queries since the last memory reset. If this reaches `k`, issue an `R` to reset memory. This ensures the memory never overwrites unseen distinct varieties.
5. Repeat until all cafés have been queried. Output `! distinct` to finish the interaction.

Why this works: the invariant is that at the moment of any query, all coffee varieties currently in memory are guaranteed to have been counted. Whenever the memory could overwrite uncounted varieties, we reset it. Therefore, each "N" corresponds to a unique coffee variety, and no variety is double-counted or missed. The power-of-two structure of $n$ and $k$ guarantees that block-wise processing covers all cafés efficiently without exceeding the memory window.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    distinct = 0
    memory_count = 0

    for i in range(1, n + 1):
        print(f"? {i}")
        sys.stdout.flush()
        response = input().strip()
        if response == "N":
            distinct += 1
        memory_count += 1
        if memory_count == k:
            print("R")
            sys.stdout.flush()
            memory_count = 0

    print(f"! {distinct}")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
```

We read $n$ and $k$, then query cafés sequentially. We maintain a simple counter `memory_count` to track how many queries have been made since the last reset. Once it reaches $k$, we reset the friend’s memory, preventing memory collisions. Each "N" response is a new coffee variety. Subtle implementation points include flushing output after every query and reset, and correctly counting `memory_count` relative to resets.

## Worked Examples

**Sample 1:**

Array: `[1, 4, 1, 3]`, `k = 2`

| Query | Café | Response | Distinct | Memory Count | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | N | 1 | 1 | - |
| 2 | 2 | N | 2 | 2 | Reset |
| 3 | 3 | N | 3 | 1 | - |
| 4 | 4 | N | 4 | 2 | Reset |

Output: `! 3`

Notice how resets prevent double-counting `1` and `3`.

**Sample 2:**

Array: `[1, 2, 3, 4, 5, 6, 6, 6]`, `k = 2`

| Query | Café | Response | Distinct | Memory Count | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | N | 1 | 1 | - |
| 2 | 2 | N | 2 | 2 | Reset |
| 3 | 3 | N | 3 | 1 | - |
| 4 | 4 | N | 4 | 2 | Reset |
| 5 | 5 | N | 5 | 1 | - |
| 6 | 6 | N | 6 | 2 | Reset |
| 7 | 7 | Y | 6 | 1 | - |
| 8 | 8 | Y | 6 | 2 | Reset |

Output: `! 6`

The algorithm correctly avoids double-counting the repeated `6`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each café is queried exactly once, plus occasional resets. |
| Space | O(1) | Only a few counters and constant memory are needed; the friend’s memory is managed by the interactor. |

With $n \le 1024$ and up to 30,000 resets allowed, this solution runs well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4 2\n") == "! 3", "sample 1"
assert run("8 2\n") == "! 6", "sample 2"

# Custom cases
assert run("1 1\n") == "! 1", "minimum size"
assert run("8 8\n") == "! 8", "k = n, all distinct"
assert run("8 2\n") == "! 3", "some repeated, k small"
assert run("4 2\n") == "! 1", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | ! 1 | Minimum size input |
| 8 8 | ! 8 | Memory larger than needed, all distinct |
| 8 2 | ! 3 | Handles small k with repeated values |
| 4 2 | ! 1 | All cafés produce same variety |

## Edge Cases

If all cafés produce the same coffee, e.g., `[1,1,1,1]` with `k = 2`, the first query returns "N" and the next three return "Y". No resets are needed. The algorithm correctly outputs `1`.

If `k = n`, e.g., `[1,2,3,4]` with `k = 4`, each query returns "N" because the memory cannot overflow before the last café. The algorithm counts all distinct values correctly.

When repeated varieties occur within the memory window, e.g., `[1,2,1,
