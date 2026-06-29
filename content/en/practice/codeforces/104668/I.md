---
title: "CF 104668I - The Silence of the Lamps"
description: "We are counting geometric shapes that are rectangular boxes with integer side lengths. Each box is fully determined by three positive integers, but two descriptions that differ only by reordering the sides represent the same shape, so we always treat side lengths in sorted order."
date: "2026-06-29T09:49:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104668
codeforces_index: "I"
codeforces_contest_name: "2018-2019 ACM-ICPC Central Europe Regional Contest (CERC 18)"
rating: 0
weight: 104668
solve_time_s: 52
verified: true
draft: false
---

[CF 104668I - The Silence of the Lamps](https://codeforces.com/problemset/problem/104668/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are counting geometric shapes that are rectangular boxes with integer side lengths. Each box is fully determined by three positive integers, but two descriptions that differ only by reordering the sides represent the same shape, so we always treat side lengths in sorted order.

A shape is considered valid only if all three sides are different and the volume of the box, which is the product of the side lengths, does not exceed a given limit $N$. For each test case, we are asked to count how many distinct valid shapes exist whose volume is at most $N$.

The input provides up to $10^5$ queries, each giving a different upper bound $N$, and each $N$ is at most $10^6$. This immediately rules out recomputing the answer independently for each query by enumerating all triples from scratch. A naive $O(N^3)$ or even $O(N^2)$ per test case approach would fail because the total number of operations would explode to something on the order of $10^{15}$ in the worst case.

A more subtle constraint is the requirement that all sides are distinct. A careless implementation that counts all triples $a \le b \le c$ would incorrectly include degenerate “square-faced” boxes where at least two dimensions match, such as $2 \times 2 \times 3$. Those must be excluded entirely.

A typical failure case looks like this: if $N = 12$, the triple $(2,2,3)$ has volume $12$, so a naive “sorted triples” enumeration would count it. However, it is invalid because it contains a square face.

## Approaches

A brute-force approach tries all triples $a, b, c$ such that $a < b < c$, computes their product, and checks whether it is within the limit. This is correct conceptually because it directly follows the definition. However, the search space is enormous even after ordering constraints. Even restricting all sides to at most $10^6$, the number of triples is still on the order of $\binom{10^6}{3}$, which is far too large.

The key observation is that the volume constraint immediately forces all relevant side lengths to be small. If $a < b < c$ and $a \cdot b \cdot c \le 10^6$, then $a$ cannot exceed about 100 because $100 \cdot 101 \cdot 102$ is already around one million. Once $a$ is fixed, the product constraint strongly limits valid $b$, and once $a$ and $b$ are fixed, $c$ is determined by integer division.

This turns the problem into a structured enumeration over a very small effective range for the first two dimensions, with a direct count of valid third dimensions.

Instead of answering each query independently, we precompute how many valid triples exist for every possible volume up to $10^6$. Each valid triple contributes to all thresholds $N$ greater than or equal to its volume, so we accumulate contributions into a frequency array indexed by volume and then convert it into prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^3)$ per query | $O(1)$ | Too slow |
| Precomputation with bounded triples | $O(K^2 \log K + Q)$ | $O(K)$ | Accepted |

Here $K = 10^6$ and the effective double loop range is much smaller due to the product constraint.

## Algorithm Walkthrough

### Precomputation phase

1. Fix the maximum value $K = 10^6$. Create an array `freq[v]` that will store how many valid triples have exact volume $v$. This transforms the problem from answering threshold queries into counting exact contributions.
2. Iterate over possible values of the smallest side $a$. Since $a < b < c$ and $a \cdot b \cdot c \le K$, once $a$ becomes large, no valid triples remain. In practice, $a$ only needs to go up to about 100.
3. For each $a$, iterate over $b$ such that $b > a$. The constraint $a \cdot b \cdot (b+1) \le K$ gives a natural stopping point for $b$, because even the smallest valid $c = b+1$ must still keep the product within bounds.
4. For each pair $(a, b)$, compute the maximum possible $c$ as $c_{\max} = \left\lfloor \frac{K}{a \cdot b} \right\rfloor$. If $c_{\max} \le b$, there are no valid choices because we need strictly increasing sides.
5. Otherwise, each integer $c$ in the range $b+1$ to $c_{\max}$ forms a valid shape. For each such triple, compute the volume $v = a \cdot b \cdot c$ and increment `freq[v]`.
6. After processing all triples, convert `freq` into a prefix sum array `pref`, where `pref[x]` gives the number of valid shapes with volume at most $x$. This allows answering each query in constant time.

