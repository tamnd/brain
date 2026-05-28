---
title: "CF 131C - The World is a Theatre"
description: "We have a theatre club with n boys and m girls. A performance group must contain exactly t people, with two extra restrictions: at least 4 of them must be boys, and at least 1 must be a girl. The task is to count how many different valid groups can be formed."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 131
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 95 (Div. 2)"
rating: 1400
weight: 131
solve_time_s: 95
verified: true
draft: false
---

[CF 131C - The World is a Theatre](https://codeforces.com/problemset/problem/131/C)

**Rating:** 1400  
**Tags:** combinatorics, math  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a theatre club with `n` boys and `m` girls. A performance group must contain exactly `t` people, with two extra restrictions: at least 4 of them must be boys, and at least 1 must be a girl.

The task is to count how many different valid groups can be formed. Two groups are considered different if at least one selected person differs.

The constraints are very small. Both `n` and `m` are at most 30, so even fairly expensive combinatorial computations are safe. The answer also fits inside a 64-bit integer, which means we can directly compute combinations without modular arithmetic.

The key observation from the constraints is that we do not need advanced optimization techniques. The number of possible boy counts is tiny, because the chosen group has size `t`, and boys must contribute at least 4 members. We can simply try every feasible split between boys and girls.

There are a few edge cases that can easily produce wrong answers if the iteration bounds are careless.

Consider this input:

```
4 10 5
```

The only valid composition is 4 boys and 1 girl. The correct answer is:

```
40
```

A buggy loop that starts boys from 0 instead of 4 would count many invalid teams.

Another tricky case is when there are not enough girls available for a particular split.

```
10 1 8
```

The only valid composition is 7 boys and 1 girl. Choosing 6 boys and 2 girls is impossible because only one girl exists. A careless implementation that blindly computes combinations for all splits may attempt invalid values such as `C(1, 2)`.

One more subtle case appears when `t` is close to `n + m`.

```
4 1 5
```

There is exactly one valid group: everybody must be selected.

A loop with incorrect upper bounds might accidentally skip the case where all boys are chosen.

## Approaches

The brute-force idea is straightforward. We could enumerate every subset of people and check whether its size is exactly `t`, whether it contains at least 4 boys, and whether it contains at least 1 girl.

This works because every valid troupe corresponds to exactly one subset. The problem is the number of subsets. In the worst case there are 60 people total, which means `2^60` subsets. That is astronomically large, far beyond what can run in 2 seconds.

The structure of the problem gives a much better direction. We do not actually care about the identities during enumeration, only about how many boys and girls are selected.

Suppose we decide that the group contains exactly `b` boys. Then the number of girls is forced to be `t - b`.

For this fixed split:

```
ways = C(n, b) * C(m, t - b)
```

because we independently choose `b` boys from `n` and `t - b` girls from `m`.

The only remaining task is to iterate over every valid value of `b`.

The brute-force approach fails because it treats every subset separately. The combinatorial approach groups huge numbers of subsets together by composition. Instead of examining individual groups, we count all groups of one structure at once.

Since there are at most 30 possible values to try, this solution is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n+m)) | O(1) | Too slow |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and `t`.
2. Iterate over the number of selected boys, call it `boys`.
3. The minimum valid number of boys is 4, because the statement requires at least 4 boys.
4. The maximum valid number of boys is `min(n, t - 1)`.

We cannot choose more than `n` boys, and we must leave room for at least one girl.
5. For each valid `boys` value, compute:

```
girls = t - boys
```
6. Count the number of ways to choose these people:

```
C(n, boys) * C(m, girls)
```
7. Add this value to the answer.
8. Print the final answer.

### Why it works

Every valid troupe has a unique number of selected boys. When we iterate through all feasible boy counts, every valid troupe appears in exactly one iteration.

For a fixed split `(boys, girls)`, the choices are independent. We first choose which boys participate, then choose which girls participate. Multiplying the two combination counts gives the exact number of troupes with that composition.

Since the loop covers all valid compositions and no composition overlaps with another, the final sum counts every valid troupe exactly once.

## Python Solution

