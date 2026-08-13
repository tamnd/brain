---
title: "CF 102307C - Common Subsequence"
description: "We have two DNA strings A and B, both of length n. The only characters that can appear are A, T, G, and C. We do not need to construct the common subsequence. We only need to decide whether its maximum possible length is at least 0.99n."
date: "2026-08-13T23:39:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "C"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 155
verified: true
draft: false
---

[CF 102307C - Common Subsequence](https://codeforces.com/problemset/problem/102307/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two DNA strings `A` and `B`, both of length `n`. The only characters that can appear are `A`, `T`, `G`, and `C`. We do not need to construct the common subsequence. We only need to decide whether its maximum possible length is at least `0.99n`.

A useful way to read the condition is to count what may be missing from the common subsequence. If its length is `L`, then each original string has `n - L` characters that are not used by that common subsequence. The requirement

`L >= 0.99n`

is equivalent to

`n - L <= 0.01n`.

Since `n - L` is an integer, we are allowed to lose at most `floor(n / 100)` characters from each string. Let

`k = floor(n / 100)`.

The target LCS length is then exactly `n - k`. If we can find a common subsequence of that length, the answer is positive.

The length bound of `10^5` rules out the ordinary `O(n^2)` LCS dynamic programming. At the maximum size that would mean about `10^10` DP cells, far beyond what a one-second limit can handle. The useful parameter is not the full length of the LCS, which is almost `n`, but the small number `k` of characters that we are allowed to discard. At `n = 10^5`, `k` is only `1000`.

There are several boundary cases that are easy to mishandle. When `n < 100`, we have `k = 0`, so no character may be discarded at all. For example,

```
A
T
```

has LCS length `0`, while the required length is `1`, so the correct output is `Not brothers :(`. A solution that accidentally rounds `0.99n` down would incorrectly accept it.

The exact threshold also matters when `n` is a multiple of `100`. For example,

```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATA
```

has length `100`, and its LCS is `99`. Since `99 = 0.99 * 100`, the correct answer is `Long lost brothers D:`. Requiring a length strictly greater than `0.99n` would reject a valid case.

One more boundary case is just below the threshold. With `n = 100`, if the LCS is `98`, two characters have to be discarded from each string, which is already too many. A careless implementation that checks whether the number of mismatches is at most one would confuse positional mismatches with deletions and can fail on shifted matches.

## Approaches

The straightforward solution is the standard LCS dynamic programming. Define `lcs[i][j]` as the longest common subsequence of the first `i` characters of `A` and the first `j` characters of `B`. If the current characters match, we can extend the diagonal state. Otherwise, we take the better result obtained by skipping a character from either string. This is correct because every common subsequence either uses the current pair of characters or skips at least one of them.

The problem is the size of the table. There are `(n + 1)^2` states, so for `n = 10^5` we get roughly `10^10` operations. The memory requirement would also be quadratic if the whole table were stored.

The key observation is that an acceptable common subsequence deletes only `k = floor(n / 100)` characters from either string. Instead of asking for the LCS over all possible prefixes, we can describe a state by how many characters have already been deleted from each string.

Let `dp[i][j]` represent the greatest number of characters that can already be matched after deleting `i` characters from `A` and `j` characters from `B`. Suppose the state currently contains `p = dp[i][j]` matched characters. The matched characters occupy the first `i + p` positions of `A` and the first `j + p` positions of `B`. The next characters to compare are consequently

`A[i + p]` and `B[j + p]`.

If they are equal, there is no reason to stop matching them. We can extend the common subsequence immediately and continue while the next pair is equal. If they differ, any common subsequence continuing from this state must discard either the next character of `A` or the next character of `B`. Those are exactly the two transitions

`dp[i + 1][j] = max(dp[i + 1][j], dp[i][j])`

and

`dp[i][j + 1] = max(dp[i][j + 1], dp[i][j])`.

This turns the large prefix-indexed LCS table into a table indexed only by deletion counts. There are only `(k + 1)^2` such states, and the matching phase moves directly through equal runs instead of processing every pair of string positions.

The brute-force solution works because every possible way of skipping characters is represented by the usual LCS recurrence, but it fails because it considers deletion counts all the way up to `n`. The observation that an accepted answer can delete only `1%` of the characters lets us keep only the small deletion frontier.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2)` | `O(n^2)` | Too slow |
| Optimal | `O(nk)` amortized, where `k = floor(n/100)` | `O(k^2)` | Accepted |

For `n = 10^5`, the useful parameter is `k <= 1000`, so the DP operates on roughly one million deletion states instead of ten billion prefix pairs. The matching runs are amortized over the frontier, giving the required bound for this approach.

## Algorithm Walkthrough

1. Read the two DNA strings and let `n` be their common length. Compute `k = n // 100`, because an accepted common subsequence may omit at most that many characters from either string.
2. Compute the required common subsequence length as `target = n - k`. This integer form avoids floating-point comparisons with `0.99`.
3. If `k` is zero, no deletion is allowed. The only possible common subsequence of length `n` is the entire string, so the answer is simply whether `A` and `B` are identical.
4. Create a DP table indexed by deletion counts. Initially `dp[0][0] = 0`, meaning that before deleting anything, no characters have been matched yet.
5. Process states `(i, j)` in increasing order. At a state, let `p = dp[i][j]`. The first `i` characters deleted from `A` and the first `j` characters deleted from `B`, together with the `p` matched characters, place the two current positions at `i + p` and `j + p`.
6. While both positions are inside their strings and the characters are equal, increase `p`. Matching these equal characters greedily is safe because they are the immediate next characters on both sides, so keeping them costs no deletion and can only move the common subsequence farther forward.
7. Store the extended value back in `dp[i][j]`. If it has reached `target`, an acceptable common subsequence has been found and we can immediately accept.
8. If `i < k`, propagate the current value to `dp[i + 1][j]`. This represents deleting the next unmatched character of `A`. If `j < k`, propagate it to `dp[i][j + 1]`, representing deletion of the next unmatched character of `B`. We never need states beyond `k`, because a solution using more than `k` deletions cannot satisfy the required LCS length.

