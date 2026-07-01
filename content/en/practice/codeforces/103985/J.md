---
title: "CF 103985J - \u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f \u0438 \u043f\u043e\u0431\u0438\u0442\u043e\u0432\u043e\u0435 \u0418"
description: "We are given a list of non-negative integers, each representing a value assigned to a person in a group. The task is to compute a global measure of “group cohesion”, defined as the sum over all unordered pairs of people of the bitwise AND of their values."
date: "2026-07-02T06:15:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103985
codeforces_index: "J"
codeforces_contest_name: "\u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 (\u041c\u041a\u041e\u0428\u041f) 2017, \u041b\u0438\u0433\u0430 \u0410"
rating: 0
weight: 103985
solve_time_s: 39
verified: true
draft: false
---

[CF 103985J - \u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f \u0438 \u043f\u043e\u0431\u0438\u0442\u043e\u0432\u043e\u0435 \u0418](https://codeforces.com/problemset/problem/103985/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of non-negative integers, each representing a value assigned to a person in a group. The task is to compute a global measure of “group cohesion”, defined as the sum over all unordered pairs of people of the bitwise AND of their values.

Concretely, for every pair of distinct indices $i < j$, we take $a_i \& a_j$, and we sum these values over all pairs. The output is a single integer.

The constraint on $n$ reaches up to 150,000, and each value can be as large as $10^8$. A direct pairwise computation would require about $n^2 / 2$ operations, which at this scale is on the order of $10^{10}$, far beyond any reasonable time limit. This immediately rules out any quadratic solution.

The values are bounded by $10^8$, which fits within 27 bits. That means any bitwise decomposition approach can safely iterate over at most 30 bit positions, making a bit-by-bit counting strategy plausible.

A subtle failure mode for naive approaches is integer overflow or recomputing the same contribution multiple times incorrectly. Another common mistake is attempting to optimize by sorting, which does not preserve pairwise bitwise relationships.

For example, if all numbers are identical, say $[7,7,7]$, every pair contributes $7$, so the answer is $3 \cdot 7 = 21$. Any incorrect approach that tries to “compress duplicates” without accounting for pair counts can easily miscount multiplicities.

## Approaches

The brute-force solution iterates over all pairs $(i, j)$ and computes $a_i \& a_j$. This is straightforward and correct because it directly follows the definition of the problem. However, its cost grows quadratically with $n$, and with 150,000 elements, this leads to more than ten billion operations, which is not feasible.

The key observation is that the bitwise AND operation is independent across bits. A bit contributes to the final sum only if it is set in both numbers of a pair. This suggests reversing the viewpoint: instead of iterating over pairs, we count contributions bit by bit.

Fix a bit position $b$. We count how many numbers have this bit set, say $c_b$. Any pair of such numbers contributes $2^b$ to the final sum, and the number of such pairs is $\binom{c_b}{2}$. Summing over all bits gives the answer.

This transforms the problem from pair enumeration into frequency counting over bits, reducing complexity dramatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Bit counting | $O(n \log A)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process the array while maintaining counts of how many numbers contain each bit.

1. Initialize an array `cnt` of size 31 (enough for values up to $10^8$). Each position stores how many numbers seen so far have that bit set. This structure lets us track bit frequencies incrementally.
2. Iterate over each number $x$ in the input. For each bit position $b$ from 0 to 30, check whether bit $b$ is set in $x$. If it is, increment `cnt[b]`. This ensures that after processing all numbers, `cnt[b]` equals the total number of elements contributing that bit.
3. After counting, compute the answer by iterating over all bit positions. For each bit $b$, if `cnt[b] >= 2`, then there are $\binom{cnt[b]}{2}$ pairs contributing this bit.
4. Add $\binom{cnt[b]}{2} \cdot 2^b$ to the final answer. This reconstructs the total contribution of all pairs sharing that bit.
5. Output the accumulated sum.

The critical step is separating contributions by bit, which avoids double counting and ensures each pair is considered exactly once per bit.

### Why it works

Each pair $(i, j)$ contributes independently for each bit where both numbers have a 1. For a fixed bit, the contribution depends only on how many numbers contain that bit, not on their identities. Therefore, counting pairs of indices within each bit group exactly reconstructs the total sum without enumerating pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    cnt = [0] * 31
    
    for x in a:
        b = 0
        while x:
            if x & 1:
                cnt[b] += 1
            x >>= 1
            b += 1
    
    ans = 0
    for b in range(31):
        c = cnt[b]
        if c >= 2:
            ans += (c * (c - 1) // 2) * (1 << b)
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation uses a direct bit scan per number rather than checking all 31 bits with a fixed loop. This keeps operations tight and avoids unnecessary bit checks for zero tails.

The main subtlety is ensuring each bit position is aligned correctly with its index in `cnt`. The variable `b` tracks the bit index as we shift the number.

## Worked Examples

### Example 1

Input:

```
4
3 5 2 3
```

We track bit counts:

| Number | Binary | Bits added |
| --- | --- | --- |
| 3 | 011 | 0, 1 |
| 5 | 101 | 0, 2 |
| 2 | 010 | 1 |
| 3 | 011 | 0, 1 |

Final counts:

- bit 0: 3 numbers
- bit 1: 3 numbers
- bit 2: 1 number

Now contributions:

- bit 0: C(3,2) * 1 = 3
- bit 1: C(3,2) * 2 = 6
- bit 2: 0

Total = 9

This trace confirms that each bit is handled independently and pair contributions accumulate correctly.

### Example 2

Input:

```
3
4 4 4
```

| Number | Binary | Bits added |
| --- | --- | --- |
| 4 | 100 | 2 |
| 4 | 100 | 2 |
| 4 | 100 | 2 |

Counts:

- bit 2: 3

Contribution:

- C(3,2) * 4 = 3 * 4 = 12

All pairs are identical, and every pair contributes 4, so 3 pairs yield 12.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot B)$ | Each number is processed over up to 31 bits |
| Space | $O(B)$ | Only a fixed array for bit counts |

The value of $B = 31$ is constant relative to constraints, so the solution is effectively linear in $n$. This easily fits within 4 seconds for 150,000 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import comb
    
    n_and_rest = inp.strip().split()
    n = int(n_and_rest[0])
    a = list(map(int, n_and_rest[1:]))

    cnt = [0] * 31
    for x in a:
        b = 0
        while x:
            if x & 1:
                cnt[b] += 1
            x >>= 1
            b += 1

    ans = 0
    for b in range(31):
        c = cnt[b]
        if c >= 2:
            ans += (c * (c - 1) // 2) * (1 << b)

    return str(ans)

# sample
assert run("4\n3 5 2 3") == "9"

# all equal
assert run("3\n7 7 7") == str(3 * 7)

# single element
assert run("1\n5") == "0"

# no shared bits
assert run("3\n1 2 4") == "0"

# max-ish simple
assert run("5\n1 1 1 1 1") == str(10)

print("OK")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 3 5 2 3 | 9 | sample correctness |
| 3 7 7 7 | 21 | duplicate handling |
| 1 5 | 0 | single element edge case |
| 3 1 2 4 | 0 | disjoint bits |
| 5 1 1 1 1 1 | 10 | combinatorial counting |

## Edge Cases

For a single element input like `1\n5`, the algorithm sets bit counts for the number but never reaches a count of at least two. Every `cnt[b]` is at most 1, so all binomial contributions vanish, producing 0, which matches the fact that no pairs exist.

For identical elements such as `3\n7 7 7`, all bits of 7 are counted three times. Each bit contributes $\binom{3}{2} \cdot 2^b$. Summing over bits reconstructs exactly three copies of 7 across the three pairs, matching the pairwise definition directly.

For numbers with disjoint bit sets like `1 2 4`, every bit appears in exactly one number, so all `cnt[b] ≤ 1`, meaning no pair shares any bit. The algorithm correctly returns 0, aligning with the fact that every AND is zero across all pairs.
