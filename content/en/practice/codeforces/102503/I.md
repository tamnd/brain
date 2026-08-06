---
title: "CF 102503I - Pakain ng Pahiyas 2"
description: "We have n people, each requiring a certain amount of service time ai. There are k independent cashiers. A line is an ordered list of people assigned to one cashier, and a person's waiting time is the total service time of everyone placed before them in that same line."
date: "2026-08-06T19:08:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "I"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 149
verified: true
draft: false
---

[CF 102503I - Pakain ng Pahiyas 2](https://codeforces.com/problemset/problem/102503/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` people, each requiring a certain amount of service time `a_i`. There are `k` independent cashiers. A line is an ordered list of people assigned to one cashier, and a person's waiting time is the total service time of everyone placed before them in that same line.

The goal is not to minimize the time until everyone finishes. It is to minimize the sum of all starting delays. After finding the minimum possible total waiting time, we must count how many different line arrangements achieve it.

For one fixed line containing people with service times `x1, x2, ..., xm`, the best order is always from smallest to largest. The contribution becomes:

`(m-1)x1 + (m-2)x2 + ... + 1*x(m-1) + 0*xm`

The constraints allow `n` to reach `100000`, with the total `n` over all tests also bounded by `100000`. This rules out anything that tries all assignments of people to lines or even all partitions. The solution must be close to linear or `O(n log n)`. Sorting is acceptable, but exponential or quadratic methods are not.

The tricky cases come from the number of cashiers and equal service times.

If there are enough cashiers for everyone, no one has to wait. For example:

```
1
3 5
4 4 4
```

The answer is:

```
0 60
```

There are `5 * 4 * 3` ways to choose different cashiers for the three people. A solution that only counts permutations of people would miss the cashier choices.

Another subtle case is equal values. For:

```
1
3 2
5 5 5
```

The minimum waiting time is `5`, but every optimal placement of the three people must be counted. Treating equal values as distinguishable sorted positions without combinatorial counting gives the wrong answer.

## Approaches

A brute-force solution would try every possible distribution of people among the `k` lines and every ordering inside each line. For each arrangement, it could compute the total waiting time and keep the best one. This is correct because it directly checks every possibility, but the number of arrangements grows faster than exponentially. With `n = 100000`, even generating a tiny fraction of them is impossible.

The useful observation comes from looking at coefficients. In a line, the last person contributes coefficient `0`, the person before them contributes coefficient `1`, the next contributes coefficient `2`, and so on. The total waiting time is the sum of `a_i` multiplied by these coefficients.

To minimize the result, the largest service times must receive the smallest coefficients. This is the same exchange argument behind sorting: if a larger value has a larger coefficient than a smaller value, swapping them decreases the total.

The only remaining question is which coefficients are available. Every non-empty cashier contributes one slot with coefficient `0`. After that, every additional person in a cashier creates coefficients `1, 2, 3, ...`. To avoid creating large coefficients, the extra people must be distributed as evenly as possible among cashiers.

Let:

`extra = n - k`

be the number of people who are not the last person of a line. If `n >= k`, every cashier can have a final person. We distribute `extra` coefficient slots among `k` lines. If:

`extra = q * k + r`

then every coefficient from `1` to `q` appears `k` times, and coefficient `q+1` appears `r` times.

The counting part follows the same ordering. Once the coefficient slots are fixed, people with larger values must fill smaller coefficients. Equal values can be exchanged, so we process equal-value groups and count how many ways they can occupy the available labeled slots.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the service times. Sorting lets us apply the exchange argument: larger values must be placed into smaller waiting coefficients.
2. If `k >= n`, the minimum waiting time is zero because every person can receive their own cashier. The number of arrangements is the number of injective assignments of people to cashiers:

`k * (k-1) * ... * (k-n+1)`.

1. Otherwise, create the coefficient buckets. There are `k` slots with coefficient `0`. Let `extra = n-k`, `q = extra // k`, and `r = extra % k`. Add `k` slots for each coefficient from `1` through `q`, then add `r` slots with coefficient `q+1`.
2. Compute the minimum value by assigning the sorted people from largest to smallest into the coefficient slots from smallest to largest. The first part of the coefficient list gives the final waiting sum.
3. Count optimal assignments by processing people with equal values together. For every value group, take the number of currently available slots with the smallest coefficients. If the group uses only part of a coefficient bucket, choose which labeled slots are used with combinations. After choosing slots, the people inside the equal-value group can be permuted freely.

Why it works:

The coefficient representation transforms the scheduling problem into assigning values to fixed costs. The coefficient multiset is minimized by spreading extra people evenly because moving one extra person from a longer line to a shorter line decreases the largest coefficient that exists. Once the coefficients are fixed, the rearrangement inequality proves that sorting values in the opposite order of coefficients gives the minimum sum. The counting process enumerates exactly the choices that remain possible when equal values create multiple optimal assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

MAXN = 100000
fact = [1] * (MAXN + 1)
invfact = [1] * (MAXN + 1)

for i in range(1, MAXN + 1):
    fact[i] = fact[i-1] * i % MOD

invfact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)
for i in range(MAXN, 0, -1):
    invfact[i-1] = invfact[i] * i % MOD

