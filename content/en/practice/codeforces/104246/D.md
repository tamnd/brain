---
title: "CF 104246D - Distribute the Pizza"
description: "A pizza is cut into identical radial slices. Each slice corresponds to a fixed central angle θ, so once θ is known, the total number of slices in a full pizza is completely determined by how many times θ fits into 360 degrees."
date: "2026-07-01T22:14:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104246
codeforces_index: "D"
codeforces_contest_name: "CodeSmash 2021 by RAPL"
rating: 0
weight: 104246
solve_time_s: 71
verified: false
draft: false
---

[CF 104246D - Distribute the Pizza](https://codeforces.com/problemset/problem/104246/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

A pizza is cut into identical radial slices. Each slice corresponds to a fixed central angle θ, so once θ is known, the total number of slices in a full pizza is completely determined by how many times θ fits into 360 degrees. The radius r is given but plays no role in how the slices are divided or distributed.

Two people want to split all available slices between them, and each slice must be given entirely to one person. The only question is whether the total number of slices can be split into two equal integer groups.

So the task reduces to checking whether the full pizza can be split into an even number of slices, given that the number of slices is implied by θ.

The constraints are small enough that each test case must be answered in constant time. With up to 2400 test cases, any solution that recomputes anything expensive per case is unnecessary. A direct arithmetic check is sufficient.

A subtle failure case appears when the number of slices is odd. For example, if θ = 120, then the pizza has 3 slices. One person would get 1 slice and the other 2, which is not equal, so the answer must be NO. Another case is θ = 360, which yields a single slice, which is also impossible to split evenly.

The radius input can also mislead implementation: if it is parsed or used in computations, it can introduce unnecessary complexity or incorrect logic. It should be ignored entirely.

## Approaches

The brute-force way to think about the problem is to explicitly construct the pizza division. Given θ, we compute the number of slices n = 360 / θ, then simulate distributing these slices alternately or by counting and checking whether both people end up with the same number. This works, but it is overkill: the simulation itself is O(n) per test case, and in the worst case θ = 1 gives 360 slices per test, leading to unnecessary repeated work across up to 2400 cases.

The key observation is that we never need to simulate distribution at all. The only requirement for equal distribution is that the total number of slices is divisible by 2. Since the problem guarantees that θ divides 360, the number of slices is always an integer, so we only need to check whether (360 / θ) is even.

This reduces each test case to a single division and modulo check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(360 / θ) per test | O(1) | Too slow |
| Direct Arithmetic Check | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We compute the number of slices implied by the angle, then test whether that count is evenly divisible between the two people.

1. Read θ for each test case, ignoring r entirely because it does not affect slice count or distribution.
2. Compute the total number of slices as n = 360 / θ. This is valid because the problem guarantees the pizza can be divided into equal slices.
3. Check whether n is divisible by 2. If n % 2 == 0, both people can receive exactly n / 2 slices.
4. Output "YES" if the condition holds, otherwise output "NO".

### Why it works

The structure of the problem fixes the pizza into n identical discrete objects (slices). Any valid distribution must assign whole objects. Equal distribution is equivalent to splitting a set of size n into two equal integer parts. The only property that matters is parity of n. Since n is uniquely determined by 360 / θ, the decision reduces entirely to checking whether that quotient is even.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        r, theta = map(int, input().split())
        n = 360 // theta
        if n % 2 == 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently. The integer division is safe because θ is guaranteed to divide 360 evenly.

The only subtle implementation detail is ensuring that r is still parsed even though it is unused. Forgetting to read it correctly would desynchronize input parsing.

## Worked Examples

We trace the logic on the sample cases.

### Sample Input

```
310 45
5 40
8 60
```

| r | θ | n = 360/θ | n % 2 | Output |
| --- | --- | --- | --- | --- |
| 310 | 45 | 8 | 0 | YES |
| 5 | 40 | 9 | 1 | NO |
| 8 | 60 | 6 | 0 | YES |

The first case produces 8 slices, which splits into 4 and 4. The second produces 9 slices, which cannot be evenly divided. The third produces 6 slices, which splits into 3 and 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires constant-time arithmetic operations |
| Space | O(1) | No additional data structures are used |

The input size of at most 2400 test cases is easily handled with constant work per case, well within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio

    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""3
310 45
5 40
8 60
""") == "YES\nNO\nYES"

# theta = 360, single slice
assert run("""1
10 360
""") == "NO"

# theta = 180, two slices
assert run("""1
10 180
""") == "YES"

# theta = 90, four slices
assert run("""1
10 90
""") == "YES"

# theta = 120, three slices
assert run("""1
10 120
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| θ = 360 | NO | single slice edge case |
| θ = 180 | YES | minimal even split |
| θ = 120 | NO | odd number of slices case |
| θ = 90 | YES | general even case |

## Edge Cases

When θ = 360, the pizza becomes a single slice. The algorithm computes n = 1 and immediately rejects it since 1 is not divisible by 2, producing NO as required.

When θ = 180, we get n = 2. The modulo check confirms it is even, so the output is YES, corresponding to one slice per person.

When θ = 120, n = 3. Even though division is exact, parity fails, and the algorithm correctly outputs NO.
