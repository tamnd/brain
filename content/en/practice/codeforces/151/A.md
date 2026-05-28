---
title: "CF 151A - Soft Drinking"
description: "A group of friends wants to make identical toasts using three resources: soft drink, lime slices, and salt. Every toast consumes a fixed amount of each resource. The task is to determine how many complete toasts each friend can make before at least one resource runs out."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 151
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 107 (Div. 2)"
rating: 800
weight: 151
solve_time_s: 91
verified: true
draft: false
---

[CF 151A - Soft Drinking](https://codeforces.com/problemset/problem/151/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

A group of friends wants to make identical toasts using three resources: soft drink, lime slices, and salt. Every toast consumes a fixed amount of each resource. The task is to determine how many complete toasts each friend can make before at least one resource runs out.

The input gives the number of friends, the number and size of drink bottles, the number of limes and slices per lime, the amount of salt, and the amount of each ingredient needed for one toast. From these values, we must compute how many total toasts can be produced from each resource independently, then determine the limiting resource.

The constraints are tiny, every value is at most 1000. Even an inefficient solution would run comfortably within the limits. There is no need for advanced algorithms, data structures, or optimization tricks. The challenge is simply translating the wording into correct arithmetic.

The most common mistake is misunderstanding what the final answer represents. We are not asked for the total number of toasts. We are asked for how many toasts each friend can make equally.

Consider this input:

```
3 1 3 1 1 100 3 1
```

The drink allows only `1 * 3 / 3 = 1` total toast. A careless solution might print `1`, but that is the total number of toasts for the entire group. Since there are 3 friends, each friend can make `1 / 3 = 0` toasts. The correct output is:

```
0
```

Another subtle case is when one resource is much smaller than the others.

```
5 100 100 1 1 1 1 1
```

The drink and limes are abundant, but there is only enough salt for one toast total. Dividing among 5 friends gives `0`. A solution that forgets to take the minimum across all resources would fail here.

Integer division is also essential. Toasts must be complete. Fractional toasts are not allowed.

```
2 1 5 1 1 100 6 1
```

There are only 5 milliliters of drink, and each toast needs 6 milliliters. The correct number of drink-based toasts is `0`, not `0.833...`.

## Approaches

A brute-force approach would simulate making toasts one at a time. Each step would subtract the required drink, one lime slice, and the required salt until some resource becomes insufficient. At the end, we would divide the number of successful toasts by the number of friends.

This works because every toast consumes fixed amounts of resources. The simulation is easy to reason about and always correct. Even in the worst case, the number of possible toasts is small enough to fit comfortably within time limits.

Still, simulation is unnecessary. The structure of the problem gives a direct mathematical shortcut.

Each resource independently determines a maximum number of total toasts:

The drink provides:

```
(k * l) / nl
```

total toasts.

The limes provide:

```
(c * d)
```

total toasts, because each toast needs exactly one slice.

The salt provides:

```
p / np
```

total toasts.

The actual number of total toasts is the minimum of these three values, because the first exhausted resource stops production. Since every friend must receive the same number of toasts, we divide the total equally among `n` friends.

This reduces the problem to a few arithmetic operations and integer divisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

Here, `T` is the number of simulated toasts.

## Algorithm Walkthrough

1. Read the eight integers from input.
2. Compute the total amount of drink available.

```
total_drink = k * l
```

This converts the number of bottles into total milliliters.

1. Compute how many total toasts the drink can support.

```
drink_toasts = total_drink // nl
```

Integer division is required because partial toasts are invalid.

1. Compute the total number of lime slices.

```
lime_toasts = c * d
```

Each toast consumes exactly one slice, so this value already equals the number of possible toasts from limes.

1. Compute how many total toasts the salt can support.

```
salt_toasts = p // np
```

Again, integer division removes incomplete toasts.

1. Find the smallest among the three toast counts.

```
total_toasts = min(drink_toasts, lime_toasts, salt_toasts)
```

The limiting resource determines the maximum possible number of total toasts.

1. Divide equally among all friends.

```
answer = total_toasts // n
```

1. Print the result.

### Why it works

Every toast consumes fixed amounts of drink, lime, and salt. That means each resource independently imposes an upper bound on the number of total toasts. Any attempt to exceed one of these bounds would require more of that resource than exists.

Taking the minimum of the three bounds gives the maximum feasible number of total toasts. Dividing by the number of friends gives the maximum equal number of toasts per friend. Since all calculations use integer division, the algorithm never counts incomplete toasts.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k, l, c, d, p, nl, np = map(int, input().split())

drink_toasts = (k * l) // nl
lime_toasts = c * d
salt_toasts = p // np

total_toasts = min(drink_toasts, lime_toasts, salt_toasts)

print(total_toasts // n)
```

The first line reads all eight integers in a single statement. Since the problem has only one test case, there is no loop.

The drink calculation multiplies the number of bottles by the milliliters per bottle before dividing by the amount needed per toast. Reversing this order would be incorrect because integer division would lose information too early.

The lime calculation is simpler because each toast needs exactly one slice. No division is required.

The salt calculation uses integer division for the same reason as the drink calculation, incomplete toasts are not allowed.

The `min` call is the key step. Even if two resources can support many toasts, the smallest resource becomes the bottleneck.

Finally, the answer is divided equally among all friends using integer division again. This avoids assigning fractional toasts to people.

## Worked Examples

### Example 1

Input:

```
3 4 5 10 8 100 3 1
```

| Variable | Value |
| --- | --- |
| n | 3 |
| k | 4 |
| l | 5 |
| c | 10 |
| d | 8 |
| p | 100 |
| nl | 3 |
| np | 1 |
| total drink | 20 |
| drink_toasts | 6 |
| lime_toasts | 80 |
| salt_toasts | 100 |
| total_toasts | 6 |
| answer | 2 |

The drink is the limiting resource here. Even though limes and salt are plentiful, only 6 total toasts can be made. Dividing equally among 3 friends gives 2 toasts each.

### Example 2

Input:

```
5 100 100 1 1 1 1 1
```

| Variable | Value |
| --- | --- |
| n | 5 |
| k | 100 |
| l | 100 |
| c | 1 |
| d | 1 |
| p | 1 |
| nl | 1 |
| np | 1 |
| total drink | 10000 |
| drink_toasts | 10000 |
| lime_toasts | 1 |
| salt_toasts | 1 |
| total_toasts | 1 |
| answer | 0 |

This example shows why the final division by `n` matters. The group can make only one total toast, which is not enough for every friend to receive one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No extra memory proportional to input size is used |

The input size is constant, so the running time and memory usage never grow. This easily fits within the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, k, l, c, d, p, nl, np = map(int, input().split())

    drink_toasts = (k * l) // nl
    lime_toasts = c * d
    salt_toasts = p // np

    total_toasts = min(drink_toasts, lime_toasts, salt_toasts)

    print(total_toasts // n)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("3 4 5 10 8 100 3 1\n") == "2\n", "sample 1"

# minimum values
assert run("1 1 1 1 1 1 1 1\n") == "1\n", "minimum case"

# not enough drink for one toast per friend
assert run("3 1 3 1 1 100 3 1\n") == "0\n", "group division case"

# salt is the bottleneck
assert run("5 100 100 100 100 4 1 2\n") == "0\n", "salt bottleneck"

# maximum values
assert run("1000 1000 1000 1000 1000 1000 1 1\n") == "1000\n", "maximum values"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1 1 1 1` | `1` | Minimum valid input |
| `3 1 3 1 1 100 3 1` | `0` | Total toasts must still be divided among friends |
| `5 100 100 100 100 4 1 2` | `0` | Salt can become the limiting resource |
| `1000 1000 1000 1000 1000 1000 1 1` | `1000` | Handles maximum constraints correctly |

## Edge Cases

One easy mistake is forgetting that the answer must be equal for all friends.

Consider:

```
3 1 3 1 1 100 3 1
```

The algorithm computes:

```
drink_toasts = (1 * 3) // 3 = 1
lime_toasts = 1
salt_toasts = 100
```

The minimum is `1`, meaning the group can make one total toast. Dividing equally among 3 friends gives:

```
1 // 3 = 0
```

So the correct answer is:

```
0
```

Another tricky case occurs when one resource is overwhelmingly smaller than the others.

```
5 100 100 1 1 1 1 1
```

The algorithm computes:

```
drink_toasts = 10000
lime_toasts = 1
salt_toasts = 1
```

The minimum is `1`, so the total number of toasts is only one despite the huge amount of drink.

After dividing among 5 friends:

```
1 // 5 = 0
```

The algorithm correctly identifies the bottleneck resource.

Integer division is also critical.

```
2 1 5 1 1 100 6 1
```

The drink calculation becomes:

```
(1 * 5) // 6 = 0
```

Even though 5 milliliters is close to the required 6, it is still insufficient for a complete toast. Because the algorithm uses floor division, it correctly rejects partial toasts and outputs:

```
0
```
