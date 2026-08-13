---
title: "CF 102282J - \u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We have two strings, s1 and s2. The first string is the text that should have been copied, while the second is the text that was actually written. During copying, two kinds of mistakes are allowed: a character can be omitted, or a character can be replaced by another character."
date: "2026-08-13T09:16:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102282
codeforces_index: "J"
codeforces_contest_name: "2011, \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u0441\u0442 \u0421\u0413\u0410\u0423 \u043d\u0430 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b ACM ICPC"
rating: 0
weight: 102282
solve_time_s: 59
verified: true
draft: false
---

[CF 102282J - \u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102282/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two strings, `s1` and `s2`. The first string is the text that should have been copied, while the second is the text that was actually written. During copying, two kinds of mistakes are allowed: a character can be omitted, or a character can be replaced by another character. We need the minimum number of such mistakes that transforms `s1` into `s2`.

The distinction between the two operations matters. We are not allowed to insert a new character into `s1`. Consequently, `s2` cannot be longer than `s1`, and the problem guarantees that the given pair is valid under these rules. A replacement costs one error, regardless of which two letters are involved, and omitting one character also costs one error.

Both strings have length at most 1024. A quadratic algorithm therefore performs at most roughly one million state transitions, which is easily manageable within the one-second limit. An exponential search over all possible ways to align the strings, however, would become unnecessarily expensive even at this small length.

There are several boundary cases that can make a careless implementation incorrect. If the strings are already equal, such as

```
abc
abc
```

the answer is `0`. An implementation that counts positions where characters differ without considering the possibility of skipped characters is fine here, but it will fail on the more general cases.

A skipped character can occur at the beginning or at the end. For example,

```
abc
bc
```

has answer `1`, because the first `a` can be omitted. Similarly,

```
abc
ab
```

has answer `1`, because the final `c` can be omitted. An approach that only compares equal-length positions cannot represent either operation correctly.

A skipped character can also occur between two matching characters:

```
abc
ac
```

The answer is again `1`, because `b` is omitted. A greedy implementation that immediately treats `b` and `c` as a replacement would obtain `1` here by coincidence, but more complicated strings can make such a local decision suboptimal.

Finally, a replacement and a deletion can occur in the same prefix. For example,

```
abcd
acd
```

needs only one error, deleting `b`. A DP formulation must distinguish between matching the current characters, deleting the current character of `s1`, and replacing the current character. Treating every mismatch as a replacement loses the possibility of a cheaper alignment later.

## Approaches

The most direct brute-force idea is to enumerate all possible alignments between the two strings. When the current characters are equal, they can be matched. When they differ, there are several possibilities: replace the current character of `s1`, or delete it and try to match the same character of `s2` against a later position of `s1`. Exploring these choices recursively is correct because every valid sequence of mistakes corresponds to one path through this decision tree.

The problem with this approach is that the same suffixes are reached many times. A sequence containing many mismatches can branch repeatedly between replacement and deletion. In the worst case, the number of recursive paths grows exponentially, roughly as `O(2^n)` for a string of length `n`. With `n = 1024`, that is completely infeasible.

The key observation is that the result of a subproblem depends only on two positions, not on the entire history that led there. Suppose we have already processed the first `i` characters of `s1` and the first `j` characters of `s2`. Everything before those positions is finished, so the only relevant information is the pair `(i, j)`.

That turns the problem into dynamic programming. Let `dp[i][j]` be the minimum number of errors needed to transform the first `i` characters of `s1` into the first `j` characters of `s2`.

From state `(i, j)`, there are three possible ways to finish the current characters. We can match `s1[i-1]` with `s2[j-1]` at zero cost if they are equal, or replace `s1[i-1]` with `s2[j-1]` at cost one if they differ. We can also delete `s1[i-1]`, which moves to `(i-1, j)` and costs one.

There is no transition corresponding to insertion into `s1`, because insertion is not one of the permitted mistakes. This is the only significant difference from the usual full edit-distance problem.

The brute-force recursion works because it explicitly explores these same choices. Dynamic programming simply recognizes that many different recursive paths arrive at the same `(i, j)` state and stores its best answer once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n)` in the worst case | `O(n)` recursion depth | Too slow |
| Optimal DP | `O(nm)` | `O(nm)` | Accepted |

## Algorithm Walkthrough

1. Let `n = len(s1)` and `m = len(s2)`. Create a DP table where `dp[i][j]` represents the minimum number of errors needed to transform `s1[:i]` into `s2[:j]`.
2. Initialize `dp[0][0] = 0`. Transforming an empty prefix into another empty prefix requires no mistakes.
3. Initialize the first column with `dp[i][0] = i`. If the target prefix is empty, every one of the first `i` characters of `s1` must be deleted, so exactly `i` errors are necessary.
4. Initialize the first row with `dp[0][j]` as impossible for every `j > 0`. An empty source string cannot produce a non-empty target because insertion is not an allowed operation. We can represent these states with a very large value.
5. Process every state `(i, j)` with `i >= 1` and `j >= 1`. First consider consuming both current characters. If `s1[i-1] == s2[j-1]`, this costs zero additional errors. Otherwise, replacing one character with the other costs one.
6. Also consider deleting `s1[i-1]`. This changes the state from `(i, j)` to `(i-1, j)` and adds one error.
7. Take the smaller cost among the character match or replacement and the deletion. The resulting value is the optimal answer for `dp[i][j]`.
8. After filling the table, output `dp[n][m]`, which represents transforming the entire first string into the entire second string.

### Why it works

The invariant is that `dp[i][j]` always stores the minimum possible number of errors for transforming exactly the first `i` characters of `s1` into exactly the first `j` characters of `s2`.

Consider an optimal transformation for a state `(i, j)`. Its final action must either consume both last characters, which means they are matched or one is replaced by the other, or delete the last character of the source prefix. These are exactly the transitions considered by the recurrence. Since each transition adds precisely the cost of its final operation and the preceding state is itself optimal by the DP invariant, taking the minimum over the transitions gives the optimal value for `(i, j)`. The base cases cover all transformations involving an empty prefix, so the invariant holds for the entire table and the final state is the required minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s1 = input().strip()
    s2 = input().strip()

    n = len(s1)
    m = len(s2)

    INF = n + m + 1

    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(1, n + 1):
        dp[i][0] = i

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1

            # Match the two characters, or replace s1[i - 1].
            dp[i][j] = dp[i - 1][j - 1] + cost

            # Delete s1[i - 1].
            dp[i][j] = min(dp[i][j], dp[i - 1][j] + 1)

    print(dp[n][m])

if __name__ == "__main__":
    solve()
```

