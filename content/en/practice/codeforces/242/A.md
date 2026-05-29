---
title: "CF 242A - Heads or Tails"
description: "We know how many times each player flipped a coin. Vasya flipped x times and Petya flipped y times. Every head gives one point, every tail gives nothing. Valera does not remember the exact final scores, but he remembers three facts."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 242
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 149 (Div. 2)"
rating: 1100
weight: 242
solve_time_s: 206
verified: true
draft: false
---

[CF 242A - Heads or Tails](https://codeforces.com/problemset/problem/242/A)

**Rating:** 1100  
**Tags:** brute force, implementation  
**Solve time:** 3m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We know how many times each player flipped a coin. Vasya flipped `x` times and Petya flipped `y` times. Every head gives one point, every tail gives nothing.

Valera does not remember the exact final scores, but he remembers three facts. Vasya got at least `a` heads, Petya got at least `b` heads, and Vasya finished strictly ahead of Petya.

We must print every pair `(c, d)` such that:

- `c` is a possible number of heads for Vasya
- `d` is a possible number of heads for Petya
- `a ≤ c ≤ x`
- `b ≤ d ≤ y`
- `c > d`

The output pairs must appear in lexicographically increasing order. That means smaller `c` comes first, and for equal `c`, smaller `d` comes first.

The constraints are tiny. Every value is at most `100`. Even checking all possible pairs only requires at most `101 × 101 = 10201` iterations, which is completely trivial for a 2 second limit. This immediately suggests a direct brute-force enumeration.

The only real danger in this problem is getting the inequality or iteration ranges wrong.

One easy mistake is allowing draws. Vasya must be the winner, so the condition is strictly `c > d`, not `c ≥ d`.

Consider this input:

```
2 2 1 1
```

Possible scores are:

```
2 1
2 2
1 1
1 2
```

Only `(2, 1)` is valid because Vasya must have more heads than Petya. A careless implementation using `>=` would incorrectly include `(1,1)` and `(2,2)`.

Another subtle case happens when Petya's minimum score is already too large for most Vasya scores.

Example:

```
3 5 1 4
```

Petya always has at least `4` heads. Vasya can have at most `3`. No valid outcome exists, so the correct output is:

```
0
```

A careless solution that blindly prints all pairs in range without checking the winner condition would fail here.

Ordering is also important. The pairs must already be sorted lexicographically. If we iterate `c` from small to large, and for each `c` iterate `d` from small to large, the generated order automatically satisfies the requirement.

## Approaches

The most straightforward approach is to try every possible final score pair.

Vasya's score can range from `a` to `x`. Petya's score can range from `b` to `y`. For every pair `(c, d)` in these ranges, we check whether `c > d`. If yes, we store the pair.

This brute-force method is correct because every valid game outcome corresponds to exactly one pair inside these bounds, and every pair we output satisfies all conditions from the statement.

The brute-force approach already fits comfortably within the limits. At worst, we test about ten thousand pairs, which is negligible.

There is no hidden optimization trick here because the search space is already extremely small. The real observation is recognizing that the constraints are intentionally tiny, so a direct implementation is the intended solution. Trying to derive formulas or complicated pruning only makes the code harder to read without improving performance in any meaningful way.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O((x - a + 1)(y - b + 1)) | O(number of answers) | Accepted |
| Optimized Mathematical Derivation | O(number of answers) | O(number of answers) | Unnecessary |

## Algorithm Walkthrough

1. Read the four integers `x`, `y`, `a`, and `b`.
2. Create an empty list `ans` to store all valid score pairs.
3. Iterate Vasya's possible score `c` from `a` to `x`.

These are all values consistent with Valera's memory that Vasya scored at least `a` heads and cannot exceed the number of flips.
4. For each `c`, iterate Petya's possible score `d` from `b` to `y`.

These are all values consistent with Petya's remembered lower bound.
5. Check whether `c > d`.

Vasya must strictly win the game. Equal scores correspond to a draw and must not be included.
6. If the condition holds, append `(c, d)` to the answer list.
7. Print the number of stored pairs.
8. Print every pair in the order they were generated.

Because `c` increases first and `d` increases second, the output is automatically lexicographically sorted.

### Why it works

The algorithm examines every possible score pair that satisfies the remembered lower bounds and the physical limits imposed by the number of coin tosses.

For each pair, it checks the exact winning condition from the problem. No valid pair can be missed because every feasible outcome appears somewhere in the nested loops. No invalid pair can be printed because we only add pairs where Vasya's score is strictly larger than Petya's.

The iteration order guarantees lexicographical ordering automatically.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, y, a, b = map(int, input().split())

    ans = []

    for c in range(a, x + 1):
        for d in range(b, y + 1):
            if c > d:
                ans.append((c, d))

    print(len(ans))

    for c, d in ans:
        print(c, d)

solve()
```

The program directly follows the algorithm described above.

The outer loop iterates through all possible scores for Vasya. The inner loop iterates through all possible scores for Petya. The condition `c > d` exactly matches the requirement that Vasya wins.

The ranges use `x + 1` and `y + 1` because Python's `range` excludes the upper endpoint. Forgetting the `+1` would incorrectly skip the maximum possible score.

The answers are stored before printing because the first output line must contain the total number of valid pairs. We only know that count after enumeration finishes.

The ordering requirement is handled naturally by the loop structure. Since `c` increases monotonically, and `d` increases monotonically for each fixed `c`, the produced sequence is already sorted correctly.

## Worked Examples

### Example 1

Input:

```
3 2 1 1
```

### Trace

| c | d | c > d | Added to answer |
| --- | --- | --- | --- |
| 1 | 1 | No | No |
| 1 | 2 | No | No |
| 2 | 1 | Yes | (2, 1) |
| 2 | 2 | No | No |
| 3 | 1 | Yes | (3, 1) |
| 3 | 2 | Yes | (3, 2) |

Final answer list:

```
(2, 1)
(3, 1)
(3, 2)
```

Output:

```
3
2 1
3 1
3 2
```

This example shows the strict inequality clearly. Pairs with equal scores are rejected because they represent draws.

### Example 2

Input:

```
3 5 1 4
```

### Trace

| c | d | c > d | Added to answer |
| --- | --- | --- | --- |
| 1 | 4 | No | No |
| 1 | 5 | No | No |
| 2 | 4 | No | No |
| 2 | 5 | No | No |
| 3 | 4 | No | No |
| 3 | 5 | No | No |

Final answer list is empty.

Output:

```
0
```

This example demonstrates the case where Petya's minimum remembered score already prevents Vasya from winning in every scenario.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((x - a + 1)(y - b + 1)) | We check every possible pair once |
| Space | O(k) | `k` is the number of valid pairs stored |

Since all values are at most `100`, the total number of iterations is at most about ten thousand. This is tiny compared to the time limit, so the solution easily fits within both time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    x, y, a, b = map(int, input().split())

    ans = []

    for c in range(a, x + 1):
        for d in range(b, y + 1):
            if c > d:
                ans.append((c, d))

    out = [str(len(ans))]

    for c, d in ans:
        out.append(f"{c} {d}")

    print("\n".join(out))

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
assert run("3 2 1 1\n") == (
    "3\n"
    "2 1\n"
    "3 1\n"
    "3 2\n"
), "sample 1"

# minimum-size input
assert run("1 1 1 1\n") == (
    "0\n"
), "minimum case"

# exactly one valid pair
assert run("2 1 2 1\n") == (
    "1\n"
    "2 1\n"
), "single valid answer"

# no valid outcomes
assert run("3 5 1 4\n") == (
    "0\n"
), "Petya always ahead or tied"

# boundary ordering check
assert run("3 3 1 1\n") == (
    "3\n"
    "2 1\n"
    "3 1\n"
    "3 2\n"
), "lexicographical order"

# maximum-size style case
out = run("100 100 100 100\n")
assert out == "0\n", "largest equal bounds"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `0` | Minimum constraints and strict inequality |
| `2 1 2 1` | One pair `(2,1)` | Exact boundary inclusion |
| `3 5 1 4` | `0` | No valid outcomes exist |
| `3 3 1 1` | Ordered valid pairs | Lexicographical ordering |
| `100 100 100 100` | `0` | Maximum boundary values |

## Edge Cases

Consider the smallest possible input:

```
1 1 1 1
```

The algorithm checks only one pair:

| c | d | c > d |
| --- | --- | --- |
| 1 | 1 | No |

Since the condition fails, the answer list stays empty and the program prints:

```
0
```

This correctly handles the draw case.

Now consider a situation where Petya's minimum remembered score is already too high:

```
3 5 1 4
```

The outer loop produces `c = 1, 2, 3`. The inner loop produces `d = 4, 5`. Every comparison fails because `c` is never larger than `d`.

The algorithm correctly prints no valid outcomes.

Finally, consider an ordering-sensitive example:

```
4 3 2 1
```

Generated valid pairs are:

```
2 1
3 1
3 2
4 1
4 2
4 3
```

The nested loops naturally produce lexicographical order because `c` increases first, then `d`. No additional sorting step is required.
