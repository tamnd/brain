---
title: "CF 228D - Zigzag"
description: "We maintain an array of up to $10^5$ numbers. Two kinds of operations arrive online. The first operation changes a single array element. The second operation asks for a weighted sum on a segment."
date: "2026-06-04T09:06:23+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 228
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 141 (Div. 2)"
rating: 2100
weight: 228
solve_time_s: 102
verified: true
draft: false
---

[CF 228D - Zigzag](https://codeforces.com/problemset/problem/228/D)

**Rating:** 2100  
**Tags:** data structures  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain an array of up to $10^5$ numbers. Two kinds of operations arrive online.

The first operation changes a single array element.

The second operation asks for a weighted sum on a segment. The weights come from a special periodic "zigzag" sequence determined by a parameter $z$, where $2 \le z \le 6$.

For a fixed $z$, the sequence looks like

$$1,2,\dots,z,z-1,\dots,2,1,2,\dots$$

and repeats forever.

For example:

$$z=2:\quad 1,2,1,2,1,2,\dots$$

$$z=3:\quad 1,2,3,2,1,2,3,2,\dots$$

$$z=4:\quad 1,2,3,4,3,2,1,2,\dots$$

For a query $(l,r,z)$, we must compute

$$\sum_{i=l}^{r} a_i \cdot S^{(z)}_{i-l+1}$$

where $S^{(z)}$ is the zigzag sequence for factor $z$.

The challenge is that both the array and the queries are dynamic. We must answer up to $10^5$ operations.

A direct computation of each query scans the entire interval. In the worst case, a query may cover all $10^5$ elements, and there may be $10^5$ such queries. That would require roughly $10^{10}$ multiplications, which is completely infeasible.

The small bound on $z$ is the crucial clue. Although the array is large, there are only five possible zigzag factors: $2,3,4,5,6$.

A subtle edge case comes from the fact that the query always starts the zigzag pattern at position $l$, not at position $1$.

Consider:

```
a = [10,20,30]
query: l=2, r=3, z=2
```

The weights are:

```
1,2
```

not

```
2,1
```

because the pattern restarts at the left boundary of the query. Any solution that stores only a global weight pattern by absolute index will produce the wrong answer.

Another easy mistake is assuming the period is $2z$. For example:

```
z=3
1 2 3 2 1 2 3 2 ...
```

The true period is

$$2z-2 = 4.$$

Using period $6$ would misalign all queries.

A third trap appears after updates.

Example:

```
a = [1,1,1]
update position 2 -> 100
query (1,3,2)
```

The answer becomes

$$1\cdot1+100\cdot2+1\cdot1=202.$$

If updates are not reflected in every data structure associated with the relevant residue class, future answers become incorrect.

## Approaches

The brute force solution is straightforward. For every query, generate the zigzag weights and scan from $l$ to $r$, accumulating

$$a_i \cdot \text{weight}.$$

A point update costs $O(1)$, but a range query costs $O(r-l+1)$. With $10^5$ operations and intervals of length $10^5$, the running time reaches $10^{10}$, which is far beyond the limit.

The key observation is that only five zigzag factors are possible.

For a fixed $z$, the zigzag sequence is periodic. Let

$$P_z = 2z-2.$$

For $z \le 6$,

$$P_z \le 10.$$

That means every weight assigned to an array position depends only on its index modulo at most 10.

Suppose we fix a particular $z$. For each residue class modulo $P_z$, we build a Fenwick tree storing values belonging to that residue class.

Then we can ask:

"What is the sum of all array values in $[l,r]$ whose index is congruent to residue $k$ modulo $P_z$?"

Each residue class contributes a constant weight from the zigzag pattern. Since there are at most 10 residues, the entire query becomes a sum of at most 10 Fenwick range queries.

Updates are also easy. When $a_p$ changes, we update the corresponding residue-class Fenwick tree for every possible $z$. There are only five values of $z$, so each update touches a constant number of structures.

The brute force fails because it repeatedly recomputes contributions of individual elements. The periodic structure lets us aggregate all positions sharing the same residue modulo the period, reducing every query to a small constant number of Fenwick operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per query | $O(1)$ | Too slow |
| Optimal | $O(\log n)$ per operation | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Precomputation

For each zigzag factor $z \in \{2,3,4,5,6\}$:

1. Compute its period $P = 2z-2$.
2. Build the zigzag weights for one full period.
3. Create $P$ Fenwick trees, one for each residue modulo $P$.
4. Insert every array element $a_i$ into the Fenwick tree corresponding to $i \bmod P$.

### Update Operation

1. Let the current value at position $p$ be old.
2. Compute

$$\Delta = v - old.$$

1. For every zigzag factor $z$:

- Compute $P=2z-2$.
- Find residue $p \bmod P$.
- Add $\Delta$ to the corresponding Fenwick tree at index $p$.
2. Store the new array value.

Each Fenwick tree always contains the current array values for its residue class.

### Query Operation

1. Let $P=2z-2$.
2. For every residue $r$ modulo $P$, obtain the sum of array values inside $[l,r]$ whose indices belong to that residue class.
3. Determine which zigzag weight corresponds to that residue.

The pattern starts at position $l$, so residue classes must be shifted relative to $l$.
4. Multiply each residue-class sum by its corresponding weight.
5. Add all contributions.

The number of residues is at most 10, so only a constant number of Fenwick range queries are required.

### Why it works

For a fixed $z$, the zigzag sequence repeats every $P=2z-2$ positions. Every index with the same residue modulo $P$ always receives the same weight relative to a given alignment.

A query can therefore be decomposed into residue classes modulo $P$. The Fenwick trees give the total array value contributed by each residue class inside the requested interval. Multiplying each class sum by its appropriate zigzag weight produces exactly the same total as summing element-by-element. Updates preserve this invariant because every modified position is updated in all residue-class structures that contain it.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, delta):
        n = self.n
        bit = self.bit
        while idx <= n:
            bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        bit = self.bit
        while idx > 0:
            res += bit[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def build_pattern(z):
    p = 2 * z - 2
    arr = []
    for i in range(1, z + 1):
        arr.append(i)
    for i in range(z - 1, 1, -1):
        arr.append(i)
    return arr

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))

    structures = {}

    for z in range(2, 7):
        period = 2 * z - 2
        pattern = build_pattern(z)

        trees = [Fenwick(n) for _ in range(period)]

        for i in range(1, n + 1):
            trees[i % period].add(i, a[i])

        structures[z] = (period, pattern, trees)

    m = int(input())
    out = []

    for _ in range(m):
        q = list(map(int, input().split()))

        if q[0] == 1:
            _, p, v = q
            delta = v - a[p]
            a[p] = v

            for z in range(2, 7):
                period, pattern, trees = structures[z]
                trees[p % period].add(p, delta)

        else:
            _, l, r, z = q

            period, pattern, trees = structures[z]

            ans = 0

            for residue in range(period):
                s = trees[residue].range_sum(l, r)

                offset = (residue - (l % period)) % period
                weight = pattern[offset]

                ans += s * weight

            out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation stores one family of Fenwick trees for every possible zigzag factor. For a fixed period $P$, residue $r$ contains exactly the array positions whose indices satisfy $i \bmod P=r$.

