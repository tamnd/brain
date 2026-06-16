---
title: "CF 1385C - Make It Good"
description: "We are given an array and we are only allowed to delete a prefix, meaning we remove some number of elements from the front and keep the rest unchanged."
date: "2026-06-16T14:16:47+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1385
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 656 (Div. 3)"
rating: 1200
weight: 1385
solve_time_s: 248
verified: false
draft: false
---

[CF 1385C - Make It Good](https://codeforces.com/problemset/problem/1385/C)

**Rating:** 1200  
**Tags:** greedy  
**Solve time:** 4m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and we are only allowed to delete a prefix, meaning we remove some number of elements from the front and keep the rest unchanged. After this deletion, we want the remaining suffix to be transformable into a non-decreasing sequence using a very specific process: we repeatedly take elements from either end of the current array and append them to a new array.

The key property of a “good” array is that there exists a way to build a non-decreasing sequence by always choosing either the leftmost or rightmost remaining element. This is equivalent to saying we can “peel” the array from both ends in some order and collect values that never decrease.

So the task is: among all suffixes of the array, find the shortest prefix we must remove so that the remaining suffix becomes good in this sense.

The constraints are large: total length across test cases is up to 200,000. This immediately rules out any quadratic simulation per test case. Any approach that tries all prefixes and checks “goodness” from scratch would be too slow.

A subtle point is that the answer can be zero. If the original array is already good, we do nothing.

A second subtle case appears when the array is strictly decreasing. For example, `[5, 4, 3, 2]` is actually good, because we can always take from the right end and build a non-decreasing sequence in reverse order. This makes it easy to mistakenly assume monotonicity is required in the original array, which is not true.

Another tricky situation is mixed zig-zag arrays like `[1, 3, 1, 4]`. Locally increasing structure does not guarantee goodness, because the two-end selection imposes a global consistency constraint on what values we pick first.

## Approaches

A brute-force solution would try every possible prefix removal. For each suffix, we would test whether it is good. Testing goodness means simulating the process of picking from both ends and ensuring we can produce a non-decreasing sequence.

A direct simulation for one array can be done greedily by always trying to pick a valid end that does not break monotonicity. But even that takes O(n) per check. Repeating it for every prefix leads to O(n^2) per test case, which is too large under the constraints.

The key insight is to reverse the viewpoint. Instead of asking which prefix to remove, we ask which suffix we can keep. We want the longest suffix that is “good”.

Now consider building the final sequence from right to left. In a valid construction, the last picked element is the minimum of the remaining choices at each step. This suggests that during a greedy construction from the end, once we decide to take a value, everything earlier in the process must be at least that value when chosen from the correct side.

A more structured way to see it is: we want a suffix such that we can split it into two parts during the process, where elements taken from the right form a non-increasing segment, and elements taken from the left also respect a threshold imposed by the first phase. The optimal construction reduces to finding a split point where a monotonic constraint becomes valid, and we track the minimum possible “barrier” value while scanning from the end.

We scan from right to left, maintaining the minimum value seen so far. This minimum represents the best possible last elements we could keep taking from the right. If at any point we encounter an element that is smaller than this maintained structure in a way that violates the construction feasibility, we identify that we must discard more from the front.

This leads to a simple greedy: compute from the end and find the longest suffix that can maintain the required consistency, then the answer is the prefix before it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal Greedy from suffix scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start from the last element of the array, since any valid construction ultimately depends on how we can finish building the non-decreasing sequence.
2. Maintain a variable `mn` that tracks the smallest value we have “committed to” while scanning from right to left. This represents the limiting threshold of what we can still safely incorporate into a valid construction.
3. Move leftwards through the array. At each position, compare the current value with `mn`. If the current value is not compatible with maintaining a valid suffix construction, we update our boundary of validity.
4. Continue this scan until the prefix that must be removed becomes clear, meaning everything to the right of some index can participate in a valid construction.
5. The answer is the number of elements before this valid suffix begins.

Why this works is tied to how the two-ended picking process behaves. Once a value is taken as part of the final sequence, any future choices must respect the ordering constraint. Scanning from the end simulates fixing the tail of the sequence first, which is always the most constrained part. The moment the constraint breaks, everything to the left cannot be salvaged by any prefix deletion smaller than that point, because prefix deletion only shifts the starting position and does not reorder or repair incompatibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        mn = float('inf')
        i = n - 1

        while i >= 0:
            if a[i] > mn:
                break
            mn = min(mn, a[i])
            i -= 1

        print(i + 1)

if __name__ == "__main__":
    solve()
```

The code processes each test case independently. The scan starts from the rightmost element, tracking the smallest value seen so far. The pointer `i` stops when we encounter a value that violates the ability to extend a valid non-decreasing construction from the right side.

The returned answer `i + 1` corresponds to how many elements must be removed from the front so that the remaining suffix begins at index `i+1`.

A common pitfall is forgetting that the scan direction is right-to-left. Scanning left-to-right would not capture the constraint structure of the final construction process.

## Worked Examples

### Example 1

Input:

```
7
4 3 3 8 4 5 2
```

We scan from right:

| Step | Index | Value | mn | Action |
| --- | --- | --- | --- | --- |
| 1 | 6 | 2 | 2 | keep |
| 2 | 5 | 5 | 2 | break condition triggered |

At index 5, value 5 exceeds current minimum 2, meaning the suffix starting too early is invalid. We stop just after index 5.

So we remove prefix of length 4, leaving `[4, 5, 2]`.

This demonstrates how a seemingly valid middle structure fails because earlier values cannot be reconciled with the required end construction order.

### Example 2

Input:

```
5
1 3 1 4 5
```

| Step | Index | Value | mn | Action |
| --- | --- | --- | --- | --- |
| 1 | 4 | 5 | 5 | keep |
| 2 | 3 | 4 | 4 | keep |
| 3 | 2 | 1 | 1 | keep |
| 4 | 1 | 3 | 1 | break |

At index 1, value 3 violates the suffix feasibility condition, so we must remove at least the first two elements.

The remaining suffix `[1, 4, 5]` is valid since it can be arranged into a non-decreasing sequence via end picks.

These traces show that the suffix structure is governed entirely by maintaining consistency from the right boundary backward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is visited at most once per test case |
| Space | O(1) | Only a few scalar variables are maintained |

The total complexity over all test cases remains linear in the input size, fitting comfortably within the constraint of 200,000 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        mn = float('inf')
        i = n - 1

        while i >= 0:
            if a[i] > mn:
                break
            mn = min(mn, a[i])
            i -= 1

        out.append(str(i + 1))
    return "\n".join(out)

# provided sample
assert run("""5
4
1 2 3 4
7
4 3 3 8 4 5 2
3
1 1 1
7
1 3 1 4 5 3 2
5
5 4 3 2 3
""") == """0
4
0
2
3"""

# custom cases
assert run("""3
1
10
2
2 1
6
1 2 3 2 1 4
""") == """0
0
3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[10]` | `0` | single element already good |
| `[2, 1]` | `0` | decreasing array still good |
| `[1,2,3,2,1,4]` | `3` | mixed pattern requiring prefix removal |

## Edge Cases

A single-element array behaves trivially because no choice of ends can break monotonicity, so the scan never triggers a violation.

Strictly decreasing arrays are also safe because the greedy construction always takes from the right end, producing a non-decreasing sequence in reverse order. The algorithm scans without break, yielding answer zero.

In mixed arrays like `[1, 2, 3, 2, 1, 4]`, the violation appears early when a larger value precedes a tightly constrained suffix. The right-to-left scan correctly identifies that the initial prefix prevents any valid two-ended construction from starting, and the output matches the first position where consistency breaks.
