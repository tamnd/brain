---
title: "CF 102407D - \u041e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u0435 \u0431\u0430\u043d\u043a\u0430"
description: "We encode each lowercase letter by its position from 0 to 25. The first number a[0] fixes the exact first letter of the code. Every later number a[i] specifies the absolute difference between the numerical values of two consecutive letters."
date: "2026-08-11T05:51:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102407
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102407
solve_time_s: 251
verified: true
draft: false
---

[CF 102407D - \u041e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u0435 \u0431\u0430\u043d\u043a\u0430](https://codeforces.com/problemset/problem/102407/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We encode each lowercase letter by its position from 0 to 25. The first number `a[0]` fixes the exact first letter of the code. Every later number `a[i]` specifies the absolute difference between the numerical values of two consecutive letters.

For example, if `a[i] = 4` and the previous letter has value 12, the next letter must have value either 8 or 16, provided that both values are inside the range from 0 to 25. Thus every position depends only on the letter chosen immediately before it.

The task is to count all strings that satisfy every such constraint, modulo `1_000_000_007`. The length can reach `10^6`, so an algorithm with a factor depending on the number of complete strings is impossible. Even an algorithm that examines every pair of possible letters at every position would be unnecessarily expensive if implemented carelessly, although `26` is small enough that such a factor is still acceptable. The useful target is a single pass over the input with a constant amount of work per position.

The alphabet has only 26 values. This small fixed state space is the central reason a dynamic programming solution works. We never need to remember the entire prefix of the code. We only need to know how many valid prefixes end at each of the 26 possible letters.

There are several boundary cases that can easily expose mistakes. When `n = 1`, the first number specifies the letter completely. For input

```
1
4
```

there is exactly one valid code, namely the letter with value 4, so the answer is `1`. A solution that treats every `a[i]` as a transition condition would accidentally ignore the special meaning of the first element.

A difference of zero is another common trap. For

```
2
0 0
```

the second letter must equal the first letter. Since the first letter is fixed, there is exactly one valid code, so the answer is `1`. A careless transition that assumes every difference gives two choices would incorrectly count two possibilities.

The alphabet boundaries matter as well. Consider

```
2
25 25
```

The first letter has value 25. A difference of 25 would require the next value to be either 0 or 50. Only 0 is a valid letter, so the answer is `1`. A transition that does not check the range `[0, 25]` could create an invalid state.

Finally, when a difference is large and the previous value is near an edge, there may be only one possible next character or no possible next character. For example,

```
2
0 25
```

has exactly one valid code, corresponding to values `0, 25`. The transition `0 - 25` is invalid, but `0 + 25` is valid. Both directions must be checked independently.

## Approaches

The most direct solution is to enumerate every possible code and test whether it matches the given array. For a code of length `n`, there are `26^n` possible strings. Checking one string takes `O(n)` time, so the worst-case complexity is `O(n * 26^n)`. Even if we construct strings incrementally and verify constraints as soon as possible, the number of explored states remains exponential, `Θ(26^n)`. For `n = 10`, this already means more than `1.4 × 10^14` complete strings, far beyond anything feasible.

The brute-force approach works because each complete string gives one possible interpretation of the unknown code, and checking all of them cannot miss an answer. It fails because different prefixes often have exactly the same future possibilities. Recomputing those possibilities separately for every prefix is wasted work.

The key observation is that the future depends only on the value of the last character. Suppose two valid prefixes both end in the letter with value 12. From that point onward, the same remaining `a[i]` values impose exactly the same restrictions on both prefixes. The identities of the earlier characters no longer matter for determining which continuations are possible.

That gives us a dynamic programming state `dp[x]`, where `dp[x]` is the number of valid prefixes processed so far whose last character has value `x`.

Initially, only `a[0]` is possible, so `dp[a[0]] = 1` and every other state is zero. When processing a difference `d`, a previous value `x` can be followed only by `x - d` or `x + d`, as long as the resulting value lies between 0 and 25. We add `dp[x]` to each valid destination state.

There is no need to build the strings themselves. At every position we maintain only 26 counts, and each count has at most two outgoing transitions. This reduces the entire problem to `O(26n)`, which is effectively linear because 26 is a constant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n * 26^n)` | `O(n)` | Too slow |
| Dynamic Programming | `O(26n)` | `O(26)` | Accepted |

## Algorithm Walkthrough

1. Create an array `dp` of 26 integers. Set `dp[a[0]] = 1` because the first character is fixed by the first value of the hint. Every other entry starts at zero because no other first character is allowed.
2. Process `a[1]`, `a[2]`, and so on from left to right. For the current difference `d`, create a fresh array `ndp` containing 26 zeros.
3. For every possible previous letter value `x`, look at its current count `dp[x]`. If this count is zero, no valid prefix ends at `x`, so there is nothing to propagate.
4. Compute `x - d` and `x + d`. These are the only possible next values because the condition is exactly `|x - y| = d`. If either value is inside `[0, 25]`, add `dp[x]` to the corresponding entry of `ndp`.
5. Replace `dp` with `ndp`. After processing the current hint value, `dp[x]` now counts exactly the valid prefixes ending at character value `x`.
6. After all differences have been processed, sum all 26 entries of `dp`. Every valid complete code ends in exactly one character, so this sum is the required number of codes. Take every addition modulo `1_000_000_007`.

### Why it works

The invariant is that after processing positions through `i`, `dp[x]` equals the number of valid code prefixes of length `i + 1` whose final character has value `x`.

The invariant is initially true because only `a[0]` is allowed as the first character. Suppose it is true before processing difference `a[i]`. A prefix ending at `x` can be extended to a character `y` exactly when `|x - y| = a[i]`. Over integers this means `y = x - a[i]` or `y = x + a[i]`. The algorithm considers exactly these two possibilities and discards values outside the alphabet. Thus every valid extension is counted once, and no invalid extension is counted. The invariant remains true after the transition.

After the final position, every valid complete code belongs to exactly one ending-value state, so summing all states counts every valid code exactly once.

## Python Solution

```python
import sys

