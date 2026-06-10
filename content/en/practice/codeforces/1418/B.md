---
title: "CF 1418B - Negative Prefixes"
description: "We have an array and a second binary array describing which positions are locked and which are unlocked. A locked position must keep its original value. An unlocked position may receive any value that originally belonged to an unlocked position."
date: "2026-06-11T06:50:21+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1418
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 95 (Rated for Div. 2)"
rating: 1300
weight: 1418
solve_time_s: 120
verified: false
draft: false
---

[CF 1418B - Negative Prefixes](https://codeforces.com/problemset/problem/1418/B)

**Rating:** 1300  
**Tags:** greedy, sortings  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We have an array and a second binary array describing which positions are locked and which are unlocked.

A locked position must keep its original value. An unlocked position may receive any value that originally belonged to an unlocked position. In other words, we are free to permute the values sitting on unlocked indices, but locked values are fixed forever.

After choosing such a rearrangement, we look at the prefix sums of the resulting array. Let $k$ be the last position whose prefix sum is negative. If every prefix sum is non-negative, then $k=0$.

Our task is to produce any valid rearrangement that makes $k$ as small as possible.

The key observation from the constraints is that $n\le100$. Even though this is small, the number of unlocked positions can also be close to 100, and trying all permutations would require up to $100!$ possibilities, which is completely impossible.

The challenge is understanding what arrangement minimizes the last negative prefix.

A subtle point is that we are not asked to maximize the number of non-negative prefixes. We only care about the position of the last negative prefix. Sometimes a prefix must stay negative because a locked negative value appears early and cannot be changed.

Another easy mistake is to think that the actual values of the prefix sums matter globally. The only freedom comes from unlocked positions, so we should focus on how to place those values to make prefixes as large as possible as early as possible.

Consider:

```
a = [-8, 4, -2, -6, 4, 7, 1]
l = [ 1, 0,  0,  0, 1, 1, 0]
```

The first element is locked and already makes the first prefix negative. We cannot fix that. The best strategy is to place the largest available unlocked values as early as possible to recover from that negative balance as soon as we can.

Another edge case occurs when every position is locked:

```
a = [2, -3, 4, -1]
l = [1,  1, 1,  1]
```

No rearrangement is allowed. The answer must be exactly the original array.

A third edge case is when all positions are unlocked:

```
a = [0, 1, -4]
l = [0, 0,  0]
```

The optimal arrangement is:

```
[1, 0, -4]
```

Putting larger values first maximizes every prefix sum and minimizes how long negative prefixes can persist.

## Approaches

A brute force solution would collect all values on unlocked positions, generate every possible permutation, rebuild the array, compute its prefix sums, determine the corresponding value of $k$, and keep the best arrangement.

This is correct because it examines every legal rearrangement. Unfortunately, if there are $m$ unlocked positions, it requires $m!$ permutations. Even for $m=15$, this is already far beyond practical limits.

The crucial observation is that we do not actually care about a particular prefix. We care about making prefix sums become non-negative as early as possible.

Suppose we look only at unlocked positions. If two unlocked positions $i<j$ contain values $x<y$, then placing $y$ at the earlier position increases every prefix sum from position $i$ onward by $y-x$. Larger values help all future prefixes when placed earlier.

This is exactly the same exchange argument used to prove that sorting in descending order maximizes all partial sums.

Take any arrangement of unlocked values. If an earlier unlocked position contains a smaller value than a later unlocked position, swapping them cannot decrease any future prefix sum. Repeating this process eventually produces the unlocked values in descending order.

That arrangement maximizes every prefix sum simultaneously. Since every prefix is as large as possible, negative prefixes disappear as early as possible, which minimizes the last position having a negative prefix.

So the solution is remarkably simple:

1. Extract all values from unlocked positions.
2. Sort them in descending order.
3. Traverse the array from left to right.
4. Whenever an unlocked position is encountered, place the next largest available value there.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m!\cdot n)$ | $O(m)$ | Too slow |
| Optimal | $O(n\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the array and the lock-status array.
2. Collect all values whose positions are unlocked, meaning their lock value is 0.
3. Sort this collection in descending order.

The largest unlocked values should appear at the earliest unlocked positions because earlier positions contribute to more prefix sums.
4. Scan the array from left to right.
5. Whenever a locked position is encountered, leave its value unchanged.
6. Whenever an unlocked position is encountered, take the next value from the sorted descending list and place it there.
7. Output the resulting array.

### Why it works

Consider two unlocked positions $i<j$. If the value at $i$ is smaller than the value at $j$, swapping them increases every prefix sum that includes position $i$ but not yet position $j$, while leaving later prefixes unchanged. No prefix sum decreases.

Thus any arrangement that is not sorted descending on unlocked positions can be improved by such a swap. Repeatedly applying this argument leads to the descending arrangement.

The descending arrangement maximizes every prefix sum among all legal rearrangements. Since each prefix sum is individually as large as possible, the point where prefix sums stop being negative occurs as early as possible. Hence the resulting value of $k$ is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        l = list(map(int, input().split()))

        free = []

        for i in range(n):
            if l[i] == 0:
                free.append(a[i])

        free.sort(reverse=True)

        ptr = 0

        for i in range(n):
            if l[i] == 0:
                a[i] = free[ptr]
                ptr += 1

        print(*a)

solve()
```

The first part gathers all values located at unlocked positions.

Sorting in descending order implements the greedy choice proven above. The largest available value is always assigned to the earliest available unlocked position.

The reconstruction phase walks through the original array. Locked positions are untouched. Unlocked positions receive values from the sorted list in order.

No prefix sums need to be computed explicitly. The proof shows that maximizing every prefix sum is equivalent to minimizing the last negative prefix.

All values fit comfortably inside Python integers, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
a = [-8, 4, -2, -6, 4, 7, 1]
l = [ 1, 0,  0,  0, 1, 1, 0]
```

Unlocked values are:

```
[4, -2, -6, 1]
```

After sorting:

```
[4, 1, -2, -6]
```

| Position | Locked? | Value placed | Result array |
| --- | --- | --- | --- |
| 1 | Yes | -8 | [-8] |
| 2 | No | 4 | [-8, 4] |
| 3 | No | 1 | [-8, 4, 1] |
| 4 | No | -2 | [-8, 4, 1, -2] |
| 5 | Yes | 4 | [-8, 4, 1, -2, 4] |
| 6 | Yes | 7 | [-8, 4, 1, -2, 4, 7] |
| 7 | No | -6 | [-8, 4, 1, -2, 4, 7, -6] |

Final array:

```
[-8, 4, 1, -2, 4, 7, -6]
```

This example shows that even though the first prefix is forced negative by a locked value, placing the largest available unlocked values early helps recover as quickly as possible.

### Example 2

Input:

```
a = [0, 1, -4, 6, 3]
l = [0, 0, 0, 1, 1]
```

Unlocked values:

```
[0, 1, -4]
```

Sorted descending:

```
[1, 0, -4]
```

| Position | Locked? | Value placed | Result array |
| --- | --- | --- | --- |
| 1 | No | 1 | [1] |
| 2 | No | 0 | [1, 0] |
| 3 | No | -4 | [1, 0, -4] |
| 4 | Yes | 6 | [1, 0, -4, 6] |
| 5 | Yes | 3 | [1, 0, -4, 6, 3] |

Final array:

```
[1, 0, -4, 6, 3]
```

This demonstrates the core greedy idea. The largest unlocked values are moved as far left as possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting the unlocked values dominates |
| Space | $O(n)$ | Storage of unlocked values |

Since $n\le100$, this solution is extremely fast. Even with 1000 test cases, sorting at most 100 numbers per case easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        l = list(map(int, input().split()))

        free = [a[i] for i in range(n) if l[i] == 0]
        free.sort(reverse=True)

        ptr = 0
        for i in range(n):
            if l[i] == 0:
                a[i] = free[ptr]
                ptr += 1

        out.append(" ".join(map(str, a)))

    return "\n".join(out)

# provided samples
assert run(
"""5
3
1 3 2
0 0 0
4
2 -3 4 -1
1 1 1 1
7
-8 4 -2 -6 4 7 1
1 0 0 0 1 1 0
5
0 1 -4 6 3
0 0 0 1 1
6
-1 7 10 4 -8 -1
1 0 0 0 0 1
"""
) == (
"""3 2 1
2 -3 4 -1
-8 4 1 -2 4 7 -6
1 0 -4 6 3
-1 10 7 4 -8 -1"""
)

# minimum size
assert run(
"""1
1
5
0
"""
) == "5"

# all locked
assert run(
"""1
4
1 2 3 4
1 1 1 1
"""
) == "1 2 3 4"

# all unlocked
assert run(
"""1
4
-1 5 2 0
0 0 0 0
"""
) == "5 2 0 -1"

# duplicate values
assert run(
"""1
5
7 7 7 7 7
0 1 0 1 0
"""
) == "7 7 7 7 7"
```

### Test Case Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | Same element | Minimum size |
| All positions locked | Original array | No rearrangement allowed |
| All positions unlocked | Descending order | Pure greedy behavior |
| All values equal | Unchanged array | Handling duplicates correctly |

## Edge Cases

Consider the case where every position is locked:

```
n = 4
a = [2, -3, 4, -1]
l = [1, 1, 1, 1]
```

The unlocked set is empty. Sorting does nothing, reconstruction does nothing, and the algorithm outputs the original array. This is the only legal answer.

Consider the case where every position is unlocked:

```
n = 3
a = [0, 1, -4]
l = [0, 0, 0]
```

The algorithm extracts all values, sorts them into:

```
[1, 0, -4]
```

and places them back. Any other arrangement gives some prefix sum that is no larger than the corresponding prefix sum of this arrangement.

Consider a forced negative prefix:

```
n = 3
a = [-10, 8, 7]
l = [1, 0, 0]
```

The first value is locked, so the first prefix is always $-10$. The algorithm sorts unlocked values into:

```
[8, 7]
```

yielding:

```
[-10, 8, 7]
```

Prefix sums become:

```
-10, -2, 5
```

The last negative prefix occurs at position 2. No rearrangement can do better because the largest available value is already used as early as possible.

Finally, consider duplicate unlocked values:

```
n = 5
a = [3, 3, -1, -1, 2]
l = [0, 0, 0, 0, 1]
```

Sorting produces:

```
[3, 3, -1, -1]
```

The reconstruction remains valid even with repeated values. The proof depends only on relative ordering, not on uniqueness.
