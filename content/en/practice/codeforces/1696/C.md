---
title: "CF 1696C - Fishingprince Plays With Array"
description: "We are given two arrays and a fixed integer $m$. Starting from the first array, we may repeatedly split an element divisible by $m$ into $m$ equal pieces, or merge $m$ consecutive equal elements into one larger element."
date: "2026-06-09T22:39:31+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1696
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 21"
rating: 1400
weight: 1696
solve_time_s: 508
verified: false
draft: false
---

[CF 1696C - Fishingprince Plays With Array](https://codeforces.com/problemset/problem/1696/C)

**Rating:** 1400  
**Tags:** constructive algorithms, greedy, implementation, math  
**Solve time:** 8m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two arrays and a fixed integer $m$. Starting from the first array, we may repeatedly split an element divisible by $m$ into $m$ equal pieces, or merge $m$ consecutive equal elements into one larger element.

The question is whether these operations allow us to transform the first array into the second.

The operations look complicated because the array length changes and many different sequences of moves are possible. The key observation is that neither operation changes the "atomic value" hidden inside an element.

Take an element $x$. Repeatedly divide it by $m$ while possible:

$$x = base \cdot m^t$$

where $base$ is no longer divisible by $m$.

For example, when $m=2$,

$$12 = 3 \cdot 2^2$$

and

$$8 = 1 \cdot 2^3.$$

The split operation only moves powers of $m$ between the value and the number of copies. The underlying $base$ never changes.

The constraints strongly suggest that we need a nearly linear solution. The sum of all array lengths over all test cases is at most $2 \cdot 10^5$. An $O(n^2)$ algorithm would require around $4 \cdot 10^{10}$ operations in the worst case, which is far beyond the limit. A solution around $O(n)$ or $O(n \log n)$ per test case is required.

Several edge cases are easy to mishandle.

Consider:

```
m = 2
a = [8]
b = [4,4]
```

The correct answer is `Yes`. A solution that only compares arrays element-by-element would incorrectly reject it. Splitting turns $8$ into two $4$'s.

Consider:

```
m = 2
a = [2,2]
b = [4]
```

The correct answer is `Yes`. Here the transformation requires merging rather than splitting.

Consider:

```
m = 2
a = [2,4]
b = [1,1,1,1,1,1]
```

The correct answer is `Yes`.

After full expansion:

$$2 \to (1,2),\quad 4 \to (1,4)$$

giving six copies of base value $1$. A careless implementation that keeps the two groups separate would miss that adjacent groups with the same base may combine.

Consider:

```
m = 3
a = [3,3]
b = [9]
```

The correct answer is `No`.

Each $3$ contributes one copy of base $1$. Together they contribute two copies, but merging requires groups of exactly $m=3$. We cannot create a single $9$.

## Approaches

A brute-force approach would try to simulate all possible sequences of splits and merges. This is correct in principle because every reachable array could eventually be explored.

The problem is the size of the state space. Even a single value such as

$$10^9 = 2^9 \cdot 1953125$$

can be split many times, creating exponentially many intermediate arrays. The number of reachable configurations grows far too quickly for exhaustive search.

The breakthrough comes from examining what never changes.

Take an element $x$. Remove every possible factor of $m$:

$$x = base \cdot m^t.$$

If we fully expand $x$, it becomes

$$base$$

repeated $m^t$ times.

For example, with $m=2$,

$$12 = 3 \cdot 2^2$$

behaves exactly like four copies of $3$.

The order of these base values never changes. Operations only redistribute powers of $m$ inside a contiguous block corresponding to the same base value.

This means every element can be represented as a pair:

$$(base,\ count)$$

where

$$count = m^t.$$

For $12$ with $m=2$, the pair is $(3,4)$.

Adjacent pairs with the same base can be merged because their expanded forms are indistinguishable. After compressing an entire array this way, the transformation question becomes:

Do the two compressed sequences of $(base,count)$ pairs match exactly?

If they do, the arrays represent the same fully expanded sequence and are mutually reachable. If they do not, no sequence of operations can fix the mismatch.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O((n+k)\log_m V)$ | $O(n+k)$ | Accepted |

Here $V \le 10^9$ is the largest element value.

## Algorithm Walkthrough

1. Process the first array from left to right.
2. For each value $x$, repeatedly divide by $m$ while divisible. Let the remaining value be `base`.
3. Count how many factors of $m$ were removed. If $x = base \cdot m^t$, then this element contributes `cnt = m^t` copies of `base`.
4. Store the pair `(base, cnt)`.
5. If the previous stored pair has the same `base`, add the counts together instead of creating a new pair.

This works because adjacent blocks with the same base represent consecutive copies of the same expanded value.
6. Repeat the same compression process for the second array.
7. Compare the two resulting sequences of pairs.
8. If the sequences are identical, print `Yes`. Otherwise print `No`.

### Why it works

For every element $x$, the value

$$base = \frac{x}{m^t}$$

cannot be changed by either operation.

Splitting converts

$$(base,m^t)$$

into $m$ copies of

$$(base,m^{t-1}),$$

while merging performs the reverse transformation.

Thus every operation preserves the expanded sequence of base values. The only freedom is how the total multiplicity of a base value is grouped into elements.

After compressing adjacent equal bases into a single count, we obtain a canonical representation. Two arrays are reachable from one another if and only if these canonical representations are identical. The algorithm computes exactly this representation and compares the results.

## Python Solution

```python
import sys
input = sys.stdin.readline

def normalize(arr, m):
    res = []

    for x in arr:
        base = x
        cnt = 1

        while base % m == 0:
            base //= m
            cnt *= m

        if res and res[-1][0] == base:
            res[-1][1] += cnt
        else:
            res.append([base, cnt])

    return res

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        k = int(input())
        b = list(map(int, input().split()))

        na = normalize(a, m)
        nb = normalize(b, m)

        ans.append("Yes" if na == nb else "No")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `normalize` function builds the canonical representation. Each number is reduced to its indivisible base value, and the removed powers of $m$ are converted into a multiplicity count.

The subtle part is merging adjacent entries with the same base. Without this step, arrays such as `[2,4]` and `[1,1,1,1,1,1]` would normalize differently even though they represent the same expanded sequence.

The count is stored directly as $m^t$. Since every original value is at most $10^9$, repeated multiplication remains safely within Python's integer range.

The final comparison is simply equality between two lists of pairs. Once the canonical forms match, every necessary split or merge sequence exists automatically.

## Worked Examples

### Example 1

Input:

```
m = 2
a = [1, 2, 2, 4, 2]
b = [1, 4, 4, 2]
```

Normalization of `a`:

| Value | Base | Count | Current Representation |
| --- | --- | --- | --- |
| 1 | 1 | 1 | [(1,1)] |
| 2 | 1 | 2 | [(1,3)] |
| 2 | 1 | 2 | [(1,5)] |
| 4 | 1 | 4 | [(1,9)] |
| 2 | 1 | 2 | [(1,11)] |

Normalization of `b`:

| Value | Base | Count | Current Representation |
| --- | --- | --- | --- |
| 1 | 1 | 1 | [(1,1)] |
| 4 | 1 | 4 | [(1,5)] |
| 4 | 1 | 4 | [(1,9)] |
| 2 | 1 | 2 | [(1,11)] |

Both normalize to:

```
[(1,11)]
```

Answer: `Yes`.

This example shows that many different groupings of the same expanded sequence become identical after normalization.

### Example 2

Input:

```
m = 3
a = [3,3,3,3,3,3,3,3]
b = [6,6,6,6]
```

Normalization of `a`:

| Value | Base | Count |
| --- | --- | --- |
| 3 | 1 | 3 |
| 3 | 1 | 3 |
| 3 | 1 | 3 |
| 3 | 1 | 3 |
| 3 | 1 | 3 |
| 3 | 1 | 3 |
| 3 | 1 | 3 |
| 3 | 1 | 3 |

Compressed form:

```
[(1,24)]
```

Normalization of `b`:

| Value | Base | Count |
| --- | --- | --- |
| 6 | 2 | 3 |
| 6 | 2 | 3 |
| 6 | 2 | 3 |
| 6 | 2 | 3 |

Compressed form:

```
[(2,12)]
```

The base values differ, so no sequence of operations can transform one array into the other.

Answer: `No`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+k)\log_m V)$ | Each value is divided by $m$ until no longer divisible |
| Space | $O(n+k)$ | Stores the normalized sequences |

Since $V \le 10^9$, each element can be divided at most about 30 times. The total number of array elements across all test cases is at most $2 \cdot 10^5$, so the solution comfortably fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    input_stream = io.StringIO(inp)

    def input():
        return input_stream.readline()

    def normalize(arr, m):
        res = []

        for x in arr:
            base = x
            cnt = 1

            while base % m == 0:
                base //= m
                cnt *= m

            if res and res[-1][0] == base:
                res[-1][1] += cnt
            else:
                res.append([base, cnt])

        return res

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        k = int(input())
        b = list(map(int, input().split()))

        out.append(
            "Yes"
            if normalize(a, m) == normalize(b, m)
            else "No"
        )

    return "\n".join(out)

# provided sample
assert run(
"""5
5 2
1 2 2 4 2
4
1 4 4 2
6 2
1 2 2 8 2 2
2
1 16
8 3
3 3 3 3 3 3 3 3
4
6 6 6 6
8 3
3 9 6 3 12 12 36 12
16
9 3 2 2 2 3 4 12 4 12 4 12 4 12 4 4
8 3
3 9 6 3 12 12 36 12
7
12 2 4 3 4 12 56
"""
) == """Yes
Yes
No
Yes
No"""

# minimum size
assert run(
"""1
1 2
1
1
1
"""
) == "Yes"

# split once
assert run(
"""1
1 2
8
2
4 4
"""
) == "Yes"

# merge impossible
assert run(
"""1
2 3
3 3
1
9
"""
) == "No"

# adjacent equal bases must combine
assert run(
"""1
2 2
2 4
6
1 1 1 1 1 1
"""
) == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a=[1], b=[1]` | Yes | Smallest valid instance |
| `a=[8], b=[4,4]` | Yes | Pure splitting |
| `a=[3,3], b=[9]` | No | Insufficient multiplicity for merging |
| `a=[2,4], b=[1,1,1,1,1,1]` | Yes | Adjacent equal bases must be merged during normalization |

## Edge Cases

Consider:

```
m = 2
a = [8]
b = [4,4]
```

Normalization gives:

```
a -> [(1,8)]
b -> [(1,8)]
```

The algorithm returns `Yes`. The actual transformation is obtained by splitting $8$ once.

Consider:

```
m = 2
a = [2,2]
b = [4]
```

Normalization gives:

```
a -> [(1,4)]
b -> [(1,4)]
```

The algorithm returns `Yes`. The corresponding operation is merging the two equal values.

Consider:

```
m = 2
a = [2,4]
b = [1,1,1,1,1,1]
```

Normalization gives:

```
a -> [(1,6)]
b -> [(1,6)]
```

The crucial step is combining adjacent entries with base value $1$. Without that compression, the left side would appear as `[(1,2),(1,4)]` and the comparison would fail incorrectly.

Consider:

```
m = 3
a = [3,3]
b = [9]
```

Normalization gives:

```
a -> [(1,6)]
b -> [(1,9)]
```

The counts differ, so the algorithm returns `No`. Even though all base values match, there is not enough multiplicity to create a single $9$.