```python
import sys
from math import comb

input = sys.stdin.readline

n, m, t = map(int, input().split())

answer = 0

for boys in range(4, min(n, t - 1) + 1):
    girls = t - boys
    
    if 1 <= girls <= m:
        answer += comb(n, boys) * comb(m, girls)

print(answer)
```

The solution directly follows the combinatorial reasoning.

The loop starts from 4 because fewer boys would violate the rules. The upper bound is `min(n, t - 1)` because we cannot select more boys than exist, and selecting all `t` people as boys would leave zero girls.

The check:

```
if 1 <= girls <= m:
```

protects against invalid girl counts. Without this condition, we could attempt impossible selections such as choosing 5 girls when only 2 exist.

Python's `math.comb` computes exact binomial coefficients efficiently and safely handles the required range. Since the answer fits in 64-bit integer range, overflow is not an issue.

## Worked Examples

### Example 1

Input:

```
5 2 5
```

Possible valid splits are:

| Boys | Girls | C(5, Boys) | C(2, Girls) | Contribution |
| --- | --- | --- | --- | --- |
| 4 | 1 | 5 | 2 | 10 |

Total answer:

```
10
```

This example shows the simplest nontrivial case. Only one composition is possible because selecting 5 people with at least 4 boys and at least 1 girl forces exactly 4 boys and 1 girl.

### Example 2

Input:

```
6 3 7
```

Valid splits:

| Boys | Girls | C(6, Boys) | C(3, Girls) | Contribution |
| --- | --- | --- | --- | --- |
| 4 | 3 | 15 | 1 | 15 |
| 5 | 2 | 6 | 3 | 18 |
| 6 | 1 | 1 | 3 | 3 |

Final answer:

```
36
```

This trace demonstrates how multiple valid compositions contribute independently. Each row counts groups with a fixed boy-girl distribution, and the total is the sum of all distributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | We iterate through all feasible boy counts once |
| Space | O(1) | Only a few integer variables are stored |

The maximum value of `t` is at most 60, so the loop performs only a tiny number of iterations. The solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from math import comb

def solve():
    input = sys.stdin.readline
    
    n, m, t = map(int, input().split())
    
    ans = 0
    
    for boys in range(4, min(n, t - 1) + 1):
        girls = t - boys
        
        if 1 <= girls <= m:
            ans += comb(n, boys) * comb(m, girls)
    
    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    
    solve()
    
    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
assert run("5 2 5\n") == "10", "sample 1"

# minimum valid configuration
assert run("4 1 5\n") == "1", "minimum sizes"

# only one possible girl count
assert run("10 1 8\n") == str(comb(10, 7)), "single girl available"

# multiple valid splits
assert run("6 3 7\n") == "36", "multiple compositions"

# larger boundary-style case
assert run("30 30 30\n") == str(
    sum(comb(30, b) * comb(30, 30 - b)
        for b in range(4, 30))
), "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 1 5` | `1` | Exact boundary where everyone must be chosen |
| `10 1 8` | `120` | Cases with only one possible girl count |
| `6 3 7` | `36` | Multiple valid compositions |
| `30 30 30` | Computed value | Large combinatorial values near limits |

## Edge Cases

Consider the input:

```
4 10 5
```

The algorithm iterates over boy counts starting from 4. The only valid split is:

```
boys = 4
girls = 1
```

The computation becomes:

```
C(4,4) * C(10,1) = 1 * 10 = 10
```

No invalid cases with fewer than 4 boys are considered.

Now examine:

```
10 1 8
```

The loop checks:

| Boys | Girls | Valid? |
| --- | --- | --- |
| 4 | 4 | No |
| 5 | 3 | No |
| 6 | 2 | No |
| 7 | 1 | Yes |

Only the final row satisfies `girls <= m`. The answer becomes:

```
C(10,7) * C(1,1) = 120
```

This confirms the importance of validating the girl count before adding combinations.

Finally, consider:

```
4 1 5
```

The loop range is:

```
range(4, min(4, 4) + 1)
```

which includes exactly one value:

```
boys = 4
girls = 1
```

The algorithm correctly counts the single troupe containing everyone.
