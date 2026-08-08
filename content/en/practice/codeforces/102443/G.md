---
title: "CF 102443G - Too Many Hyphens"
description: "We have a string made only of + and -. We may insert curly braces anywhere, without changing the original characters."
date: "2026-08-09T01:43:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "G"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 110
verified: true
draft: false
---

[CF 102443G - Too Many Hyphens](https://codeforces.com/problemset/problem/102443/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string made only of `+` and `-`. We may insert curly braces anywhere, without changing the original characters. After insertion, the braces themselves must form a valid parenthesis sequence: scanning from left to right, the number of `{` characters must never be smaller than the number of `}`, and the two counts must be equal at the end.

The reason for inserting braces is to separate every pair of adjacent hyphens. In the final string, between every two consecutive original `-` characters there must be at least one brace. Consecutive `+` characters do not need any special treatment.

Among all valid strings, we only keep those using the minimum possible number of braces. These are the optimal escaped strings. They are sorted lexicographically using the order `+ < - < { < }`, and the task is to output the `k`-th one. If fewer than `k` optimal strings exist, we print `Overflow`. The original input string has at most 60 characters, while `k` can be as large as `10^18`.

The first useful quantity is the number `r` of positions where two consecutive original characters are both `-`. Every such position must contain at least one inserted brace. Thus at least `r` braces are necessary. However, braces have to form a balanced sequence, so their total number must be even. The minimum number of braces is consequently the smallest even number at least `r`.

For example, with `s = "--"`, there is one forbidden adjacency, so at least one brace is needed. One brace cannot form a balanced sequence, so the optimum uses two braces. The three optimal strings are `-{-}`, `-{}-`, and `{-}-`. A careless solution that simply uses one brace at the required position would violate the balanced-brace condition.

Another edge case is a string with no consecutive hyphens. For example, with

```
-+-+
2
```

there is nothing to escape, so the only optimal string is `-+-+`. Since `k = 2`, the correct output is `Overflow`. A solution that always inserts a pair of braces would be wrong because the task asks for the minimum number of inserted braces. This is also one of the official samples.

The empty-gap positions at the beginning and end of the string are also legal places for braces. For `s = "--"`, the string `{-}-` is optimal even though its braces are not between the two hyphens. The opening brace is before the first hyphen and the closing brace is between the hyphens, so the required gap is still protected and the braces remain balanced. An implementation that only considers inserting braces directly into bad gaps would miss this string.

The length bound of 60 is small enough for a dynamic program whose state has several dimensions, but far too large for enumerating all possible escaped strings. The value `k <= 10^18` also tells us that counts should be capped at `10^18`: once a state has at least that many completions, its exact larger value can never affect the answer.

## Approaches

A direct brute-force solution could try every possible way of inserting braces, check whether the resulting brace sequence is balanced, check every consecutive pair of hyphens, and then retain only strings with the minimum number of braces. This is correct because every possible escaped string is considered. The problem is the search space. There are up to 60 original characters and, in the worst case, up to 60 braces in an optimal solution. A character-by-character search tree with four possible output characters has depth up to 120, giving the crude upper bound

[
1 + 4 + 4^2 + \dots + 4^{120}
= \frac{4^{121}-1}{3},
]

which is roughly `2^240 / 3` nodes. Even a much more careful brute-force enumeration of valid balanced brace strings is exponential. For 60 braces, there are already Catalan-number-scale possibilities, far beyond what can be generated in one second.

The brute-force works because every choice can be checked locally and the final validity conditions are simple. It fails because many different prefixes have exactly the same future possibilities. For example, once we know how many original characters have been consumed, how many braces have been inserted, the current brace balance, and whether the current gap has already received a brace, the exact history before that point no longer matters.

That observation turns the problem into a finite-state dynamic program. We count the number of optimal completions from each such state. Once those counts are available, lexicographic unranking becomes straightforward: at each position we consider the possible next characters in the required order `+`, `-`, `{`, `}`, ask how many complete optimal strings begin with each choice, and either take that choice or skip its entire block.

The only subtle point is how to represent the gaps between original characters. Suppose `i` original characters have already been emitted. We are currently filling the gap immediately before `s[i]`, or the final gap when `i == n`. If `s[i-1]` and `s[i]` are both `-`, this gap must receive at least one brace before we are allowed to emit `s[i]`. A single boolean records whether that has already happened.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `n` | Exponential in `n` | Too slow |
| Optimal | `O(n B²)` | `O(n B²)` | Accepted |

Here `B` is the minimum number of braces and `B <= 60`.

## Algorithm Walkthrough

1. Count every adjacent pair `s[i - 1] = s[i] = '-'`. Call this number `r`. Every such gap needs at least one brace, so no valid solution can use fewer than `r` braces.
2. Compute `B`, the minimum number of braces, as the smallest even number greater than or equal to `r`. Braces form a balanced parenthesis sequence, so their total number must be even. The value `B` is always achievable: distribute at least one brace to every required gap and use the remaining braces to complete a balanced sequence.
3. Define a dynamic programming state `(i, balance, used, has)`. Here `i` is the number of original characters already emitted, `balance` is the number of currently unmatched `{` characters, `used` is the total number of inserted braces so far, and `has` tells whether the current gap already contains at least one brace.
4. From a state, consider inserting `{`. This is legal when fewer than `B` braces have been used. It increases `balance`, increases `used`, and marks the current gap as having a brace.
5. Consider inserting `}`. This is legal only when `balance > 0` and fewer than `B` braces have been used. It decreases `balance`, increases `used`, and also marks the current gap as having a brace. A closing brace cannot be emitted at balance zero because that would make the brace sequence invalid.
6. Consider emitting the next original character `s[i]`. This is legal only if either the current gap is not one of the required hyphen gaps, or `has` is already true. After emitting the original character, advance `i` and reset `has` to false because we have entered the next gap.
7. The terminal state is reached when all original characters have been emitted. At that point, only states with exactly `B` inserted braces and balance zero are valid. The final gap is allowed to contain braces, so the DP continues inserting braces even when `i == n`.
8. Memoize the number of valid completions from every state. Since `k` is at most `10^18`, cap every count at `10^18`. Counts larger than this are indistinguishable for deciding which side of `k` they lie on.
9. Before constructing the answer, inspect the count of the initial state. If it is smaller than `k`, print `Overflow`.
10. Otherwise, construct the answer from left to right. At each state, inspect possible next characters in lexicographic order. For `+` or `-`, there is at most one original-character choice. For `{` and `}`, the DP gives the number of completions after taking that character. If a branch contains fewer than `k` strings, subtract that count from `k` and try the next character. Otherwise, append the character and move to that state.

The invariant is that every DP state represents exactly the information that can affect future validity: how much of the original string remains, how many braces are available, the current parenthesis balance, and whether the current required gap has already been protected. Consequently, every legal continuation is counted exactly once. During unranking, lexicographic order partitions all completions into consecutive blocks according to their next character, so skipping complete blocks and descending into the block containing `k` always selects the correct string.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10**18

def solve():
    s = input().strip()
    k = int(input())
    n = len(s)

    required = 0
    for i in range(1, n):
        if s[i - 1] == '-' and s[i] == '-':
            required += 1

    B = required
    if B % 2:
        B += 1

    memo = {}

    def add_cap(a, b):
        x = a + b
        return LIMIT if x > LIMIT else x

    def count(i, balance, used, has):
        key = (i, balance, used, has)
        if key in memo:
            return memo[key]

        if used > B or balance > B:
            return 0

        if i == n:
            if used == B and balance == 0:
                return 1

            if used == B:
                return 0

        ans = 0

        # Try inserting '{'.
        if used < B:
            ans = add_cap(ans, count(i, balance + 1, used + 1, True))

        # Try inserting '}'.
        if used < B and balance > 0:
            ans = add_cap(ans, count(i, balance - 1, used + 1, True))

        # Try emitting the next original character.
        if i < n:
            required_gap = (
                i > 0 and
                s[i - 1] == '-' and
                s[i] == '-'
            )

            if not required_gap or has:
                ans = add_cap(ans, count(i + 1, balance, used, False))

        memo[key] = ans
        return ans

    total = count(0, 0, 0, False)

    if total < k:
        print("Overflow")
        return

    ans = []
    i = 0
    balance = 0
    used = 0
    has = False

    while not (i == n and used == B and balance == 0):
        choices = []

        # Original character, if legal.
        if i < n:
            required_gap = (
                i > 0 and
                s[i - 1] == '-' and
                s[i] == '-'
            )

            if not required_gap or has:
                choices.append((s[i], (i + 1, balance, used, False)))

        # Opening brace.
        if used < B:
            choices.append(('{', (i, balance + 1, used + 1, True)))

        # Closing brace.
        if used < B and balance > 0:
            choices.append(('}', (i, balance - 1, used + 1, True)))

        choices.sort(key=lambda x: x[0])

        for ch, state in choices:
            ni, nb, nu, nh = state
            ways = count(ni, nb, nu, nh)

            if ways < k:
                k -= ways
            else:
                ans.append(ch)
                i, balance, used, has = state
                break

    print(''.join(ans))

if __name__ == "__main__":
    solve()
```

The first loop counts the exact number of gaps that must contain braces. From that value, `B` is obtained by rounding up to an even number. The special case `B = 0` needs no separate handling because the same DP naturally allows only the original string.

The `count` function is the central dynamic program. The `i == n` case is handled before the transition logic because there is no original character left to emit, but braces may still have to be placed in the final gap. A state is accepting only when all `B` braces have been used and the balance is zero.

The `required_gap` expression checks precisely the gap between `s[i - 1]` and `s[i]`. This is why the condition uses `i > 0` and `i < n` implicitly through the surrounding branch. The `has` flag is reset only after an original character is emitted, so braces inserted before that character all belong to the same gap.

The lexicographic construction deliberately considers the original character, `{`, and `}` separately and sorts them by their actual character values. Since `+ < - < { < }`, Python's normal string ordering already gives the required order.

There is no integer-overflow problem in Python, but the explicit cap at `10^18` keeps the number of distinct integer values in the DP bounded and mirrors the only precision that the unranking process needs. The cap is applied after every addition, not after the entire DP has been evaluated.

## Worked Examples

For the first official sample, `s = "++--"` and `k = 2`. There is one bad gap, so the minimum number of braces is two. The optimal strings are ordered as `++-{-}`, `++-{}-`, `++{-}-`, `+{+-}-`, and `{++-}-`. The second one is consequently the answer. The sample and this ordering are given in the original statement.

| `i` | `balance` | `used` | `has` | Chosen prefix |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | false | `+` |
| 1 | 0 | 0 | false | `++` |
| 2 | 0 | 0 | false | `++-` |
| 3 | 0 | 0 | false | `++-` |
| 3 | 1 | 1 | true | `++-{` |
| 4 | 0 | 2 | false | `++-{}` |
| 4 | 0 | 2 | false | `++-{}-` |

At the first two positions, the only optimal strings beginning with those original pluses form the lexicographically earliest block. At the first hyphen, the first candidate is also forced. Inside the required gap, choosing `}` immediately is impossible because the balance is zero, so `{` is selected. Once the opening brace has been inserted, the next original hyphen is lexicographically smaller than `}`, so the algorithm emits it before closing the pair. This produces `++-{}-`.

For the second official sample, `s = "-+-+"`. There are no consecutive hyphens, so `B = 0`. The only optimal escaped string is the original string itself. Since `k = 2`, the initial DP count is one and the algorithm immediately prints `Overflow`.

| `i` | `balance` | `used` | `has` | Chosen prefix |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | false | `-` |
| 1 | 0 | 0 | false | `-+` |
| 2 | 0 | 0 | false | `-+-` |
| 3 | 0 | 0 | false | `-+-+` |

Because no braces are permitted in an optimal string when zero braces suffice, there is exactly one completion. The requested second completion does not exist.

## Complexity Analysis

Let `n <= 60` be the original string length and `B <= 60` be the minimum number of braces.

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n B²)` | There are `O(n B²)` relevant states and each has constant-size transitions. |
| Space | `O(n B²)` | The memoization table stores one capped count for each state. |

The additional boolean `has` only multiplies the state count by two, so it does not change the asymptotic complexity. With `n` and `B` both at most 60, the number of states is comfortably below one million, which fits the 1 second and 512 MB limits of the problem.

## Test Cases

```python
import sys
import io
from functools import lru_cache

LIMIT = 10**18

def solve_string(inp: str) -> str:
    data = inp.strip().split()
    s = data[0]
    k = int(data[1])
    n = len(s)

    required = sum(
        1 for i in range(1, n)
        if s[i - 1] == '-' and s[i] == '-'
    )

    B = required if required % 2 == 0 else required + 1

    @lru_cache(None)
    def count(i, balance, used, has):
        if used > B or balance > B:
            return 0

        if i == n:
            return int(used == B and balance == 0)

        ans = 0

        if used < B:
            ans = min(
                LIMIT,
                ans + count(i, balance + 1, used + 1, True)
            )

            if balance > 0:
                ans = min(
                    LIMIT,
                    ans + count(i, balance - 1, used + 1, True)
                )

        required_gap = (
            i > 0 and
            s[i - 1] == '-' and
            s[i] == '-'
        )

        if not required_gap or has:
            ans = min(
                LIMIT,
                ans + count(i + 1, balance, used, False)
            )

        return ans

    if count(0, 0, 0, False) < k:
        return "Overflow"

    ans = []
    i = balance = used = 0
    has = False

    while not (i == n and used == B and balance == 0):
        choices = []

        if i < n:
            required_gap = (
                i > 0 and
                s[i - 1] == '-' and
                s[i] == '-'
            )

            if not required_gap or has:
                choices.append(
                    (s[i], (i + 1, balance, used, False))
                )

        if used < B:
            choices.append(
                ('{', (i, balance + 1, used + 1, True))
            )

            if balance > 0:
                choices.append(
                    ('}', (i, balance - 1, used + 1, True))
                )

        choices.sort()

        for ch, state in choices:
            ways = count(*state)
            if ways < k:
                k -= ways
            else:
                ans.append(ch)
                i, balance, used, has = state
                break

    return ''.join(ans)

# Provided sample 1
assert solve_string("++--\n2\n") == "++-{}-", "sample 1"

# Provided sample 2
assert solve_string("-+-+\n2\n") == "Overflow", "sample 2"

# Minimum-size input
assert solve_string("+\n1\n") == "+", "minimum-size input"

# Boundary case: all optimal strings for "--" are
# -{-}, -{}-, {-}-
assert solve_string("--\n1\n") == "-{-}", "first lexicographic answer"
assert solve_string("--\n2\n") == "-{}-", "second lexicographic answer"
assert solve_string("--\n3\n") == "{-}-", "last lexicographic answer"
assert solve_string("--\n4\n") == "Overflow", "past last answer"

# Maximum-size input, all characters equal
assert solve_string("+" * 60 + "\n1\n") == "+" * 60, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `+\n1` | `+` | Minimum length and zero required braces |
| `--\n1` | `-{-}` | Required gap and lexicographic choice |
| `--\n3` | `{-}-` | Braces may occur outside the required gap |
| `--\n4` | `Overflow` | Exact boundary of the number of solutions |
| 60 pluses with `k = 1` | 60 pluses | Maximum input length and all-equal characters |

## Edge Cases

For `s = "--"` and `k = 1`, there is one required gap, so the minimum brace count is two. The first character of the lexicographically smallest solution is `-`, because `- < {`. After that hyphen, the required gap must contain a brace. Choosing `{` is possible and leaves the original second hyphen as the next character, since `- < }`. The remaining `}` is placed after the second hyphen, giving `-{-}`. The algorithm reaches exactly that state sequence and returns the first solution.

For `s = "--"` and `k = 3`, the first two candidates `-{-}` and `-{}-` are skipped during unranking. The remaining candidate begins with `{`, which is lexicographically larger than `-`, and is `{-}-`. This case catches the mistake of assuming every brace must be placed directly between the two hyphens.

For `s = "-+-+"`, there are no required gaps. The minimum brace count is zero, so inserting any braces would make the result non-optimal. The DP therefore has exactly one terminal completion, namely `-+-+`. With `k = 2`, the initial count is smaller than `k`, so the algorithm correctly prints `Overflow`.

For a maximum-length string consisting entirely of pluses, such as 60 plus signs, there are no required gaps and the optimal brace count is zero. The DP contains essentially one path through the original characters and returns the input unchanged. This exercises the upper length boundary without introducing unnecessary combinatorial complexity.

For a string consisting entirely of hyphens, every internal gap is required. With 60 hyphens there are 59 required gaps, so the optimal number of braces is 60, not 59. The extra brace is forced by the requirement that the total number of braces be even. This is the boundary that most directly tests the calculation of `B`, and the DP handles it without a special case because it treats the required-gap condition and the global balance condition independently.
