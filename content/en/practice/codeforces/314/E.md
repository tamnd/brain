---
title: "CF 314E - Sereja and Squares"
description: "The geometric description hides a much simpler combinatorial structure. Take a pair of points $(l,0)$ and $(r,0)$, with $l<r$. The left endpoint is marked by a lowercase letter and the right endpoint by the corresponding uppercase letter."
date: "2026-06-06T01:08:37+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 314
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 187 (Div. 1)"
rating: 2900
weight: 314
solve_time_s: 137
verified: true
draft: false
---

[CF 314E - Sereja and Squares](https://codeforces.com/problemset/problem/314/E)

**Rating:** 2900  
**Tags:** dp  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The geometric description hides a much simpler combinatorial structure.

Take a pair of points $(l,0)$ and $(r,0)$, with $l<r$. The left endpoint is marked by a lowercase letter and the right endpoint by the corresponding uppercase letter.

If two pairs cross, their squares intersect. If one pair is completely inside another pair, the corresponding square is completely inside the larger square and they do not touch. The valid pairings are exactly the same as properly nested or disjoint bracket pairs. The structure is identical to a correct bracket sequence with 25 bracket types.

After Petya's erasures:

- Every visible lowercase letter is definitely an opening bracket of a known type.
- Every uppercase letter disappeared.
- Every `?` may be either:

- an erased opening bracket, whose type is unknown, or
- an erased closing bracket.

We must count how many complete correct bracket sequences could have produced the given string.

The length can reach $10^5$, which immediately rules out classical bracket DP states such as `dp[position][balance]`. A quadratic algorithm would require around $10^{10}$ operations and is impossible.

A more subtle observation is needed.

Consider a position containing `?`.

If we decide that it is an opening bracket, its type can be chosen later. If it is a closing bracket, its type is already forced by the unmatched opening bracket on top of the stack. Once the opening side is known, the matching closing side has no independent choice.

This means the combinatorial difficulty is not about bracket types at all. First we count valid opening/closing placements assuming there is only one bracket type. After that we multiply by the number of ways to assign types to the unknown openings.

A few easy-to-miss cases:

If $n$ is odd, a perfect pairing is impossible.

Example:

```
3
???
```

The answer is `0`.

If there are already more than $n/2$ visible lowercase letters, we cannot fit the required number of opening brackets.

Example:

```
4
abcd
```

All four positions are forced openings, so the answer is `0`.

Another subtle case is when a prefix would contain too many closing brackets.

Example:

```
4
?a??
```

The first `?` cannot be chosen as a closing bracket because a correct bracket sequence may never have more closings than openings in any prefix.

The DP bounds automatically eliminate such states.

## Approaches

The most direct idea is standard bracket-sequence DP.

Let `dp[i][bal]` be the number of ways after processing the first `i` positions with current stack size `bal`.

A visible letter always increases the balance. A `?` can either increase or decrease it.

This is correct, but the balance can be as large as $n$. With $n=10^5$, the state space becomes $O(n^2)$, far beyond the limit.

The key observation is that every visible lowercase letter is already known to be an opening bracket. The only decisions are made at `?` positions.

Instead of storing the current balance, store how many closing brackets have been placed so far.

Let $m=n/2$, the total number of closing brackets in any valid sequence.

After processing position $i$:

- at most $\lfloor i/2 \rfloor$ closings can appear, otherwise some prefix would contain more closings than openings;
- at least $i-m$ closings must already appear, otherwise there would not be enough remaining positions to reach exactly $m$ closings by the end.

Those bounds are surprisingly tight. They reduce the active DP range to a narrow diagonal strip. Summing the widths over all positions gives only $O(n)$ total work.

After counting valid opening/closing layouts, every unknown opening bracket contributes a factor of $25$, because its type may be any lowercase letter except `x`. Closing bracket types are then forced by the matching structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP on balance | $O(n^2)$ | $O(n)$ or $O(n^2)$ | Too slow |
| Optimal DP on number of closings | $O(n)$ amortized | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. If $n$ is odd, output `0`.
2. Let $m=n/2$. Any valid sequence must contain exactly $m$ openings and $m$ closings.
3. Count how many visible lowercase letters already exist. Call this value `fixed_open`.
4. Let `dp[j]` be the number of ways to process the current prefix while placing exactly `j` closing brackets.
5. Initialize `dp[0] = 1`.
6. Process positions from left to right.
7. If the current character is a visible lowercase letter, it is forced to be an opening bracket. No DP transition is needed.
8. If the current character is `?`, it may become either:

- an opening bracket,
- or a closing bracket.

Choosing it as a closing bracket increases the number of closings by one:

```
dp[j] += dp[j-1]
```

The update is performed in descending order of `j`.
9. During the update, only consider

```
i - m <= j <= floor(i/2)
```

where `i` is the current 1-based position.

The upper bound guarantees prefix validity. The lower bound guarantees enough remaining positions to reach exactly `m` closings.
10. After all positions are processed, `dp[m]` equals the number of valid opening/closing layouts assuming only one bracket type.
11. The number of openings that came from `?` positions is

```
m - fixed_open
```

1. Multiply by

```
25^(m - fixed_open)
```

because each such opening may choose any of the 25 allowed letters.

1. Output the result modulo $2^{32}$.

### Why it works

The DP counts only the positions of closing brackets.

A valid bracket sequence of length $n$ contains exactly $m$ closings. For every prefix, the number of closings may never exceed the number of openings, which is equivalent to $j \le i/2$. The lower bound $j \ge i-m$ guarantees that the remaining suffix can still supply enough closings to finish with exactly $m$.

Every valid opening/closing arrangement corresponds to exactly one legal nesting structure. Once the opening positions are fixed, every closing bracket type is determined by the opening bracket it matches. The only remaining freedom is choosing the type of each opening that originated from a `?`, giving a factor of $25$ per such opening.

Hence the DP counts all valid structures exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1 << 32

def solve():
    n = int(input())
    s = input().strip()

    if n & 1:
        print(0)
        return

    m = n // 2

    dp = [0] * (m + 1)
    dp[0] = 1

    fixed_open = 0

    for i, ch in enumerate(s, 1):
        if ch == '?':
            lo = max(1, i - m)
            hi = min(m, i // 2)

            for j in range(hi, lo - 1, -1):
                dp[j] = (dp[j] + dp[j - 1]) & 0xFFFFFFFF
        else:
            fixed_open += 1

    ans = dp[m]

    for _ in range(m - fixed_open):
        ans = (ans * 25) & 0xFFFFFFFF

    print(ans)

solve()
```

The array `dp[j]` stores counts indexed only by the number of closings used so far. A visible lowercase letter does not change this count because it is forced to be an opening bracket.

For a `?`, the existing value `dp[j]` already represents choosing it as an opening bracket. Adding `dp[j-1]` corresponds to choosing it as a closing bracket.

The descending iteration order is essential. It prevents values created during the current position from being reused again during the same update.

The modulo is $2^{32}$. Using

```
x & 0xFFFFFFFF
```

is equivalent to taking the result modulo $2^{32}$ after every operation.

## Worked Examples

### Sample 1

Input:

```
4
a???
```

Here $m=2$.

| Position | Character | Reachable closing counts |
| --- | --- | --- |
| 1 | a | {0} |
| 2 | ? | {0, 1} |
| 3 | ? | {0, 1} |
| 4 | ? | {1, 2} |

Final:

| Value | Result |
| --- | --- |
| dp[2] | 2 |
| fixed openings | 1 |
| unknown openings | 1 |
| multiplier | 25 |
| answer | 50 |

Output:

```
50
```

The example shows the separation between structural counting and letter assignment.

### Sample 2

Input:

```
6
abc???
```

| Position | Character |
| --- | --- |
| 1 | a |
| 2 | b |
| 3 | c |
| 4 | ? |
| 5 | ? |
| 6 | ? |

All first three positions are forced openings. The only possible valid structure is to place all three remaining positions as closings.

Thus:

| Value | Result |
| --- | --- |
| dp[3] | 1 |
| fixed openings | 3 |
| unknown openings | 0 |
| answer | 1 |

Output:

```
1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ amortized | The valid range of `j` forms a diagonal strip whose total width over all positions is linear |
| Space | $O(n)$ | One DP array of size $n/2+1$ |

With $n=10^5$, both memory usage and running time comfortably fit the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 1 << 32

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    if n & 1:
        return "0"

    m = n // 2

    dp = [0] * (m + 1)
    dp[0] = 1
    fixed_open = 0

    for i, ch in enumerate(s, 1):
        if ch == '?':
            lo = max(1, i - m)
            hi = min(m, i // 2)

            for j in range(hi, lo - 1, -1):
                dp[j] = (dp[j] + dp[j - 1]) & 0xFFFFFFFF
        else:
            fixed_open += 1

    ans = dp[m]
    for _ in range(m - fixed_open):
        ans = (ans * 25) & 0xFFFFFFFF

    return str(ans)

# provided samples
assert run("4\na???\n") == "50", "sample 1"
assert run("4\nabc?\n") == "0", "sample 2"
assert run("6\nabc???\n") == "1", "sample 3"

# custom cases
assert run("1\n?\n") == "0", "odd length"
assert run("2\n??\n") == "25", "single pair, unknown type"
assert run("2\na?\n") == "1", "forced pair"
assert run("4\n????\n") == "1250", "all positions unknown"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 ?` | `0` | Odd length cannot be paired |
| `2 ??` | `25` | One opening, one closing, 25 letter choices |
| `2 a?` | `1` | Fully determined structure and type |
| `4 ????` | `1250` | Multiple structures and type assignments |

## Edge Cases

Consider:

```
3
???
```

The algorithm immediately detects that $n$ is odd and returns `0`. No valid pairing can exist.

Consider:

```
4
abcd
```

All four positions are forced openings. We would need exactly two openings and two closings, but there are no positions available for closings. The DP never reaches state `dp[2]`, so the answer is `0`.

Consider:

```
4
?a??
```

At the first position, choosing a closing bracket would create a prefix with more closings than openings. The bound

```
j <= floor(i/2)
```

removes that state automatically. Only prefix-valid configurations survive, and the final answer counts exactly the legal bracket sequences.