The invariant is that `dp[i][j]` stores the furthest point reached by a valid matching that has used at most `i` deletions from `A` and at most `j` deletions from `B`. When the next characters match, extending the matching is always optimal for that state. When they do not match, every possible continuation must skip at least one of those two characters, and the two transitions enumerate exactly those possibilities. Consequently, every common subsequence using at most `k` deletions is represented by some DP path, and every DP path corresponds to a valid common subsequence. Reaching `n - k` matched characters is thus equivalent to satisfying the original condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

YES = "Long lost brothers D:"
NO = "Not brothers :("

def is_brothers(a: str, b: str) -> bool:
    n = len(a)
    k = n // 100
    target = n - k

    # If k == 0, we need an LCS of length n.
    if k == 0:
        return a == b

    # dp[i][j] = furthest number of characters matched after
    # deleting i characters from a and j characters from b.
    size = k + 2
    dp = [[0] * size for _ in range(size)]

    for i in range(k + 1):
        row = dp[i]

        for j in range(k + 1):
            p = row[j]

            x = i + p
            y = j + p

            while x < n and y < n and a[x] == b[y]:
                p += 1
                x += 1
                y += 1

            row[j] = p

            if p >= target:
                return True

            if i < k and p > dp[i + 1][j]:
                dp[i + 1][j] = p

            if j < k and p > row[j + 1]:
                row[j + 1] = p

    return False

def main() -> None:
    a = input().strip()
    b = input().strip()

    print(YES if is_brothers(a, b) else NO)

if __name__ == "__main__":
    main()
```

The first part of `is_brothers` converts the percentage requirement into an integer deletion budget. Since `n - LCS` is integral, `k = n // 100` is exactly the maximum number of characters that may be removed.

