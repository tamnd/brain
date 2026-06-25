---
title: "CF 106123E - Dinosaur Stomp"
description: "We have an array where each value represents the number of chicken stars on a plate. Before anything is destroyed, Cole may choose exactly one position and replace its value with 0."
date: "2026-06-25T11:33:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106123
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 10-15-25 Div. 1 (Advanced)"
rating: 0
weight: 106123
solve_time_s: 47
verified: true
draft: false
---

[CF 106123E - Dinosaur Stomp](https://codeforces.com/problemset/problem/106123/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array where each value represents the number of chicken stars on a plate.

Before anything is destroyed, Cole may choose exactly one position and replace its value with `0`. After that, Barney chooses a contiguous subarray of length `k` and destroys every plate inside that segment. Barney wants to destroy as many chicken stars as possible, while Cole wants to make Barney's best possible choice as weak as possible.

The task is to determine the final number of chicken stars Barney destroys when both players act optimally.

The array size can reach `10^5`, which immediately rules out any solution that recomputes all length-`k` subarray sums after every possible choice of Cole. An `O(n^2)` algorithm would perform around `10^10` operations in the worst case, far beyond the limit.

The subtle part is that Cole changes only one position, but that position affects many different length-`k` windows. A naive implementation often updates windows one by one for every candidate position, which becomes too slow.

Consider the input

```
5 3
3 5 7 4 7
```

The length-3 window sums are:

```
[15, 16, 18]
```

If Cole removes the value `7` at position `3`, the window sums become:

```
[8, 9, 11]
```

and Barney destroys `11`.

A careless approach might only look at the currently largest window and try to weaken it. That is not enough, because after weakening one window, a different window may become the new maximum.

Another edge case appears when `k = n`.

```
4 4
1 10 4 8
```

There is only one possible window. Cole should remove the largest value, `10`, giving

```
1 + 0 + 4 + 8 = 13
```

and the answer is `13`.

Any solution must correctly handle the fact that some windows are affected by Cole's choice while others remain unchanged.

## Approaches

The brute force idea is straightforward. Compute every length-`k` window sum. Then, for each position `i`, pretend that `a[i]` becomes zero, update every window containing `i`, find the largest resulting window sum, and keep the best answer over all choices of `i`.

This is correct because it directly simulates the game. The problem is cost. A position may belong to `O(k)` windows, and there are `n` positions. In the worst case this becomes `O(nk)`, which is `O(n^2)` when `k` is large.

The key observation is that changing `a[i]` affects only the windows containing position `i`.

Let `S[j]` be the sum of the `j`-th length-`k` window.

After setting `a[i] = 0`:

```
windows containing i:  S[j] - a[i]
other windows:         S[j]
```

For a fixed position `i`, Barney's best choice is the maximum among:

```
1. The largest unaffected window.
2. The largest affected window after subtracting a[i].
```

So we need two values efficiently.

The largest unaffected window can be obtained using prefix and suffix maximum arrays over the window sums.

The largest affected window is simply:

```
max_window_sum_in_containing_range - a[i]
```

which becomes a range maximum query on the window-sum array.

Since the window sums never change, we can preprocess them once and answer every range maximum query in `O(1)` using a sparse table.

This reduces the whole problem to `O(n log n)` preprocessing and `O(n)` evaluation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Optimal | O(n log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Compute all length-`k` window sums using a sliding window.

Let the number of windows be `W = n - k + 1`.
2. Build a prefix maximum array over the window sums.

`pref[j]` stores the largest window sum among windows `1..j`.
3. Build a suffix maximum array over the window sums.

`suff[j]` stores the largest window sum among windows `j..W`.
4. Build a sparse table for range maximum queries on the window sums.

This lets us obtain the maximum window sum inside any interval in `O(1)` time.
5. For every position `i`, determine which windows contain it.

A window starting at `j` contains position `i` exactly when:

```
j ≤ i ≤ j + k - 1
```

Hence:

```
L = max(1, i - k + 1)
R = min(i, W)
```
6. Compute the largest unaffected window.

All unaffected windows lie outside `[L, R]`.

Using prefix and suffix maxima:

```
outside = max(
    pref[L - 1] if L > 1,
    suff[R + 1] if R < W
)
```
7. Compute the largest affected window.

Query the maximum window sum inside `[L, R]` and subtract `a[i]`.

```
inside = max_window_in_[L,R] - a[i]
```
8. Barney's best achievable destruction after Cole chooses `i` is

```
max(outside, inside)
```
9. Take the minimum value over all positions `i`.

### Why it works

For a fixed position `i`, every window belongs to exactly one of two groups.

Windows containing `i` lose exactly `a[i]` from their sum. Windows not containing `i` remain unchanged.

Barney chooses the largest resulting window, so the answer for that position is the maximum between the best unaffected window and the best affected window. The algorithm computes both quantities exactly.

Since every possible position `i` is examined and Cole chooses the position producing the smallest such value, the final answer is exactly the minimax value of the game.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

w = n - k + 1

# window sums
S = [0] * w
cur = sum(a[:k])
S[0] = cur

for i in range(k, n):
    cur += a[i] - a[i - k]
    S[i - k + 1] = cur

# prefix max
pref = [0] * w
pref[0] = S[0]
for i in range(1, w):
    pref[i] = max(pref[i - 1], S[i])

# suffix max
suff = [0] * w
suff[-1] = S[-1]
for i in range(w - 2, -1, -1):
    suff[i] = max(suff[i + 1], S[i])

# sparse table for RMQ max
lg = [0] * (w + 1)
for i in range(2, w + 1):
    lg[i] = lg[i // 2] + 1

K = lg[w] + 1
st = [S[:]]

j = 1
while (1 << j) <= w:
    prev = st[j - 1]
    length = w - (1 << j) + 1
    row = [0] * length
    half = 1 << (j - 1)

    for i in range(length):
        row[i] = max(prev[i], prev[i + half])

    st.append(row)
    j += 1

def range_max(l, r):
    length = r - l + 1
    p = lg[length]
    return max(st[p][l], st[p][r - (1 << p) + 1])

INF = 10**30
answer = INF

for idx in range(n):
    L = max(0, idx - k + 1)
    R = min(idx, w - 1)

    outside = 0

    if L > 0:
        outside = max(outside, pref[L - 1])

    if R + 1 < w:
        outside = max(outside, suff[R + 1])

    inside = range_max(L, R) - a[idx]

    answer = min(answer, max(outside, inside))

print(answer)
```

The first section computes all length-`k` window sums in linear time using a standard sliding window.

The prefix and suffix arrays allow us to obtain the largest window outside any interval without scanning the array again.

The sparse table stores range maxima of the window-sum array. Since the array never changes, a sparse table is ideal because it provides `O(1)` maximum queries after preprocessing.

One implementation detail that is easy to miss is the conversion between positions and window indices. The code uses zero-based indexing, so the containing-window interval becomes:

```
L = max(0, idx - k + 1)
R = min(idx, w - 1)
```

Another subtle point is when every window contains the chosen position. In that case there are no unaffected windows. The variable `outside` remains `0`, which is correct because all array values are positive and every real window sum is nonnegative.

## Worked Examples

### Example 1

Input:

```
5 3
3 5 7 4 7
```

Window sums:

```
[15, 16, 18]
```

| Position | Value Removed | Containing Windows | Largest Inside Before Removal | Inside After Removal | Outside Max | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | [15] | 15 | 12 | 18 | 18 |
| 2 | 5 | [15,16] | 16 | 11 | 18 | 18 |
| 3 | 7 | [15,16,18] | 18 | 11 | 0 | 11 |
| 4 | 4 | [16,18] | 18 | 14 | 15 | 15 |
| 5 | 7 | [18] | 18 | 11 | 16 | 16 |

The minimum result is `11`.

This example shows the situation where removing a value from a position shared by many windows is much more effective than removing it from a boundary position.

### Example 2

Input:

```
4 4
1 10 4 8
```

Window sums:

```
[23]
```

| Position | Value Removed | Inside After Removal | Outside Max | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | 22 | 0 | 22 |
| 2 | 10 | 13 | 0 | 13 |
| 3 | 4 | 19 | 0 | 19 |
| 4 | 8 | 15 | 0 | 15 |

The minimum result is `13`.

This demonstrates the special case where only one window exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Window sums, prefix/suffix arrays, and sparse table construction |
| Space | O(n log n) | Sparse table storage |

With `n ≤ 100000`, an `O(n log n)` solution comfortably fits within typical competitive programming limits. The range maximum queries become constant time after preprocessing, allowing every position to be evaluated efficiently.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    w = n - k + 1

    S = [0] * w
    cur = sum(a[:k])
    S[0] = cur

    for i in range(k, n):
        cur += a[i] - a[i - k]
        S[i - k + 1] = cur

    pref = [0] * w
    pref[0] = S[0]
    for i in range(1, w):
        pref[i] = max(pref[i - 1], S[i])

    suff = [0] * w
    suff[-1] = S[-1]
    for i in range(w - 2, -1, -1):
        suff[i] = max(suff[i + 1], S[i])

    lg = [0] * (w + 1)
    for i in range(2, w + 1):
        lg[i] = lg[i // 2] + 1

    K = lg[w] + 1
    st = [S[:]]

    j = 1
    while (1 << j) <= w:
        prev = st[j - 1]
        length = w - (1 << j) + 1
        row = [0] * length
        half = 1 << (j - 1)

        for i in range(length):
            row[i] = max(prev[i], prev[i + half])

        st.append(row)
        j += 1

    def rmq(l, r):
        length = r - l + 1
        p = lg[length]
        return max(st[p][l], st[p][r - (1 << p) + 1])

    ans = 10**30

    for idx in range(n):
        L = max(0, idx - k + 1)
        R = min(idx, w - 1)

        outside = 0

        if L > 0:
            outside = max(outside, pref[L - 1])

        if R + 1 < w:
            outside = max(outside, suff[R + 1])

        inside = rmq(L, R) - a[idx]

        ans = min(ans, max(outside, inside))

    return str(ans) + "\n"

# provided samples
assert run("5 3\n3 5 7 4 7\n") == "11\n", "sample 1"
assert run("4 4\n1 10 4 8\n") == "13\n", "sample 2"

# custom cases
assert run("1 1\n5\n") == "0\n", "single element"
assert run("5 1\n4 4 4 4 4\n") == "4\n", "k equals 1"
assert run("5 5\n7 7 7 7 7\n") == "28\n", "single window all equal"
assert run("3 2\n1 100 1\n") == "1\n", "boundary overlap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5` | `0` | Minimum possible size |
| `5 1 / 4 4 4 4 4` | `4` | Every window has length 1 |
| `5 5 / 7 7 7 7 7` | `28` | Single window covering entire array |
| `3 2 / 1 100 1` | `1` | Position shared by multiple windows |

## Edge Cases

Consider:

```
1 1
5
```

There is only one plate and one window. Cole sets that plate to zero. The only window sum becomes zero, so Barney destroys zero chicken stars. The algorithm computes one window sum equal to `5`, then evaluates the only position and obtains `5 - 5 = 0`.

Consider:

```
4 4
1 10 4 8
```

Every window contains every position because there is only one window. For position `2`, the affected-window maximum is `23 - 10 = 13` and there are no unaffected windows. The algorithm correctly leaves `outside = 0` and returns `13`.

Consider:

```
3 2
1 100 1
```

The window sums are `[101, 101]`. Removing the middle value affects both windows simultaneously, producing `[1, 1]`. The algorithm identifies that the containing-window interval covers all windows and computes:

```
inside = 101 - 100 = 1
outside = 0
```

giving the correct answer `1`.

These cases verify that the interval computation for affected windows, the handling of missing unaffected windows, and the minimax logic all behave correctly.
