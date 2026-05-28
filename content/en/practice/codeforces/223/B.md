---
title: "CF 223B - Two Strings"
description: "We are given two lowercase strings, s and t. The task is not simply to check whether t is a subsequence of s. We must answer a stronger question. Consider every possible way to obtain t as a subsequence of s."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 223
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 138 (Div. 1)"
rating: 1900
weight: 223
solve_time_s: 102
verified: true
draft: false
---

[CF 223B - Two Strings](https://codeforces.com/problemset/problem/223/B)

**Rating:** 1900  
**Tags:** data structures, dp, strings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two lowercase strings, `s` and `t`.

The task is not simply to check whether `t` is a subsequence of `s`. We must answer a stronger question.

Consider every possible way to obtain `t` as a subsequence of `s`. A position `i` in `s` is called usable if there exists at least one valid subsequence where `s[i]` is one of the chosen characters. We must determine whether every position of `s` is usable.

For example, if:

```
s = "abab"
t = "ab"
```

then the subsequence `"ab"` can be formed in three different ways:

```
(1,2)
(1,4)
(3,4)
```

Every character position appears in at least one occurrence, so the answer is `"Yes"`.

The lengths of both strings can reach `2 * 10^5`. This immediately rules out anything quadratic. Even an `O(nm)` dynamic programming solution would require around `4 * 10^10` operations in the worst case, which is completely infeasible under a 2 second limit.

We need something close to linear time, ideally `O(n)` or `O(n log n)`.

The tricky part is that a character can belong to some subsequences but not others. A naive implementation may only construct one matching subsequence and mistakenly conclude that unused positions are impossible to use.

Consider:

```
s = "abab"
t = "ab"
```

If we greedily match the earliest possible subsequence, we get positions `(1,2)`. Positions `3` and `4` are unused in this particular matching, but they are still usable in other matchings.

Another subtle case happens when `t` is not a subsequence at all.

```
s = "abc"
t = "d"
```

No valid subsequence exists, so naturally no position in `s` can appear in one. The answer must be `"No"`.

Repeated characters also create edge cases.

```
s = "aaaa"
t = "aa"
```

Every position is usable because we can choose any pair of indices in increasing order. A solution that only tracks one leftmost and one rightmost matching may accidentally miss this flexibility if implemented incorrectly.

## Approaches

The brute force idea is straightforward. Generate all subsequences of `s` equal to `t`, then mark which positions participate in at least one occurrence.

This works logically because the problem definition is exactly about the union of all valid occurrences.

The problem is the number of subsequences. Even for moderate strings, the count becomes exponential. For example:

```
s = "aaaaaaaaaa..."
t = "aaaaa..."
```

The number of valid subsequences becomes combinatorial. Enumerating them is impossible.

A slightly better brute force would test every position independently. For each index `i`, we force the subsequence to include `s[i]` and check whether the remaining parts of `t` can be matched on the left and right.

This avoids enumerating all subsequences, but doing a full subsequence check for every position still costs `O(nm)`.

The key observation is that whether a position can participate depends only on how many characters of `t` can be matched before it and after it.

Suppose position `i` in `s` contains character `c`.

If we want `s[i]` to represent `t[j]`, then:

1. The prefix `t[0...j-1]` must be matchable before `i`.
2. The suffix `t[j+1...]` must be matchable after `i`.

This suggests preprocessing.

We compute:

1. `L[i]`, the maximum prefix length of `t` matchable using `s[0...i]`.
2. `R[i]`, the minimum suffix start in `t` matchable using `s[i...n-1]`.

These arrays let us answer, for every position, whether there exists some index `j` in `t` such that:

```
t[j] == s[i]
```

and enough characters can be matched on both sides.

The entire solution becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Per-position subsequence check | O(nm) | O(1) | Too slow |
| Optimal greedy preprocessing | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the earliest possible matching positions for every character of `t`.

Traverse `s` from left to right with a pointer `p` inside `t`.

Whenever `s[i] == t[p]`, store that position as the earliest occurrence of `t[p]`, then advance `p`.

If we fail to match all characters of `t`, then `t` is not a subsequence of `s`, so the answer is immediately `"No"`.
2. Compute the latest possible matching positions for every character of `t`.

Traverse `s` from right to left with a pointer `p` starting at the end of `t`.

Whenever `s[i] == t[p]`, store that position as the latest occurrence of `t[p]`, then decrement `p`.
3. For every position `i` in `s`, determine whether it can participate in some subsequence.

Suppose `s[i] = c`.

We want to know whether there exists some position `j` in `t` such that:

```
t[j] = c
```

and we can place:

- all earlier characters of `t` before `i`
- all later characters of `t` after `i`
4. Use the earliest and latest arrays to verify this efficiently.

If position `j` of `t` is assigned to `i`, then:

- the earliest position of `t[j-1]` must be before `i`
- the latest position of `t[j+1]` must be after `i`

Boundary cases for the first and last character are handled naturally.
5. If some position in `s` cannot satisfy any valid `j`, print `"No"`.
6. Otherwise print `"Yes"`.

### Why it works

The earliest matching array guarantees the maximum possible room on the right. The latest matching array guarantees the maximum possible room on the left.

For a fixed assignment of `s[i]` to `t[j]`, the conditions:

```
earliest[j-1] < i < latest[j+1]
```

are both necessary and sufficient.

Necessary, because the subsequence order must remain increasing.

Sufficient, because the greedy earliest and latest constructions already prove that such left and right matches exist independently, and their ranges do not overlap.

So every valid participation question reduces to checking interval feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()

    n = len(s)
    m = len(t)

    left = [-1] * m
    right = [-1] * m

    p = 0
    for i in range(n):
        if p < m and s[i] == t[p]:
            left[p] = i
            p += 1

    if p < m:
        print("No")
        return

    p = m - 1
    for i in range(n - 1, -1, -1):
        if p >= 0 and s[i] == t[p]:
            right[p] = i
            p -= 1

    positions = {}
    for j, ch in enumerate(t):
        positions.setdefault(ch, []).append(j)

    for i, ch in enumerate(s):
        ok = False

        if ch not in positions:
            print("No")
            return

        for j in positions[ch]:
            left_ok = (j == 0 or left[j - 1] < i)
            right_ok = (j == m - 1 or right[j + 1] > i)

            if left_ok and right_ok:
                ok = True
                break

        if not ok:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    solve()
```

The first traversal computes the earliest possible positions for every character of `t`. Greedy matching is correct because choosing a character earlier can only increase flexibility for later matches.

The second traversal computes the latest possible positions. This symmetric construction maximizes flexibility on the left side.

The dictionary `positions` stores every occurrence index of each character in `t`. When processing `s[i]`, we only test compatible positions in `t`, which keeps the implementation simple.

The conditions:

```
left[j - 1] < i
right[j + 1] > i
```

encode whether enough room exists on both sides.

One subtle detail is boundary handling. When `j == 0`, there is no left prefix to match, so the left condition is automatically true. The same applies for the last character.

Another easy mistake is forgetting the case where `t` is not a subsequence at all. The first greedy scan detects this immediately.

## Worked Examples

### Example 1

Input:

```
s = "abab"
t = "ab"
```

The earliest matching positions are:

| t index | character | earliest |
| --- | --- | --- |
| 0 | a | 0 |
| 1 | b | 1 |

The latest matching positions are:

| t index | character | latest |
| --- | --- | --- |
| 0 | a | 2 |
| 1 | b | 3 |

Now check every position in `s`.

| s index | s[i] | candidate j | left condition | right condition | usable |
| --- | --- | --- | --- | --- | --- |
| 0 | a | 0 | true | 3 > 0 | yes |
| 1 | b | 1 | 0 < 1 | true | yes |
| 2 | a | 0 | true | 3 > 2 | yes |
| 3 | b | 1 | 0 < 3 | true | yes |

Every position is usable, so the answer is `"Yes"`.

This example demonstrates that a character may participate even if it does not belong to the earliest greedy matching.

### Example 2

Input:

```
s = "abac"
t = "ab"
```

Earliest positions:

| t index | character | earliest |
| --- | --- | --- |
| 0 | a | 0 |
| 1 | b | 1 |

Latest positions:

| t index | character | latest |
| --- | --- | --- |
| 0 | a | 0 |
| 1 | b | 1 |

Now test positions in `s`.

| s index | s[i] | candidate j | left condition | right condition | usable |
| --- | --- | --- | --- | --- | --- |
| 0 | a | 0 | true | 1 > 0 | yes |
| 1 | b | 1 | 0 < 1 | true | yes |
| 2 | a | 0 | true | 1 > 2 = false | no |

Position `2` cannot be used because every valid `"ab"` subsequence must place `b` after the chosen `a`, but no such `b` exists after index `2`.

So the answer is `"No"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each traversal scans the strings once |
| Space | O(m) | Arrays and character-position lists |

The solution easily fits within the limits. With strings up to `2 * 10^5`, linear time is exactly the target complexity range for a 2 second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    t = input().strip()

    n = len(s)
    m = len(t)

    left = [-1] * m
    right = [-1] * m

    p = 0
    for i in range(n):
        if p < m and s[i] == t[p]:
            left[p] = i
            p += 1

    if p < m:
        print("No")
        return

    p = m - 1
    for i in range(n - 1, -1, -1):
        if p >= 0 and s[i] == t[p]:
            right[p] = i
            p -= 1

    positions = {}
    for j, ch in enumerate(t):
        positions.setdefault(ch, []).append(j)

    for i, ch in enumerate(s):
        ok = False

        if ch not in positions:
            print("No")
            return

        for j in positions[ch]:
            left_ok = (j == 0 or left[j - 1] < i)
            right_ok = (j == len(t) - 1 or right[j + 1] > i)

            if left_ok and right_ok:
                ok = True
                break

        if not ok:
            print("No")
            return

    print("Yes")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("abab\nab\n") == "Yes\n", "sample 1"

# t is not a subsequence
assert run("abc\nd\n") == "No\n", "missing character"

# single character strings
assert run("a\na\n") == "Yes\n", "minimum size"

# repeated characters
assert run("aaaa\naa\n") == "Yes\n", "all positions usable"

# unusable middle character
assert run("abac\nab\n") == "No\n", "late a cannot participate"

# boundary ordering issue
assert run("ba\na\n") == "No\n", "first character unusable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abc / d` | `No` | `t` is not a subsequence |
| `a / a` | `Yes` | Minimum valid input |
| `aaaa / aa` | `Yes` | Repeated characters and multiple matchings |
| `abac / ab` | `No` | Character appears in `t` but cannot fit ordering |
| `ba / a` | `No` | Prefix character cannot participate |

## Edge Cases

Consider:

```
s = "abc"
t = "d"
```

The left greedy scan never matches any character of `t`. The pointer stops before reaching the end of `t`, so the algorithm immediately prints `"No"`.

This is correct because no subsequence equal to `t` exists at all.

Now consider:

```
s = "aaaa"
t = "aa"
```

The earliest positions become `[0, 1]` and the latest positions become `[2, 3]`.

Take index `1` in `s`. It can represent:

```
t[0]
```

because there is still a valid `a` after it for `t[1]`.

Take index `2`. It can represent:

```
t[1]
```

because there is still a valid `a` before it for `t[0]`.

Every position passes one of the checks, so the algorithm prints `"Yes"`.

Finally consider:

```
s = "abac"
t = "ab"
```

The second `'a'` at position `2` fails because:

```
right[1] = 1
```

and:

```
1 > 2
```

is false.

There is no `b` available after index `2`, so this character cannot belong to any valid subsequence. The algorithm correctly returns `"No"`.
