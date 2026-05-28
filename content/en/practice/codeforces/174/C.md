---
title: "CF 174C - Range Increments"
description: "We start with an array of length n filled with zeros. One operation chooses a segment [l, r] and adds 1 to every element inside that segment. The final array is given."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 174
codeforces_index: "C"
codeforces_contest_name: "VK Cup 2012 Round 3 (Unofficial Div. 2 Edition)"
rating: 1800
weight: 174
solve_time_s: 103
verified: true
draft: false
---

[CF 174C - Range Increments](https://codeforces.com/problemset/problem/174/C)

**Rating:** 1800  
**Tags:** data structures, greedy  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of length `n` filled with zeros. One operation chooses a segment `[l, r]` and adds `1` to every element inside that segment.

The final array is given. We must reconstruct a sequence of operations that produces exactly that array, while using as few operations as possible.

The key detail is that operations may overlap freely. If one position ends up with value `5`, then exactly five chosen segments must cover that position. Different positions can share operations if their required increments overlap.

The constraints immediately rule out anything quadratic. The array length reaches `10^5`, and values also reach `10^5`. A solution that repeatedly scans intervals or simulates increments cell by cell would easily perform around `10^10` operations in the worst case. We need something linear or close to linear.

There is also a construction requirement. We are not only asked for the minimum count, we must explicitly output the intervals themselves. Since the statement guarantees the optimal answer contains at most `10^5` operations, an `O(answer)` construction is acceptable.

Several edge cases are easy to mishandle.

Consider a strictly increasing array:

```
1 2 3 4
```

The correct answer is four segments:

```
[1,4]
[2,4]
[3,4]
[4,4]
```

A careless greedy that tries to extend old intervals as far as possible without opening new ones would fail, because every increase from `a[i-1]` to `a[i]` forces additional intervals to begin at `i`.

Now consider decreasing values:

```
4 3 2 1
```

The optimal construction is:

```
[1,1]
[1,2]
[1,3]
[1,4]
```

Here no new intervals are needed after the first position. Instead, some intervals simply end earlier. An implementation that always keeps all intervals alive until the end would overshoot later positions.

Another subtle case contains zeros inside the array:

```
2 0 2
```

The middle zero completely separates the left and right parts. No interval may cross index `2`, otherwise that position would become positive. The optimal solution uses four independent intervals:

```
[1,1]
[1,1]
[3,3]
[3,3]
```

Any approach that treats intervals as reusable across zeros will produce an invalid array.

## Approaches

A brute-force perspective helps expose the structure of the problem.

Suppose we process the array from left to right. At position `i`, we know how many currently active intervals cover it. If fewer than `a[i]` intervals are active, we open new intervals starting at `i`. If too many intervals are active, we close some intervals before reaching `i`.

One naive implementation would explicitly track every active segment and repeatedly search for which intervals to close. In the worst case, this becomes quadratic. For example, an alternating pattern like:

```
1 0 1 0 1 0 ...
```

forces frequent interval creation and destruction. Repeated linear scans over active intervals would be too slow for `10^5` elements.

The crucial observation is that the minimum number of operations is completely determined by increases in the array.

Whenever:

```
a[i] > a[i-1]
```

we must start exactly:

```
a[i] - a[i-1]
```

new intervals at position `i`.

There is no way around this. Existing intervals already contribute only `a[i-1]` coverage at position `i-1`, so to raise coverage further at `i`, additional intervals must begin there.

Conversely, if the value decreases, some intervals simply terminate before the current position.

This transforms the problem into interval bookkeeping. We maintain all currently active intervals. When the required height increases, we open new intervals. When it decreases, we close enough intervals at the previous position.

A stack works perfectly here. Every active interval stores only its starting index. When an interval must end, we pop it and output `[start, current_position - 1]`.

Each interval is pushed once and popped once, so the entire process is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an empty stack. Each element represents an active interval and stores only its starting position.
2. Iterate through the array from left to right.
3. At position `i`, compare `a[i]` with the number of active intervals, which is simply `len(stack)`.
4. If there are too many active intervals, repeatedly pop intervals from the stack until the stack size becomes `a[i]`.

Each popped interval ends at `i - 1`, because it cannot continue into the current position.
5. If there are too few active intervals, repeatedly push the current position `i` onto the stack until the stack size becomes `a[i]`.

Every new interval begins at `i`.
6. Continue this process for all positions.
7. After processing the entire array, all remaining active intervals must end at position `n`. Pop them all and output their segments.

### Why it works

The invariant is simple:

After processing position `i`, the stack contains exactly the intervals that cover position `i`.

Its size is therefore exactly `a[i]`.

Whenever the target value increases, additional coverage must appear for the first time at the current position, so new intervals are unavoidable. Starting them later would fail to cover the current cell, while starting them earlier would incorrectly increase previous cells.

Whenever the target value decreases, some intervals must stop before the current position. Ending any subset of active intervals works equally well, so using a stack is sufficient.

Because new intervals are created only when mathematically necessary, the total number of intervals is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    stack = []
    ans = []

    for i in range(n):
        pos = i + 1

        while len(stack) > a[i]:
            start = stack.pop()
            ans.append((start, pos - 1))

        while len(stack) < a[i]:
            stack.append(pos)

    while stack:
        start = stack.pop()
        ans.append((start, n))

    print(len(ans))
    print("\n".join(f"{l} {r}" for l, r in ans))

solve()
```

The stack stores the starting positions of all intervals currently covering the current index.

When the required height drops, intervals must terminate before the current position. Since all active intervals are equivalent, popping any intervals works. Using a stack gives constant-time insertion and removal.

When the required height rises, we start new intervals at the current position. Each push corresponds to one new operation.

A common off-by-one mistake appears when closing intervals. If we are currently at position `i`, then removed intervals must end at `i - 1`, because they should not contribute to the current cell.

Another subtle detail is the final cleanup. Intervals remaining active after the loop must extend all the way to `n`.

The solution never modifies the array directly. It only maintains how many intervals are active at each position, which is enough to reconstruct the optimal answer.

## Worked Examples

### Example 1

Input:

```
6
1 2 1 1 4 1
```

| Position | Target Value | Active Before | Action | Active After |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | start [1,...] | 1 |
| 2 | 2 | 1 | start [2,...] | 2 |
| 3 | 1 | 2 | close [2,2] | 1 |
| 4 | 1 | 1 | nothing | 1 |
| 5 | 4 | 1 | start 3 intervals at 5 | 4 |
| 6 | 1 | 4 | close three [5,5] | 1 |

After the scan finishes, one interval remains active, so it becomes `[1,6]`.

Final intervals:

```
[2,2]
[5,5]
[5,5]
[5,5]
[1,6]
```

This trace demonstrates the central invariant. The stack size always equals the required height at the current position.

### Example 2

Input:

```
5
3 3 1 2 0
```

| Position | Target Value | Active Before | Action | Active After |
| --- | --- | --- | --- | --- |
| 1 | 3 | 0 | start 3 intervals at 1 | 3 |
| 2 | 3 | 3 | nothing | 3 |
| 3 | 1 | 3 | close two at 2 | 1 |
| 4 | 2 | 1 | start one at 4 | 2 |
| 5 | 0 | 2 | close two at 4 | 0 |

Generated intervals:

```
[1,2]
[1,2]
[4,4]
[1,4]
```

This example shows that intervals naturally split when the height decreases. The zero at the end forces every active interval to terminate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | each interval is pushed and popped once |
| Space | O(k) | stack and answer storage |

Here `k` is the number of operations in the optimal answer.

The statement guarantees `k ≤ 10^5`, so both memory usage and runtime comfortably fit within the limits. The algorithm performs only linear work and uses simple stack operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    stack = []
    ans = []

    for i in range(n):
        pos = i + 1

        while len(stack) > a[i]:
            start = stack.pop()
            ans.append((start, pos - 1))

        while len(stack) < a[i]:
            stack.append(pos)

    while stack:
        start = stack.pop()
        ans.append((start, n))

    out = [str(len(ans))]
    out.extend(f"{l} {r}" for l, r in ans)

    return "\n".join(out)

# provided sample
assert solve_io(
    "6\n1 2 1 1 4 1\n"
).startswith("5")

# minimum size
assert solve_io(
    "1\n1\n"
).startswith("1")

# all equal
assert solve_io(
    "4\n3 3 3 3\n"
).startswith("3")

# strictly increasing
assert solve_io(
    "5\n1 2 3 4 5\n"
).startswith("5")

# strictly decreasing
assert solve_io(
    "5\n5 4 3 2 1\n"
).startswith("5")

# zeros separating regions
assert solve_io(
    "3\n2 0 2\n"
).startswith("4")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | one interval | minimum-size array |
| `3 3 3 3` | three intervals | intervals can span entire array |
| `1 2 3 4 5` | five intervals | every increase starts new intervals |
| `5 4 3 2 1` | five intervals | intervals terminate gradually |
| `2 0 2` | four intervals | zeros split independent regions |

## Edge Cases

Consider the input:

```
3
2 0 2
```

At position `1`, two intervals begin.

```
stack = [1, 1]
```

At position `2`, the required value becomes zero. Both intervals must terminate at position `1`.

```
[1,1]
[1,1]
```

At position `3`, two completely new intervals begin:

```
[3,3]
[3,3]
```

The algorithm correctly prevents intervals from crossing the zero.

Now consider:

```
4
1 2 3 4
```

The stack sizes evolve as:

```
1 -> 2 -> 3 -> 4
```

Every increase forces exactly one new interval to begin. No interval ever closes before the end, producing:

```
[1,4]
[2,4]
[3,4]
[4,4]
```

This confirms the rule that increases determine the minimum number of operations.

Finally, consider:

```
5
5 4 3 2 1
```

Initially five intervals start at position `1`.

As the target decreases, intervals terminate one by one:

```
[1,1]
[1,2]
[1,3]
[1,4]
[1,5]
```

The algorithm handles shrinking coverage correctly by closing intervals exactly when the active count becomes too large.
