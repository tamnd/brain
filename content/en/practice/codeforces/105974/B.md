---
title: "CF 105974B - Distinct Xor Subsequence Queries"
description: "The task is to maintain a sequence while values are appended to it. After each append operation, some queries ask for the k-th smallest distinct value that can be obtained by taking any subsequence of the current sequence and XORing the chosen elements."
date: "2026-06-25T13:33:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105974
codeforces_index: "B"
codeforces_contest_name: "Introductory Problems: XOR Basis"
rating: 0
weight: 105974
solve_time_s: 44
verified: true
draft: false
---

[CF 105974B - Distinct Xor Subsequence Queries](https://codeforces.com/problemset/problem/105974/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to maintain a sequence while values are appended to it. After each append operation, some queries ask for the k-th smallest distinct value that can be obtained by taking any subsequence of the current sequence and XORing the chosen elements. The empty subsequence is allowed, so zero is always one of the possible answers. If fewer than k different XOR results exist, the query returns -1. This is the query version of maintaining the XOR span of a sequence.

The sequence length can grow to 200000 and every value fits into 60 bits. A solution that tries to generate subsequences is immediately impossible because the number of subsequences grows exponentially. Even a solution that stores every reachable XOR value would eventually need to handle up to 2^60 possible values, which cannot fit in memory. The useful observation is that XOR behaves like linear algebra over bits. The number of bits is fixed at 60, so operations proportional to the bit count are possible.

A few edge cases are easy to miss. Consider a sequence containing only repeated values.

```
Input
3
1 5
1 5
2 3
```

After the two insertions, the possible XOR values are only 0 and 5. The answer is -1, not another generated value. A solution that counts inserted elements instead of independent XOR directions will fail here.

Another case is when a value can be formed from previous values.

```
Input
4
1 1
1 2
1 3
2 4
```

The reachable values are 0, 1, 2, 3. The answer is -1 because there are only four distinct values. A careless implementation may think three numbers create eight subsequences and answer as if there were eight different XOR results.

A boundary case is the first query.

```
Input
2
2 1
2 2
```

Before any insertion, the only possible XOR is 0 from the empty subsequence. The first query returns 0 and the second returns -1. The basis must support the empty XOR value even though no numbers have been inserted.

## Approaches

The straightforward approach is to keep a set of all XOR values that can be created. When a new number arrives, every existing value can either remain unchanged or be XORed with the new number. This works because every old subsequence either skips the new element or takes it. However, after many operations the set can approach the full XOR space size, which is up to 2^60. Updating and storing that many values is impossible.

The reason the brute force grows so quickly is that many different subsequences are actually redundant. For XOR, every number is a vector of bits, and taking XOR is equivalent to adding vectors where addition is done modulo 2. A set of independent vectors is enough to describe every possible XOR result. This structure is called a linear basis.

We maintain one basis vector for each possible highest set bit. When inserting a number, we try to remove its highest bit using an existing basis vector. If the number becomes zero, it was already representable. If it still has a highest bit that no basis vector owns, we store it there. Since there are only 60 bits, every insertion is fast.

For answering the k-th smallest query, the basis represents a space with exactly 2^rank different values. The basis vectors can be treated as binary decisions. Starting from the highest bit, we decide whether the answer should have that bit set by checking how many values are possible with the bit equal to zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) per update | O(2^60) | Too slow |
| Optimal | O(60) per operation | O(60) | Accepted |

## Algorithm Walkthrough

1. Maintain an array `basis` of size 60. `basis[i]` stores the vector whose highest set bit is `i`, or zero if no such vector exists.

When a number is inserted, we reduce it from high bits to low bits. The highest bit is the most important part because two basis vectors cannot share the same highest bit.

1. For an insertion, scan bits from 59 down to 0. If the current bit of the number is zero, it does not affect the reduction. If there is already a basis vector at this bit, XOR it away. Otherwise, store the current number as the new basis vector.

This preserves the same set of reachable XOR values because replacing a number by its XOR with another reachable number does not change what can be formed.

1. Keep the current rank, which is the number of non-zero basis vectors. The number of distinct XOR values is `2^rank`.

If a query asks for a k larger than this amount, there is no answer.

1. To find the k-th smallest value, process the basis from the highest bit downward. The vectors with smaller highest bits cannot change decisions already made on larger bits.

For a basis vector at bit `i`, exactly half of all remaining combinations have bit `i` equal to zero and half have it equal to one. If `k` is inside the zero group, skip the vector. Otherwise, take the vector and subtract the size of the zero group from `k`.

1. Return the constructed value.

