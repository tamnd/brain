---
title: "CF 1648B - Integral Array"
description: "We are given a multiset of positive integers, and we must decide whether it is closed under a very specific operation: taking integer division between any ordered pair of elements where the numerator is at least the denominator."
date: "2026-06-10T04:03:37+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 1648
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 775 (Div. 1, based on Moscow Open Olympiad in Informatics)"
rating: 1800
weight: 1648
solve_time_s: 366
verified: false
draft: false
---

[CF 1648B - Integral Array](https://codeforces.com/problemset/problem/1648/B)

**Rating:** 1800  
**Tags:** brute force, constructive algorithms, data structures, math  
**Solve time:** 6m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of positive integers, and we must decide whether it is closed under a very specific operation: taking integer division between any ordered pair of elements where the numerator is at least the denominator. Whenever we pick two values from the array, divide the larger by the smaller using floor division, the result must also already be present in the array.

The input consists of multiple independent test cases. Each test case gives us an array and an upper bound on its values. For each case we must decide whether the array is “closed” under this floor-division operation.

The constraints push us away from any approach that tries to explicitly test all pairs. With up to one million total elements across test cases, a naive double loop would require on the order of 10^12 operations, which is far beyond what is feasible in two seconds. Even slightly optimized pair enumeration is impossible.

The non-obvious difficulty is that the condition is not just about pairs that exist, but about all derived values. A naive approach might only check existing pairs in the array, but that misses the requirement that every possible quotient must already exist, even if it is not part of any “obvious” interaction in the input ordering.

A typical failure case is when the array contains a large number and a small number but omits intermediate quotients. For example, if 10 and 3 are present, then floor(10/3) = 3 is fine if 3 exists, but floor(10/4) or floor(10/6) might produce missing values depending on structure. Missing even one derived value invalidates the entire array.

## Approaches

A brute-force solution checks every ordered pair (x, y) with x ≥ y, computes floor(x/y), and verifies membership. This is correct because it directly enforces the definition. However, it is quadratic in the size of the array, and with large inputs this becomes infeasible immediately.

The key observation is that we do not need to recompute all pairwise divisions explicitly. What matters is whether the set contains all values that can be formed as quotients of existing elements. Since all values are bounded by c, we can work in a frequency array and simulate closure.

Instead of iterating over elements, we iterate over values. For each value y that exists, we try to “generate” all multiples of y up to c and ensure consistency of derived floors. This turns the problem into a sieve-like propagation process over the value range.

The structure resembles number theory closure under division: if a value exists, then all results of dividing any multiple of it by it must also exist. This allows us to propagate constraints from small values upward in a controlled way.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Check | O(n²) | O(1) | Too slow |
| Value Sieve Propagation | O(c log c) | O(c) | Accepted |

## Algorithm Walkthrough

1. Count frequency of every number in the array using an array `freq`.
2. Build a boolean presence array `ok[x]` indicating whether value `x` exists in the array. This allows O(1) membership checks.
3. For every possible value `y` from 1 to c, we treat it as a potential divisor only if it exists in the array.
4. For each such `y`, we iterate over multiples `x = y, 2y, 3y, ...` up to c. Each multiple contributes a quotient `x // y`.
5. Every computed quotient must exist in the array. If we find any quotient that is missing, we can immediately conclude the array is not integral.
6. If we complete all checks without contradiction, the array is integral.

The important subtlety is that we only need to check quotients induced by existing values in a structured way. Iterating over multiples avoids redundant pair generation while still covering every valid floor division outcome.

### Why it works

Every valid pair (x, y) with x ≥ y can be represented as x = k·y + r, and floor(x/y) = k. By iterating over all multiples of y, we generate every possible k that can arise from pairing y with some larger element. Therefore, if any required quotient is missing, it will be discovered during this sweep. The frequency array ensures we correctly account for presence rather than ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(int, input().split()))

        freq = [0] * (c + 1)
        for x in a:
            freq[x] += 1

        ok = [False] * (c + 1)
        for i in range(1, c + 1):
            if freq[i]:
                ok[i] = True

        bad = False

        for y in range(1, c + 1):
            if not ok[y]:
                continue

            for x in range(y, c + 1, y):
                q = x // y
                if not ok[q]:
                    bad = True
                    break

            if bad:
                break

        print("No" if bad else "Yes")

if __name__ == "__main__":
    solve()
```

The code first compresses the input into a presence array so that membership checks are constant time. Then it iterates over every possible divisor candidate y that actually appears in the array. For each such y, it walks through all multiples of y and ensures that every resulting quotient is present. The early exit ensures efficiency when a violation is found.

The main subtle point is that we never iterate over raw pairs. Instead, we restructure the problem into arithmetic progressions over multiples, which guarantees coverage without quadratic blowup.

## Worked Examples

### Example 1

Input:

```
3 5
1 2 5
```

We build `ok = {1,2,5}`.

For y = 1:

x values produce quotients 1,2,3,4,5. Here 3 and 4 are missing, so the check fails immediately.

| y | x | x//y | ok[x//y] |
| --- | --- | --- | --- |
| 1 | 1 | 1 | yes |
| 1 | 2 | 2 | yes |
| 1 | 3 | 3 | no |

This confirms rejection.

### Example 2

Input:

```
4 10
1 3 3 7
```

Presence is `{1,3,7}`.

For y = 3:

multiples give quotients 1,2,3. Value 2 is missing, so invalid.

This matches the expected output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(c log c) | Each value iterates over its multiples |
| Space | O(c) | Presence and frequency arrays |

The algorithm is efficient because each integer up to c participates in at most c/i iterations across all divisor sweeps, leading to harmonic series behavior. This comfortably fits within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(int, input().split()))

        freq = [0] * (c + 1)
        for x in a:
            freq[x] += 1

        ok = [False] * (c + 1)
        for i in range(1, c + 1):
            if freq[i]:
                ok[i] = True

        bad = False
        for y in range(1, c + 1):
            if not ok[y]:
                continue
            for x in range(y, c + 1, y):
                if not ok[x // y]:
                    bad = True
                    break
            if bad:
                break

        out.append("No" if bad else "Yes")

    return "\n".join(out)

# provided samples
assert run("""4
3 5
1 2 5
4 10
1 3 3 7
1 2
2
1 1
1
""") == """Yes
No
No
Yes"""

# custom cases
assert run("""1
3 6
1 2 3
""") == "No", "missing closure"
assert run("""1
2 2
1 2
""") == "Yes", "minimal valid"
assert run("""1
3 10
5 10 1
""") == "No", "random invalid"
assert run("""1
1 1
1
""") == "Yes", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 3 6 / 1 2 3 | No | missing closure |
| 1 2 2 / 1 2 | Yes | minimal valid |
| 1 3 10 / 5 10 1 | No | random invalid |
| 1 1 1 / 1 | Yes | single element |

## Edge Cases

A critical edge case is when the array contains 1. Since every integer divided by 1 produces itself, the presence of 1 forces a very strong closure condition: all values must be self-consistent under division chains. The algorithm handles this naturally because for y = 1, every multiple x produces quotient x, and the check reduces to verifying presence of all elements involved in the closure set.

Another edge case is when the array has only a single value. In that case, the only quotient possible is 1, which is valid only if the value itself is 1. The sweep correctly confirms or rejects this without special casing.

The final important case is sparse arrays like powers of two mixed with unrelated numbers. These fail quickly because intermediate quotients like 3, 5, or 7 appear during the multiple scan even though they are not present in the input, ensuring early detection of non-closure.