The first two input lines contain the two strings, so `strip()` is enough to remove their trailing newlines. There are no multiple test cases in the input format.

The DP table has `(n + 1) * (m + 1)` states. The first column is initialized to `i` because converting `s1[:i]` into an empty string requires deleting all `i` characters.

The first row is left at `INF` except for `dp[0][0]`. This is deliberate. A positive-length target cannot be constructed from an empty source using only deletion and replacement. Using an explicit impossible value prevents an accidental transition from inventing an insertion operation.

For each ordinary state, `cost` is either zero or one. If the current characters agree, consuming both of them costs nothing. If they disagree, consuming both corresponds to one replacement. The second transition deletes the current source character and leaves the target position unchanged.

The indices use `i - 1` and `j - 1` because `dp[i][j]` describes prefixes of lengths `i` and `j`. This is the main off-by-one detail in the implementation. Python integers have no overflow issue, and the largest meaningful answer is at most `n`, since the valid input guarantees that `s2` can be obtained by deleting characters and replacing characters from `s1`.

## Worked Examples

For the first sample, the strings are `flash` and `flesh`. The relevant DP states can be traced as follows.

| `i` | `j` | `s1[i-1]` | `s2[j-1]` | Match/replace cost | Delete cost | `dp[i][j]` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | f | f | 0 | 2 | 0 |
| 2 | 2 | l | l | 0 | 2 | 0 |
| 3 | 3 | a | e | 1 | 1 | 1 |
| 4 | 4 | s | s | 0 | 2 | 1 |
| 5 | 5 | h | h | 0 | 2 | 1 |

The two strings agree everywhere except for `a` versus `e`. Replacing `a` with `e` costs one error, so the final state is `dp[5][5] = 1`.

For the second sample, the strings are `bread` and `beer`. The lengths differ, so at least one deletion is required.

| `i` | `j` | `s1[i-1]` | `s2[j-1]` | Match/replace cost | Delete cost | `dp[i][j]` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | b | b | 0 | 2 | 0 |
| 2 | 2 | r | e | 1 | 1 | 1 |
| 3 | 2 | e | e | 0 | 1 | 1 |
| 4 | 3 | a | e | 1 | 2 | 1 |
| 5 | 4 | d | r | 1 | 2 | 2 |

