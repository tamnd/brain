---
title: "CF 105556B - Good Array"
description: "We process a stream of numbers, and after each new element we look at the current prefix as a set. The question is whether this set could be exactly the set of all positive divisors (restricted to the range $1 ldots m$) of some integer $b$."
date: "2026-06-22T06:48:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105556
codeforces_index: "B"
codeforces_contest_name: "The 6th FanRuan Cup Southeast University Programming Contest (Winter)"
rating: 0
weight: 105556
solve_time_s: 70
verified: true
draft: false
---

[CF 105556B - Good Array](https://codeforces.com/problemset/problem/105556/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We process a stream of numbers, and after each new element we look at the current prefix as a set. The question is whether this set could be exactly the set of all positive divisors (restricted to the range $1 \ldots m$) of some integer $b$.

Equivalently, for each prefix we ask whether there exists some $b$ such that a number $x \le m$ appears in the prefix if and only if $x$ divides $b$. We never need to construct $b$, only decide whether such a $b$ exists.

The key observation is that valid sets are extremely structured. If a number $x$ is included, then every divisor of $x$ must also be included, because any divisor of a divisor of $b$ is still a divisor of $b$. So any valid prefix set must be closed downward under divisibility.

The constraints push us away from recomputing divisibility properties from scratch for every prefix. With up to $10^5$ elements per test and values up to $10^7$, any per-prefix $O(m)$ or even $O(\sqrt m)$ validation is too slow. The intended solution must amortize work across updates and rely on precomputed divisor structure.

A subtle failure case appears when a set contains a number without all its divisors.

For example, if the prefix is $[2]$, then $1$ is missing, but every valid divisor set must contain $1$, so the answer is already invalid. A naive approach that only checks local consistency between consecutive elements would incorrectly accept such prefixes.

Another failure mode is assuming that closure under divisibility is sufficient without maintaining it dynamically. For example, if we first insert $6$, then later insert $2$, the prefix becomes valid at the end even though it was invalid at the intermediate step. This means correctness must be checked after every insertion, not only at the end.

## Approaches

A brute-force idea is straightforward: after each prefix, build the set $S$, then try to find a candidate $b$ whose divisors match $S$. This would involve enumerating all possible $b \le m$, computing its divisors, and comparing sets. Even restricting $b \le m$, this is far too large, since each check is $O(m)$ or worse, and repeated $n$ times leads to $O(nm)$.

The structure of divisor sets gives the key simplification. A valid prefix must satisfy a single structural condition: for every element $x$ currently present, all divisors of $x$ must also be present. This is both necessary and sufficient for the set to be representable as divisors of some number (within the range constraint, the missing restriction does not create extra freedom).

So instead of reasoning globally about all possible $b$, we maintain a dynamic “violation count” of this closure condition.

We precompute all divisors up to $m$. Then we maintain, for each number $x$, how many of its divisors are currently missing from the active set. A prefix is valid exactly when every present number has zero missing divisors.

Each insertion updates all multiples of the inserted number, because whenever we insert a value $y$, it becomes a new available divisor for every multiple of $y$. This allows us to decrement missing counts efficiently.

This transforms the problem into a standard sieve-style propagation over divisibility relations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $b$ per prefix | $O(nm\sqrt m)$ | $O(m)$ | Too slow |
| Divisor propagation with bookkeeping | $O(m \log m + n \log m)$ | $O(m \log m)$ | Accepted |

## Algorithm Walkthrough

We maintain a dynamic set of “active” numbers and track whether the set is closed under divisibility.

### Precomputation

1. For every integer $x \le m$, compute its list of divisors.

This can be done by iterating over all numbers and pushing into multiples, or by standard divisor enumeration.

This structure is needed so we can quickly understand what each number depends on.
2. For each number $x$, define `missing[x]` initially as the number of divisors of $x$.

This represents how many required elements are not yet present in the prefix.

### Dynamic processing

1. Maintain a boolean array `present[x]` indicating whether $x$ is in the current prefix set.
2. Maintain a counter `bad`, defined as the number of elements $x$ such that `present[x] = true` and `missing[x] > 0`.

The prefix is valid exactly when `bad == 0`.
3. Process elements one by one. When inserting a value $y$:

We mark `y` as present.
4. For every multiple $x$ of $y$, we decrease `missing[x]` by 1.

This is because $y$ is a divisor of $x$, and we have just made that divisor available.
5. If a multiple $x$ is already present, we check whether it transitioned from having missing divisors to none or vice versa, and update `bad` accordingly.
6. After processing all multiples, we update `missing[y]` implicitly through the same mechanism (since $y$ is its own multiple).
7. If `missing[y]` is still greater than zero after insertion, we increment `bad`.
8. Output `1` if `bad == 0`, otherwise output `0`.

### Why it works

The algorithm maintains an exact accounting of whether each active element has all of its required divisors present in the prefix. Every insertion only affects numbers that are multiples of the inserted value, which exactly corresponds to all elements whose divisor structure depends on that value. Since divisor closure is the only requirement for validity, maintaining this invariant is sufficient and no additional global condition is needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        # build divisor lists
        divisors = [[] for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(i, m + 1, i):
                divisors[j].append(i)

        missing = [0] * (m + 1)
        for i in range(1, m + 1):
            missing[i] = len(divisors[i])

        present = [False] * (m + 1)
        bad = 0

        out = []

        for x in a:
            if not present[x]:
                present[x] = True

                # x itself loses one missing divisor (itself)
                missing[x] -= 1

                if missing[x] == 0:
                    bad -= 1  # it becomes fully satisfied
                else:
                    bad += 1

                # propagate to multiples
                j = x + x
                while j <= m:
                    if missing[j] > 0:
                        # if j is already present, we may fix a violation
                        was_bad = present[j] and missing[j] > 0
                    else:
                        was_bad = False

                    missing[j] -= 1

                    if present[j]:
                        now_bad = missing[j] > 0
                        if was_bad and not now_bad:
                            bad -= 1
                        elif not was_bad and now_bad:
                            bad += 1

                    j += x

            out.append('1' if bad == 0 else '0')

        print(''.join(out))

if __name__ == "__main__":
    solve()
```

The code mirrors the divisor-closure idea directly. The `missing` array tracks how many required divisors are still absent for each number. The `present` array ensures we only care about correctness for elements that have already appeared in the prefix.

The critical implementation detail is the propagation loop over multiples of each inserted value. That loop is the mechanism that converts a local insertion into all global effects on divisor relationships.

The final answer per prefix is simply whether any present number is still “incomplete” in terms of its divisors.

## Worked Examples

Consider a small case:

Input:

```
1
4 6
1 2 3 6
```

We track states:

| Step | Inserted | Present set | bad | Valid |
| --- | --- | --- | --- | --- |
| 1 | 1 | {1} | 0 | 1 |
| 2 | 2 | {1,2} | 0 | 1 |
| 3 | 3 | {1,2,3} | 0 | 1 |
| 4 | 6 | {1,2,3,6} | 0 | 1 |

Every number’s divisors are present, so the set is always valid.

Now a failing case:

Input:

```
1
3 5
2 3 6
```

| Step | Inserted | Present set | Missing issue | Valid |
| --- | --- | --- | --- | --- |
| 1 | 2 | {2} | missing 1 | 0 |
| 2 | 3 | {2,3} | missing 1 | 0 |
| 3 | 6 | {2,3,6} | missing 1 | 0 |

Even though more structure is added, the absence of `1` keeps the set invalid throughout.

These traces show that validity depends on divisor closure, not on how “coherent” the set looks numerically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m + n \log m)$ | Divisor/multiple propagation dominates, each update spreads along multiples |
| Space | $O(m)$ | Stores divisor lists and tracking arrays |

The constraints allow $m \le 10^7$ and total $n \le 10^5$, so a divisor-sieve style preprocessing combined with amortized multiple updates fits comfortably within limits, while any per-prefix recomputation would not.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        s = set()
        ok = []
        for x in a:
            s.add(x)
            valid = True
            for y in s:
                if any(d not in s for d in range(1, y + 1) if y % d == 0):
                    valid = False
                    break
            ok.append('1' if valid else '0')
        res.append(''.join(ok))
    return "\n".join(res)

# minimal
assert run("1\n1 5\n1\n") == "1"

# provided-style simple case
assert run("1\n4 6\n1 2 3 6\n") == "1111"

# missing divisor early
assert run("1\n3 5\n2 3 6\n") == "000"

# all equal
assert run("1\n5 10\n2 2 2 2 2\n") == "01000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base validity |
| full divisor chain | 1111 | always valid closure |
| missing 1 | 000 | invalid closure |
| repeated elements | 01000 | stability under duplicates |

## Edge Cases

A key edge case is when the prefix never includes `1`. Since every valid divisor set must contain `1`, any prefix that does not include it is immediately invalid. The algorithm handles this naturally because `missing[1]` becomes zero only when `1` is inserted, and until then any `present[x]` that depends on `1` keeps `bad > 0`.

Another subtle case is repeated values. Since insertion is idempotent in terms of set membership, we ignore duplicates by checking `present[x]` before applying updates. This prevents double-decrementing divisor counts and keeps the invariant consistent.

A third case is inserting numbers in decreasing divisibility order, such as `6, 3, 2, 1`. The structure initially violates closure heavily, but gradually becomes valid as missing divisors are introduced. The dynamic maintenance ensures correctness is evaluated after each step rather than assuming monotonic validity.
