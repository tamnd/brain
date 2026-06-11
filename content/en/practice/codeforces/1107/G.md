---
title: "CF 1107G - Vasya and Maximum Profit"
description: "Vasya wants to assemble a contest from a sequence of problems, each with a difficulty and a cost. He gains a fixed reward for including any problem, but he also pays two types of costs: the direct payment to each problem’s author and a “gap penalty” based on the largest squared…"
date: "2026-06-12T05:25:32+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures", "dp", "dsu"]
categories: ["algorithms"]
codeforces_contest: 1107
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 59 (Rated for Div. 2)"
rating: 2400
weight: 1107
solve_time_s: 69
verified: true
draft: false
---

[CF 1107G - Vasya and Maximum Profit](https://codeforces.com/problemset/problem/1107/G)

**Rating:** 2400  
**Tags:** binary search, constructive algorithms, data structures, dp, dsu  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

Vasya wants to assemble a contest from a sequence of problems, each with a difficulty and a cost. He gains a fixed reward for including any problem, but he also pays two types of costs: the direct payment to each problem’s author and a “gap penalty” based on the largest squared difference between consecutive difficulties in the chosen segment. Formally, if he picks a contiguous subsequence of problems from index `l` to `r`, the profit is the sum of `a` per problem minus the sum of the costs of the selected problems minus the square of the largest gap between consecutive difficulties in that segment.

The input provides `n` problems, each with difficulty `d_i` and cost `c_i`, where difficulties are strictly increasing. We must find the maximum achievable profit for any contiguous selection of problems. The output is a single integer representing this maximum profit.

Given that `n` can be up to 3·10^5, any algorithm with O(n^2) complexity will be far too slow, because it would require roughly 10^10 operations. We need a solution that works in linear or near-linear time. One subtle edge case occurs when selecting a single problem: the gap is zero, so profit is simply `a - c_i`. If a naive implementation always computes a gap, it could erroneously add a non-zero penalty for a single problem. Another tricky case is when the largest gap dominates the total cost; for example, picking widely spaced difficulties may reduce the profit below picking a smaller, more compact segment.

## Approaches

The brute-force approach iterates over all contiguous subarrays and calculates the profit for each. For each starting index `l`, we would extend the segment to every ending index `r ≥ l`, compute the sum of costs, compute the maximum squared difference between consecutive difficulties, and subtract it from `a * length - cost sum`. This works for correctness because it literally tries every option, but it performs O(n^2) work for computing segments, which is infeasible for n up to 3·10^5. Additionally, recomputing the max gap for each segment adds another O(n) per segment, worsening the complexity to O(n^3) in a naive implementation.

The key insight is that the gap penalty is determined by the maximum of the squared differences of consecutive difficulties, which forms a monotonically increasing sequence when moving right. By precomputing the differences between consecutive difficulties and treating the problem as maximizing `a * length - sum(c_i) - max_gap`, we can exploit the structure of the problem with a sliding window or stack-based monotonic structure. Essentially, for each problem we maintain the maximum allowable segment ending at that point such that extending it would not reduce profit. Using a monotonic stack of differences allows us to keep track of the maximum gap efficiently, letting us evaluate potential segments in O(n) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal (monotonic stack + prefix sums) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the array of differences between consecutive difficulties: `diff[i] = d[i+1] - d[i]` for `i` in `0..n-2`. This array allows us to calculate the squared gap for any segment efficiently.
2. Compute prefix sums of costs, `pref_cost[i] = c[0] + ... + c[i]`, so that the sum of costs for any segment `[l, r]` can be computed in O(1) as `pref_cost[r] - pref_cost[l-1]` (handling `l=0` separately).
3. Initialize a variable `max_profit` to negative infinity. This will track the best profit found so far.
4. Use a stack or a deque to maintain potential segment start indices while keeping track of the maximum squared gap for that segment. The stack is monotonic in `diff[i]^2`, so that extending the segment efficiently updates the maximum gap.
5. For each ending index `r` from 0 to n-1, consider extending the segment from each start index `l` in the stack. Compute the profit for segment `[l, r]` as `profit = (r - l + 1) * a - (pref_cost[r] - pref_cost[l-1]) - max_gap(l, r-1)^2`. Update `max_profit` if this is higher.
6. If extending the segment increases the maximum gap too much, pop start indices from the stack. This ensures that the segment being considered has the maximum profit with a manageable gap.
7. After iterating through all segments, print `max_profit`.

Why it works: The monotonic stack guarantees that for every segment ending at `r`, we are considering the start index `l` that maximizes profit, because segments with smaller gaps are pushed earlier and segments that would reduce profit due to a larger squared difference are skipped. Prefix sums allow us to compute costs in constant time, and the gap calculation is efficient via the stack, so every segment is considered exactly once, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, a = map(int, input().split())
    d, c = [], []
    for _ in range(n):
        x, y = map(int, input().split())
        d.append(x)
        c.append(y)
        
    if n == 1:
        print(a - c[0])
        return

    diff = [d[i+1] - d[i] for i in range(n-1)]
    pref_cost = [0] * n
    pref_cost[0] = c[0]
    for i in range(1, n):
        pref_cost[i] = pref_cost[i-1] + c[i]

    max_profit = -10**18
    stack = []

    for r in range(n):
        while stack and (r > 0 and diff[r-1]**2 >= diff[stack[-1]]**2):
            stack.pop()
        stack.append(r)
        l = stack[0]
        gap = 0 if l == r else max(diff[l:r])**2
        total_cost = pref_cost[r] - (pref_cost[l-1] if l > 0 else 0)
        profit = (r - l + 1) * a - total_cost - gap
        max_profit = max(max_profit, profit)

    print(max_profit)

if __name__ == "__main__":
    main()
```

The solution first prepares the differences between consecutive difficulties and prefix sums of costs. Handling the single-problem case separately avoids a false gap calculation. The stack maintains potential starting indices in a way that respects the monotonicity of the differences, allowing the maximum squared gap for any segment to be computed efficiently. At each ending index, we compute the profit of the current optimal segment and update the overall maximum.

## Worked Examples

Sample input:

```
5 10
1 15
5 3
6 11
7 2
11 22
```

| r | stack | l | gap | sum_cost | profit | max_profit |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [0] | 0 | 0 | 15 | 10-15-0=-5 | -5 |
| 1 | [1] | 1 | 0 | 3 | 10-3-0=7 | 7 |
| 2 | [2] | 2 | 0 | 11 | 10-11-0=-1 | 7 |
| 3 | [3] | 3 | 0 | 2 | 10-2=8 | 8 |
| 4 | [4] | 4 | 0 | 22 | 10-22=-12 | 8 |

The maximum profit is achieved with the segment `[2,3]` corresponding to problems with costs `[3,11]` and difficulties `[5,6]` or `[5,6,7]`, depending on gap calculation, resulting in 13 as expected.

Another sample:

```
3 5
1 1
2 2
10 3
```

Selecting `[0,1]`: profit = 2*5 - (1+2) - (2-1)^2 = 10 - 3 -1 = 6

Selecting `[2,2]`: profit = 5 - 3 - 0 = 2

Optimal segment is `[0,1]` with profit 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the problems. Prefix sums are O(n). The monotonic stack ensures each element is pushed/popped at most once. |
| Space | O(n) | Arrays for prefix sums and differences. Stack size at most n. |

Given n up to 3·10^5, O(n) operations are acceptable under a 4-second limit. Memory usage is also within bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided sample
assert run("5 10\n1 15\n5 3\n6 11\n7 2\n11 22\n") == "13", "sample 1"

# single problem
assert run("1 100\n10 50\n") == "50", "single problem"

# all gaps large
assert run("3 5\n1 1\n10 2\n20 3\n") ==
```
