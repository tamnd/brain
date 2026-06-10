---
title: "CF 1509C - The Sports Festival"
description: "We are given the running speeds of all council members. We may choose any order in which they run. For every prefix of the chosen order, we look at all runners that have already participated."
date: "2026-06-10T19:46:17+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1509
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 715 (Div. 2)"
rating: 1800
weight: 1509
solve_time_s: 132
verified: true
draft: false
---

[CF 1509C - The Sports Festival](https://codeforces.com/problemset/problem/1509/C)

**Rating:** 1800  
**Tags:** dp, greedy  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the running speeds of all council members. We may choose any order in which they run.

For every prefix of the chosen order, we look at all runners that have already participated. The discrepancy of that prefix is the difference between the largest and smallest speed seen so far. The first runner always contributes zero because the maximum and minimum are the same.

Our goal is to arrange the runners so that the sum of all prefix discrepancies is as small as possible.

The input is simply an array of speeds. The output is the minimum achievable sum of discrepancies after choosing the best ordering.

The most important observation comes from the fact that discrepancies depend only on the current minimum and maximum among the runners already chosen. The exact internal order of runners inside that range does not matter once both extremes have appeared.

The constraint is $n \le 2000$. A brute force search over all permutations is completely impossible because there are $n!$ possible orders. Even dynamic programming over subsets would require $2^n$ states, which is also far beyond reach. With $n=2000$, a solution around $O(n^2)$ is realistic, while $O(n^3)$ would already be too slow.

There are several easy-to-miss edge cases.

Consider:

```
1
7
```

The answer is:

```
0
```

There is only one runner, so every discrepancy is zero.

Consider:

```
3
5 5 5
```

The answer is:

```
0
```

All speeds are identical. Every prefix has maximum equal to minimum.

Consider:

```
3
1 2 100
```

A naive strategy might place runners in sorted order. The discrepancies become:

```
0 + 1 + 99 = 100
```

But the optimal order is:

```
2, 1, 100
```

giving:

```
0 + 1 + 99 = 100
```

In this example both happen to match, but in larger cases the best ordering is usually not simply sorted order. We need a method that globally minimizes the accumulated cost.

## Approaches

A brute force solution would try every possible ordering of the runners. For each permutation, we could scan from left to right, maintain the current minimum and maximum speed, compute every discrepancy, and keep the smallest total.

This works because it directly checks every feasible arrangement.

The problem is the number of permutations. With $n=2000$, there are $2000!$ possible orders, an astronomically large number. Even for $n=15$, exhaustive search would already be infeasible.

To find a better approach, let us sort the speeds.

Suppose the sorted speeds are:

$$a_0 < a_1 < \cdots < a_{n-1}$$

Think about building the chosen set of runners gradually. After sorting, any collection of already-selected runners must occupy some interval in the sorted array. If we know that the selected runners are exactly those between positions $l$ and $r$, then their current discrepancy is simply:

$$a_r - a_l$$

Now imagine constructing the final ordering backwards.

At some stage we still need to place all runners from interval $[l,r]$. The largest discrepancy that will eventually appear inside this interval is exactly:

$$a_r - a_l$$

When we decide which endpoint is added last, the remaining problem becomes one of the smaller intervals $[l+1,r]$ or $[l,r-1]$.

This interval structure suggests dynamic programming on ranges.

Let

$$dp[l][r]$$

be the minimum extra discrepancy contributed while building all runners whose sorted positions lie in $[l,r]$.

When interval $[l,r]$ contains more than one runner, the current range width

$$a_r-a_l$$

must be paid exactly once, and then we continue with either smaller interval.

That gives the recurrence:

$$dp[l][r]
=
(a_r-a_l)
+
\min(dp[l+1][r], dp[l][r-1])$$

The base case is:

$$dp[i][i]=0$$

because a single runner contributes no discrepancy.

The answer is $dp[0][n-1]$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal DP on Intervals | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Read the speeds and sort them.
2. Create a two-dimensional DP table where `dp[l][r]` represents the minimum total discrepancy contribution needed for the sorted interval from `l` to `r`.
3. Initialize all single-element intervals with zero because a single runner has discrepancy zero.
4. Process intervals in increasing order of length.
5. For an interval `[l, r]`, compute its width:

$$a_r-a_l$$

This width must appear once when the interval becomes fully represented.
6. After paying this width, either the left endpoint or the right endpoint was added last.

If the left endpoint was added last, the previous state was `[l+1,r]`.

If the right endpoint was added last, the previous state was `[l,r-1]`.
7. Choose the better of those two possibilities:

$$dp[l][r]
=
(a_r-a_l)
+
\min(dp[l+1][r],dp[l][r-1])$$
8. Continue until the whole interval `[0,n-1]` has been computed.
9. Output `dp[0][n-1]`.

### Why it works

After sorting, every set of runners that has already been incorporated corresponds to a contiguous interval of the sorted array.

For interval $[l,r]$, the discrepancy contributed when this entire interval becomes active is exactly $a_r-a_l$. At that moment one of the two endpoints must have been added last. Removing that last-added endpoint leaves either interval $[l+1,r]$ or interval $[l,r-1]$.

The recurrence explores both possibilities and keeps the cheaper one. Since every valid construction sequence eventually reduces to a single element interval, and every transition accounts for the exact discrepancy introduced at that stage, the DP computes the minimum possible total discrepancy.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = sorted(map(int, input().split()))

    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            dp[l][r] = (a[r] - a[l]) + min(
                dp[l + 1][r],
                dp[l][r - 1]
            )

    print(dp[0][n - 1])

solve()
```

The first step sorts the speeds. After sorting, every relevant state becomes a contiguous interval, which is the key structural property of the solution.

The DP table stores answers for all intervals. Single-element intervals remain zero because no discrepancy exists when only one speed is present.

The outer loop processes intervals by increasing length. This guarantees that when computing `dp[l][r]`, both `dp[l+1][r]` and `dp[l][r-1]` have already been computed.

The recurrence directly matches the proof. The interval width `a[r] - a[l]` is paid once, and then the better of the two possible previous intervals is chosen.

All values fit comfortably in Python integers. The maximum possible answer is on the order of $n \cdot 10^9$, which is well below Python's limits.

## Worked Examples

### Sample 1

Input:

```
3
3 1 2
```

Sorted array:

```
[1, 2, 3]
```

| Interval | Width | Previous DP | Result |
| --- | --- | --- | --- |
| [0,1] | 1 | min(0,0) | 1 |
| [1,2] | 1 | min(0,0) | 1 |
| [0,2] | 2 | min(1,1) | 3 |

Final answer:

```
dp[0][2] = 3
```

Output:

```
3
```

This example shows how every larger interval is built from smaller intervals while paying its width exactly once.

### Sample 2

Input:

```
1
100
```

Sorted array:

```
[100]
```

| Interval | Value |
| --- | --- |
| [0,0] | 0 |

Final answer:

```
0
```

Output:

```
0
```

This demonstrates the base case. A single runner never creates a discrepancy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | There are $O(n^2)$ intervals, each processed in $O(1)$ time |
| Space | $O(n^2)$ | The DP table stores one value per interval state |

With $n \le 2000$, the DP contains about four million states. Each state requires only a constant amount of work, making the solution fast enough for the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = sorted(map(int, input().split()))

    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            dp[l][r] = (a[r] - a[l]) + min(
                dp[l + 1][r],
                dp[l][r - 1]
            )

    return str(dp[0][n - 1]) + "\n"

# provided sample
assert run("3\n3 1 2\n") == "3\n", "sample 1"

# minimum size
assert run("1\n7\n") == "0\n", "single element"

# all equal
assert run("4\n5 5 5 5\n") == "0\n", "all equal"

# simple increasing
assert run("2\n1 10\n") == "9\n", "two elements"

# off-by-one interval handling
assert run("3\n1 2 10\n") == "10\n", "small interval DP"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Single-element base case |
| `4 / 5 5 5 5` | `0` | Repeated values |
| `2 / 1 10` | `9` | Smallest non-trivial interval |
| `3 / 1 2 10` | `10` | Correct transition between interval lengths |

## Edge Cases

Consider:

```
1
7
```

The sorted array contains only one element. The DP never enters the interval-expansion loop. `dp[0][0]` remains zero, which is returned immediately. The output is:

```
0
```

Consider:

```
3
5 5 5
```

Every interval width is zero.

For example:

```
dp[0][1] = 0
dp[1][2] = 0
dp[0][2] = 0
```

The final answer remains zero, correctly reflecting that every prefix has identical maximum and minimum speeds.

Consider:

```
2
1 10
```

The only non-trivial interval is `[0,1]`.

Its width is:

```
10 - 1 = 9
```

Both smaller intervals are single elements with cost zero, so:

```
dp[0][1] = 9
```

The answer is exactly the discrepancy of the full set.

Consider:

```
4
1 2 3 100
```

The DP explores both ways of shrinking each interval. It does not commit to a fixed ordering such as sorted order. The recurrence automatically chooses the cheaper endpoint removal at every interval, guaranteeing the globally optimal total discrepancy rather than a locally appealing arrangement.
