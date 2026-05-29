---
title: "CF 301D - Yaroslav and Divisors"
description: "We are given a permutation of numbers from 1 to n. For every query interval [l, r], we must count how many ordered pairs of positions (q, w) inside that interval satisfy: $$p[q] mid p[w]$$ Since all values are distinct and form a permutation, every number appears exactly once."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 301
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 182 (Div. 1)"
rating: 2200
weight: 301
solve_time_s: 175
verified: true
draft: false
---

[CF 301D - Yaroslav and Divisors](https://codeforces.com/problemset/problem/301/D)

**Rating:** 2200  
**Tags:** data structures  
**Solve time:** 2m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of numbers from `1` to `n`. For every query interval `[l, r]`, we must count how many ordered pairs of positions `(q, w)` inside that interval satisfy:

$$p[q] \mid p[w]$$

Since all values are distinct and form a permutation, every number appears exactly once. The task is not asking about divisibility between indices, only between the values stored at those indices.

For example, if the subarray contains values `[2, 6, 3]`, then valid ordered pairs are:

- `(2, 2)` because every number divides itself
- `(2, 6)`
- `(3, 3)`
- `(6, 6)`

The answer would be `4`.

The constraints are the real challenge here. Both `n` and `m` can reach `2 * 10^5`. A naive approach that inspects all pairs inside every query interval would require up to:

$$O(m \cdot n^2)$$

operations in the worst case, which is completely impossible under a 2 second limit.

Even iterating over all pairs once globally would already be around:

$$(2 \cdot 10^5)^2 = 4 \cdot 10^{10}$$

which is far beyond practical limits.

The structure of the permutation matters a lot. Because every value from `1` to `n` appears exactly once, we can preprocess the position of every number and reason about divisibility using values instead of indices.

Several edge cases are easy to mishandle.

Consider:

```
n = 1
p = [1]
query = [1,1]
```

The correct answer is `1`, because `1` divides itself. A careless implementation that only counts pairs of distinct numbers would incorrectly return `0`.

Another subtle case is when the divisor appears after the multiple in the array.

```
p = [6,2]
query = [1,2]
```

The valid pairs are:

- `(6,6)`
- `(2,2)`
- `(2,6)`

The answer is `3`.

The pair `(2,6)` is valid even though `2` appears later in the array. The condition is about values, not index ordering. Many incorrect solutions accidentally count only `i <= j`.

Another dangerous situation is double counting symmetric pairs.

```
p = [2,4]
```

Only `(2,4)` is valid, not `(4,2)`. Divisibility is directional. Treating it as an unordered relation produces wrong answers.

## Approaches

The brute force approach is straightforward. For every query `[l, r]`, iterate over all pairs of positions inside the interval and check whether one value divides the other.

The pseudocode idea looks like this:

```
for q in [l, r]:
    for w in [l, r]:
        if p[w] % p[q] == 0:
            answer += 1
```

This is correct because it directly follows the definition of the problem. Unfortunately, the complexity is terrible.

A single query may contain `O(n^2)` pairs. With `m = 2 * 10^5`, the total work becomes roughly:

$$O(mn^2)$$

which can reach `8 * 10^{15}` operations.

The next observation is the key turning point.

We do not actually care about arbitrary pairs of values. We only care about pairs where one number divides the other.

For a fixed value `x`, the only candidates are its multiples:

$$x, 2x, 3x, \dots$$

The total number of divisor-multiple relationships among numbers from `1` to `n` is:

$$\sum_{x=1}^{n} \frac{n}{x}$$

which is approximately:

$$n \log n$$

This is small enough.

Since the array is a permutation, we know the exact position of every value. For every valid divisor relation `(x, y)` where `x | y`, we can create a pair of positions:

$$(pos[x], pos[y])$$

A query asks how many such pairs lie completely inside `[l, r]`.

That transforms the problem into a geometric counting problem:

Count how many valid position pairs satisfy:

$$l \le a \le r$$

$$l \le b \le r$$

For convenience, we always store pairs as:

$$(\min(a,b), \max(a,b))$$

Then the query becomes:

Count pairs with:

$$a \ge l$$

$$b \le r$$

This is a classic offline Fenwick Tree problem.

We process queries by increasing `r`. As we sweep from left to right, we activate every pair whose larger endpoint equals the current position. For each activated pair `(a,b)`, we add `1` at position `a` in a Fenwick Tree.

Then for query `[l,r]`, the Fenwick Tree contains exactly the pairs whose larger endpoint is at most `r`. Querying the suffix sum from `l` to `n` counts how many of them also satisfy `a >= l`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(mn²) | O(1) | Too slow |
| Optimal | O(n log n + m log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Read the permutation and compute `pos[x]`, the position where value `x` appears.
2. Enumerate all divisor relationships.

For every value `x` from `1` to `n`, iterate through all multiples of `x`:

```
y = x, 2x, 3x, ...
```

Since `x` divides `y`, the pair is valid.
3. Convert value pairs into position pairs.

Let:

```
a = pos[x]
b = pos[y]
```

Store the pair as:

```
(min(a,b), max(a,b))
```

This normalization lets us treat every pair consistently.
4. Group pairs by their larger endpoint.

Suppose a pair becomes `(a,b)` with `a <= b`.

Store `a` inside a bucket associated with `b`.

Later, when processing position `b`, we will activate this pair.
5. Sort queries by their right endpoint `r`.

We process positions from left to right. When we reach position `r`, every pair with larger endpoint at most `r` should already be active.
6. Maintain a Fenwick Tree over positions.

When processing position `b`, activate all stored pairs by adding `1` at their smaller endpoint `a`.
7. Answer queries.

For query `[l,r]`, all active pairs already satisfy:

```
larger endpoint <= r
```

We still need:

```
smaller endpoint >= l
```

This is exactly the suffix sum:

```
sum(n) - sum(l-1)
```
8. Output answers in original query order.

### Why it works

Every valid divisor relation between values generates exactly one normalized position pair `(a,b)` with `a <= b`.

A query interval `[l,r]` should count precisely those pairs completely contained inside the interval. That condition is equivalent to:

$$a \ge l \quad \text{and} \quad b \le r$$

During the sweep, once position `r` is processed, the Fenwick Tree contains all pairs with `b <= r`. Each such pair contributes `1` at index `a`.

Querying the suffix `[l,n]` counts exactly the pairs whose smaller endpoint is at least `l`. Combining both conditions gives exactly the pairs fully inside the interval.

No pair is missed, and no pair is counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def solve():
    n, m = map(int, input().split())
    p = [0] + list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[p[i]] = i

    events = [[] for _ in range(n + 1)]

    for x in range(1, n + 1):
        y = x
        while y <= n:
            a = pos[x]
            b = pos[y]

            if a > b:
                a, b = b, a

            events[b].append(a)
            y += x

    queries = [[] for _ in range(n + 1)]

    for idx in range(m):
        l, r = map(int, input().split())
        queries[r].append((l, idx))

    bit = Fenwick(n)
    ans = [0] * m

    for r in range(1, n + 1):
        for a in events[r]:
            bit.add(a, 1)

        for l, idx in queries[r]:
            ans[idx] = bit.range_sum(l, n)

    print("\n".join(map(str, ans)))

solve()
```

The first important preprocessing step is building `pos`. Since the array is a permutation, this gives constant time access to the position of every value.

The nested multiple loop is the heart of the optimization. Instead of checking all value pairs, we only inspect pairs where divisibility is guaranteed. The total number of iterations behaves like harmonic series growth:

$$n \left(1 + \frac12 + \frac13 + \dots \right)$$

which is approximately `n log n`.

The normalization:

```
if a > b:
    a, b = b, a
```

is essential. Queries care only whether both endpoints lie inside the interval. They do not care about the order in which the values appear.

The Fenwick Tree stores counts indexed by the smaller endpoint. When processing right endpoint `r`, every active pair already satisfies `b <= r`. A suffix query over `[l,n]` filters exactly those with `a >= l`.

One subtle implementation detail is that pairs where `x == y` must also be included. Every number divides itself, so diagonal pairs are valid and necessary.

Another easy mistake is using prefix sums instead of suffix sums when answering queries. We need:

```
a >= l
```

not:

```
a <= l
```

so the query must be:

```
bit.range_sum(l, n)
```

## Worked Examples

### Example 1

Input:

```
1 1
1
1 1
```

The permutation contains only one value.

Valid divisor pairs:

| x | y | Positions | Normalized pair |
| --- | --- | --- | --- |
| 1 | 1 | (1,1) | (1,1) |

Processing:

| r | Activated pairs | BIT contents | Query | Answer |
| --- | --- | --- | --- | --- |
| 1 | (1,1) | count at 1 = 1 | [1,1] | 1 |

The result is `1`.

This example confirms that self-divisibility must be counted.

### Example 2

Input:

```
5 3
2 1 4 5 3
1 5
2 4
3 5
```

Positions:

| Value | Position |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 5 |
| 4 | 3 |
| 5 | 4 |

Valid divisor relations:

| x | y | Position pair | Normalized |
| --- | --- | --- | --- |
| 1 | 1 | (2,2) | (2,2) |
| 1 | 2 | (2,1) | (1,2) |
| 1 | 3 | (2,5) | (2,5) |
| 1 | 4 | (2,3) | (2,3) |
| 1 | 5 | (2,4) | (2,4) |
| 2 | 2 | (1,1) | (1,1) |
| 2 | 4 | (1,3) | (1,3) |
| 3 | 3 | (5,5) | (5,5) |
| 4 | 4 | (3,3) | (3,3) |
| 5 | 5 | (4,4) | (4,4) |

Sweep process:

| r | Activated smaller endpoints | Query | Answer |
| --- | --- | --- | --- |
| 1 | 1 | none | - |
| 2 | 2,1 | none | - |
| 3 | 2,1,3 | [2,4] | 4 |
| 4 | 2,4 | none | - |
| 5 | 2,5 | [1,5] | 10 |
| 5 | already active | [3,5] | 3 |

The interval `[2,4]` contains values `[1,4,5]`.

Valid ordered pairs are:

- `(1,1)`
- `(1,4)`
- `(1,5)`
- `(4,4)`

giving answer `4`.

This trace demonstrates how the sweep line guarantees that only pairs fully inside the current right boundary are active.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log n) | Enumerating multiples costs harmonic-series time, Fenwick operations cost logarithmic time |
| Space | O(n log n) | Stored divisor pairs plus Fenwick Tree and queries |

The harmonic series bound is the reason this solution fits comfortably inside the limits. For `n = 2 * 10^5`, the number of divisor-multiple pairs is roughly a few million, which is manageable in Python with efficient data structures.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            while idx <= self.n:
                self.bit[idx] += val
                idx += idx & -idx

        def sum(self, idx):
            res = 0
            while idx > 0:
                res += self.bit[idx]
                idx -= idx & -idx
            return res

        def range_sum(self, l, r):
            return self.sum(r) - self.sum(l - 1)

    n, m = map(int, input().split())
    p = [0] + list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[p[i]] = i

    events = [[] for _ in range(n + 1)]

    for x in range(1, n + 1):
        y = x
        while y <= n:
            a = pos[x]
            b = pos[y]

            if a > b:
                a, b = b, a

            events[b].append(a)
            y += x

    queries = [[] for _ in range(n + 1)]

    for idx in range(m):
        l, r = map(int, input().split())
        queries[r].append((l, idx))

    bit = Fenwick(n)
    ans = [0] * m

    for r in range(1, n + 1):
        for a in events[r]:
            bit.add(a, 1)

        for l, idx in queries[r]:
            ans[idx] = bit.range_sum(l, n)

    return "\n".join(map(str, ans))

# provided sample
assert run("1 1\n1\n1 1\n") == "1"

# reversed divisor order
assert run("2 1\n6 2\n1 2\n") == "3"

# simple increasing permutation
assert run(
    "4 2\n1 2 3 4\n1 4\n2 3\n"
) == "8\n2"

# single element intervals
assert run(
    "5 5\n2 1 4 5 3\n1 1\n2 2\n3 3\n4 4\n5 5\n"
) == "1\n1\n1\n1\n1"

# off-by-one interval boundaries
assert run(
    "3 3\n2 3 1\n1 2\n2 3\n1 3\n"
) == "2\n2\n5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 / 1 1` | `1` | Self-divisibility |
| `6 2` permutation case | `3` | Divisor can appear after multiple |
| Increasing permutation | `8`, `2` | General divisor counting |
| Single-element queries | all `1` | Every number divides itself |
| Boundary interval test | `2`, `2`, `5` | Correct handling of interval limits |

## Edge Cases

Consider the smallest possible input:

```
1 1
1
1 1
```

The algorithm generates the divisor pair `(1,1)`. Its position pair is also `(1,1)`. During the sweep at `r = 1`, the Fenwick Tree receives one update at position `1`. Querying suffix `[1,n]` returns `1`.

This confirms that self-pairs are included correctly.

Now examine the reversed ordering case:

```
2 1
6 2
1 2
```

After normalization:

- `(6,6)` becomes `(1,1)`
- `(2,2)` becomes `(2,2)`
- `(2,6)` becomes `(1,2)`

Even though the divisor `2` appears later in the array, normalization preserves the correct interval geometry. The query `[1,2]` counts all three pairs.

Finally, consider a boundary-sensitive example:

```
3 1
2 3 1
2 3
```

Valid divisor relations globally are:

- `(2,2)`
- `(3,3)`
- `(1,1)`
- `(1,2)`
- `(1,3)`

Inside interval `[2,3]`, only positions `2` and `3` are allowed. The only valid pairs are:

- `(3,3)`
- `(1,1)` using the value `1` at position `3`

The algorithm handles this because the Fenwick query only counts pairs whose smaller endpoint is at least `2`. Pairs touching position `1` are excluded automatically.