The important transition is around the middle of the strings. Instead of replacing `r` with `e` and losing the useful alignment, the DP can delete `r` and then match the original `e`. The remaining characters can be aligned with one more replacement, giving the minimum of two errors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nm)` | There are `(n+1)(m+1)` states and each state takes constant time. |
| Space | `O(nm)` | The complete DP table is stored. |

With both strings limited to 1024 characters, the table contains only about 1.05 million states. Each state performs a constant number of integer operations, so the solution is comfortably within the stated limits. The memory consumption is also small compared with 128 MB.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.splitlines()
    s1 = data[0].strip()
    s2 = data[1].strip()

    n = len(s1)
    m = len(s2)

    INF = n + m + 1
    dp = [[INF] * (m + 1) for _ in range(n + 1)]

    dp[0][0] = 0

    for i in range(1, n + 1):
        dp[i][0] = i

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j - 1] + cost,
                dp[i - 1][j] + 1
            )

    return str(dp[n][m])

# Provided sample 1
assert solve_data("flash\nflesh\n") == "1", "sample 1"

# Provided sample 2
assert solve_data("bread\nbeer\n") == "2", "sample 2"

# Minimum-size strings, equal characters
assert solve_data("a\na\n") == "0", "equal one-character strings"

# Minimum-size strings, replacement
assert solve_data("a\nb\n") == "1", "one-character replacement"

# Deletion at the beginning
assert solve_data("abc\nbc\n") == "1", "deletion at beginning"

# Deletion at the end
assert solve_data("abc\nab\n") == "1", "deletion at end"

# Deletion in the middle
assert solve_data("abc\nac\n") == "1", "deletion in middle"

# All characters equal, maximum length
s = "a" * 1024
assert solve_data(s + "\n" + s + "\n") == "0", "maximum equal strings"

# Maximum number of deletions
s1 = "a" * 1024
s2 = "a"
assert solve_data(s1 + "\n" + s2 + "\n") == "1023", "maximum deletions"

# Several operations together
assert solve_data("abcdef\nacef\n") == "2", "multiple deletions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` / `a` | `0` | Minimum-size input and zero errors |
| `a` / `b` | `1` | Replacement transition |
| `abc` / `bc` | `1` | Deletion at the beginning |
| `abc` / `ab` | `1` | Deletion at the end and boundary handling |
| `abc` / `ac` | `1` | Deletion in the middle |
| `a...a` of length 1024 / same string | `0` | Maximum input size and all characters equal |
| `a...a` of length 1024 / `a` | `1023` | Large number of deletions |
| `abcdef` / `acef` | `2` | Multiple deletions without accidental replacements |

## Edge Cases

The first boundary case is deletion at the beginning. For

```
abc
bc
```

the DP reaches `dp[1][0] = 1`, representing deletion of `a`. From there, `b` matches `b` and `c` matches `c`, so `dp[3][2] = 1`. A position-by-position comparison would see `a != b` and incorrectly describe the first operation as a replacement, even though the optimal alignment is a deletion.

Deletion at the end is handled by the first column of the DP. For

```
abc
ab
```

the state `dp[2][2]` becomes zero because `ab` already matches. Moving from `(2, 2)` to `(3, 2)` uses the deletion transition, producing `dp[3][2] = 1`. The algorithm does not need a special case for the final character because the same recurrence handles it naturally.

A deletion in the middle demonstrates why the DP must preserve alternative alignments. For

```
abc
ac
```

the optimal path matches `a`, deletes `b`, and then matches `c`. The corresponding states are `dp[1][1] = 0`, `dp[2][1] = 1`, and `dp[3][2] = 1`. A greedy mismatch handler might replace `b` with `c`, but the DP keeps both possibilities and selects the cheaper continuation.

For equal one-character strings,

```
a
a
```

the diagonal transition has cost zero, giving `dp[1][1] = 0`. This checks that matching characters are never counted as errors.

At the maximum input size, consider two identical strings consisting of 1024 `a` characters. Every diagonal transition costs zero, so the final answer remains zero after roughly one million constant-time state updates. The algorithm scales directly with the stated length bound and does not rely on recursion depth or exponential branching.

The opposite extreme is a 1024-character source and a one-character target:

```
aaaaaaaa...
a
```

The first column records the cost of deleting arbitrary source prefixes, and the DP can keep one `a` as the matched target character while deleting the other 1023 characters. The final answer is `1023`, confirming that the initialization for an empty target and the deletion transition work correctly at the largest boundary.
