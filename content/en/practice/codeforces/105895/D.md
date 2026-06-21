---
title: "CF 105895D - Kings Game (Hard Version)"
description: "We are given an array of positive integers. Each query focuses on a contiguous segment of this array, and for that segment we are allowed to pick any subsequence (not necessarily contiguous, but preserving order) to form a “game array”."
date: "2026-06-21T15:12:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105895
codeforces_index: "D"
codeforces_contest_name: "The 21st Southeast University Programming Contest (Summer)"
rating: 0
weight: 105895
solve_time_s: 70
verified: true
draft: false
---

[CF 105895D - Kings Game (Hard Version)](https://codeforces.com/problemset/problem/105895/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. Each query focuses on a contiguous segment of this array, and for that segment we are allowed to pick any subsequence (not necessarily contiguous, but preserving order) to form a “game array”.

That chosen subsequence is used in a two-player game. Players alternate moves starting from A. In one move, a player picks any element that is strictly greater than 1 and replaces it with one of its non-trivial divisors greater than 1. Eventually elements can be reduced until everything becomes 1, at which point no move is possible and the player who is about to move loses.

The question is not to simulate the game directly. For each segment, we must count how many non-empty subsequences make player A win under optimal play, and output this count modulo 998244353.

The constraints are large, with total array length and total queries up to 10^6 across test cases. That immediately rules out anything that builds or evaluates subsequences per query. Even O(n log n) per query would be too slow; we need O(1) or O(log n) per query after preprocessing.

A subtle issue is that subsequences are defined by index choices, so two subsequences are different if they pick different positions, even if values coincide. Also, empty subsequences are disallowed.

A key edge case appears when all selected elements are equal to 1. In that situation, no move is ever possible in the game, so the first player immediately loses. A naive counting approach that ignores this case would incorrectly include invalid winning configurations.

## Approaches

A brute-force solution would, for each query, enumerate all subsequences of the segment and simulate the game outcome. Even ignoring game simulation, a segment of length m has 2^m subsequences, and m can be large, so this is impossible.

The first simplification comes from understanding the game itself. Each move operates on a single element greater than 1, and reduces it by choosing a divisor. Regardless of how the divisor is chosen, the only important fact is that the element strictly decreases and eventually becomes 1. Each element can be “used” only until it becomes 1, after which it is irrelevant.

This means every element greater than 1 effectively contributes at least one move opportunity, while elements equal to 1 contribute nothing. More importantly, since a player can always reduce a chosen element directly to 1 in one move, the internal structure of factorization does not affect optimal play: each useful element behaves like a single token that can be consumed exactly once.

So the game reduces to a simple turn-based process: players alternately consume elements that are greater than 1. The winner depends only on how many such elements exist in the chosen subsequence.

If we define the subsequence, let k be the number of elements greater than 1 inside it. The game consists of exactly k moves, so A wins if and only if k is odd.

Now the problem becomes purely combinatorial. For a given segment, we count subsequences such that the number of chosen “good” elements (values greater than 1) is odd.

Let there be c elements greater than 1 and z elements equal to 1 in the segment. Every subsequence is formed by independently choosing each element or not. The z elements contribute only multiplicative freedom, while the c elements determine parity.

Among c elements, the number of subsets with odd size is exactly 2^(c-1) when c > 0, and 0 when c = 0. Each choice of the z elements doubles the number of valid subsequences, contributing a factor 2^z.

So for c > 0, the answer becomes 2^z * 2^(c-1) = 2^(segment length - 1). If c = 0, all elements are 1, and no valid winning subsequence exists.

Thus each query reduces to checking whether the segment contains at least one value greater than 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (subsequences + simulation) | O(2^n · n) per query | O(n) | Too slow |
| Prefix count of values > 1 | O(1) per query after O(n) preprocessing | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Classify each element

We scan the array once and classify every element as either “active” if it is greater than 1 or “inactive” if it equals 1. Only active elements influence the game parity.

This classification is sufficient because the internal divisor operation never affects the fact that an element remains playable until it becomes 1.

### 2. Build prefix information

We compute a prefix sum array where each position stores how many active elements appear up to that index. This allows us to query, for any segment, how many active elements it contains in constant time.

The reason this works is that subsequences are chosen independently of values, so we only need counts, not positions.

### 3. Answer each query using the segment classification

For a query [l, r], we compute the number of active elements c in that range using prefix differences. If c is zero, the answer is immediately zero because the game has no moves at all.

Otherwise, the segment length is len = r - l + 1. Every non-empty subsequence is equally weighted in terms of structure, and exactly half of the subsets over active elements have odd size. The inactive elements only multiply the count by 2^(number of inactive elements), so the final answer depends only on len.

We output 2^(len - 1) modulo 998244353.

### Why it works

The invariant is that only the parity of the number of elements greater than 1 in the chosen subsequence determines the winner. The divisor operation never changes this parity-relevant structure because each active element contributes exactly one unavoidable “consumable unit” under optimal play. Since subsequences treat elements independently, the counting reduces to a parity-constrained subset count, and inactive elements do not affect parity but only scale the number of configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modexp(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    b = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + (1 if b[i] > 1 else 0)

    for _ in range(q):
        l, r = map(int, input().split())
        c = pref[r] - pref[l - 1]
        if c == 0:
            print(0)
        else:
            length = r - l + 1
            print(modexp(2, length - 1))
```

The prefix array `pref` tracks how many elements in the array segment are strictly greater than 1. Each query subtracts two prefix values to get the count in O(1).

The exponentiation step computes powers of two modulo 998244353 efficiently using binary exponentiation. Since the exponent is at most 10^6, this is fast enough across all queries.

A subtle point is that we never explicitly compute z, the number of ones, because it cancels out in the final expression. This is what makes the solution scale to large inputs.

## Worked Examples

### Example 1

Consider the array:

`[1, 1, 4, 16, 2, 8, 3, 7]`

Take the full segment [1, 8].

We compute how many elements are greater than 1:

| i | value | >1? | prefix |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 4 | 1 | 1 |
| 4 | 16 | 1 | 2 |
| 5 | 2 | 1 | 3 |
| 6 | 8 | 1 | 4 |
| 7 | 3 | 1 | 5 |
| 8 | 7 | 1 | 6 |

So c = 6, length = 8. Since c > 0, answer is 2^(8 - 1) = 2^7 = 128.

This shows that even though the distribution of large numbers looks complex, only the length matters once at least one active element exists.

### Example 2

Take a segment consisting only of ones, say `[1, 1, 1, 1]`.

Here c = 0. No element can ever be used in the game, so A immediately loses for every subsequence. The answer is 0.

A naive subset counting approach that ignores the “no moves” condition would incorrectly output 2^4 - 1 = 15, but those subsequences do not satisfy the game condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test case | Prefix computation is linear, each query is O(1) plus modular exponentiation in constant time |
| Space | O(n) | Prefix array storage |

The total constraints over all test cases reach 10^6, so linear preprocessing and constant-time queries are essential. The solution stays comfortably within limits.

## Test Cases

```python
import sys, io

MOD = 998244353

def modexp(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, q = map(int, input().split())
        b = list(map(int, input().split()))

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + (1 if b[i] > 1 else 0)

        for _ in range(q):
            l, r = map(int, input().split())
            c = pref[r] - pref[l - 1]
            if c == 0:
                out.append("0")
            else:
                out.append(str(modexp(2, r - l)))
    return "\n".join(out)

# custom tests

assert solve("""1
1 1
1
1 1
""") == "0"

assert solve("""1
3 1
2 3 4
1 3
""") == str(modexp(2, 2))

assert solve("""1
4 1
1 1 1 1
1 4
""") == "0"

assert solve("""1
5 2
1 2 1 3 1
1 5
2 4
""") == "\n".join([str(modexp(2,4)), str(modexp(2,2))])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1 | 0 | all elements are dead |
| all active | 2^(n-1) | full active segment behavior |
| all ones | 0 | empty game validity |
| mixed queries | powers of two | consistency across ranges |

## Edge Cases

When a segment contains only ones, the algorithm correctly returns zero because the prefix difference c becomes zero, triggering the special case. This avoids incorrectly counting subsequences that have no actual game moves.

When a segment contains exactly one element greater than 1, every valid subsequence that includes it contributes a win condition based purely on inclusion parity, and the formula 2^(len-1) still holds. The prefix check ensures we do not mistakenly treat all-ones segments as valid.

When the segment is large but sparse in active elements, the algorithm still behaves correctly because it never depends on positions of active elements, only their existence.
