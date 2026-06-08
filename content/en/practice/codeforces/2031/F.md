---
title: "CF 2031F - Penchick and Even Medians"
description: "The original problem is interactive: there is a hidden permutation, and we must locate the positions of the two middle values, namely $frac n2$ and $frac n2 + 1$, using median queries. For the hack version used in the archive, the interaction is removed."
date: "2026-06-08T11:53:50+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "interactive", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 2031
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 987 (Div. 2)"
rating: 2800
weight: 2031
solve_time_s: 153
verified: false
draft: false
---

[CF 2031F - Penchick and Even Medians](https://codeforces.com/problemset/problem/2031/F)

**Rating:** 2800  
**Tags:** binary search, constructive algorithms, interactive, probabilities  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

The original problem is interactive: there is a hidden permutation, and we must locate the positions of the two middle values, namely $\frac n2$ and $\frac n2 + 1$, using median queries.

For the hack version used in the archive, the interaction is removed. The entire permutation is given directly in the input.

Each test case contains an even integer $n$ and a permutation of the numbers from $1$ to $n$. We must output the two indices whose values are exactly $\frac n2$ and $\frac n2 + 1$. The order of the two indices does not matter.

The constraints are very small. The sum of all $n$ values over the test file is at most $10^4$. Even an $O(n^2)$ solution would pass comfortably, but the structure of the input allows a direct linear scan.

A common mistake is to output the values instead of their positions.

For example, with

```
n = 6
p = [6, 2, 3, 5, 1, 4]
```

the middle values are $3$ and $4$. Their positions are $3$ and $6$, so the correct output is:

```
3 6
```

not

```
3 4
```

Another easy mistake is forgetting that the permutation is indexed from 1 in the statement, while Python arrays are indexed from 0. If value $3$ appears at `p[2]`, the answer is position `3`.

## Approaches

The brute-force approach is to examine every position and check whether the value equals $\frac n2$ or $\frac n2 + 1$. Since there are only two target values, we can store their positions when we encounter them.

Because the array is already a permutation, each target value appears exactly once. A single scan is sufficient.

The original interactive version requires a sophisticated strategy involving median queries, but none of that survives in the hack format. Once the permutation is given explicitly, the entire task reduces to locating two known values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

In this case the brute-force scan is already optimal.

## Algorithm Walkthrough

1. Read $n$.
2. Read the permutation $p$.
3. Let `a = n // 2` and `b = a + 1`.
4. Scan the permutation from left to right.
5. When value `a` is found, store its 1-based position.
6. When value `b` is found, store its 1-based position.
7. Output the two stored positions.

### Why it works

The permutation contains every integer from $1$ to $n$ exactly once.

The values $\frac n2$ and $\frac n2 + 1$ each occur at exactly one position. During the scan we record those unique positions. Since every element is examined once, both positions are found, and the output is exactly the pair of indices requested by the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        
        x = n // 2
        y = x + 1
        
        pos_x = pos_y = -1
        
        for i, v in enumerate(p, start=1):
            if v == x:
                pos_x = i
            elif v == y:
                pos_y = i
        
        print(pos_x, pos_y)

solve()
```

The code first computes the two target values. Since the permutation property guarantees uniqueness, we only need one variable for each position.

The `enumerate(..., start=1)` call is important. The problem asks for 1-based indices, so using `start=1` avoids an extra conversion later.

The scan visits every element exactly once. Whenever one of the target values is encountered, its position is recorded. After the loop finishes, both positions are known and can be printed immediately.

## Worked Examples

### Example 1

Input permutation:

```
n = 6
p = [6, 2, 3, 5, 1, 4]
```

The target values are $3$ and $4$.

| Position | Value | pos(3) | pos(4) |
| --- | --- | --- | --- |
| 1 | 6 | -1 | -1 |
| 2 | 2 | -1 | -1 |
| 3 | 3 | 3 | -1 |
| 4 | 5 | 3 | -1 |
| 5 | 1 | 3 | -1 |
| 6 | 4 | 3 | 6 |

Output:

```
3 6
```

This example shows the direct interpretation of the task. The values $3$ and $4$ are located at positions $3$ and $6$.

### Example 2

Input permutation:

```
n = 10
p = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```

The target values are $5$ and $6$.

| Position | Value | pos(5) | pos(6) |
| --- | --- | --- | --- |
| 1 | 10 | -1 | -1 |
| 2 | 9 | -1 | -1 |
| 3 | 8 | -1 | -1 |
| 4 | 7 | -1 | -1 |
| 5 | 6 | -1 | 5 |
| 6 | 5 | 6 | 5 |
| 7 | 4 | 6 | 5 |
| 8 | 3 | 6 | 5 |
| 9 | 2 | 6 | 5 |
| 10 | 1 | 6 | 5 |

Output:

```
6 5
```

The order does not matter, so `5 6` would also be accepted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan of the permutation |
| Space | O(1) | Only a few variables are stored |

Since the total sum of $n$ over all test cases is at most $10^4$, a linear scan is far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        a = n // 2
        b = a + 1

        pa = pb = -1

        for i, v in enumerate(p, start=1):
            if v == a:
                pa = i
            elif v == b:
                pb = i

        out.append(f"{pa} {pb}")

    return "\n".join(out)

# sample from statement
assert run(
"""2
6
6 2 3 5 1 4
10
10 9 8 7 6 5 4 3 2 1
"""
) == "3 6\n6 5"

# minimum n
assert run(
"""1
6
1 2 3 4 5 6
"""
) == "3 4"

# reversed minimum n
assert run(
"""1
6
6 5 4 3 2 1
"""
) == "4 3"

# middle values at ends
assert run(
"""1
8
4 1 2 3 5 6 7 8
"""
) == "1 5"

# larger case
assert run(
"""1
12
12 1 2 3 4 5 7 8 9 10 11 6
"""
) == "12 7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 / 1 2 3 4 5 6` | `3 4` | Smallest valid size |
| `6 / 6 5 4 3 2 1` | `4 3` | Reverse order permutation |
| `8 / 4 1 2 3 5 6 7 8` | `1 5` | Targets at extreme positions |
| `12 / 12 1 2 3 4 5 7 8 9 10 11 6` | `12 7` | Larger permutation |

## Edge Cases

Consider the permutation

```
6
6 5 4 3 2 1
```

The target values are $3$ and $4$. They appear at positions $4$ and $3$. A solution that outputs the values themselves would print `3 4`, which is wrong. The scan correctly returns the positions `4 3`.

Consider

```
8
4 1 2 3 5 6 7 8
```

The target values are $4$ and $5$. One appears at the first position and the other at the fifth position. Using zero-based indices by mistake would produce `0 4`. The algorithm uses `enumerate(..., start=1)`, so it outputs the correct answer `1 5`.

Consider

```
10
10 9 8 7 6 5 4 3 2 1
```

The two target values are adjacent in value but not in position. The algorithm does not rely on any ordering assumption. It simply records where each target value occurs and returns `6 5`, which is correct.
