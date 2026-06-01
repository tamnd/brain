---
title: "CF 107B - Basketball Team"
description: "We have a university with several departments. Each department contributes some number of basketball players. Herr Wafa belongs to department h, and he is already guaranteed a place on the final team. The team must contain exactly n players including Wafa himself."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 107
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 83 (Div. 1 Only)"
rating: 1600
weight: 107
solve_time_s: 142
verified: true
draft: false
---

[CF 107B - Basketball Team](https://codeforces.com/problemset/problem/107/B)

**Rating:** 1600  
**Tags:** combinatorics, dp, math, probabilities  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a university with several departments. Each department contributes some number of basketball players. Herr Wafa belongs to department `h`, and he is already guaranteed a place on the final team.

The team must contain exactly `n` players including Wafa himself. Every valid team containing Wafa is equally likely. We need the probability that at least one of Wafa's teammates also comes from his department.

Suppose department `h` contains `s[h]` players in total, including Wafa. Then there are `s[h] - 1` other players from his department who could become his teammates.

The total number of available players is the sum of all `s[i]`. If this total is smaller than `n`, forming a complete team is impossible, so the answer is `-1`.

The constraints are small enough that combinatorial computations are feasible. The number of departments can reach 1000, and each department size can reach 100, so the total number of players is at most `100000`. We cannot enumerate all possible teams because the number of combinations grows exponentially. Even choosing 50 players from 1000 already produces astronomically many possibilities.

The key observation is that we only need a probability, not the actual teams. This strongly suggests counting combinations mathematically.

There are several edge cases that can silently break naive implementations.

Consider this input:

```
5 2 1
2 2
```

The university has only 4 players, but the team size is 5. The correct output is:

```
-1
```

A careless implementation might still try to compute combinations with invalid parameters.

Another tricky case appears when Wafa is the only player in his department:

```
3 3 2
5 1 5
```

There are enough total players, but there are no possible teammates from department 2. The correct probability is:

```
0
```

Some implementations incorrectly divide by zero or assume every department contributes at least two players.

A third subtle case happens when the entire university must be selected:

```
4 2 1
2 2
```

All four players must be chosen. Since department 1 has two players including Wafa, the answer is:

```
1
```

A floating-point approximation based on iterative probabilities can accumulate errors here if written carelessly.

## Approaches

The brute-force idea is straightforward. Since Wafa is always selected, we only need to choose the remaining `n - 1` players from everyone else. We could enumerate every possible subset of size `n - 1`, check whether at least one chosen player comes from Wafa's department, and count how many subsets satisfy the condition.

This works conceptually because every valid team containing Wafa is equally likely. The probability is simply:

$$\frac{\text{favorable teams}}{\text{all teams}}$$

The problem is the number of subsets. If there are around 100000 players and we must choose even 50 of them, the number of combinations is enormous. Exhaustive enumeration is completely impossible.

The important observation is that we do not need to generate teams explicitly. We only need to count them.

After fixing Wafa in the team, there are:

$$\text{total players} - 1$$

remaining candidates, and we choose:

$$n - 1$$

of them.

Instead of counting favorable teams directly, it is easier to count the complement event.

The bad event is that none of Wafa's teammates come from his department. Since department `h` has `s[h] - 1` other players besides Wafa, we must avoid all of them.

That leaves:

$$(\text{total players} - 1) - (s[h] - 1)$$

eligible players outside his department.

The probability of the bad event becomes:

$$\frac{\binom{\text{outside}}{n-1}} {\binom{\text{total}-1}{n-1}}$$

Then the required answer is:

$$1 - \text{bad probability}$$

This transforms the problem from exponential enumeration into a few combinatorial calculations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) or O(1) combinatorics | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and `h`.
2. Read the department sizes array `s`.
3. Compute the total number of players:

$$total = \sum s[i]$$
4. If `total < n`, print `-1`.

Forming a valid team is impossible because there are not enough players in the university.
5. Let:

$$own = s[h-1]$$

This is the number of players in Wafa's department, including Wafa himself.
6. Compute the total number of ways to choose Wafa's teammates:

$$\binom{total-1}{n-1}$$

We subtract one because Wafa is already fixed in the team.
7. Compute the number of bad teams where none of the teammates come from Wafa's department.

There are:

$$total - own$$

players outside his department, so the count is:

$$\binom{total-own}{n-1}$$
8. The bad probability is:

$$\frac{\binom{total-own}{n-1}} {\binom{total-1}{n-1}}$$
9. Print:

$$1 - \text{bad probability}$$

### Why it works

Every team containing Wafa is equally likely, so probability reduces to counting combinations.

The denominator counts all possible teammate selections. The numerator of the complement event counts exactly those selections where every teammate comes from another department. Since these two sets partition all possibilities into "good" and "bad", subtracting the bad probability from 1 gives the required answer.

