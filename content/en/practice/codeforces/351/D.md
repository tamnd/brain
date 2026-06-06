---
title: "CF 351D - Jeff and Removing Periods"
description: "For each query we look at a subarray of the given array and ask for its beauty. A single operation chooses several equal values whose positions form an arithmetic progression, removes them, and then allows us to reorder everything that remains. That last sentence is the key."
date: "2026-06-06T22:08:08+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 351
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 204 (Div. 1)"
rating: 2700
weight: 351
solve_time_s: 159
verified: true
draft: false
---

[CF 351D - Jeff and Removing Periods](https://codeforces.com/problemset/problem/351/D)

**Rating:** 2700  
**Tags:** data structures  
**Solve time:** 2m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

For each query we look at a subarray of the given array and ask for its **beauty**.

A single operation chooses several equal values whose positions form an arithmetic progression, removes them, and then allows us to reorder everything that remains.

That last sentence is the key. After the first operation, the order of the remaining elements becomes completely controllable. If a value appears $c$ times, we can place all $c$ copies on positions forming an arithmetic progression and delete them in one operation. From that point onward, each distinct value can always be removed in exactly one operation.

The only difficult part is the **first** operation, because it must use the original order of the queried subarray.

The array length and the number of queries are both up to $10^5$. Any solution that processes a query independently is immediately ruled out. Even $O(\sqrt n)$ work per query would already be close to the limit. We need an offline data structure solution with roughly $O((n+q)\sqrt n)$ total complexity.

A subtle edge case appears when a value occurs exactly once inside the query interval.

```
[5, 7, 5]
```

For the interval $[2,2]$, the value $7$ appears once. A single position is trivially an arithmetic progression, so that value can be deleted immediately. Any solution that only checks values occurring at least twice would miss this.

Another easy mistake is to think that after reordering we may somehow combine different values into one operation.

```
[1, 1, 2, 2]
```

Operations always delete equal values only. Even after reordering, the best we can do is delete all $1$'s in one operation and all $2$'s in another. The answer is $2$, not $1$.

The most important corner case is when every value occurs multiple times, but none of them already forms an arithmetic progression.

```
positions of 1: 1, 3, 6
positions of 2: 2, 5, 9
```

Neither set of positions is an arithmetic progression. The first operation cannot completely eliminate any value. That extra failed first operation increases the answer by one.

## Approaches

The brute force viewpoint is surprisingly useful.

Suppose we know all occurrences of every value inside a query interval. A value is immediately removable if all of its occurrences in the interval lie on an arithmetic progression. If we remove such a value first, then the remaining distinct values can each be deleted in one operation after reordering.

Let $D$ be the number of distinct values in the interval.

If some value is immediately removable, we spend one operation deleting it, then $D-1$ more operations for the remaining distinct values. The answer is $D$.

If no value is immediately removable, the first operation can only delete part of some value. After that operation, all $D$ distinct values still exist. Reordering then needs $D$ additional operations. The answer is $D+1$.

So every query reduces to two quantities:

1. The number of distinct values.
2. Whether there exists at least one value whose occurrences inside the interval form an arithmetic progression.

This observation is the entire problem. It appears in many accepted solutions and is the foundation of the standard Mo's algorithm approach.

A naive implementation would still be too slow. For each query we would have to gather occurrences of every value and test the arithmetic progression condition from scratch. In the worst case that becomes $O(n)$ or worse per query, which is far beyond what $10^5$ queries allow.

The interval endpoints move gradually under Mo's algorithm. The number of distinct values is easy to maintain. The real challenge is maintaining the number of values whose current occurrences form an arithmetic progression.

The accepted solution precomputes auxiliary arrays that tell us exactly when adding or removing one occurrence causes a value to stop being an arithmetic progression, or start being one again. Then every Mo update becomes $O(1)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ or worse | $O(n)$ | Too slow |
| Optimal (Mo + AP maintenance) | $O((n+q)\sqrt n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Key characterization

Let $D$ be the number of distinct values in the current interval.

Let $G$ be the number of values whose occurrences inside the interval form an arithmetic progression.

If $G>0$, the answer is $D$.

If $G=0$, the answer is $D+1$.

So the entire task becomes maintaining $D$ and $G$.

### Preprocessing occurrence structure

For every position $i$:

1. Compute `pre[i]`, the previous occurrence of the same value.
2. Compute `bak[i]`, the next occurrence of the same value.

Then build two helper arrays.

`fl[i]` stores the leftmost position beyond which the chain of equal values ending at $i$ stops being an arithmetic progression.

`fr[i]` stores the symmetric information when looking to the right.

These arrays are computed by dynamic recurrence on consecutive occurrences of the same value.

### Mo ordering

1. Sort all queries using the standard Mo ordering.
2. Maintain a current interval $[L,R]$.
3. Move $L$ and $R$ to match each query.

### Maintaining distinct values

1. Keep `cnt[value]`.
2. When a frequency changes from $0$ to $1$, increase $D$.
3. When a frequency changes from $1$ to $0$, decrease $D$.

### Maintaining arithmetic progression values

1. Keep $G$, the number of values whose current occurrences form an arithmetic progression.
2. When a boundary moves, only one occurrence is inserted or removed.
3. Using `fl` and `fr`, determine in $O(1)$ whether that update changes the AP status of the corresponding value.
4. Increase or decrease $G$ accordingly.

The precomputed arrays tell us exactly when a newly exposed occurrence creates the first violation of equal spacing, or when removing an occurrence eliminates the last violation.

### Answering a query

1. After the interval is adjusted, we know $D$ and $G$.
2. If $G>0$, output $D$.
3. Otherwise output $D+1$.

### Why it works

After the first operation, arbitrary reordering is allowed. Every remaining distinct value can then be arranged so that all its copies lie on an arithmetic progression and can be deleted in one operation.

A query interval needs exactly one less operation if there exists a value that can already be deleted completely before any reordering occurs. That condition is equivalent to saying that the occurrences of that value inside the interval form an arithmetic progression.

Thus the answer depends only on the number of distinct values and on whether at least one value is currently "good". The Mo structure maintains exactly these two pieces of information, so every reported answer is correct.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))

    maxv = 100000

    pre = [0] * (n + 1)
    bak = [0] * (n + 1)
    fl = [0] * (n + 1)
    fr = [0] * (n + 2)

    last = [0] * (maxv + 1)

    for i in range(1, n + 1):
        pre[i] = last[a[i]]
        last[a[i]] = i

        if pre[i] == 0 or pre[pre[i]] == 0:
            fl[i] = 0
        elif pre[pre[i]] - pre[i] == pre[i] - i:
            fl[i] = fl[pre[i]]
        else:
            fl[i] = pre[pre[i]]

    last = [0] * (maxv + 1)

    for i in range(n, 0, -1):
        bak[i] = last[a[i]]
        last[a[i]] = i

        if bak[i] == 0 or bak[bak[i]] == 0:
            fr[i] = n + 1
        elif bak[bak[i]] - bak[i] == bak[i] - i:
            fr[i] = fr[bak[i]]
        else:
            fr[i] = bak[bak[i]]

    q = int(input())
    block = isqrt(n) + 1

    queries = []
    for idx in range(q):
        l, r = map(int, input().split())
        queries.append((l, r, idx))

    queries.sort(key=lambda x: (x[0] // block, x[1]))

    cnt = [0] * (maxv + 1)
    ans = [0] * q

    distinct = 0
    good = 0

    def add_left(pos, cur_r):
        nonlocal distinct, good
        x = a[pos]

        cnt[x] += 1
        if cnt[x] == 1:
            distinct += 1
            good += 1
        elif fr[pos] <= cur_r and fr[bak[pos]] > cur_r:
            good -= 1

    def remove_left(pos, cur_r):
        nonlocal distinct, good
        x = a[pos]

        cnt[x] -= 1
        if cnt[x] == 0:
            distinct -= 1
            good -= 1
        elif fr[pos] <= cur_r and fr[bak[pos]] > cur_r:
            good += 1

    def add_right(pos, cur_l):
        nonlocal distinct, good
        x = a[pos]

        cnt[x] += 1
        if cnt[x] == 1:
            distinct += 1
            good += 1
        elif fl[pos] >= cur_l and fl[pre[pos]] < cur_l:
            good -= 1

    def remove_right(pos, cur_l):
        nonlocal distinct, good
        x = a[pos]

        cnt[x] -= 1
        if cnt[x] == 0:
            distinct -= 1
            good -= 1
        elif fl[pos] >= cur_l and fl[pre[pos]] < cur_l:
            good += 1

    L = 1
    R = 0

    for l, r, idx in queries:
        while L > l:
            L -= 1
            add_left(L, R)

        while R < r:
            R += 1
            add_right(R, L)

        while L < l:
            remove_left(L, R)
            L += 1

        while R > r:
            remove_right(R, L)
            R -= 1

        ans[idx] = distinct if good > 0 else distinct + 1

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The preprocessing stage builds the previous and next occurrence links for every value. Those links are then used to compute `fl` and `fr`, which encode where the arithmetic progression property first breaks.

The Mo structure maintains a sliding interval. Every update changes only one position, so the status of only one value can change. The helper arrays let us detect that change in constant time.

A common source of bugs is forgetting that the update functions must use the **current** interval boundaries, not the query boundaries being processed. Another frequent mistake is updating the interval endpoints before evaluating the transition conditions.

## Worked Examples

### Sample 1

Input interval:

```
[2, 2, 1, 1, 2]
```

| Value | Positions |
| --- | --- |
| 1 | 3, 4 |
| 2 | 1, 2, 5 |

Distinct values:

| D | Good values |
| --- | --- |
| 2 | Value 1 |

The positions of value $1$ are $(3,4)$, which is an arithmetic progression.

Since a good value exists, the answer is $D=2$.

This example demonstrates the central observation: one value can be removed immediately, then the remaining value is removed after reordering.

### Custom Example

Array:

```
[1, 2, 1, 2, 2, 1]
```

Query:

```
[1, 6]
```

| Value | Positions |
| --- | --- |
| 1 | 1, 3, 6 |
| 2 | 2, 4, 5 |

Check equal spacing:

| Value | Differences | AP? |
| --- | --- | --- |
| 1 | 2, 3 | No |
| 2 | 2, 1 | No |

Here $D=2$ and $G=0$.

Answer:

$$D + 1 = 3$$

The first operation cannot completely eliminate any value, so an extra operation is unavoidable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+q)\sqrt n)$ | Standard Mo's algorithm with $O(1)$ updates |
| Space | $O(n)$ | Occurrence links, helper arrays, frequencies, queries |