Why it works: the basis vectors are independent, so every reachable XOR value has exactly one representation as a subset of basis vectors. The highest differing bit between two representations decides which value is larger, which means the search from high bits to low bits matches the sorted order of all possible values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    basis = [0] * 60
    rank = 0
    ans = []

    def insert(x):
        nonlocal rank
        for b in range(59, -1, -1):
            if ((x >> b) & 1) == 0:
                continue
            if basis[b]:
                x ^= basis[b]
            else:
                basis[b] = x
                rank += 1
                return

    def kth_smallest(k):
        if k > (1 << rank):
            return -1

        res = 0
        remaining = rank

        for b in range(59, -1, -1):
            if basis[b]:
                remaining -= 1
                cnt_zero = 1 << remaining
                if k > cnt_zero:
                    k -= cnt_zero
                    res ^= basis[b]

        return res

    for _ in range(q):
        t, x = map(int, input().split())
        if t == 1:
            insert(x)
        else:
            ans.append(str(kth_smallest(x)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `insert` function is the Gaussian elimination step over binary vectors. The loop starts from bit 59 because the input values are smaller than 2^60, so bit positions above 59 never appear.

The query function first checks whether the requested position exists. The expression `1 << rank` works because every independent basis vector doubles the number of possible XOR values.

The variable `remaining` counts how many basis choices are still undecided after the current bit. This gives the size of the block where the current bit is zero. The subtraction from `k` happens only when we skip that entire block and choose the current bit as one.

No large arrays of XOR values are created, so the implementation stays within the memory limit.

## Worked Examples

Sample 1:

```
7
1 5
1 6
2 1
2 2
2 3
2 4
2 5
```

| Operation | Basis state | Rank | Query result |
| --- | --- | --- | --- |
| Insert 5 | 101 | 1 |  |
| Insert 6 | 101, 011 | 2 |  |
| Query 1 | values: 0,3,5,6 | 2 | 0 |
| Query 2 | values: 0,3,5,6 | 2 | 3 |
| Query 3 | values: 0,3,5,6 | 2 | 5 |
| Query 4 | values: 0,3,5,6 | 2 | 6 |
| Query 5 | values: 0,3,5,6 | 2 | -1 |

This shows that the basis rank, not the number of inserted elements, controls how many different answers exist.

Sample 2:

```
3
1 1000
1 1000
2 3
```

| Operation | Basis state | Rank | Query result |
| --- | --- | --- | --- |
| Insert 1000 | 1111101000 | 1 |  |
| Insert 1000 | unchanged | 1 |  |
| Query 3 | values: 0,1000 | 1 | -1 |

The second insertion adds no new dimension because the value is already represented.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(60q) | Each insertion and query scans at most 60 bits |
| Space | O(60) | Only one basis vector per bit is stored |

The maximum number of operations is 200000, so around twelve million bit operations are required. This is easily within limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    data = sys.stdin.readline
    q = int(data())
    basis = [0] * 60
    rank = 0
    out = []

    def insert(x):
        nonlocal rank
        for b in range(59, -1, -1):
            if (x >> b) & 1:
                if basis[b]:
                    x ^= basis[b]
                else:
                    basis[b] = x
                    rank += 1
                    return

    def kth(k):
        if k > (1 << rank):
            return -1
        res = 0
        rem = rank
        for b in range(59, -1, -1):
            if basis[b]:
                rem -= 1
                if k > (1 << rem):
                    k -= 1 << rem
                    res ^= basis[b]
        return res

    for _ in range(q):
        t, x = map(int, data().split())
        if t == 1:
            insert(x)
        else:
            out.append(str(kth(x)))

    sys.stdin = old
    return "\n".join(out)

assert run("""7
1 5
1 6
2 1
2 2
2 3
2 4
2 5
""") == "0\n3\n5\n6\n-1"

assert run("""3
1 1000
1 1000
2 3
""") == "-1"

assert run("""2
2 1
2 2
""") == "0\n-1"

assert run("""4
1 1
1 2
1 3
2 4
""") == "-1"

assert run("""5
1 7
1 2
1 5
2 1
2 8
""") == "0\n-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty sequence queries | 0, -1 | Empty subsequence handling |
| Repeated values | -1 | Dependent insertions |
| Three independent values | -1 for out of range | Correct rank counting |
| Mixed basis values | 0, -1 | Ordering and query boundaries |

## Edge Cases

For repeated values, such as:

```
3
1 5
1 5
2 3
```

The first insertion creates one basis vector. The second insertion reduces to zero because it is identical to the existing direction. The rank stays one, so only two values exist: 0 and 5. The third smallest value does not exist.

For values that combine into another value:

```
4
1 1
1 2
1 3
2 4
```

The third insertion does not increase the rank because `1 XOR 2 = 3`. The basis still has only two independent vectors, giving four possible XOR results. The algorithm correctly returns -1.

For the empty sequence:

```
2
2 1
2 2
```

The rank is zero, so the number of reachable values is `2^0 = 1`. The only value is zero, which comes from choosing nothing. The first query returns zero and the second cannot be answered.
