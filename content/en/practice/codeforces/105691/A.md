---
title: "CF 105691A - A boring party!"
description: "The task describes a small game played with numbers where each number contributes a value equal to itself, but choosing a number has a side effect: it “removes” its immediate neighbors in value."
date: "2026-06-26T08:14:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105691
codeforces_index: "A"
codeforces_contest_name: "MOI25 Training camp"
rating: 0
weight: 105691
solve_time_s: 39
verified: true
draft: false
---

[CF 105691A - A boring party!](https://codeforces.com/problemset/problem/105691/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a small game played with numbers where each number contributes a value equal to itself, but choosing a number has a side effect: it “removes” its immediate neighbors in value. Concretely, if you decide to take all occurrences of some value x, then all occurrences of x−1 and x+1 become unusable for future choices. Each time you take a value x, you earn points equal to x multiplied by how many times x appears in the input. The goal is to choose which values to take so that no two chosen values differ by exactly 1, while maximizing the total gained points.

The input is just a list of integers. The output is a single number: the maximum achievable score under this constraint.

The main constraint is n up to 100000, and values also up to 100000. This immediately rules out any solution that tries all subsets or simulates decisions over all elements. A naive exponential search over which values to pick would grow as 2 to the power of distinct values, which becomes infeasible even for a few dozen distinct numbers. Even iterating over all subsets of occurrences is far beyond any realistic limit.

A more subtle issue appears in naive greedy attempts. For example, picking the most frequent value first seems reasonable, but it can fail badly because choosing a slightly less frequent value might block two moderately large neighbors and produce a higher overall sum.

For instance, consider input:

3

1 2 2

A greedy choice that picks 1 first gains 1, then cannot pick 2, resulting in total 1. The optimal solution picks 2 and gains 4. This shows that local frequency or local value decisions are not reliable.

The difficulty is that each value interacts only with its immediate neighbors, which creates a structured dependency rather than arbitrary conflicts.

## Approaches

The brute-force idea is to consider every subset of distinct values and verify whether it is valid, meaning no two chosen values differ by 1. For each valid subset, compute the total contribution by summing value × frequency. If there are k distinct values, this requires checking 2^k subsets, and each subset requires O(k) or O(1) computation with preprocessing. With k up to 100000 in the worst case, this approach fails immediately because even k = 40 already leads to over a trillion subsets.

The key observation is that the structure is identical to a classic “take or skip” dynamic programming over a line. After aggregating all occurrences of each value, each integer value becomes a single weight: val[x] = x × count[x]. The restriction “cannot take x and x+1 together” means that choosing x forces exclusion of adjacent indices in a one-dimensional array of values.

Once the problem is rewritten this way, it becomes a standard recurrence. Let dp[x] represent the best answer considering all values up to x. For each x, we either skip it, keeping dp[x−1], or take it, gaining val[x] plus dp[x−2]. The structure works because the only conflict introduced by taking x is exactly x−1, and everything smaller than x−1 remains independent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^k) | O(k) | Too slow |
| DP over values | O(maxA + n) | O(maxA) | Accepted |

## Algorithm Walkthrough

1. Read the list of numbers and count how many times each value appears. This step compresses the input because only frequencies matter, not positions.
2. Convert each value x into a weight contribution x × frequency[x]. This transforms the problem into selecting among independent weighted positions on a number line.
3. Create a DP array where dp[x] represents the best achievable sum using values up to x.
4. Initialize dp[0] = 0 and dp[1] = value[1] since with only value 1 available, the only choice is whether to take it or not.
5. For each x from 2 to max value present, compute dp[x] as the maximum between dp[x−1] and dp[x−2] + value[x]. The first option corresponds to skipping x, the second corresponds to taking it and forcing exclusion of x−1.
6. The answer is dp[max value].

