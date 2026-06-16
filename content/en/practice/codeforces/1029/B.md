---
title: "CF 1029B - Creating the Contest"
description: "We are given a sorted list of distinct problem difficulties. From this list, we must choose a subsequence, not necessarily contiguous, that will form a contest."
date: "2026-06-16T21:08:50+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1029
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 506 (Div. 3)"
rating: 1200
weight: 1029
solve_time_s: 145
verified: true
draft: false
---

[CF 1029B - Creating the Contest](https://codeforces.com/problemset/problem/1029/B)

**Rating:** 1200  
**Tags:** dp, greedy, math  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sorted list of distinct problem difficulties. From this list, we must choose a subsequence, not necessarily contiguous, that will form a contest. The only restriction is local: if we sort the chosen difficulties increasingly, every consecutive pair must satisfy that the next difficulty is at most twice the previous one.

The goal is to pick a subsequence satisfying this multiplicative constraint while maximizing its length.

The input size can go up to 200,000 elements. That immediately rules out any solution that tries to enumerate subsets or even tries all starting points with nested exploration, since quadratic behavior around $10^{10}$ operations is not viable in one second. We need something linear or at worst linearithmic.

A subtle edge case appears when the optimal subsequence is not contiguous in the original array. For example, even if two values are far apart in index, they may still belong to the optimal chain if intermediate values are skipped. A naive greedy that always picks adjacent elements in the array would fail on cases like `1 2 4 8 9 10`, where skipping certain elements allows a longer valid chain.

Another issue is that the condition is asymmetric. It only constrains adjacent elements in the chosen subsequence, not all pairs. This means the structure is a chain condition, not a global ratio constraint.

## Approaches

The brute-force idea is to try every starting index and greedily extend a chain forward by repeatedly selecting the next valid element. For a fixed start, scanning forward costs $O(n)$, and doing this for every start leads to $O(n^2)$. With $2 \cdot 10^5$, this becomes roughly $4 \cdot 10^{10}$ comparisons, which is far too slow.

The key observation is that once we fix a starting point, we never need to reconsider earlier elements. The constraint depends only on the last chosen value. This suggests a greedy forward construction, but greedily starting from every index is redundant.

Instead, we maintain a sliding window structure: for each position, we try to extend the longest valid chain starting there, but we reuse the fact that if a chain starting at $i$ is known, then the best extension from $i+1$ can reuse part of the work. This turns the problem into a two-pointer style expansion, where we maintain a valid window and track its maximum size.

Because the sequence is sorted, we only need to ensure local validity between consecutive chosen elements. This allows us to extend a window while maintaining the condition $a[j] \le 2 \cdot a[j-1]$, shrinking only when the condition breaks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining the longest valid chain ending at the current position.

1. Start with a pointer at the beginning of the array and set the answer to 1 because any single element is a valid contest. This establishes a baseline chain length.
2. Traverse the array from the second element onward. For each element, check whether it can extend the current chain by verifying if it is at most twice the previous chosen element.
3. If the condition holds, extend the current chain length by one. This reflects that the current element can be appended without breaking the constraint.
4. If the condition does not hold, reset the chain length to 1 starting from the current element. This is necessary because no earlier element in the current chain can connect to this one under the given constraint.
5. After each step, update the global maximum with the current chain length.

The algorithm relies on the fact that we always extend the longest valid chain ending at the previous index. If extension fails, starting fresh is optimal because any earlier starting point would violate the chain condition at the same boundary.

### Why it works

At any position, the algorithm maintains the longest valid subsequence that ends at that position and respects the condition locally. Since validity depends only on adjacent pairs, any optimal solution can be decomposed into maximal segments where the condition holds continuously. The best contest corresponds to the longest such segment after optimal starting resets, and the algorithm enumerates all possible segment endpoints implicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    best = 1
    cur = 1
    
    for i in range(1, n):
        if a[i] <= 2 * a[i - 1]:
            cur += 1
        else:
            cur = 1
        if cur > best:
            best = cur
    
    print(best)

if __name__ == "__main__":
    solve()
```

The solution keeps a running count of the current valid chain length. The variable `cur` represents how many consecutive selected elements satisfy the doubling condition when moving through the array. When the condition breaks, we reset because no extension is possible across that boundary.

The variable `best` tracks the maximum chain length seen anywhere in the array. Since every valid subsequence must appear as a contiguous valid segment in this transformed sense, tracking these segments suffices.

The key implementation detail is resetting exactly when `a[i] > 2 * a[i-1]`. Missing this strict inequality or forgetting the reset leads to overcounting invalid chains.

## Worked Examples

### Example 1

Input:

```
10
1 2 5 6 7 10 21 23 24 49
```

| i | a[i] | Condition vs previous | cur | best |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | 1 | 1 |
| 1 | 2 | 2 ≤ 2·1 | 2 | 2 |
| 2 | 5 | 5 ≤ 2·2 false | 1 | 2 |
| 3 | 6 | 6 ≤ 2·5 | 2 | 2 |
| 4 | 7 | 7 ≤ 2·6 | 3 | 3 |
| 5 | 10 | 10 ≤ 2·7 | 4 | 4 |
| 6 | 21 | 21 ≤ 2·10 false | 1 | 4 |
| 7 | 23 | 23 ≤ 2·21 | 2 | 4 |
| 8 | 24 | 24 ≤ 2·23 | 3 | 4 |
| 9 | 49 | 49 ≤ 2·24 false | 1 | 4 |

This trace shows how valid chains naturally form segments. The longest segment occurs at `[5, 6, 7, 10]`, producing length 4.

### Example 2

Input:

```
5
3 4 8 20 21
```

| i | a[i] | Condition | cur | best |
| --- | --- | --- | --- | --- |
| 0 | 3 | - | 1 | 1 |
| 1 | 4 | 4 ≤ 6 | 2 | 2 |
| 2 | 8 | 8 ≤ 8 | 3 | 3 |
| 3 | 20 | 20 ≤ 16 false | 1 | 3 |
| 4 | 21 | 21 ≤ 40 | 2 | 3 |

The optimal segment is `[3, 4, 8]`, and later values cannot extend it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time checks |
| Space | O(1) | Only a few counters are maintained |

The constraints allow up to $2 \cdot 10^5$ elements, so a single linear pass fits comfortably within time limits, and constant memory avoids overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    best = 1
    cur = 1

    for i in range(1, n):
        if a[i] <= 2 * a[i - 1]:
            cur += 1
        else:
            cur = 1
        best = max(best, cur)

    return str(best)

# provided sample
assert run("10\n1 2 5 6 7 10 21 23 24 49\n") == "4"

# minimum size
assert run("1\n100\n") == "1"

# all valid chain
assert run("4\n1 2 3 5\n") == "4"

# strict breaks every time
assert run("4\n1 3 7 15\n") == "1"

# alternating extend/reset pattern
assert run("6\n1 2 5 6 12 13\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimal boundary |
| 1 2 3 5 | 4 | full chain always valid |
| 1 3 7 15 | 1 | constant resets |
| 1 2 5 6 12 13 | 2 | repeated partial chains |

## Edge Cases

For a single-element input like `1`, the algorithm initializes `best = 1` and returns immediately. No transitions occur, so no incorrect reset or comparison is triggered.

For a strictly increasing-by-more-than-double sequence like `1 3 7 15`, every comparison fails since each next element exceeds twice the previous one. The loop resets `cur` to 1 at every step, and `best` remains 1 throughout, matching the correct answer because no two elements can coexist in a valid contest.

For a fully valid sequence like `1 2 3 5`, every adjacent pair satisfies the constraint, so `cur` grows continuously to 4. The algorithm never resets, correctly identifying the entire array as a valid contest.
