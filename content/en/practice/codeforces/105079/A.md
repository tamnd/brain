---
title: "CF 105079A - Ordering Cupcakes"
description: "We are given a party with a fixed number of guests, and each guest names exactly one cupcake flavor they would be satisfied with. Each flavor is identified by an integer from 1 to M."
date: "2026-06-27T22:48:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105079
codeforces_index: "A"
codeforces_contest_name: "UTPC x WiCS Contest 04-05-23 (UT Internal)"
rating: 0
weight: 105079
solve_time_s: 71
verified: false
draft: false
---

[CF 105079A - Ordering Cupcakes](https://codeforces.com/problemset/problem/105079/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a party with a fixed number of guests, and each guest names exactly one cupcake flavor they would be satisfied with. Each flavor is identified by an integer from 1 to M. Alice can only buy cupcakes in bundles of 12, meaning if she orders x dozens of a flavor, she receives exactly 12x cupcakes of that flavor.

The requirement is that for every flavor, Alice must buy enough cupcakes so that at least as many cupcakes of that flavor are available as the number of guests who prefer it. The output is not the number of cupcakes, but the number of dozens per flavor, for all M flavors.

The key transformation is that the problem reduces to counting demand per flavor and then rounding that demand up to the nearest multiple of 12 independently for each flavor.

The constraints are small enough that a direct frequency count is sufficient. With N up to 10000 and M up to 100, we can safely scan all guests once and compute frequencies in linear time. Even a slightly more expensive approach would pass, but anything involving nested iteration over guests per flavor would be unnecessary overkill.

A subtle failure case appears when the number of guests for a flavor is exactly divisible by 12 versus not divisible. For example, if 12 guests want flavor 1, then exactly 1 dozen is enough. If 13 guests want flavor 1, then 1 dozen is insufficient and we must buy 2 dozens, giving 24 cupcakes, even though only 13 are needed. A naive approach that divides using integer division without rounding up would undercount in these cases.

Another edge case is when no guest wants a flavor at all. The correct output is 0 dozens for that flavor. Any implementation that initializes counts incorrectly or forgets to handle zero-frequency flavors could accidentally output 1 due to rounding logic applied blindly.

## Approaches

A brute-force way to think about this is to simulate buying cupcakes incrementally. For each flavor, we could repeatedly increase the number of dozens until 12 times that value is at least the required number of guests. This is correct because it directly enforces the constraint, but in the worst case we might iterate up to N/12 steps per flavor. With M flavors, this becomes O(M * N), which is still acceptable here but unnecessarily indirect.

The more direct observation is that each flavor is independent. There is no coupling between flavors because cupcakes are flavor-specific and constraints are per-flavor. This means we only need the frequency count of each flavor, then convert each count into a ceiling division by 12. The key simplification is recognizing that the bakery constraint only introduces rounding, not interaction.

Once we accept that each flavor reduces to a single arithmetic operation, the problem becomes a straightforward counting task followed by integer ceiling division.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M * N / 12) | O(M) | Too slow in structure, unnecessary |
| Optimal | O(N + M) | O(M) | Accepted |

## Algorithm Walkthrough

### Steps

1. Read N and M, then read the list of guest preferences.

This gives a direct representation of demand per flavor, which is the only information relevant to the output.
2. Initialize an array `cnt` of size M+1 to zero.

Each index corresponds to a flavor, and we accumulate how many guests require it.
3. Iterate through all guests and increment `cnt[f_i]` for each preference.

This compresses the entire input into per-flavor demand counts.
4. For each flavor i from 1 to M, compute required dozens as `(cnt[i] + 11) // 12`.

This is integer ceiling division by 12, ensuring we never underbuy cupcakes.
5. Output each computed value on its own line.

### Why it works

Each flavor is completely independent in both demand and supply. The only constraint is that 12 cupcakes come together per unit purchase. For any non-negative integer demand d, the smallest integer x such that 12x ≥ d is exactly the ceiling of d/12. Since no flavor can substitute for another, solving each flavor separately produces a globally optimal solution with minimal total cupcakes purchased.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    cnt = [0] * (m + 1)

    for f in arr:
        cnt[f] += 1

    out = []
    for i in range(1, m + 1):
        out.append(str((cnt[i] + 11) // 12))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first builds a frequency table so that all later computation is O(1) per flavor. The use of `(cnt[i] + 11) // 12` is the standard integer trick for ceiling division without floating point operations.

One subtle point is indexing: flavors start at 1, so the frequency array must be of size M+1, not M. This avoids off-by-one errors when a guest selects flavor M.

## Worked Examples

### Sample 1

Input:

```
3 2
1 2 1
```

| Step | cnt[1] | cnt[2] | Output calc |
| --- | --- | --- | --- |
| After counting | 2 | 1 | - |
| Final | 2 | 1 | (2+11)//12 = 0, (1+11)//12 = 1 |

Output:

```
1
1
```

The trace shows that even small counts under 12 still produce 1 dozen because at least one cupcake is needed and purchases come in blocks of 12.

### Sample 2

Input:

```
14 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1
```

| Step | cnt[1] | cnt[2] | Output calc |
| --- | --- | --- | --- |
| After counting | 14 | 0 | - |
| Final | 14 | 0 | (14+11)//12 = 2, 0 |

Output:

```
2
0
```

This confirms the rounding behavior: 14 requires 2 dozens since one dozen (12) is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | One pass to count frequencies and one pass to compute results |
| Space | O(M) | Frequency array for M flavors |

The constraints allow up to 10000 guests and 100 flavors, so this solution runs in negligible time and memory, dominated only by input parsing.

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

# sample 1
assert run("3 2\n1 2 1\n") == "1\n1"

# sample 2
assert run("14 2\n" + "1 "*14 + "\n") == "2\n0"

# single guest
assert run("1 3\n2\n") == "0\n1\n0"

# all same flavor exactly 12
assert run("12 1\n" + "1 "*12 + "\n") == "1"

# boundary just over
assert run("13 1\n" + "1 "*13 + "\n") == "2"

# no demand except last flavor
assert run("5 4\n1 1 1 1 1\n") == "1\n0\n0\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single guest | 0 1 0 | sparse demand handling |
| 12 exact | 1 | exact division case |
| 13 single flavor | 2 | ceiling boundary |
| no demand for most flavors | zeros | correct zero handling |

## Edge Cases

A key edge case is when a flavor has zero demand. For example:

Input:

```
5 3
1 1 1 1 1
```

The count array becomes cnt[1]=5, cnt[2]=0, cnt[3]=0. Applying ceiling division gives 1, 0, 0.

The algorithm correctly produces zero for flavors 2 and 3 because `(0 + 11) // 12 = 0`. A flawed implementation that mistakenly enforces a minimum of 1 dozen per flavor would incorrectly output positive values even when no guest requests that flavor.

Another edge case is exact multiples of 12. For cnt[i]=12, we get `(12+11)//12 = 1`, matching the fact that one dozen is perfectly sufficient. This confirms that the rounding logic does not overbuy in clean division cases.
