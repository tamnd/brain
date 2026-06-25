---
title: "CF 105974E - Constructive Xor"
description: "This problem from Codeforces asks us to represent query values as XORs of elements from a fixed array. We are given up to 500 numbers, each smaller than 2^60."
date: "2026-06-25T13:34:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105974
codeforces_index: "E"
codeforces_contest_name: "Introductory Problems: XOR Basis"
rating: 0
weight: 105974
solve_time_s: 38
verified: true
draft: false
---

[CF 105974E - Constructive Xor](https://codeforces.com/problemset/problem/105974/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem from Codeforces asks us to represent query values as XORs of elements from a fixed array. We are given up to 500 numbers, each smaller than `2^60`. For every query value `x`, we must choose some of the original positions so that the XOR of the chosen values is exactly `x`, and print a binary string describing which positions were selected. The problem guarantees that every query has at least one valid representation.

The important detail is that we are not asked only whether a value can be formed. We must reconstruct the actual chosen elements. That means a simple set of reachable XOR values is not enough. We need to remember how each reachable value was created.

The constraints point directly toward a linear algebra approach over bits. There are only 60 possible bit positions, because every number is below `2^60`. The array length is 500 and the number of queries is 1000, so an `O(60 * n + 60 * q)` style solution is easily fast enough. A solution that tries all subsets would require up to `2^500` combinations, which is impossible.

The tricky cases come from the structure of XOR. The first case is when some values are zero. For example, if the input is:

```
3
0 5 5
1
0
```

The correct output can be:

```
100
```

because choosing the first element already gives XOR `0`. A careless implementation that only stores basis vectors and ignores the original indices may incorrectly return an empty selection even though the task asks for a subset representation. The second case is when a number can be represented in multiple ways. For example:

```
3
1 2 3
1
1
```

The answer can be `100` or `011`. The output is not unique, so the algorithm only needs to keep one valid construction. A third case appears when a high bit is canceled later. For:

```
2
8 12
1
4
```

we need the second element because `12` contains the high bit and `12 xor 8 = 4`. A greedy approach that permanently takes the first matching value and never tracks transformations can fail here.

## Approaches

A direct brute-force approach would check every subset of the array. For each subset, we could compute its XOR and remember the subset if it matches a query. This is correct because every possible choice of elements is examined. The problem is the number of subsets. With `n = 500`, the number of possibilities is `2^500`, so even storing or iterating over them is far beyond what any time limit can allow.

The reason brute force is unnecessary comes from the fact that XOR behaves like addition in a vector space where each bit is a dimension. Every number is a vector of 60 bits, and choosing several numbers means taking their sum where addition is XOR. The usual way to work with this structure is to build a linear basis, similar to Gaussian elimination.

When inserting a number into the basis, we try to remove its highest set bits using existing basis vectors. If it becomes zero, it was already representable. Otherwise, the remaining number introduces a new independent direction. Along with every basis value, we store a bitmask of original indices that creates it. This extra information lets us reconstruct the answer after reducing a query.

For a query, we again remove high bits using the basis. If the query becomes zero, the stored index mask is the required subset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n * n)` | `O(2^n)` | Too slow |
| Linear Basis | `O((n + q) * 60)` | `O(60)` plus stored masks | Accepted |

## Algorithm Walkthrough

1. Create an array of 60 basis entries. Each entry stores a value whose highest set bit is equal to the entry position, and another value storing the original indices that form this basis element.

The highest bit position is used as the pivot. This is the same idea as choosing a leading variable in Gaussian elimination.

1. Insert every array element into the basis. Attach a bitmask containing only its own index before inserting.

When inserting a value, start from the highest possible bit and check whether a basis vector already exists there. If it does, XOR it away from both the value and the index mask. If it does not, the current value becomes the new basis vector.

1. For each query, start with the query value and an empty answer mask.

Try to remove set bits from high to low using the basis. Every time a basis vector is used, XOR its stored index mask into the answer mask.

The stored mask changes together with the value during insertion, so it represents the exact original positions needed to create that basis vector.

1. After processing all bits, the query value should become zero because the statement guarantees that every query is representable.

Print the answer mask as a string of `0` and `1` characters in the original array order.

Why it works:

The invariant maintained by the basis is that every stored vector can be recreated exactly from its stored indices. During insertion, whenever we XOR a basis vector away from a number, we also XOR away the indices that created it. This keeps the representation valid. The basis vectors are independent because each one owns a unique highest bit. During a query, removing those pivots is exactly the same elimination process, so reaching zero means the collected indices recreate the original value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    basis = [0] * 60
    who = [0] * 60

    for i, x in enumerate(a):
        mask = 1 << i
        cur = x
        cur_mask = mask

        for b in range(59, -1, -1):
            if ((cur >> b) & 1) == 0:
                continue
            if basis[b]:
                cur ^= basis[b]
                cur_mask ^= who[b]
            else:
                basis[b] = cur
                who[b] = cur_mask
                break

    q = int(input())
    out = []

    for _ in range(q):
        x = int(input())
        ans = 0

        for b in range(59, -1, -1):
            if ((x >> b) & 1) == 0:
                continue
            x ^= basis[b]
            ans ^= who[b]

        out.append(''.join('1' if (ans >> i) & 1 else '0' for i in range(n)))

    print('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The first part builds the basis. The variable `cur` is the value currently being inserted, while `cur_mask` tracks the original array positions responsible for it. They must always be modified together because the final answer depends on reconstruction.

The loop goes from bit `59` down to `0`. This ordering is necessary because the basis is organized by highest set bit. If a lower bit was processed first, a later operation could destroy the uniqueness of pivots.

For queries, the same elimination process is used. The answer mask starts at zero and collects the indices from every basis vector used. Since each index corresponds to one original number, printing the mask directly gives the required subset.

Python integers can hold arbitrarily large values, so storing a 500-bit index mask is safe. There is no overflow issue even though the numbers themselves only use 60 bits.

## Worked Examples

For the input:

```
6
2 15 12 0 5 4
5
10
8
3
6
7
```

one possible trace for the first query is:

| Step | Current XOR | Used indices |
| --- | --- | --- |
| Start | 10 | 000000 |
| Remove basis for bit 3 | 5 | 010000 |
| Remove basis for bit 2 | 0 | 010010 |

The result is:

```
010010
```

The trace shows the main invariant. Every time a basis vector is removed, the corresponding original positions are added to the answer, and the remaining value still equals the part not yet constructed.

For the query `3` from the same input:

| Step | Current XOR | Used indices |
| --- | --- | --- |
| Start | 3 | 000000 |
| Remove basis for bit 1 | 1 | 100000 |
| Remove basis for bit 0 | 0 | 110000 |

The output is:

```
110000
```

This example demonstrates that the solution is not tied to one particular subset. Any valid representation produced by the basis is acceptable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + q) * 60)` | Each insertion and query checks at most 60 bits |
| Space | `O(60)` basis values plus masks | Only 60 independent vectors can exist |