The algorithm cannot overcount or miss cases because each team corresponds to exactly one subset of `n - 1` teammates.

## Python Solution

```python
import sys
from math import comb

input = sys.stdin.readline

def solve():
    n, m, h = map(int, input().split())
    s = list(map(int, input().split()))

    total = sum(s)

    if total < n:
        print(-1)
        return

    own = s[h - 1]

    total_ways = comb(total - 1, n - 1)
    bad_ways = comb(total - own, n - 1)

    ans = 1.0 - (bad_ways / total_ways)

    print(ans)

solve()
```

The first part reads the input and computes the total number of players.

The impossible case must be handled before any combinatorial computation. If `total < n`, combinations like `C(3, 5)` would be invalid.

The expression `comb(total - 1, n - 1)` counts all possible teammate sets because Wafa himself is already fixed on the team.

The expression `comb(total - own, n - 1)` is subtle. We remove all players from Wafa's department, including the other members of that department. Since Wafa is already fixed separately, only players outside the department remain eligible for the bad event.

The final answer uses floating-point division. Python integers handle arbitrarily large combination values safely, so there is no overflow risk.

The indexing `s[h - 1]` is easy to get wrong because departments are numbered from 1 while Python lists are 0-indexed.

## Worked Examples

### Example 1

Input:

```
3 2 1
2 1
```

There are 3 total players. Wafa's department contains 2 players.

| Variable | Value |
| --- | --- |
| total | 3 |
| own | 2 |
| total - 1 | 2 |
| n - 1 | 2 |
| total ways | C(2,2) = 1 |
| bad ways | C(1,2) = 0 |
| answer | 1 - 0/1 = 1 |

All players must be selected, so the second player from Wafa's department is guaranteed to appear on the team.

### Example 2

Input:

```
2 3 1
2 1 1
```

Wafa needs one teammate.

| Variable | Value |
| --- | --- |
| total | 4 |
| own | 2 |
| total - 1 | 3 |
| n - 1 | 1 |
| total ways | C(3,1) = 3 |
| bad ways | C(2,1) = 2 |
| answer | 1 - 2/3 = 1/3 |

There are three possible teammates. Only one belongs to Wafa's department, so the probability is `1/3`.

This trace confirms that counting the complement event matches direct reasoning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) effectively | Only a few combinatorial computations |
| Space | O(1) | Uses a constant number of variables |

The solution easily fits within the limits. Python's built-in `math.comb` handles large combinations efficiently, and the algorithm performs only a constant number of operations regardless of the number of departments.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import comb

def solve():
    input = sys.stdin.readline

    n, m, h = map(int, input().split())
    s = list(map(int, input().split()))

    total = sum(s)

    if total < n:
        print(-1)
        return

    own = s[h - 1]

    total_ways = comb(total - 1, n - 1)
    bad_ways = comb(total - own, n - 1)

    ans = 1.0 - (bad_ways / total_ways)

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("3 2 1\n2 1\n") == "1.0", "sample 1"

# impossible case
assert run("5 2 1\n2 2\n") == "-1", "not enough players"

# Wafa alone in department
assert run("3 3 2\n5 1 5\n") == "0.0", "no teammate possible"

# all players selected
assert run("4 2 1\n2 2\n") == "1.0", "forced inclusion"

# symmetric departments
res = float(run("3 3 1\n2 2 2\n"))
assert abs(res - 0.4) < 1e-9, "probability check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 2 1 / 2 2` | `-1` | Impossible team formation |
| `3 3 2 / 5 1 5` | `0.0` | Wafa has no department teammate |
| `4 2 1 / 2 2` | `1.0` | Entire university must be selected |
| `3 3 1 / 2 2 2` | `0.4` | General combinatorial probability |

## Edge Cases

Consider the impossible scenario:

```
5 2 1
2 2
```

The total number of players is only 4, but the team size is 5. The algorithm checks `total < n` immediately and prints `-1`. No combinatorial formulas are evaluated, so invalid states are avoided safely.

Now consider the case where Wafa is alone in his department:

```
3 3 2
5 1 5
```

Here `own = 1`. That means there are zero additional players from his department.

The algorithm computes:

$$\binom{10-1}{2} = \binom{9}{2}$$

for all possible teammate selections, and:

$$\binom{10-1}{2} = \binom{9}{2}$$

again for bad selections, because every possible teammate is outside his department. The resulting probability becomes:

$$1 - 1 = 0$$

which is correct.

Finally, consider the forced-selection case:

```
4 2 1
2 2
```

The team size equals the total number of players. Every player must be chosen.

The algorithm computes:

$$\binom{3}{3} = 1$$

total team, and:

$$\binom{2}{3} = 0$$

bad teams. Since no bad team exists, the answer becomes exactly `1`.
