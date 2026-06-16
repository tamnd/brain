---
title: "CF 1538E - Funny Substrings"
description: "We are given a very small “programming language” where variables store strings. Each variable is either assigned a literal string of length at most five, or defined as the concatenation of two previously defined variables."
date: "2026-06-16T15:08:31+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "hashing", "implementation", "matrices", "strings"]
categories: ["algorithms"]
codeforces_contest: 1538
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 725 (Div. 3)"
rating: 2100
weight: 1538
solve_time_s: 399
verified: true
draft: false
---

[CF 1538E - Funny Substrings](https://codeforces.com/problemset/problem/1538/E)

**Rating:** 2100  
**Tags:** data structures, hashing, implementation, matrices, strings  
**Solve time:** 6m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small “programming language” where variables store strings. Each variable is either assigned a literal string of length at most five, or defined as the concatenation of two previously defined variables. The program is a sequence of such assignments, and only the value of the final variable matters.

Our task is not to reconstruct the final string explicitly, but to compute how many times the substring `"haha"` appears in it, including overlapping occurrences.

The critical constraint is that strings can grow exponentially in length due to repeated concatenation. Even though each base string is tiny, repeated `x = a + b` operations can quickly create strings far too large to materialize. A direct simulation is therefore impossible.

The subtle difficulty comes from overlap effects. When concatenating two strings `A + B`, occurrences of `"haha"` can appear entirely in `A`, entirely in `B`, or straddling the boundary between them. That boundary behavior depends only on the suffix of `A` and prefix of `B`, and not on their full content.

Edge cases that break naive approaches are all about this boundary:

A first failure mode is ignoring overlaps across concatenation boundaries. For example, `"ha" + "ha"` does not contain `"haha"` internally in either half, but the concatenation forms one occurrence.

A second failure mode is trying to maintain only a count without enough prefix and suffix information. For instance, if we only track how many `"haha"` appear inside each variable, we lose the ability to detect new occurrences formed after concatenation.

A third failure mode is truncating strings incorrectly. We do not need full strings, but we do need enough context so that every possible cross-boundary match is detectable. Since the pattern length is four, keeping a small fixed prefix and suffix is sufficient.

## Approaches

A brute force interpretation would explicitly build every string and then scan it for occurrences of `"haha"`. Each concatenation would copy entire strings, and counting would require a linear scan. Since string sizes can double at each step, after `n` operations the string length can reach exponential size, making this approach infeasible even for the maximum `n = 50`.

The key observation is that we only ever care about matches of a fixed pattern of length four. Any occurrence of `"haha"` lies completely inside a local window of four characters. When concatenating two strings, any new occurrence that crosses the boundary must start in the last three characters of the left string and extend into the first three characters of the right string. Therefore, it is sufficient to maintain three pieces of information per variable: the number of `"haha"` occurrences inside it, a prefix of up to three characters, and a suffix of up to three characters.

With this representation, concatenation becomes constant time: internal counts are added, and boundary crossings are computed by checking at most three overlap positions between suffix and prefix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force string construction | O(total string size) | O(total string size) | Too slow |
| DP with counts + prefix/suffix trimming | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We process statements in order, maintaining for each variable a compact state consisting of three components: the number of `"haha"` occurrences, the first up to three characters of the string, and the last up to three characters.

1. If a statement is of the form `x := s`, we directly initialize the variable. We count occurrences of `"haha"` in `s` by brute force since `|s| ≤ 5`, and store prefix and suffix (truncated to length 3). This is safe because the string is small.
2. If a statement is `x = a + b`, we combine the stored states of `a` and `b`. The total internal count starts as `cnt[a] + cnt[b]`.
3. We then compute cross-boundary occurrences. Since `"haha"` has length 4, any crossing occurrence must be formed by taking a suffix of `a` and a prefix of `b`. We try all splits where we take `k` characters from the end of `a` (from 1 to 3) and `4-k` characters from the start of `b`, checking whether the concatenation equals `"haha"`. Each match increments the count.
4. We construct the new prefix by taking `a.prefix + b.prefix` and trimming to length at most 3.
5. We construct the new suffix similarly from `a.suffix + b.suffix`, also trimming to length at most 3.
6. The final answer is the count stored in the variable used in the last statement.

The reason this works is that every occurrence of `"haha"` is either fully contained inside one of the components, or it spans the concatenation boundary. Any spanning occurrence must intersect the boundary in at most 3 characters from each side, because the pattern length is 4. Our prefix and suffix storage guarantees we never lose any information needed to detect such overlaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def calc_small(s):
    cnt = 0
    for i in range(len(s) - 3):
        if s[i:i+4] == "haha":
            cnt += 1
    return cnt

def merge(a, b):
    cnt = a[0] + b[0]

    A = a[1]
    B = b[2]

    # cross boundary check
    for k in range(1, 4):
        if k <= len(a[2]) and (4 - k) <= len(b[1]):
            if a[2][-k:] + b[1][:4 - k] == "haha":
                cnt += 1

    new_pref = (a[1] + b[1])[:3]
    new_suf = (a[2] + b[2])[-3:]

    return (cnt, new_pref, new_suf)

t = int(input())
for _ in range(t):
    n = int(input())
    mp = {}

    last_var = None

    for _ in range(n):
        parts = input().strip().split()

        if ":=" in parts:
            x = parts[0]
            s = parts[2]
            cnt = calc_small(s)
            mp[x] = (cnt, s[:3], s[-3:])
            last_var = x
        else:
            x = parts[0]
            a = parts[2]
            b = parts[4]
            mp[x] = merge(mp[a], mp[b])
            last_var = x

    print(mp[last_var][0])
```

The implementation relies on compressing every string into a constant-size signature. The `calc_small` function is safe because base strings are at most length five. The `merge` function is the core: it only inspects up to three characters from each side, which is sufficient to detect all boundary occurrences of a four-character pattern.

A common pitfall is incorrectly iterating over the boundary splits. We explicitly test all ways a 4-character pattern can be split across two strings, ensuring no overlap case is missed. Another subtle point is keeping prefix and suffix capped at length three; longer storage is unnecessary and would risk accidental O(n²) behavior.

## Worked Examples

Consider the first sample where variables evolve and concatenate repeatedly.

For simplicity, track only the final meaningful variable `d`.

| Step | Operation | Count | Prefix | Suffix |
| --- | --- | --- | --- | --- |
| a | `"h"` | 0 | h | h |
| b | `"aha"` | 0 | aha | aha |
| c | a + b | 1 | h+aha → `hah` | h+aha → `aha` |
| c | c + c | 3 | hah + hah → `hah` | aha + aha → `aha` |
| e | c + c | 3 | hah | aha |
| d | a + c | 3 | h + hah → `hah` | h + aha → `aha` |

This trace shows that most growth is irrelevant except near boundaries. The count increases only when cross-boundary combinations form `"haha"`.

Now consider the exponential growth case where `x := haha` is repeatedly doubled. Each doubling preserves structure, and cross-boundary overlaps contribute a large number of new occurrences, producing exponential growth in the count while representation size stays constant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each statement performs constant work, since merging checks only a fixed number of boundary cases |
| Space | O(n) | We store one constant-size state per variable |

The constraints allow up to 50 statements per test case and 1000 test cases, so this solution is easily within limits. Each operation is constant time, and no string ever grows beyond length 3 in stored form.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    def calc_small(s):
        cnt = 0
        for i in range(len(s) - 3):
            if s[i:i+4] == "haha":
                cnt += 1
        return cnt

    def merge(a, b):
        cnt = a[0] + b[0]
        for k in range(1, 4):
            if k <= len(a[2]) and (4 - k) <= len(b[1]):
                if a[2][-k:] + b[1][:4-k] == "haha":
                    cnt += 1
        return (cnt, (a[1] + b[1])[:3], (a[2] + b[2])[-3:])

    t = int(input())
    for _ in range(t):
        n = int(input())
        mp = {}
        last = None

        for _ in range(n):
            parts = input().split()
            if ":=" in parts:
                x = parts[0]
                s = parts[2]
                mp[x] = (calc_small(s), s[:3], s[-3:])
                last = x
            else:
                x = parts[0]
                a = parts[2]
                b = parts[4]
                mp[x] = merge(mp[a], mp[b])
                last = x

        print(mp[last][0])

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample 1
assert run("""4
6
a := h
b := aha
c = a + b
c = c + c
e = c + c
d = a + c
15
x := haha
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
x = x + x
1
haha := hah
5
haahh := aaaha
ahhhh = haahh + haahh
haahh = haahh + haahh
ahhhh = ahhhh + haahh
ahhaa = haahh + ahhhh
""") == """3
32767
0
0"""

# custom cases
assert run("""1
1
a := haha""") == "1", "single exact match"

assert run("""1
2
a := ha
b := ha
c = a + b""") == "1", "boundary match only"

assert run("""1
3
a := h
b := a + a
c = b + b""") == "0", "no possible match"

assert run("""1
1
x := aaaaa""") == "0", "no pattern present"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single exact match | 1 | direct base string counting |
| boundary match only | 1 | cross-boundary detection correctness |
| no possible match | 0 | correctness under no occurrences |
| no pattern present | 0 | safe handling of irrelevant strings |

## Edge Cases

A key edge case is when a full occurrence is split exactly across the concatenation boundary. For input `a := ha` and `b := ha`, both sides individually contain no `"haha"`, but their concatenation forms one valid occurrence. The algorithm handles this by explicitly checking all boundary splits using suffix and prefix combinations.

Another case is repeated doubling, where a short string rapidly grows in conceptual size. For example, starting from `x := haha` and repeatedly applying `x = x + x`, the number of occurrences grows exponentially. The algorithm handles this because it never expands the string, and every doubling is processed in constant time using prefix-suffix overlap logic.

A third case is strings that do not contain the pattern at all but still influence future matches via suffix-prefix structure. Even when internal count is zero, the stored prefix and suffix remain essential, and the algorithm preserves them independently of occurrence count, ensuring future concatenations are still evaluated correctly.
