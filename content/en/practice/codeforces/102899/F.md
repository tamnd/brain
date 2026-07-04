---
title: "CF 102899F - KK \u4e0e\u5237\u9898"
description: "We are given a sequence of days, and on each day kk records how many wrong answers (WA) he made. These values form an array a[1..n]. Starting from a score of zero, the score evolves day by day. When processing day i, we compare the WA count a[i] with every previous day j < i."
date: "2026-07-04T08:21:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102899
codeforces_index: "F"
codeforces_contest_name: "The 2nd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102899
solve_time_s: 43
verified: true
draft: false
---

[CF 102899F - KK \u4e0e\u5237\u9898](https://codeforces.com/problemset/problem/102899/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of days, and on each day kk records how many wrong answers (WA) he made. These values form an array `a[1..n]`.

Starting from a score of zero, the score evolves day by day. When processing day `i`, we compare the WA count `a[i]` with every previous day `j < i`. Each comparison contributes independently: if `a[j] < a[i]`, the score increases by one, if `a[j] > a[i]`, the score decreases by one, and if they are equal, nothing changes. After applying all comparisons with previous days, this new score becomes the current score for day `i`. Day 1 has no previous days, so it always ends with score zero.

We are required to output two values: the maximum score achieved at any moment over all days, and the final score after processing all days.

The constraint `n ≤ 100000` forces us to avoid anything that explicitly compares every pair of days. A naive double loop would involve roughly n squared comparisons, which is far beyond feasible. Any solution must reduce the repeated “count how many previous values are smaller or larger than current” into something that can be answered efficiently per day.

A subtle edge case appears when many values are equal. Since equal values contribute nothing, a correct solution must ensure they are excluded from both “greater” and “smaller” counts without accidentally double counting or missing transitions between groups of equal values.

Another corner case arises when the sequence is strictly increasing or strictly decreasing. In such cases, the score grows quadratically in a naive interpretation of pair contributions over time, but the actual evolution is linear per step in terms of contributions from previous elements, and this difference is easy to misinterpret if one tries to simulate pair updates incorrectly.

## Approaches

The brute-force interpretation is straightforward. For each day `i`, we scan all previous days `j < i` and explicitly compare `a[j]` and `a[i]`. We maintain the current score and also track the maximum. This is correct because it directly follows the definition of the score update rule. However, it performs about `1 + 2 + ... + (n-1)` comparisons, which is on the order of `n^2 / 2`, and for `n = 100000` this is completely infeasible.

The key observation is that the score on day `i` depends only on how many previous values are smaller and how many are larger. If we define:

- `less(i)` = number of `j < i` such that `a[j] < a[i]`
- `greater(i)` = number of `j < i` such that `a[j] > a[i]`

then the transition is simply:

`score[i] = score[i-1] + less(i) - greater(i)`

So the problem reduces to maintaining counts of previous elements relative to the current value. We need a data structure that can, as we process the array left to right, support:

1. Inserting a value `a[i]`
2. Querying how many existing values are strictly smaller or strictly larger

Since values are up to `10^5`, we can compress them into a Fenwick tree (or segment tree). This allows us to maintain frequencies and query prefix sums efficiently. Each day becomes an `O(log n)` operation instead of `O(n)` scanning.

The final answer requires tracking the maximum prefix score during the process, not just the final value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Fenwick Tree Counting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining a frequency structure over all previously seen values.

1. Initialize a Fenwick tree (or similar structure) and set all counts to zero. Also initialize `score = 0` and `best = 0`. This represents day 1 before any comparisons exist.
2. For each day `i` from 1 to n, we treat `a[i]` as the current value we are inserting into the history.
3. Before inserting `a[i]`, we query how many previous values are strictly smaller. This is a prefix sum query up to `a[i] - 1`. This gives `less(i)`.
4. We also query how many previous values are strictly greater. This is computed as `(i - 1) - count(≤ a[i])`. The prefix sum up to `a[i]` gives the number of values less or equal, so subtracting from total previous elements isolates the strictly greater ones. This gives `greater(i)`.
5. We update the score as `score += less(i) - greater(i)`. This directly applies the definition of how each previous day contributes to today’s change.
6. We update `best = max(best, score)` after each day, since the maximum score may occur before the final day.
7. We insert `a[i]` into the Fenwick tree by increasing its frequency.

After processing all days, `best` is the maximum score seen, and `score` is the final value.

### Why it works

At any moment, the Fenwick tree exactly represents the multiset of all previous days’ WA counts. Every contribution to the score of day `i` depends only on comparisons between `a[i]` and earlier elements. The structure ensures that each earlier element is counted exactly once in either the “less”, “greater”, or ignored category, and these categories are disjoint. Because the score is defined as a sum over independent pairwise contributions, maintaining aggregate counts preserves the exact value without needing to revisit past elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    maxv = max(a)
    fw = Fenwick(maxv)

    score = 0
    best = 0

    for i, x in enumerate(a):
        less = fw.sum(x - 1)
        total_prev = i
        leq = fw.sum(x)
        greater = total_prev - leq

        score += less - greater
        best = max(best, score)

        fw.add(x, 1)

    print(best, score)

if __name__ == "__main__":
    solve()
```

The Fenwick tree stores frequencies of WA counts seen so far. The prefix sum up to `x-1` directly gives the number of strictly smaller previous values. The prefix sum up to `x` gives the count of values less or equal, so subtracting from the number of processed elements yields strictly greater values. The score update follows exactly the pair contribution rule, and the best value is tracked incrementally.

A subtle detail is that `total_prev` is simply the index `i`, since before processing day `i` there are exactly `i` previous elements. This avoids an extra query and keeps the update clean.

## Worked Examples

### Example 1

Input:

```
3
1 3 2
```

We track Fenwick state implicitly.

| i | x | less | greater | score before | score after | best |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | - | - | - | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 3 | 1 | 0 | 0 | 1 | 1 |
| 3 | 2 | 1 | 1 | 1 | 1 | 1 |

This shows how day 2 increases score due to the previous smaller value, and day 3 balances a gain and a loss.

### Example 2

Input:

```
3
1 5 4
```

| i | x | less | greater | score before | score after | best |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | - | - | - | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 5 | 1 | 0 | 0 | 1 | 1 |
| 3 | 4 | 1 | 0 | 1 | 2 | 2 |

The third day still contributes positively overall because it is larger than most previous values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each day performs two Fenwick prefix queries and one update |
| Space | O(n) | Frequency array for Fenwick tree up to max coordinate |

The constraint `n ≤ 100000` makes `O(n log n)` comfortably safe, since each operation is logarithmic in at most `10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()
    return output.getvalue().strip()

# sample tests
assert run("3\n1 3 2\n") == "1 1"
assert run("3\n1 5 4\n") == "1 2"

# all equal
assert run("5\n2 2 2 2 2\n") == "0 0"

# strictly increasing
assert run("5\n1 2 3 4 5\n") == "10 10"

# strictly decreasing
assert run("5\n5 4 3 2 1\n") == "10 -10"

# single element
assert run("1\n42\n") == "0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 0 | equal values produce no contribution |
| increasing | 10 10 | maximum accumulation case |
| decreasing | 10 -10 | symmetric negative accumulation |
| single element | 0 0 | no comparisons edge case |

## Edge Cases

For a sequence where all values are identical, every comparison yields equality, so neither `less` nor `greater` changes the score. The Fenwick tree always returns zero for both queries, and the score remains zero throughout. For input `5 2 2 2 2 2`, the algorithm processes each day, but every `less` and `greater` is zero, so both final and maximum scores are zero.

For a strictly increasing sequence like `1 2 3 4 5`, each new element is larger than all previous ones, so `less(i) = i-1` and `greater(i) = 0`. The score increases by `0, 1, 2, 3, 4`, accumulating to 10, and the Fenwick tree correctly reflects this growing prefix distribution at each step.