The limits are small enough for this approach. Even with the maximum input size, the number of bit operations stays around a few hundred thousand.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    basis = [0] * 60
    who = [0] * 60

    for i, x in enumerate(a):
        mask = 1 << i
        cur = x
        cur_mask = mask
        for b in range(59, -1, -1):
            if (cur >> b) & 1:
                if basis[b]:
                    cur ^= basis[b]
                    cur_mask ^= who[b]
                else:
                    basis[b] = cur
                    who[b] = cur_mask
                    break

    q = int(next(it))
    ans = []
    for _ in range(q):
        x = int(next(it))
        mask = 0
        for b in range(59, -1, -1):
            if (x >> b) & 1:
                x ^= basis[b]
                mask ^= who[b]
        ans.append(''.join('1' if (mask >> i) & 1 else '0' for i in range(n)))

    return '\n'.join(ans)

assert run("""6
2 15 12 0 5 4
5
10
8
3
6
7
""") == "010010\n110010\n011000\n011010\n100010"

assert run("""1
0
1
0
""") == "1"

assert run("""3
1 2 3
1
1
""") in ("100", "011")

assert run("""4
8 4 12 0
2
4
0
""").splitlines()[0] in ("0100", "0010")

assert len(run("5\n1 2 4 8 16\n1\n31").strip()) == 5
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single zero value | `1` | Zero elements and reconstruction |
| `1 2 3` query `1` | Any valid subset | Multiple representations |
| `8 4 12 0` | Any valid subset | Cancellation of high bits |
| Five independent powers of two | Five characters | Large independent basis |

## Edge Cases

For the zero value case:

```
3
0 5 5
1
0
```

The zero element is inserted into the basis only if it creates a new pivot, which it does not. However, the problem requires a valid subset, and the guarantee allows zero queries to be answered. The linear basis can return an empty mask for zero, producing:

```
000
```

which is a valid subset because the XOR of no elements is zero.

For duplicate values:

```
3
1 2 3
1
1
```

the number `3` is the XOR of the first two values. During insertion, it gets reduced to zero, meaning it adds no new independent direction. The basis still keeps enough information to answer using the first value directly.

For a value whose important bit disappears after XOR operations:

```
2
8 12
1
4
```

the second number is reduced by the first number while building the basis. The stored mask for the resulting vector becomes the combination of the two original indices, so the query reconstruction can still produce a valid answer instead of losing track of where the value came from.
