---
title: "CF 1877A - Goals of Victory"
description: "We have a round-robin football tournament with $n$ teams. Every pair of teams plays exactly one match. For each team, its efficiency is defined as: $$text{goals scored} - text{goals conceded}$$ After the tournament finishes, the efficiencies of all teams are computed."
date: "2026-06-08T22:55:11+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1877
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 902 (Div. 2, based on COMPFEST 15 - Final Round)"
rating: 800
weight: 1877
solve_time_s: 92
verified: true
draft: false
---

[CF 1877A - Goals of Victory](https://codeforces.com/problemset/problem/1877/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a round-robin football tournament with $n$ teams. Every pair of teams plays exactly one match.

For each team, its efficiency is defined as:

$$\text{goals scored} - \text{goals conceded}$$

After the tournament finishes, the efficiencies of all teams are computed. One team's efficiency is lost, and we are given the efficiencies of the remaining $n-1$ teams. The task is to determine the missing efficiency.

The constraints are extremely small. There are at most 500 test cases and at most 100 teams per test case. Even an $O(n^2)$ solution would be trivial here. The real challenge is recognizing the mathematical property that uniquely determines the missing value.

A common mistake is to think we need to reconstruct match results. The statement even provides one possible tournament, which may tempt us into modeling matches. That is unnecessary because the missing efficiency can be derived directly from a global invariant.

Consider a simple example:

```
n = 2
known efficiencies = [5]
```

There is only one match. If one team has efficiency $+5$, the other must have efficiency $-5$. The answer is:

```
-5
```

Another easy-to-miss case is when efficiencies are negative:

```
n = 3
known efficiencies = [-3, -7]
```

The correct answer is:

```
10
```

A careless implementation that takes the absolute value or assumes efficiencies are non-negative would fail.

A third edge case is when all known efficiencies are zero:

```
n = 4
known efficiencies = [0, 0, 0]
```

The missing efficiency is also:

```
0
```

The invariant used by the solution still holds perfectly.

## Approaches

A brute-force mindset starts by trying to reconstruct the tournament. Since every efficiency depends on many matches, we might attempt to infer scores that satisfy the given values and then derive the missing team's efficiency.

This approach quickly becomes impractical. A round-robin tournament contains

$$\frac{n(n-1)}{2}$$

matches, and each match may have many possible score combinations. Searching through possible tournaments is completely unnecessary.

The key observation comes from looking at how efficiencies are formed.

For any match, suppose Team A scores $x$ goals and Team B scores $y$ goals.

Team A contributes:

$$x-y$$

to its efficiency.

Team B contributes:

$$y-x$$

to its efficiency.

Adding these contributions gives:

$$(x-y)+(y-x)=0$$

Every match contributes zero to the sum of all teams' efficiencies. Since the tournament is just a collection of matches, the total efficiency across all teams must also be zero.

If the efficiencies are:

$$e_1,e_2,\dots,e_n$$

then

$$e_1+e_2+\cdots+e_n=0$$

We are given $n-1$ of them. If their sum is $S$, then the missing efficiency must be:

$$-S$$

This reduces the entire problem to summing the given numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force reconstruction | Exponential | Exponential | Too slow |
| Sum invariant | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read $n$.
3. Read the $n-1$ known efficiencies.
4. Compute their sum $S$.
5. Output $-S$.

The reason step 5 works is that the sum of efficiencies of all teams in a tournament is always zero. The missing value must exactly cancel the sum of the known values.

### Why it works

Every match contributes opposite values to the two participating teams. If one team gains $x-y$, the other gains $y-x$. The total contribution of that match to the global efficiency sum is zero.

Since every match contributes zero, the sum of efficiencies of all teams after the entire tournament is also zero. Let the missing efficiency be $m$. If the known efficiencies sum to $S$, then:

$$S + m = 0$$

which implies:

$$m = -S$$

The algorithm computes exactly this value, so it is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(-sum(a))
```

The implementation follows the mathematical observation directly.

The variable `a` stores the $n-1$ known efficiencies. Their sum is computed with Python's built-in `sum()` function. Since the total efficiency of all teams must equal zero, the missing efficiency is simply the negative of that sum.

There are no tricky boundary conditions. Negative values, positive values, and zeros are all handled naturally. Integer overflow is not a concern in Python, and even in fixed-width languages the values remain very small under the given constraints.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [3, -4, 5]
```

| Step | Value |
| --- | --- |
| Read efficiencies | [3, -4, 5] |
| Compute sum S | 4 |
| Missing efficiency | -4 |

Output:

```
-4
```

The known efficiencies add up to 4. Since the total must be 0, the missing team must contribute -4.

### Example 2

Input:

```
n = 11
a = [-30, 12, -57, 7, 0, -81, -68, 41, -89, 0]
```

| Step | Value |
| --- | --- |
| Read efficiencies | given list |
| Compute sum S | -265 |
| Missing efficiency | 265 |

Output:

```
265
```

This example demonstrates that large negative totals are handled exactly the same way. The missing value simply cancels the accumulated sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Sum the $n-1$ efficiencies once |
| Space | O(1) | Only a few variables besides the input list |

With $n \le 100$ and at most 500 test cases, the total amount of work is tiny. The solution runs comfortably within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans.append(str(-sum(a)))

    sys.stdout.write("\n".join(ans))

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
assert run(
"""2
4
3 -4 5
11
-30 12 -57 7 0 -81 -68 41 -89 0
"""
) == """-4
265"""

# minimum size
assert run(
"""1
2
5
"""
) == """-5"""

# all zeros
assert run(
"""1
4
0 0 0
"""
) == """0"""

# all equal values
assert run(
"""1
5
7 7 7 7
"""
) == """-28"""

# mixed positive and negative
assert run(
"""1
3
-3 -7
"""
) == """10"""

# boundary-style values
assert run(
"""1
4
100 -100 100
"""
) == """-100"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2, [5]` | `-5` | Minimum valid tournament |
| `n=4, [0,0,0]` | `0` | Zero-sum case |
| `n=5, [7,7,7,7]` | `-28` | All equal values |
| `n=3, [-3,-7]` | `10` | Negative efficiencies |
| `n=4, [100,-100,100]` | `-100` | Positive and negative cancellation |

## Edge Cases

Consider the minimum-size tournament:

```
1
2
5
```

The algorithm computes:

```
S = 5
answer = -5
```

There is only one match, so the two teams' efficiencies must be opposites. The output is correct.

Consider all-zero efficiencies:

```
1
4
0 0 0
```

The algorithm computes:

```
S = 0
answer = 0
```

Since the total efficiency must be zero, the missing value is also zero.

Consider negative values:

```
1
3
-3 -7
```

The algorithm computes:

```
S = -10
answer = 10
```

The invariant does not depend on signs. The missing efficiency simply balances the total back to zero.

Consider a cancellation-heavy input:

```
1
4
100 -100 100
```

The algorithm computes:

```
S = 100
answer = -100
```

Even though some values cancel each other, the remaining total determines the missing efficiency uniquely. The output is correct because the overall sum becomes zero.
