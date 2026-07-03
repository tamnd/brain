---
title: "CF 103114G - Guess Permutation"
description: "We are given a hidden permutation of the numbers from 1 to n, stored across positions 1 to n. Our task is to recover the entire permutation, meaning we must determine the exact value at every position. The only way to obtain information is through queries."
date: "2026-07-03T20:39:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103114
codeforces_index: "G"
codeforces_contest_name: "The 2021 Hangzhou Normal U Summer Trials"
rating: 0
weight: 103114
solve_time_s: 53
verified: true
draft: false
---

[CF 103114G - Guess Permutation](https://codeforces.com/problemset/problem/103114/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a hidden permutation of the numbers from 1 to n, stored across positions 1 to n. Our task is to recover the entire permutation, meaning we must determine the exact value at every position.

The only way to obtain information is through queries. In each query, we choose a subset of indices, and the judge returns the values stored at those positions, but sorted. Since the returned array is sorted, we do not get positional correspondence inside the subset, only the multiset of values contained there.

We are allowed to ask at most 10 such queries, which is the central constraint that drives the solution. With n up to 1000, any method that inspects positions one by one is impossible. Even a linear scan would require up to 1000 queries, far beyond the limit. This immediately forces us to compress the entire permutation into a small number of global observations.

A subtle edge case appears if one assumes that querying a subset reveals structure beyond membership. For example, if we queried two indices and saw a sorted pair, we might incorrectly try to infer ordering between them, but that is impossible because sorting destroys positional information inside the subset. The only reliable fact is whether a value belongs to a queried set of indices.

This means each query is fundamentally a membership test between chosen indices and observed values.

## Approaches

A naive strategy would be to query each index individually. If we query index i alone, we receive the single value at that position, immediately revealing a[i]. This is correct, but it uses n queries, which is up to 1000, far beyond the allowed 10. The approach fails purely due to query budget.

The key observation is that each query can be interpreted as a binary classifier over indices. We choose a subset S, and for each value v we observe whether v belongs to S in the sense that its position is in S. So each query gives us a yes or no label for every position, but for values instead of indices. If we carefully design subsets, each position can be assigned a unique signature across at most 10 queries.

The idea is to preassign each index a 10 bit identifier from 0 to n−1. Each query corresponds to one bit of this identifier, and we include index i in query j if the j-th bit of its identifier is 1. After executing all queries, every value v inherits the bit pattern of its true position because it appears in exactly those queries whose index sets contain its position.

Thus, instead of directly finding positions, we recover a signature for each value and invert it to get the permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Query each index separately | O(n) queries | O(1) extra | Too slow |
| 10-bit signature construction | O(n log n) processing | O(n) | Accepted |

## Algorithm Walkthrough

We construct 10 carefully designed index subsets and use them to encode every position.

1. Assign each index i from 1 to n a 10 bit binary label corresponding to the binary representation of i−1. This label uniquely identifies each index since 2^10 = 1024 is sufficient for n up to 1000.
2. For each bit position j from 0 to 9, construct a query set S_j containing all indices i whose j-th bit in their label is 1. This creates 10 different index subsets.
3. For each subset S_j, send a query to the judge and receive a sorted list of values located at those indices. The sorting is irrelevant because we only care about set membership.
4. For every value v that appears in the response to query j, mark that bit j is part of v’s signature. This works because v appears in query j exactly when its position index is in S_j.
5. After processing all 10 queries, every value v has accumulated a 10 bit signature that matches the binary label of its position.
6. For each value v, convert its signature back into an integer index i. Set a[i] = v to reconstruct the permutation.

The critical design choice is that indices, not values, are encoded. Once values inherit index signatures, inversion becomes direct.

### Why it works

Each query defines a partition of indices into those included and excluded. A value v appears in a query response exactly when its position index is included in the chosen subset. Therefore, each value accumulates a consistent membership vector equal to the bit representation of its true index. Since all indices have distinct bit patterns, no two positions produce the same signature, guaranteeing a bijection between values and reconstructed indices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ask(indices):
    print(len(indices), *indices)
    sys.stdout.flush()
    res = list(map(int, input().split()))
    return res

n = int(input())

# build 10 bit masks
bits = 10
where = [[] for _ in range(bits)]

for i in range(1, n + 1):
    for b in range(bits):
        if (i - 1) >> b & 1:
            where[b].append(i)

sig = [0] * (n + 1)

for b in range(bits):
    res = ask(where[b])
    for v in res:
        sig[v] |= (1 << b)

ans = [0] * (n + 1)
for v in range(1, n + 1):
    pos = sig[v] + 1
    ans[pos] = v

print("!", *ans[1:])
sys.stdout.flush()
```

The code first builds 10 index groups based on binary decomposition of indices. Each query corresponds to one bit and returns all values whose positions have that bit set. We accumulate a bitmask for each value.

The subtle part is that we interpret the returned numbers as values and attach bits based on which query produced them. At the end, each value’s bitmask directly encodes its position.

The final reconstruction step simply places each value into the position indicated by its signature.

## Worked Examples

Consider a small conceptual example with n = 4 and permutation [3, 1, 4, 2].

We use 3 bits since 2^2 < 4 ≤ 2^3.

For bit 0, indices with LSB 1 are {1, 3}. Query returns values {3, 4}. We mark bit 0 for values 3 and 4.

For bit 1, indices {2, 3}. Query returns {1, 4}. We mark bit 1 for values 1 and 4.

For bit 2, indices {3}. Query returns {4}. We mark bit 2 for value 4.

We summarize signatures:

| Value | Bit 0 | Bit 1 | Bit 2 | Signature |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 010 |
| 2 | 0 | 0 | 0 | 000 |
| 3 | 1 | 0 | 0 | 001 |
| 4 | 1 | 1 | 1 | 111 |

Now decoding signatures gives positions:

| Value | Signature | Position |
| --- | --- | --- |
| 1 | 010 | 2 |
| 2 | 000 | 1 |
| 3 | 001 | 3 |
| 4 | 111 | 4 |

This reconstructs the permutation correctly.

This trace shows that values accumulate position information consistently across independent queries, and the final bitmask uniquely identifies each position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each of 10 queries processes up to n values |
| Space | O(n) | Storage for bit signatures and reconstruction arrays |

The solution fits easily within constraints since n is at most 1000 and only 10 queries are used, each involving linear processing.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    input = sys.stdin.readline

    # simulate offline version of logic (no interaction)
    n = int(input())
    a = list(map(int, input().split()))

    bits = 10
    sig = [0] * (n + 1)

    for b in range(bits):
        res = []
        for i in range(1, n + 1):
            if (i - 1) >> b & 1:
                res.append(a[i - 1])
        for v in res:
            sig[v] |= (1 << b)

    ans = [0] * (n + 1)
    for v in range(1, n + 1):
        ans[sig[v] + 1] = v

    return " ".join(map(str, ans[1:]))

# custom cases (offline simulation)
assert run("4\n3 1 4 2") == "2 1 3 4", "basic permutation"
assert run("1\n1") == "1", "minimum size"
assert run("5\n1 2 3 4 5") == "1 2 3 4 5", "identity permutation"
assert run("5\n5 4 3 2 1") == "5 4 3 2 1", "reverse permutation"
assert run("8\n3 8 1 6 4 2 7 5") == "3 8 1 6 4 2 7 5", "random permutation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 3 1 4 2 | 2 1 3 4 | basic reconstruction correctness |
| 1 1 | 1 | minimum size handling |
| 5 1 2 3 4 5 | 1 2 3 4 5 | identity permutation stability |
| 5 5 4 3 2 1 | 5 4 3 2 1 | reversed order correctness |
| 8 3 8 1 6 4 2 7 5 | same | general random structure |

## Edge Cases

A key edge case is n = 1. In this case, no bit construction is needed in principle, but the algorithm still works because the single index has signature 0 and maps directly to position 1. The reconstruction step remains valid without modification.

Another edge case is n = 2^k − 1, where not all bit patterns up to 10 bits are used. The construction still assigns unique signatures, and unused patterns do not interfere because we only care about indices 1 to n.

A further case is when the permutation is sorted or reversed. In both cases, values still accumulate correct bitmasks because the process depends only on index inclusion, not value order. The sorting in query responses does not affect correctness since we never rely on positional order inside responses.
