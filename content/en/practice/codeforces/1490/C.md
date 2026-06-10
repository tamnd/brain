---
title: "CF 1490C - Sum of Cubes"
description: "We are given several numbers, and for each number $x$, we must determine whether it can be written as the sum of two positive cubes. In other words, we want to know whether there exist positive integers $a$ and $b$ such that $$a^3 + b^3 = x."
date: "2026-06-10T22:37:19+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1490
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 702 (Div. 3)"
rating: 1100
weight: 1490
solve_time_s: 150
verified: true
draft: false
---

[CF 1490C - Sum of Cubes](https://codeforces.com/problemset/problem/1490/C)

**Rating:** 1100  
**Tags:** binary search, brute force, math  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several numbers, and for each number $x$, we must determine whether it can be written as the sum of two positive cubes.

In other words, we want to know whether there exist positive integers $a$ and $b$ such that

$$a^3 + b^3 = x.$$

The answer for each test case is simply "YES" if such a pair exists and "NO" otherwise.

The largest possible value of $x$ is $10^{12}$. That bound immediately tells us something useful about the size of the search space. Since

$$10000^3 = 10^{12},$$

any cube participating in the sum must come from an integer no larger than about 10,000.

A naive search over all pairs $(a,b)$ would require checking roughly $10^4 \times 10^4 = 10^8$ combinations for a single test case. With up to 100 test cases, that becomes completely impractical.

The constraints suggest that an algorithm around $10^4$ operations per test case is perfectly reasonable, while $10^8$ operations per test case is not.

There are a few easy-to-miss edge cases.

Consider:

```
1
1
```

The correct answer is:

```
NO
```

Although $1 = 1^3$, the problem requires a sum of two positive cubes. The smallest possible sum is $1^3 + 1^3 = 2$.

Consider:

```
1
16
```

The correct answer is:

```
YES
```

because $16 = 2^3 + 2^3$. A careless implementation that only checks distinct values of $a$ and $b$ would incorrectly reject this case.

Consider:

```
1
2
```

The correct answer is:

```
YES
```

because $2 = 1^3 + 1^3$. This is the smallest valid representation and is a useful boundary test.

Another common mistake is using floating-point cube roots. For values near $10^{12}$, rounding errors can cause an exact cube to be missed. Integer arithmetic avoids that problem entirely.

## Approaches

The most direct solution is to try every possible pair $(a,b)$. Since every relevant cube root is at most about 10,000, we could iterate through all values of $a$ and $b$, compute $a^3+b^3$, and check whether it equals $x$.

This approach is correct because it explicitly examines every candidate pair. The problem is the running time. Roughly $10^8$ pairs must be checked for a single test case, which is far beyond what fits within the time limit.

The key observation is that once we choose one cube, the other cube is completely determined.

Suppose we fix $a$. Then we need

$$b^3 = x - a^3.$$

Instead of trying every possible $b$, we only need to determine whether the value $x-a^3$ is itself a perfect cube.

Since there are only about 10,000 possible cube values, we can precompute all cubes up to $10^{12}$ and store them in a hash set. Then for every candidate $a$, we compute $x-a^3$ and perform an $O(1)$ membership test in the set.

This reduces the search from checking all pairs to checking only all possible first elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(M^2)$ | $O(1)$ | Too slow |
| Optimal | $O(M)$ | $O(M)$ | Accepted |

Here $M \approx 10^4$, the largest possible cube root.

## Algorithm Walkthrough

1. Precompute all cubes $i^3$ for positive integers $i$ while $i^3 \le 10^{12}$.
2. Store those cubes in a hash set. This allows constant-time checks of whether a number is a perfect cube from our precomputed range.
3. For each test case, read $x$.
4. Iterate through every precomputed cube value $c=a^3$.
5. Compute the remaining value $x-c$.
6. Check whether $x-c$ exists in the cube set.
7. If it exists, then $x=a^3+b^3$ for some positive integer $b$, so output `"YES"` and stop processing this test case.
8. If the loop finishes without finding a match, output `"NO"`.

### Why it works

The algorithm checks every possible value of the first cube $a^3$. For any valid representation $x=a^3+b^3$, the iteration will eventually reach that particular $a^3$. At that moment, the computed remainder equals $b^3$, which is present in the cube set, so the algorithm answers `"YES"`.

Conversely, whenever the algorithm finds that $x-a^3$ belongs to the cube set, there exists a positive integer $b$ whose cube equals that remainder. The equation $x=a^3+b^3$ is then satisfied, so answering `"YES"` is correct.

Since every possible first cube is examined and the membership test exactly recognizes precomputed cubes, no valid representation can be missed and no invalid representation can be accepted.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10 ** 12

cubes = []
cube_set = set()

i = 1
while i ** 3 <= LIMIT:
    c = i ** 3
    cubes.append(c)
    cube_set.add(c)
    i += 1

t = int(input())

for _ in range(t):
    x = int(input())

    found = False

    for c in cubes:
        if c >= x:
            break

        if x - c in cube_set:
            found = True
            break

    print("YES" if found else "NO")
```

The first section precomputes all cubes up to $10^{12}$. There are only 10,000 of them, so both memory usage and preprocessing time are tiny.

The hash set is the crucial data structure. Without it, checking whether $x-c$ is a cube would require another search, making the solution slower.

Inside each test case, we iterate through every possible first cube. For each one, we compute the remaining amount needed to reach $x$. If that remainder is in the cube set, we have found a valid decomposition.

The condition `if c >= x: break` is a small optimization. Once the current cube is at least $x$, all later cubes are even larger, so the remainder would be zero or negative. Since both integers must be positive, no solution can appear beyond that point.

Python integers automatically handle values larger than 32 bits, so there is no overflow concern even when cubes approach $10^{12}$.

## Worked Examples

### Example 1

Input:

```
35
```

| Current cube $c$ | Remainder $35-c$ | In cube set? |
| --- | --- | --- |
| 1 | 34 | No |
| 8 | 27 | Yes |

The algorithm reaches $c=8=2^3$. The remainder is 27, which equals $3^3$. Since 27 is in the cube set, the answer is `"YES"`.

This example shows how checking a single cube automatically determines the only possible partner cube.

### Example 2

Input:

```
34
```

| Current cube $c$ | Remainder $34-c$ | In cube set? |
| --- | --- | --- |
| 1 | 33 | No |
| 8 | 26 | No |
| 27 | 7 | No |

The next cube would be 64, which exceeds 34, so the loop stops.

No remainder was found in the cube set, so the answer is `"NO"`.

This example demonstrates that every candidate first cube is checked, yet none produces another cube as the remainder.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M)$ per test case | Iterate through all precomputed cubes |
| Space | $O(M)$ | Store cubes and the hash set |

Here $M \approx 10^4$, because $10000^3 = 10^{12}$.

At most 10,000 cube values are examined for each test case. Even with 100 test cases, the total work is only about one million iterations, which comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    LIMIT = 10 ** 12

    cubes = []
    cube_set = set()

    i = 1
    while i ** 3 <= LIMIT:
        c = i ** 3
        cubes.append(c)
        cube_set.add(c)
        i += 1

    t = int(input())
    ans = []

    for _ in range(t):
        x = int(input())

        found = False

        for c in cubes:
            if c >= x:
                break

            if x - c in cube_set:
                found = True
                break

        ans.append("YES" if found else "NO")

    return "\n".join(ans) + "\n"

# provided sample
assert run(
"""7
1
2
4
34
35
16
703657519796
"""
) == """NO
YES
NO
NO
YES
YES
YES
"""

# minimum value
assert run(
"""1
1
"""
) == """NO
"""

# smallest valid representation
assert run(
"""1
2
"""
) == """YES
"""

# equal cubes
assert run(
"""1
16
"""
) == """YES
"""

# large boundary cube sum
assert run(
"""1
2000000000000
"""
) == """YES
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `NO` | Smallest possible value |
| `2` | `YES` | Smallest valid decomposition |
| `16` | `YES` | Case where both cubes are equal |
| `2000000000000` | `YES` | Large values near the cube-root boundary |

## Edge Cases

Consider the input:

```
1
1
```

The algorithm starts with the smallest cube, $1$. Since $1 \ge x$, the loop immediately stops. No valid pair exists because both cubes must be positive. The output is `"NO"`.

Consider the input:

```
1
2
```

The first cube is $1$. The remainder is $2-1=1$. Since 1 is present in the cube set, the algorithm finds the representation $1^3+1^3$ and outputs `"YES"`.

Consider the input:

```
1
16
```

The algorithm checks $1$, then $8$. For $c=8$, the remainder is also $8$. Because the cube set contains 8, the algorithm accepts the decomposition $2^3+2^3$. This confirms that equal cubes are handled naturally.

Consider the input:

```
1
34
```

The algorithm examines every possible first cube less than 34. The remainders are 33, 26, and 7, none of which are cubes. The search ends and the answer is `"NO"`. This verifies that the algorithm does not falsely accept numbers that are close to a valid cube sum but not actually representable.
