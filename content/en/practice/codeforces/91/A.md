---
title: "CF 91A - Newspaper Headline"
description: "We have a source string s1, which represents the headline of one newspaper. We may take as many copies of this headline as we want and concatenate them together."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 91
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 75 (Div. 1 Only)"
rating: 1500
weight: 91
solve_time_s: 117
verified: true
draft: false
---

[CF 91A - Newspaper Headline](https://codeforces.com/problemset/problem/91/A)

**Rating:** 1500  
**Tags:** greedy, strings  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a source string `s1`, which represents the headline of one newspaper. We may take as many copies of this headline as we want and concatenate them together. From the resulting long string, we are allowed to delete arbitrary characters while keeping the remaining characters in order.

The target string `s2` must appear as a subsequence of the concatenated headlines. The task is to determine the minimum number of copies of `s1` needed to construct `s2`. If some character of `s2` never appears in `s1`, the task is impossible.

The operation is entirely about subsequences. We are not rearranging characters, only skipping them. For example, if `s1 = "abc"` and `s2 = "cab"`, one copy is not enough because `"cab"` is not a subsequence of `"abc"`. Two copies work because `"cab"` is a subsequence of `"abcabc"`.

The constraints heavily shape the solution. The length of `s1` is at most `10^4`, which is small enough for preprocessing. The length of `s2` can reach `10^6`, which means any algorithm doing a full scan of `s1` for every character of `s2` would be far too slow. A quadratic style solution such as `O(|s1| * |s2|)` could require around `10^10` operations in the worst case, which is impossible within two seconds. The target complexity should be close to linear in `|s2|`, with at most logarithmic overhead.

Several edge cases are easy to mishandle.

Consider:

```
s1 = "abc"
s2 = "xyz"
```

The correct answer is `-1` because no amount of concatenation can create characters that never appear in `s1`. A careless greedy implementation might loop forever trying to match `'x'`.

Another tricky case is:

```
s1 = "abc"
s2 = "cab"
```

The correct answer is `2`. The first copy provides `'c'`, but after reaching the end of the string we must start over to obtain `'a'` and `'b'`. An implementation that only checks whether `s2` is a subsequence of repeated scans without counting resets correctly may output `1`.

Repeated characters also matter:

```
s1 = "ab"
s2 = "bbbb"
```

The answer is `4`. Each copy contributes only one `'b'`. A naive approach that counts distinct characters or frequencies instead of preserving order would fail here.

A subtle boundary condition appears when the current character exists in `s1`, but not after the current position:

```
s1 = "abca"
s2 = "aa"
```

The answer is `1`, because both `'a'` characters can be matched inside the same copy. If the current position handling is off by one, the algorithm may incorrectly start a new copy after the first `'a'`.

## Approaches

The most direct approach simulates the process literally. We keep scanning through `s1` trying to match characters of `s2` in order. Whenever we reach the end of `s1`, we start another copy and continue matching.

This brute-force method is correct because it follows exactly the subsequence construction process. For every character in `s2`, it searches for the next usable occurrence in the current copy of `s1`.

The problem is performance. Suppose `s1` has length `10^4` and `s2` has length `10^6`. In the worst case, for each character of `s2` we may scan almost all of `s1`. That produces roughly `10^10` character comparisons, which is far beyond the time limit.

The key observation is that repeated linear scans waste work. Every time we ask, “where is the next occurrence of character `c` after position `p`?”, we recompute the answer from scratch. Since `s1` never changes, we should preprocess it once and answer these queries quickly.

A convenient structure is to store, for every character, the sorted list of positions where it appears in `s1`.

For example:

```
s1 = "abac"
```

We store:

```
a -> [0, 2]
b -> [1]
c -> [3]
```

Now suppose we are currently at position `1` and need the next `'a'`. Instead of scanning linearly, we binary search inside `[0, 2]` to find the first value greater than `1`, which is `2`.

If no such position exists, the current copy of `s1` is exhausted. We start a new copy and take the first occurrence of that character.

This transforms the expensive repeated scans into efficient logarithmic queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | s1 | × |
| Optimal | O( | s1 | + |

## Algorithm Walkthrough

1. Preprocess `s1` by storing all occurrence positions for every character.

For each index `i` in `s1`, append `i` to the list corresponding to `s1[i]`.
2. Before processing `s2`, verify that every character of `s2` appears somewhere in `s1`.

If even one character is missing, print `-1` immediately because no number of concatenations can create it.
3. Start with one copy of `s1`.

Maintain a variable `pos` representing the current position inside the active copy. Initially set `pos = -1`, meaning we have not used any character yet.
4. Process characters of `s2` from left to right.

For the current character `c`, retrieve its sorted occurrence list.
5. Use binary search to find the first occurrence strictly greater than `pos`.

This gives the next valid subsequence position inside the current copy.
6. If such a position exists, move `pos` to that index.

We successfully matched the character without needing another newspaper.
7. If no valid occurrence exists, start a new copy of `s1`.

Increment the answer counter, then take the first occurrence of `c` from its list and set `pos` to that value.
8. After processing all characters, output the number of copies used.

### Why it works

The algorithm always consumes as much as possible from the current copy before starting a new one. This greedy choice is optimal because starting a new copy earlier never creates additional matching opportunities inside the current copy.

At every step, `pos` represents the latest matched position in the current newspaper. The binary search selects the earliest possible valid next occurrence. Choosing the earliest occurrence leaves the maximum remaining suffix available for future characters, which can only help.

Whenever no occurrence exists after `pos`, every subsequence continuation inside the current copy is impossible. Starting a new copy is not merely a choice, it is necessary.

Because the algorithm only starts a new copy when forced, the total number of copies is minimal.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    s1 = input().strip()
    s2 = input().strip()

    positions = {}

    for i, ch in enumerate(s1):
        if ch not in positions:
            positions[ch] = []
        positions[ch].append(i)

    for ch in s2:
        if ch not in positions:
            print(-1)
            return

    ans = 1
    pos = -1

    for ch in s2:
        arr = positions[ch]

        idx = bisect_right(arr, pos)

        if idx == len(arr):
            ans += 1
            pos = arr[0]
        else:
            pos = arr[idx]

    print(ans)

solve()
```

The preprocessing step builds a dictionary from characters to sorted occurrence positions. Since we scan `s1` from left to right, the lists are automatically sorted.

The impossibility check happens before the main loop. This avoids corner cases where the matching process would repeatedly fail on a missing character.

The variable `pos` tracks the latest matched index inside the current copy of `s1`. Using `-1` initially is convenient because the first valid occurrence for any character will always be greater than `-1`.

The crucial implementation detail is the use of `bisect_right`. We need the first occurrence strictly after the current position. Using `bisect_left` would incorrectly allow reusing the same character position multiple times.

When binary search fails to find a valid next position, we must start a new copy and use the first occurrence of the character. Forgetting to reset `pos` correctly here is a common bug.

The algorithm never explicitly constructs repeated copies of `s1`. It only simulates transitions between them, which keeps memory usage small even when the answer is large.

## Worked Examples

### Example 1

Input:

```
s1 = "abc"
s2 = "abcbc"
```

Occurrence lists:

```
a -> [0]
b -> [1]
c -> [2]
```

| Current char | Current pos | Next usable position | New copy needed | Answer |
| --- | --- | --- | --- | --- |
| a | -1 | 0 | No | 1 |
| b | 0 | 1 | No | 1 |
| c | 1 | 2 | No | 1 |
| b | 2 | none | Yes | 2 |
| c | 1 | 2 | No | 2 |

Final answer:

```
2
```

The trace shows the greedy behavior clearly. The first three characters fit inside one copy. After matching `'c'` at position `2`, no later `'b'` exists, so a new copy becomes mandatory.

### Example 2

Input:

```
s1 = "ab"
s2 = "bbbb"
```

Occurrence lists:

```
b -> [1]
```

| Current char | Current pos | Next usable position | New copy needed | Answer |
| --- | --- | --- | --- | --- |
| b | -1 | 1 | No | 1 |
| b | 1 | none | Yes | 2 |
| b | 1 | none | Yes | 3 |
| b | 1 | none | Yes | 4 |

Final answer:

```
4
```

This example demonstrates that the algorithm respects ordering constraints rather than frequencies. Each copy contributes only one usable `'b'`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s1 |
| Space | O( | s1 |

With `|s2|` up to `10^6`, the solution remains efficient because each step only performs a logarithmic search over occurrence lists. The memory usage is tiny compared to the limit, since we only store indices from `s1`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_right

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    s1 = input().strip()
    s2 = input().strip()

    positions = {}

    for i, ch in enumerate(s1):
        if ch not in positions:
            positions[ch] = []
        positions[ch].append(i)

    for ch in s2:
        if ch not in positions:
            return "-1"

    ans = 1
    pos = -1

    for ch in s2:
        arr = positions[ch]

        idx = bisect_right(arr, pos)

        if idx == len(arr):
            ans += 1
            pos = arr[0]
        else:
            pos = arr[idx]

    return str(ans)

# provided sample
assert run("abc\nxyz\n") == "-1", "sample 1"

# minimum size
assert run("a\na\n") == "1", "single character"

# repeated resets
assert run("ab\nbbbb\n") == "4", "multiple newspaper copies"

# subsequence fits in one copy
assert run("abca\naa\n") == "1", "same copy reuse"

# boundary transition
assert run("abc\ncab\n") == "2", "wrap to next copy"

# large repeated pattern
assert run("abc\nabcabcabc\n") == "3", "exact repeated copies"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abc / xyz` | `-1` | Missing character detection |
| `a / a` | `1` | Minimum valid input |
| `ab / bbbb` | `4` | Multiple forced resets |
| `abca / aa` | `1` | Correct handling of repeated characters inside one copy |
| `abc / cab` | `2` | Transition between copies |
| `abc / abcabcabc` | `3` | Exact concatenation behavior |

## Edge Cases

Consider the impossible case:

```
s1 = "abc"
s2 = "xyz"
```

During preprocessing, the algorithm stores positions only for `'a'`, `'b'`, and `'c'`. While checking `s2`, the character `'x'` is missing from the dictionary, so the algorithm immediately prints `-1`. No simulation occurs.

Now examine the wraparound case:

```
s1 = "abc"
s2 = "cab"
```

The algorithm first matches `'c'` at position `2`. The next character is `'a'`. Binary search inside `[0]` for a value greater than `2` fails, so the algorithm starts a new copy and sets `pos = 0`. Then `'b'` matches at position `1`. The final answer becomes `2`.

For repeated characters:

```
s1 = "ab"
s2 = "bbbb"
```

After matching the first `'b'` at position `1`, every later search for `'b'` inside the same copy fails because there is no position greater than `1`. The algorithm correctly starts a new copy every time, producing `4`.

Finally, consider:

```
s1 = "abca"
s2 = "aa"
```

The first `'a'` matches position `0`. For the second `'a'`, binary search finds position `3`, which is still inside the same copy. The answer remains `1`. This confirms the algorithm does not reset prematurely when another valid occurrence exists later in the current copy.
