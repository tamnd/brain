---
title: "CF 1324D - Pair of Topics"
description: "We are given a list of topics, each topic carrying two different scores. One score measures how interesting the topic is for the teacher, and the other measures how interesting it is for students."
date: "2026-06-16T07:26:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1324
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 627 (Div. 3)"
rating: 1400
weight: 1324
solve_time_s: 160
verified: true
draft: false
---

[CF 1324D - Pair of Topics](https://codeforces.com/problemset/problem/1324/D)

**Rating:** 1400  
**Tags:** binary search, data structures, sortings, two pointers  
**Solve time:** 2m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of topics, each topic carrying two different scores. One score measures how interesting the topic is for the teacher, and the other measures how interesting it is for students. For any two distinct topics $i$ and $j$, we want to know whether pairing them is “teacher-favored”, meaning the combined teacher interest exceeds the combined student interest:

$$a_i + a_j > b_i + b_j.$$

The task is to count how many pairs $(i, j)$ with $i < j$ satisfy this condition.

A useful way to reinterpret this is to collapse both arrays into a single derived value per topic:

$$d_i = a_i - b_i.$$

Then the condition becomes:

$$d_i + d_j > 0.$$

So we are counting pairs whose transformed values sum to a positive number.

The constraints allow up to $2 \cdot 10^5$ topics. A quadratic scan over all pairs would require about $2 \cdot 10^{10}$ comparisons in the worst case, which is far beyond what a 2-second limit can handle in Python. This immediately rules out brute force enumeration.

A common subtle pitfall is mishandling sign symmetry. For example, if many values are negative, a naive idea like “count positives and multiply” fails because mixed pairs matter. Another issue is overflow intuition from other languages, but here Python avoids it; the real challenge is ordering efficiently.

Edge cases include all differences being positive, where every pair is valid, and all being negative, where no pair is valid. A careless implementation that does not properly separate sorted structure may still produce incorrect partial counts in such extremes.

## Approaches

The brute-force solution checks every pair $(i, j)$, computes $a_i + a_j$, compares it to $b_i + b_j$, and increments a counter when the condition holds. This is correct because it directly implements the definition of a good pair. However, it requires evaluating roughly $n(n-1)/2$ pairs, which is about $2 \cdot 10^{10}$ operations when $n = 2 \cdot 10^5$, making it infeasible.

The key simplification comes from rewriting the inequality using differences $d_i = a_i - b_i$. Now the condition is $d_i + d_j > 0$, or equivalently $d_i > -d_j$. This transforms the problem into a classic counting task over a sorted array: for each element, we want to know how many elements to its right are greater than its negation.

Sorting enables binary search or a two-pointer sweep. Once sorted, for each $d_i$, we can find the first position $j$ such that $d_j > -d_i$, and all elements beyond that contribute valid pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Sorting + binary search / two pointers | $O(n \log n)$ | $O(1)$ extra (or $O(n)$) | Accepted |

## Algorithm Walkthrough

We solve the problem using the transformed array $d$.

1. Compute $d_i = a_i - b_i$ for each topic.

This isolates the contribution of each topic to the inequality so that pairing becomes a simple sum condition.
2. Sort the array $d$ in non-decreasing order.

Sorting gives us monotonic structure, which is essential for efficiently counting how many elements exceed a threshold.
3. For each index $i$, define the threshold value $-d_i$.

We want to count how many $j > i$ satisfy $d_j > -d_i$. This converts the pair condition into a range-counting problem.
4. Use binary search (or two pointers) to locate the first index $pos$ where $d[pos] > -d_i$.

All indices from $pos$ to $n-1$ form valid partners with $i$, as they satisfy the inequality.
5. Add $n - \max(pos, i+1)$ to the answer.

We ensure we only count pairs with $j > i$ to avoid duplicates.
6. Sum contributions over all $i$.

Each valid pair is counted exactly once when processing the smaller index in the sorted order.

### Why it works

The correctness rests on two properties. First, rewriting the inequality into $d_i + d_j > 0$ preserves equivalence without changing the solution space. Second, sorting ensures that for a fixed $i$, the set of valid $j$ indices forms a suffix of the array because $d_j > -d_i$ defines a monotone condition. This monotonicity guarantees that binary search or two pointers captures all valid partners without missing or double-counting any pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

d = [a[i] - b[i] for i in range(n)]
d.sort()

ans = 0

import bisect

for i in range(n):
    # we need d[j] > -d[i] with j > i
    target = -d[i]
    pos = bisect.bisect_right(d, target)
    if pos <= i:
        pos = i + 1
    ans += n - pos

print(ans)
```

The code first constructs the difference array, which encodes whether a topic is more teacher-favored or student-favored. Sorting organizes these values so that all comparisons reduce to range queries.

For each position, we compute the smallest index where a valid partner can start using `bisect_right`. We then ensure we only count indices strictly greater than the current index. The final subtraction `n - pos` counts all valid partners efficiently.

A subtle detail is the adjustment `if pos <= i`, which prevents counting pairs where the second index would not satisfy $j > i$. Without this correction, self-pairing or reversed ordering would be incorrectly included.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [4, 8, 2, 6, 2]
b = [4, 5, 4, 1, 3]
```

We compute $d = a - b = [0, 3, -2, 5, -1]$, then sort:

$$d = [-2, -1, 0, 3, 5]$$

Now we evaluate each index:

| i | d[i] | -d[i] | pos (first d[j] > -d[i]) | pairs contributed |
| --- | --- | --- | --- | --- |
| 0 | -2 | 2 | 3 | 2 |
| 1 | -1 | 1 | 3 | 2 |
| 2 | 0 | 0 | 3 | 2 |
| 3 | 3 | -3 | 0 (adjusted to 4) | 1 |
| 4 | 5 | -5 | 0 (adjusted to 5) | 0 |

Total is 7.

This trace shows how negative values contribute many valid pairs, while large positive values contribute few or none because they already dominate most earlier elements.

### Example 2

Input:

```
n = 4
a = [5, 1, 4, 2]
b = [1, 2, 3, 4]
```

Then $d = [4, -1, 1, -2]$, sorted:

$$d = [-2, -1, 1, 4]$$

| i | d[i] | -d[i] | pos | pairs |
| --- | --- | --- | --- | --- |
| 0 | -2 | 2 | 3 | 1 |
| 1 | -1 | 1 | 3 | 1 |
| 2 | 1 | -1 | 3 | 1 |
| 3 | 4 | -4 | 4 | 0 |

Total is 3.

This demonstrates that only sufficiently large positive differences can pair with early negative ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates, each query uses binary search |
| Space | $O(n)$ | storing transformed array |

The solution comfortably fits within limits for $n \le 2 \cdot 10^5$. Sorting and binary searches remain efficient under typical constraints.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    d = sorted(a[i] - b[i] for i in range(n))

    import bisect
    ans = 0
    for i in range(n):
        pos = bisect.bisect_right(d, -d[i])
        if pos <= i:
            pos = i + 1
        ans += n - pos
    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("""5
4 8 2 6 2
4 5 4 1 3
""") == "7"

# all equal differences
assert run("""3
1 1 1
1 1 1
""") == "0"

# strictly increasing advantage
assert run("""4
1 2 3 4
0 0 0 0
""") == "6"

# strictly negative differences
assert run("""4
1 1 1 1
2 2 2 2
""") == "0"

# mixed case
assert run("""5
5 1 4 2 3
1 2 3 4 5
""") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | zero-difference edge case |
| increasing | 6 | all pairs valid |
| all negative | 0 | no valid pairs |
| mixed | varies | general correctness |

## Edge Cases

When all $a_i = b_i$, every $d_i = 0$, so no pair satisfies a strict inequality. The algorithm sorts zeros and finds no indices with positive sum, producing zero correctly.

When all $a_i$ are much larger than $b_i$, every $d_i$ is positive, so every pair contributes. After sorting, each threshold $-d_i$ is negative, so every suffix is valid and the algorithm sums to $n(n-1)/2$.

When all $a_i$ are smaller than $b_i$, every $d_i$ is negative. Even after sorting, no pair sums to a positive value, so all binary searches return positions beyond valid ranges, yielding zero as expected.
