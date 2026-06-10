---
title: "CF 1501B - Napoleon Cake"
description: "We build the cake layer by layer. After placing the i-th layer, we pour a[i] units of cream onto the top. That cream spreads downward and covers the top a[i] layers currently present. If there are fewer than a[i] layers, every existing layer becomes covered."
date: "2026-06-10T21:02:10+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1501
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 707 (Div. 2, based on Moscow Open Olympiad in Informatics)"
rating: 900
weight: 1501
solve_time_s: 135
verified: false
draft: false
---

[CF 1501B - Napoleon Cake](https://codeforces.com/problemset/problem/1501/B)

**Rating:** 900  
**Tags:** dp, implementation, sortings  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We build the cake layer by layer. After placing the `i`-th layer, we pour `a[i]` units of cream onto the top. That cream spreads downward and covers the top `a[i]` layers currently present. If there are fewer than `a[i]` layers, every existing layer becomes covered.

For each layer, we must decide whether it is covered by at least one cream operation. The output is an array of zeros and ones, ordered from bottom to top. A value of `1` means that layer is drenched, while `0` means it remains dry.

The total number of layers across all test cases is at most `2·10^5`, which is small enough for a linear solution but too large for anything quadratic. A method that examines every affected layer for every pouring operation could require about `n²` work in the worst case. With `n = 2·10^5`, that would mean around forty billion operations, which is far beyond the time limit.

Several situations are easy to mishandle.

One case is when the amount of cream exceeds the number of existing layers.

Input:

```
1
4
5 0 0 0
```

The first operation already covers all existing layers, so the answer is

```
1 0 0 0
```

A careless implementation that tries to access layers below the bottom may produce invalid indices.

Another tricky case comes from overlapping intervals.

Input:

```
1
6
0 3 0 0 1 3
```

The correct answer is

```
1 1 0 1 1 1
```

Multiple cream operations cover some layers repeatedly, but a layer only needs to be covered once. Simulating every operation independently wastes time.

A third case is when no cream is poured.

Input:

```
1
3
0 0 0
```

The answer is

```
0 0 0
```

If we incorrectly propagate previous coverage after it should have ended, some layers may be marked as covered even though no operation reaches them.

## Approaches

The most direct solution is to process every pouring operation and explicitly mark the layers it affects. When we are at position `i`, the cream reaches from layer `i` downward for `a[i]` positions. We could iterate through those layers and mark them as covered.

This approach is correct because every affected layer gets visited at least once. The problem appears when many values are large. For example, if every `a[i] = n`, the first operation touches one layer, the second touches two, and so on, leading to roughly

$$1 + 2 + \dots + n = O(n^2)$$

operations.

The structure of the problem suggests a better view. Every pouring operation creates a contiguous segment of layers that become covered. Instead of marking the whole segment immediately, we can process the layers from top to bottom and remember how many more positions downward are still inside some active cream interval.

Suppose we are currently at layer `i` and there are `cur` layers remaining from intervals that started above. Then layer `i` is covered whenever `cur > 0`. If `a[i]` itself is larger than `cur`, a new interval beginning at `i` extends the coverage farther downward, so we update

```
cur = max(cur, a[i])
```

After handling the current layer, we move one layer lower and decrease `cur` by one.

Processing from top to bottom turns many overlapping intervals into a single counter, giving linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start from the top layer and move toward the bottom.
2. Maintain a variable `cur`, representing how many consecutive layers, including the current one, are still covered by cream coming from layers above.
3. At position `i`, update `cur = max(cur, a[i])`.

If a new pouring operation reaches farther downward than previous ones, its effect replaces the old range. Otherwise, the previous coverage is already sufficient.
4. If `cur > 0`, mark layer `i` as covered.

A positive value means at least one cream interval includes this layer.
5. After processing the layer, decrease `cur` by one, but never below zero.

Moving one step downward consumes one layer of remaining coverage.
6. Continue until reaching the bottom layer.

### Why it works

While scanning downward, `cur` always equals the number of consecutive layers starting from the current one that are guaranteed to be covered by some cream operation already encountered. Every pouring operation starts at its own position and extends downward for exactly `a[i]` layers. Taking the maximum between the existing value and `a[i]` keeps the longest interval currently affecting lower layers. Decreasing `cur` after each step correctly removes one layer from the remaining range. Since a layer is marked covered exactly when some interval reaches it, the algorithm produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    ans = [0] * n
    cur = 0

    for i in range(n - 1, -1, -1):
        cur = max(cur, a[i])
        if cur > 0:
            ans[i] = 1
        cur = max(0, cur - 1)

    out.append(" ".join(map(str, ans)))

print("\n".join(out))
```

The scan runs from right to left because the top layer corresponds to the largest index. The variable `cur` stores the remaining depth of coverage. Before deciding the state of layer `i`, we incorporate the cream poured at that layer by taking the maximum with `a[i]`.

The order of operations matters. We first update `cur`, then decide whether the current layer is covered, and only afterward decrease `cur`. Reversing these steps would shorten every interval by one and produce incorrect answers.

The call to `max(0, cur - 1)` prevents negative values. Although negative numbers would still make the condition `cur > 0` false, keeping `cur` nonnegative makes the meaning of the variable precise.

## Worked Examples

Consider the first sample.

Input:

```
6
0 3 0 0 1 3
```

| i | a[i] | cur before update | cur after update | ans[i] | cur after decrement |
| --- | --- | --- | --- | --- | --- |
| 5 | 3 | 0 | 3 | 1 | 2 |
| 4 | 1 | 2 | 2 | 1 | 1 |
| 3 | 0 | 1 | 1 | 1 | 0 |
| 2 | 0 | 0 | 0 | 0 | 0 |
| 1 | 3 | 0 | 3 | 1 | 2 |
| 0 | 0 | 2 | 2 | 1 | 1 |

Final answer:

```
1 1 0 1 1 1
```

This example shows how a large interval started at index 5 keeps affecting lower layers until its counter reaches zero.

Consider another example.

Input:

```
10
0 0 0 1 0 5 0 0 0 2
```

| i | a[i] | cur before update | cur after update | ans[i] | cur after decrement |
| --- | --- | --- | --- | --- | --- |
| 9 | 2 | 0 | 2 | 1 | 1 |
| 8 | 0 | 1 | 1 | 1 | 0 |
| 7 | 0 | 0 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 |
| 5 | 5 | 0 | 5 | 1 | 4 |
| 4 | 0 | 4 | 4 | 1 | 3 |
| 3 | 1 | 3 | 3 | 1 | 2 |
| 2 | 0 | 2 | 2 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 |

Final answer:

```
0 1 1 1 1 1 0 0 1 1
```

This trace demonstrates how overlapping intervals are naturally merged by keeping only the largest remaining coverage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each layer is processed exactly once |
| Space | O(n) | The answer array stores one value per layer |

Since the total number of layers across all test cases is at most `2·10^5`, a linear algorithm performs only a few hundred thousand iterations. This comfortably fits within the time limit and memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans = [0] * n
        cur = 0

        for i in range(n - 1, -1, -1):
            cur = max(cur, a[i])
            if cur > 0:
                ans[i] = 1
            cur = max(0, cur - 1)

        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# provided samples
assert run(
"""3
6
0 3 0 0 1 3
10
0 0 0 1 0 5 0 0 0 2
3
0 0 0
"""
) == """1 1 0 1 1 1
0 1 1 1 1 1 0 0 1 1
0 0 0"""

# minimum size
assert run(
"""1
1
0
"""
) == "0"

# single layer covered
assert run(
"""1
1
1
"""
) == "1"

# all values equal
assert run(
"""1
5
5 5 5 5 5
"""
) == "1 1 1 1 1"

# off-by-one case
assert run(
"""1
5
0 0 0 0 1
"""
) == "0 0 0 0 1"

# large interval near the end
assert run(
"""1
5
0 0 0 3 0
"""
) == "0 1 1 1 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 0` | `0` | Minimum size |
| `1 / 1 / 1` | `1` | Single covered layer |
| `5 / 5 5 5 5 5` | `1 1 1 1 1` | Large overlapping intervals |
| `5 / 0 0 0 0 1` | `0 0 0 0 1` | Boundary at the top layer |
| `5 / 0 0 0 3 0` | `0 1 1 1 0` | Interval length off-by-one errors |

## Edge Cases

Consider the case where the amount of cream exceeds the number of existing layers.

Input:

```
1
4
5 0 0 0
```

Scanning from right to left gives:

| i | a[i] | cur after update | ans[i] |
| --- | --- | --- | --- |
| 3 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 0 | 5 | 5 | 1 |

The answer becomes

```
1 0 0 0
```

The algorithm never needs to access nonexistent layers. It only stores the remaining coverage length.

Now consider overlapping intervals.

Input:

```
1
5
0 2 0 3 0
```

At index 3, a length-three interval starts. When index 1 is reached, its interval is shorter than the remaining coverage, so `max(cur, a[i])` keeps the longer one. The answer is

```
1 1 1 1 0
```

No layer is counted twice, and no extra work is done.

Finally, consider the case with no cream.

Input:

```
1
3
0 0 0
```

The variable `cur` remains zero throughout the scan.

| i | cur after update | ans[i] |
| --- | --- | --- |
| 2 | 0 | 0 |
| 1 | 0 | 0 |
| 0 | 0 | 0 |

The output is

```
0 0 0
```

Since the coverage counter never becomes positive, every layer correctly stays dry.