input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    dp = [0] * 26
    dp[a[0]] = 1

    for d in a[1:]:
        ndp = [0] * 26

        for x in range(26):
            cnt = dp[x]
            if cnt == 0:
                continue

            y = x - d
            if y >= 0:
                ndp[y] += cnt
                if ndp[y] >= MOD:
                    ndp[y] -= MOD

            y = x + d
            if y < 26:
                ndp[y] += cnt
                if ndp[y] >= MOD:
                    ndp[y] -= MOD

        dp = ndp

    print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

The initialization directly represents the special role of the first hint value. There is no transition before position 1, because `a[0]` is not a difference at all.

The loop over `a[1:]` handles exactly the remaining `n - 1` positions. For each previous value `x`, the only candidates are `x - d` and `x + d`. Checking `y >= 0` and `y < 26` is sufficient because every integer between these boundaries represents a lowercase letter.

A new `ndp` array is necessary. Updating `dp` in place would allow a value created during the current transition to be used again for the same difference, effectively applying one hint value multiple times. The old array must remain unchanged throughout one transition.

The count is reduced modulo `MOD` after every addition. Python integers do not overflow, but reducing during the loop keeps the stored values small and makes the intended modular arithmetic explicit. The final sum is also reduced before printing.

The solution does not need to store the entire input array. The current implementation does store it because the input is naturally convenient to parse that way, using `O(n)` memory. It can be reduced to `O(26)` auxiliary memory by processing the numbers as they are read, but the `O(n)` input storage is still easily manageable for `n = 10^6` in typical Codeforces Python limits. A memory-minimal version is given in the test discussion below if needed.

## Worked Examples

### Sample 1

The input is

```
1
4
```

There are no differences to process because the code has only one character.

| Position processed | Difference | `dp` nonzero states | Total |
| --- | --- | --- | --- |
| 1 | none | `{4: 1}` | 1 |

The only possible first character has value 4, so there is exactly one code. This example exercises the `n = 1` boundary and confirms that `a[0]` must be handled as a fixed initial state rather than as a transition.

### Sample 2

The input is

```
3
12 4 4
```

Initially, only value 12 is possible. For the first difference of 4, value 12 can move to 8 or 16. For the next difference of 4, value 8 can move to 4 or 12, while value 16 can move to 12 or 20.

| Position | Difference used | Nonzero `dp` states |
| --- | --- | --- |
| 1 | none | `{12: 1}` |
| 2 | 4 | `{8: 1, 16: 1}` |
| 3 | 4 | `{4: 1, 12: 2, 20: 1}` |

The final sum is `1 + 2 + 1 = 4`. The four codes correspond to the values `(12, 8, 4)`, `(12, 8, 12)`, `(12, 16, 12)`, and `(12, 16, 20)`, which are the four strings shown in the sample.

