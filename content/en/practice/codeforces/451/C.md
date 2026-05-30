---
title: "CF 451C - Predict Outcome of the Game"
description: "We have a football tournament involving three teams. Every game produces exactly one winner, so each played game contributes exactly one win to one of the teams. After k games have already been played, we do not know the exact number of wins of the three teams."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 451
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 258 (Div. 2)"
rating: 1700
weight: 451
solve_time_s: 115
verified: true
draft: false
---

[CF 451C - Predict Outcome of the Game](https://codeforces.com/problemset/problem/451/C)

**Rating:** 1700  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a football tournament involving three teams. Every game produces exactly one winner, so each played game contributes exactly one win to one of the teams.

After `k` games have already been played, we do not know the exact number of wins of the three teams. We only know two absolute differences:

- The difference between the wins of team 1 and team 2 is `d1`.
- The difference between the wins of team 2 and team 3 is `d2`.

The tournament will eventually contain `n` games in total. We want to know whether it is possible to complete the tournament so that, after all `n` games are finished, every team has exactly the same number of wins.

Since every game contributes one win, the final number of wins across all teams is exactly `n`. If all three teams must finish equal, each team must end with `n / 3` wins. This immediately implies that `n` must be divisible by 3.

The constraints are the first clue that a mathematical solution is required. The number of test cases reaches `10^5`, and `n` can be as large as `10^12`. Any approach that simulates games or searches over win distributions is impossible. Even doing work proportional to `k` would fail. We need a constant-time check for each test case.

The tricky part is that the differences are absolute values. Knowing `|a - b| = d1` and `|b - c| = d2` does not uniquely determine the current win counts. Several sign configurations are possible.

A common mistake is to assume a single ordering such as `a ≥ b ≥ c`. Consider:

```
n = 6
k = 4
d1 = 1
d2 = 0
```

One valid distribution is `(2,1,1)`, which leads to a valid final tournament. If we only check the ordering `a ≥ b ≥ c`, we would find it, but in other cases the only valid arrangement may use a different ordering.

Another subtle case occurs when the current strongest team already has too many wins. For example:

```
n = 6
k = 3
d1 = 3
d2 = 0
```

The only possible distribution is `(3,0,0)`. Since each team must finish with `2` wins, team 1 already exceeds the final target. The answer is `"no"`.

A third edge case is divisibility. Consider:

```
n = 4
k = 0
d1 = 0
d2 = 0
```

Even though the current state is perfectly balanced, four total wins cannot be divided equally among three teams. The answer must be `"no"`.

## Approaches

A brute-force approach would try to reconstruct the numbers of wins of the three teams after the first `k` matches. Let those counts be `(a,b,c)`.

They must satisfy:

```
a + b + c = k
|a - b| = d1
|b - c| = d2
```

One could enumerate possible values of `a`, `b`, and `c`, check the constraints, and then verify whether the remaining `n-k` games can balance all teams.

This works conceptually because every valid current state can be tested directly. The problem is scale. Since `k` can be as large as `10^12`, even iterating over possible values of one variable is completely infeasible.

The key observation is that there are only four distinct ways to assign signs to the two absolute differences.

Let team 2's wins be some value `x`.

Then team 1 must be either `x+d1` or `x-d1`.

Similarly, team 3 must be either `x+d2` or `x-d2`.

That creates only four candidate patterns:

```
(x+d1, x, x+d2)
(x+d1, x, x-d2)
(x-d1, x, x+d2)
(x-d1, x, x-d2)
```

For each pattern, the equation

```
a + b + c = k
```

determines `x` uniquely.

After obtaining `(a,b,c)`, we only need to verify whether:

1. All counts are non-negative integers.
2. No team already exceeds the final target `n/3`.
3. The remaining games are enough to raise all teams to `n/3`.

The third condition turns out to be equivalent to checking that the total additional wins required equals exactly the number of remaining games.

Since there are only four configurations, every test case can be solved in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) or worse | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check whether `n` is divisible by 3. If not, equal final scores are impossible, so return `"no"`.
2. Let the final target wins per team be:

```
target = n / 3
```
3. Enumerate the four sign configurations:

```
(+d1, +d2)
(+d1, -d2)
(-d1, +d2)
(-d1, -d2)
```
4. For a chosen configuration, write:

```
a = x + s1*d1
b = x
c = x + s2*d2
```

where `s1` and `s2` are either `+1` or `-1`.
5. Use the condition `a+b+c=k` to compute `x`.

```
3x + s1*d1 + s2*d2 = k
```

Hence

```
x = (k - s1*d1 - s2*d2) / 3
```
6. If the numerator is not divisible by 3, this configuration cannot represent valid win counts. Skip it.
7. Construct `(a,b,c)` and verify that all values are non-negative.
8. Let

```
mx = max(a,b,c)
```

If `mx > target`, then some team already has more wins than its final allowed total. Skip this configuration.
9. Compute how many wins are needed to bring every team to the target:

```
need = (target-a) + (target-b) + (target-c)
```
10. If `need == n-k`, then the remaining games can exactly provide those wins, so return `"yes"`.
11. If none of the four configurations works, return `"no"`.

### Why it works

The only uncertainty in the current standings comes from the directions of the two absolute differences. Every valid triple `(a,b,c)` must correspond to one of the four sign assignments.

For a fixed assignment, the equation `a+b+c=k` uniquely determines the standings. No valid distribution is missed.

If a team already exceeds the final target `n/3`, there is no way to remove wins later, so that configuration is impossible. If all teams are at most the target, then the exact number of wins required to reach `(target,target,target)` is

```
(target-a)+(target-b)+(target-c).
```

Because each future game contributes exactly one additional win, the configuration is feasible precisely when this required total equals the number of remaining games `n-k`.

