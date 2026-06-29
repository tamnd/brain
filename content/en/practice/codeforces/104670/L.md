---
title: "CF 104670L - Locust Locus"
description: "Each input line describes a pair of periodic events. For a given pair, two species reappear every fixed number of years, and we are told the last year when both of them appeared together. From that information we want to predict when that same pair will next appear together."
date: "2026-06-29T09:37:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104670
codeforces_index: "L"
codeforces_contest_name: "2021-2022 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2021)"
rating: 0
weight: 104670
solve_time_s: 43
verified: true
draft: false
---

[CF 104670L - Locust Locus](https://codeforces.com/problemset/problem/104670/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input line describes a pair of periodic events. For a given pair, two species reappear every fixed number of years, and we are told the last year when both of them appeared together. From that information we want to predict when that same pair will next appear together.

So for every triple consisting of a last simultaneous year and two cycle lengths, we are effectively looking at a repeating pattern on the number line: starting from that year, one event repeats every `c1` years and the other every `c2` years. The pair coincides whenever both cycles align again.

The task is to compute the next such coincidence year for each pair and then select the earliest one among all pairs.

The constraints are small enough that we can directly compute the answer per pair without any need for optimization tricks beyond basic arithmetic. With at most 99 pairs and cycle lengths below 100, even a direct computation per pair is trivial in constant time.

A naive mistake that can appear here is assuming the next simultaneous appearance is simply `y + max(c1, c2)`. That fails because alignment depends on both cycles simultaneously, not just the slower one.

For example, if `y = 2000`, `c1 = 6`, `c2 = 4`, then adding 6 gives 2006, but 2006 is not divisible by 4 from the base alignment, so it is not a valid simultaneous appearance. The correct next coincidence is determined by the least common multiple.

Another subtle issue is forgetting that we are asked for the _first year among all pairs_, not the first pair independently. Each pair produces a candidate year, and only after computing all candidates do we compare them.

## Approaches

A direct way to solve the problem is to simulate year by year starting from `y + 1`, checking for each candidate year whether it matches both cycles. For a given pair, this means repeatedly checking whether `(year - y) % c1 == 0` and `(year - y) % c2 == 0`. Since cycles are at most 99, the next match is guaranteed within at most `lcm(c1, c2)` steps, which is bounded by 9801. With at most 99 pairs, this approach is still acceptable, but it is unnecessarily indirect.

A cleaner observation comes from understanding what “both cycles align again” means structurally. Once two periodic sequences coincide at year `y`, they will coincide again exactly every `lcm(c1, c2)` years. This removes any need for simulation. The next occurrence is fixed as `y + lcm(c1, c2)`.

This reduces the task to computing one arithmetic value per pair and taking a minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k · lcm(c1,c2)) | O(1) | Accepted but unnecessary |
| LCM Direct Computation | O(k log min(c1,c2)) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each pair, read the last simultaneous year `y` and cycle lengths `c1`, `c2`. This defines a repeating alignment problem anchored at `y`.
2. Compute the greatest common divisor of `c1` and `c2`, then derive the least common multiple using `lcm = (c1 // gcd) * c2`. This gives the exact period after which both cycles align again.
3. Compute the next occurrence year for this pair as `y + lcm`.
4. Track the minimum of all computed next occurrence years across all pairs, since the problem asks for the earliest future coincidence among all species pairs.

### Why it works

Once two periodic processes align at a point in time, their future alignments form a strictly periodic sequence governed by the least common multiple of their individual periods. Any earlier coincidence than `lcm(c1, c2)` would contradict the definition of least common multiple, since it would imply a smaller shared period. Therefore, each pair contributes exactly one candidate next year, and selecting the minimum across pairs preserves correctness globally.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    k = int(input())
    ans = 10**30

    for _ in range(k):
        y, c1, c2 = map(int, input().split())
        g = math.gcd(c1, c2)
        lcm = (c1 // g) * c2
        ans = min(ans, y + lcm)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads each triple and immediately transforms it into a deterministic future event year. The key implementation detail is computing the least common multiple using integer-safe division before multiplication, which prevents overflow and preserves correctness even when values are close to the upper bound.

The final answer is maintained incrementally, avoiding storage of all candidates.

## Worked Examples

Consider the input:

```
2
1992 13 17
1992 14 18
```

For the first pair, we compute `lcm(13, 17) = 221`, so the next year is `1992 + 221 = 2213`.

For the second pair, `lcm(14, 18) = 126`, so the next year is `1992 + 126 = 2118`.

| Pair | y | c1 | c2 | gcd | lcm | Next year |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1992 | 13 | 17 | 1 | 221 | 2213 |
| 2 | 1992 | 14 | 18 | 2 | 126 | 2118 |

The answer is `2118` because it is the smaller of the two candidate years. This trace shows that each pair is independent and only contributes one fixed future event.

Now consider:

```
1
2001 5 7
```

Here `gcd(5,7)=1`, so `lcm=35` and the next occurrence is `2036`. There are no competing pairs, so this is the final answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log C) | Each pair requires a gcd computation on values up to 99, which is constant bounded in practice |
| Space | O(1) | Only a few integers are maintained regardless of input size |

The constraints allow up to 99 pairs, and each computation is constant-time arithmetic, so the solution comfortably runs within limits.

## Test Cases

```python
import sys, io
import math

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import gcd

    k = int(input())
    ans = 10**30
    for _ in range(k):
        y, c1, c2 = map(int, input().split())
        g = gcd(c1, c2)
        lcm = (c1 // g) * c2
        ans = min(ans, y + lcm)
    return str(ans)

def run(inp: str) -> str:
    return solve_io(inp)

# provided samples (from statement image, reconstructed format)
assert run("2\n1992 13 17\n1992 14 18\n") == "2118"
assert run("1\n2001 5 7\n") == "2036"

# custom cases
assert run("1\n2020 2 3\n") == "2026", "minimum case style"
assert run("3\n2010 2 3\n2011 4 6\n2012 5 7\n") == str(min(2010+6, 2011+12, 2012+35)), "multiple pairs"
assert run("1\n2021 99 99\n") == str(2021 + 99), "equal cycles"
assert run("2\n1800 1 1\n1801 2 3\n") == str(min(1800+1, 1801+6)), "boundary gcd"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 pair small cycles | 2026 | smallest meaningful lcm behavior |
| multiple pairs | computed min | global minimum selection |
| equal cycles | y + c | gcd edge case where lcm reduces |
| boundary gcd cases | correct min | correctness at extremes |

## Edge Cases

A first edge case occurs when both cycle lengths are identical. For an input like `2021 10 10`, the gcd equals the number itself, so the lcm collapses to 10. The algorithm correctly produces `2021 + 10`, and no special handling is needed because the formula naturally handles this case.

Another case is when one cycle divides the other, such as `2010 4 12`. Here the gcd is 4, so lcm becomes 12, not 16. A naive multiplication approach without dividing by gcd would overestimate the period and produce an incorrect later year, while the implemented formula avoids double counting shared factors.

A final edge case is when multiple pairs produce very close candidate years. Since we only track a running minimum, the algorithm correctly handles ties and ordering without requiring sorting or storage of intermediate results.
