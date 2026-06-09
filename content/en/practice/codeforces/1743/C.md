---
title: "CF 1743C - Save the Magazines"
description: "We have a row of boxes. Box i contains a[i] magazines. A binary string tells us which boxes initially have lids. Every lid is attached to a box that initially contains '1'. That lid has only two choices: stay where it is, or move one position to the left."
date: "2026-06-09T16:01:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1743
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 137 (Rated for Div. 2)"
rating: 1100
weight: 1743
solve_time_s: 138
verified: true
draft: false
---

[CF 1743C - Save the Magazines](https://codeforces.com/problemset/problem/1743/C)

**Rating:** 1100  
**Tags:** constructive algorithms, dp, greedy  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of boxes. Box `i` contains `a[i]` magazines. A binary string tells us which boxes initially have lids.

Every lid is attached to a box that initially contains `'1'`. That lid has only two choices: stay where it is, or move one position to the left. A lid cannot move more than once.

After all decisions are made, every box covered by a lid contributes its magazine count to the answer. The goal is to maximize the total number of saved magazines.

The interesting part is that lids are independent objects, but their choices interact. A lid from position `i` can protect either box `i` or box `i-1`. Choosing one option may prevent another lid from protecting a more valuable box.

The total length across all test cases is at most `2 · 10^5`, which immediately rules out anything quadratic. An `O(n²)` algorithm would perform roughly `4 · 10^10` operations in the worst case, far beyond the limit. We need a linear or near-linear solution per test case.

Several edge cases make greedy implementations fail.

Consider:

```
n = 2
s = 01
a = [10, 1]
```

The only lid starts at position 2. Keeping it there saves `1`, while moving it left saves `10`. The correct answer is `10`. A strategy that always keeps existing covered boxes protected would return `1`.

Consider:

```
n = 3
s = 011
a = [5, 100, 1]
```

The optimal result is `105`.

Move the lid from position 2 to position 1, keep the lid at position 3. Saved boxes are `{1, 3}` with value `5 + 1 = 6`, which is not optimal.

Instead, keep the lid at position 2 and move the lid from position 3 to position 2. Since two lids cannot occupy the same final box, we need a better interpretation of the process. The correct greedy solution effectively chooses the best magazines within a consecutive block of ones. A simplistic local decision can easily lose the value `100`.

Another subtle case is:

```
n = 4
s = 0111
a = [5, 4, 5, 1]
```

The answer is `14`, not `10`.

A naive strategy that always protects the currently covered box would save `4 + 5 + 1 = 10`. Moving the lid from position 2 to position 1 allows us to save `5 + 5 + 4 = 14`.

The key observation is that sometimes we deliberately sacrifice a smaller covered box to free a lid for a larger uncovered box.

## Approaches

A brute-force solution would examine every lid and try both possibilities, stay or move left. If there are `k` lids, this creates `2^k` possible configurations. In the worst case, every position contains a lid, so `k = n`.

For `n = 2 · 10^5`, even `2^50` is already impossible, and `2^200000` is astronomically large. The brute-force approach is correct because it explicitly checks every legal arrangement, but it becomes unusable almost immediately.

To find a faster solution, we need to understand what a lid actually represents.

Suppose we encounter a `'1'`. That lid guarantees that one box among a small local region will eventually be protected. If a `'1'` follows a `'0'`, we have a choice: either protect the current box or shift protection onto the previous uncovered box.

This creates a chain effect inside every consecutive segment of ones. Whenever we see a `'1'` after another `'1'`, the protection can effectively be rearranged among the boxes in that segment. The only magazines we might lose are the smallest values within the rearranged region.

A particularly elegant greedy process emerges.

We scan from left to right.

When we reach a position containing `'1'`, we tentatively save its magazines by adding `a[i]` to the answer.

If the previous position is `'0'`, we have discovered the start of a new block of ones. We may want to shift protection left and include that previous box instead.

The greedy rule is:

Maintain the minimum magazine count among the currently chosen protected boxes inside the active block.

When a new `'1'` extends the block, if the previous uncovered box has more magazines than the smallest protected box so far, replace that smallest value with the previous box's value.

This replacement is exactly what the optimal rearrangement would do. We trade away the weakest protected box and protect a more valuable uncovered box instead.

The result is a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k) | O(k) | Too slow |
| Optimal Greedy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the answer to zero.
2. Scan the array from left to right.
3. When `s[i] = '1'`, add `a[i]` to the answer because this box is initially protected and is a candidate to remain protected.
4. If `s[i] = '1'` and `s[i-1] = '0'`, a new block of ones begins. Set a variable `cur` to `a[i]`.

Here `cur` stores the smallest magazine count currently chosen inside this active block.
5. If `s[i] = '1'` and `s[i-1] = '1'`, update `cur = min(cur, a[i])`.

The smallest protected value in the block may have changed.
6. Whenever a block starts after a zero, compare the uncovered box value `a[i-1]` with `cur`.

If `a[i-1] > cur`, replacing the weakest protected box with this uncovered box increases the answer by `a[i-1] - cur`.

Add this difference to the answer and set `cur = a[i-1]`.
7. Continue until the end of the array.

A more implementation-friendly version used by most accepted solutions is slightly different but equivalent.

When we encounter a `'1'` after a `'0'`, we start a block and keep track of the value of the previous zero-position box. As the block grows, whenever a new protected value is larger than that stored value, we swap them conceptually and gain additional magazines.

### Why it works

Consider a maximal segment that looks like:

```
0 1 1 1 1 ...
```

