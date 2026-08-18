---
title: "CF 102218A - Alan's Birthday"
description: "We are given a string of lowercase English letters, and we may rearrange its characters in any order. Alan searches his dictionary from the lexicographically smallest string toward the largest one, so the best gift is the rearrangement that appears as early as possible in that…"
date: "2026-08-18T22:31:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "A"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 593
verified: false
draft: false
---

[CF 102218A - Alan's Birthday](https://codeforces.com/problemset/problem/102218/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of lowercase English letters, and we may rearrange its characters in any order. Alan searches his dictionary from the lexicographically smallest string toward the largest one, so the best gift is the rearrangement that appears as early as possible in that ordering.

The lexicographically smallest rearrangement is simply the string with all characters placed in increasing alphabetical order. For example, the characters of `mac` can only be rearranged into strings such as `mac`, `mca`, `amc`, and so on, and `acm` is the first of them lexicographically.

The length can reach (10^7), which is much larger than the size where expensive algorithms are comfortable under a roughly one-second time limit. An (O(N^2)) algorithm would require around (10^{14}) operations at the upper bound, and an (O(N!)) enumeration is far beyond that. Even a comparison-based (O(N\log N)) sort performs on the order of hundreds of millions of comparisons when (N=10^7). The crucial extra information is that every character belongs to an alphabet of only 26 lowercase letters.

The first edge case is a one-character string. For input `1` followed by `z`, the answer is still `z`. There is nothing to rearrange, and an implementation that assumes at least two characters could introduce an unnecessary boundary error.

The second edge case is repeated characters. For input `5` followed by `aaaaa`, the answer is `aaaaa`. A careless implementation that treats equal characters as distinct objects may perform redundant work, although the result must contain exactly the same five copies.

The third edge case is a mixture where the smallest character occurs several times. For input `6` followed by `zzabca`, the answer is `aabcz z`, or `aabczz` without the space. The two `a` characters must both come before every larger character. An implementation that only moves the smallest character once would produce the wrong ordering.

## Approaches

A direct brute-force approach would generate every possible rearrangement of the string, compare them, and keep the lexicographically smallest one. There are (N!) permutations when all characters are distinct. Comparing two strings can inspect up to (N) characters, so the worst-case work is (O(N\cdot N!)). At (N=10^7), even writing down the first tiny fraction of these permutations is impossible. Repeated characters reduce the number of distinct permutations, but the worst case still has all characters distinct in principle, and the input alphabet restriction does not rescue permutation enumeration for large (N).

A more sensible general-purpose approach is comparison sorting. If we sort the characters in ascending order, the result is exactly the lexicographically smallest rearrangement. That takes (O(N\log N)) comparisons with a standard comparison sort. It is correct, but the constraint (N\le 10^7) makes the extra logarithmic factor unnecessarily expensive, especially under the 1.25 second limit used by the original problem.

The key observation is that there are only 26 possible characters. We do not need to discover the relative order of millions of individual characters because their alphabetical order is already known. We only need to count how many `a` characters exist, then how many `b` characters exist, and so on through `z`. Once those 26 frequencies are known, the answer is obtained by writing each character its counted number of times in alphabetical order.

This is counting sort in its simplest possible form. Instead of paying (O(N\log N)) to compare characters whose ordering is already known, we scan the input once and use a fixed array of 26 counters. Constructing the answer also takes (O(N)), so the entire algorithm is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all rearrangements | (O(N\cdot N!)) | (O(N)) | Too slow |
| Comparison sort | (O(N\log N)) | (O(N)) | Unnecessarily expensive |
| Counting characters | (O(N)) | (O(N)) for input/output, (O(26)) auxiliary | Accepted |

## Algorithm Walkthrough

1. Read (N) and the string (S). The value of (N) tells us the expected number of characters, while the actual string contains the characters we must rearrange.
2. Create 26 counters, one for every lowercase letter. For each character in (S), increment the counter corresponding to its alphabet position. Since there are only 26 possible positions, each character can be classified in constant time.
3. Traverse the 26 counters from `a` through `z`. For a character with frequency (f), append that character exactly (f) times to the result. All copies of a smaller character must precede every copy of a larger character in a lexicographically minimal string.
4. Write the resulting string. Every input character was counted exactly once and then emitted exactly once, so the output is a rearrangement of the original string.

### Why it works

After counting, the algorithm knows exactly how many copies of every letter occur in the input. Suppose the resulting string had a larger character before a smaller character. Swapping those two positions would make the string lexicographically smaller while preserving all character frequencies. Hence such an inversion cannot occur in the lexicographically smallest rearrangement. The only arrangement with no such inversion is the one where all `a` characters come first, followed by all `b` characters, and so on through `z`. The algorithm constructs exactly that arrangement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    count = [0] * 26

    for ch in s:
        count[ord(ch) - ord('a')] += 1

    result = []
    for i, freq in enumerate(count):
        if freq:
            result.append(chr(ord('a') + i) * freq)

    sys.stdout.write(''.join(result))

if __name__ == "__main__":
    solve()
```

The first line reads the declared length, although the algorithm does not need to use it after the input has been read. Keeping the value is useful for matching the input format, while iterating over the actual string avoids assumptions about line boundaries beyond the statement's guarantee.

The expression `ord(ch) - ord('a')` converts a lowercase letter into an index from 0 through 25. For example, `a` becomes 0, `b` becomes 1, and `z` becomes 25. The counter array therefore needs only 26 entries regardless of whether the string contains ten characters or ten million.

The result is built from blocks such as `a * 3` or `m * 2`. This is preferable to repeatedly concatenating one character at a time, because repeated string concatenation can create unnecessary copying. The list contains at most 26 strings, and `''.join(result)` combines them into the final output once.

No integer can overflow in Python. The largest counter is only (10^7), which is easily represented by Python integers.

The `.strip()` call removes the newline produced by `readline()`. Since the input contains only lowercase letters, there are no meaningful spaces that need to be preserved.

## Worked Examples

For Sample 1, the input string is `mac`.

| Character read | Counter state for nonzero letters | Result |
| --- | --- | --- |
| `m` | `m: 1` |  |
| `a` | `a: 1, m: 1` |  |
| `c` | `a: 1, c: 1, m: 1` |  |
| Emit `a` | `a: 1, c: 1, m: 1` | `a` |
| Emit `c` | `a: 1, c: 1, m: 1` | `ac` |
| Emit `m` | `a: 1, c: 1, m: 1` | `acm` |

The frequency array preserves exactly one copy of each input character. Traversing the alphabet places `a` before `c` and `c` before `m`, giving `acm`, which is the first possible rearrangement in lexicographic order.

For Sample 2, the input string is `geso`.

| Character read | Counter state for nonzero letters | Result |
| --- | --- | --- |
| `g` | `g: 1` |  |
| `e` | `e: 1, g: 1` |  |
| `s` | `e: 1, g: 1, s: 1` |  |
| `o` | `e: 1, g: 1, o: 1, s: 1` |  |
| Emit `e` | `e: 1, g: 1, o: 1, s: 1` | `e` |
| Emit `g` | `e: 1, g: 1, o: 1, s: 1` | `eg` |
| Emit `o` | `e: 1, g: 1, o: 1, s: 1` | `ego` |
| Emit `s` | `e: 1, g: 1, o: 1, s: 1` | `egos` |

Again, the final string contains exactly the same multiset of characters as the input. Its letters are in nondecreasing alphabetical order, so no pair of positions can be swapped to obtain a lexicographically smaller string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | The input is scanned once, and the 26 counters are emitted in constant alphabet size. |
| Space | (O(N)) | The input string and the resulting output occupy linear space, while the frequency array uses only 26 counters. |

With (N) as large as (10^7), linear processing is the appropriate target. The algorithm performs a constant amount of work per input character and never allocates a data structure proportional to the number of possible permutations. The auxiliary counting state remains fixed at 26 entries, which is particularly suitable for the original 64 MB memory limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    count = [0] * 26

    for ch in s:
        count[ord(ch) - ord('a')] += 1

    result = []
    for i, freq in enumerate(count):
        if freq:
            result.append(chr(ord('a') + i) * freq)

    sys.stdout.write(''.join(result))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("3\nmac\n") == "acm", "sample 1"
assert run("4\ngeso\n") == "egos", "sample 2"

# Minimum-size input
assert run("1\nz\n") == "z", "single character"

# All characters are equal
assert run("7\naaaaaaa\n") == "aaaaaaa", "all equal"

# Boundary alphabet characters and repeated letters
assert run("8\nzzzzaaaa\n") == "aaaazzzz", "alphabet boundaries"

# Maximum-size input
s = "a" * 10_000_000
assert run(f"{len(s)}\n{s}\n") == s, "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` / `z` | `z` | Minimum size and no-rearrangement case |
| `7` / `aaaaaaa` | `aaaaaaa` | Repeated characters and frequency counting |
| `8` / `zzzzaaaa` | `aaaazzzz` | Smallest and largest alphabet characters, including repeated blocks |
| `10000000` / ten million `a` characters | The same ten million `a` characters | Maximum input size and linear processing |

The maximum-size assertion is deliberately constructed rather than written as a literal ten-million-character line. In an actual contest submission, only the judge input needs to contain that data, while the test expresses the same boundary condition programmatically.

## Edge Cases

For the one-character case, consider:

```
1
z
```

The counter for `z` becomes 1 and every other counter remains zero. The emission phase skips the empty letters and outputs one `z`. There is no indexing of a second character, so the boundary at (N=1) is handled naturally.

For repeated characters, consider:

```
5
aaaaa
```

Every iteration increments the same counter, leaving `count['a'] = 5`. The output phase emits `a * 5`, producing `aaaaa`. No distinct-permutation logic is needed because the frequency representation already captures the entire state relevant to the answer.

For repeated smallest characters mixed with larger ones, consider:

```
6
zzabca
```

The counters become `a:2`, `b:1`, `c:1`, and `z:2`. The emission order is `aa`, then `b`, then `c`, then `zz`, producing:

```
aabczz
```

A rearrangement beginning with only one `a`, such as `abaczz`, cannot be optimal because another `a` exists and placing it immediately after the first `a` makes the string smaller.

For the alphabet boundary case, consider:

```
4
zaba
```

The frequencies are `a:2`, `b:1`, and `z:1`. The algorithm emits the `a` block first, then `b`, then `z`, producing:

```
aabz
```

This confirms that the algorithm does not depend on the input order and correctly handles both ends of the lowercase alphabet.

The maximum-size case follows exactly the same logic. If all (10^7) characters are `a`, the scan performs (10^7) constant-time counter increments, and the output phase emits one block of (10^7) characters. There is no sorting step and no attempt to enumerate arrangements, so the running time grows linearly with the actual input size.
