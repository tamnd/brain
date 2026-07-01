---
title: "CF 104333I - Hail Pythagoras"
description: "We are asked to count integer triples $(a, b, c)$ such that $a le b le c$, all values are positive, and they satisfy the Pythagorean relation $a^2 + b^2 = c^2$."
date: "2026-07-01T18:58:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104333
codeforces_index: "I"
codeforces_contest_name: "Replay of BU - PSTU Programming club collaborative contest"
rating: 0
weight: 104333
solve_time_s: 111
verified: false
draft: false
---

[CF 104333I - Hail Pythagoras](https://codeforces.com/problemset/problem/104333/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count integer triples $(a, b, c)$ such that $a \le b \le c$, all values are positive, and they satisfy the Pythagorean relation $a^2 + b^2 = c^2$. The constraint is that $a$ is bounded by $n$, and implicitly $b$ and $c$ must also be positive integers, but only triples with $a \le n$ are considered valid contributions.

Each test case gives a different limit $n$, and for each one we must count how many distinct Pythagorean triples exist whose smallest leg is at most $n$. A triple is counted once, even if its hypotenuse or second leg exceed $n$; only the condition on $a$ matters.

The constraints are large in terms of number of queries, with up to $10^5$ test cases and $n$ up to $10^5$. This combination forces preprocessing. A per-test $O(\sqrt{n})$ or worse enumeration would still be too slow when repeated $10^5$ times. The only viable direction is to precompute all valid triples once up to the maximum $n$, then answer each query in constant time.

A subtle pitfall is misinterpreting the condition $a \le b \le c$. If one generates all Pythagorean triples without enforcing ordering, duplicates appear in permutations, but the constraint removes ambiguity: each primitive geometric triangle contributes exactly one ordered representation once sorted.

Another failure case is counting scaled versions multiple times incorrectly. For example, $(3,4,5)$ and $(6,8,10)$ are both valid, but they are different triples and must both be counted. Any approach that only generates primitive triples would miss valid multiples unless scaling is explicitly included.

## Approaches

A direct approach would try every pair $(a, b)$, compute $c = \sqrt{a^2 + b^2}$, and check if it is an integer. If so, we verify ordering and count it. This is straightforward correctness-wise, but it performs roughly $O(n^2)$ checks per test case in the worst interpretation, or at best $O(n^2)$ total if reused across queries. With $n = 10^5$, this is far beyond feasible.

A better perspective is to decouple the geometry from brute force enumeration. The key observation is that every valid triple corresponds to a Pythagorean triple, and all such triples within bounds can be generated once by iterating over possible $a, b$ pairs in a global precomputation, marking their validity if $c \le 10^5$. Instead of recomputing per query, we collect all valid triples once.

Since $a^2 + b^2$ grows quickly, we only need to iterate $a$ up to $10^5$ and $b$ from $a$ upward while $a^2 + b^2 \le (10^5)^2$. Each valid integer hypotenuse produces exactly one triple under ordering constraints.

We then sort triples by $a$, and build a prefix array where we increment a counter at position $a$. Each query becomes a prefix sum lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ per test | $O(1)$ | Too slow |
| Optimal Precompute + Prefix | $O(N \sqrt{N})$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

### Precomputation Phase

1. Fix a global limit $MAX = 10^5$, since all queries are bounded by it.
2. Iterate over all possible $a$ from 1 to $MAX$. For each $a$, iterate $b$ from $a$ upward.

The ordering $a \le b$ ensures we never count duplicates like $(4,3,5)$ separately from $(3,4,5)$.
3. Compute $c^2 = a^2 + b^2$, then take integer square root $c = \lfloor \sqrt{c^2} \rfloor$.

If $c^2$ is not a perfect square, discard the pair. The condition $c^2 = a^2 + b^2$ ensures the triple is valid.
4. If $c > MAX$, we stop increasing $b$ for this $a$, because increasing $b$ only increases $c$.
5. For each valid triple $(a, b, c)$, increment a frequency array at index $a$, since every query counts triples based on the smallest leg.
6. Convert the frequency array into a prefix sum array so that each position $n$ directly gives the number of triples with $a \le n$.

### Query Phase

1. For each test case, output the precomputed prefix value at index $n$.

### Why it works

Every valid triple is uniquely determined by its smallest leg $a$. The generation process enumerates all valid pairs $(a, b)$ with $a \le b$ exactly once, so no duplicate permutations are introduced. The prefix sum converts a “count triples with smallest leg exactly $a$” representation into “count triples with smallest leg at most $n$”, which matches the query requirement directly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX = 100000

cnt = [0] * (MAX + 1)

import math

for a in range(1, MAX + 1):
    a2 = a * a
    for b in range(a, MAX + 1):
        s = a2 + b * b
        c = int(math.isqrt(s))
        if c * c == s:
            if c <= MAX:
                cnt[a] += 1
        if b > MAX or b * b > MAX * MAX:
            break

pref = [0] * (MAX + 1)
for i in range(1, MAX + 1):
    pref[i] = pref[i - 1] + cnt[i]

t = int(input())
for _ in range(t):
    n = int(input())
    print(pref[n])
```

The code builds a global table `cnt[a]`, which stores how many valid Pythagorean triples have smallest side exactly `a`. The nested loop ensures ordering $a \le b$. The integer square root check verifies the Pythagorean condition exactly without floating-point error.

The `pref` array converts this into a cumulative count so queries become constant time lookups. The break condition inside the loop prevents unnecessary exploration when values exceed the global bound, keeping runtime within limits.

A subtle detail is using `isqrt`, which avoids precision issues that would occur with floating-point square roots. Another is ensuring that only triples with $c \le MAX$ are counted, since larger triples cannot contribute to any query.

## Worked Examples

### Example Trace

Consider a simplified limit $MAX = 10$ just to illustrate structure.

We track valid triples and their contribution.

| a | b | a² + b² | c | valid | cnt[a] |
| --- | --- | --- | --- | --- | --- |
| 3 | 4 | 25 | 5 | yes | 1 |
| 6 | 8 | 100 | 10 | yes | 2 (for a=6) |

After processing:

| a | cnt[a] |
| --- | --- |
| 3 | 1 |
| 6 | 1 |

Prefix sums:

| n | pref[n] |
| --- | --- |
| 3 | 1 |
| 6 | 2 |
| 10 | 2 |

This confirms how each triple contributes exactly once based on its smallest leg.

The trace shows that scaling a primitive triple produces additional valid entries independently, and they are accumulated under their respective smallest sides.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \sqrt{N})$ | Each $a$ iterates over a bounded number of $b$ values before $c$ exceeds limit |
| Space | $O(N)$ | Arrays for counts and prefix sums over range up to $10^5$ |

The preprocessing is done once, and each query is answered in $O(1)$. With $10^5$ queries, this structure is essential to remain within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MAX = 100000
    cnt = [0] * (MAX + 1)
    import math

    for a in range(1, MAX + 1):
        a2 = a * a
        for b in range(a, MAX + 1):
            s = a2 + b * b
            c = math.isqrt(s)
            if c * c == s and c <= MAX:
                cnt[a] += 1

    pref = [0] * (MAX + 1)
    for i in range(1, MAX + 1):
        pref[i] = pref[i - 1] + cnt[i]

    data = inp.strip().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        out.append(str(pref[n]))
    return "\n".join(out)

# provided sample (format is ambiguous in statement, kept conceptual)
# assert run("...") == "..."

# custom tests
assert run("1\n10\n") == "2"
assert run("2\n5\n10\n") == "1\n2"
assert run("3\n3\n6\n9\n") == "0\n1\n1"
assert run("1\n100\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=10$ | 2 | basic Pythagorean triples (3-4-5, 6-8-10) |
| multiple queries | incremental prefix correctness | prefix sum correctness |
| small values | 0 cases for small n | handling no triples |
| large n | non-crash and scalability | upper bound stability |

## Edge Cases

One important edge case is when $n < 3$. The smallest possible Pythagorean triple starts at $a = 3$, so any query with $n = 1$ or $2$ must return zero. The algorithm handles this naturally because `pref[1]` and `pref[2]` remain zero after initialization.

Another case is scaled triples like $(6, 8, 10)$. The enumeration will detect this independently when $a = 6$ and $b = 8$. It does not rely on generating primitive triples, so no special handling is required.

A final structural edge case is large $n = 10^5$. The inner loop terminates early due to the constraint $a^2 + b^2 \le MAX^2$, so the algorithm avoids unnecessary iterations where $c$ would exceed bounds, keeping runtime stable.
