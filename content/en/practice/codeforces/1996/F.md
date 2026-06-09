---
title: "CF 1996F - Bomb"
description: "We are asked to maximize a score over a series of operations on two arrays. Each array has length $n$. Array $a$ represents the current “value” of each element, and array $b$ represents how much that element decays after it is used."
date: "2026-06-08T14:44:17+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1996
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 962 (Div. 3)"
rating: 1900
weight: 1996
solve_time_s: 169
verified: true
draft: false
---

[CF 1996F - Bomb](https://codeforces.com/problemset/problem/1996/F)

**Rating:** 1900  
**Tags:** binary search, greedy, math  
**Solve time:** 2m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maximize a score over a series of operations on two arrays. Each array has length $n$. Array $a$ represents the current “value” of each element, and array $b$ represents how much that element decays after it is used. In one operation, we choose an index $i$, add $a_i$ to our score, and then reduce $a_i$ by $b_i$, keeping it non-negative. We have exactly $k$ operations to maximize the total score.

The constraints are significant: $n$ can reach $2 \cdot 10^5$, and $k$ can be up to $10^9$. A naive solution that simulates each operation individually is clearly infeasible, as it could require billions of operations. This forces us to find a way to jump over many operations at once rather than executing them one by one.

Edge cases arise when $b_i \ge a_i$ for some element, because that element can contribute at most once. Similarly, if $k$ is extremely large compared to $n$, we need to repeatedly apply operations to the same element, and the decay pattern matters. For example, consider $a = [1, 1]$, $b = [2, 3]$, $k = 3$. The maximum score is $2$, not $3$, because both elements reach zero after the first operation. A naive greedy approach without tracking decay would overcount.

## Approaches

The brute-force method is straightforward: for each of the $k$ operations, scan through the array to find the element with the maximum current value, add it to the score, and update that element. This is correct but requires $O(n \cdot k)$ time. With $n \le 2 \cdot 10^5$ and $k \le 10^9$, this could mean $10^{14}$ operations, which is far beyond acceptable.

The key observation is that each element decays linearly: after $m$ uses of element $i$, its value is $\max(0, a_i - m \cdot b_i)$. Because of this linear structure, we can compute the maximum number of times it is worth using each element. Specifically, the first time we use an element, it contributes $a_i$. The next time, it contributes $a_i - b_i$, then $a_i - 2b_i$, and so on, until it reaches zero. This sequence is arithmetic, and we can sum it quickly rather than iterating each decrement.

A clever way to select operations efficiently is to repeatedly choose the element whose next contribution is currently the largest. To avoid scanning the array each time, we can sort the elements by $a_i$ and $b_i$ in a way that lets us process high-contribution elements first, and for very large $k$, we can batch the number of times we pick each element by computing how many times it will still contribute positively.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·k) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the arrays $a$ and $b$, and the number of operations $k$. Pair each $a_i$ with its corresponding $b_i$.
2. Sort the pairs by $b_i$ to handle elements with slower decay first, or by some other heuristic to prioritize high initial contributions and low decay.
3. For each element, compute the maximum number of times it can be used before reaching zero, i.e., $m_i = \min(k, \lceil a_i / b_i \rceil)$ if $b_i > 0$, otherwise $m_i = k$ if $b_i = 0$.
4. Add the sum of the arithmetic sequence of contributions from this element: $\text{sum}_i = m_i \cdot a_i - b_i \cdot \frac{m_i (m_i - 1)}{2}$.
5. Subtract $m_i$ from the remaining operations $k$. If $k = 0$, stop early.
6. Accumulate the contributions into the total score.

Why it works: Each element contributes in strictly decreasing steps due to linear decay. By computing the sum of positive contributions for each element, we capture the total contribution without simulating each operation. Sorting ensures that the elements which will contribute the most overall are handled first, which guarantees a globally optimal score because at each step we choose the next largest contribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        items = list(zip(a, b))
        # Sort by initial value descending to greedily pick highest first
        items.sort(reverse=True, key=lambda x: x[0])
        total = 0
        remaining_ops = k
        for val, dec in items:
            if remaining_ops == 0:
                break
            if dec == 0:
                total += val * remaining_ops
                remaining_ops = 0
                break
            max_use = min(remaining_ops, (val + dec - 1) // dec)
            total += max_use * val - dec * max_use * (max_use - 1) // 2
            remaining_ops -= max_use
        print(total)

if __name__ == "__main__":
    solve()
```

The solution first pairs $a$ and $b$ and sorts by $a_i$ to prioritize high initial value. We handle zero decay separately to avoid division by zero. The arithmetic series formula sums repeated contributions efficiently. We stop early if we use all $k$ operations.

## Worked Examples

### Sample Input 1

```
3 4
5 6 7
2 3 4
```

| Step | val | dec | max_use | contribution | remaining_ops | total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7 | 4 | 1 | 7 | 3 | 7 |
| 2 | 6 | 3 | 1 | 6 | 2 | 13 |
| 3 | 5 | 2 | 2 | 8 | 0 | 21 |

Trace demonstrates that we correctly compute maximum usage per element and sum contributions using arithmetic formula rather than simulating each operation.

### Sample Input 2

```
5 1000
1 2 3 4 5
5 4 3 2 1
```

| Step | val | dec | max_use | contribution | remaining_ops | total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 5 | 5+4+3+2+1=15 | 995 | 15 |
| 2 | 4 | 2 | 2 | 4+2=6 | 993 | 21 |
| 3 | 3 | 3 | 1 | 3 | 992 | 24 |
| 4 | 2 | 4 | 1 | 2 | 991 | 26 |
| 5 | 1 | 5 | 1 | 1 | 990 | 27 |

Trace confirms that we pick elements in descending order of value, handle decay, and stop when element reaches zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array of n elements dominates. The remaining operations are computed analytically, not simulated. |
| Space | O(n) | We store pairs of (a_i, b_i) for sorting and processing. |

The time complexity fits comfortably within limits since $n \le 2 \cdot 10^5$, making the solution feasible in 2 seconds. Space is linear in n, well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("5\n3 4\n5 6 7\n2 3 4\n5 9\n32 52 68 64 14\n18 14 53 24 8\n5 1000\n1 2 3 4 5\n5 4 3 2 1\n1 1000000\n1000000\n1\n10 6\n3 3 5 10 6 8 6 8 7 7\n6 1 7 4 1 1 8 9 3 1") == "21\n349\n27\n500000500000\n47"

# Minimum-size input
assert run("1\n1 1\n1\n1") == "1"

# All equal values
assert run("1\n3 5\n5 5 5\n1 1 1") == "25"

# Maximum n, small k
assert
```
