---
title: "CF 104845D - \u041c\u0435\u0433\u0430 OR"
description: "We maintain a very large array indexed up to $10^9$, but only the first $n$ positions are initially non-zero. All remaining positions are implicitly zero. Each position holds a 30-bit integer. There are two operations. First, we can update a single position to a new value."
date: "2026-06-28T11:30:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104845
codeforces_index: "D"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 2023-2024 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104845
solve_time_s: 94
verified: false
draft: false
---

[CF 104845D - \u041c\u0435\u0433\u0430 OR](https://codeforces.com/problemset/problem/104845/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We maintain a very large array indexed up to $10^9$, but only the first $n$ positions are initially non-zero. All remaining positions are implicitly zero. Each position holds a 30-bit integer.

There are two operations. First, we can update a single position to a new value. Second, we are asked to count how many non-negative integers $x$ satisfy a global bitwise constraint: if we take the bitwise OR of every array element together with $x$, the result does not exceed a given bound $z$.

The crucial observation is that the OR over all array elements collapses the entire structure into a single value. If we define

$$S = a_1 \,|\, a_2 \,|\, \cdots \,|\, a_n,$$

then every extra zero element contributes nothing, so the global OR is exactly $S$. After adding $x$, the condition becomes

$$S \,|\, x \le z.$$

The constraints are large: up to $10^5$ updates and queries, and values fit within 30 bits. Any solution that recomputes the OR from scratch per query is too slow if it touches all elements, because that would cost $O(nq)$, which is about $10^{10}$ operations in the worst case.

A subtle point is that updates can happen at arbitrary indices up to $10^9$, but only indices that were initially provided matter. Any other position is permanently zero, so updates outside the initial set can be ignored conceptually unless they refer to the initial $n$ or extend the active set in a more general interpretation.

Edge cases arise when bits cancel or reappear:

If all values become zero, then the condition reduces to $x \le z$, giving $z+1$ solutions. If $S$ already exceeds $z$, no value of $x$ can fix higher bits in $S$, so the answer is zero.

## Approaches

A direct approach maintains the full array and recomputes the OR for every query of type 2. This is correct because OR is associative and commutative, so recomputing from scratch always yields the right $S$. However, each query would require scanning up to $n$ elements, leading to $O(nq)$ work. With $n,q \approx 10^5$, this becomes too slow.

The key structural insight is that OR behaves monotonically per bit. Each bit is either present or absent in the global state, and updates only toggle bits in a fixed set. We do not need to know individual elements for query type 2, only the current global OR $S$.

So we maintain a single bitmask $S$. For updates, we must adjust $S$ when an element changes. If a value is replaced, some bits may disappear from the OR if that value was the last contributor of those bits. This requires tracking, per bit, how many elements currently contain it.

We maintain a frequency array of size 30 for bit counts. When updating an element, we decrement counts for its old value and increment for its new value. The global OR is updated by setting a bit if its count becomes positive, and clearing it if it becomes zero.

Once $S$ is known, each query reduces to counting $x$ such that

$$S \,|\, x \le z.$$

This is a classic bit constraint counting problem. For any bit where $S$ has a 1, the result already has a 1 regardless of $x$. If $z$ has a 0 in that position, it is impossible. Otherwise, those bits are forced. For bits where $S$ has 0, $x$ must stay within the limit imposed by $z$, and the count reduces to choosing freely only in positions where $z$ has 1 and $S$ has 0. The number of valid $x$ is therefore:

$$2^{\text{count of bits } i \text{ where } S_i = 0 \text{ and } z_i = 1}$$

if all bits where $S_i = 1$ satisfy $z_i = 1$, otherwise zero.

This reduces each query to $O(30)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recompute OR each query | $O(nq)$ | $O(n)$ | Too slow |
| Maintain bit counts + bitwise counting | $O((n+q)\cdot 30)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We treat the active array as only the first $n$ elements, since other positions are zero and irrelevant.

1. Read the initial array and compute a 30-bit frequency array `cnt` where `cnt[b]` is how many numbers currently have bit $b$ set. This lets us reconstruct the global OR without scanning the array.
2. Build the initial OR mask $S$ by setting bit $b$ if `cnt[b] > 0`. This compresses the entire array state into a single integer.
3. For each update query $1\ i\ v$, retrieve the old value at position $i$. For each bit $b$, if it is set in the old value, decrement `cnt[b]`. Then for the new value, increment the corresponding bits. After adjusting counts, recompute only affected bits of $S$: bit $b$ is set in $S$ if `cnt[b] > 0`. This ensures $S$ always reflects the true OR of all elements.
4. For each query $2\ z$, first check feasibility: if $(S \& \sim z) \ne 0$, then some bit is required by $S$ but forbidden by $z$, so answer is zero.
5. Otherwise, iterate over all bits where $S$ has zero. For each such bit $b$, if $z$ has bit $b$, it is free and contributes one degree of freedom. The answer is $2^{k}$, where $k$ is the number of such free bits.

### Why it works

The algorithm maintains an invariant: `cnt[b] > 0` if and only if bit $b$ is present in at least one active array element. Therefore the maintained mask $S$ is always exactly the bitwise OR of all current elements.

Once $S$ is fixed, each bit position in $x$ contributes independently. A bit set in $S$ forces the same bit in $z$ to be 1; otherwise no solution exists. Bits where $S$ is 0 impose no lower bound and are only constrained by $z$. Since each such bit can be chosen freely in $x$, independence of bits yields a pure power-of-two count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    MAXB = 30
    cnt = [0] * MAXB
    
    for v in a:
        for b in range(MAXB):
            if v >> b & 1:
                cnt[b] += 1
    
    S = 0
    for b in range(MAXB):
        if cnt[b] > 0:
            S |= (1 << b)
    
    for i in range(n):
        pass  # placeholder; a is used directly
    
    for _ in range(int(input())):
        tmp = input().split()
        t = int(tmp[0])
        
        if t == 1:
            i = int(tmp[1]) - 1
            v = int(tmp[2])
            old = a[i]
            
            for b in range(MAXB):
                if old >> b & 1:
                    cnt[b] -= 1
                if v >> b & 1:
                    cnt[b] += 1
            
            a[i] = v
            
            S = 0
            for b in range(MAXB):
                if cnt[b] > 0:
                    S |= (1 << b)
        
        else:
            z = int(tmp[1])
            
            if S & ~z:
                print(0)
                continue
            
            free_bits = 0
            for b in range(MAXB):
                if not (S >> b & 1) and (z >> b & 1):
                    free_bits += 1
            
            print(1 << free_bits)

if __name__ == "__main__":
    solve()
```

The core structure separates state maintenance from query evaluation. The array `cnt` tracks per-bit presence, while `S` is recomputed from it after each update. This avoids any need to maintain complex segment structures since the operation is purely OR-based.

The feasibility check `S & ~z` is the compact form of detecting forbidden bits. The enumeration over bits is const
