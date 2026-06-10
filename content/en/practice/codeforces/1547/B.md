---
title: "CF 1547B - Alphabetical Strings"
description: "We are given a string and need to determine whether it could have been built by the following process. We start with an empty string. First we place 'a'. Then we place 'b', then 'c', and so on, always using consecutive letters of the alphabet."
date: "2026-06-10T13:42:35+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1547
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 731 (Div. 3)"
rating: 800
weight: 1547
solve_time_s: 347
verified: false
draft: false
---

[CF 1547B - Alphabetical Strings](https://codeforces.com/problemset/problem/1547/B)

**Rating:** 800  
**Tags:** greedy, implementation, strings  
**Solve time:** 5m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string and need to determine whether it could have been built by the following process.

We start with an empty string. First we place `'a'`. Then we place `'b'`, then `'c'`, and so on, always using consecutive letters of the alphabet. Each new letter may only be attached to the current left end or the current right end of the existing string.

The question is whether the given string could be the final result of such a construction.

For example, `"bac"` is valid. We can start with `"a"`, place `'b'` on the left to get `"ba"`, then place `'c'` on the right to get `"bac"`.

The length of the string is at most 26, since there are only 26 lowercase letters. Even though there can be up to 10,000 test cases, each individual string is tiny. This means we can afford to perform several scans of each string without any concern for performance. Any algorithm proportional to the string length is effectively constant time.

The main difficulty is recognizing the construction in reverse.

A common mistake is to check only whether the string contains consecutive letters. Consider:

```
acb
```

The letters are exactly `'a'`, `'b'`, and `'c'`, but the answer is `NO`. Starting from `'a'`, there is no sequence of left/right insertions that produces `"acb"`.

Another easy trap is forgetting that the string must contain `'a'`.

```
z
```

The answer is `NO` because every valid construction starts with `'a'`.

Repeated letters must also be rejected.

```
aa
```

The answer is `NO`. The construction uses each letter at most once.

A more subtle case is:

```
xyz
```

These are consecutive letters, but valid strings always use the first `n` letters of the alphabet. A length-3 alphabetical string must consist of `'a'`, `'b'`, and `'c'`, not `'x'`, `'y'`, and `'z'`.

## Approaches

A brute-force solution would try to simulate every possible construction. For a string of length `n`, each of the letters after `'a'` can be placed on either the left or the right. That creates `2^(n-1)` possible strings.

For `n = 26`, this becomes:

```
2^25 = 33,554,432
```

possible constructions. Generating and checking tens of millions of candidates is unnecessary.

The key observation is that the construction process is much easier to verify backwards.

Suppose a string is valid. The largest letter present must have been inserted last. Since every insertion happens at one of the two ends, the largest letter must currently be at one of the two ends of the final string.

For example, if the string contains letters `'a'` through `'e'`, then `'e'` must be at the leftmost or rightmost position.

After removing `'e'`, the same argument applies to `'d'`. It must now be at one of the ends of the remaining substring. Then `'c'`, then `'b'`, and finally `'a'`.

This suggests a greedy verification process. We repeatedly look for the current largest required letter and check whether it lies at either end of the remaining interval. If it does, we remove that end. If it does not, the string could never have been produced by the allowed construction.

Because each letter is processed exactly once, the solution runs in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Let `n` be the length of the string.
2. Find the position of `'a'`. If `'a'` does not appear exactly once, immediately answer `NO`.
3. Maintain two pointers, `l` and `r`, initially both equal to the position of `'a'`.
4. We will try to expand outward while expecting letters `'b'`, `'c'`, `'d'`, and so on.
5. For each expected letter:

Check whether it is immediately to the left of the current interval, at position `l - 1`.

If so, move `l` one step left.
6. Otherwise, check whether it is immediately to the right of the current interval, at position `r + 1`.

If so, move `r` one step right.
7. If the expected letter is in neither location, answer `NO`.
8. If every letter from `'b'` through the largest required letter is successfully attached, answer `YES`.

The idea is that we reconstruct the original building process. The current interval always represents the letters already confirmed to form a valid alphabetical block. The next letter must have been attached directly to one of its ends. If it is not found there, no valid construction exists.

### Why it works

The invariant is that the substring between `l` and `r` contains exactly the letters already verified, arranged exactly as they would appear in a valid construction.

Initially this is true because the interval contains only `'a'`.

Assume it remains true after processing letters up to some character `c`. In a valid alphabetical string, the next character must have been appended to the left end or right end of the existing block. Consequently, in the final string that character must be immediately adjacent to the current interval. If it appears anywhere else, the construction rules are violated.

When we extend the interval by one position containing the expected next character, the invariant continues to hold.

If all letters are processed successfully, we have reconstructed a legal sequence of insertions, proving the string is alphabetical. If some expected character cannot be attached to either end, no legal insertion sequence could have produced the string, so the answer is `NO`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_alphabetical(s):
    n = len(s)

    if s.count('a') != 1:
        return False

    pos = s.index('a')
    l = r = pos

    for ch in range(ord('b'), ord('a') + n):
        c = chr(ch)

        if l > 0 and s[l - 1] == c:
            l -= 1
        elif r + 1 < n and s[r + 1] == c:
            r += 1
        else:
            return False

    return True

t = int(input())

for _ in range(t):
    s = input().strip()
    print("YES" if is_alphabetical(s) else "NO")
```

The first check guarantees that there is exactly one `'a'`. Any valid construction starts from a single `'a'`, so missing or repeated occurrences immediately invalidate the string.

The pointers `l` and `r` describe the verified interval. At the beginning this interval contains only `'a'`.

The loop processes expected characters in increasing alphabetical order. For a string of length `n`, the required letters are exactly `'a'` through `'a' + n - 1`. If the next character appears immediately to the left, we expand left. If it appears immediately to the right, we expand right.

The order of the two checks does not matter because a character cannot simultaneously appear on both sides. The boundary checks `l > 0` and `r + 1 < n` prevent out-of-range access.

Once all required letters are attached successfully, the string satisfies the construction rules.

## Worked Examples

### Example 1

Input:

```
bac
```

| Expected Letter | l | r | Action |
| --- | --- | --- | --- |
| a | 1 | 1 | Start at position of `a` |
| b | 0 | 1 | Found left of interval |
| c | 0 | 2 | Found right of interval |

The interval grows from `"a"` to `"ba"` and then to `"bac"`. Every next letter appears exactly where a valid insertion would place it, so the answer is `YES`.

### Example 2

Input:

```
acb
```

| Expected Letter | l | r | Action |
| --- | --- | --- | --- |
| a | 0 | 0 | Start at position of `a` |
| b | 0 | 0 | Not at left or right boundary |

The next required character is `'b'`, but the only adjacent position contains `'c'`. Since `'b'` cannot be attached to the existing block, reconstruction fails immediately. The answer is `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed at most once |
| Space | O(1) | Only a few indices and variables are stored |

Since `n ≤ 26`, the running time is extremely small. Even with `10^4` test cases, the total amount of work is only a few hundred thousand character operations, well within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def is_alphabetical(s):
        n = len(s)

        if s.count('a') != 1:
            return False

        pos = s.index('a')
        l = r = pos

        for ch in range(ord('b'), ord('a') + n):
            c = chr(ch)

            if l > 0 and s[l - 1] == c:
                l -= 1
            elif r + 1 < n and s[r + 1] == c:
                r += 1
            else:
                return False

        return True

    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()
        ans.append("YES" if is_alphabetical(s) else "NO")

    print("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run(
"""11
a
ba
ab
bac
ihfcbadeg
z
aa
ca
acb
xyz
ddcba
"""
) == """YES
YES
YES
YES
YES
NO
NO
NO
NO
NO
NO
"""

# minimum size
assert run(
"""1
a
"""
) == """YES
"""

# missing 'a'
assert run(
"""1
z
"""
) == """NO
"""

# duplicate 'a'
assert run(
"""1
aa
"""
) == """NO
"""

# maximum length valid string
assert run(
"""1
zyxwvutsrqponmlkjihgfedcba
"""
) == """YES
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `YES` | Smallest valid string |
| `z` | `NO` | Missing `'a'` |
| `aa` | `NO` | Duplicate letters |
| `zyxwvutsrqponmlkjihgfedcba` | `YES` | Maximum length and continuous left expansions |

## Edge Cases

### String without `'a'`

Input:

```
1
z
```

The algorithm first checks the number of occurrences of `'a'`. The count is zero, so it immediately returns `NO`.

This is correct because every valid construction begins with `'a'`.

### Multiple occurrences of `'a'`

Input:

```
1
aa
```

The count of `'a'` is two. The algorithm rejects the string before any further processing.

A valid construction never reuses a letter, so two `'a'` characters are impossible.

### Consecutive letters but wrong arrangement

Input:

```
1
acb
```

The interval starts at position `0`, containing `'a'`.

The next required character is `'b'`.

The position to the right contains `'c'`, not `'b'`, and there is no position to the left.

The algorithm returns `NO`.

This demonstrates why merely checking that the string contains consecutive letters is insufficient. The relative placement must also be achievable through left/right insertions.

### Largest valid size

Input:

```
1
zyxwvutsrqponmlkjihgfedcba
```

The interval starts at the final position containing `'a'`.

Each subsequent character appears immediately to the left of the current interval:

```
b, c, d, ..., z
```

The interval expands left until it covers the entire string. Every step succeeds, so the algorithm returns `YES`.

This confirms that the pointer logic correctly handles expansions reaching the boundary of the string.
