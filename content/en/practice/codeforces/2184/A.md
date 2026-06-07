---
title: "CF 2184A - Social Experiment"
description: "We have $n$ people. They must be partitioned into teams, where every team has either 2 or 3 members. After the teams are formed, each team independently chooses one of two civilizations."
date: "2026-06-07T21:36:15+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2184
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1072 (Div. 3)"
rating: 800
weight: 2184
solve_time_s: 108
verified: true
draft: false
---

[CF 2184A - Social Experiment](https://codeforces.com/problemset/problem/2184/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have $n$ people. They must be partitioned into teams, where every team has either 2 or 3 members. After the teams are formed, each team independently chooses one of two civilizations.

The number of people assigned to a civilization is the sum of the sizes of all teams that chose it. We want to arrange both the team sizes and the civilization choices so that the difference between the two civilization populations is as small as possible.

For each test case, we are given only the value $n$, and we must output the minimum achievable difference.

The constraints are very small. There are up to $10^4$ test cases and each $n$ is at most $10^4$. Even a simple $O(n)$ solution per test case would pass comfortably. Still, the structure of the problem allows an $O(1)$ solution.

The tricky part is realizing that teams, not individual people, choose civilizations. We cannot arbitrarily distribute people between the two civilizations. Every team contributes either 2 or 3 people at once.

Consider $n=2$. There is only one team of size 2. One civilization gets 2 people and the other gets 0, so the answer is 2. A careless approach might assume we can split people individually and incorrectly return 0.

Consider $n=5$. We can form teams of sizes 2 and 3. Assign the size-2 team to one civilization and the size-3 team to the other. The difference is 1. Any solution that only checks whether $n$ is even or odd would miss this.

Consider $n=7$. One valid partition is $2+2+3$. The civilization totals can become $5$ and $2$, giving difference $3$, or $4$ and $3$, giving difference $1$. The ability to choose civilization assignments after forming teams is essential.

## Approaches

A brute-force approach would enumerate all ways to represent $n$ as a sum of 2s and 3s. For each representation, it would try all possible assignments of teams to the two civilizations and record the minimum difference.

This works because every valid solution corresponds to some team decomposition and some assignment of teams. The problem is that the number of decompositions and assignments grows exponentially. Even for moderate values of $n$, exploring all possibilities becomes impractical.

The key observation is that team sizes are only 2 and 3. Since

$$3 - 2 = 1,$$

we can construct totals very flexibly. The only thing that matters is the remainder of $n$ modulo 2.

If $n$ is even, we can always split the people equally between the two civilizations. One simple construction is to form only teams of size 2. Then each civilization can receive exactly half of the teams. The difference becomes 0.

If $n$ is odd, an equal split is impossible because the civilization populations must sum to an odd number. The best possible difference is at least 1.

The next question is whether difference 1 is always achievable for odd $n$.

For every odd $n \ge 5$, we can write

$$n = 3 + 2k.$$

Create one team of size 3 and $k$ teams of size 2. Since the remaining $2k$ people form an even total, we can split those evenly. The extra team of size 3 contributes one more person to one civilization than the other, producing difference exactly 1.

The only odd value that does not fit this construction is $n=3$. With a single team of size 3, one civilization gets all 3 people and the other gets 0, so the difference is 3.

This completely determines the answer:

- $n=3$ gives 3.
- Any other odd $n$ gives 1.
- Any even $n$ gives 0, except $n=2$, which gives 2.

These cases can be written more compactly as $n \bmod 2$, except for the special values $2$ and $3$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $n$.
2. If $n=2$, output 2.

There is only one team of size 2, so one civilization receives all people.
3. Otherwise, if $n=3$, output 3.

There is only one team of size 3, so one civilization receives all people.
4. Otherwise, output $n \bmod 2$.

If $n$ is even, a perfect split exists and the answer is 0.

If $n$ is odd and at least 5, a split with difference 1 exists, and a smaller difference is impossible because the total population is odd.

### Why it works

For even $n$, forming only size-2 teams allows the total population to be divided equally between the two civilizations, so the minimum difference is 0.

For odd $n \ge 5$, write $n=3+2k$. Assign the size-3 team to one side and split the size-2 teams evenly. The civilization populations differ by exactly 1. Since the total population is odd, a difference of 0 cannot exist.

The cases $n=2$ and $n=3$ are exceptional because only one team can be formed. One civilization receives everyone and the other receives nobody.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

ans = []
for _ in range(t):
    n = int(input())

    if n == 2:
        ans.append("2")
    elif n == 3:
        ans.append("3")
    else:
        ans.append(str(n % 2))

sys.stdout.write("\n".join(ans))
```

The first two conditions handle the only exceptional values. For $n=2$ and $n=3$, there is exactly one team, so the difference equals the team size itself.

For every larger value, parity completely determines the answer. Even values return 0 because an equal split is possible. Odd values return 1 because the total population is odd, ruling out difference 0, and the construction using one size-3 team achieves difference 1.

No arithmetic overflow concerns exist because all values are tiny. The implementation performs only a few constant-time operations per test case.

## Worked Examples

### Example 1

Input:

```
5
2
3
5
8
11
```

| n | Special Case? | n % 2 | Answer |
| --- | --- | --- | --- |
| 2 | Yes | 0 | 2 |
| 3 | Yes | 1 | 3 |
| 5 | No | 1 | 1 |
| 8 | No | 0 | 0 |
| 11 | No | 1 | 1 |

For $2$ and $3$, only one team exists, so the special rules apply. For larger values, parity alone determines the result.

### Example 2

Input:

```
3
5
12
13
```

| n | Special Case? | n % 2 | Answer |
| --- | --- | --- | --- |
| 5 | No | 1 | 1 |
| 12 | No | 0 | 0 |
| 13 | No | 1 | 1 |

For $12$, an equal split is achievable. For $5$ and $13$, the total population is odd, so the best possible difference is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few comparisons and a modulo operation |
| Space | O(1) | Uses a constant amount of extra memory |

With at most $10^4$ test cases, the total work is negligible. The solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())

        if n == 2:
            ans.append("2")
        elif n == 3:
            ans.append("3")
        else:
            ans.append(str(n % 2))

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run("3\n2\n5\n12\n") == "2\n1\n0"

# minimum valid values
assert run("2\n2\n3\n") == "2\n3"

# smallest odd value with answer 1
assert run("1\n5\n") == "1"

# even value
assert run("1\n8\n") == "0"

# maximum constraint
assert run("1\n10000\n") == "0"

# large odd value
assert run("1\n9999\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2, 3` | `2, 3` | Both special cases |
| `5` | `1` | First odd value where difference 1 is achievable |
| `8` | `0` | Standard even case |
| `10000` | `0` | Maximum even input |
| `9999` | `1` | Maximum odd-style behavior |

## Edge Cases

For the input

```
1
2
```

the algorithm enters the first special-case branch and returns 2. There is only one team of size 2, so the civilization populations are $2$ and $0$. The difference is exactly 2.

For the input

```
1
3
```

the algorithm enters the second special-case branch and returns 3. There is only one team of size 3, so the civilization populations are $3$ and $0$.

For the input

```
1
5
```

the algorithm reaches the general rule and returns $5 \bmod 2 = 1$. A valid construction is teams of sizes 2 and 3 assigned to different civilizations, producing populations $2$ and $3$.

For the input

```
1
12
```

the algorithm returns $12 \bmod 2 = 0$. We can form six teams of size 2 and send three teams to each civilization. Both civilizations receive 6 people, giving difference 0.