Every lid inside this segment can only move left by one position. The total number of boxes that can end up protected equals the number of lids in the segment.

Among all boxes consisting of the leading zero-position and the boxes in the segment, exactly one box must be excluded from protection. To maximize the saved magazines, we should exclude the box with the smallest magazine count.

The greedy scan maintains exactly this invariant. As the segment grows, it continuously tracks the smallest currently protected value. Whenever a better candidate appears, it replaces that smallest value. By the end of the segment, every value except the minimum one contributes to the answer, which is the optimal choice.

Since segments are independent, optimizing each segment independently yields a globally optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()
        a = list(map(int, input().split()))

        ans = 0
        prev = 0

        for i in range(n):
            if s[i] == '1':
                if i > 0 and s[i - 1] == '0':
                    prev = a[i - 1]

                if prev and prev > a[i]:
                    ans += prev
                    prev = a[i]
                else:
                    ans += a[i]

        print(ans)

solve()
```

The variable `ans` stores the total magazines saved so far.

The variable `prev` represents the candidate uncovered box immediately before the current block of ones. When a block begins at position `i`, the box at `i-1` is the only uncovered box that can potentially enter the protected set through lid shifts.

When we process a `'1'`, we compare its value with `prev`.

If `prev > a[i]`, protecting the previous box is better than protecting this current box. We add `prev` and keep the smaller value as the new candidate that might later be discarded.

If `prev <= a[i]`, the current box is at least as valuable, so we keep it protected and add `a[i]`.

The update `prev = a[i]` after a replacement is the subtle part. It means the smaller value becomes the weakest chosen box in the current segment, which may later be replaced again by an even larger candidate.

All arithmetic easily fits inside Python integers because the maximum answer is at most `2 · 10^5 × 10^4 = 2 · 10^9`.

## Worked Examples

### Sample 1

```
s = 01110
a = [10, 5, 8, 9, 6]
```

| i | s[i] | a[i] | prev before | action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 10 | 0 | skip | 0 |
| 1 | 1 | 5 | 10 | take 10, set prev=5 | 10 |
| 2 | 1 | 8 | 5 | take 8 | 18 |
| 3 | 1 | 9 | 5 | take 9 | 27 |
| 4 | 0 | 6 | 5 | skip | 27 |

Final answer: `27`.

The first lid is better used on box 1 than box 2 because `10 > 5`. After that decision, the remaining boxes in the block stay protected.

### Sample 2

```
s = 011011
a = [20, 10, 9, 30, 20, 19]
```

| i | s[i] | a[i] | prev before | action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 20 | 0 | skip | 0 |
| 1 | 1 | 10 | 20 | take 20, prev=10 | 20 |
| 2 | 1 | 9 | 10 | take 10, prev=9 | 30 |
| 3 | 0 | 30 | 9 | skip | 30 |
| 4 | 1 | 20 | 30 | take 30, prev=20 | 60 |
| 5 | 1 | 19 | 20 | take 20, prev=19 | 80 |

Final answer: `80`.

This example shows how the same greedy logic works independently on multiple segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed once |
| Space | O(1) | Only a few variables are maintained |

The sum of all `n` values across test cases is at most `2 · 10^5`. A linear scan over all positions performs only a few hundred thousand operations, which comfortably fits within the time limit. The algorithm uses constant extra memory regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()
        a = list(map(int, input().split()))

        ans = 0
        prev = 0

        for i in range(n):
            if s[i] == '1':
                if i > 0 and s[i - 1] == '0':
                    prev = a[i - 1]

                if prev and prev > a[i]:
                    ans += prev
                    prev = a[i]
                else:
                    ans += a[i]

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run(
"""4
5
01110
10 5 8 9 6
6
011011
20 10 9 30 20 19
4
0000
100 100 100 100
4
0111
5 4 5 1
"""
) == "27\n80\n0\n14"

# minimum size
assert run(
"""1
1
0
7
"""
) == "0"

# single lid
assert run(
"""1
2
01
10 1
"""
) == "10"

# all ones
assert run(
"""1
4
1111
5 5 5 5
"""
) == "20"

# replacement chain
assert run(
"""1
4
0111
100 1 2 3
"""
) == "105"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, s=0` | `0` | Minimum size input |
| `01, [10,1]` | `10` | Moving a lid left is beneficial |
| `1111, [5,5,5,5]` | `20` | No leading zero before the block |
| `0111, [100,1,2,3]` | `105` | Multiple replacements inside one block |

## Edge Cases

Consider:

```
n = 2
s = 01
a = [10, 1]
```

At the start of the block, `prev = 10`. Since `10 > 1`, the algorithm adds `10` and stores `1` as the weakest value. The final answer is `10`, which is optimal because the lid should move left.

Consider:

```
n = 4
s = 0111
a = [5, 4, 5, 1]
```

The algorithm starts with `prev = 5`. At value `4`, it replaces and gains `5`. At value `5`, it gains `5`. At value `1`, it gains `4`. Total saved magazines equal `14`. This is exactly the optimal arrangement where the smallest value in the segment, namely `1`, is excluded.

Consider:

```
n = 4
s = 0000
a = [100, 100, 100, 100]
```

No position contains a lid, so the scan never adds anything. The answer remains `0`, which is correct.

Consider:

```
n = 4
s = 1111
a = [3, 7, 2, 8]
```

There is no preceding zero that can enter the protected set. Every lid simply protects some box inside the segment, and all four boxes can remain protected. The algorithm adds all values and returns `20`.