Since every possible sign assignment is examined and each one is checked exactly against the tournament constraints, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def possible(n, k, d1, d2):
    if n % 3 != 0:
        return False

    target = n // 3

    for s1 in (1, -1):
        for s2 in (1, -1):
            rem = k - s1 * d1 - s2 * d2

            if rem % 3 != 0:
                continue

            x = rem // 3

            a = x + s1 * d1
            b = x
            c = x + s2 * d2

            if min(a, b, c) < 0:
                continue

            if max(a, b, c) > target:
                continue

            need = (target - a) + (target - b) + (target - c)

            if need == n - k:
                return True

    return False

def main():
    t = int(input())

    ans = []
    for _ in range(t):
        n, k, d1, d2 = map(int, input().split())
        ans.append("yes" if possible(n, k, d1, d2) else "no")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()
```

The first check handles the unavoidable divisibility requirement. If `n` is not a multiple of three, equal final scores cannot exist.

The nested loops enumerate the four possible interpretations of the absolute differences. For each one, the sum constraint determines the middle value `x`. If the resulting value is not integral, that configuration cannot correspond to actual win counts.

The non-negativity check removes impossible standings. The maximum-value check is essential because wins cannot be taken away from a team later.

The final equality

```
need == n - k
```

captures whether the remaining games are exactly sufficient to raise all teams to the common target.

All arithmetic uses integers, so there are no overflow concerns even when `n` reaches `10^12`, since Python integers are unbounded.

## Worked Examples

### Example 1

Input:

```
n = 6
k = 4
d1 = 1
d2 = 0
```

Target:

```
target = 2
```

Trying configuration `(s1,s2)=(+1,+1)`:

| Step | Value |
| --- | --- |
| rem | 4 - 1 - 0 = 3 |
| x | 1 |
| a | 2 |
| b | 1 |
| c | 1 |
| max(a,b,c) | 2 |
| need | 0 + 1 + 1 = 2 |
| n-k | 2 |

Since `need = n-k`, this configuration is feasible and the answer is `"yes"`.

This example shows a case where one team is currently leading, but the remaining games are sufficient to equalize all teams.

### Example 2

Input:

```
n = 6
k = 3
d1 = 3
d2 = 0
```

Target:

```
target = 2
```

Trying `(s1,s2)=(+1,+1)`:

| Step | Value |
| --- | --- |
| rem | 3 - 3 - 0 = 0 |
| x | 0 |
| a | 3 |
| b | 0 |
| c | 0 |
| max(a,b,c) | 3 |
| target | 2 |

The largest team already exceeds the final allowed score, so this configuration is impossible.

The remaining sign configurations either produce negative counts or fail divisibility checks.

The answer is `"no"`.

This example demonstrates why checking only the differences is insufficient. A team may already have accumulated too many wins to ever be balanced later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Exactly four configurations are tested per case |
| Space | O(1) | Only a few integer variables are stored |

With up to `10^5` test cases, the solution performs only a constant amount of arithmetic for each one. The total workload easily fits within the time limit, and memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def possible(n, k, d1, d2):
        if n % 3 != 0:
            return False

        target = n // 3

        for s1 in (1, -1):
            for s2 in (1, -1):
                rem = k - s1 * d1 - s2 * d2

                if rem % 3 != 0:
                    continue

                x = rem // 3

                a = x + s1 * d1
                b = x
                c = x + s2 * d2

                if min(a, b, c) < 0:
                    continue

                if max(a, b, c) > target:
                    continue

                need = (target - a) + (target - b) + (target - c)

                if need == n - k:
                    return True

        return False

    t = int(input())
    out = []

    for _ in range(t):
        n, k, d1, d2 = map(int, input().split())
        out.append("yes" if possible(n, k, d1, d2) else "no")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# provided samples
assert run(
"""5
3 0 0 0
3 3 0 0
6 4 1 0
6 3 3 0
3 3 3 2
"""
) == "yes\nyes\nyes\nno\nno"

# minimum case
assert run(
"""1
3 0 0 0
"""
) == "yes"

# n not divisible by 3
assert run(
"""1
4 0 0 0
"""
) == "no"

# already perfectly balanced
assert run(
"""1
9 9 0 0
"""
) == "yes"

# large values
assert run(
"""1
999999999999 0 0 0
"""
) == "yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 0 0 0` | `yes` | Smallest balanced tournament |
| `4 0 0 0` | `no` | Divisibility by 3 is mandatory |
| `9 9 0 0` | `yes` | Tournament already finished and balanced |
| `999999999999 0 0 0` | `yes` | Handles maximum-scale arithmetic |

## Edge Cases

Consider:

```
1
4 0 0 0
```

The algorithm immediately checks `n % 3`. Since `4 % 3 = 1`, equal final scores are impossible. The output is `"no"`. A solution that only reasons about the current standings would incorrectly accept this case.

Consider:

```
1
6 3 3 0
```

Using the valid sign assignment gives:

```
(a,b,c) = (3,0,0)
```

The target is `2`. Since `max(a,b,c)=3`, one team already has more wins than allowed in the final balanced state. The algorithm rejects the configuration and outputs `"no"`.

Consider:

```
1
3 3 3 2
```

All four sign assignments are examined. Some produce negative win counts, while the others fail the divisibility requirement. No valid distribution of current wins exists at all. The algorithm correctly outputs `"no"` because the reported differences cannot arise after three games.

Consider:

```
1
6 4 1 0
```

One configuration yields:

```
(a,b,c) = (2,1,1)
```

No team exceeds the target `2`, and exactly two wins remain to be distributed. The required additional wins are also `2`, so the algorithm outputs `"yes"`. This confirms that having a current leader is acceptable as long as the leader has not already exceeded the final target.
