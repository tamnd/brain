---
title: "CF 1705A - Mark the Photographer"
description: "We have a total of $2n$ people with known heights. Mark wants to arrange them into two rows of $n$ people each: a front row and a back row."
date: "2026-06-09T21:22:54+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1705
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 807 (Div. 2)"
rating: 800
weight: 1705
solve_time_s: 118
verified: true
draft: false
---

[CF 1705A - Mark the Photographer](https://codeforces.com/problemset/problem/1705/A)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a total of $2n$ people with known heights. Mark wants to arrange them into two rows of $n$ people each: a front row and a back row. The requirement is that for every position $j$ (from $1$ to $n$), the person in the back row must be at least $x$ units taller than the person directly in front.

The input consists of multiple test cases. Each test case gives $n$, $x$, and the list of $2n$ heights. The output is either "YES" if such an arrangement exists or "NO" if it does not.

The constraints are small: $n$ is at most $100$ and heights are at most $1000$. This implies that an $O(n \log n)$ sorting-based solution will be efficient enough. Edge cases include situations where all heights are equal, $x$ is larger than the difference between the tallest and shortest individuals, or when $n = 1$ (single pairs). A careless implementation might try to pair heights arbitrarily, leading to a failed solution on these minimal or equal-height cases.

For example, consider input `1 100` with heights `50 50`. A naive pairing without sorting could claim success, but the correct output is "NO" because no back row person is 100 units taller than the front.

## Approaches

The brute-force solution considers every possible subset of $n$ people for the back row and every permutation of the remaining people for the front row. For each pairing, we check if the height difference is at least $x$ for all positions. This has a complexity of $O(\binom{2n}{n} \cdot n!)$, which becomes impractical even for $n=10$.

The key observation is that we do not need to consider all permutations. To maximize the chances of meeting the height requirement, we should pair the shortest person in the front row with the shortest person in the back row that is taller than them. This naturally leads to sorting all $2n$ people by height. We can then assign the first $n$ heights to the front row and the last $n$ heights to the back row. Checking the $j$-th pair directly suffices to determine if the arrangement is possible.

This greedy approach works because once heights are sorted, any other arrangement cannot improve the minimal differences; pairing a taller back-row person with a shorter front-row person reduces the remaining back-row differences. Sorting guarantees that if the minimal condition fails for any pair in the sorted order, it cannot succeed in any other order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2n)! / (n!)²) | O(2n) | Too slow |
| Sorting + Greedy | O(n log n) | O(2n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$, $x$, and the list of $2n$ heights.
3. Sort the entire list of heights in ascending order. This ensures the smallest people are at the start, and the tallest at the end.
4. Assign the first $n$ heights to the front row and the last $n$ heights to the back row.
5. Iterate over each position $j$ from $0$ to $n-1$. Check if the height of the back row person minus the front row person is at least $x$.
6. If all differences meet or exceed $x$, print "YES"; otherwise, print "NO".

Why it works: Sorting guarantees that for every potential front-row person, the corresponding back-row person is the smallest available taller person. If this minimal configuration fails, any permutation would either decrease some differences or leave them unchanged, so no valid arrangement exists. The invariant is that the $j$-th back row height in the sorted assignment is always greater than or equal to any other possible back-row candidate for the $j$-th front row person.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    heights = list(map(int, input().split()))
    heights.sort()
    front = heights[:n]
    back = heights[n:]
    possible = True
    for j in range(n):
        if back[j] - front[j] < x:
            possible = False
            break
    print("YES" if possible else "NO")
```

This solution starts by reading input efficiently using `sys.stdin.readline`. Sorting ensures the front and back rows are chosen greedily to maximize the height differences. The loop explicitly checks each position, and an early break avoids unnecessary comparisons once a violation is detected. A subtle point is to remember that `heights[n:]` correctly slices the taller half for the back row.

## Worked Examples

### Sample 1

Input:

```
3 6
1 3 9 10 12 16
```

Sorted heights: `[1, 3, 9, 10, 12, 16]`

Front row: `[1, 3, 9]`

Back row: `[10, 12, 16]`

| j | front[j] | back[j] | back[j]-front[j] | meets x=6 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 10 | 9 | Yes |
| 1 | 3 | 12 | 9 | Yes |
| 2 | 9 | 16 | 7 | Yes |

All differences ≥ 6, output "YES".

### Sample 2

Input:

```
3 1
2 5 2 2 2 5
```

Sorted heights: `[2, 2, 2, 2, 5, 5]`

Front row: `[2, 2, 2]`

Back row: `[2, 5, 5]`

| j | front[j] | back[j] | back[j]-front[j] | meets x=1 |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 0 | No |

Fail at the first position, output "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates; iterating the pairs is O(n) |
| Space | O(n) | Two slices for front and back rows; negligible compared to input |

With $n \le 100$ and $t \le 100$, this solution performs at most $100 * 100 log 100 ≈ 70000$ operations, well within the 1s limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        heights = list(map(int, input().split()))
        heights.sort()
        front = heights[:n]
        back = heights[n:]
        possible = True
        for j in range(n):
            if back[j] - front[j] < x:
                possible = False
                break
        print("YES" if possible else "NO")
    return output.getvalue().strip()

# Provided samples
assert run("3\n3 6\n1 3 9 10 12 16\n3 1\n2 5 2 2 2 5\n1 2\n8 6") == "YES\nNO\nYES"

# Custom tests
assert run("1\n1 100\n50 50") == "NO", "equal heights cannot satisfy large x"
assert run("1\n2 0\n1 2 3 4") == "YES", "x=0 always succeeds"
assert run("1\n3 2\n1 2 3 4 5 6") == "YES", "simple increasing sequence"
assert run("1\n3 4\n1 2 3 4 5 6") == "NO", "x too large for minimal difference"
assert run("1\n1 1\n1 3") == "YES", "single pair success"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 100\n50 50` | NO | equal heights cannot satisfy large x |
| `2 0\n1 2 3 4` | YES | x=0 trivially succeeds |
| `3 2\n1 2 3 4 5 6` | YES | basic increasing sequence |
| `3 4\n1 2 3 4 5 6` | NO | x too large for minimal difference |
| `1 1\n1 3` | YES | smallest n edge case |

## Edge Cases

For equal heights with a high x, e.g., `n=1`, `x=100`, heights `[50,50]`, the algorithm sorts to `[50,50]`, assigns front = `[50]`, back = `[50]`, and
