---
title: "CF 2193C - Replace and Sum"
description: "We start with two arrays of the same length. For any position, we may directly overwrite a[i] with b[i]. We may also copy values from right to left by replacing a[i] with the current value of a[i+1]. Each query asks for the largest possible sum on a subarray a[l.."
date: "2026-06-07T20:50:05+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2193
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1076 (Div. 3)"
rating: 1000
weight: 2193
solve_time_s: 172
verified: true
draft: false
---

[CF 2193C - Replace and Sum](https://codeforces.com/problemset/problem/2193/C)

**Rating:** 1000  
**Tags:** data structures, greedy  
**Solve time:** 2m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with two arrays of the same length.

For any position, we may directly overwrite `a[i]` with `b[i]`. We may also copy values from right to left by replacing `a[i]` with the current value of `a[i+1]`.

Each query asks for the largest possible sum on a subarray `a[l..r]` after performing any number of these operations.

The key detail is that every query is independent. We are not required to keep the modifications made for one query when answering another query.

The constraints immediately rule out any approach that simulates operations for each query. Across all test cases, both the total array size and the total number of queries can reach `2 * 10^5`. An `O(nq)` solution could require around `4 * 10^10` operations, which is far beyond what fits in a 2-second limit. We need preprocessing that allows each query to be answered in constant or logarithmic time.

The most subtle part of the problem is understanding what values can eventually appear at a position.

Consider:

```
a = [3, 2, 1]
b = [1, 2, 3]
```

Position 1 can eventually become `3`. We set position 3 to `b[3]=3`, copy it to position 2, then copy position 2 to position 1.

A common mistake is to think that position `i` can only choose between `a[i]` and `b[i]`. Here position 1 reaches a value originating from position 3.

Another easy mistake is to assume that the best value for position `i` is the maximum element strictly to its right.

Consider:

```
a = [10]
b = [1]
```

There is no right neighbor at all. The correct maximum value at position 1 is still `10`, because we may simply leave it unchanged.

A third trap is overlooking that copied values may themselves have been created using `b`.

Consider:

```
a = [1, 1]
b = [1, 100]
```

Position 1 can become `100` by first setting position 2 to `100` and then copying left. Any reasoning based only on the original array `a` misses this possibility.

## Approaches

A brute-force view is to answer each query independently. One could try to determine the best sequence of operations and compute the maximum achievable sum on the requested segment.

This works conceptually because the operations are simple and local. The problem is that even describing the space of possible states is enormous. With up to `2 * 10^5` positions and `2 * 10^5` queries, any per-query simulation is hopelessly slow.

The breakthrough comes from studying a single position.

Take some index `i`. Every copy operation moves information from right to left. Because of that, any value that finally appears at position `i` must originate from some position `j ≥ i`.

At position `j`, the largest value we can make available is:

```
max(a[j], b[j])
```

since we may either keep `a[j]` or overwrite it with `b[j]`.

Define:

```
t[j] = max(a[j], b[j])
```

Then the largest value that can ever reach position `i` is:

```
s[i] = max(t[j]) for all j ≥ i
```

which is simply a suffix maximum.

No final value at position `i` can exceed `s[i]`, because every reachable source lies in the suffix starting at `i`.

Even better, the entire array `s` is actually achievable. If `t[i] = s[i]`, we place that value directly at position `i`. Otherwise `s[i] = s[i+1]`, so we copy from the right.

This means that for every position:

```
best possible value at i = s[i]
```

The maximum possible sum on any query interval is therefore just the sum of `s[l..r]`.

After computing the suffix maxima array once, we build prefix sums and answer every query in `O(1)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / at least O(nq) | Large | Too slow |
| Optimal | O(n + q) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For every position `i`, compute

```
t[i] = max(a[i], b[i])
```

This is the largest value that position `i` itself can contribute as a source.
2. Build a suffix maximum array `s`.

```
s[n] = t[n]
s[i] = max(t[i], s[i+1])
```

`s[i]` represents the largest value that can ever reach position `i`.
3. Build prefix sums of `s`.

```
pref[0] = 0
pref[i] = pref[i-1] + s[i]
```
4. For a query `(l, r)`, return

```
pref[r] - pref[l-1]
```

because the optimal achievable array is exactly `s`.

### Why it works

Every value that ends up at position `i` must originate from some position `j ≥ i`, since all copying moves leftward. The greatest source value available at position `j` is `max(a[j], b[j])`. Consequently, no final value at position `i` can exceed the maximum of those quantities over the entire suffix, namely `s[i]`.

This gives an upper bound on every position.

The array `s` itself is achievable. Whenever `t[i] = s[i]`, we create that value directly at position `i`. Otherwise the suffix maximum comes from somewhere to the right, meaning `s[i] = s[i+1]`, and we obtain it by copying from position `i+1`.

Since each position can simultaneously attain its upper bound, the optimal final array is exactly `s`, and every query answer is the sum of the corresponding interval in `s`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        s = [0] * n

        cur = 0
        for i in range(n - 1, -1, -1):
            cur = max(cur, a[i], b[i])
            s[i] = cur

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + s[i]

        ans = []
        for _ in range(q):
            l, r = map(int, input().split())
            ans.append(str(pref[r] - pref[l - 1]))

        out.append(" ".join(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first loop computes the suffix maxima directly. The variable `cur` stores the largest value seen so far while scanning from right to left. Since `cur` always equals the maximum of all `max(a[j], b[j])` in the processed suffix, assigning `s[i] = cur` produces exactly the array described in the proof.

The prefix-sum array uses one-based indexing. This avoids special handling when `l = 1`, since every interval sum becomes the standard expression:

```
pref[r] - pref[l - 1]
```

All values fit comfortably in Python integers. The largest possible query sum is roughly `2 * 10^5 * 10^4 = 2 * 10^9`, which is still well within 64-bit range.

## Worked Examples

### Example 1

Input:

```
a = [3, 2, 1]
b = [1, 2, 3]
query = [1, 3]
```

First compute suffix maxima.

| i | max(a[i], b[i]) | Current suffix maximum | s[i] |
| --- | --- | --- | --- |
| 3 | 3 | 3 | 3 |
| 2 | 2 | 3 | 3 |
| 1 | 3 | 3 | 3 |

So:

```
s = [3, 3, 3]
```

Prefix sums:

| Position | Prefix Sum |
| --- | --- |
| 0 | 0 |
| 1 | 3 |
| 2 | 6 |
| 3 | 9 |

Answer:

```
pref[3] - pref[0] = 9
```

This demonstrates how a value created at the far right can propagate all the way to the left.

### Example 2

Input:

```
a = [4, 3, 2, 1]
b = [5, 1, 3, 1]
queries:
(1,2)
(2,4)
(3,4)
```

Suffix construction:

| i | max(a[i], b[i]) | Current suffix maximum | s[i] |
| --- | --- | --- | --- |
| 4 | 1 | 1 | 1 |
| 3 | 3 | 3 | 3 |
| 2 | 3 | 3 | 3 |
| 1 | 5 | 5 | 5 |

Thus:

```
s = [5, 3, 3, 1]
```

Prefix sums:

| Position | Prefix Sum |
| --- | --- |
| 0 | 0 |
| 1 | 5 |
| 2 | 8 |
| 3 | 11 |
| 4 | 12 |

Query results:

| Query | Computation | Answer |
| --- | --- | --- |
| (1,2) | 8 - 0 | 8 |
| (2,4) | 12 - 5 | 7 |
| (3,4) | 12 - 8 | 4 |

This example shows that different positions may have different optimal values, determined solely by suffix maxima.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test case | One suffix pass, one prefix pass, then O(1) per query |
| Space | O(n) | Stores suffix maxima and prefix sums |

The total sum of all `n` and all `q` over the entire input is at most `2 * 10^5`, so the overall runtime is linear in the input size and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        s = [0] * n
        cur = 0
        for i in range(n - 1, -1, -1):
            cur = max(cur, a[i], b[i])
            s[i] = cur

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + s[i]

        ans = []
        for _ in range(q):
            l, r = map(int, input().split())
            ans.append(str(pref[r] - pref[l - 1]))

        out.append(" ".join(ans))

    return "\n".join(out)

# provided sample
assert run(
"""4
3 1
3 2 1
1 2 3
1 3
1 1
1
2
1 1
3 2
6 7 5
9 6 8
1 2
2 3
4 3
4 3 2 1
5 1 3 1
1 2
2 4
3 4
"""
) == """9
2
17 16
8 7 4"""

# minimum size
assert run(
"""1
1 1
5
3
1 1
"""
) == "5"

# propagation from far right
assert run(
"""1
2 1
1 1
1 100
1 2
"""
) == "200"

# all equal values
assert run(
"""1
4 2
7 7 7 7
7 7 7 7
1 4
2 3
"""
) == "28 14"

# boundary interval ending at n
assert run(
"""1
3 2
1 5 2
4 3 6
1 3
3 3
"""
) == "18 6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | 5 | Smallest valid instance |
| Large value only in `b[n]` | 200 | Propagation from rightmost position |
| All values equal | 28 14 | Stability when every choice is identical |
| Query touching last index | 18 6 | Prefix-sum boundaries and suffix construction |

## Edge Cases

Consider:

```
1
2 1
1 1
1 100
1 2
```

We have `t = [1, 100]`, so the suffix maxima array is:

```
s = [100, 100]
```

The answer is `200`.

A solution that only looks at `a` would produce `2`, which is incorrect because position 2 can first become `100` and then propagate left.

Now consider:

```
1
1 1
10
1
1 1
```

There is no right neighbor. The suffix maximum array is:

```
s = [10]
```

The answer is `10`.

Any solution that assumes every value must come from copying would miss the possibility of simply leaving `a[1]` unchanged.

Finally, consider:

```
1
3 1
3 2 1
1 2 3
1 3
```

The suffix maxima array becomes:

```
s = [3, 3, 3]
```

The answer is `9`.

This confirms the central invariant: every position is bounded by the maximum attainable source value in its suffix, and that bound is always achievable.
