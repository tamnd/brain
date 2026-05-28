---
title: "CF 29A - Spit Problem"
description: "Each camel stands at a unique coordinate on a number line. A camel at position x spits exactly toward position x + d. If another camel stands there, it gets hit. We need to determine whether there exists a pair of camels such that each one hits the other."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 29
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 29 (Div. 2, Codeforces format)"
rating: 1000
weight: 29
solve_time_s: 72
verified: true
draft: false
---
[CF 29A - Spit Problem](https://codeforces.com/problemset/problem/29/A)

**Rating:** 1000  
**Tags:** brute force  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

Each camel stands at a unique coordinate on a number line. A camel at position `x` spits exactly toward position `x + d`. If another camel stands there, it gets hit. We need to determine whether there exists a pair of camels such that each one hits the other.

Suppose camel A stands at `x1` and spits distance `d1`. It targets position `x1 + d1`. Camel B stands at `x2` and spits distance `d2`. The two camels spit at each other if:

```
x1 + d1 = x2
x2 + d2 = x1
```

The input gives the position and spit distance for every camel. The output is `"YES"` if at least one mutual pair exists, otherwise `"NO"`.

The constraints are very small. There are at most 100 camels, so even an algorithm that checks every pair directly is completely fine. A double loop over all pairs performs at most `100 * 100 = 10,000` checks, which is tiny for a 2-second limit. This immediately tells us we do not need sophisticated data structures or optimization tricks.

There are a few easy-to-miss edge cases.

A camel may spit left instead of right because `d` can be negative. For example:

```
2
5 -2
3 2
```

Camel at `5` targets `3`, and camel at `3` targets `5`, so the answer is `"YES"`. A careless solution that assumes all spits go right would fail here.

Another subtle case is when one camel hits another, but the reverse is not true:

```
2
0 2
2 5
```

Camel at `0` hits camel at `2`, but camel at `2` targets `7`. The correct answer is `"NO"`. A buggy implementation might only check whether one camel can hit another, instead of checking mutual targeting.

A third case involves multiple camels where only one pair works:

```
4
0 3
3 -3
10 1
20 -5
```

The correct answer is `"YES"` because the first two camels spit at each other. The algorithm must stop as soon as it finds any valid pair.

## Approaches

The most direct approach is to compare every pair of camels. For each pair `(i, j)`, we check whether camel `i` spits exactly onto camel `j`, and camel `j` spits exactly onto camel `i`.

Formally, if camel `i` is `(xi, di)` and camel `j` is `(xj, dj)`, then they spit at each other when:

```
xi + di = xj
xj + dj = xi
```

This brute-force approach is correct because every possible pair is examined. If a valid pair exists anywhere in the input, we will eventually test it.

The time complexity is `O(n²)` because we inspect all ordered pairs. With `n ≤ 100`, that is at most 10,000 comparisons, which is trivial.

Since the constraints are already tiny, there is no need for a more advanced optimization. We could store camel positions in a hash map and try to search targets faster, but the added complexity gives no practical benefit here. The pairwise solution is already fast, simple, and easy to verify.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Checking | O(n²) | O(1) | Accepted |
| Hash Map Lookup | O(n) average | O(n) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Read the number of camels.
2. Store every camel as a pair `(x, d)` where `x` is the position and `d` is the spit distance.
3. Iterate through all pairs of distinct camels `(i, j)`.
4. For each pair, compute the target positions:

```
camel i targets xi + di
camel j targets xj + dj
```
5. Check whether camel `i` targets camel `j` and camel `j` targets camel `i`.

This means checking:

```
xi + di == xj
xj + dj == xi
```
6. If both conditions are true, immediately print `"YES"` and terminate.

We can stop early because the problem only asks whether at least one such pair exists.
7. If all pairs are checked and none satisfy the condition, print `"NO"`.

### Why it works

The algorithm checks every possible pair of camels exactly once. A pair is accepted only if each camel's spit lands precisely on the other camel's position. Since the definition of "spitting at each other" is exactly these two equations, the algorithm cannot miss a valid pair and cannot incorrectly accept an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
camels = []

for _ in range(n):
    x, d = map(int, input().split())
    camels.append((x, d))

for i in range(n):
    xi, di = camels[i]

    for j in range(i + 1, n):
        xj, dj = camels[j]

        if xi + di == xj and xj + dj == xi:
            print("YES")
            sys.exit()

print("NO")
```

The program begins by reading all camels into a list of `(position, distance)` pairs.

The nested loops iterate over every unique pair. Using `j` from `i + 1` avoids checking the same pair twice and avoids comparing a camel with itself.

Inside the loop, the condition directly matches the mathematical definition of mutual spitting. The first equality checks whether camel `i` hits camel `j`. The second checks the reverse direction.

As soon as a valid pair is found, the program prints `"YES"` and exits immediately. Early termination keeps the implementation simple and avoids unnecessary work.

There are no overflow concerns because Python integers handle these ranges easily. Negative spit distances also work naturally because addition handles both directions on the number line.

## Worked Examples

### Example 1

Input:

```
2
0 1
1 -1
```

| i | j | Camel i `(x,d)` | Camel j `(x,d)` | `xi + di` | `xj + dj` | Mutual? |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | (0, 1) | (1, -1) | 1 | 0 | Yes |

The first camel targets position `1`, which is where the second camel stands. The second camel targets position `0`, where the first camel stands. The algorithm immediately prints `"YES"`.

### Example 2

Input:

```
3
0 2
2 5
10 -3
```

| i | j | Camel i `(x,d)` | Camel j `(x,d)` | `xi + di` | `xj + dj` | Mutual? |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | (0, 2) | (2, 5) | 2 | 7 | No |
| 0 | 2 | (0, 2) | (10, -3) | 2 | 7 | No |
| 1 | 2 | (2, 5) | (10, -3) | 7 | 7 | No |

The first camel hits the second, but the second does not hit back. None of the pairs satisfy both equations simultaneously, so the answer is `"NO"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every pair of camels is checked once |
| Space | O(1) extra | Only a few variables besides the input list |

With at most 100 camels, the quadratic solution performs only about 10,000 pair checks. That is far below the limits, so the solution easily fits within both time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    camels = []

    for _ in range(n):
        x, d = map(int, input().split())
        camels.append((x, d))

    for i in range(n):
        xi, di = camels[i]

        for j in range(i + 1, n):
            xj, dj = camels[j]

            if xi + di == xj and xj + dj == xi:
                return "YES"

    return "NO"

# provided sample
assert run("2\n0 1\n1 -1\n") == "YES", "sample 1"

# minimum size
assert run("1\n0 5\n") == "NO", "single camel"

# one-direction hit only
assert run("2\n0 2\n2 5\n") == "NO", "not mutual"

# negative distances
assert run("2\n5 -2\n3 2\n") == "YES", "left and right spit"

# larger case with one valid pair
assert run(
    "5\n0 3\n3 -3\n10 1\n20 -5\n7 2\n"
) == "YES", "find pair among many"

# no valid pairs
assert run(
    "4\n0 1\n2 1\n4 1\n6 1\n"
) == "NO", "all spit away"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single camel | NO | Cannot form a pair |
| One-direction hit only | NO | Both directions must hold |
| Negative distances | YES | Leftward spits are handled correctly |
| Larger mixed case | YES | Algorithm finds a valid pair among unrelated camels |
| All spits away | NO | No false positives |

## Edge Cases

Consider a case where spits go left:

```
2
5 -2
3 2
```

The algorithm checks the pair:

```
5 + (-2) = 3
3 + 2 = 5
```

Both conditions are true, so it prints `"YES"`. Negative distances work naturally because the computation is just integer addition.

Now consider a one-sided hit:

```
2
0 2
2 5
```

The algorithm computes:

```
0 + 2 = 2
2 + 5 = 7
```

The first condition succeeds, but the second fails. Since both are required simultaneously, the pair is rejected and the final answer becomes `"NO"`.

Finally, consider multiple camels with only one matching pair:

```
4
0 3
3 -3
10 1
20 -5
```

The algorithm tests pairs in order. When it reaches the first two camels:

```
0 + 3 = 3
3 + (-3) = 0
```

The pair satisfies the condition, so the algorithm immediately prints `"YES"` without wasting time checking the remaining pairs.