The `k == 0` branch handles all strings shorter than `100` directly. In this case the required LCS is the entire string, so equality of the two inputs is both necessary and sufficient.

The DP table has dimensions `(k + 2) x (k + 2)`. The extra row and column make the transitions safe when `i` or `j` is equal to `k`. We still process only states from `0` through `k`, because larger deletion counts cannot produce an acceptable answer.

The variables `x = i + p` and `y = j + p` are the actual current positions in the two strings. After a matching character is consumed, both positions and `p` advance together. This is less error-prone than recomputing the positions from scratch inside the loop.

The checks `i < k` and `j < k` are necessary before propagating to another deletion state. Without them, the code could access the extra boundary row or column as if it were a valid state and accidentally use more than the allowed number of deletions.

No floating-point arithmetic is used. Testing `p >= n - n // 100` is exactly equivalent to testing `p >= 0.99n`, including when `n` is not divisible by `100`.

Python integers do not have an overflow issue here, and every DP value is at most `n`. The main memory cost comes from the roughly one million DP entries when `n = 100000`, which stays comfortably below the memory limit.

## Worked Examples

For Sample 1,

```
A = GAATTGCGTACAATGC
B = GAATTGCGTACAATGC
```

the length is `16`, so `k = 16 // 100 = 0`. The required LCS length is `16`.

| n | k | target | Initial state | Result |
| --- | --- | --- | --- | --- |
| 16 | 0 | 16 | `dp[0][0] = 0` | `A == B`, accept |

The zero-deletion case is handled directly because the only way to obtain a common subsequence of length `16` is to keep every character. The two strings are identical, so the output is `Long lost brothers D:`.

For Sample 2,

```
A = CCATAGAGAA
B = CGATAGAGAA
```

the length is `10`, so again `k = 0` and the target is `10`.

| n | k | target | Comparison | Result |
| --- | --- | --- | --- | --- |
| 10 | 0 | 10 | `CCATAGAGAA != CGATAGAGAA` | reject |

The strings differ at their second character. Because the deletion budget is zero, that single difference cannot be removed or bypassed. Their LCS is at most `9`, below the required `10`, so the correct output is `Not brothers :(`.

A larger example shows the actual deletion DP. Consider

```
A = AAAAAAAAAA
B = AAAATAAAAA
```

Here `n = 10`, so the original problem would still have `k = 0`. To illustrate the DP mechanism itself, imagine the same structure at `n = 100`, with one differing character. Then `k = 1`, and deleting the extra character lets the two strings share `99` characters.

| State `(i,j)` | `p` before extension | Next positions | Action | `p` after extension |
| --- | --- | --- | --- | --- |
| `(0,0)` | 0 | `(0,0)` | Match equal prefix | 4 |
| `(1,0)` | 4 | `(5,4)` | Continue matching | 99 |
| `(0,1)` | 4 | `(4,5)` | Continue matching | 99 |

The first mismatch can be handled in two ways. Deleting the character from `A` produces state `(1,0)`, while deleting the character from `B` produces `(0,1)`. One of those paths reaches the required `99` matched characters. This demonstrates why the DP needs both deletion transitions instead of treating a mismatch as a simple positional mismatch.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nk)` | There are `O(k^2)` deletion states, and the equal-character extensions are amortized across the `k` deletion layers. |
| Space | `O(k^2)` | The DP table contains `(k + 2)^2` integer states. |

Here `k = floor(n / 100)`, so at the maximum `n = 100000`, we have `k = 1000`. The algorithm works with roughly one million deletion states instead of the roughly ten billion states of ordinary LCS. The memory consumption is also far below a full `n x n` LCS table.

## Test Cases

```python
import sys
import io

YES = "Long lost brothers D:"
NO = "Not brothers :("

