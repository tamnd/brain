---
title: "CF 102437B - Breaking the Code"
description: "We start with a string s of length n. We may repeatedly delete one character, but only a character currently occupying one of the first two or one of the last two positions can be removed. After exactly n-k deletions, the remaining characters form the password."
date: "2026-08-09T12:40:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 373
verified: true
draft: false
---

[CF 102437B - Breaking the Code](https://codeforces.com/problemset/problem/102437/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a string `s` of length `n`. We may repeatedly delete one character, but only a character currently occupying one of the first two or one of the last two positions can be removed. After exactly `n-k` deletions, the remaining characters form the password. Among all possible passwords of length `k`, we need the lexicographically smallest one.

The constraint `n <= 500000` rules out anything quadratic in the string length. Even `O(nk)` can become quadratic when `k` is close to `n`, so we need a solution whose main work is close to linear or at worst `O(n log n)`. The small alphabet of 26 lowercase letters helps with some boundary choices, but it does not by itself solve the problem because lexicographic comparison can depend on a long common prefix.

The first edge case is `k = n`. No deletion is possible, so the answer is simply the original string. For example, with `s = "abc"` and `k = 3`, the answer is `abc`. A solution that always assumes at least one deletion may accidentally access an invalid second or penultimate position.

The second edge case is `k = 1`. Every individual character can be left as the final character, because we can repeatedly delete from the left until that character becomes the first character. Thus the answer is the smallest character of the whole string. For `s = "zba"` and `k = 1`, the answer is `a`.

The third edge case is `k = 2`. In this case every pair of positions can be made the two surviving characters. For `s = "bac"` and `k = 2`, the possible answers include `ac` and `ba`, so the answer is `ac`. Simply sorting the two smallest characters would suggest `ab`, but `ab` is not a subsequence of `bac` and cannot be produced.

A more subtle boundary case appears when only one deletion is available. For `s = "abcde"` and `k = 4`, we cannot delete `c`, because initially only `a`, `b`, `d`, and `e` are accessible. The possible strings are `bcde`, `acde`, `abce`, and `abcd`, so the answer is `abcd`. A solution that treats the operation as arbitrary subsequence deletion would incorrectly allow `abde`.

## Approaches

A direct brute-force solution can recursively try all four deletion operations. It is correct because every legal operation is explicitly considered, so every reachable string appears somewhere in the recursion tree. However, after `n-k` deletions the tree has up to `4^(n-k)` operation sequences. With `n = 500000`, even a tiny fraction of this search space is impossible to explore. Storing all distinct intermediate strings is also far too expensive.

The useful observation comes from looking at the positions that survive rather than the characters that disappear. During the process, the remaining positions always have a very restricted shape. They consist of one contiguous interval, possibly with one additional surviving position before that interval and possibly with one additional surviving position after it.

To see why, start with the whole string, which is one interval. If we delete the first character, we shorten the interval from the left. If we delete the second character, the first character can remain as a singleton while the rest stays contiguous. The same argument applies symmetrically on the right. Repeating this process can never create a complicated collection of intervals. At most one singleton can be detached from each side of a central contiguous interval.

The converse is also true. Suppose the surviving positions are a contiguous interval, with optionally one surviving character before it and optionally one after it. Everything before the central interval can be deleted from the left, preserving the optional left character by repeatedly deleting the second position. Everything after the central interval can be handled symmetrically from the right. Thus every string with this structure is reachable.

So every reachable password has one of four forms. It can be a contiguous substring of length `k`. It can be one character followed by a contiguous substring of length `k-1`. It can be a contiguous substring of length `k-1` followed by one character. Or it can be one character, then a contiguous substring of length `k-2`, then one character.

The remaining challenge is to find the lexicographically smallest substring of a fixed length efficiently. We construct a suffix array for `s`. For two substrings having the same length, their lexicographic order is the same as the order of the corresponding suffixes, unless the substrings are equal. We group suffixes according to their first `m` characters using the suffix array and its LCP array. This gives every length-`m` substring a compact lexicographic rank.

Once these ranks are available, each of the four structural cases becomes a linear scan. For the form `c + middle`, the first character dominates the comparison, followed by the rank of `middle`. For `middle + c`, the middle substring dominates first, followed by the final character. For `c + middle + d`, the comparison is made in the order `c`, `middle`, `d`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(4^(n-k))` states | Exponential | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Handle `k = 1` and `k = 2` directly. For one character, choose the minimum character. For two characters, scan every possible first position and pair it with the minimum character appearing later. This works because every two-position subsequence is reachable.
2. For `k >= 3`, construct the suffix array of `s` with a sentinel smaller than every lowercase letter. The suffix array gives the lexicographic ordering of all suffixes.
3. Construct the LCP array using Kasai's algorithm. The LCP value between consecutive suffixes tells us how long their common prefix is.
4. For a required middle length `m`, scan the suffix array and assign the same rank to consecutive suffixes whose LCP is at least `m`. Two positions have the same rank exactly when their length-`m` substrings are equal. The ranks are ordered lexicographically.
5. Consider passwords that are exactly one contiguous substring of length `k`. Among all valid starting positions, choose the position with the smallest length-`k` substring rank.
6. Consider passwords of the form `c + middle`, where `middle` has length `k-1`. For every possible starting position of `middle`, the best possible `c` is the smallest character occurring before that position. Compare candidates first by `c`, then by the rank of `middle`.
7. Consider passwords of the form `middle + c`. For every possible middle substring of length `k-1`, choose the smallest character after it. Compare candidates first by the middle substring rank, then by that final character.
8. Consider passwords of the form `c + middle + d`, where `middle` has length `k-2`. For every possible middle start, choose the smallest character before it and the smallest character after it. Compare candidates by `c`, then the middle rank, then `d`.
9. Reconstruct the best candidate from each of the four forms and compare those at the end. There are only four complete candidates, so comparing them directly costs at most `O(k)` total additional work.

Why it works

The central invariant is that every reachable set of surviving positions is exactly a contiguous interval with at most one extra position on each side. The deletion operations preserve this property, and every set having this property can be constructed by deleting unwanted characters from the corresponding side.

The four cases in the algorithm enumerate exactly these four possible shapes. Inside each case, the chosen boundary characters are independently minimized because they occur before or after the contiguous middle. The suffix-derived ranks compare middle substrings correctly because all middle substrings in one case have the same length. Thus each case produces its lexicographically smallest reachable password, and taking the minimum of those four candidates gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_suffix_array(s):
    n = len(s)

    # 1..26 are letters, 0 is the unique sentinel.
    a = [x - 96 for x in s] + [0]
    N = n + 1

    cnt = [0] * 27
    for x in a:
        cnt[x] += 1

    pos = [0] * 27
    for i in range(1, 27):
        pos[i] = pos[i - 1] + cnt[i - 1]

    p = [0] * N
    for i, x in enumerate(a):
        p[pos[x]] = i
        pos[x] += 1

    c = [0] * N
    classes = 1
    for i in range(1, N):
        if a[p[i]] != a[p[i - 1]]:
            classes += 1
        c[p[i]] = classes - 1

    shift = 1
    while shift < N:
        pn = [
            x - shift if x >= shift else x - shift + N
            for x in p
        ]

        cnt = [0] * classes
        for x in pn:
            cnt[c[x]] += 1

        pos = [0] * classes
        total = 0
        for i in range(classes):
            pos[i] = total
            total += cnt[i]

        p_new = [0] * N
        for x in pn:
            cls = c[x]
            p_new[pos[cls]] = x
            pos[cls] += 1

        c_new = [0] * N
        new_classes = 1
        for i in range(1, N):
            cur = p_new[i]
            prev = p_new[i - 1]

            cur_pair = (c[cur], c[(cur + shift) % N])
            prev_pair = (c[prev], c[(prev + shift) % N])

            if cur_pair != prev_pair:
                new_classes += 1

            c_new[cur] = new_classes - 1

        p = p_new
        c = c_new
        classes = new_classes
        shift <<= 1

    # Remove the sentinel suffix.
    return p[1:], a

def build_lcp(suffix_array, a):
    N = len(a)
    rank = [0] * N

    for i, pos in enumerate(suffix_array):
        rank[pos] = i

    lcp = [0] * N
    common = 0

    for i in range(N):
        r = rank[i]

        if r == 0:
            continue

        j = suffix_array[r - 1]

        while i + common < N and j + common < N:
            if a[i + common] != a[j + common]:
                break
            common += 1

        lcp[r] = common

        if common:
            common -= 1

    return lcp

def fixed_length_ranks(suffix_array, lcp, n, length):
    """
    rank[i] is the lexicographic rank of s[i:i+length].
    Equal substrings receive the same rank.
    """
    rank = [0] * n

    group = -1

    for idx, pos in enumerate(suffix_array):
        if idx == 0:
            group = 0
        elif lcp[idx] < length:
            group += 1

        rank[pos] = group

    return rank

def best_by_rank(rank, lo, hi):
    best = lo

    for i in range(lo + 1, hi + 1):
        if rank[i] < rank[best]:
            best = i

    return best

def solve_instance(s, k):
    n = len(s)

    if k == 1:
        return min(s)

    if k == 2:
        best = None
        right_min = s[-1]

        for i in range(n - 2, -1, -1):
            candidate = s[i] + right_min

            if best is None or candidate < best:
                best = candidate

            if s[i] < right_min:
                right_min = s[i]

        return best

    suffix_array, a = build_suffix_array(s)
    lcp = build_lcp(suffix_array, a)

    values = s.encode()

    # Prefix minima and suffix minima of characters.
    pref = bytearray(n)
    suf = bytearray(n + 1)

    pref[0] = values[0]
    for i in range(1, n):
        pref[i] = min(pref[i - 1], values[i])

    suf[n] = 123
    for i in range(n - 1, -1, -1):
        suf[i] = min(suf[i + 1], values[i])

    candidates = []

    # Case 1: one contiguous substring of length k.
    ranks = fixed_length_ranks(suffix_array, lcp, n, k)
    start = best_by_rank(ranks, 0, n - k)
    candidates.append(values[start:start + k])

    # Case 2: one character + substring of length k - 1.
    middle_len = k - 1
    ranks = fixed_length_ranks(
        suffix_array, lcp, n, middle_len
    )

    best_key = None
    best_start = -1
    best_left = -1

    for start in range(1, n - middle_len + 1):
        left_char = pref[start - 1]
        key = (left_char, ranks[start])

        if best_key is None or key < best_key:
            best_key = key
            best_start = start
            best_left = left_char

    candidates.append(
        bytes([best_left]) +
        values[best_start:best_start + middle_len]
    )

    # Case 3: substring of length k - 1 + one character.
    best_key = None
    best_start = -1
    best_right = -1

    for start in range(0, n - middle_len):
        end = start + middle_len
        right_char = suf[end]
        key = (ranks[start], right_char)

        if best_key is None or key < best_key:
            best_key = key
            best_start = start
            best_right = right_char

    candidates.append(
        values[best_start:best_start + middle_len] +
        bytes([best_right])
    )

    # Case 4: one character + substring of length k - 2
    # + one character.
    middle_len = k - 2
    ranks = fixed_length_ranks(
        suffix_array, lcp, n, middle_len
    )

    best_key = None
    best_start = -1
    best_left = -1
    best_right = -1

    for start in range(1, n - middle_len):
        end = start + middle_len

        left_char = pref[start - 1]
        right_char = suf[end]

        key = (left_char, ranks[start], right_char)

        if best_key is None or key < best_key:
            best_key = key
            best_start = start
            best_left = left_char
            best_right = right_char

    candidates.append(
        bytes([best_left]) +
        values[best_start:best_start + middle_len] +
        bytes([best_right])
    )

    return min(candidates).decode()

def solve():
    s = input().strip()
    k = int(input())
    print(solve_instance(s, k))

if __name__ == "__main__":
    solve()
```

The implementation first handles the two smallest values of `k` separately. This avoids having to represent an empty middle interval. For `k = 2`, every pair of surviving positions is reachable, so a right-to-left suffix minimum is enough.

For larger `k`, `build_suffix_array` adds a sentinel smaller than every real character. The standard doubling construction repeatedly sorts suffixes by the pair of equivalence classes representing their first `2^h` characters. Counting sort keeps each doubling phase linear, giving `O(n log n)` construction time.

`build_lcp` uses Kasai's algorithm. The LCP array is needed because a suffix rank alone distinguishes suffixes even when their first `m` characters are equal. `fixed_length_ranks` merges consecutive suffixes whenever their common prefix has length at least `m`, producing the exact lexicographic classes of length-`m` substrings.

The prefix and suffix minima are stored in `bytearray` objects. This keeps their memory consumption small while still allowing constant-time access to the smallest possible outer character for every middle interval.

The ranges in the four cases are deliberately different. For a left extra character, the middle must start at least at position `1`, but it may end at `n-1`. For a right extra character, the middle may start at `0`, but its end must leave one character after it. With two extras, both restrictions apply. These are the places where off-by-one errors are most likely.

No integer can overflow in Python, and the suffix array stores only integer indices and ranks. The final candidates are byte strings, which also makes lexicographic comparison efficient.

## Worked Examples

### Sample 1

For `s = "abacaba"` and `k = 3`, the four structural forms have middle lengths `3`, `2`, `2`, and `1`.

| Form | Best construction | Candidate |
| --- | --- | --- |
| Middle only | `aba` | `aba` |
| Left + middle | `a` + `ab` | `aab` |
| Middle + right | `ab` + `a` | `aba` |
| Left + middle + right | `a` + `a` + `a` | `aaa` |

The last form wins. Its surviving positions are `1, 3, 5`. Starting from `abacaba`, delete the second character `b`, then the penultimate character `b`, then two more accessible `c` and `b` characters as needed, leaving `aaa`.

The important part of the trace is that the answer is not a contiguous substring. A solution considering only substrings would stop at `aab`, while the allowed left and right singleton positions make `aaa` possible.

### Sample 2

For `s = "qwerty"` and `k = 2`, every pair of positions is reachable.

| First position | Best possible second character | Candidate |
| --- | --- | --- |
| `q` | `e` | `qe` |
| `w` | `e` | `we` |
| `e` | `r` | `er` |
| `r` | `t` | `rt` |
| `t` | `y` | `ty` |

The smallest candidate is `er`.

This case also demonstrates why the `k = 2` shortcut is useful. The answer is simply the lexicographically smallest subsequence of length two, which can be found with a suffix minimum without constructing a suffix array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Suffix array construction dominates; LCP, fixed-length ranks, and candidate scans are linear |
| Space | `O(n)` | Suffix array, LCP array, rank arrays, and auxiliary arrays are all linear |

With `n <= 500000`, `O(n log n)` is feasible, while the brute-force state space grows exponentially. The suffix array is constructed once, and the three fixed substring lengths needed by the structural cases are processed with linear scans afterward.

## Test Cases

```
# Save the submitted solution as solution.py before running this block.
from solution import solve_instance

def run(inp: str) -> str:
    lines = inp.strip().splitlines()
    s = lines[0].strip()
    k = int(lines[1])
    return solve_instance(s, k)

# Provided samples
assert run("abacaba\n3\n") == "aaa", "sample 1"
assert run("qwerty\n2\n") == "er", "sample 2"

# Minimum-size input
assert run("z\n1\n") == "z", "minimum size"

# Two-character password, catches incorrect sorting of characters
assert run("bac\n2\n") == "ac", "two-character subsequence"

# Only one deletion is possible, so the interior character cannot be removed
assert run("abcde\n4\n") == "abcd", "one deletion boundary"

# All characters equal
assert run("aaaaa\n3\n") == "aaa", "all equal"

# No deletion is required
assert run("abc\n3\n") == "abc", "k equals n"

# Maximum-size case
s = "z" * 500000
assert run(s + "\n250000\n") == "z" * 250000, "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `z / 1` | `z` | Minimum possible input and `k = 1` |
| `bac / 2` | `ac` | Two-position subsequence and ordering |
| `abcde / 4` | `abcd` | Characters in the interior are not immediately deletable |
| `aaaaa / 3` | `aaa` | Equal characters and repeated substring ranks |
| `abc / 3` | `abc` | No deletions |
| `z...z / 250000` | `z...z` | Maximum input size and highly repetitive suffixes |

## Edge Cases

For `s = "zba"` and `k = 1`, the algorithm immediately returns `a`. Every character can be made the sole survivor by deleting characters from the appropriate side, so the minimum character is sufficient.

For `s = "bac"` and `k = 2`, the algorithm scans possible first positions from right to left while maintaining the smallest character to their right. It considers `ac` from positions `2,3` and `ba` from positions `1,3`, choosing `ac`. The tempting string `ab` cannot be formed because the surviving characters must preserve their original order.

For `s = "abcde"` and `k = 4`, the only deletion is made while five characters remain. The accessible characters are `a`, `b`, `d`, and `e`, so `c` cannot be removed. The four resulting strings have minimum `abcd`. The structural characterization also sees this directly: deleting `c` would leave two non-singleton intervals, which is not one of the four reachable forms.

For `s = "abacaba"` and `k = 3`, the optimal password `aaa` has surviving positions `1`, `3`, and `5`. These positions form a left singleton, a one-character middle interval, and a right singleton. This is exactly the most general shape allowed by the deletion operations.

For `s = "abc"` and `k = 3`, every structural case that is valid reconstructs the original string, and no deletion is performed. The answer remains `abc`, confirming that the boundary calculations do not require an actual removable character.

For the maximum-size string consisting entirely of `500000` copies of `z`, every possible length-`k` middle substring is identical. The fixed-length ranking procedure groups them into the same equivalence class, so any valid starting position is acceptable and the resulting answer is the expected `k` copies of `z`.

If you want, I can also provide a **shorter Codeforces-style version** of this editorial, keeping the same proof but reducing the implementation discussion substantially.