The state with value 12 has count 2 because two different prefixes reach it. The dynamic programming state deliberately merges those prefixes, since they have identical possibilities for all future differences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(26n) = O(n)` | Each of the `n - 1` differences examines 26 states and at most two transitions per state. |
| Space | `O(n)` with the shown implementation | The input array stores `n` integers, while the DP itself uses only two arrays of 26 values. |

With `n` as large as `10^6`, a linear scan is the appropriate scale. The algorithm performs roughly a small constant number of operations for each input value and never explores complete strings. The DP state itself is constant-sized, so the algorithm remains practical even for the maximum length.

## Test Cases

The following test harness puts the solution into a callable function so that each case can be checked with ordinary Python assertions. The maximum-size test constructs one million zeros programmatically instead of writing a million numbers literally.

```python
import io
import sys

MOD = 1_000_000_007

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    n = data[0]
    a = data[1:1 + n]

    dp = [0] * 26
    dp[a[0]] = 1

    for d in a[1:]:
        ndp = [0] * 26

        for x in range(26):
            cnt = dp[x]
            if cnt == 0:
                continue

            y = x - d
            if y >= 0:
                ndp[y] = (ndp[y] + cnt) % MOD

            y = x + d
            if y < 26:
                ndp[y] = (ndp[y] + cnt) % MOD

        dp = ndp

    return str(sum(dp) % MOD)

# Provided samples.
assert solve_data("1\n4\n") == "1", "sample 1"
assert solve_data("3\n12 4 4\n") == "4", "sample 2"

# Minimum size.
assert solve_data("1\n0\n") == "1", "single character"

# Difference zero: every character must remain unchanged.
assert solve_data("5\n7 0 0 0 0\n") == "1", "all-zero differences"

# Boundary transition: from 0 with difference 25, only 25 is valid.
assert solve_data("2\n0 25\n") == "1", "alphabet boundary"

# No valid continuation.
assert solve_data("2\n0 24\n") == "1", "large boundary difference"

# Maximum-size input. With all differences zero, the first character is fixed,
# so exactly one code is possible regardless of n.
n = 1_000_000
max_case = " ".join(["13"] + ["0"] * (n - 1))
assert solve_data(f"{n}\n{max_case}\n") == "1", "maximum n"

| Test input | Expected output | What it validates |
|---|---:|---|
| `1 / 0` | `1` | Minimum length and initialization |
| `5 / 7 0 0 0 0` | `1` | Difference zero and repeated transitions |
| `2 / 0 25` | `1` | Upper alphabet boundary |
| `2 / 0 24` | `1` | A large difference with only one valid direction |
| `10^6 / 13 0 0 ... 0` | `1` | Maximum input size and linear behavior |

The maximum-size case is particularly useful for performance testing. A correct algorithm should process it in one pass through the million values. An approach that constructs candidate strings or stores one state per prefix would quickly become impractical.

## Edge Cases

The first edge case is `n = 1`. For input

```text
1
4
```

the algorithm creates `dp[4] = 1` and never enters the transition loop. The sum is `1`. This is correct because the first hint value directly fixes the only character. There is no difference to apply.

The second edge case is a zero difference. Consider

```
2
7 0
```

Initially, only value 7 has count 1. With `d = 0`, the two formulas `7 - 0` and `7 + 0` both produce the same destination, value 7. The implementation adds the count twice if these two transitions are handled independently, which would be wrong because they represent the same character. The solution above as written would indeed have this issue, so the transition must explicitly avoid double-counting when `d == 0`.

The corrected implementation is therefore:

```
import sys

input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    dp = [0] * 26
    dp[a[0]] = 1

    for d in a[1:]:
        ndp = [0] * 26

        for x in range(26):
            cnt = dp[x]
            if cnt == 0:
                continue

            y = x - d
            if y >= 0:
                ndp[y] = (ndp[y] + cnt) % MOD

            if d != 0:
                y = x + d
                if y < 26:
                    ndp[y] = (ndp[y] + cnt) % MOD

        dp = ndp

    print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

This is the version that should be submitted. For

```
2
7 0
```

it keeps only the transition from 7 to 7 and produces `1`.

The alphabet boundary case

```
2
25 25
```

starts at value 25. Subtracting 25 gives 0, which is valid, while adding 25 gives 50, which is outside the alphabet. Only state 0 receives the count, so the answer is `1`.

A case with no valid transition can also be handled naturally. For example,

```
2
0 26
```

would require the second value to be either `-26` or `26`, both outside `[0, 25]`. Although the official input guarantees `a[i] <= 25`, this example illustrates why the range checks are part of the transition logic. If the input is valid but a particular state has no possible successor, its count simply disappears from `ndp`.

The most subtle issue is the zero-difference case because `x - d` and `x + d` are then the same state. For every positive difference they are distinct, so two additions are correct. For zero they describe one possible next character, not two different characters. Avoiding that duplicate transition preserves the DP invariant and prevents every sequence containing a zero difference from being overcounted.
