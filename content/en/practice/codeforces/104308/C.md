---
title: "CF 104308C - Optimal Pairing"
description: "We are given several test cases. In each test case, there is an even-length array. We must partition the array into disjoint pairs so that every element belongs to exactly one pair. For each pair, its contribution to the answer is the larger of the two values inside that pair."
date: "2026-07-01T20:01:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104308
codeforces_index: "C"
codeforces_contest_name: "Mirror of Independence Day Programming Contest 2023 by MIST Computer Club"
rating: 0
weight: 104308
solve_time_s: 63
verified: true
draft: false
---

[CF 104308C - Optimal Pairing](https://codeforces.com/problemset/problem/104308/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases. In each test case, there is an even-length array. We must partition the array into disjoint pairs so that every element belongs to exactly one pair. For each pair, its contribution to the answer is the larger of the two values inside that pair. The goal is to choose the pairing strategy that minimizes the total sum of these pairwise maxima.

So the task is not about finding a single optimal match but about deciding how to group values so that large elements do not unnecessarily inflate many pair costs.

The constraints allow up to $10^5$ total elements across all test cases, with values up to $10^9$. This immediately rules out any approach that tries all pairings. The number of ways to partition $n$ elements into pairs grows super-exponentially, so even for $n = 20$ brute force is already infeasible. A valid solution must run in roughly $O(n \log n)$ or better per test case, since sorting $10^5$ elements is already near the limit of what is comfortably fast in Python.

A few edge situations are worth keeping in mind.

If all elements are equal, every pairing has identical cost, so any correct algorithm must preserve that invariance.

If the array is already sorted in decreasing order, a naive greedy like pairing first with second, third with fourth is actually optimal, but pairing first with last is disastrous because it forces the maximum element into every pair involving it indirectly through structure.

A subtle failure case for incorrect greedy strategies appears when values interleave, for example `[1, 100, 2, 99]`. Pairing extremes `(1,100)` and `(2,99)` yields cost `100 + 99 = 199`, while optimal pairing `(1,2)` and `(99,100)` yields `2 + 100 = 102`. Any strategy that does not explicitly control ordering will tend to miss this structure.

## Approaches

The brute-force idea is straightforward. We try every possible pairing of the array into $n/2$ pairs, compute the sum of maxima for each configuration, and take the minimum. This is correct because it evaluates the objective directly for every valid structure. The problem is that the number of perfect matchings on $n$ elements is $(n-1)!!$, which already becomes enormous at small $n$. For $n = 20$, this is over $10^7$ possibilities, and each evaluation costs $O(n)$, so this approach collapses immediately.

The key observation is that the cost of a pair depends only on the larger element. This means every element contributes either as a "winner" in its pair or is hidden under a larger partner. To minimize the sum, we want large elements to be used as infrequently as possible as maxima. That suggests pairing large elements with as small elements as possible, but this intuition must be made consistent globally.

Once the array is sorted, we can reason about local structure. Consider any four elements $a \le b \le c \le d$. If we pair them as $(a, d)$ and $(b, c)$, the cost is $d + c$. If we instead pair them as $(a, b)$ and $(c, d)$, the cost is $b + d$. Since $c \ge b$, the second configuration never increases cost and is strictly better unless values are equal. This exchange argument shows that crossings between small and large elements are harmful, and optimal structure collapses into adjacent pairing after sorting.

Thus the solution becomes sorting the array and pairing consecutive elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal (sorting + greedy pairing) | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the array for the current test case. The structure of the problem is fully contained within each test case, so no cross-case interaction exists.
2. Sort the array in non-decreasing order. This step exposes the natural ordering of elements so that we can reason locally about optimal pair formation.
3. Traverse the sorted array in steps of two, pairing consecutive elements. Each pair is formed as `(a[i], a[i+1])`. This pairing ensures that every smaller element is matched with the closest possible larger element, preventing large elements from being wasted on multiple pairs.
4. For each pair, add the second element (the larger one after sorting) to the answer. Since the array is sorted, `a[i+1]` is guaranteed to be the maximum of the pair.
5. Output the accumulated sum for the test case.

### Why it works

After sorting, any pairing that introduces a "crossing" structure, where a smaller element is paired with a very large one while another pair contains intermediate values, can be locally improved by swapping endpoints. Each swap reduces or preserves total cost because it prevents a larger element from being overshadowed unnecessarily. Repeated application of this exchange eliminates all non-adjacent pairings, leaving only consecutive pairing as a stable configuration. This structure ensures that every element except those in even positions contributes exactly once as a maximum, and these maxima are the smallest possible choices available at their pairing stage.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        ans = 0
        for i in range(1, n, 2):
            ans += a[i]
        out.append(str(ans))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution is structured around sorting and a linear scan. The key implementation detail is that we sum every second element starting from index 1 after sorting, since those are the elements acting as maxima in each optimal pair. Using fast I/O is necessary because the total input size can reach $10^5$ integers across test cases.

## Worked Examples

### Example 1

Input:

`[1, 100, 2, 99]`

After sorting, the array becomes `[1, 2, 99, 100]`.

| Step | Array | Pair formed | Pair cost | Running sum |
| --- | --- | --- | --- | --- |
| 1 | [1, 2, 99, 100] | (1,2) | 2 | 2 |
| 2 | [1, 2, 99, 100] | (99,100) | 100 | 102 |

The total is 102, showing that adjacent pairing avoids wasting large values across different pairs.

### Example 2

Input:

`[5, 5, 5, 5, 1, 1]`

Sorted array: `[1, 1, 5, 5, 5, 5]`

| Step | Array | Pair formed | Pair cost | Running sum |
| --- | --- | --- | --- | --- |
| 1 | [1, 1, 5, 5, 5, 5] | (1,1) | 1 | 1 |
| 2 | [1, 1, 5, 5, 5, 5] | (5,5) | 5 | 6 |
| 3 | [1, 1, 5, 5, 5, 5] | (5,5) | 5 | 11 |

Any rearrangement produces the same or higher sum because swapping pairs cannot reduce both large elements simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ per test case | Sorting dominates, pairing is linear |
| Space | $O(1)$ extra (excluding input) | Only accumulation and in-place sort are used |

The constraints allow up to $10^5$ elements total, so sorting once per test case is well within limits. The linear scan is negligible compared to sorting.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        ans = 0
        for i in range(1, n, 2):
            ans += a[i]
        out.append(str(ans))
    print("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        from contextlib import redirect_stdout
        import io as sio
        out = sio.StringIO()
        with redirect_stdout(out):
            solve()
        return out.getvalue().strip()
    finally:
        sys.stdin = old_stdin

# sample-like test
assert run("""1
4
1 100 2 99
""") == "102"

# minimum case
assert run("""1
2
10 1
""") == "10"

# all equal
assert run("""1
6
5 5 5 5 5 5
""") == "15"

# already sorted
assert run("""1
4
1 2 3 4
""") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 4 1 100 2 99 | 102 | interleaving forces correct sorting strategy |
| 1 2 10 1 | 10 | smallest valid case |
| 1 6 all 5s | 15 | symmetry and equal-value stability |
| 1 4 1 2 3 4 | 6 | already sorted increasing order correctness |

## Edge Cases

For interleaving inputs like `[1, 100, 2, 99]`, the algorithm sorts to `[1, 2, 99, 100]` and forms pairs `(1,2)` and `(99,100)`. The second elements `2` and `100` are accumulated, giving 102. Any attempt to pair without sorting produces crossing pairs that inflate at least one large element into a higher-cost position.

For duplicate-heavy inputs like `[5, 5, 5, 5, 1, 1]`, sorting produces stable adjacency where swapping pairs does not change outcomes. The algorithm consistently assigns one copy of each pair as the maximum, and since all large elements are equal, no rearrangement can reduce the total.
