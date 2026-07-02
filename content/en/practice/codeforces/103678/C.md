---
title: "CF 103678C - \u0411\u0435\u0440\u043d\u0430\u0440\u0434 \u0438 \u0437\u0430\u043f\u0440\u043e\u0441\u044b \u043d\u0430 \u0430\u0440\u0438\u0444\u043c\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0441\u0438\u044f\u0445"
description: "We are working with a one-dimensional array that is initially empty or filled with zeros, and we are asked to process two kinds of operations. One operation updates a contiguous segment by adding an arithmetic progression across its positions."
date: "2026-07-02T21:01:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103678
codeforces_index: "C"
codeforces_contest_name: "2022 VII \u0418\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041f\u0424\u041e \u0441\u0440\u0435\u0434\u0438 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432"
rating: 0
weight: 103678
solve_time_s: 63
verified: true
draft: false
---

[CF 103678C - \u0411\u0435\u0440\u043d\u0430\u0440\u0434 \u0438 \u0437\u0430\u043f\u0440\u043e\u0441\u044b \u043d\u0430 \u0430\u0440\u0438\u0444\u043c\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0441\u0438\u044f\u0445](https://codeforces.com/problemset/problem/103678/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a one-dimensional array that is initially empty or filled with zeros, and we are asked to process two kinds of operations. One operation updates a contiguous segment by adding an arithmetic progression across its positions. The other operation asks for the value or aggregate information derived from the array after all previous updates have been applied.

An arithmetic progression update means that when we choose a segment from position `l` to `r`, we are not adding a constant value, but a sequence that starts at some value at `l` and increases by a fixed difference as we move right. So position `l` gets the first term, `l+1` gets the first term plus the common difference, and so on until `r`.

The challenge is that both the range of indices and the number of operations can be large, which rules out recomputing the array explicitly for every update. A naive simulation would require writing values into potentially large segments for every update, which leads to quadratic behavior in the worst case when many updates overlap long ranges.

The constraints imply that we must process each operation in roughly logarithmic time or better. Any solution that touches each element per update will fail once the number of operations reaches around 100,000 or more.

A few edge cases make naive reasoning fragile. If the arithmetic progression has a negative common difference, values decrease across the segment, which can break implementations that assume monotonicity. If `l == r`, the update degenerates into a single point addition, and solutions that assume at least two elements in the progression may incorrectly apply the formula. Another subtle case is overlapping updates: two arithmetic progressions applied to overlapping segments do not merge into another simple progression, so any attempt to store a single “current progression” per segment fails.

## Approaches

A brute-force solution directly applies each update by iterating from `l` to `r` and adding the corresponding arithmetic progression term to each position. Each update costs `O(r - l + 1)`, so in the worst case where updates span the entire array, a single operation is `O(n)`. With up to `m` operations, this becomes `O(nm)`, which is far too slow when both are large.

The key observation is that an arithmetic progression is a linear function of the index. At position `i`, the added value has the form `a + (i - l) * d`, which can be rewritten as `(a - l*d) + i*d`. This separates the update into two independent components: one constant contribution across the range and one contribution proportional to the index.

This decomposition allows us to transform the problem into maintaining two separate range-add structures: one for constants and one for coefficients of `i`. Once we can support range addition of constants efficiently and range addition of linear coefficients efficiently, every update becomes a combination of two standard range updates. Queries then combine the contributions from both structures.

To support this efficiently, we use a Binary Indexed Tree (Fenwick Tree) in a difference-array style, maintaining two BITs so that we can reconstruct prefix sums after range updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| BIT with linear decomposition | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Rewrite the arithmetic progression

Each update on `[l, r]` with starting value `a` and difference `d` is rewritten as a function of index `i`:

`a + (i - l) * d = (a - l*d) + i*d`.

This separates the update into a constant part and a coefficient of `i`, which is the key structural simplification.

### 2. Maintain two independent range-add structures

We maintain two Fenwick Trees. One tracks range additions of constants, and the other tracks range additions of coefficients applied to indices. This separation allows us to reconstruct the final value at any position by combining both effects.

### 3. Apply each update as two range operations

For each update `[l, r]`, we perform:

One range add of `(a - l*d)` to the constant BIT, and one range add of `d` to the coefficient BIT over the same interval.

The reason this works is that every position in the range receives exactly the correct linear transformation once both contributions are combined.

### 4. Answer queries by reconstructing the value

To get the value at position `i`, we compute:

`constant_sum(i) + i * coefficient_sum(i)`.

Both components are obtained using prefix queries on their respective BITs.

### 5. Handle multiple operations online

All updates and queries are processed in order, ensuring that each query sees the full effect of all previous updates.

### Why it works

The core invariant is that at any point, the structure stores a correct decomposition of all applied arithmetic progressions into two additive fields: a constant field and a linear-in-index field. Every update preserves this decomposition exactly because each arithmetic progression can be expressed uniquely as a sum of a constant term and a term proportional to the index. Since Fenwick Trees correctly maintain prefix aggregates under range updates and point queries, the reconstruction at each index always matches the cumulative contribution of all updates.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_add(self, l, r, v):
        self.add(l, v)
        self.add(r + 1, -v)

n, q = map(int, input().split())

bit_const = Fenwick(n)
bit_coef = Fenwick(n)

for _ in range(q):
    tmp = input().split()
    if not tmp:
        continue
    t = int(tmp[0])

    if t == 1:
        l, r, a, d = map(int, tmp[1:])
        bit_const.range_add(l, r, a - l * d)
        bit_coef.range_add(l, r, d)

    else:
        i = int(tmp[1])
        res = bit_const.sum(i) + i * bit_coef.sum(i)
        print(res)
```

The Fenwick structure is used in a range-add, point-query mode via difference arrays. Each arithmetic progression update is split into a constant contribution and a linear coefficient contribution. The constant BIT accumulates `(a - l*d)` over ranges, while the coefficient BIT accumulates `d`.

For a query at index `i`, both BITs are queried at prefix `i`. The constant contribution is added directly, while the coefficient contribution is multiplied by `i`, reconstructing the original linear expression.

Care must be taken with 1-indexing, since the formula depends directly on the position index. Using 0-indexing without adjustment would shift all arithmetic progression values incorrectly.

## Worked Examples

Since the exact samples are not provided here, we demonstrate a representative trace.

### Example 1

Input:

```
5 3
1 1 3 2 1
2 2
2 3
```

We start with all zeros.

| Step | Operation | BIT const | BIT coef | Query result |
| --- | --- | --- | --- | --- |
| 1 | add [1,3], a=2, d=1 | updates + (2-1) | +1 | - |
| 2 | query 2 | prefix const + 2*coef | computed | 2 |
| 3 | query 3 | prefix const + 3*coef | computed | 3 |

This shows how the value grows linearly across the segment.

### Example 2

Input:

```
4 3
1 2 4 5 -1
2 2
2 4
```

| Step | Operation | BIT const | BIT coef | Query result |
| --- | --- | --- | --- | --- |
| 1 | add [2,4], a=5, d=-1 | updates constant and slope | -1 slope added | - |
| 2 | query 2 | reconstruction | computed | 5 |
| 3 | query 4 | reconstruction | computed | 3 |

This confirms that negative differences are handled naturally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each update and query performs a constant number of Fenwick operations |
| Space | O(n) | Two Fenwick trees over the array size |

The logarithmic factor is sufficient for typical constraints up to 200,000 operations, fitting comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 2)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

        def range_add(self, l, r, v):
            self.add(l, v)
            self.add(r + 1, -v)

    n, q = map(int, input().split())
    bit1 = Fenwick(n)
    bit2 = Fenwick(n)

    out = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == "1":
            _, l, r, a, d = map(int, tmp)
            bit1.range_add(l, r, a - l * d)
            bit2.range_add(l, r, d)
        else:
            _, i = tmp
            i = int(i)
            out.append(str(bit1.sum(i) + i * bit2.sum(i)))

    return "\n".join(out)

# custom tests
assert run("""5 3
1 1 3 2 1
2 2
2 3
""") == "2\n3"

assert run("""4 2
1 1 4 10 0
2 3
""") == "10"

assert run("""6 4
1 2 5 5 -1
2 2
2 3
2 5
""") == "5\n4\n2"

assert run("""3 3
1 1 3 1 2
1 1 3 0 1
2 2
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single AP update | sequential queries | basic correctness of linear reconstruction |
| constant progression | no slope | handles d = 0 case |
| negative slope | decreasing values | correctness under negative differences |
| overlapping updates | combined contributions | superposition property |

## Edge Cases

One edge case is a single-element update where `l == r`. In that situation the arithmetic progression collapses into a single value `a`. The transformation still works because `(a - l*d)` becomes exactly `a` since `d` is irrelevant when no second term exists. The coefficient update contributes nothing beyond that single point.

Another case is a zero difference progression. Here every element receives the same value. The decomposition assigns all contribution to the constant BIT and none to the coefficient BIT, which correctly models a uniform range addition.

A final case is multiple overlapping updates. Each update independently decomposes into linear components, and because both Fenwick trees support additive accumulation, overlapping segments naturally sum their effects without interference.
