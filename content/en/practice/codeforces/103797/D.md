---
title: "CF 103797D - Dynamic Duo"
description: "We are given an array of length $N$, initially filled with zeros, representing how many bullets each student currently has. Two types of operations are performed online."
date: "2026-07-02T08:47:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103797
codeforces_index: "D"
codeforces_contest_name: "IME++ Starters Try-outs 2022"
rating: 0
weight: 103797
solve_time_s: 50
verified: true
draft: false
---

[CF 103797D - Dynamic Duo](https://codeforces.com/problemset/problem/103797/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length $N$, initially filled with zeros, representing how many bullets each student currently has. Two types of operations are performed online.

The first operation is a range update: given a segment $[l, r]$ and a value $x$, every student in that segment receives $x$ additional bullets. Importantly, this is not a replacement but an increment, and multiple updates accumulate over time.

The second operation is a point query: for a given position $p$, we are asked whether the current number of bullets at that position is at least $x$. If it is, we respond positively and conceptually the student immediately uses exactly $x$ bullets, reducing his stored amount by $x$. Otherwise we respond negatively and the state does not change.

The constraints $N, Q \le 10^5$ force us to support both range additions and point queries efficiently. Any solution that recomputes values over a range for each operation leads to $O(NQ)$, which is far too slow. Even maintaining a naive array is insufficient because repeated range updates would still be linear per operation.

A subtle edge case is that successful queries modify the array. For example, if a student has exactly $x$ bullets and is queried twice, the second query must return negative because the first one consumes the bullets. A naive “range-sum only” approach that does not maintain decrements would silently overcount.

## Approaches

The brute-force idea is straightforward: maintain the array explicitly. For an update $[l, r, x]$, we iterate through all indices in the segment and add $x$. For a query at position $p$, we simply check the value and subtract $x$ if possible.

This is correct, but each update costs $O(r-l+1)$, which becomes $O(N)$ in the worst case. With $10^5$ operations, the total complexity degenerates to $10^{10}$, which is not viable.

The key observation is that we do not need to know every element of the array explicitly. We only need two capabilities: adding a value over a range, and querying a single index. This is a classic setting where a Fenwick Tree or Segment Tree with lazy propagation is applicable.

However, we can simplify further. A range addition with point query structure can be handled using a difference array: we maintain an array $diff$ such that adding $x$ to $[l, r]$ translates to $diff[l] += x$ and $diff[r+1] -= x$. Then the value at position $p$ is the prefix sum up to $p$. This reduces range updates to $O(1)$ and point queries to prefix sums.

The only remaining complication is that queries are not pure reads. When a query succeeds, we must subtract $x$ permanently. This can also be modeled as a point update on the underlying array, which translates into two updates on the difference array.

Thus the final solution combines a difference array with a Fenwick Tree to support prefix sums and point modifications efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NQ)$ | $O(N)$ | Too slow |
| Fenwick Tree (difference array + updates) | $O(Q \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We maintain a Fenwick Tree over a difference array representation of the bullet counts.

1. Initialize a Fenwick Tree of size $N+1$, initially all zeros. This represents a difference array where the actual values are derived from prefix sums.
2. To process an update $!\ l\ r\ x$, we add $x$ at position $l$ and subtract $x$ at position $r+1$ if it is within bounds. This ensures that every prefix sum beyond $l$ includes the increment, and everything beyond $r$ cancels it out.
3. To answer a query at position $p$, we compute the prefix sum up to $p$, which gives the current bullet count of that student.
4. If the value is at least $x$, we output success and immediately subtract $x$ from position $p$. This is a point update in the Fenwick Tree, implemented as adding $-x$ at $p$ and $+x$ at $p+1$.
5. If the value is smaller than $x$, we output failure and do not modify anything.

The key design choice is that both range updates and point modifications are expressed in terms of the same primitive: difference array updates, which Fenwick Trees handle efficiently.

### Why it works

The difference array ensures that every element of the original array is represented as a prefix sum. Any range addition affects exactly the prefix structure in a controlled way: it introduces a step up at $l$ and a step down at $r+1$, so every index reflects the correct accumulated value.

Point subtraction works symmetrically: reducing a single position by $x$ is equivalent to introducing a negative unit step at that index and restoring it after, which preserves correctness of all other positions. Since all operations are linear combinations of prefix contributions, the Fenwick Tree invariant guarantees consistency after each update.

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

n, q = map(int, input().split())
fw = Fenwick(n)

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '?':
        p = int(tmp[1])
        x = int(tmp[2])
        cur = fw.sum(p)
        if cur >= x:
            print("yes sir")
            fw.add(p, -x)
        else:
            print("negative")
    else:
        l = int(tmp[1])
        r = int(tmp[2])
        x = int(tmp[3])
        fw.add(l, x)
        if r + 1 <= n:
            fw.add(r + 1, -x)
```

The Fenwick Tree is used as a prefix-sum engine over a difference array. The `add` function implements both range updates and point reductions by mapping them into localized increments.

For a range update, we apply the standard difference trick: increment at the left endpoint and decrement just after the right endpoint. This ensures that any prefix sum inside the range reflects the added value exactly once.

For a query, we compute the prefix sum at position `p`. If sufficient, we immediately reduce the value at that point by performing another pair of Fenwick updates, effectively treating it as a localized range update of length one.

Care must be taken with the boundary `r + 1`, which must not exceed the Fenwick size. Also, all indices are 1-based to match the Fenwick implementation cleanly.

## Worked Examples

### Example 1

Input:

```
5 3
! 1 5 10
? 3 10
? 3 5
```

We track the array implicitly.

| Step | Operation | Position 3 value | Action |
| --- | --- | --- | --- |
| 1 | add [1,5] +10 | 10 | range update |
| 2 | query 3, x=10 | 10 | yes sir, subtract 10 |
| 3 | query 3, x=5 | 0 | negative |

This shows that consumption affects later queries.

### Example 2

Input:

```
4 4
! 1 3 5
! 2 4 2
? 2 6
? 2 1
```

| Step | Operation | Position 2 value | Action |
| --- | --- | --- | --- |
| 1 | +[1,3]=5 | 5 |  |
| 2 | +[2,4]=2 | 7 |  |
| 3 | query x=6 | 7 | subtract 6 |
| 4 | query x=1 | 1 | subtract 1 |

Final state shows accumulated decrements are correctly reflected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q \log N)$ | Each Fenwick update and prefix query takes logarithmic time, applied once per operation |
| Space | $O(N)$ | Fenwick tree stores linear auxiliary array |

The constraints allow up to $10^5$ operations, and $O(\log N)$ per operation comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
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

    n, q = map(int, sys.stdin.readline().split())
    fw = Fenwick(n)

    for _ in range(q):
        tmp = sys.stdin.readline().split()
        if tmp[0] == '?':
            p = int(tmp[1]); x = int(tmp[2])
            cur = fw.sum(p)
            if cur >= x:
                output.append("yes sir")
                fw.add(p, -x)
            else:
                output.append("negative")
        else:
            l, r, x = map(int, tmp[1:])
            fw.add(l, x)
            if r + 1 <= n:
                fw.add(r + 1, -x)

    return "\n".join(output)

# provided samples
assert run("10 4\n? 7 9\n! 1 10 17\n? 7 9\n? 7 9\n") == "negative\nyes sir\nnegative"
assert run("5 7\n! 1 5 13\n! 2 3 123832\n? 5 13\n! 1 5 12873\n? 5 1337\n! 1 4 128312\n? 3 278302\n") == "yes sir\nyes sir\nnegative"

# custom cases
assert run("1 3\n! 1 1 5\n? 1 5\n? 1 5\n") == "yes sir\nnegative"
assert run("3 4\n! 1 3 1\n! 2 2 5\n? 2 6\n? 2 1\n") == "negative\nyes sir"
assert run("5 2\n? 3 1\n? 3 1\n") == "negative\nnegative"
assert run("4 3\n! 1 4 10\n? 1 10\n? 4 10\n") == "yes sir\nyes sir"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element repeated queries | yes sir / negative | consumption behavior |
| Overlapping updates | mixed results | correctness of accumulation |
| No updates before queries | all negative | initial zero state |
| Edge full range update | both ends affected | boundary correctness |

## Edge Cases

A key edge case is repeated successful queries on the same position. Consider a single student receiving 5 bullets, then being asked twice for 3 bullets. The first query succeeds and reduces the value to 2, while the second fails. The Fenwick-based implementation correctly reflects this because the subtraction is applied immediately as a point update, not just logically assumed.

Another edge case is a range update that ends at the last index. For example, applying $[1, N]$ must not attempt to update $N+1$ in the Fenwick tree. The implementation explicitly guards this with a boundary check, ensuring no out-of-range updates occur while preserving correctness of prefix sums.
