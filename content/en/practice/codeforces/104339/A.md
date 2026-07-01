---
title: "CF 104339A - Three kings"
description: "Each king commands an army split into identical regiments. Barley has $a$ regiments, each containing $x$ soldiers, so his total army size is $a cdot x$. Hops and Malt are described the same way, using $b cdot y$ and $c cdot z$."
date: "2026-07-01T18:37:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104339
codeforces_index: "A"
codeforces_contest_name: "FAMCS Olympiad for scholars, Qualification (copy)"
rating: 0
weight: 104339
solve_time_s: 57
verified: true
draft: false
---

[CF 104339A - Three kings](https://codeforces.com/problemset/problem/104339/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Each king commands an army split into identical regiments. Barley has $a$ regiments, each containing $x$ soldiers, so his total army size is $a \cdot x$. Hops and Malt are described the same way, using $b \cdot y$ and $c \cdot z$.

The task is not to rank all three armies, but to find the maximum total army size among them and then list every king whose army matches that maximum. The output must contain the names of all such kings, and those names must be printed in lexicographical order.

The constraints are small enough that direct arithmetic is sufficient. Each value is at most $10^3$, so each total army size is at most $10^6$. Even if we recompute everything multiple times, the cost is negligible. This places the solution firmly in constant time per test case.

The only subtlety comes from equality cases. It is easy to incorrectly print a single king if one is strictly larger, but the problem explicitly requires collecting all kings tied for the maximum. Another possible mistake is forgetting lexicographical ordering of names, which matters only when multiple kings qualify.

A concrete edge case is when all three armies are equal, for example:

Input:

```
2 2 2 3 3 3
```

All totals are $6$, so the correct output is:

```
Barley Hops Malt
```

A naive “pick the max and print one name” approach would fail here.

Another edge case is when two kings tie for maximum:

Input:

```
2 3 3 6 3 4
```

Totals are Barley $12$, Hops $9$, Malt $12$, so both Barley and Malt must be printed.

## Approaches

A brute-force interpretation would compute each army size independently and then repeatedly scan through the results to determine which are maximal. Since there are only three values, even an overcomplicated approach remains trivial in complexity, but one could imagine extending this pattern to many kings where repeated scans become expensive.

In this problem, the structure is simple enough that no iterative refinement is needed. We compute three products once, compare them once, and then select all entries equal to the maximum. The key observation is that the “decision set” is extremely small and fixed in size, so sorting or multiple passes are unnecessary.

The brute-force idea works because it directly evaluates all candidates. It becomes unnecessary not due to inefficiency, but because there is no combinatorial structure to exploit, the dataset is fixed-size and fully independent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct evaluation with scanning | O(1) | O(1) | Accepted |
| Optimal direct comparison | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total army sizes for each king as $A = a \cdot x$, $B = b \cdot y$, and $C = c \cdot z$. This transforms the input from regiment structure into comparable scalar values.
2. Determine the maximum value among $A$, $B$, and $C$. This represents the strongest army size.
3. Initialize an empty list of winners. For each king, check whether their total equals the maximum. If so, include their name. This ensures ties are preserved.
4. Output the selected names in lexicographical order. Since the names are fixed strings, this reduces to ordering among "Barley", "Hops", and "Malt".

### Why it works

Each king’s strength is fully captured by a single scalar multiplication. The comparison of armies reduces to comparing these scalars, and equality against the maximum correctly identifies all strongest armies. Because every king is checked independently against the same reference value, no winner can be omitted or incorrectly added.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, c, x, y, z = map(int, input().split())

    barley = a * x
    hops = b * y
    malt = c * z

    mx = max(barley, hops, malt)

    ans = []
    if barley == mx:
        ans.append("Barley")
    if hops == mx:
        ans.append("Hops")
    if malt == mx:
        ans.append("Malt")

    print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The solution first converts each king’s regiments into a total count. It then finds the maximum among the three computed values. Each king name is conditionally appended if and only if their computed total matches this maximum. The ordering of checks is already lexicographically correct because "Barley" comes before "Hops" and "Malt", so no additional sorting is needed.

## Worked Examples

### Sample 1

Input:

```
2 4 3 6 3 4
```

Totals:

Barley = 12, Hops = 12, Malt = 12

| Step | Barley | Hops | Malt | Max | Current Winners |
| --- | --- | --- | --- | --- | --- |
| Compute totals | 12 | 12 | 12 | - | - |
| Find max | 12 | 12 | 12 | 12 | - |
| Check Barley | 12 | 12 | 12 | 12 | Barley |
| Check Hops | 12 | 12 | 12 | 12 | Barley Hops |
| Check Malt | 12 | 12 | 12 | 12 | Barley Hops Malt |

This demonstrates full tie handling where every king matches the maximum.

### Sample 2

Input:

```
2 3 3 6 3 4
```

Totals:

Barley = 12, Hops = 9, Malt = 12

| Step | Barley | Hops | Malt | Max | Current Winners |
| --- | --- | --- | --- | --- | --- |
| Compute totals | 12 | 9 | 12 | - | - |
| Find max | 12 | 9 | 12 | 12 | - |
| Check Barley | 12 | 9 | 12 | 12 | Barley |
| Check Hops | 12 | 9 | 12 | 12 | Barley |
| Check Malt | 12 | 9 | 12 | 12 | Barley Malt |

This shows selective inclusion of only those matching the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and comparisons are performed |
| Space | O(1) | Only a constant number of variables are used |

The computation is constant-time regardless of input magnitude, which is easily within the limits of a 2-second constraint and 256 MB memory cap.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return io.StringIO().getvalue() if False else (lambda: (solve(), ""))[1]()

# provided samples
assert run("2 4 3 6 3 4\n") == "Barley Hops Malt", "sample 1"
assert run("2 3 3 6 3 4\n") == "Barley Malt", "sample 2"

# custom cases
assert run("1 1 1 1 2 3\n") == "Hops Malt", "tie on max 3"
assert run("5 1 1 2 2 2\n") == "Barley", "single max"
assert run("3 3 3 3 3 3\n") == "Barley Hops Malt", "all equal"
assert run("10 1 10 1 5 1\n") == "Barley Malt", "boundary tie"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 2 3 | Hops Malt | multiple winners, non-trivial ordering |
| 5 1 1 2 2 2 | Barley | single clear maximum |
| 3 3 3 3 3 3 | Barley Hops Malt | full tie case |
| 10 1 10 1 5 1 | Barley Malt | tie with different magnitudes |

## Edge Cases

When all three armies are equal, the algorithm still correctly includes every king because each comparison checks equality against the same maximum value. For input:

```
3 3 3 3 3 3
```

the computed totals are all 9, so the maximum is 9, and all three conditional checks succeed, producing all names in correct order.

When exactly two armies tie for maximum, such as:

```
2 3 3 6 3 4
```

Barley and Malt both evaluate to 12 while Hops is smaller. The max is 12, so only those two are appended. The algorithm does not rely on strict ordering between kings, only equality against the global maximum, which ensures correctness regardless of how ties are distributed.
