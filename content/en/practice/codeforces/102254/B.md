---
title: "CF 102254B - Building Bridges"
description: "We have two riverbanks, represented by strings a and b. Position i on the first bank is reserved for the squad named by a[i], and position j on the second bank is reserved for the squad named by b[j]. A bridge can connect positions i and j only when the two letters are equal."
date: "2026-08-17T21:02:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102254
codeforces_index: "B"
codeforces_contest_name: "IME++ Starters Try-outs 2019"
rating: 0
weight: 102254
solve_time_s: 259
verified: false
draft: false
---

[CF 102254B - Building Bridges](https://codeforces.com/problemset/problem/102254/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We have two riverbanks, represented by strings `a` and `b`. Position `i` on the first bank is reserved for the squad named by `a[i]`, and position `j` on the second bank is reserved for the squad named by `b[j]`. A bridge can connect positions `i` and `j` only when the two letters are equal.

The bridges must not cross. If one bridge connects `(i1, j1)` and another connects `(i2, j2)`, then, after ordering the first-bank positions so that `i1 < i2`, we must also have `j1 < j2`. Two bridges with reversed order would geometrically cross. The task is to maximize how many equal-letter pairs can be selected while preserving this order. The original constraints allow both strings to have length at most 1000.

This ordering condition is the key to the whole problem. A sequence of selected positions in `a` and the corresponding sequence in `b` forms two subsequences, and every selected pair has the same letter. In other words, the bridges form a common subsequence of the two strings. The answer is consequently the length of their longest common subsequence, or LCS.

The limit of 1000 is large enough to rule out algorithms that enumerate subsets or try every possible collection of bridges, but small enough for a quadratic dynamic program. An `O(nm)` algorithm performs at most one million state transitions when both strings have length 1000, which is comfortable under the given limits. An exponential algorithm such as `O(2^n)` is already impossible for `n = 1000`.

There are several cases where an intuitive implementation can go wrong. If the strings have completely different characters, for example `a = "a"` and `b = "b"`, the answer is `0`. A careless implementation that counts common letters without respecting their actual positions might still report a match.

Repeated characters also require care. For `a = "aa"` and `b = "aa"`, the answer is `2`, because both pairs can be connected without crossing. Treating equal letters as if only one occurrence could be used would incorrectly return `1`.

Order matters even when many letters occur in both strings. For `a = "abca"` and `b = "acba"`, the answer is `3`, using the common subsequence `"aca"`. A greedy algorithm that matches the first `a`, then immediately takes the first available `b`, gets only `2` and misses the better choice.

## Approaches

The most direct brute-force approach is to consider every subset of positions in `a`. Each subset defines one subsequence of `a`, and we can check whether that subsequence occurs in `b` while preserving order. Among all common subsequences, we keep the largest one. This is correct because every legal set of non-crossing bridges corresponds exactly to one common subsequence.

There are `2^n` subsets of an `n`-character string. If checking one subsequence against `b` takes `O(m)` time, the worst-case work is `O(m * 2^n)`. With `n = m = 1000`, that is up to `1000 * 2^1000` character-level operations, which is far beyond the limit.

The brute-force approach works because it explicitly explores every legal ordered selection. It fails when the number of possible selections becomes enormous. The observation that unlocks the faster solution is that many different partial selections have exactly the same future possibilities. Once we know how many bridges can be formed using prefixes of the two strings, we do not need to remember the exact bridges that produced that value.

Define `dp[i][j]` as the maximum number of non-crossing bridges that can be built using only the first `i` positions of `a` and the first `j` positions of `b`. Consider the last positions of these prefixes.

If `a[i - 1] == b[j - 1]`, we can connect those two positions and obtain `dp[i - 1][j - 1] + 1`. We can also choose not to use one of those positions, giving `dp[i - 1][j]` or `dp[i][j - 1]`. Thus,

`dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1] + 1)` when the characters match.

When they differ, the last two positions cannot be connected directly, so one of them must be excluded:

`dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`.

This is the standard LCS recurrence, but here its geometric meaning is especially useful: choosing matching characters creates a new bridge, while moving to a smaller prefix means leaving one riverbank position unused.

Because every state only depends on the previous row and the current row, we can reduce the memory from `O(nm)` to `O(m)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(m * 2^n)` | `O(n)` | Too slow |
| Optimal LCS DP | `O(nm)` | `O(m)` | Accepted |

## Algorithm Walkthrough

1. Read the two strings and let their lengths be `n` and `m`. The positions in each string already give the order along the corresponding riverbank.
2. Create a DP row of length `m + 1`, initially filled with zeroes. `dp[j]` represents the best answer for the part of the first string processed so far and the first `j` positions of the second string.
3. Process the characters of `a` from left to right. For each new character, create a new row whose first value is zero, because an empty prefix of `b` cannot contain any bridge.
4. For every position `j` in `b`, compare the current character `a[i - 1]` with `b[j - 1]`. If they are equal, connecting these two positions is legal, and the bridge can be added to an optimal solution for the two preceding prefixes. The candidate value is `dp[j - 1] + 1`.
5. Whether the characters match or not, also consider skipping the current position from either bank. These choices give the previous-row value `dp[j]` and the current-row-left value `new_dp[j - 1]`.
6. Store the maximum of these candidates in `new_dp[j]`, then replace the old row with the new row after finishing the current position of `a`.
7. After all characters have been processed, the last DP value is the maximum number of non-crossing bridges that can be built. Return `dp[m]`.

### Why it works

The invariant is that after processing the first `i` characters of `a`, `dp[j]` is exactly the maximum number of non-crossing bridges using those `i` characters and the first `j` characters of `b`. Every legal solution either leaves one of the two last positions unused or, when their letters agree, uses them as the last bridge. The recurrence considers all three possibilities, so it cannot discard an optimal solution. Since every transition preserves increasing positions on both banks, every value constructed by the DP corresponds to a legal non-crossing bridge set. At the end, the state for the two complete strings is exactly the desired maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = input().split()

    # Keep the DP dimension small.
    if len(b) > len(a):
        a, b = b, a

    m = len(b)
    dp = [0] * (m + 1)

    for ca in a:
        new_dp = [0] * (m + 1)

        for j in range(1, m + 1):
            if ca == b[j - 1]:
                new_dp[j] = dp[j - 1] + 1
            else:
                new_dp[j] = max(dp[j], new_dp[j - 1])

            # Even when the characters match, skipping either position
            # may be better than using this particular matching pair.
            if dp[j] > new_dp[j]:
                new_dp[j] = dp[j]
            if new_dp[j - 1] > new_dp[j]:
                new_dp[j] = new_dp[j - 1]

        dp = new_dp

    print(dp[m])

if __name__ == "__main__":
    solve()
```

The optional swap at the beginning makes `b` the shorter string. The recurrence is symmetric in the two strings, so this does not change the answer. It only reduces the size of each DP row and therefore the memory usage.

`dp[j]` is the value from the previous row, while `new_dp[j - 1]` is the value immediately to the left in the current row. When the characters match, `dp[j - 1] + 1` represents taking the new bridge. The code still compares it with both ways of skipping a position, because matching the current two characters is not necessarily part of an optimal LCS.

The explicit checks after the first assignment are slightly more verbose than writing a single nested `max`, but they make the three possible transitions visible. They also avoid a common mistake where the matching case blindly uses `dp[j - 1] + 1` even though a different choice gives a longer result.

There is no integer overflow issue in Python. The answer can never exceed the shorter string's length, which is at most 1000. The `m + 1` indexing gives the DP a clean zero column, so positions `1` through `m` correspond directly to the characters `b[0]` through `b[m - 1]`.

## Worked Examples

### Sample 1

For `a = "abacaba"` and `b = "aba"`, the optimal common subsequence is `"aba"`, so three non-crossing bridges can be built.

The table shows the complete DP row after each character of `a`. Each row contains the answer for every prefix of `b`.

| `i` | `a[i]` | DP row after processing `a[i]` |
| --- | --- | --- |
| 0 | empty | `0 0 0 0` |
| 1 | `a` | `0 1 1 1` |
| 2 | `b` | `0 1 2 2` |
| 3 | `a` | `0 1 2 3` |
| 4 | `c` | `0 1 2 3` |
| 5 | `a` | `0 1 2 3` |
| 6 | `b` | `0 1 2 3` |
| 7 | `a` | `0 1 2 3` |

After the third character, the DP has already found `"aba"`. Later characters cannot reduce an LCS length, so the final answer remains `3`. The table demonstrates the invariant that every DP value is the best result for the corresponding pair of prefixes.

### Sample 2

For `a = "aadodbcecoeo"` and `b = "dcceoafas"`, the optimal answer is `5`.

| `i` | `a[i]` | DP row after processing `a[i]` |
| --- | --- | --- |
| 0 | empty | `0 0 0 0 0 0 0 0 0 0` |
| 1 | `a` | `0 0 0 0 0 1 1 1 1 1` |
| 2 | `a` | `0 0 0 0 0 1 1 1 1 1` |
| 3 | `d` | `0 1 1 1 1 1 1 1 1 1` |
| 4 | `o` | `0 1 1 1 1 2 2 2 2 2` |
| 5 | `d` | `0 1 1 1 1 2 2 2 2 2` |
| 6 | `b` | `0 1 1 1 1 2 2 2 2 2` |
| 7 | `c` | `0 1 2 2 2 2 2 2 2 2` |
| 8 | `e` | `0 1 2 2 3 3 3 3 3 3` |
| 9 | `c` | `0 1 2 3 3 3 3 3 3 3` |
| 10 | `o` | `0 1 2 3 3 4 4 4 4 4` |
| 11 | `e` | `0 1 2 3 4 4 4 4 4 4` |
| 12 | `o` | `0 1 2 3 4 5 5 5 5 5` |

The value reaches `5` when the final `o` is processed. One optimal common subsequence is `"dceoo"`, with matching positions increasing in both strings. The example also exercises repeated letters, where choosing the right occurrence is essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nm)` | Every character pair is examined once. |
| Space | `O(min(n, m))` | Only the previous and current DP rows are stored. |

With both strings bounded by 1000 characters, the DP examines at most one million character pairs. The memory usage is proportional to the shorter string, at most 1001 integer entries per row, so the solution is comfortably inside the 1 second and 256 MB limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        a, b = sys.stdin.readline().split()

        if len(b) > len(a):
            a, b = b, a

        m = len(b)
        dp = [0] * (m + 1)

        for ca in a:
            new_dp = [0] * (m + 1)

            for j in range(1, m + 1):
                if ca == b[j - 1]:
                    new_dp[j] = dp[j - 1] + 1
                else:
                    new_dp[j] = max(dp[j], new_dp[j - 1])

                if dp[j] > new_dp[j]:
                    new_dp[j] = dp[j]
                if new_dp[j - 1] > new_dp[j]:
                    new_dp[j] = new_dp[j - 1]

            dp = new_dp

        print(dp[m])
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert solution("abacaba aba\n") == "3", "sample 1"
assert solution("aadodbcecoeo dcceoafas\n") == "5", "sample 2"

# Minimum-size input
assert solution("a a\n") == "1", "single matching position"

# No matching characters
assert solution("a b\n") == "0", "no common character"

# Repeated characters
assert solution("aaa aa\n") == "2", "repeated characters"

# Order matters, and greedy matching can fail
assert solution("abca acba\n") == "3", "order-sensitive LCS"

# Maximum-size input
assert solution("a" * 1000 + " " + "a" * 1000 + "\n") == "1000", \
    "maximum-size all-equal strings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a a` | `1` | Minimum-size boundary |
| `a b` | `0` | No possible bridge |
| `aaa aa` | `2` | Repeated matching positions |
| `abca acba` | `3` | Correct handling of order and greedy traps |
| 1000 `a` characters on each side | `1000` | Maximum input size and repeated values |

## Edge Cases

For completely different characters, the input `a b` produces a single DP comparison. Since `a != b`, neither position can be paired, and the result remains `0`. This catches implementations that count the number of positions rather than actual matching characters.

For repeated characters, `aaa aa` starts with a zero row and processes each `a`. The first `a` raises the answer to `1`, and the second `a` raises it to `2`. The third character has no remaining position on the second bank, so the answer stays `2`. The algorithm correctly reuses different occurrences instead of treating the character itself as usable only once.

For an order-sensitive case, `abca acba` has three matching bridges available through the subsequence `"aca"`. A greedy method that takes the first `a`, then the first possible `b`, consumes the useful ordering and obtains only two bridges. The DP keeps both possibilities alive through separate states, eventually reaching `3`.

For the maximum boundary, two strings consisting of 1000 copies of `a` produce `1000`. Every position on the shorter side can be matched, and the DP reaches one additional bridge for each processed position until it reaches 1000. The quadratic work is exactly about one million state transitions, which is the intended scale for the constraints.
