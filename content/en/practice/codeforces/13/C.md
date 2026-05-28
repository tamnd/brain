---
title: "CF 13C - Sequence"
description: "We are given an array of integers, and we may repeatedly increment or decrement any element by one. Every such change co"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 13
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 13"
rating: 2200
weight: 13
solve_time_s: 136
verified: false
draft: false
---

[CF 13C - Sequence](https://codeforces.com/problemset/problem/13/C)

**Rating:** 2200  
**Tags:** dp, sortings  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and we may repeatedly increment or decrement any element by one. Every such change costs one operation. The goal is to transform the array into a non-decreasing sequence while spending the minimum total cost.

Another way to phrase the task is this: we want to build a new array `b` such that

$$b_1 \le b_2 \le \dots \le b_n$$

and the total modification cost

$$\sum |a_i - b_i|$$

is as small as possible.

The input size immediately shapes the solution space. The array length can reach 5000, which is too large for anything exponential or cubic with large constants. A naive search over all possible target arrays is impossible because the values themselves can be as large as $10^9$. Even trying every integer in a range is hopeless.

At the same time, $n = 5000$ is small enough for an $O(n^2)$ dynamic programming solution. A clean $O(n^2)$ implementation with simple transitions comfortably fits inside the time limit.

The most dangerous part of this problem is that the optimal final values are not obvious. A greedy strategy that fixes local inversions can fail badly.

Consider this example:

```
3
10 1 10
```

The best answer is `9`, by transforming the array into:

```
1 1 10
```

or

```
10 10 10
```

A greedy approach that only repairs adjacent violations may produce a larger cost because changing one element affects future constraints.

Another subtle case is when the sequence is strictly decreasing:

```
4
4 3 2 1
```

The optimal answer is `4`, achieved with:

```
2 2 2 2
```

A careless implementation might only try target values already appearing in the same order, which misses better balanced solutions.

Large negative values are also important:

```
3
-1000000000 0 -1000000000
```

The correct answer is `1000000000`.

The optimal transformation is:

```
-1000000000 -1000000000 -1000000000
```

Using 32-bit integers overflows here, so the implementation must use Python integers or 64-bit types in other languages.

## Approaches

The brute-force idea is conceptually simple. We try every possible non-decreasing target array and compute its cost. The difficulty is that the values are unbounded. Even restricting ourselves to values appearing in the array still leaves exponentially many sequences.

Suppose we compressed the possible target values into $m$ candidates. There are still roughly $m^n$ non-decreasing assignments to consider. With $n = 5000$, this is completely impossible.

The key observation is that the exact numeric values are less important than their relative ordering. If we sort all array values, then every optimal target array can be chosen from this sorted list.

Why is this true?

Suppose some optimal target value lies between two existing numbers. Moving it to the nearest existing value cannot increase the total absolute difference cost, because absolute value is piecewise linear. This lets us discretize the state space.

Now the problem becomes:

Choose a non-decreasing sequence from the sorted candidate values while minimizing total adjustment cost.

This structure naturally suggests dynamic programming.

Let the sorted unique candidate values be:

$$v_1 \le v_2 \le \dots \le v_m$$

Define:

$$dp[i][j]$$

as the minimum cost to process the first `i` elements such that the `i`-th transformed value equals `v[j]`.

The non-decreasing constraint means that previous choices must satisfy:

$$v[k] \le v[j]$$

so the transition is:

$$dp[i][j] = |a_i - v_j| + \min_{k \le j} dp[i-1][k]$$

A direct implementation of this transition is $O(nm^2)$, which becomes too slow when $m \approx n = 5000$.

The optimization comes from maintaining prefix minima. While iterating through `j`, we keep track of:

$$\min_{k \le j} dp[i-1][k]$$

in constant time per state.

That reduces the complexity to $O(nm)$, which is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal DP with Prefix Minimums | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array `a`.
2. Create a sorted copy of the array.

The sorted values become the candidate target values. Any optimal non-decreasing sequence can be represented using these values.
3. Let `vals` be this sorted array.

We do not even need to remove duplicates. Keeping duplicates does not affect correctness.
4. Define a DP array where `dp[j]` represents the minimum cost after processing the current prefix, ending with target value `vals[j]`.
5. Initialize the first row.

For the first element, the cost is simply:

$$|a[0] - vals[j]|$$
6. Process the array from left to right.

For each new element, build a new DP row.
7. Maintain a running prefix minimum while iterating through `vals`.

At position `j`, we need the minimum previous cost among all indices `0..j`. Instead of scanning repeatedly, update:

$$best = \min(best, dp[j])$$
8. Transition into the new state.

The cost becomes:

$$newdp[j] = best + |a[i] - vals[j]|$$

This guarantees the sequence remains non-decreasing because transitions only come from earlier or equal candidate values.
9. Replace the old DP row with the new one.
10. After processing all elements, the answer is the minimum value in the final DP row.

### Why it works

The DP invariant is:

$$dp[j]$$

stores the minimum cost for transforming the processed prefix into a non-decreasing sequence whose last value equals `vals[j]`.

Every valid non-decreasing sequence ending at `vals[j]` must come from some previous value `vals[k]` where `k <= j`. Taking the minimum over those states explores all legal possibilities.

The prefix minimum optimization does not change the recurrence. It only computes:

$$\min_{k \le j} dp[k]$$

incrementally instead of recomputing it every time.

Because every state transition is represented exactly once, and every illegal decreasing transition is excluded, the algorithm always produces the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    vals = sorted(a)

    dp = [abs(a[0] - v) for v in vals]

    for i in range(1, n):
        newdp = [0] * n

        best = float('inf')

        for j in range(n):
            best = min(best, dp[j])
            newdp[j] = best + abs(a[i] - vals[j])

        dp = newdp

    print(min(dp))

solve()
```

The first step constructs the sorted candidate values. These are the only values we ever assign to transformed elements.

The DP array stores the minimum achievable cost for every possible final value. Initially, only the first element matters, so the cost is just the absolute difference from each candidate.

The core optimization is the running variable `best`. Without it, each transition would require scanning all previous states:

```
min(dp[0:j+1])
```

inside the loop, producing $O(n^3)$ behavior in the worst case.

Instead, `best` always stores the minimum DP value seen so far while moving left to right. Since valid transitions only come from indices `<= j`, this exactly matches the recurrence.

One subtle point is that we sort the original array values, not the indices. The DP states represent possible assigned values, not positions.

Another detail is that duplicates are allowed in `vals`. Removing duplicates is optional. Keeping them simplifies the code and preserves correctness because repeated states behave identically.

Python integers automatically handle large values safely, so no special overflow handling is needed.

## Worked Examples

### Example 1

Input:

```
5
3 2 -1 2 11
```

Sorted candidate values:

```
[-1, 2, 2, 3, 11]
```

Initial DP row:

| Candidate | Cost |
| --- | --- |
| -1 | 4 |
| 2 | 1 |
| 2 | 1 |
| 3 | 0 |
| 11 | 8 |

Processing `2`:

| j | vals[j] | best prefix | newdp[j] |
| --- | --- | --- | --- |
| 0 | -1 | 4 | 7 |
| 1 | 2 | 1 | 1 |
| 2 | 2 | 1 | 1 |
| 3 | 3 | 0 | 1 |
| 4 | 11 | 0 | 9 |

Processing `-1`:

| j | vals[j] | best prefix | newdp[j] |
| --- | --- | --- | --- |
| 0 | -1 | 7 | 7 |
| 1 | 2 | 1 | 4 |
| 2 | 2 | 1 | 4 |
| 3 | 3 | 1 | 5 |
| 4 | 11 | 1 | 13 |

Processing `2`:

| j | vals[j] | best prefix | newdp[j] |
| --- | --- | --- | --- |
| 0 | -1 | 7 | 10 |
| 1 | 2 | 4 | 4 |
| 2 | 2 | 4 | 4 |
| 3 | 3 | 4 | 5 |
| 4 | 11 | 4 | 13 |

Processing `11`:

| j | vals[j] | best prefix | newdp[j] |
| --- | --- | --- | --- |
| 0 | -1 | 10 | 22 |
| 1 | 2 | 4 | 13 |
| 2 | 2 | 4 | 13 |
| 3 | 3 | 4 | 12 |
| 4 | 11 | 4 | 4 |

Final answer:

```
4
```

This trace shows how the DP naturally balances earlier modifications against future constraints.

### Example 2

Input:

```
4
4 3 2 1
```

Sorted candidate values:

```
[1, 2, 3, 4]
```

Initial DP:

| Candidate | Cost |
| --- | --- |
| 1 | 3 |
| 2 | 2 |
| 3 | 1 |
| 4 | 0 |

After processing all elements, the final DP row becomes:

| Final value | Total cost |
| --- | --- |
| 1 | 6 |
| 2 | 4 |
| 3 | 4 |
| 4 | 6 |

Answer:

```
4
```

The optimal transformation makes every element equal to either `2` or `3`. This example demonstrates why local fixes are insufficient. The globally optimal answer spreads the adjustment across multiple positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | There are `n` DP rows and `n` candidate values |
| Space | O(n) | Only two DP rows are stored |

With $n = 5000$, the algorithm performs about 25 million simple operations, which is acceptable in Python with careful implementation. The memory usage stays small because we only keep the current and previous DP rows.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    vals = sorted(a)

    dp = [abs(a[0] - v) for v in vals]

    for i in range(1, n):
        newdp = [0] * n

        best = float('inf')

        for j in range(n):
            best = min(best, dp[j])
            newdp[j] = best + abs(a[i] - vals[j])

        dp = newdp

    print(min(dp))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("5\n3 2 -1 2 11\n") == "4", "sample 1"

# minimum size
assert run("1\n7\n") == "0", "single element is already non-decreasing"

# already sorted
assert run("5\n1 2 3 4 5\n") == "0", "already non-decreasing"

# strictly decreasing
assert run("4\n4 3 2 1\n") == "4", "requires balanced adjustments"

# all equal
assert run("6\n9 9 9 9 9 9\n") == "0", "all equal values"

# negative values
assert run("3\n-5 -10 0\n") == "5", "handles negatives correctly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Minimum-size array |
| `1 2 3 4 5` | `0` | Already sorted sequence |
| `4 3 2 1` | `4` | Global optimum beats greedy local fixes |
| `9 9 9 9 9 9` | `0` | Duplicate values |
| `-5 -10 0` | `5` | Negative integers and absolute differences |

## Edge Cases

Consider the strictly decreasing array:

```
4
4 3 2 1
```

The algorithm does not try to repair inversions one by one. Instead, it evaluates all valid target endings simultaneously.

When processing the third and fourth elements, the DP states corresponding to target values `2` and `3` become cheapest because they balance adjustment costs across all positions.

The final answer becomes:

```
4
```

which corresponds to transformations like:

```
2 2 2 2
```

or

```
3 3 3 3
```

Now consider large negative values:

```
3
-1000000000 0 -1000000000
```

The sorted candidates are:

```
[-1000000000, -1000000000, 0]
```

The optimal DP path keeps every value at `-1000000000`.

The total cost is:

```
0 + 1000000000 + 0 = 1000000000
```

Since Python integers have arbitrary precision, the implementation safely handles this case without overflow.

Finally, consider repeated values mixed with disorder:

```
5
1 5 5 2 2
```

A greedy strategy might only decrease the `5`s or increase the `2`s locally.

The DP instead evaluates all possibilities globally. It discovers that converting the array into:

```
1 2 2 2 2
```

costs only `6`, which is optimal.

The non-decreasing invariant is maintained automatically because transitions only move forward through the sorted candidate list.