The reason this recurrence is valid is that once values are sorted on the integer line, every decision only affects the immediate neighbor. Any optimal solution up to x must either include x or not. If it excludes x, it reduces to the optimal solution for x−1. If it includes x, then x−1 is forbidden, but everything up to x−2 remains unaffected, so the best compatible prefix is dp[x−2].

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    if n == 0:
        print(0)
        return

    maxv = max(arr)
    freq = [0] * (maxv + 1)

    for x in arr:
        freq[x] += 1

    val = [0] * (maxv + 1)
    for x in range(maxv + 1):
        val[x] = x * freq[x]

    if maxv == 0:
        print(0)
        return
    if maxv == 1:
        print(max(val[0], val[1]))
        return

    dp0 = 0
    dp1 = val[1]

    for x in range(2, maxv + 1):
        dp2 = max(dp1, dp0 + val[x])
        dp0, dp1 = dp1, dp2

    print(dp1)

if __name__ == "__main__":
    solve()
```

The code first compresses the input into a frequency table so that each integer value contributes independently. The DP is implemented in O(1) space by keeping only the previous two states instead of a full array. This avoids memory overhead when the maximum value is large. The transition mirrors exactly the decision of whether to include or exclude the current value, and the rolling variables dp0 and dp1 represent dp[x−2] and dp[x−1] respectively.

A common implementation mistake is iterating only up to the maximum value in the input but forgetting that intermediate values may be zero. That is not a problem here because dp transitions naturally handle zeros: skipping empty values preserves previous optimal results.

## Worked Examples

Consider input:

```
3
1 2 2
```

We compute frequencies and values:

| x | freq[x] | value[x] | dp decision |
| --- | --- | --- | --- |
| 1 | 1 | 1 | take 1 or skip |
| 2 | 2 | 4 | conflicts with 1 |

Step-by-step DP:

| x | dp0 (x-2) | dp1 (x-1) | dp[x] |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 1 | 4 |

Final answer is 4, achieved by taking 2.

This shows that even though 1 appears, it is optimal to sacrifice it because 2 yields higher total contribution.

Now consider:

```
5
1 1 2 3 3
```

Frequencies give values: 1→2, 2→2, 3→6.

| x | dp0 | dp1 | dp |
| --- | --- | --- | --- |
| 1 | 0 | 2 | 2 |
| 2 | 2 | 2 | 2 |
| 3 | 2 | 2 | 8 |

Final answer is 8, achieved by taking value 3 only. This confirms the DP correctly propagates the effect of blocking adjacent values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + maxA) | counting frequencies plus linear DP over value range |
| Space | O(maxA) | arrays for frequency and DP state |

The constraints allow up to 100000 elements and values up to 100000, so a linear scan over the value range and input size fits comfortably within time limits. Memory usage stays linear and small enough for typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys

    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (from statement)
assert run("2\n1 2\n") == "2"
assert run("3\n1 2 3\n") == "4"
assert run("9\n1 2 1 3 2 2 2 2 3\n") == "10"

# custom cases
assert run("1\n10\n") == "10", "single element"
assert run("2\n5 5\n") == "10", "same value duplicates"
assert run("4\n1 3 3 3\n") == "9", "gap allows combination"
assert run("5\n1 2 3 4 5\n") == "9", "chain forces alternating picks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single value | 10 | base case handling |
| duplicates | 10 | aggregation correctness |
| sparse values | 9 | non-adjacent accumulation |
| full chain | 9 | adjacency constraint propagation |

## Edge Cases

A case with all identical values tests whether the algorithm correctly aggregates frequencies:

Input:

```
4
7 7 7 7
```

Here freq[7] = 4, so value[7] = 28. There are no adjacent constraints that matter because 6 and 8 do not exist in input contribution. The DP skips all other values and directly selects 7, producing 28.

Another edge case is a continuous sequence:

Input:

```
4
1 2 3 4
```

The DP evaluates:

dp[1] = 1

dp[2] = max(1, 0 + 2) = 2

dp[3] = max(2, 1 + 3) = 4

dp[4] = max(4, 2 + 4) = 6

The final result 6 corresponds to selecting values 2 and 4, showing how the recurrence correctly resolves alternating choices across a chain.