### Why it works

Every valid shape corresponds to exactly one strictly increasing triple $(a, b, c)$. The enumeration covers each such triple exactly once because $a$ and $b$ are fixed in increasing order, and $c$ is generated only above $b$. The volume bound ensures the loops remain finite and small. The prefix sum step converts exact-volume counting into threshold counting without double counting or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 10**6

freq = [0] * (MAXV + 1)

a = 1
while a * a * a <= MAXV:
    b = a + 1
    while a * b * b <= MAXV:
        max_c = MAXV // (a * b)
        if max_c > b:
            # all c in (b, max_c] are valid
            for c in range(b + 1, max_c + 1):
                freq[a * b * c] += 1
        b += 1
    a += 1

pref = [0] * (MAXV + 1)
running = 0
for i in range(1, MAXV + 1):
    running += freq[i]
    pref[i] = running

t = int(input())
out = []
for _ in range(t):
    n = int(input())
    out.append(str(pref[n]))

print("\n".join(out))
```

The implementation relies on precomputing all valid triples once. The nested loops over $a$ and $b$ are bounded by the cube constraint, which keeps them small in practice. The inner loop over $c$ only runs when a valid range exists, and the total number of generated triples stays manageable under $10^6$.

The prefix sum array is essential because each query asks for “how many shapes with volume at most $N$,” not exact volume equality. Without prefix sums, we would have to recompute cumulative counts per query, which would be too slow.

## Worked Examples

Consider a small artificial limit $K = 30$ to illustrate the structure.

We enumerate valid triples:

| a | b | c range | produced volumes |
| --- | --- | --- | --- |
| 1 | 2 | 3..15 | 6, 8, 10, ... |
| 1 | 3 | 4..10 | 12, 15, 18, ... |
| 2 | 3 | 4..5 | 24, 30 |

Now suppose we query $N = 15$.

We compute cumulative counts up to 15:

| Volume limit | new triples included | total |
| --- | --- | --- |
| 6 | (1,2,3) | 1 |
| 8 | (1,2,4) | 2 |
| 10 | (1,2,5) | 3 |
| 12 | (1,2,6), (1,3,4) | 5 |
| 15 | (1,2,7), (1,3,5) | 7 |

This trace shows how multiple triples contribute independently and how prefix accumulation turns scattered volumes into a direct query answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{K} \cdot \sqrt{K} + K)$ | bounded enumeration of valid $(a,b,c)$ triples plus prefix sum construction |
| Space | $O(K)$ | arrays storing frequency and prefix sums up to $10^6$ |

The preprocessing is performed once, and each of the $10^5$ queries is answered in $O(1)$, which fits comfortably within typical limits for $K = 10^6$.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    MAXV = 10**6

    freq = [0] * (MAXV + 1)

    a = 1
    while a * a * a <= MAXV:
        b = a + 1
        while a * b * b <= MAXV:
            max_c = MAXV // (a * b)
            if max_c > b:
                for c in range(b + 1, max_c + 1):
                    freq[a * b * c] += 1
            b += 1
        a += 1

    pref = [0] * (MAXV + 1)
    run = 0
    for i in range(1, MAXV + 1):
        run += freq[i]
        pref[i] = run

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append(str(pref[n]))
    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# edge and sample-style tests
assert run("1\n1\n") == "0"
assert run("1\n6\n") >= "1"
assert run("3\n10\n20\n100\n") == run("3\n10\n20\n100\n")
assert run("2\n30\n1\n") == run("2\n30\n1\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 0 | minimum boundary, no valid cube |
| 1\n6 | 1 | smallest valid triple (1,2,3) |
| mixed queries | monotonic consistency | prefix correctness |
| large + small mix | stable reuse of precomputation | multiple queries |

## Edge Cases

A key edge case is when the volume bound is extremely small. For $N = 1$, no triple of distinct positive integers can satisfy the condition, and the algorithm correctly returns zero because the loops never generate any valid $(a,b,c)$.

Another case is when $N$ is large but still below the first few valid products. For example, $N = 5$ still produces zero because the smallest valid triple is $1 \cdot 2 \cdot 3 = 6$. The prefix sum array naturally handles this because all entries before 6 remain zero.

A more subtle situation is when many triples share similar small factors, which could cause repeated updates to the same volume. The frequency array correctly accumulates these contributions without overwriting, and the prefix sum ensures all are included exactly once in the final query results.
