---
title: "CF 452F - Permutation"
description: "We are given a permutation of the numbers 1...n. For two distinct values a and b, their average is (a+b)/2. Since the permutation contains every integer exactly once, this average is also present whenever a+b is even."
date: "2026-06-07T17:10:09+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "hashing"]
categories: ["algorithms"]
codeforces_contest: 452
codeforces_index: "F"
codeforces_contest_name: "MemSQL Start[c]UP 2.0 - Round 1"
rating: 2700
weight: 452
solve_time_s: 174
verified: true
draft: false
---

[CF 452F - Permutation](https://codeforces.com/problemset/problem/452/F)

**Rating:** 2700  
**Tags:** data structures, divide and conquer, hashing  
**Solve time:** 2m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers `1...n`. For two distinct values `a` and `b`, their average is `(a+b)/2`. Since the permutation contains every integer exactly once, this average is also present whenever `a+b` is even.

The question is whether there exists a pair `a, b` such that their average appears somewhere between them in the permutation order.

A more useful reformulation is to look at arithmetic progressions in value space. Let

$$a = x-k,\qquad b = x+k.$$

Then `x` is exactly the average of `a` and `b`. The task becomes:

Does there exist a value `x` and a distance `k > 0` such that the position of `x` in the permutation lies strictly between the positions of `x-k` and `x+k`?

The size of the permutation can reach `300000`. Any algorithm that explicitly checks all pairs or all arithmetic progressions is immediately ruled out. Even an `O(n^2)` solution would require roughly `9·10^{10}` operations in the worst case, which is far beyond the limit.

The tricky part is that the condition mixes two different orderings. Values are compared in arithmetic progression order, while "between" refers to positions inside the permutation.

Consider the permutation

```
1 5 2 4 3
```

The value `2` lies between `1` and `3`, so the answer is `YES`.

Now consider

```
1 3 4 2
```

For the only possible progression `(1,2,3)`, the value `2` is not between `1` and `3`. The answer is `NO`.

A common mistake is to examine only adjacent values or only progressions of length three in the permutation order. The arithmetic progression is defined on the values themselves, not on neighboring positions.

## Approaches

The brute-force idea is straightforward. For every possible center value `x`, try every distance `k` such that `x-k` and `x+k` remain inside `1...n`. Using the stored positions of all values, we can check whether the position of `x` lies between the positions of the two endpoints.

This is correct because every valid answer corresponds to exactly one center `x` and one distance `k`. The problem is the running time. There are `Θ(n^2)` possible pairs `(x,k)`, which is much too large for `n = 300000`.

The key observation appears when we process the permutation from left to right.

Suppose we are currently visiting value `x`.

Every value already seen lies to the left of `x` in the permutation. Every value not yet seen lies to the right of `x`.

Define a binary array over the value axis:

```
0 = already processed
1 = not processed yet
```

When we arrive at `x`, we change the state of value `x` from `1` to `0`.

Now look at a symmetric pair of values:

```
x-k , x+k
```

If their states are different, then one of them is already processed and the other is not. That means one endpoint lies to the left of `x` and the other lies to the right of `x`. Hence `x` is between them in the permutation, and we have found a valid arithmetic progression.

So for every processed value `x`, we only need to know whether the binary sequence around `x`

```
[x-t ... x+t]
```

with

```
t = min(x-1, n-x)
```

is symmetric around the center.

If the sequence is perfectly symmetric, then every pair `(x-k, x+k)` has equal states.

If the sequence is not symmetric, some pair has different states, which immediately gives a valid answer.

Checking symmetry of a range is a classic rolling-hash task. We maintain the binary array in a segment tree storing both forward and reverse hashes. After updating one position, we query the largest symmetric interval around `x` and test whether its forward hash equals its reverse hash.

The first non-palindromic interval proves the answer is `YES`. If every interval remains palindromic, the answer is `NO`. This is the intended `O(n log n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal (segment tree + hashing) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a binary array over values `1...n`.

Initially every entry is `1`, meaning that value has not yet appeared in the permutation.
2. Build a segment tree over this array.

Each node stores the length of its segment, its forward rolling hash, and its reverse rolling hash.
3. Process the permutation from left to right.

When value `x` is visited, update position `x` in the segment tree from `1` to `0`.
4. Let

$$t=\min(x-1,n-x).$$

This is the largest distance for which both `x-t` and `x+t` exist.
5. Query the interval

$$[x-t,\;x+t].$$

Obtain its forward hash and reverse hash.
6. If the hashes differ, the interval is not a palindrome.

Then there exists some distance `k` such that the states of `x-k` and `x+k` are different.
7. Different states mean one endpoint is already processed and the other is not.

One endpoint is on the left side of `x` in the permutation and the other is on the right side.
8. The value `x` lies between the two endpoints, so a valid pair exists.

Print `"YES"` and stop.
9. If all values are processed without finding such an interval, print `"NO"`.

### Why it works

At the moment value `x` is processed, every value marked `0` appears before `x` in the permutation, and every value marked `1` appears after `x`.

For any distance `k`, the pair `(x-k, x+k)` contributes a valid arithmetic progression exactly when their states differ. One endpoint then lies before `x` and the other after `x`, placing `x` between them.

The symmetric interval around `x` is a palindrome if and only if every symmetric pair has equal states. A non-palindromic interval is equivalent to the existence of a pair with different states, which is equivalent to the existence of a valid arithmetic progression centered at `x`.

The algorithm checks this condition for every possible center value, so it finds an answer whenever one exists and never reports a false positive.

## Python Solution

```python
import sys
input = sys.stdin.readline

MASK = (1 << 64) - 1
BASE = 911382323

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    powb = [1] * (n + 1)
    for i in range(1, n + 1):
        powb[i] = (powb[i - 1] * BASE) & MASK

    size = 1
    while size < n:
        size <<= 1

    seg_len = [0] * (2 * size)
    seg_f = [0] * (2 * size)
    seg_r = [0] * (2 * size)

    for i in range(size):
        idx = size + i
        seg_len[idx] = 1
        if i < n:
            seg_f[idx] = 1
            seg_r[idx] = 1

    for v in range(size - 1, 0, -1):
        l = v * 2
        r = l + 1

        len_l = seg_len[l]
        len_r = seg_len[r]

        seg_len[v] = len_l + len_r

        seg_f[v] = (
            seg_f[l] + (seg_f[r] * powb[len_l])
        ) & MASK

        seg_r[v] = (
            seg_r[r] + (seg_r[l] * powb[len_r])
        ) & MASK

    def update(pos):
        v = size + pos - 1
        seg_f[v] = 0
        seg_r[v] = 0

        v //= 2
        while v:
            l = v * 2
            r = l + 1

            len_l = seg_len[l]
            len_r = seg_len[r]

            seg_f[v] = (
                seg_f[l] + (seg_f[r] * powb[len_l])
            ) & MASK

            seg_r[v] = (
                seg_r[r] + (seg_r[l] * powb[len_r])
            ) & MASK

            v //= 2

    def combine(a, b):
        len_a, f_a, r_a = a
        len_b, f_b, r_b = b

        return (
            len_a + len_b,
            (f_a + f_b * powb[len_a]) & MASK,
            (r_b + r_a * powb[len_b]) & MASK,
        )

    def query(l, r):
        l = l + size - 1
        r = r + size - 1

        left = (0, 0, 0)
        right = (0, 0, 0)

        while l <= r:
            if l & 1:
                left = combine(left, (seg_len[l], seg_f[l], seg_r[l]))
                l += 1

            if not (r & 1):
                right = combine((seg_len[r], seg_f[r], seg_r[r]), right)
                r -= 1

            l //= 2
            r //= 2

        return combine(left, right)

    for x in p:
        update(x)

        t = min(x - 1, n - x)
        if t == 0:
            continue

        length, fh, rh = query(x - t, x + t)

        if fh != rh:
            print("YES")
            return

    print("NO")

solve()
```

The segment tree stores a rolling hash for every interval in both directions. A range query returns the forward hash and reverse hash of the requested interval. Equality means the interval is a palindrome.

The update operation changes a single value from `1` to `0`. This corresponds exactly to moving a value from the "unseen" set to the "already processed" set.

The largest symmetric interval around `x` is used because every possible pair `(x-k, x+k)` must be examined. Any mismatch anywhere inside that interval produces the required arithmetic progression.

A subtle point is the order of operations. We must update `x` before checking the interval. At the moment of the check, `x` itself belongs to the processed side, which matches the invariant that every `0` corresponds to a value appearing no later than the current position.

Using 64-bit hashing keeps the implementation compact and fast. Collisions are theoretically possible but negligible in practice for competitive programming.

## Worked Examples

### Example 1

Input:

```
4
1 3 4 2
```

| Current value x | Binary state after update (values 1..4) | Queried interval | Palindrome? |
| --- | --- | --- | --- |
| 1 | 0 1 1 1 | none | - |
| 3 | 0 1 0 1 | [2,4] = 1 0 1 | Yes |
| 4 | 0 1 0 0 | none | - |
| 2 | 0 0 0 0 | [1,3] = 0 0 0 | Yes |

No queried interval is non-palindromic, so no center value has endpoints on opposite sides. The answer is `NO`.

### Example 2

Input:

```
5
1 5 2 4 3
```

| Current value x | Binary state after update (values 1..5) | Queried interval | Palindrome? |
| --- | --- | --- | --- |
| 1 | 0 1 1 1 1 | none | - |
| 5 | 0 1 1 1 0 | none | - |
| 2 | 0 0 1 1 0 | [1,3] = 0 0 1 | No |

For `x = 2`, the symmetric pair `(1,3)` has states `(0,1)`. Value `1` is left of `2` in the permutation and value `3` is right of `2`. Thus `2` lies between them and the answer is `YES`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | One update and one range query per permutation element |
| Space | O(n) | Segment tree and power arrays |

With `n = 300000`, an `O(n log n)` algorithm performs only a few million segment tree operations, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    MASK = (1 << 64) - 1
    BASE = 911382323

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    p = list(map(int, input().split()))

    powb = [1] * (n + 1)
    for i in range(1, n + 1):
        powb[i] = (powb[i - 1] * BASE) & MASK

    size = 1
    while size < n:
        size <<= 1

    seg_len = [0] * (2 * size)
    seg_f = [0] * (2 * size)
    seg_r = [0] * (2 * size)

    for i in range(size):
        idx = size + i
        seg_len[idx] = 1
        if i < n:
            seg_f[idx] = 1
            seg_r[idx] = 1

    for v in range(size - 1, 0, -1):
        l = v * 2
        r = l + 1
        seg_len[v] = seg_len[l] + seg_len[r]
        seg_f[v] = (seg_f[l] + seg_f[r] * powb[seg_len[l]]) & MASK
        seg_r[v] = (seg_r[r] + seg_r[l] * powb[seg_len[r]]) & MASK

    def update(pos):
        v = size + pos - 1
        seg_f[v] = seg_r[v] = 0
        v //= 2
        while v:
            l = v * 2
            r = l + 1
            seg_f[v] = (seg_f[l] + seg_f[r] * powb[seg_len[l]]) & MASK
            seg_r[v] = (seg_r[r] + seg_r[l] * powb[seg_len[r]]) & MASK
            v //= 2

    def combine(a, b):
        la, fa, ra = a
        lb, fb, rb = b
        return (
            la + lb,
            (fa + fb * powb[la]) & MASK,
            (rb + ra * powb[lb]) & MASK,
        )

    def query(l, r):
        l = l + size - 1
        r = r + size - 1
        left = (0, 0, 0)
        right = (0, 0, 0)

        while l <= r:
            if l & 1:
                left = combine(left, (seg_len[l], seg_f[l], seg_r[l]))
                l += 1
            if not (r & 1):
                right = combine((seg_len[r], seg_f[r], seg_r[r]), right)
                r -= 1
            l //= 2
            r //= 2

        return combine(left, right)

    for x in p:
        update(x)
        t = min(x - 1, n - x)
        if t:
            _, fh, rh = query(x - t, x + t)
            if fh != rh:
                return "YES"

    return "NO"

# provided samples
assert run("4\n1 3 4 2\n") == "NO", "sample 1"
assert run("5\n1 5 2 4 3\n") == "YES", "sample 2"

# custom cases
assert run("1\n1\n") == "NO", "minimum size"
assert run("3\n1 2 3\n") == "YES", "simple progression"
assert run("3\n1 3 2\n") == "NO", "small negative case"
assert run("5\n5 4 3 2 1\n") == "YES", "reversed permutation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `NO` | Minimum size |
| `3 / 1 2 3` | `YES` | Smallest positive example |
| `3 / 1 3 2` | `NO` | Smallest negative example |
| `5 / 5 4 3 2 1` | `YES` | Endpoints on opposite sides despite reversed order |

## Edge Cases

Consider the smallest possible input:

```
1
1
```

No pair of distinct values exists. The algorithm performs one update, finds `t = 0`, never queries a range, and correctly prints `NO`.

Consider

```
3
1 3 2
```

The only arithmetic progression in values is `(1,2,3)`. After processing `2`, both `1` and `3` have already been seen, so their states are equal. The interval `[1,3]` is palindromic and the algorithm outputs `NO`.

Consider

```
3
1 2 3
```

When `2` is processed, value `1` has state `0` and value `3` has state `1`. The interval `[1,3]` becomes non-palindromic. The algorithm immediately reports `YES`, matching the fact that `2` lies between `1` and `3`.

Finally, consider a center near the boundary, such as value `1` or value `n`. Then `t = 0`, so there are no valid symmetric pairs. The algorithm skips the query entirely, avoiding off-by-one errors and correctly handling the edges of the value range.