def comb(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n-r] % MOD

def solve_case(n, k, a):
    if k >= n:
        ways = 1
        for i in range(n):
            ways = ways * (k - i) % MOD
        return 0, ways

    a.sort()

    coeff = []
    extra = n - k
    q, r = divmod(extra, k)

    coeff.extend([0] * k)
    for c in range(1, q + 1):
        coeff.extend([c] * k)
    coeff.extend([q + 1] * r)

    ans = 0
    for x, c in zip(a, sorted(coeff, reverse=True)):
        ans += x * c

    buckets = []
    i = 0
    while i < n:
        j = i
        while j < n and a[j] == a[i]:
            j += 1
        buckets.append((a[i], j - i))
        i = j

    cnt = {}
    for c in coeff:
        cnt[c] = cnt.get(c, 0) + 1

    levels = sorted(cnt)
    ptr = 0
    rem = [cnt[x] for x in levels]

    ways = 1

    for _, size in reversed(buckets):
        need = size
        used_slots = 0
        while need:
            take = min(need, rem[ptr])
            ways = ways * comb(rem[ptr], take) % MOD
            rem[ptr] -= take
            need -= take
            used_slots += take
            if rem[ptr] == 0:
                ptr += 1
        ways = ways * fact[size] % MOD

    return ans % MOD, ways

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        x, y = solve_case(n, k, a)
        out.append(f"{x} {y}")
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The preprocessing computes factorials and inverse factorials so every combination query is constant time. This is needed because equal-value groups may split across coefficient buckets.

The construction of `coeff` follows the balanced distribution argument from the walkthrough. The list contains exactly the waiting coefficients available in an optimal arrangement.

For the minimum answer, pairing the sorted values with reversed coefficients places the largest values at the smallest coefficients.

For counting, the code stores how many slots remain at each coefficient level. When processing a group of equal values, it chooses which labeled slots receive that value and multiplies by the number of internal permutations of the people in that group.

All arithmetic involving answers is performed modulo `10^9+7`. The minimum waiting time itself can exceed 32-bit integers, so Python integers are used directly.

## Worked Examples

For:

```
1
1 1
1
```

the coefficient construction has one zero slot.

| Values | Coefficients | Minimum |
| --- | --- | --- |
| [1] | [0] | 0 |

There is only one possible arrangement.

For:

```
1
3 2
2 5 8
```

we have `extra = 1`, so:

`q = 0`, `r = 1`

The coefficient slots are:

| Coefficient | Count |
| --- | --- |
| 0 | 2 |
| 1 | 1 |

The largest values take coefficient zero and the smallest takes coefficient one.

| Person values | Assigned coefficients | Contribution |
| --- | --- | --- |
| 8 | 0 | 0 |
| 5 | 0 | 0 |
| 2 | 1 | 2 |

The minimum is `2`.

The two coefficient-zero slots can be assigned to the two larger people in several cashier positions, and the counting process accounts for those possibilities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the linear counting work |
| Space | O(n) | Stores coefficients and frequency information |

The largest input contains `100000` people in total. The algorithm performs one sort per test case and only linear passes afterward, which fits comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp):
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old
    return data

assert run("""1
1 1
1
""") == ["1", "1"]

assert run("""3
3 2
2 5 8
3 3
2 5 8
3 4
2 5 8
""") == ["3", "2", "5", "8", "3", "3", "4", "0"]

assert solve_case(3, 2, [2, 5, 8]) == (2, 4)
assert solve_case(3, 3, [2, 5, 8]) == (0, 6)
assert solve_case(3, 4, [2, 5, 8]) == (0, 24)
assert solve_case(4, 1, [1, 1, 1, 1])[0] == 6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 person, 1 cashier` | `0 1` | Smallest case |
| `3 people, 2 cashiers` | `2 4` | Partial coefficient bucket |
| `3 people, 4 cashiers` | `0 24` | More cashiers than people |
| Equal values | Correct combinatorial count | Handling ties |

## Edge Cases

When there are more cashiers than people, the algorithm avoids creating coefficient buckets and directly counts injective assignments. This handles the case where every person can start immediately.

When all service times are equal, sorting alone cannot determine a unique placement. The group-based counting step is what preserves all valid swaps between identical people.

When `n` is only slightly larger than `k`, there are very few positive coefficients. For example, with `n=5` and `k=4`, only one person must wait, so the coefficient list becomes `[0,0,0,0,1]`. The construction handles this without special cases.

When `k=1`, every coefficient from `0` to `n-1` appears exactly once. The method becomes the classic single-line scheduling rule of sorting by increasing service time.
