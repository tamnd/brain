---
title: "CF 124A - The number of positions"
description: "Petr is standing somewhere in a line containing n people. Positions are numbered from 1 at the front to n at the back. He knows two things about his position. At least a people are standing in front of him, and at most b people are standing behind him."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 124
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 92 (Div. 2 Only)"
rating: 1000
weight: 124
solve_time_s: 87
verified: true
draft: false
---

[CF 124A - The number of positions](https://codeforces.com/problemset/problem/124/A)

**Rating:** 1000  
**Tags:** math  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

Petr is standing somewhere in a line containing `n` people. Positions are numbered from `1` at the front to `n` at the back.

He knows two things about his position. At least `a` people are standing in front of him, and at most `b` people are standing behind him. We must count how many different positions satisfy both conditions.

If Petr stands at position `p`, then exactly `p - 1` people are in front of him and exactly `n - p` people are behind him. The task becomes finding how many integers `p` satisfy both inequalities:

- `p - 1 >= a`
- `n - p <= b`

The constraints are tiny, since `n <= 100`. Even a brute-force loop over every position is fast enough. There is no need for advanced optimization, data structures, or dynamic programming. The main challenge is translating the wording into correct inequalities without making off-by-one mistakes.

The most common mistake is misunderstanding the phrase "no less than `a` people in front". This means `at least a`, not exactly `a`.

Consider this example:

```
5 2 1
```

Valid positions are `3` and `4`.

Position `5` is invalid because there are `0` people behind Petr, which is allowed, but there are `4` people in front, which is also allowed. Actually position `5` is valid too. A careless implementation that assumes exactly `a` people in front would incorrectly return only one position.

Another subtle edge case appears when `b = 0`.

Example:

```
4 1 0
```

Petr must stand at the very back because nobody can stand behind him. The only valid position is `4`. A wrong interpretation such as `behind < b` instead of `behind <= b` would reject the correct answer.

There is also an easy off-by-one trap when converting between positions and counts.

Example:

```
3 0 2
```

All positions are valid. Position `1` has `0` people in front and `2` behind. Position `3` has `2` in front and `0` behind. Forgetting that position numbering starts from `1` often breaks these boundary cases.

## Approaches

The brute-force approach directly tests every possible position from `1` to `n`.

For each position `p`, we compute:

- people in front = `p - 1`
- people behind = `n - p`

If both conditions hold, we increment the answer.

This works because the constraints are extremely small. At worst we check `100` positions, which is effectively instantaneous.

The interesting part is recognizing that we can derive the answer mathematically without iterating.

From:

```
p - 1 >= a
```

we get:

```
p >= a + 1
```

From:

```
n - p <= b
```

we get:

```
p >= n - b
```

So Petr's position must satisfy both lower bounds simultaneously:

```
p >= max(a + 1, n - b)
```

The largest possible position is always `n`, so every valid position lies in:

```
[max(a + 1, n - b), n]
```

The number of integers in this interval is:

```
n - max(a + 1, n - b) + 1
```

This simplifies to the well-known compact formula:

```
min(n - a, b + 1)
```

Both methods are fully acceptable here. The formula is cleaner and constant time, while brute force is easier to derive initially.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n`, `a`, and `b`.
2. Petr must have at least `a` people in front of him.

Since position `p` has `p - 1` people in front, the smallest valid position is `a + 1`.
3. Petr must have at most `b` people behind him.

Since position `p` has `n - p` people behind, we solve:

```
n - p <= b
```

which gives:

```
p >= n - b
```
4. The stricter of these two lower bounds determines the first valid position:

```
start = max(a + 1, n - b)
```
5. Every position from `start` through `n` is valid.

Count them using interval length:

```
answer = n - start + 1
```
6. Print the answer.

### Why it works

A position is valid if and only if it satisfies both constraints simultaneously.

The first condition excludes positions too close to the front. The second excludes positions too far toward the front as well, because too many people would remain behind Petr.

After converting both statements into inequalities on `p`, every valid position forms one continuous interval ending at `n`. Counting the integers in that interval gives exactly the number of legal positions, neither missing nor adding any cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, a, b = map(int, input().split())

start = max(a + 1, n - b)
answer = n - start + 1

print(answer)
```

The program directly follows the mathematical derivation from the walkthrough.

The expression `a + 1` is the first position that has at least `a` people in front. This is the most common place to make an off-by-one mistake. Position `a` would only have `a - 1` people in front.

The expression `n - b` comes from rearranging the condition on people behind Petr. Another frequent mistake is writing `n - b + 1`, which incorrectly shifts the interval.

Finally, `n - start + 1` computes the size of an inclusive interval. The `+1` matters because both endpoints count as valid positions.

## Worked Examples

### Example 1

Input:

```
3 1 1
```

| Variable | Value |
| --- | --- |
| n | 3 |
| a | 1 |
| b | 1 |
| a + 1 | 2 |
| n - b | 2 |
| start | 2 |
| answer | 2 |

Valid positions are `2` and `3`.

This example shows that the answer counts every position from the computed lower bound through the end of the line.

### Example 2

Input:

```
5 2 3
```

| Variable | Value |
| --- | --- |
| n | 5 |
| a | 2 |
| b | 3 |
| a + 1 | 3 |
| n - b | 2 |
| start | 3 |
| answer | 3 |

Valid positions are `3`, `4`, and `5`.

This trace demonstrates that the stricter lower bound controls the answer. Even though `n - b = 2`, Petr still cannot stand before position `3` because he needs at least two people in front.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

The constraints are extremely small, but the solution is constant time anyway. It easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    n, a, b = map(int, input().split())

    start = max(a + 1, n - b)
    answer = n - start + 1

    print(answer)

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
assert run("3 1 1\n") == "2\n", "sample 1"

# custom cases
assert run("1 0 0\n") == "1\n", "single person line"
assert run("4 1 0\n") == "1\n", "must stand last"
assert run("5 0 4\n") == "5\n", "all positions valid"
assert run("100 99 99\n") == "1\n", "maximum boundary"
assert run("6 2 2\n") == "3\n", "middle interval"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0` | `1` | Minimum-size input |
| `4 1 0` | `1` | Boundary case where nobody can stand behind Petr |
| `5 0 4` | `5` | Every position is valid |
| `100 99 99` | `1` | Maximum values with only one valid position |
| `6 2 2` | `3` | Correct interval counting in the middle range |

## Edge Cases

Consider the input:

```
4 1 0
```

The algorithm computes:

```
a + 1 = 2
n - b = 4
start = 4
answer = 1
```

Only position `4` works because Petr cannot have anyone behind him. The algorithm correctly handles the inclusive condition `<= b`.

Now consider:

```
5 0 4
```

We get:

```
a + 1 = 1
n - b = 1
start = 1
answer = 5
```

Every position is valid. This confirms the formula handles the full-range case correctly.

Finally, consider:

```
3 0 2
```

The computation becomes:

```
a + 1 = 1
n - b = 1
start = 1
answer = 3
```

All three positions are counted. This case verifies that the conversion between positions and counts of people in front is handled without off-by-one errors.
