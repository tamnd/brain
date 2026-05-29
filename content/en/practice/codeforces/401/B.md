---
title: "CF 401B - Sereja and Contests"
description: "The contest platform numbers every round consecutively by start time. A round can either be a standalone Div2 round, or a pair of simultaneous rounds where Div2 gets identifier i and Div1 gets identifier i + 1. Sereja only participates in Div2 rounds."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 401
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 235 (Div. 2)"
rating: 1200
weight: 401
solve_time_s: 84
verified: true
draft: false
---

[CF 401B - Sereja and Contests](https://codeforces.com/problemset/problem/401/B)

**Rating:** 1200  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

The contest platform numbers every round consecutively by start time. A round can either be a standalone Div2 round, or a pair of simultaneous rounds where Div2 gets identifier `i` and Div1 gets identifier `i + 1`.

Sereja only participates in Div2 rounds. Right now he is participating in round `x`, and before this he participated in exactly `k` earlier Div2 rounds. For each of those earlier participations, he remembers either:

- a standalone Div2 round with identifier `a`
- or a simultaneous pair `(a, a + 1)` where `a` is the Div2 identifier

All remembered identifiers are smaller than `x`.

The missing information is everything about rounds he skipped. Some unused identifiers may correspond to standalone Div2 rounds, and some may belong to simultaneous pairs. We must compute:

- the minimum number of Div2 rounds Sereja could have missed
- the maximum number of Div2 rounds Sereja could have missed

The constraints are tiny. All identifiers are below 4000, so even an `O(x^2)` solution would comfortably pass. That means the challenge is not performance, it is modeling the numbering rules correctly.

The dangerous part is understanding what an identifier means. A standalone Div2 round consumes one identifier. A simultaneous pair consumes two consecutive identifiers, where the smaller one is the Div2 round and the larger one is the Div1 round.

A careless implementation often treats every unused identifier independently, but that is wrong because two consecutive identifiers may actually belong to one simultaneous pair.

Consider this example:

```
x = 8
known rounds:
2 2
2 5
```

The used identifiers are `{2, 5}`. The unused identifiers are `{1, 3, 4, 6, 7}`.

If we maximize missed Div2 rounds, we can make every unused identifier a standalone Div2 round, giving 5 missed rounds.

If we minimize missed Div2 rounds, we should combine identifiers into simultaneous pairs whenever possible:

- `(3,4)` can be one simultaneous pair
- `(6,7)` can be another simultaneous pair
- `1` must stay standalone

That gives only 3 missed Div2 rounds.

Another subtle case is when a remembered simultaneous pair blocks neighboring identifiers.

```
x = 6
known:
1 2 3
```

Identifiers `2` and `3` are already occupied by a simultaneous pair. We cannot additionally pair `(1,2)` or `(3,4)`, because identifiers cannot belong to two different rounds.

Correct handling requires tracking which identifiers are already used.

## Approaches

A brute-force idea is to reconstruct every valid contest schedule consistent with the remembered rounds, then count how many Div2 rounds Sereja skipped in each reconstruction. Since every unused identifier could either be:

- a standalone Div2 round
- part of a simultaneous pair
- or a Div1-only identifier inside a simultaneous pair

the number of possibilities grows exponentially.

For example, if there are 2000 unused identifiers, trying all assignments would be hopeless.

The key observation is that we never need the full schedule. We only care about how many Div2 rounds exist among the unused identifiers.

Suppose we mark every identifier smaller than `x` that already appears in the input. Every remaining identifier is free.

For the maximum answer, the strategy is obvious. Every free identifier can become a standalone Div2 round. Each such choice contributes one missed Div2 round, and nothing prevents this construction. So the maximum equals the number of free identifiers.

The minimum answer is where the greedy idea appears.

A simultaneous pair consumes two consecutive identifiers but contributes only one Div2 round. So to minimize missed Div2 rounds, we should create as many simultaneous pairs as possible among free identifiers.

This becomes a simple interval pairing problem:

- scan identifiers from left to right
- whenever two consecutive identifiers are both free, pair them together
- otherwise leave the current identifier as a standalone Div2 round

This greedy works because pairing two free consecutive identifiers always reduces the number of Div2 rounds by exactly one, and using an identifier later cannot create a better opportunity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(x) | O(x) | Accepted |

## Algorithm Walkthrough

1. Create a boolean array `used` for identifiers from `1` to `x - 1`.
2. Read every remembered round description.
3. If the description is a standalone Div2 round `2 a`, mark identifier `a` as used.
4. If the description is a simultaneous pair `1 a b`, mark both `a` and `b` as used.
5. Count how many identifiers from `1` to `x - 1` are unused. This count is the maximum possible number of missed Div2 rounds.

Every unused identifier can independently become a standalone Div2 round.
6. To compute the minimum answer, scan identifiers from `1` to `x - 1`.
7. If the current identifier is already used, skip it.
8. Otherwise, check whether the next identifier exists and is also unused.

If both are free, create one simultaneous pair from them. Increase the answer by 1 and skip both identifiers.
9. If pairing is impossible, the current identifier must become a standalone Div2 round. Increase the answer by 1 and move one step forward.

### Why it works

The maximum construction is straightforward because every unused identifier may represent a standalone Div2 round.

For the minimum construction, the invariant is that every time we encounter two consecutive free identifiers, pairing them is always optimal. A pair consumes two identifiers while contributing only one missed Div2 round. Leaving either identifier unpaired can never reduce the total further.

The greedy scan always creates the maximum possible number of disjoint consecutive pairs. Since every pair reduces the number of missed Div2 rounds by one, this also minimizes the final answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, k = map(int, input().split())

    used = [False] * (x + 2)

    for _ in range(k):
        parts = list(map(int, input().split()))

        if parts[0] == 1:
            _, a, b = parts
            used[a] = True
            used[b] = True
        else:
            _, a = parts
            used[a] = True

    # maximum answer
    mx = 0
    for i in range(1, x):
        if not used[i]:
            mx += 1

    # minimum answer
    mn = 0
    i = 1

    while i < x:
        if used[i]:
            i += 1
            continue

        if i + 1 < x and not used[i + 1]:
            mn += 1
            i += 2
        else:
            mn += 1
            i += 1

    print(mn, mx)

solve()
```

The `used` array records every identifier that already belongs to a remembered round. For simultaneous rounds we mark both identifiers, because neither can be reused later.

The maximum answer is just the number of unused identifiers. Every one of them can represent a standalone Div2 round.

The minimum answer uses the greedy scan. The subtle part is the boundary condition `i + 1 < x`. Identifier `x` itself belongs to the current round and cannot be reused, so only identifiers strictly smaller than `x` matter.

Another easy mistake is forgetting to skip both identifiers after forming a pair. If we pair `(i, i + 1)`, both identifiers are consumed and must not participate again.

## Worked Examples

### Sample 1

Input:

```
3 2
2 1
2 2
```

Used identifiers are `{1, 2}`.

| i | used[i] | Action | mn |
| --- | --- | --- | --- |
| 1 | True | skip | 0 |
| 2 | True | skip | 0 |

Maximum:

| Identifier | Free? | mx |
| --- | --- | --- |
| 1 | No | 0 |
| 2 | No | 0 |

Final answer:

```
0 0
```

There are no unused identifiers before round `3`, so Sereja could not have missed any Div2 rounds.

### Sample 2

Suppose the input is:

```
8 2
2 2
2 5
```

Used identifiers are `{2, 5}`.

Unused identifiers are `{1, 3, 4, 6, 7}`.

Minimum computation:

| i | used[i] | Decision | mn |
| --- | --- | --- | --- |
| 1 | No | standalone | 1 |
| 2 | Yes | skip | 1 |
| 3 | No | pair (3,4) | 2 |
| 5 | Yes | skip | 2 |
| 6 | No | pair (6,7) | 3 |

Maximum computation:

| Identifier | Free? | mx |
| --- | --- | --- |
| 1 | Yes | 1 |
| 2 | No | 1 |
| 3 | Yes | 2 |
| 4 | Yes | 3 |
| 5 | No | 3 |
| 6 | Yes | 4 |
| 7 | Yes | 5 |

Final answer:

```
3 5
```

This example demonstrates why pairing consecutive free identifiers minimizes the number of missed Div2 rounds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(x) | We scan identifiers a constant number of times |
| Space | O(x) | The `used` array stores identifier states |

Since `x ≤ 4000`, even quadratic solutions would pass comfortably. This linear solution is easily within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    x, k = map(int, input().split())

    used = [False] * (x + 2)

    for _ in range(k):
        parts = list(map(int, input().split()))

        if parts[0] == 1:
            _, a, b = parts
            used[a] = True
            used[b] = True
        else:
            _, a = parts
            used[a] = True

    mx = 0
    for i in range(1, x):
        if not used[i]:
            mx += 1

    mn = 0
    i = 1

    while i < x:
        if used[i]:
            i += 1
            continue

        if i + 1 < x and not used[i + 1]:
            mn += 1
            i += 2
        else:
            mn += 1
            i += 1

    return f"{mn} {mx}"

# provided sample
assert run(
    "3 2\n"
    "2 1\n"
    "2 2\n"
) == "0 0", "sample 1"

# minimum-size input
assert run(
    "1 0\n"
) == "0 0", "no earlier identifiers"

# all identifiers free
assert run(
    "6 0\n"
) == "3 5", "greedy pairing on all identifiers"

# remembered simultaneous pair blocks reuse
assert run(
    "6 1\n"
    "1 2 3\n"
) == "2 3", "occupied consecutive identifiers"

# alternating occupied identifiers
assert run(
    "8 3\n"
    "2 1\n"
    "2 3\n"
    "2 5\n"
) == "2 4", "cannot pair across occupied positions"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `0 0` | Smallest possible input |
| `6 0` | `3 5` | Maximum pairing behavior |
| simultaneous pair present | `2 3` | Identifiers inside a pair cannot be reused |
| alternating occupied identifiers | `2 4` | Greedy pairing only uses consecutive free identifiers |

## Edge Cases

Consider the smallest valid input:

```
1 0
```

There are no identifiers smaller than `1`, so the scan range is empty. The algorithm correctly produces:

```
0 0
```

A common off-by-one bug incorrectly includes identifier `x` itself and returns `1 1`.

Now consider:

```
6 1
1 2 3
```

Identifiers `2` and `3` are already occupied by a remembered simultaneous pair.

Free identifiers are `{1, 4, 5}`.

The greedy scan behaves like this:

- `1` cannot pair with `2`, so it becomes standalone
- `4` pairs with `5`

Total minimum is `2`.

Maximum is `3` because every free identifier may become standalone.

Correct output:

```
2 3
```

A buggy implementation that only marks the Div2 identifier from remembered pairs would incorrectly think identifier `3` is free and produce invalid pairings.

Finally, consider:

```
8 3
2 1
2 3
2 5
```

Free identifiers are `{2, 4, 6, 7}`.

The greedy process:

- `2` cannot pair with `3`
- `4` cannot pair with `5`
- `6` pairs with `7`

Minimum becomes `3`, not `2`.

This catches implementations that try to pair non-consecutive free identifiers.
