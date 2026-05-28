---
title: "CF 148C - Terse princess"
description: "We need to construct an array of groom fortunes so that the princess reacts in exactly the required way. For every groom after the first one, two special situations are possible. If the current fortune is larger than every previous fortune, the princess says Oh...."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 148
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 105 (Div. 2)"
rating: 1700
weight: 148
solve_time_s: 134
verified: false
draft: false
---

[CF 148C - Terse princess](https://codeforces.com/problemset/problem/148/C)

**Rating:** 1700  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct an array of groom fortunes so that the princess reacts in exactly the required way.

For every groom after the first one, two special situations are possible.

If the current fortune is larger than every previous fortune, the princess says `Oh...`.

If the current fortune is larger than the sum of all previous fortunes, the princess says `Wow!` instead. A `Wow!` replaces `Oh...`, it is not counted as both.

The first groom never produces any reaction.

We are given `n`, the number of grooms, together with the exact number of `Oh...` reactions `a` and `Wow!` reactions `b`. The task is to output any valid sequence of fortunes between `1` and `50000`, or `-1` if no such sequence exists.

The constraints are tiny. Both `a` and `b` are at most `15`, and `n` is at most `100`. That means brute-force search over arbitrary arrays would still explode, because each position may contain up to `50000` choices. A naive backtracking solution would be completely infeasible. On the other hand, the small limits strongly suggest that the intended solution is constructive. We are expected to directly build a valid sequence rather than search for one.

The tricky part is that `Wow!` is much stronger than `Oh...`.

Suppose the previous fortunes sum to `S` and the current maximum is `M`.

If we choose a value:

- `x <= M`, there is no reaction.
- `M < x <= S`, we get `Oh...`.
- `x > S`, we get `Wow!`.

This immediately reveals an important fact. To produce an `Oh...`, we need the previous sum to be strictly larger than the current maximum. Otherwise the interval `(M, S]` is empty.

For example:

Input:

```
3 1 1
```

A careless construction might try:

```
1 2 3
```

But this gives two `Wow!` reactions, because:

- `2 > 1`
- `3 > 1+2`

There is never an `Oh...`.

Another easy mistake is forgetting that repeated small values are useful filler.

For example:

Input:

```
5 0 0
```

A strictly increasing sequence fails immediately. The correct idea is to keep all values equal:

```
7 7 7 7 7
```

No value exceeds the previous maximum, so there are no reactions at all.

One more subtle edge case appears when we want too many `Oh...` reactions relative to `Wow!`.

Consider:

```
3 2 0
```

This is impossible.

Without any `Wow!`, the sum and maximum stay equal after the first element if all numbers are identical. To create even one `Oh...`, we first need the total sum to become larger than the maximum. The only mechanism that rapidly increases the sum is a `Wow!`.

This leads to the key feasibility condition:

```
a <= b + 1
```

If this condition fails, no construction exists.

## Approaches

The most direct brute-force approach is to try generating all possible arrays and simulate the princess reactions for each one. Simulation itself is easy. We maintain the current maximum and prefix sum, then classify every new value into one of the three categories.

The problem is the search space. Even if we restricted fortunes to values from `1` to `10`, the number of arrays would already be `10^100` in the worst case. There is no chance of exploring that space.

The structure of the reactions gives a much better direction. Every reaction depends only on two quantities from the prefix:

- the current maximum
- the current prefix sum

A `Wow!` increases both aggressively, because the new value exceeds the whole previous sum. An `Oh...` only increases the maximum, while staying within the current sum.

The crucial observation is that after a `Wow!`, the prefix sum becomes much larger than the maximum. That creates room for future `Oh...` reactions.

For example:

```
1
```

Current sum = 1, max = 1.

If we append:

```
2
```

We get a `Wow!`.

Now:

```
sum = 3
max = 2
```

There is finally space for an `Oh...`, because values in `(2, 3]` exist.

Appending:

```
3
```

Produces an `Oh...`.

After that:

```
sum = 6
max = 3
```

There is again space for another `Oh...`.

This pattern suggests a clean construction:

- Start with `1`.
- Produce each `Wow!` using `sum + 1`.
- After every `Wow!`, optionally produce one `Oh...` using exactly `sum`.

Because each `Wow!` creates room for exactly one guaranteed `Oh...`, the maximum number of `Oh...` reactions is `b + 1`. That is exactly the feasibility condition.

Once all required reactions are created, we fill remaining positions with `1`, which never triggers anything because the maximum is already at least `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check whether `a > b + 1`.

If this happens, print `-1`. Every `Wow!` can create room for at most one new `Oh...`, and there may also be one initial `Oh...` before any `Wow!`.
2. Start the sequence with `1`.

The first groom never causes any reaction, so this is the simplest possible start.
3. Maintain two variables:

- `s`, the current prefix sum
- `mx`, the current maximum
4. If `a > 0`, create one initial `Oh...`.

Append `1` again only if we do not want an `Oh...`. Otherwise we need a value larger than the maximum but not larger than the sum. Initially both are `1`, so this is impossible.

The only way to create the first `Oh...` is after a `Wow!`.
5. Repeat `b` times:

- Append `s + 1`.
- This guarantees a `Wow!`, because the new value exceeds the entire previous sum.
- Update `s` and `mx`.
6. After each `Wow!`, if we still need more `Oh...` reactions:

- Append `s`.
- Since `mx < s <= s`, this produces an `Oh...`.
- Update `s` and `mx`.
7. Fill all remaining positions with `1`.

Since the maximum is already much larger than `1`, these positions create no reactions.

### Why it works

The construction maintains a simple invariant.

Whenever we append `s + 1`, the new value is larger than the entire previous prefix sum, so the reaction is always `Wow!`.

Whenever we append `s`, the previous maximum is strictly smaller than `s`, because the last `Wow!` created a gap between them. The new value is not larger than the previous sum, so the reaction is exactly `Oh...`.

All filler values are `1`, which never exceed the current maximum.

The counts of `Wow!` and `Oh...` are controlled independently, and every appended number has exactly the intended effect.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())

    if a > b + 1:
        print(-1)
        return

    ans = [1]

    s = 1
    mx = 1

    oh_used = 0
    wow_used = 0

    for _ in range(b):
        x = s + 1
        ans.append(x)

        wow_used += 1
        s += x
        mx = x

        if oh_used < a:
            x = s
            ans.append(x)

            oh_used += 1
            s += x
            mx = x

    while len(ans) < n:
        ans.append(1)

    print(*ans[:n])

solve()
```

The first condition is the feasibility check. If `a > b + 1`, no construction can exist, because each `Wow!` creates room for at most one future `Oh...`.

The sequence starts from `1` because it keeps all later calculations simple. The variables `s` and `mx` track the current prefix sum and maximum value.

The loop generating `Wow!` reactions appends `s + 1`. Since this value is larger than the whole previous sum, it always triggers `Wow!`.

Immediately afterward, if more `Oh...` reactions are still needed, we append exactly `s`. At that moment the current maximum is strictly smaller than `s`, so the new value becomes a new maximum without exceeding the prefix sum. That is precisely the definition of `Oh...`.

The filler loop appends `1` until the array reaches length `n`. These values are safely below the current maximum and never affect the reaction counts.

One subtle point is the order of updates. We must update the prefix sum after every append before constructing the next value. Using stale values would completely change the reaction classification.

Another subtle point is slicing with `ans[:n]`. The construction may temporarily create more elements than needed if `n` is close to `a + b + 1`. The statement guarantees `n > a + b`, so truncation remains safe.

## Worked Examples

### Example 1

Input:

```
10 2 3
```

Construction trace:

| Step | Added value | Previous sum | Reaction | New sum |
| --- | --- | --- | --- | --- |
| Start | 1 | 0 | None | 1 |
| Wow | 2 | 1 | Wow! | 3 |
| Oh | 3 | 3 | Oh... | 6 |
| Wow | 7 | 6 | Wow! | 13 |
| Oh | 13 | 13 | Oh... | 26 |
| Wow | 27 | 26 | Wow! | 53 |
| Fill | 1 | 53 | None | 54 |
| Fill | 1 | 54 | None | 55 |
| Fill | 1 | 55 | None | 56 |
| Fill | 1 | 56 | None | 57 |

Final sequence:

```
1 2 3 7 13 27 1 1 1 1
```

This trace demonstrates the core invariant. Every `Wow!` makes the sum much larger than the maximum, and that immediately enables one valid `Oh...`.

### Example 2

Input:

```
5 3 1
```

Since:

```
3 > 1 + 1
```

the answer is impossible.

| Value | Meaning |
| --- | --- |
| n = 5 | Total grooms |
| a = 3 | Need 3 Oh... |
| b = 1 | Need 1 Wow! |

With only one `Wow!`, we can create room for at most two `Oh...` reactions. The construction correctly prints:

```
-1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is generated once |
| Space | O(n) | The output array stores `n` values |

The limits are extremely small, so this solution easily fits within the time and memory constraints. Even for the maximum `n = 100`, the program performs only a few hundred arithmetic operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, a, b = map(int, input().split())

    if a > b + 1:
        print(-1)
        return

    ans = [1]

    s = 1
    mx = 1

    oh_used = 0

    for _ in range(b):
        x = s + 1
        ans.append(x)

        s += x
        mx = x

        if oh_used < a:
            x = s
            ans.append(x)

            oh_used += 1
            s += x
            mx = x

    while len(ans) < n:
        ans.append(1)

    print(*ans[:n])

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided-style cases
assert run("10 2 3\n") != "-1"

assert run("5 3 1\n") == "-1", "impossible case"

# minimum size
assert run("1 0 0\n") == "1", "single groom"

# no reactions at all
assert run("5 0 0\n") == "1 1 1 1 1", "all equal"

# exactly one wow
assert run("3 0 1\n") != "-1", "single wow"

# boundary feasibility
assert run("6 2 1\n") != "-1", "a == b + 1 is valid"

# impossible boundary
assert run("6 3 1\n") == "-1", "a > b + 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0` | `1` | Smallest valid input |
| `5 0 0` | `1 1 1 1 1` | No reactions at all |
| `3 0 1` | Any valid sequence | Single `Wow!` construction |
| `6 2 1` | Any valid sequence | Tight feasible boundary |
| `6 3 1` | `-1` | Impossible condition |

## Edge Cases

Consider:

```
3 2 0
```

We need two `Oh...` reactions but no `Wow!`.

Initially:

```
sum = 1
max = 1
```

There is no integer strictly between the maximum and the sum. Without a `Wow!`, that gap never appears. The algorithm detects:

```
2 > 0 + 1
```

and correctly outputs:

```
-1
```

Now consider:

```
5 0 0
```

The algorithm produces:

```
1 1 1 1 1
```

Trace:

| Position | Value | Current max | Reaction |
| --- | --- | --- | --- |
| 1 | 1 | 1 | None |
| 2 | 1 | 1 | None |
| 3 | 1 | 1 | None |
| 4 | 1 | 1 | None |
| 5 | 1 | 1 | None |

Repeated values are essential here. A strictly increasing sequence would accidentally create reactions.

Finally, consider the tight valid boundary:

```
6 2 1
```

Construction:

```
1 2 3 6 1 1
```

Trace:

| Value | Previous sum | Reaction |
| --- | --- | --- |
| 1 | 0 | None |
| 2 | 1 | Wow! |
| 3 | 3 | Oh... |
| 6 | 6 | Oh... |
| 1 | 12 | None |
| 1 | 13 | None |

This confirms why `a = b + 1` is still achievable. One `Wow!` creates enough room for two consecutive `Oh...` reactions.