With $n,q \le 10^5$, roughly $O((n+q)\sqrt n)$ operations comfortably fit inside the time limit, and the memory usage remains well below 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    from math import isqrt

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    n = int(input())
    a = [0] + list(map(int, input().split()))

    maxv = 100000

    pre = [0] * (n + 1)
    bak = [0] * (n + 1)
    fl = [0] * (n + 1)
    fr = [0] * (n + 2)

    last = [0] * (maxv + 1)

    for i in range(1, n + 1):
        pre[i] = last[a[i]]
        last[a[i]] = i

        if pre[i] == 0 or pre[pre[i]] == 0:
            fl[i] = 0
        elif pre[pre[i]] - pre[i] == pre[i] - i:
            fl[i] = fl[pre[i]]
        else:
            fl[i] = pre[pre[i]]

    last = [0] * (maxv + 1)

    for i in range(n, 0, -1):
        bak[i] = last[a[i]]
        last[a[i]] = i

        if bak[i] == 0 or bak[bak[i]] == 0:
            fr[i] = n + 1
        elif bak[bak[i]] - bak[i] == bak[i] - i:
            fr[i] = fr[bak[i]]
        else:
            fr[i] = bak[bak[i]]

    q = int(input())
    block = isqrt(n) + 1

    qs = []
    for idx in range(q):
        l, r = map(int, input().split())
        qs.append((l, r, idx))

    qs.sort(key=lambda x: (x[0] // block, x[1]))

    cnt = [0] * (maxv + 1)
    res = [0] * q

    distinct = 0
    good = 0

    def add_left(pos, cur_r):
        nonlocal distinct, good
        x = a[pos]
        cnt[x] += 1
        if cnt[x] == 1:
            distinct += 1
            good += 1
        elif fr[pos] <= cur_r and fr[bak[pos]] > cur_r:
            good -= 1

    def remove_left(pos, cur_r):
        nonlocal distinct, good
        x = a[pos]
        cnt[x] -= 1
        if cnt[x] == 0:
            distinct -= 1
            good -= 1
        elif fr[pos] <= cur_r and fr[bak[pos]] > cur_r:
            good += 1

    def add_right(pos, cur_l):
        nonlocal distinct, good
        x = a[pos]
        cnt[x] += 1
        if cnt[x] == 1:
            distinct += 1
            good += 1
        elif fl[pos] >= cur_l and fl[pre[pos]] < cur_l:
            good -= 1

    def remove_right(pos, cur_l):
        nonlocal distinct, good
        x = a[pos]
        cnt[x] -= 1
        if cnt[x] == 0:
            distinct -= 1
            good -= 1
        elif fl[pos] >= cur_l and fl[pre[pos]] < cur_l:
            good += 1

    L, R = 1, 0

    for l, r, idx in qs:
        while L > l:
            L -= 1
            add_left(L, R)
        while R < r:
            R += 1
            add_right(R, L)
        while L < l:
            remove_left(L, R)
            L += 1
        while R > r:
            remove_right(R, L)
            R -= 1

        res[idx] = distinct if good > 0 else distinct + 1

    return "\n".join(map(str, res))

# sample 1
assert run(
"""5
2 2 1 1 2
5
1 5
1 1
2 2
1 3
2 3
"""
) == "2\n1\n1\n2\n2"

# minimum size
assert run(
"""1
7
1
1 1
"""
) == "1"

# all equal
assert run(
"""4
5 5 5 5
1
1 4
"""
) == "1"

# two distinct singletons
assert run(
"""2
1 2
1
1 2
"""
) == "2"

# AP positions present
assert run(
"""5
1 2 1 3 1
1
1 5
"""
) == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | 1 | Smallest possible interval |
| All equal values | 1 | One value removed in one operation |
| Two distinct singletons | 2 | Singleton values are always good |
| Positions 1,3,5 of same value | 3 | Arithmetic progression detection |

## Edge Cases

Consider:

```
1
7
1
1 1
```

The interval contains one value appearing once. A single position is an arithmetic progression, so $G=1$, $D=1$, and the answer is $1$.

Consider:

```
4
5 5 5 5
1
1 4
```

All occurrences belong to one value. Their positions form an arithmetic progression, so the entire interval disappears in one operation. The algorithm keeps $D=1$ and $G=1$, producing answer $1$.

Consider:

```
6
1 2 1 2 2 1
1
1 6
```

Value $1$ occupies positions $1,3,6$, differences $2,3$. Value $2$ occupies positions $2,4,5$, differences $2,1$. No value is good. The algorithm ends with $D=2$ and $G=0$, returning $3$, which matches the optimal strategy.
