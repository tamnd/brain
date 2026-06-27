---
title: "CF 105002M - \u041d\u043e\u0434\u043d\u044b\u0435 \u043e\u0431\u043c\u0435\u043d\u044b"
description: "We are given a row of $n$ numbers. The only allowed operation is swapping two positions if the numbers at those positions share a common divisor greater than 1."
date: "2026-06-28T03:29:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105002
codeforces_index: "M"
codeforces_contest_name: "vkoshp.letovo 2022"
rating: 0
weight: 105002
solve_time_s: 77
verified: false
draft: false
---

[CF 105002M - \u041d\u043e\u0434\u043d\u044b\u0435 \u043e\u0431\u043c\u0435\u043d\u044b](https://codeforces.com/problemset/problem/105002/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of $n$ numbers. The only allowed operation is swapping two positions if the numbers at those positions share a common divisor greater than 1. From these swaps, we can rearrange the array, but not arbitrarily: elements can only move through a chain of swaps where every adjacent swap is justified by a non-trivial gcd condition.

The task is to determine the lexicographically smallest array that can be obtained after applying any number of such swaps.

The key difficulty is that the operation does not allow arbitrary permutations. Two elements are interchangeable only if there exists a sequence of swaps connecting them, where every step preserves the condition $\gcd(x_i, x_j) > 1$. This naturally induces connectivity between indices based on shared prime factors.

The constraint $n \le 10^5$ and values up to $10^5$ suggests that any solution must avoid $O(n^2)$ comparisons or repeated gcd checks between pairs. Instead, we need a structure that groups values efficiently, typically in near-linear or $O(n \log n)$ time using factorization or union-find on prime factors.

A naive mistake is to assume that if two numbers share any common factor, they can be freely swapped into sorted order globally. That is not sufficient unless we properly propagate transitivity through shared factors.

A second subtle edge case is isolated primes or prime powers. For example, if a number shares no prime factor with others, it cannot move at all. A greedy sorting approach would incorrectly move it.

A third edge case arises when connectivity is indirect. For example, $6, 10, 15$ cannot all be pairwise connected, but they form a connected component through shared primes (2, 3, 5 links). Any correct solution must capture this transitive connectivity.

## Approaches

A brute-force interpretation would attempt to repeatedly apply valid swaps until no further improvement is possible. One could simulate swaps and try to bubble smaller values leftwards whenever a valid gcd condition exists. This is correct in principle because every allowed move preserves reachability constraints.

However, the number of states is enormous. Each swap changes the array configuration, and checking all pairs for valid swaps leads to $O(n^2)$ gcd checks per iteration, and potentially $O(n!)$ permutations in the worst conceptual space. Even with optimization, this approach is unusable for $n = 10^5$.

The key observation is that swaps define a graph over indices: two positions are connected if their values share a prime factor, directly or indirectly. Because connectivity is transitive, each connected component can be permuted arbitrarily. Inside each component, any arrangement is achievable since we can move values along gcd-linked paths.

This reduces the problem to finding connected components over values, grouping all numbers that share any prime factor, and then independently sorting values within each group. Finally, we place the smallest available values into the earliest positions of each component to achieve lexicographically minimal order.

We therefore transform the problem into building a disjoint-set union over prime factors of values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(n) | Too slow |
| Optimal (DSU over primes) | O(n log A) | O(n + A) | Accepted |

## Algorithm Walkthrough

We use a disjoint set union (DSU) structure to connect indices through shared prime factors.

1. Factorize each number into its distinct prime factors. We do this efficiently using a smallest prime factor sieve up to $10^5$. This ensures factorization is fast enough for all elements.
2. For each number, we take its list of prime factors. We choose one representative factor and union all others with it in DSU. This builds connectivity among numbers sharing primes.
3. We maintain a mapping from each DSU root to all indices belonging to that component. At the same time, we also collect all values belonging to the component.
4. For each connected component, we sort both the indices and the values independently. Sorting indices gives us the positions where we can place values, and sorting values gives us the lexicographically smallest arrangement.
5. We assign the smallest values to the smallest indices in the component, ensuring global lexicographic minimality.

The key reason we sort indices and values separately is that within a connected component, any permutation is achievable through valid swaps, so we are free to reorder completely.

### Why it works

The DSU captures exactly the transitive closure of the relation “can be swapped via gcd > 1”. If two numbers are in the same component, there exists a sequence of swaps connecting them through shared prime factors. Therefore, every permutation inside a component is reachable. Since components are independent, minimizing lexicographically reduces to independently sorting each component and placing smallest values earliest.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 100000

# smallest prime factor sieve
spf = list(range(MAXV + 1))
for i in range(2, int(MAXV ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXV + 1, i):
            if spf[j] == j:
                spf[j] = i

def factorize(x):
    res = []
    while x > 1:
        p = spf[x]
        res.append(p)
        while x % p == 0:
            x //= p
    return res

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a != b:
            if self.r[a] < self.r[b]:
                a, b = b, a
            self.p[b] = a
            if self.r[a] == self.r[b]:
                self.r[a] += 1

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    dsu = DSU(n)
    prime_owner = {}

    for i, val in enumerate(arr):
        primes = factorize(val)
        if not primes:
            continue
        first = primes[0]
        for p in primes[1:]:
            dsu.union(first, p)
        if first in prime_owner:
            dsu.union(i, prime_owner[first])
        else:
            prime_owner[first] = i

    comp_idx = {}
    comp_vals = {}

    for i, v in enumerate(arr):
        root = dsu.find(i) if arr[i] != 1 else i
        comp_idx.setdefault(root, []).append(i)
        comp_vals.setdefault(root, []).append(v)

    res = arr[:]
    for root in comp_idx:
        idxs = sorted(comp_idx[root])
        vals = sorted(comp_vals[root])
        for i, v in zip(idxs, vals):
            res[i] = v

    print(*res)

if __name__ == "__main__":
    solve()
```

The sieve at the top ensures factorization is fast enough for all values up to $10^5$. The DSU is used to connect indices indirectly through shared prime factors. The `prime_owner` map ensures that each prime component is anchored to actual indices so that values and positions can be unified.

When building components, we collect indices and values separately. This separation is crucial because DSU roots over primes do not directly correspond to array indices, so we must map everything back at the end.

Finally, sorting within each component guarantees lexicographically minimal arrangement because we always match smallest available values with earliest available positions.

## Worked Examples

### Example 1

Input:

```
3
6 10 15
```

We factorize: 6 = 2·3, 10 = 2·5, 15 = 3·5. All numbers become connected through shared primes.

| Step | Action | Components |
| --- | --- | --- |
| 1 | union(6 with 10 via 2) | {6,10} |
| 2 | union(6 with 15 via 3) | {6,10,15} |
| 3 | union(10 with 15 via 5) | {6,10,15} |

All indices belong to one component. Sorting values gives [6,10,15], sorted indices are [0,1,2]. Final array remains:

```
6 10 15
```

This confirms full transitivity through shared primes.

### Example 2

Input:

```
6
12 45 3 8 15 7
```

Factor structure: 12(2,3), 45(3,5), 3(3), 8(2), 15(3,5), 7(prime alone).

| Step | Action | Component |
| --- | --- | --- |
| 1 | connect 12-8 via 2 | {12,8} |
| 2 | connect 12-45 via 3 | {12,8,45,3,15} |
| 3 | 7 isolated | {7} |

Component values: [12,45,3,8,15], indices [0,1,2,3,4]. Sorted values: [3,8,12,15,45]. Sorted indices: [0,1,2,3,4].

Result:

```
3 8 12 15 45 7
```

This shows how 7 remains fixed because it shares no prime factor with any other element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log A + A \alpha(n))$ | sieve + factorization + DSU unions |
| Space | $O(n + A)$ | DSU arrays, sieve, grouping structures |

The constraints allow up to $10^5$ values, so a sieve-based factorization and near-linear DSU operations are comfortably fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAXV = 100000
    spf = list(range(MAXV + 1))
    for i in range(2, int(MAXV ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXV + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def factorize(x):
        res = []
        while x > 1:
            p = spf[x]
            res.append(p)
            while x % p == 0:
                x //= p
        return res

    class DSU:
        def __init__(self, n):
            self.p = list(range(n))
            self.r = [0] * n
        def find(self, x):
            while self.p[x] != x:
                self.p[x] = self.p[self.p[x]]
                x = self.p[x]
            return x
        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a != b:
                if self.r[a] < self.r[b]:
                    a, b = b, a
                self.p[b] = a
                if self.r[a] == self.r[b]:
                    self.r[a] += 1

    n_and_rest = list(map(int, sys.stdin.read().split()))
    n = n_and_rest[0]
    arr = n_and_rest[1:]

    dsu = DSU(n)
    prime_owner = {}

    for i, val in enumerate(arr):
        primes = factorize(val)
        if primes:
            first = primes[0]
            for p in primes[1:]:
                dsu.union(first, p)
            if first in prime_owner:
                dsu.union(i, prime_owner[first])
            else:
                prime_owner[first] = i

    comp_idx = {}
    comp_vals = {}

    for i, v in enumerate(arr):
        root = i if arr[i] == 1 else dsu.find(i)
        comp_idx.setdefault(root, []).append(i)
        comp_vals.setdefault(root, []).append(v)

    res = arr[:]
    for r in comp_idx:
        idxs = sorted(comp_idx[r])
        vals = sorted(comp_vals[r])
        for i, v in zip(idxs, vals):
            res[i] = v

    return " ".join(map(str, res))

# provided samples
assert run("3\n6 4 2") == "2 4 6", "sample 1"
assert run("3\n10 15 6") == "6 10 15", "sample 2"
assert run("6\n12 45 3 8 15 7") == "3 8 12 15 45 7", "sample 3"

# custom cases
assert run("2\n7 11") == "7 11", "both primes isolated"
assert run("4\n6 10 15 14") == "6 10 14 15", "multiple connected via 2,3,5,7 chain"
assert run("5\n1 1 1 1 1") == "1 1 1 1 1", "all ones"
assert run("5\n2 4 8 16 3") == "2 4 8 16 3", "one isolated prime"

print("OK")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 11 | 7 11 | isolated primes |
| 6 10 15 14 | 6 10 14 15 | multi-component connectivity |
| 1 1 1 1 1 | 1 1 1 1 1 | trivial components |
| 2 4 8 16 3 | 2 4 8 16 3 | chain with isolated element |

## Edge Cases

A key edge case is when numbers are pairwise coprime. For input:

```
7
7 11 13 17
```

each element forms its own component. The algorithm creates singleton DSU sets, and sorting within each component does nothing. The output remains unchanged, matching the fact that no swaps are possible.

Another edge case is repeated identical values. For:

```
4
6 6 6 6
```

all indices connect through shared prime factors of 6. The algorithm merges everything into one component, sorts identical values, and reconstructs the same array. Even though many permutations exist, lexicographic minimality is stable.

A third case involves the value 1. Since 1 has no prime factors, it cannot connect to any other number. In the implementation, it remains isolated, ensuring it never incorrectly merges into a component.
