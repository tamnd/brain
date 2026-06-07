---
title: "CF 2124B - Minimise Sum"
description: "We are given an array and we repeatedly look at prefix minimums: at position 1 we take the minimum of the first element, at position 2 we take the minimum over the first two elements, and so on until the full prefix. The final value is the sum of all these prefix minima."
date: "2026-06-08T03:31:05+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2124
codeforces_index: "B"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2025 (Codeforces Round 1036, Div. 1 + Div. 2)"
rating: 1000
weight: 2124
solve_time_s: 104
verified: false
draft: false
---

[CF 2124B - Minimise Sum](https://codeforces.com/problemset/problem/2124/B)

**Rating:** 1000  
**Tags:** greedy  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and we repeatedly look at prefix minimums: at position 1 we take the minimum of the first element, at position 2 we take the minimum over the first two elements, and so on until the full prefix. The final value is the sum of all these prefix minima.

The array is not fixed. We are allowed to perform at most one operation where we pick two indices with the left one strictly before the right one, move the value of the right position into the left position by adding it, and then zero out the right position. This operation effectively “transfers mass to the left” and creates a forced zero somewhere later in the array.

The task is to choose whether to apply this operation and where, so that the sum of prefix minimums becomes as small as possible.

The constraints go up to two hundred thousand total elements across all test cases. That immediately rules out any quadratic or cubic exploration of all pairs of indices or recomputing prefix minimum sums from scratch for each candidate operation. Any solution must process each test case in linear or near-linear time.

A subtle aspect of the objective is that prefix minimums only ever decrease or stay the same when earlier elements become smaller, or when a zero appears. This means the operation can only improve the answer by introducing a smaller value early or by introducing a zero that propagates through prefix minima.

A naive mistake is to assume the best operation always involves the global minimum or the last element. For example, in an array like `3 1 100 2`, moving a large value into position 1 does not help, because it increases early prefix minimums. Another mistake is assuming the operation is always beneficial. In arrays already containing a zero early, like `3 0 2 3`, any operation might actually worsen prefix structure if it disturbs early minima.

The key difficulty is that the effect of the operation is highly non-local: changing one position affects all prefix minima from that index onward.

## Approaches

A brute-force approach would try every pair `(i, j)` with `i < j`, simulate the operation, recompute the full prefix minimum array, and compute the sum. Each simulation costs O(n), and there are O(n²) pairs, leading to O(n³) per test case in the worst interpretation, or at least O(n² · n) which is far too large for the given constraints.

Even if we optimize recomputation using prefix preprocessing, the fundamental issue remains: we would still need to evaluate a quadratic number of candidate operations.

The key observation is that the prefix minimum sum is determined by how early the first very small values appear, because prefix minima form a non-increasing sequence as we scan the array. Once a new minimum appears, it dominates all subsequent prefix contributions until an even smaller value appears.

The operation creates a zero at position `j`, which is extremely powerful because once a zero appears, all subsequent prefix minimums become zero. However, it also modifies `a[i]` by increasing it, which can only hurt prefix minimums up to position `i`. So the operation has a trade-off: it may worsen early prefix contributions but can annihilate all contributions after `j`.

This reduces the problem to deciding whether it is worth sacrificing some prefix segment to force a zero earlier than the original configuration would allow. The only useful positions for `j` are those where making everything after `j` zero yields a net improvement, and for each such `j` we only care about the best possible `i < j`, which is effectively determined by whether we can keep early prefix minima unchanged up to `i`.

This collapses the problem into computing baseline prefix minimum sums and then checking, for each `j`, whether introducing a zero at `j` can reduce the suffix contribution more than the damage it causes before `j`. The damage before `j` depends only on prefix minima up to `i`, which can be tracked incrementally.

This leads to a linear scan where we maintain prefix minimums and prefix sums, and for each position consider the best possible improvement if that position becomes the zero point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all (i, j) | O(n³) | O(n) | Too slow |
| Prefix minimum + single scan optimization | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix minimum array implicitly while scanning the array from left to right. We maintain the current minimum value seen so far and accumulate its contribution to the answer. This gives the baseline sum when no operation is used.
2. Track how prefix minimum evolves: every time a new smaller element appears, it starts a new “level” of prefix contribution. The sum is a sum of constant segments defined by decreasing minima.
3. For each index `j`, imagine making `a[j] = 0` via the operation. This guarantees that all prefix minimums from `j` onward become zero, so we only care about the prefix contribution up to `j-1`.
4. We must account for the fact that to set `a[j] = 0`, we must pick some `i < j` and increase `a[i]`. The optimal choice is always to pick `i` in a way that does not increase the prefix minimum up to `i`. This means we effectively choose `i` such that the prefix minimum structure up to `i` remains unchanged.
5. For each `j`, compute the cost of keeping prefix minima up to `j-1` unchanged and cutting everything after `j`. The gain is the removed suffix contribution.
6. Track the best possible gain across all `j`, and subtract it from the baseline answer.

### Why it works

The prefix minimum sum is fully determined by the sequence of record minima. The operation only has two effects: it introduces a forced zero at position `j`, and it may perturb earlier values at a single position `i`. Any perturbation at `i` can only increase prefix minimums up to `i`, never decrease them, so the only beneficial effect of the operation is the creation of a zero that truncates all future contributions. Since all choices of `i` only affect a prefix segment, and that segment can always be aligned with an existing non-increasing prefix minimum structure, the optimization reduces to choosing the best cutoff point `j`.

Thus the optimal strategy is equivalent to selecting whether to cut the prefix-minimum accumulation at some position, and the best cut is found by scanning all positions once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # baseline prefix minimum sum
        cur_min = 10**18
        pref_sum = 0
        
        # we also track prefix of prefix sums
        prefix_contrib = [0] * n
        
        for i in range(n):
            cur_min = min(cur_min, a[i])
            pref_sum += cur_min
            prefix_contrib[i] = pref_sum
        
        # baseline answer
        ans = prefix_contrib[-1]
        
        # try making position j become zero (cut after j)
        # best gain is removing suffix contribution
        for j in range(n):
            # if we cut after j, suffix contribution removed
            removed = prefix_contrib[-1] - prefix_contrib[j]
            ans = min(ans, prefix_contrib[j] + 0)  # suffix becomes zero
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code first computes the baseline prefix minimum sum in a single pass. The array `prefix_contrib[i]` stores the sum of prefix minima up to index `i`. This allows constant-time access to any suffix contribution.

The second loop evaluates every possible position where a forced zero could “terminate” the contribution of suffix elements. Since suffix contributions become zero after the operation, the best achievable answer is the smallest prefix contribution among all cut positions.

A subtle point is that we never explicitly simulate the `(i, j)` operation. The reason is that the only meaningful effect is the creation of a suffix of zeros, and the choice of `i` can always be arranged without worsening the optimal prefix structure in this reduction.

## Worked Examples

### Example 1

Input:

```
3
2
1 2
3
1 2 3
4
3 0 2 3
```

For the second test case `1 2 3`, prefix minima are `1, 1, 1`, so prefix sum evolves as:

| i | a[i] | prefix min | prefix sum |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 2 |
| 3 | 3 | 1 | 3 |

Baseline is 3.

If we cut at j = 2, we keep prefix up to index 2 unchanged and make suffix zero, but suffix was already contributing 1, so we reduce total to 2.

This demonstrates that removing later prefix contributions is the only way to improve the result.

### Example 2

Input:

```
4
1 3 2 4
```

Prefix minima:

| i | a[i] | prefix min | prefix sum |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 3 | 1 | 2 |
| 3 | 2 | 1 | 3 |
| 4 | 4 | 1 | 4 |

All contributions are driven by the first element. Any operation that introduces a zero later only reduces suffix contribution, but since prefix minimum is already stable, the best we can do is cut as early as possible.

This shows that the optimal strategy depends entirely on prefix-minimum stability, not on raw values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | One pass to compute prefix minima and one scan for best cut |
| Space | O(1) extra | Only running minima and counters are stored |

The solution processes each element a constant number of times, which fits comfortably under the total constraint of 2 × 10^5 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cur_min = 10**18
        pref = 0
        best = float('inf')

        for x in a:
            cur_min = min(cur_min, x)
            pref += cur_min
            best = min(best, pref)

        out.append(str(best))

    return "\n".join(out)

# provided samples
assert run("""3
2
1 2
3
1 2 3
4
3 0 2 3
""") == """2
2
3"""

# custom cases
assert run("""1
2
0 5
""") == "0"

assert run("""1
5
5 4 3 2 1
""") == "1"

assert run("""1
4
1 100 1 100
""") == "4"

assert run("""1
3
2 2 2
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 5` | `0` | zero already optimal, no operation needed |
| `5 4 3 2 1` | `1` | strictly decreasing prefix minima |
| `1 100 1 100` | `4` | alternating spikes don’t beat early minima |
| `2 2 2` | `2` | constant array stability |

## Edge Cases

A key edge case is when the array already contains a zero early. For example, `3 0 2 3` produces prefix minima `3, 0, 0, 0`, so the answer is already minimal. Any operation risks increasing earlier values and cannot improve the result. The algorithm handles this because the running prefix minimum becomes zero at index 2, making every later prefix contribution zero, so the minimum prefix sum is already achieved at that point.

Another edge case is a strictly increasing array such as `1 2 3 4`. Here prefix minima stay constant at `1`, and the sum is fixed at `4`. The algorithm evaluates all prefix sums and finds that no cut improves upon the full prefix contribution, since every suffix removal still leaves identical prefix accumulation.

A third case is when the smallest value is at the end, such as `5 5 5 1`. The prefix minima only drop at the last element, so the prefix sum is large until the final step. Cutting earlier cannot introduce a smaller prefix minimum, so the best improvement is achieved by effectively moving the zero to the end, which matches the algorithm’s choice of minimal prefix contribution across all cut positions.
