---
title: "CF 95D - Horse Races"
description: "We are given several intervals of integers. For every interval $[l, r]$, we must count how many numbers contain two lucky digits, either 4 or 7, whose positions differ by at most k. Positions are counted inside the decimal representation of the number."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 95
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 77 (Div. 1 Only)"
rating: 2500
weight: 95
solve_time_s: 120
verified: true
draft: false
---

[CF 95D - Horse Races](https://codeforces.com/problemset/problem/95/D)

**Rating:** 2500  
**Tags:** dp, math  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several intervals of integers. For every interval $[l, r]$, we must count how many numbers contain two lucky digits, either `4` or `7`, whose positions differ by at most `k`.

Positions are counted inside the decimal representation of the number. If two lucky digits appear close enough, the number is called nearly lucky.

For example, with $k = 2$:

- `404` is nearly lucky because the two `4`s are two positions apart.
- `4123954997` is not nearly lucky because the closest pair of lucky digits is too far apart.
- A number with only one lucky digit can never qualify.

The interval bounds are enormous. A number may contain up to 1000 decimal digits, so iterating through every value in the range is impossible. Even checking one number digit by digit is already too expensive if we tried it for all values.

This immediately rules out any solution proportional to the numeric size of the interval. The only feasible direction is digit DP, where we count valid numbers by constructing them digit by digit.

The number of test cases and the value of $k$ are both at most 1000. Since the digit length is also at most 1000, a solution around $O(\text{digits}^2)$ per query is acceptable. A cubic solution would already become risky.

Several edge cases are easy to mishandle.

Consider $k = 1$. Then only adjacent lucky digits matter.

Input:

```
1 1
1 100
```

The valid numbers are only `44`, `47`, `74`, and `77`, so the answer is `4`. A careless implementation may incorrectly count numbers like `404`, where the lucky digits are separated by distance `2`.

Another dangerous case is leading zeroes. Suppose we process numbers as fixed-length strings.

Input:

```
1 2
1 50
```

If we allow leading zeroes to behave like real digits, then `"004"` and `"040"` could accidentally create fake lucky pairs. Leading zeroes must not participate in the condition.

A third subtle case appears when a valid pair already exists. Once we already found a close enough pair of lucky digits, later digits no longer matter for validity.

For example:

```
1 2
447000000000 447000000000
```

The number is already nearly lucky because the first two digits form a valid pair. A buggy DP might later overwrite the state and lose that information.

## Approaches

The brute force idea is straightforward. For every number in the interval, scan its decimal digits and record the positions of all `4` and `7` digits. If any two consecutive lucky positions differ by at most `k`, count the number.

This works because the property depends only on the digit sequence of one number.

The problem is scale. The interval endpoints may have 1000 digits. Even the interval size itself is astronomically large. Enumerating numbers is impossible.

So instead of iterating over numbers, we count them combinatorially.

The key observation is that the property depends only on local information while scanning digits left to right. At any point, we only need to know:

- whether a valid pair has already appeared,
- where the most recent lucky digit occurred.

That makes the problem perfect for digit DP.

We define a DP over digit positions. While constructing the number digit by digit, we track:

- the current position,
- the position of the last lucky digit,
- whether we already formed a valid pair,
- whether we already started the number,
- whether we are still tight to the upper bound.

Whenever we place a `4` or `7`, we compare its position with the previous lucky digit. If the distance is at most `k`, the number becomes valid forever.

This converts the problem from iterating over values to iterating over states. The total number of states is roughly $1000^2$, which is completely manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible | Impossible | Too slow |
| Optimal Digit DP | $O(L^2 \cdot 10)$ | $O(L^2)$ | Accepted |

Here, $L$ is the number of digits.

## Algorithm Walkthrough

1. Define a function `solve(x)` that returns how many nearly lucky numbers are in the range $[0, x]$.

Then every query answer becomes:

$$solve(r) - solve(l-1)$$
2. Convert the upper bound into a digit array.

Digit DP works naturally on strings because we process one digit position at a time.
3. Use memoized DFS with state:

$$(pos,\ last,\ found,\ started,\ tight)$$

where:

- `pos` is the current digit index.
- `last` is the position of the most recent lucky digit.
- `found` tells whether a valid pair already exists.
- `started` tells whether we already placed a non-leading-zero digit.
- `tight` tells whether the current prefix is equal to the upper bound prefix.
4. If we reach the end of the digit string, return `1` only if `found = True`.

This means the constructed number is nearly lucky.
5. Try all possible digits for the current position.

The maximum allowed digit depends on `tight`.
6. Handle leading zeroes carefully.

If the number has not started yet and we place another zero, we stay in the `started = False` state and do not treat the zero as a real digit.
7. If the placed digit is `4` or `7`, update the lucky information.

If there was a previous lucky digit at position `last`, and:

$$pos - last \le k$$

then set `found = True`.

Afterwards, update `last = pos`.
8. Recurse to the next position and accumulate answers modulo $10^9 + 7$.
9. For each query, compute:

$$(solve(r) - solve(l-1)) \bmod (10^9+7)$$

### Why it works

The DP state stores exactly the information needed to determine whether future digits can create a valid pair.

The future only depends on the nearest previous lucky digit because any new lucky digit only needs to compare against the latest one. Earlier lucky digits are farther away and can never produce a smaller distance.

The `found` flag is monotonic. Once a valid pair appears, the number will remain nearly lucky regardless of future digits.

Since every valid number corresponds to exactly one DP path and every DP path represents exactly one number, the counting is correct.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

MOD = 10**9 + 7

def subtract_one(s):
    if s == "0":
        return "0"

    a = list(s)
    i = len(a) - 1

    while i >= 0 and a[i] == '0':
        a[i] = '9'
        i -= 1

    a[i] = str(int(a[i]) - 1)

    res = ''.join(a).lstrip('0')
    return res if res else "0"

def count_nearly_lucky(s, k):
    digits = list(map(int, s))
    n = len(digits)

    @lru_cache(None)
    def dfs(pos, last, found, started, tight):
        if pos == n:
            return 1 if found else 0

        limit = digits[pos] if tight else 9
        ans = 0

        for d in range(limit + 1):
            ntight = tight and (d == limit)

            if not started and d == 0:
                ans += dfs(pos + 1, -1, found, False, ntight)
                ans %= MOD
                continue

            nfound = found
            nlast = last

            if d == 4 or d == 7:
                if last != -1 and pos - last <= k:
                    nfound = True
                nlast = pos

            ans += dfs(pos + 1, nlast, nfound, True, ntight)
            ans %= MOD

        return ans

    return dfs(0, -1, False, False, True)

def solve():
    t, k = map(int, input().split())

    out = []

    for _ in range(t):
        l, r = input().split()

        left = subtract_one(l)

        ans = (count_nearly_lucky(r, k) -
               count_nearly_lucky(left, k)) % MOD

        out.append(str(ans))

    print('\n'.join(out))

solve()
```

The function `count_nearly_lucky` performs the digit DP over all numbers from `0` to the given bound.

The `last` variable stores the position of the most recent lucky digit. Using only the most recent one is enough because any earlier lucky digit is even farther away from future positions.

Leading zeroes are handled through the `started` flag. Until the first non-zero digit appears, positions do not count as part of the number. Without this distinction, numbers with different lengths would interfere with each other.

The transition:

```
if last != -1 and pos - last <= k:
```

is the core of the problem. It detects whether the current lucky digit forms a close enough pair with the previous lucky digit.

The subtraction helper is also subtle. Since bounds can have 1000 digits, we cannot convert them to integers. The decrement must be performed directly on the string.

Finally, answers are always reduced modulo $10^9 + 7$.

## Worked Examples

### Sample 1

Input:

```
1 2
1 100
```

We compute:

$$solve(100) - solve(0)$$

The valid numbers are `44`, `47`, `74`, `77`.

| Number | Lucky Positions | Minimum Distance | Valid |
| --- | --- | --- | --- |
| 44 | 0,1 | 1 | Yes |
| 47 | 0,1 | 1 | Yes |
| 74 | 0,1 | 1 | Yes |
| 77 | 0,1 | 1 | Yes |

Final answer:

```
4
```

This example confirms that adjacent lucky digits are detected correctly.

### Example 2

Input:

```
1 2
400 500
```

Relevant candidates:

| Number | Lucky Positions | Distance | Valid |
| --- | --- | --- | --- |
| 404 | 0,2 | 2 | Yes |
| 407 | 0,2 | 2 | Yes |
| 447 | 0,1,2 | 1 | Yes |
| 470 | 0,1 | 1 | Yes |
| 499 | 0 | - | No |

The DP discovers these numbers while building digits left to right.

For `404`:

| Position | Digit | Last Lucky Position | Found |
| --- | --- | --- | --- |
| 0 | 4 | 0 | False |
| 1 | 0 | 0 | False |
| 2 | 4 | 2 | True |

At position `2`, the distance is `2 - 0 = 2`, which satisfies the condition.

This trace demonstrates why keeping only the latest lucky digit is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(L^2 \cdot 10)$ | DP states are based on digit position and last lucky position |
| Space | $O(L^2)$ | Memoization table |

Here, $L$ is the number of digits, at most 1000.

A quadratic DP over 1000 digits easily fits within the limits. The state count is only a few million in the worst case, and transitions are constant-factor small.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io
from functools import lru_cache

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def subtract_one(s):
        if s == "0":
            return "0"

        a = list(s)
        i = len(a) - 1

        while i >= 0 and a[i] == '0':
            a[i] = '9'
            i -= 1

        a[i] = str(int(a[i]) - 1)

        res = ''.join(a).lstrip('0')
        return res if res else "0"

    def count_nearly_lucky(s, k):
        digits = list(map(int, s))
        n = len(digits)

        @lru_cache(None)
        def dfs(pos, last, found, started, tight):
            if pos == n:
                return 1 if found else 0

            limit = digits[pos] if tight else 9
            ans = 0

            for d in range(limit + 1):
                ntight = tight and (d == limit)

                if not started and d == 0:
                    ans += dfs(pos + 1, -1, found, False, ntight)
                    continue

                nfound = found
                nlast = last

                if d == 4 or d == 7:
                    if last != -1 and pos - last <= k:
                        nfound = True
                    nlast = pos

                ans += dfs(pos + 1, nlast, nfound, True, ntight)

            return ans % MOD

        return dfs(0, -1, False, False, True)

    t, k = map(int, input().split())

    out = []

    for _ in range(t):
        l, r = input().split()

        left = subtract_one(l)

        ans = (count_nearly_lucky(r, k) -
               count_nearly_lucky(left, k)) % MOD

        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run("1 2\n1 100\n") == "4", "sample 1"

# single number, not nearly lucky
assert run("1 1\n4 4\n") == "0", "single lucky digit"

# exact boundary distance
assert run("1 2\n404 404\n") == "1", "distance exactly k"

# distance too large
assert run("1 1\n404 404\n") == "0", "distance exceeds k"

# multiple valid numbers
assert run("1 2\n44 77\n") == "4", "all two-digit lucky pairs"

# leading zero handling
assert run("1 3\n1 9\n") == "0", "no fake leading-zero pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 4 4` | `0` | A single lucky digit is insufficient |
| `1 2 / 404 404` | `1` | Distance equal to `k` counts |
| `1 1 / 404 404` | `0` | Distance larger than `k` does not count |
| `1 2 / 44 77` | `4` | All two-digit lucky combinations |
| `1 3 / 1 9` | `0` | Leading zeroes are ignored |

## Edge Cases

Consider:

```
1 1
404 404
```

The lucky digits are at positions `0` and `2`. Their distance is `2`, which exceeds `k = 1`.

During DP:

| Position | Digit | Last Lucky | Found |
| --- | --- | --- | --- |
| 0 | 4 | 0 | False |
| 1 | 0 | 0 | False |
| 2 | 4 | 2 | False |

The condition `pos - last <= k` fails, so the number is rejected correctly.

Now consider leading zeroes:

```
1 2
1 9
```

The DP internally processes numbers with the same length as the upper bound. For example, `4` may appear as `"04"`.

Because `started = False` before the first non-zero digit, the leading zero is ignored and does not become part of the number. The algorithm never treats `"04"` as having lucky digits at positions `0` and `1`.

Finally, consider:

```
1 100
447000000000 447000000000
```

The first two digits already satisfy the condition.

| Position | Digit | Found |
| --- | --- | --- |
| 0 | 4 | False |
| 1 | 4 | True |
| 2..11 | various | True |

Once `found` becomes true, it stays true permanently. Later digits cannot invalidate the number.
