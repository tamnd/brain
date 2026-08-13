---
title: "CF 102302D - Guessing Messages"
description: "Samuelo's text is a string s, and Roppa's guessed hidden message is another string t. The guess is considered correct if we can delete some characters from s while keeping the remaining characters in their original order and obtain exactly t."
date: "2026-08-13T07:35:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "D"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 113
verified: true
draft: false
---

[CF 102302D - Guessing Messages](https://codeforces.com/problemset/problem/102302/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

Samuelo's text is a string `s`, and Roppa's guessed hidden message is another string `t`. The guess is considered correct if we can delete some characters from `s` while keeping the remaining characters in their original order and obtain exactly `t`. In other words, `t` must be a subsequence of `s`.

For example, in `threeyellowfurryfiends`, the characters needed for `hellofriend` appear in the right order, although many unrelated characters occur between them. We only care about relative order, not about contiguous positions.

Both strings can contain up to `10^6` characters. That size rules out any approach that examines pairs of positions repeatedly in a quadratic loop. With one million characters, an `O(nm)` algorithm can perform up to `10^12` operations, far beyond what a 1 second limit can accommodate. The intended solution must process the strings essentially once, giving linear time in their total length. The memory limit also makes an `O(nm)` dynamic programming table impractical, since one million by one million entries would require an enormous amount of memory.

Several edge cases are easy to mishandle. First, the two strings can have the same length. For example,

```
abc
abc
```

has answer `YES`, because every character must be used and the strings are identical. An implementation that accidentally requires an unused character after the last match could incorrectly return `NO`.

The guess can also be longer than the original text. For example,

```
ab
abc
```

has answer `NO`. There are not enough characters in `s` to form `t`. A careless implementation that only checks whether every character of `t` occurs somewhere in `s`, without respecting multiplicity and order, could get this wrong.

Repeated characters are another common source of errors. For

```
aab
aaa
```

the answer is `NO`, because `s` contains only two `a` characters. Merely checking whether the letter `a` appears would not be sufficient.

Finally, the matching characters can be separated by arbitrary text. For

```
axbycz
abc
```

the answer is `YES`. The characters do not need to be adjacent, so an implementation that searches for `t` as a contiguous substring would incorrectly reject it.

## Approaches

A direct but unnecessarily expensive approach is to build a dynamic programming table. Let `dp[i][j]` describe whether the first `j` characters of `t` can be obtained as a subsequence of the first `i` characters of `s`. For every pair `(i, j)`, we decide whether to ignore `s[i - 1]`, or, when the characters match, use it as the next character of `t`. This is correct because every possible subsequence either uses the current character or does not.

The problem is the number of states. There are roughly `n * m` pairs, where `n = len(s)` and `m = len(t)`. At the maximum limits, that is about `10^12` states. Even storing such a table is impossible under the memory limit, and computing it is far too slow.

The observation that removes the entire table is that we do not need to remember all possible ways to match the prefix of `t`. Suppose we are currently looking for character `t[j]`. Among all positions in `s` where that character could be matched, taking the earliest possible position is always at least as good as taking a later one. An earlier match leaves at least as much of the remaining string available for the rest of `t`.

This gives a greedy scan. We process `s` from left to right while keeping a pointer to the next character of `t` that we need. Whenever the current character of `s` matches that target character, we consume it and advance the target pointer. If the target pointer reaches the end of `t`, the whole guess has been embedded successfully. If `s` ends first, no valid embedding exists.

The brute-force DP works because it explicitly considers every prefix combination, but fails because there are too many combinations. The greedy observation lets us keep only the earliest feasible position for the current target character, reducing the problem to one pass through `s`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | O(nm) | O(nm) | Too slow and too much memory |
| Optimal Greedy Scan | O(n + m) | O(1) auxiliary space | Accepted |

## Algorithm Walkthrough

1. Read `s` and `t`, then create a pointer `j` initially equal to zero. The pointer represents the first character of `t` that has not been matched yet.
2. Scan every character `c` of `s` from left to right. If `j` is still inside `t` and `c == t[j]`, use this occurrence of `c` to match the next required character and increment `j`.
3. If `j` becomes equal to `len(t)`, every character of `t` has been matched in increasing positions of `s`, so the answer is `YES`. We can stop immediately because no further character is relevant.
4. If the scan reaches the end of `s` while `j < len(t)`, at least one required character was never found after the previous matches. The answer is `NO`.

The greedy choice is safe because when `s[i] == t[j]`, using position `i` is never worse than skipping it and using a later occurrence of the same character. The remainder of `t` can only benefit from having more positions of `s` available after the current match.

### Why it works

After processing any prefix of `s`, `j` is the maximum number of consecutive characters from the beginning of `t` that the processed prefix can match using the greedy choices. More specifically, every matched character of `t` is assigned to an increasing position in `s`, so whenever `j` reaches `len(t)`, we have explicitly constructed a valid subsequence.

Conversely, whenever the algorithm skips a character of `s`, that character is either different from the next required character or there is no remaining requirement. If it matches the next required character, consuming the earliest such occurrence cannot make a later match impossible, because every position that could be used after it is still available. Thus, if the greedy scan finishes before matching all of `t`, no alternative choice of earlier matches could have produced a valid subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()

    j = 0

    for c in s:
        if j < len(t) and c == t[j]:
            j += 1
            if j == len(t):
                print("YES")
                return

    print("NO")

if __name__ == "__main__":
    solve()
```

The input is read with `readline`, which is appropriate for strings of length up to one million. The `.strip()` call removes the newline without changing any lowercase English letters in the actual strings.

The variable `j` is the only state needed. It always points to the next character required from `t`. When `s` contains that character, we advance `j`; otherwise, the current character of `s` can safely be ignored.

The condition `j < len(t)` prevents accessing `t[j]` after the entire guess has already been matched. The immediate `YES` return also avoids scanning the remaining part of `s`, although even without this optimization the algorithm would remain linear.

There is no integer overflow issue because Python integers are arbitrary precision, and the algorithm only maintains a pointer bounded by the length of `t`. More importantly, there is no two-dimensional table, so the memory usage remains tiny compared with the 256 MB limit.

## Worked Examples

For Sample 1, the input is:

```
threeyellowfurryfiends
hellofriend
```

The pointer starts at the first character of `t`, which is `h`.

| Character from `s` | Next required character | Match? | `j` after processing |
| --- | --- | --- | --- |
| `t` | `h` | No | 0 |
| `h` | `h` | Yes | 1 |
| `r` | `e` | No | 1 |
| `e` | `e` | Yes | 2 |
| `e` | `l` | No | 2 |
| `y` | `l` | No | 2 |
| `e` | `l` | No | 2 |
| `l` | `l` | Yes | 3 |
| `l` | `o` | No | 3 |
| `o` | `o` | Yes | 4 |
| `w` | `f` | No | 4 |
| `f` | `f` | Yes | 5 |
| `u` | `r` | No | 5 |
| `r` | `r` | Yes | 6 |
| `r` | `i` | No | 6 |
| `y` | `i` | No | 6 |
| `f` | `i` | No | 6 |
| `i` | `i` | Yes | 7 |
| `e` | `e` | Yes | 8 |
| `n` | `n` | Yes | 9 |
| `d` | `d` | Yes | 10 |

At the final match, `j` equals `len(t)`, so the algorithm prints `YES`. The trace demonstrates that irrelevant characters can simply be skipped while the matched positions remain strictly increasing.

For Sample 2, the input is:

```
hardcontest
easyac
```

The scan tries to find `e` first.

| Character from `s` | Next required character | Match? | `j` after processing |
| --- | --- | --- | --- |
| `h` | `e` | No | 0 |
| `a` | `e` | No | 0 |
| `r` | `e` | No | 0 |
| `d` | `e` | No | 0 |
| `c` | `e` | No | 0 |
| `o` | `e` | No | 0 |
| `n` | `e` | No | 0 |
| `t` | `e` | No | 0 |
| `e` | `e` | Yes | 1 |
| `s` | `a` | No | 1 |
| `t` | `a` | No | 1 |

The string ends while the algorithm is still waiting for `a`. Thus `j` is only `1` while `len(t)` is `6`, so the answer is `NO`. This also demonstrates why merely finding every character somewhere in `s` is insufficient. The required order must be preserved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | The scan visits each character of `s` at most once, and the target pointer only moves forward through `t`. |
| Space | O(1) auxiliary | Only the target pointer and a few scalar values are maintained besides the input strings. |

With both strings limited to one million characters, the algorithm performs at most about one million iterations of the scan and never constructs a quadratic structure. The input strings themselves require linear memory, while the algorithm's additional memory is constant, so it comfortably fits the 256 MB memory limit.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def solve_data(inp: str) -> str:
    data = inp.splitlines()
    s = data[0]
    t = data[1]

    j = 0

    for c in s:
        if j < len(t) and c == t[j]:
            j += 1
            if j == len(t):
                return "YES\n"

    return "NO\n"

def run(inp: str) -> str:
    return solve_data(inp)

# Provided samples
assert run(
    "threeyellowfurryfiends\n"
    "hellofriend\n"
) == "YES\n", "sample 1"

assert run(
    "hardcontest\n"
    "easyac\n"
) == "NO\n", "sample 2"

# Minimum-size inputs
assert run("a\na\n") == "YES\n", "single equal character"
assert run("a\nb\n") == "NO\n", "single different character"

# Same length, but wrong order
assert run("abc\nacb\n") == "NO\n", "same length requires exact order"

# All equal characters, not enough copies
assert run("aaaa\naaaaa\n") == "NO\n", "target has too many equal characters"

# All equal characters, enough copies
assert run("aaaaa\naaa\n") == "YES\n", "repeated characters"

# Boundary case where the last character is needed
assert run("xabc\na\n") == "YES\n", "match appears after irrelevant prefix"
assert run("abcx\nabc\n") == "YES\n", "target ends exactly at final needed character"

# Maximum-size inputs
assert run("a" * 1_000_000 + "\n" + "a" * 1_000_000 + "\n") == "YES\n", \
    "maximum equal strings"

assert run("a" * 999_999 + "b\n" + "a" * 1_000_000 + "\n") == "NO\n", \
    "maximum-size target requires one unavailable character"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` / `a` | `YES` | Minimum possible strings and successful final match |
| `a` / `b` | `NO` | Minimum possible strings with no match |
| `abc` / `acb` | `NO` | Order matters even when lengths are equal |
| `aaaa` / `aaaaa` | `NO` | Repeated characters and insufficient occurrences |
| `aaaaa` / `aaa` | `YES` | Repeated characters with sufficient occurrences |
| `abcx` / `abc` | `YES` | Target finishes before the source string ends |
| `a^999999b` / `a^1000000` | `NO` | Large input and a one-character shortage at the boundary |
| `a^1000000` / `a^1000000` | `YES` | Maximum-size successful input |

## Edge Cases

When the strings have length one, the algorithm performs exactly one comparison. For input

```
a
a
```

`j` starts at zero, the only character matches `t[0]`, and `j` becomes one, which equals `len(t)`. The result is `YES`. For

```
a
b
```

the comparison fails, `j` remains zero, and the scan ends, giving `NO`.

Equal lengths require every character of `s` to be used. For

```
abc
acb
```

the algorithm matches `a`, then matches `c`, after which it needs `b`. The remaining part of `s` is only `c`, which cannot provide `b`, so the result is `NO`. The algorithm never assumes that equal lengths imply equality.

Repeated characters require enough distinct occurrences. For

```
aaaa
aaaaa
```

the pointer advances once for each of the four characters in `s`, reaching `j = 4`. The target has length five, so the scan ends with one unmatched `a` and returns `NO`. For

```
aaaaa
aaa
```

the third `a` advances `j` to three, immediately completing the target and producing `YES`.

A target can finish exactly at the final character of the source. For

```
abcx
abc
```

the pointer progresses from `0` to `1`, then `2`, then `3` while reading `a`, `b`, and `c`. Since `j == len(t)` immediately after processing `c`, the algorithm returns `YES` without needing another source character. This boundary condition is why the completion check must happen immediately after advancing the pointer.

The maximum-size case behaves identically to the small cases. With one million `a` characters in both strings, every source character matches the current target character, and the target pointer reaches one million after the final comparison. The algorithm performs linear work rather than attempting to compare every source position with every target position, which is what makes the solution viable at the stated limits.
