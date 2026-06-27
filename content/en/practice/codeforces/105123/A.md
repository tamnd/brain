---
title: "CF 105123A - Mitosis"
description: "A cell starts with c chromosomes and divides into two daughter cells containing a and b chromosomes. The division is considered correct only if every chromosome ends up in exactly one of the two daughter cells."
date: "2026-06-27T19:31:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105123
codeforces_index: "A"
codeforces_contest_name: "BioCode 2024"
rating: 0
weight: 105123
solve_time_s: 56
verified: true
draft: false
---

[CF 105123A - Mitosis](https://codeforces.com/problemset/problem/105123/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

A cell starts with `c` chromosomes and divides into two daughter cells containing `a` and `b` chromosomes. The division is considered correct only if every chromosome ends up in exactly one of the two daughter cells. That means the total number of chromosomes after the split must be exactly the same as before the split.

The input consists of the three chromosome counts, one for each daughter cell and one for the original cell. The task is simply to determine whether the two daughter counts add up to the original count. If they do, print `"YES"`. Otherwise, print `"NO"`.

The constraints are very small, since every value is between 1 and 100. Even an inefficient algorithm would run instantly. A constant time solution is enough because the answer depends on a single arithmetic comparison.

The main source of mistakes is checking the wrong condition.

Consider the input

```
20 20 40
```

The correct output is

```
YES
```

A careless implementation might compare `a == c` or `b == c`, which would incorrectly reject this valid split.

Another easy mistake is checking only whether one daughter has fewer chromosomes than the original cell. For example,

```
45 93 39
```

The correct output is

```
NO
```

Even though `45` is close to `39`, the total after division is `138`, not `39`, so the split is invalid.

## Approaches

A brute-force way to think about the problem is to simulate the division by counting every chromosome individually. We could imagine assigning each of the `c` chromosomes to one of the two daughter cells and then counting how many each receives. This correctly models mitosis, but it performs work proportional to the number of chromosomes. With the given constraints this would still be acceptable, but it is solving a much harder problem than necessary.

The key observation is that the final arrangement of chromosomes does not matter. The only property that determines whether the split is correct is conservation of the total number of chromosomes. If the daughters contain `a + b` chromosomes altogether, then the split is valid exactly when `a + b == c`.

This reduces the entire problem to one addition and one comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(c) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three integers `a`, `b`, and `c`.
2. Compute the sum `a + b`. This is the total number of chromosomes present after the cell divides.
3. Compare this sum with `c`. A correct mitosis preserves the total number of chromosomes.
4. If `a + b == c`, print `"YES"`. Otherwise, print `"NO"`.

### Why it works

The defining property of a correct mitosis is that every chromosome from the original cell appears in exactly one of the two daughter cells. No chromosome is lost or duplicated. As a result, the total number of chromosomes after division must equal the original number. The algorithm checks exactly this condition, so it accepts every valid split and rejects every invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, c = map(int, input().split())

if a + b == c:
    print("YES")
else:
    print("NO")
```

The program first reads the three integers from the input. Since there is only one test case, no loop is needed.

The comparison `a + b == c` directly matches the definition of a correct mitosis. No special handling is required because all values are positive integers and their maximum value is only 100, so integer overflow is impossible in Python.

The output consists of exactly one word, either `"YES"` or `"NO"`, matching the required format.

## Worked Examples

### Sample 1

Input:

```
45 93 39
```

| Step | a | b | c | a + b | Decision |
| --- | --- | --- | --- | --- | --- |
| Read input | 45 | 93 | 39 | 138 | 138 ≠ 39 |
| Output | 45 | 93 | 39 | 138 | NO |

The daughter cells together contain 138 chromosomes, while the original cell had only 39. Since the totals differ, the split is invalid.

### Sample 2

Input:

```
39 21 60
```

| Step | a | b | c | a + b | Decision |
| --- | --- | --- | --- | --- | --- |
| Read input | 39 | 21 | 60 | 60 | 60 = 60 |
| Output | 39 | 21 | 60 | 60 | YES |

The total number of chromosomes is preserved, so the mitosis is considered correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One addition and one comparison are performed. |
| Space | O(1) | Only three integers are stored. |

The running time and memory usage are constant, independent of the input values. This easily satisfies the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    a, b, c = map(int, input().split())
    print("YES" if a + b == c else "NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out

# provided samples
assert run("45 93 39\n") == "NO\n", "sample 1"
assert run("39 21 60\n") == "YES\n", "sample 2"

# custom cases
assert run("1 1 2\n") == "YES\n", "minimum valid case"
assert run("100 100 100\n") == "NO\n", "maximum values but invalid total"
assert run("50 50 100\n") == "YES\n", "boundary equality"
assert run("1 100 100\n") == "NO\n", "sum exceeds original by one"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 2` | `YES` | Smallest valid chromosome counts |
| `100 100 100` | `NO` | Maximum values with incorrect total |
| `50 50 100` | `YES` | Equality at the boundary |
| `1 100 100` | `NO` | Detects an incorrect sum larger than the original |

## Edge Cases

A common mistake is checking whether one daughter cell has the same number of chromosomes as the original cell instead of checking the total.

For the input

```
20 20 40
```

the algorithm computes `20 + 20 = 40`, compares it with `40`, and prints

```
YES
```

This is correct because the chromosome count is preserved across both daughter cells.

Another mistake is assuming that having one daughter cell close to the original count is sufficient.

For the input

```
45 93 39
```

the algorithm computes `45 + 93 = 138`. Since `138 != 39`, it prints

```
NO
```

The chromosome total increased, which violates the definition of a correct mitosis.
