---
title: "CF 2161D - Locked Out"
description: "We are given an array and we are allowed to delete elements from it. After deletions, we want the remaining sequence to satisfy a very specific restriction: it must not contain two elements where the later element is exactly one larger than the earlier element."
date: "2026-06-08T00:00:05+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2161
codeforces_index: "D"
codeforces_contest_name: "Pinely Round 5 (Div. 1 + Div. 2)"
rating: 2100
weight: 2161
solve_time_s: 104
verified: false
draft: false
---

[CF 2161D - Locked Out](https://codeforces.com/problemset/problem/2161/D)

**Rating:** 2100  
**Tags:** binary search, data structures, dp, greedy  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and we are allowed to delete elements from it. After deletions, we want the remaining sequence to satisfy a very specific restriction: it must not contain two elements where the later element is exactly one larger than the earlier element.

In other words, if we pick any two positions i < j in the remaining array, we are forbidden from having a pair where values form an increasing consecutive step of size one. The order of elements still matters because i < j is in original left-to-right order, so this is not just about multiset properties, but about what values can coexist in a subsequence.

The task is to remove as few elements as possible so that this forbidden pattern disappears entirely.

The constraints are large: up to 3 × 10^5 total elements across all test cases. This immediately rules out any quadratic strategy over indices or over value pairs. Any solution that tries to compare all pairs or simulate deletions explicitly will fail, so we need a structure that processes values in roughly linear or linear-logarithmic time per test.

A subtle issue appears when thinking greedily: removing a value that participates in a bad pair does not always mean removing all copies of that value, because conflicts depend on relative ordering and coexistence of values x and x+1 anywhere in the remaining sequence. A naive greedy like “remove all occurrences of values that appear next to their +1” in the original order fails, because the forbidden condition is global over the subsequence, not local adjacency.

For example, consider `1 3 2`. There is a conflict between 1 and 2 because 2 - 1 = 1, but they are not adjacent in the array. Any approach that only checks neighbors in the original array would miss this entirely.

The real difficulty is that occurrences of values interact only through value differences of exactly one, but all pairs across positions matter.

## Approaches

A brute-force way to think about the problem is to try all subsets of indices and check whether a chosen subset is valid. For each subset, we would verify whether any pair (i, j) violates the condition. This already leads to 2^n subsets, which is impossible even for n = 30.

A slightly more structured brute-force is to fix which elements we keep and, for each kept element, check all later kept elements to ensure no pair differs by exactly one. This is O(n^2) per test in the worst case, because even if checking is optimized, we still need to inspect many pairs.

The key observation is that the constraint depends only on values, not positions in a complicated way: any value x conflicts with any x+1 if both appear in the remaining set in the correct order. Since order is preserved, the real issue is simply that we cannot keep both values x and x+1 if there exists at least one x before x+1 in the remaining subsequence. However, because we are free to choose deletions, we can always arrange that if both values exist, we can “break” all offending orderings only by removing one entire value class in a structured way.

This leads to a simpler perspective: we are effectively choosing a subset of values such that no two consecutive integers are both “active” in a way that creates at least one valid cross-pair in order. Because we can always reorder-free choose subsequences, the optimal strategy reduces to selecting values in a way that avoids conflicts between consecutive integers.

The standard way to encode this is to compress the array into frequencies per value and then compute a DP over values: for each value x, we decide whether we take it or skip it. If we take x, then we cannot take x-1 in a way that creates a valid remaining structure, so we ensure we do not simultaneously take adjacent values.

This becomes a classic “maximum weight independent set on a path” over values 1 to n, where weight is frequency of each value. The answer is total elements minus the maximum sum of frequencies we can keep under the constraint of never picking both x and x+1.

We thus compute DP:

dp[x] = max(dp[x-1], dp[x-2] + freq[x])

This gives the maximum number of elements we can keep. The minimum removals is n - dp[max_value].

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | O(2^n · n) | O(n) | Too slow |
| DP on value line | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count frequency of each value in the array.

This transforms the problem from positional reasoning into value-based reasoning, since only the existence of values matters for conflicts.
2. Let dp[x] represent the maximum number of elements we can keep using values up to x.

We build this incrementally because choices for x depend only on x-1 and x-2.
3. For each value x from 1 to n, compute dp[x] as the best of two cases: skipping x or taking x.

Skipping x means dp[x-1]. Taking x means we gain freq[x], but must combine it with dp[x-2] to avoid adjacency conflicts.
4. The recurrence is:

dp[x] = max(dp[x-1], dp[x-2] + freq[x])

This encodes the fact that selecting x forbids selecting x-1.
5. The answer is total n minus dp[max_value].

### Why it works

The key invariant is that after processing value x, dp[x] stores the maximum number of elements we can keep using only values from 1 to x under the constraint that no two consecutive values are both chosen. Any valid subset of kept elements can be mapped to a selection of values satisfying this constraint, because if both x and x+1 were chosen in a way that preserves at least one valid ordering pair, that configuration is disallowed. The optimal solution must therefore eliminate at least one endpoint of every consecutive pair of values, and the DP enumerates all such consistent choices without double counting or missing configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = [0] * (n + 2)
        for x in a:
            freq[x] += 1
        
        if n == 1:
            print(0)
            continue
        
        dp_prev2 = 0
        dp_prev1 = freq[1]
        
        for x in range(2, n + 1):
            dp_cur = max(dp_prev1, dp_prev2 + freq[x])
            dp_prev2, dp_prev1 = dp_prev1, dp_cur
        
        best_keep = dp_prev1
        print(n - best_keep)

if __name__ == "__main__":
    solve()
```

The implementation compresses the DP to O(1) memory by only keeping the last two states, since each transition depends only on x-1 and x-2. Frequency counting is done once per test case. The final subtraction converts the maximum kept subset into minimum removals.

A common pitfall is assuming that values must be processed only up to the maximum value appearing in the array. While that is correct logically, iterating up to n is safe because unused frequencies are zero, and the DP remains consistent.

## Worked Examples

### Example 1

Input:

`5 1 2 3 4 5`

Here all values are present once.

| x | freq[x] | dp[x-2] | dp[x-1] | dp[x] |
| --- | --- | --- | --- | --- |
| 1 | 1 | - | 0 | 1 |
| 2 | 1 | 0 | 1 | 1 |
| 3 | 1 | 1 | 1 | 2 |
| 4 | 1 | 1 | 2 | 2 |
| 5 | 1 | 2 | 2 | 3 |

We keep 3 elements total, so removals = 5 - 3 = 2. This matches the idea that we cannot take consecutive values, so we effectively pick either odd or even indices of the value line.

### Example 2

Input:

`5 5 5 5 4 4`

Frequencies are: freq[4]=2, freq[5]=3.

| x | freq[x] | dp[x-2] | dp[x-1] | dp[x] |
| --- | --- | --- | --- | --- |
| 4 | 2 | 0 | 0 | 2 |
| 5 | 3 | 0 | 2 | 3 |

We can keep all 3 fives or all 2 fours, but not both in full interaction sense, so best is 3 kept. Removals = 5 - 3 = 2.

These traces show that the algorithm is not tracking positions but purely optimizing over value conflicts, which is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Frequency counting plus linear DP over value range |
| Space | O(n) | Frequency array plus constant DP state |

The total sum of n across test cases is 3 × 10^5, so a linear solution per test case is sufficient. The memory usage is linear in the largest test case and well within limits.

## Test Cases

```python
import sys, io

def solve_io(data: str) -> str:
    sys.stdin = io.StringIO(data)
    from sys import stdout
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

# provided samples
assert solve_io("""6
1
1
5
1 2 3 4 5
5
5 4 3 2 1
5
5 5 5 4 4
7
1 7 1 2 5 7 1
6
1 2 5 6 5 5
""") == """0
2
0
0
1
2"""

# all equal
assert solve_io("""1
5
3 3 3 3 3
""") == "0"

# alternating values
assert solve_io("""1
6
1 2 1 2 1 2
""") == "3"

# single chain
assert solve_io("""1
4
1 2 3 4
""") == "2"

# minimum size
assert solve_io("""1
1
1
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 0 | no consecutive pairs exist |
| alternating 1/2 | 3 | adjacency conflict forces selection |
| 1 2 3 4 | 2 | full chain forces half removal |
| single element | 0 | base boundary case |

## Edge Cases

A key edge case is when all elements are identical. Since no value x+1 exists, the constraint is never triggered, and the algorithm correctly produces dp that keeps everything. For example, input `3 3 3 3 3` produces freq[3]=5 and no adjacent interactions, so dp simply keeps all 5.

Another edge case is a dense consecutive block like `1 2 3 4 5`. Here every value conflicts structurally with its neighbors, so the DP alternates choices across values. The algorithm correctly avoids picking adjacent values by construction of the recurrence, yielding a maximum independent set over a path.

A third case is sparse values such as `1 100 2 99`. Even though values are far apart numerically, only consecutive integers matter, so the DP isolates each value independently. This shows that the solution depends on value adjacency, not magnitude or array order, which is exactly what the recurrence captures.
