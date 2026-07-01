---
title: "CF 104114A - AppendAppendAppend"
description: "We are given a base string s. Each day, Momo does not modify it internally, but instead builds a longer string by concatenating copies of the original s. After day 1, the string is exactly s. After day 2, it becomes s + s. After day k, it becomes s repeated k times in a row."
date: "2026-07-02T01:58:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104114
codeforces_index: "A"
codeforces_contest_name: "2022 ICPC Southeastern Europe Regional Contest"
rating: 0
weight: 104114
solve_time_s: 45
verified: true
draft: false
---

[CF 104114A - AppendAppendAppend](https://codeforces.com/problemset/problem/104114/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a base string `s`. Each day, Momo does not modify it internally, but instead builds a longer string by concatenating copies of the original `s`. After day 1, the string is exactly `s`. After day 2, it becomes `s + s`. After day k, it becomes `s` repeated k times in a row.

Bobo has another string `t`. The question is to determine the smallest day number k such that `t` can be found as a subsequence of the string formed by repeating `s` exactly k times.

A subsequence means we are allowed to delete characters from the repeated string without changing order, and we want to be able to obtain `t`.

The key difficulty is that we are not asked whether `t` is a subsequence of a fixed string, but the smallest number of repetitions of `s` needed so that it becomes possible.

The constraints allow both `s` and `t` to be up to 500,000 characters. This immediately rules out any approach that constructs the repeated string explicitly. Even two repetitions of the maximum size string would already exceed memory limits, and building up to the answer is impossible.

We also need to be careful about the fact that `t` may require many repeated scans of `s`. A naive subsequence check per day would simulate up to k passes over `s`, giving quadratic or worse behavior.

A few edge situations matter.

If `t` contains a character not present in `s`, then it is impossible in general, but the statement guarantees an answer exists, so this case is excluded.

If `t` is already a subsequence of `s`, the answer is 1.

If characters of `t` are distributed such that matching forces restarting scanning `s` many times, the answer may be large, but we must detect this without explicitly building the repeated string.

## Approaches

A direct brute-force strategy is to simulate day by day. For day k, we conceptually build `s` repeated k times and check whether `t` is a subsequence using a two-pointer scan. This subsequence check is linear in the length of the constructed string, so O(k · |s| + |t|) per day.

In the worst case, k itself can be as large as |t|, for example when each character of `t` matches only one character per copy of `s`. This leads to a total complexity around O(|s| · |t|), which is far too slow for 5 · 10^5 limits.

The key observation is that we never need to build repeated strings explicitly. Instead, we simulate the subsequence matching greedily while cycling through `s`.

We scan `t` from left to right and maintain a pointer in `s`. When we cannot match the next character of `t` in the current scan of `s`, we “wrap around” to the next copy of `s`, which corresponds exactly to moving to the next day’s repetition boundary. Each time we restart scanning `s`, we increment the day counter.

This works because subsequence matching depends only on relative order, and repeating `s` simply gives us another identical scan window.

To make this efficient, we preprocess positions of each character in `s` so that we can jump to the next valid occurrence in O(log σ) or O(1) using arrays. However, an even simpler O(n + m) greedy works by scanning `s` repeatedly using a pointer reset.

The process is equivalent to repeatedly traversing `s` while consuming `t`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (build strings per day) | O( | s | · |
| Optimal greedy scan over cycles of `s` | O( | s | + |

## Algorithm Walkthrough

We simulate matching `t` as a subsequence over repeated copies of `s` without constructing them.

1. Initialize a pointer `i = 0` for string `t` and a counter `days = 1`, representing that we are currently inside the first copy of `s`.

We also maintain a pointer `j = 0` for scanning `s`.
2. While `i < len(t)`, attempt to match `t[i]` by scanning `s` starting from position `j`.
3. Move `j` forward through `s` until either `s[j] == t[i]` or we reach the end of `s`.

This step represents trying to find the next match within the current repetition.
4. If we found a match `s[j] == t[i]`, advance both pointers (`i += 1`, `j += 1`) and continue.

This preserves subsequence order.
5. If we reached the end of `s` without finding a match, increment `days`, reset `j = 0`, and continue scanning `s` from the start.

This corresponds to moving into the next repeated copy of `s`.
6. Repeat until all characters of `t` are matched.

The final value of `days` is the minimum number of repetitions needed.

### Why it works

At any moment, the algorithm is effectively simulating a traversal over an infinite concatenation of `s`. Each time we exhaust `s` without finishing `t`, we are forced to move to the next identical block. Since every block is identical, the only state that matters is the current position inside `s` and the current index in `t`. The greedy scan ensures that each character of `t` is matched at the earliest possible position in the current or next copy of `s`, so we never overuse a block unnecessarily. This guarantees the minimal number of resets, which corresponds exactly to the minimal number of days.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()

    n = len(s)

    i = 0
    j = 0
    days = 1

    while i < len(t):
        if j == n:
            days += 1
            j = 0

        if s[j] == t[i]:
            i += 1
            j += 1
        else:
            j += 1

    print(days)

if __name__ == "__main__":
    solve()
```

The code maintains two pointers: one over `t` and one over the current copy of `s`. When the scan of `s` finishes, we increment the day counter and restart scanning. The key implementation detail is that we never build repeated strings, and the pointer `j` acts as a virtual position inside the current repetition.

A subtle point is that we must reset `j` exactly when it reaches `len(s)`, not when a match fails, since mismatches should still advance the scan inside the same repetition.

## Worked Examples

### Example 1

Let `s = dwalkcake`, `t = cakewalk`.

| step | i | j | days | action |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | scan until match 'c' |
| 2 | 0 | 5 | 1 | match 'c' |
| 3 | 1 | 6 | 1 | match 'a' |
| 4 | 2 | 7 | 1 | match 'k' |
| 5 | 3 | 8 | 1 | match 'e' |
| 6 | 4 | 9 | 1 | end of s reached, restart |
| 7 | 4 | 0 | 2 | new day begins |
| 8 | 4 | 1 | 2 | match 'w' ... |

The second cycle of `s` is needed to finish matching. This demonstrates that greedy consumption across copies is necessary.

### Example 2

Let `s = abc`, `t = acbac`.

| step | i | j | days | action |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | match 'a' |
| 2 | 1 | 1 | 1 | match 'c' |
| 3 | 2 | 2 | 1 | match 'b' |
| 4 | 3 | 3 | 2 | restart s |
| 5 | 3 | 0 | 2 | match 'a' |
| 6 | 4 | 1 | 2 | match 'c' |

We see that the second repetition is required because `t` forces reuse of earlier structure after exhausting one pass.

These traces show that the algorithm always proceeds greedily and only increases days when a full scan of `s` is consumed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O(1) | Only a few integer pointers are stored, no auxiliary structures proportional to input size are needed. |

The linear behavior fits easily within constraints where both strings are up to 5 · 10^5 characters.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf
    import sys

    input = sys.stdin.readline

    def solve():
        s = input().strip()
        t = input().strip()

        n = len(s)
        i = 0
        j = 0
        days = 1

        while i < len(t):
            if j == n:
                days += 1
                j = 0
            if s[j] == t[i]:
                i += 1
                j += 1
            else:
                j += 1

        return str(days)

    return solve()

# provided sample (as described)
assert run("dwalkcake\ncakewalk\n") == "2"

# custom cases
assert run("abc\nabc\n") == "1"
assert run("abc\ncba\n") == "3"
assert run("a\naaaaa\n") == "5"
assert run("ab\nbbbb\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abc / abc` | 1 | already subsequence in one copy |
| `abc / cba` | 3 | ordering forces multiple resets |
| `a / aaaaa` | 5 | extreme repetition of single character |
| `ab / bbbb` | 4 | worst-case skipping behavior |

## Edge Cases

One important edge case is when `t` requires repeated full scans of `s` because matches occur only near the end of each copy.

For example, if `s = abcd` and `t = dddd`, each copy of `s` contributes only one usable match at the last character. The algorithm repeatedly scans to the end, increments `days`, and continues, producing correct day count equal to the number of occurrences.

Another edge case is when `t` is very short compared to `s`, such as `s = abcde...` and `t = single character`. The algorithm matches immediately in the first scan and never increments `days`, correctly returning 1.

Finally, if `s` is a single repeated character like `aaaaa` and `t` is also all `a`, the algorithm never resets until necessary, and the number of days equals the length of `t`, which matches the minimal repetition requirement.
