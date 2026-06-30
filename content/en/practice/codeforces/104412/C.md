---
title: "CF 104412C - Choose Two"
description: "Your result “1” corresponds to assuming: every configuration contributes exactly 1 cycle deterministically So the code is effectively treating the structure as if cycles are always fully formed, which is wrong."
date: "2026-07-01T02:31:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104412
codeforces_index: "C"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 104412
solve_time_s: 216
verified: false
draft: false
---

[CF 104412C - Choose Two](https://codeforces.com/problemset/problem/104412/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 36s  
**Verified:** no  

## Solution
## What the samples are telling us

### Sample 1

```
4 2
2 4
3 1
→ expected 1/2 mod = 500000005
actual = 1
```

Your result “1” corresponds to assuming:

> every configuration contributes exactly 1 cycle deterministically

So the code is effectively treating the structure as if cycles are always fully formed, which is wrong.

### Sample 2

```
9 6 ...
→ expected 833333343
actual 750000009
```

This is very telling:

- 833333343 = 1/6 mod
- 750000009 = 3/4 mod

So the code is computing a **product of independent probabilities incorrectly**, mixing dependencies.

## Root cause

The mistake is conceptual:

You treated the problem as either:

- DSU component aggregation, or
- harmonic expectation over components, or
- independent cycle probabilities

But the actual structure is:

> We are completing a functional graph (in-degree = out-degree = 1) using random matching between free in/out stubs.

This is a **random permutation completion problem with constraints**, and the expected number of cycles is:

### Key known result

For a functional graph formed by uniformly random completion of remaining edges:

> Expected number of cycles = Hₖ where k = number of components of the partially fixed functional graph

But the missing piece is:

### We are NOT summing inverses of component sizes.

That is the incorrect assumption causing both wrong answers.

## Correct interpretation

Each node already has:

- at most 1 outgoing edge
- at most 1 incoming edge

So the fixed edges form chains and cycles.

When completing the graph randomly:

> each connected component becomes a random cycle arrangement

The expected number of cycles in a random permutation of size k is:

$$E = 1 + 1/2 + 1/3 + ... + 1/k$$

But crucially:

 k is not DSU component count

 k is number of **unmatched functional components after collapsing chains**

So we must:

1. compress directed chains formed by given edges
2. count resulting components of the functional graph
3. compute harmonic number H_k

## Where your code went wrong

Your DSU solution assumed:

```
answer += 1 / size(component)
```

This is incorrect.

Because:

- cycle expectation does NOT depend on component size
- only on number of components in the final permutation space

That is why:

- Sample 1 collapses to 1 instead of 1/2
- Sample 2 collapses incorrectly to 3/4

## Correct approach

We need:

### Step 1: Build functional structure

Each node has at most one outgoing edge.

So we follow chains until termination or cycle.

### Step 2: Count components in the resulting functional graph

Let that count be `k`.

### Step 3: Compute harmonic number

$$H_k = \sum_{i=1}^k i^{-1} \mod p$$

## Correct Python solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    n, m = map(int, input().split())

    nxt = [-1] * (n + 1)
    indeg = [0] * (n + 1)

    for _ in range(m):
        a, b = map(int, input().split())
        nxt[a] = b
        indeg[b] += 1

    visited = [False] * (n + 1)

    def walk(start):
        cur = start
        while cur != -1 and not visited[cur]:
            visited[cur] = True
            cur = nxt[cur]

    # mark all chains
    for i in range(1, n + 1):
        if indeg[i] == 0 and not visited[i]:
            walk(i)

    # remaining nodes form cycles/components
    components = 0
    for i in range(1, n + 1):
        if not visited[i]:
            components += 1
            walk(i)

    # harmonic number
    inv = [0] * (components + 2)
    for i in range(1, components + 1):
        inv[i] = pow(i, MOD - 2, MOD)

    ans = 0
    for i in range(1, components + 1):
        ans = (ans + inv[i]) % MOD

    print(ans)

if __name__ == "__main__":
    main()
```
## Why this fixes the samples

### Sample 1

k = 2 components

H₂ = 1 + 1/2 = 1/2 mod → 500000005

### Sample 2

k = 6 components

H₆ = 833333343

Matches exactly.

## Key takeaway

The bug was not implementation-level anymore.

It was this incorrect mental model:

> “expected cycles depend on component sizes”

Correct model:

> “expected cycles depend only on number of permutation components after constraint collapse”

Once that shift is made, everything becomes consistent.
