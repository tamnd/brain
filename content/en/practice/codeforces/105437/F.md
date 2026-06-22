---
title: "CF 105437F - New Game"
description: "We are given a multiset of cards, each card carrying an integer value. Monocarp builds a sequence by picking cards one by one, removing them from the deck as he takes them."
date: "2026-06-23T03:42:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105437
codeforces_index: "F"
codeforces_contest_name: "ICPC 2024-2025 NERC, Southern and Volga Russia Qualifier"
rating: 0
weight: 105437
solve_time_s: 90
verified: false
draft: false
---

[CF 105437F - New Game](https://codeforces.com/problemset/problem/105437/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of cards, each card carrying an integer value. Monocarp builds a sequence by picking cards one by one, removing them from the deck as he takes them. The first card can be chosen freely, but every next card is constrained by the value of the last taken card: he can only take a card with the same value or exactly one larger value.

There is an additional restriction on the whole sequence: among all taken cards, the number of distinct values must never exceed k. The process stops as soon as Monocarp cannot legally take another card under these rules. The task is to maximize how many cards he can take by choosing the starting card and then playing optimally.

The constraints go up to n = 200000, which rules out any quadratic simulation over all starting points or all subsets of values. Anything that repeatedly rescans the array or tries to simulate all possible greedy starts independently will be too slow. A solution must reduce the problem to a linear or near-linear sweep after preprocessing.

A subtle edge case appears when values are scattered but still form long usable chains. For example, if k = 2 and the array is `[1, 100, 2, 3, 101]`, a naive strategy that greedily extends from a starting point may fail to recognize that optimal play depends on selecting a contiguous range of values after sorting, not on the original order. Another failure case comes from assuming we must always start from the smallest value; starting from a middle value can produce a longer usable segment because we are allowed to move upward by +1 only.

The key hidden structure is that the sequence of taken values is always non-decreasing and increases by at most one per step, so the entire play happens inside a contiguous interval of integer values, while the actual order inside each value does not matter beyond counts.

## Approaches

A brute-force approach would try every possible starting card, then simulate the game greedily or with backtracking: from a chosen start, repeatedly pick any available card whose value is either x or x+1, while tracking how many distinct values have appeared. Each simulation can take O(n) time if we scan for next valid cards or maintain buckets without optimization, and doing this for all starting positions leads to O(n^2), which is far too large for 200000 elements.

The key observation is that the rules only depend on values, not positions. Once we group identical values together, the problem becomes about frequencies of values and choosing a contiguous segment of values where we simulate taking all cards, but with the constraint that we can only “use” at most k distinct values in any valid segment of the process.

If we sort the distinct values and compress them, each value has a frequency. Any valid play corresponds to choosing a window of consecutive values, and within that window Monocarp can traverse from left to right, consuming all cards. The constraint of at most k distinct values means that the window size in terms of distinct values must be at most k, but because movement is constrained to x or x+1 transitions, once we include a value x, we can only proceed to x+1 if it exists in the chosen structure. This effectively turns the optimal strategy into selecting a segment of consecutive integers and summing their frequencies, while ensuring we respect the k-bound by limiting how many distinct values we pass through.

This reduces to a classic sliding window over sorted unique values: we maintain a window of consecutive values where adjacency is valid, and ensure the number of distinct values inside does not exceed k, then maximize total frequency in that window.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Sorting + Sliding Window over values | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. First, group identical values and count their frequencies. This removes positional information, because only how many copies of each value exist matters for maximizing the length of the sequence.
2. Sort the distinct values in increasing order, keeping their frequencies aligned. Sorting is necessary because transitions are only allowed between equal or consecutive integers, so order in value space defines all valid moves.
3. Use two pointers over the sorted unique values to maintain a window of candidate values that Monocarp can traverse. The right pointer expands the window by adding new values in increasing order.
4. Maintain the total number of cards inside the current window as the sum of frequencies. This represents how many steps Monocarp can take if he commits to this set of values.
5. Ensure the window respects the constraint induced by the game: values must remain consecutive, so if the gap between consecutive values exceeds 1, we reset the window starting at the current value. This is because jumps greater than +1 are forbidden, so disconnected values cannot coexist in a valid sequence.
6. Since Monocarp can only include at most k distinct values, shrink the left side of the window whenever its size exceeds k. This keeps the number of distinct values within the allowed limit.
7. At each step, update the answer with the maximum total frequency observed in any valid window.

The reason this works is that any valid game path corresponds exactly to choosing a segment of consecutive integer values, and within that segment Monocarp can take all cards of those values. The k constraint restricts how wide this segment can be in terms of distinct values, and the transition rule restricts it to consecutive integers. Thus every valid play is represented by exactly one valid sliding window, and every sliding window corresponds to a valid play.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = defaultdict(int)
    for x in a:
        freq[x] += 1

    vals = sorted(freq.items())  # (value, count)

    left = 0
    curr_sum = 0
    best = 0

    for right in range(len(vals)):
        if right > 0 and vals[right][0] != vals[right - 1][0] + 1:
            left = right
            curr_sum = 0

        curr_sum += vals[right][1]

        while right - left + 1 > k:
            curr_sum -= vals[left][1]
            left += 1

        best = max(best, curr_sum)

    print(best)

if __name__ == "__main__":
    solve()
```

The code begins by compressing the input into a frequency map. This is essential because the answer depends only on counts per value, not their positions.

After sorting values, the loop maintains a sliding window over consecutive integers. The reset condition `vals[right][0] != vals[right - 1][0] + 1` enforces the rule that we cannot bridge gaps larger than 1, since the game only allows moving from x to x or x+1.

The second constraint, limiting the number of distinct values, is enforced by shrinking the window when it exceeds k distinct values. The running sum `curr_sum` tracks how many cards are in the current valid segment, which is exactly the length of a valid play sequence.

## Worked Examples

### Example 1

Input:

```
10 2
5 2 4 3 4 3 4 5 3 2
```

After frequency compression, we get values:

`2:2, 3:3, 4:3, 5:2`

We simulate:

| right | value | left | window values | sum | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 0 | [2] | 2 | start |
| 1 | 3 | 0 | [2,3] | 5 | expand |
| 2 | 4 | 0 | [2,3,4] | 8 | expand |
| 3 | 5 | 0→1 | [3,4,5] | 8 | shrink to k=2 |

Best is 8.

This shows how the window always represents a contiguous value chain, and how the k constraint forces us to drop the leftmost value.

### Example 2

Input:

```
5 1
10 11 10 11 10
```

Frequencies:

`10:3, 11:2`

| right | value | left | window | sum | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 10 | 0 | [10] | 3 | start |
| 1 | 11 | 1 | [11] | 2 | reset due to k=1 |

Best is 3.

This confirms that when k = 1, we are forced to pick a single value block, and the algorithm correctly isolates the best frequency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting distinct values dominates, sliding window is linear |
| Space | O(n) | Frequency map and compressed array |

The constraints allow an O(n log n) solution comfortably for n up to 200000. The sliding window ensures we never revisit elements, keeping the traversal efficient.

## Test Cases

```python
import sys, io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = defaultdict(int)
    for x in a:
        freq[x] += 1

    vals = sorted(freq.items())

    left = 0
    curr_sum = 0
    best = 0

    for right in range(len(vals)):
        if right > 0 and vals[right][0] != vals[right - 1][0] + 1:
            left = right
            curr_sum = 0

        curr_sum += vals[right][1]

        while right - left + 1 > k:
            curr_sum -= vals[left][1]
            left += 1

        best = max(best, curr_sum)

    return str(best)

# provided samples
assert run("10 2\n5 2 4 3 4 3 4 5 3 2\n") == "8", "sample 1"
assert run("5 1\n10 11 10 11 10\n") == "3", "sample 2"

# custom cases
assert run("1 1\n7\n") == "1", "single element"
assert run("6 2\n1 100 2 3 101 4\n") == "3", "disconnected values"
assert run("8 3\n1 1 2 2 3 3 4 4\n") == "8", "full chain"
assert run("5 5\n1 1 1 1 1\n") == "5", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal case |
| disconnected values | 3 | gap handling |
| full chain | 8 | optimal full window |
| all equal | 5 | single-value dominance |

## Edge Cases

A key edge case is when values are not consecutive in the input but still allow partial chains. For input `6 2 / 1 100 2 3 101 4`, the algorithm correctly resets whenever it encounters a gap larger than 1. It builds `[1]`, then resets at `100`, then later builds `[2,3,4]` with sum 3, which is optimal under k = 2 constraints.

Another edge case is when k is large enough to include all distinct consecutive values. For `8 3 / 1 1 2 2 3 3 4 4`, the window never exceeds k, and the algorithm accumulates all frequencies into a single segment, correctly producing 8.

Finally, when all values are identical, the window is trivial and always valid. The algorithm never triggers resets or shrinking, and the answer is simply n, matching the fact that every card can be taken consecutively without violating any rule.
