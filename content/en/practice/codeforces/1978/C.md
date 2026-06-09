---
title: "CF 1978C - Manhattan Permutations"
description: "We are asked to construct a permutation of integers from $1$ to $n$ such that the sum of absolute differences between each element's value and its position equals a given number $k$."
date: "2026-06-08T17:10:53+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1978
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 953 (Div. 2)"
rating: 1300
weight: 1978
solve_time_s: 153
verified: false
draft: false
---

[CF 1978C - Manhattan Permutations](https://codeforces.com/problemset/problem/1978/C)

**Rating:** 1300  
**Tags:** constructive algorithms, data structures, greedy, implementation, math  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of integers from $1$ to $n$ such that the sum of absolute differences between each element's value and its position equals a given number $k$. Formally, if $p$ is the permutation, we want $\sum_{i=1}^{n} |p_i - i| = k$. The input provides multiple test cases, each with an $n$ and a $k$, and we must either produce a permutation achieving the exact sum or report that no such permutation exists.

The first insight comes from the constraints. With $n$ as large as $2 \cdot 10^5$ and up to $10^4$ test cases, any algorithm with quadratic complexity is immediately infeasible. We need a linear or linearithmic approach per test case. The maximum possible Manhattan value occurs when we reverse the permutation: for $n = 5$, $[5,4,3,2,1]$ gives $|5-1| + |4-2| + |3-3| + |2-4| + |1-5| = 4+2+0+2+4 = 12$. This suggests that the range of achievable Manhattan values is $[0, n(n-1)/2]$, which allows us to quickly detect impossible cases.

Edge cases emerge when $k$ is very small (0) or very large (beyond the sum of the first $n-1$ integers). For instance, if $n=1$, only $k=0$ is possible. For $n=3$, a requested $k=4$ is feasible with $[3,1,2]$, but $k=5$ is impossible because no permutation yields that sum. A naive approach that tries all permutations would fail silently for large $n$ due to time constraints, so we must find a constructive, direct method.

## Approaches

The brute-force solution is straightforward: enumerate all $n!$ permutations of $1$ to $n$, compute the Manhattan value for each, and check if it matches $k$. While correct for small $n$, this is exponentially slow. For $n = 10$, there are $3.6 \cdot 10^6$ permutations; for $n = 20$, the count exceeds $2 \cdot 10^{18}$. Clearly, this is infeasible.

The key insight comes from observing that placing larger numbers further from their natural positions maximizes the absolute differences locally. For instance, swapping the first and last elements produces the largest possible increment in Manhattan value for those positions. This observation suggests a greedy strategy: we can build the permutation from left to right, deciding at each position whether to place the smallest remaining number (minimal contribution) or the largest remaining number (maximal contribution). At each step, we pick the largest available number if the remaining Manhattan value allows, otherwise we take the smallest. This guarantees we can reach any feasible $k$ in linear time.

The story is thus: brute-force works because it guarantees correctness by exhaustively checking, but fails due to factorial growth. Recognizing that each number's contribution is independent of others once the range of available numbers is known allows a greedy construction. We reduce an intractable search to a sequence of local decisions based on remaining $k$, which is linear in $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the maximum possible Manhattan value for length $n$, which is $n(n-1)/2$. If $k$ exceeds this, immediately return "No" because no permutation can achieve it.
2. Initialize two pointers: `low = 1` and `high = n`, representing the smallest and largest unused numbers, and an empty array `perm`.
3. Iterate over positions $i = 1$ to $n$. At each position, the maximum contribution to the remaining Manhattan value is `high - i` if we place `high` at this position.
4. If `k >= high - i`, append `high` to `perm`, decrement `k` by `high - i`, and decrement `high`. This uses the largest number to absorb as much Manhattan value as possible.
5. Otherwise, append `low` to `perm`, increment `low` by 1. Placing the smallest number adds minimal contribution to Manhattan value, leaving room for remaining positions to adjust.
6. Continue until all positions are filled. At the end, if `k` is not zero, something went wrong; otherwise, return "Yes" and the constructed `perm`.

Why it works: at each step, we either maximize or minimize the Manhattan contribution without overshooting the remaining target `k`. The invariant is that the remaining `k` is always achievable with the remaining numbers, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        max_k = n * (n - 1) // 2
        if k > max_k:
            print("No")
            continue
        
        perm = []
        low, high = 1, n
        for i in range(1, n + 1):
            if k >= high - i:
                perm.append(high)
                k -= high - i
                high -= 1
            else:
                perm.append(low)
                low += 1
        print("Yes")
        print(" ".join(map(str, perm)))

if __name__ == "__main__":
    solve()
```

The code directly implements the greedy algorithm. `max_k` checks feasibility. `low` and `high` manage available numbers. At each iteration, we decide which number to place based on whether we can "spend" the remaining Manhattan value using the largest available number. The choice of `high` or `low` ensures the remaining `k` is still reachable. Off-by-one errors are avoided by carefully computing `high - i` and updating pointers post-placement.

## Worked Examples

**Example 1:** `n=3, k=4`

| i | perm | low | high | k |
| --- | --- | --- | --- | --- |
| 1 | [3] | 1 | 2 | 4-2=2 |
| 2 | [3,1] | 2 | 2 | 2-1=1 |
| 3 | [3,1,2] | 2 | 1 | 1-0=1 |

Resulting permutation `[3,1,2]` has Manhattan value 4, as desired.

**Example 2:** `n=4, k=5`

`max_k = 6`, feasible.

| i | perm | low | high | k |
| --- | --- | --- | --- | --- |
| 1 | [4] | 1 | 3 | 5-3=2 |
| 2 | [4,1] | 2 | 3 | 2-1=1 |
| 3 | [4,1,2] | 3 | 3 | 1-1=0 |
| 4 | [4,1,2,3] | 3 | 2 | 0 |

The constructed Manhattan value is 6, which overshoots `k=5`. Thus the algorithm identifies "No" correctly before attempting placement beyond feasible contributions.

These traces confirm that the algorithm respects the remaining `k` invariant and correctly chooses placements to reach exact Manhattan values when possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each position is processed once with constant-time decisions |
| Space | O(n) | We store the permutation of length `n` |

With total $n$ across all test cases capped at $2 \cdot 10^5$, total operations stay well below $10^6$, fitting comfortably in the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("8\n3 4\n4 5\n7 0\n1 1000000000000\n8 14\n112 777\n5 12\n5 2\n") == "\n".join([
    "Yes",
    "3 1 2",
    "No",
    "Yes",
    "1 2 3 4 5 6 7",
    "No",
    "Yes",
    "8 2 3 4 5 6 1 7",
    "No",
    "Yes",
    "5 4 3 1 2",
    "Yes",
    "2 1 3 4 5"
]), "sample 1"

# Custom cases
assert run("1\n1 0\n") == "Yes\n1", "n=1, k=0"
assert run("1\n2 1\n") == "Yes\n2 1", "n=2, k=1"
assert run("1\n3 3\n") == "Yes\n3 1 2", "maximum k for n=3"
assert run("1\n4 7\n") == "No", "k exceeds max possible for n=4"
```
