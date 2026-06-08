---
title: "CF 1873F - Money Trees"
description: "We are given a row of trees, each tree carrying two attributes: a height and a number of fruits. We want to choose a contiguous segment of these trees."
date: "2026-06-08T23:14:32+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1873
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 898 (Div. 4)"
rating: 1300
weight: 1873
solve_time_s: 77
verified: true
draft: false
---

[CF 1873F - Money Trees](https://codeforces.com/problemset/problem/1873/F)

**Rating:** 1300  
**Tags:** binary search, greedy, math, two pointers  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of trees, each tree carrying two attributes: a height and a number of fruits. We want to choose a contiguous segment of these trees. The segment is only valid if, moving from left to right inside it, every tree’s height is divisible by the height of the next tree. This creates a directional divisibility chain that constrains where a segment can start and end.

Among all valid segments, we want the one with the maximum number of trees, but with an additional restriction: the total number of fruits collected from that segment must not exceed a given limit $k$. If no segment satisfies both conditions, the answer is zero.

The key difficulty is that validity depends on two independent constraints. One is structural, coming from the divisibility relationship between adjacent heights. The other is quantitative, coming from the sum of fruits.

The input size reaches $2 \cdot 10^5$ across all test cases, so any solution that checks all subarrays directly will not fit within time limits. A quadratic enumeration would perform about $n^2$ segment checks per test case, which in the worst case is around $10^{10}$ operations overall, far beyond what is feasible.

A subtle edge case arises when divisibility immediately fails at every adjacent pair. For example, if heights are `[2, 3, 5]`, then no segment longer than 1 is valid. Any naive solution that only checks fruit constraints would incorrectly consider longer segments.

Another edge case appears when divisibility holds everywhere but fruit values are large. For instance, heights `[8, 4, 2]` form a perfectly valid chain, but if fruits are `[10, 10, 10]` and $k = 15$, even a length-2 segment is invalid despite structural validity.

These two constraints interact in a way that suggests we should separate the problem into manageable blocks first.

## Approaches

If we ignore structure for a moment, the problem reduces to finding the longest subarray with sum at most $k$, which is a standard sliding window problem. That part alone is linear.

If we ignore the fruit constraint, we instead need to find maximal segments where every adjacent pair satisfies $h_i \bmod h_{i+1} = 0$. This can be precomputed by breaking the array into maximal “valid chains” where divisibility holds continuously. Inside each chain, any subsegment is structurally valid.

A brute-force solution would try every starting index, expand to the right while checking divisibility and maintaining a running sum. Each expansion is O(n), repeated n times, leading to O(n²) per test case. With total n up to $2 \cdot 10^5$, this is too slow.

The key observation is that divisibility constraints define independent blocks. Once $h_i$ does not divide $h_{i+1}$, no segment can cross that boundary. So we can treat each maximal valid block separately. Inside each block, the problem becomes purely: longest subarray with sum ≤ k, solvable using two pointers.

We maintain a sliding window over each block, expanding right while the sum stays within k, and shrinking from the left otherwise. Because each element enters and leaves the window at most once per block, the total complexity stays linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Block + Two Pointers | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the array from left to right and identify segments where each adjacent pair satisfies $h_i \bmod h_{i+1} = 0$. These are maximal structural blocks. We reset the block whenever the condition fails because no valid segment can cross that boundary.
2. For each block, treat it independently. Within a block, every subarray automatically satisfies the divisibility condition, so only the sum constraint remains relevant.
3. Initialize two pointers at the start of the block and a running sum of fruits.
4. Extend the right pointer step by step, adding the current fruit value to the sum. After each extension, check if the sum exceeds $k$.
5. If the sum exceeds $k$, move the left pointer forward while subtracting values until the sum becomes valid again. This restores feasibility in the smallest possible way, preserving maximal window size ending at the current right endpoint.
6. At each right endpoint, update the answer with the current window length.

The correctness of shrinking greedily comes from the fact that all values are positive. Removing more elements than necessary would only reduce the window further without enabling any new valid configuration.

### Why it works

The algorithm relies on two invariants. First, the current window always lies entirely inside a maximal divisibility block, so every candidate segment it considers is structurally valid. Second, the sliding window maintains the invariant that its sum is always ≤ k after adjustment. Because all fruit values are positive, expanding only increases the sum and shrinking only decreases it monotonically, ensuring that each pointer moves in one direction and no valid candidate is skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        h = list(map(int, input().split()))

        ans = 0
        l = 0
        s = 0

        i = 0
        while i < n:
            j = i
            while j + 1 < n and h[j] % h[j + 1] == 0:
                j += 1

            # process block [i, j]
            l = i
            s = 0

            for r in range(i, j + 1):
                s += a[r]
                while s > k and l <= r:
                    s -= a[l]
                    l += 1
                ans = max(ans, r - l + 1)

            i = j + 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first splits the array into maximal valid divisibility chains using a simple pointer expansion. Each time the condition fails, we close the block. This ensures we never attempt to form a segment across an invalid adjacency.

Inside each block, we reset the sliding window and maintain a running sum. The left pointer only moves forward, never backward, ensuring linear complexity.

A common mistake here is failing to reset the sum and left pointer at block boundaries. Without that reset, the window could incorrectly include elements from a previous invalid structural segment.

## Worked Examples

### Example 1

Input:

```
n = 5, k = 12
a = [3, 2, 4, 1, 8]
h = [4, 4, 2, 4, 1]
```

Divisibility structure creates blocks: `[4, 4, 2, 4, 1]` breaks at no point except the last step, so full array is one block.

| r | h condition valid | window (l..r) | sum | action | best |
| --- | --- | --- | --- | --- | --- |
| 0 | start | [0] | 3 | ok | 1 |
| 1 | 4 % 4 | [0,1] | 5 | ok | 2 |
| 2 | 4 % 2 | [0,1,2] | 9 | ok | 3 |
| 3 | 2 % 4 fails? actually 2 % 4 ≠ 0, block ends earlier | restart |  |  |  |

Actually block is `[0..2]` and `[3..4]`. On second block `[1,8]`, best length is 2. Final answer is 3.

This shows how structural splitting prevents invalid transitions from corrupting the window.

### Example 2

Input:

```
n = 4, k = 8
a = [5, 4, 1, 2]
h = [6, 2, 3, 1]
```

Divisibility blocks:

- `[6,2]`
- `[3,1]`

First block:

- window `[5]`, `[5,4]` sum becomes 9 > 8 so shrink → `[4]`, best 1

Second block:

- `[1,2]` sum = 3 valid, best 2

This demonstrates how the sliding window reacts only to sum constraints inside each structural segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index enters and leaves the sliding window at most once, and each element is processed once in block construction |
| Space | O(1) | Only pointers and running sums are stored |

The total complexity over all test cases is linear in the sum of n, which fits comfortably within limits.

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
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        h = list(map(int, input().split()))

        ans = 0
        i = 0

        while i < n:
            j = i
            while j + 1 < n and h[j] % h[j + 1] == 0:
                j += 1

            l = i
            s = 0
            for r in range(i, j + 1):
                s += a[r]
                while s > k:
                    s -= a[l]
                    l += 1
                ans = max(ans, r - l + 1)

            i = j + 1

        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""5
5 12
3 2 4 1 8
4 4 2 4 1
4 8
5 4 1 2
6 2 3 1
3 12
7 9 10
2 2 4
1 10
11
1
7 10
2 6 3 1 5 10 6
72 24 24 12 4 4 2
""") == """3
2
1
0
3"""

# custom cases
assert run("""1
1 5
10
7
""") == "0", "single invalid by sum"

assert run("""1
3 100
1 2 3
6 3 1
""") == "3", "full valid chain"

assert run("""1
5 5
1 2 3 4 5
10 10 10 10 10
""") == "2", "sum constraint only"

assert run("""1
4 3
1 2 3 4
2 1 4 8
""") == "2", "block boundary behavior"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element large value | 0 | sum constraint on minimal input |
| full valid chain | 3 | structural + full window |
| increasing sums | 2 | sliding window correctness |
| mixed divisibility | 2 | block splitting correctness |

## Edge Cases

One important edge case is when every adjacent pair fails divisibility immediately. In that situation each block has size one, and the algorithm reduces to checking whether each single fruit value is ≤ k. The sliding window never expands across elements, so correctness depends entirely on resetting at every index.

Another case is when the entire array is one long valid chain. Here the algorithm must behave exactly like a standard two-pointer maximum-length subarray under sum constraint. The block logic must not interfere with window continuity.

A third subtle case occurs when large fruit values force frequent shrinking. Because all values are positive, repeated shrinking always converges, and no infinite loop is possible.