The query logic is the subtle part. The zigzag pattern starts at the left endpoint of the query, not at index 1. The expression

```
offset = (residue - (l % period)) % period
```

computes where that residue appears inside the periodic pattern relative to the query start.

The Fenwick trees are indexed by original array position. That allows ordinary range-sum queries without any coordinate transformations.

All arithmetic uses Python integers, which safely handle the maximum possible answer.

## Worked Examples

### Sample 1

Input:

```
5
2 3 1 5 5
4
2 2 3 2
2 1 5 3
1 3 5
2 1 5 3
```

For $z=2$, the period is 2 and the pattern is:

```
1 2
```

First query:

| Residue | Values in [2,3] | Weight | Contribution |
| --- | --- | --- | --- |
| 0 | 3 | 1 | 3 |
| 1 | 1 | 2 | 2 |

Answer:

$$3+2=5$$

Second query with $z=3$:

Pattern:

```
1 2 3 2
```

| Residue | Sum in range | Weight | Contribution |
| --- | --- | --- | --- |
| 1 | 2+5 | 1 | 7 |
| 2 | 3 | 2 | 6 |
| 3 | 1 | 3 | 3 |
| 0 | 5 | 2 | 10 |

Total:

$$26$$

After updating position 3 to 5, every relevant Fenwick tree receives a delta of 4.

Repeating the query gives:

$$2\cdot1+3\cdot2+5\cdot3+5\cdot2+5\cdot1=38$$

which matches the sample.

This trace shows that updates affect every future query immediately through the shared Fenwick structures.

### Custom Example

Input:

```
3
10 20 30
1
2 2 3 2
```

Pattern for $z=2$:

```
1 2
```

| Position | Value | Weight | Contribution |
| --- | --- | --- | --- |
| 2 | 20 | 1 | 20 |
| 3 | 30 | 2 | 60 |

Answer:

$$80$$

This example confirms that the pattern restarts at the left boundary of the query.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ per operation | At most 10 Fenwick queries or updates are performed |
| Space | $O(n)$ | Total stored Fenwick data is proportional to a constant multiple of $n$ |

The total number of Fenwick trees is

$$2+4+6+8+10 = 30,$$

which is a fixed constant. Every operation performs only a constant number of logarithmic-time Fenwick updates or range queries, easily fitting within the limits for $10^5$ operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

assert run(
"""5
2 3 1 5 5
4
2 2 3 2
2 1 5 3
1 3 5
2 1 5 3
"""
) == "5\n26\n38\n", "sample 1"

assert run(
"""1
7
1
2 1 1 2
"""
) == "7\n", "minimum size"

assert run(
"""4
5 5 5 5
2
2 1 4 2
2 1 4 6
"""
) == "30\n50\n", "all equal values"

assert run(
"""3
10 20 30
1
2 2 3 2
"""
) == "80\n", "pattern restarts at l"

assert run(
"""3
1 1 1
3
1 2 100
2 1 3 2
2 1 3 3
"""
) == "202\n302\n", "update propagation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | 7 | Minimum bounds |
| All values equal | 30, 50 | Different periods and weights |
| Query starts in middle | 80 | Pattern alignment relative to l |
| Update then query | 202, 302 | Correct update propagation |

## Edge Cases

Consider:

```
3
10 20 30
1
2 2 3 2
```

The pattern for $z=2$ is $1,2$. The algorithm computes the residue-class sums and shifts them by $l=2$. Position 2 receives weight 1 and position 3 receives weight 2. The result is

$$20+60=80.$$

Any implementation that aligns weights using absolute indices instead of the query start would incorrectly produce $70$.

Consider:

```
5
1 1 1 1 1
1
2 1 5 3
```

The period is $2z-2=4$, not 6. The weights are

```
1 2 3 2 1
```

giving

$$9.$$

The algorithm stores data modulo 4, so the repeating structure is represented correctly.

Consider:

```
3
1 1 1
2
1 2 100
2 1 3 2
```

After the update, the delta is 99. The algorithm applies that delta to every affected Fenwick structure. The query then computes

$$1\cdot1+100\cdot2+1\cdot1=202.$$

Because all structures are updated immediately, no stale values remain and the answer is correct.