def is_brothers(a: str, b: str) -> bool:
    n = len(a)
    k = n // 100
    target = n - k

    if k == 0:
        return a == b

    size = k + 2
    dp = [[0] * size for _ in range(size)]

    for i in range(k + 1):
        row = dp[i]

        for j in range(k + 1):
            p = row[j]

            x = i + p
            y = j + p

            while x < n and y < n and a[x] == b[y]:
                p += 1
                x += 1
                y += 1

            row[j] = p

            if p >= target:
                return True

            if i < k and p > dp[i + 1][j]:
                dp[i + 1][j] = p

            if j < k and p > row[j + 1]:
                row[j + 1] = p

    return False

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        a = sys.stdin.readline().strip()
        b = sys.stdin.readline().strip()
        return YES if is_brothers(a, b) else NO
    finally:
        sys.stdin = old_stdin

# Provided sample 1
assert run(
    "GAATTGCGTACAATGC\n"
    "GAATTGCGTACAATGC\n"
) == YES, "sample 1"

# Provided sample 2
assert run(
    "CCATAGAGAA\n"
    "CGATAGAGAA\n"
) == NO, "sample 2"

# Minimum size, equal strings.
assert run("A\nA\n") == YES, "minimum equal strings"

# Minimum size, different strings. k = 0, so no deletion is allowed.
assert run("A\nT\n") == NO, "minimum different strings"

# n = 100 and exactly one deletion is enough.
a = "A" * 100
b = "A" * 50 + "T" + "A" * 49
assert run(a + "\n" + b + "\n") == YES, "one deletion boundary"

# n = 100 and two deletions are necessary, which exceeds the budget.
a = "A" * 100
b = "A" * 50 + "TT" + "A" * 48
assert run(a + "\n" + b + "\n") == NO, "two deletions boundary"

# Maximum-size all-equal input.
a = "A" * 100000
assert run(a + "\n" + a + "\n") == YES, "maximum all-equal input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A / A` | `Long lost brothers D:` | Minimum size and zero-deletion acceptance |
| `A / T` | `Not brothers :(` | Minimum size and zero-deletion rejection |
| Length `100`, one inserted `T` | `Long lost brothers D:` | Exact `0.99n` boundary |
| Length `100`, two inserted `T` characters | `Not brothers :(` | One-deletion budget must not be exceeded |
| Two equal strings of length `100000` | `Long lost brothers D:` | Maximum input size and large DP boundary |

## Edge Cases

When `n < 100`, the deletion budget is zero. For the concrete input

```
A
T
```

we get `k = 1 // 100 = 0` and `target = 1`. The algorithm immediately compares the two complete strings and finds them different, so it returns `Not brothers :(`. No attempt is made to interpret the `0.99` threshold using floating-point rounding.

At exactly `n = 100`, one deletion is allowed. Consider

```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

The second string contains one extra `T` relative to the all-`A` string. The DP can reach the mismatch with state `(0,0)`, then either delete the `T` from the second string or delete the corresponding `A` from the first string. The resulting state has one deletion and can match the remaining `99` characters, so `p` reaches `target = 99` and the algorithm accepts.

If two deletions are required, the same mechanism reaches only `98` matched characters within the allowed deletion budget. For example, with

```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

the best common subsequence has length `98`. Since `k = 1`, the DP explores only states with at most one deletion from either string, so it cannot incorrectly accept a solution that needs two deletions. The result is `Not brothers :(`.

Identical strings exercise the opposite extreme. For the maximum-size input consisting of `100000` copies of `A` in both strings, the initial state greedily consumes the entire strings, producing `p = 100000`. Since the target is also `99000`, the algorithm returns immediately. This both confirms the matching invariant and avoids unnecessary exploration of the remaining deletion states.

The distinction between subsequence and substring also matters. A mismatch does not automatically mean that the strings are incompatible, because deleting a character can realign the two suffixes. The DP explicitly represents both possibilities by deleting from `A` or from `B`. That is why a positional Hamming-distance check is not a valid substitute for LCS here.
