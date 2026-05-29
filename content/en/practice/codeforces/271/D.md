---
title: "CF 271D - Good Substrings"
description: "We are given a lowercase string and a classification of the 26 English letters into two groups, good and bad. A substring is considered valid if it contains at most k bad characters. Among all such valid substrings, we must count how many different strings appear."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 271
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 166 (Div. 2)"
rating: 1800
weight: 271
solve_time_s: 102
verified: true
draft: false
---

[CF 271D - Good Substrings](https://codeforces.com/problemset/problem/271/D)

**Rating:** 1800  
**Tags:** data structures, strings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string and a classification of the 26 English letters into two groups, good and bad. A substring is considered valid if it contains at most `k` bad characters. Among all such valid substrings, we must count how many different strings appear.

The word "distinct" changes the nature of the problem. If the same substring content appears multiple times at different positions, it should only be counted once. For example, in `"abab"`, the substring `"ab"` appears twice, but contributes only one to the answer.

The string length is at most 1500. That is small enough to enumerate all substrings, because there are only about `n^2 / 2` of them. For `n = 1500`, the total number of substrings is roughly 1.1 million. A quadratic solution is completely realistic in Python. Cubic solutions are not. If we tried to build every substring character by character and compare strings directly, the total work could grow toward `O(n^3)`.

The distinctness requirement is the tricky part. We cannot simply count valid intervals. Two different intervals may produce identical substring contents. We need a way to uniquely identify substring contents efficiently.

Several edge cases are easy to mishandle.

Consider the case where `k = 0`.

Input:

```
abc
11111111111111111111111110
0
```

Here only `'z'` is bad, so every character in `"abc"` is good. Every substring is valid, and the answer is 6. A careless implementation that stops too early when seeing a bad character might accidentally reject valid substrings.

Now consider the opposite situation where all characters are bad.

Input:

```
aaa
00000000000000000000000000
1
```

Only substrings with length 1 are allowed, because every character is bad and we may use at most one bad character. The distinct valid substrings are only `"a"`, so the answer is 1. Counting intervals instead of distinct strings would incorrectly produce 3.

Repeated substrings are another common source of bugs.

Input:

```
abab
11111111111111111111111111
4
```

Every substring is valid. The distinct substrings are:

`"a"`, `"b"`, `"ab"`, `"ba"`, `"aba"`, `"bab"`, `"abab"`.

The answer is 7, not 10. Any solution that inserts intervals instead of substring contents into a set will overcount.

Hash collisions are also a concern if hashing is implemented carelessly. With a single weak hash and no modulus discipline, two different substrings could accidentally appear equal. Competitive programming solutions usually accept a single large rolling hash here because constraints are small, but we should still implement it carefully.

## Approaches

The brute-force idea is straightforward. Generate every substring, count how many bad characters it contains, and if the count is within the limit, insert the substring itself into a set.

There are `O(n^2)` substrings. Creating a Python substring `s[l:r+1]` costs `O(length)`, because strings are copied. In the worst case, total substring length across all substrings is `O(n^3)`. With `n = 1500`, that becomes several billion character operations, which is too slow.

The bad-character counting can also become expensive if we recompute it for every substring. We need to avoid repeated scanning.

The first improvement is easy. While extending a substring from a fixed starting point, we maintain the current number of bad characters incrementally. Once the count exceeds `k`, any longer substring starting at the same position will also exceed `k`, so we can stop immediately.

That reduces the validation work to roughly quadratic.

The remaining problem is distinctness. We still cannot afford to store full substring strings repeatedly.

This is where rolling hash becomes useful. Instead of storing the actual substring, we store a numeric fingerprint. Using polynomial hashing, every substring can be represented in `O(1)` time after preprocessing.

The structure of the problem fits rolling hash perfectly because:

1. We enumerate many overlapping substrings.
2. We only need equality comparison between substrings.
3. The string length is small enough that one hash is practically safe.

We preprocess prefix hashes and powers of the base. Then every substring hash can be computed instantly. During enumeration, every valid substring contributes its hash into a set. The final set size is the number of distinct good substrings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n²) | Too slow |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the string `s`, the 26-character good/bad mask, and the limit `k`.
2. Build a helper array that tells whether a character is bad.

For example, if the mask has `'0'` at position 1, then `'b'` is bad.
3. Precompute rolling hash arrays.

We maintain:

- `prefix[i]`, the hash of the prefix ending before index `i`
- `power[i]`, the base raised to power `i`

This allows any substring hash to be extracted in constant time.
4. Iterate over every starting index `l`.
5. For each `l`, extend the substring one character at a time toward the right.

Maintain a running count `bad_count`.
6. Whenever a new character is added:

- If the character is bad, increment `bad_count`.
- If `bad_count > k`, stop extending from this `l`.

Longer substrings would only contain even more bad characters.
7. For every valid substring `s[l:r]`, compute its rolling hash in `O(1)` time and insert it into a set.

The set automatically removes duplicates.
8. After all substrings are processed, print the size of the set.

### Why it works

For every starting position, we examine substrings in increasing order of length. The moment the number of bad characters exceeds `k`, every longer substring starting there also becomes invalid because adding characters cannot decrease the bad count.

Every valid substring is inserted exactly once into the hash set. If two substrings have identical contents, their rolling hashes are equal, so the set stores only one copy. If the contents differ, their hashes differ with overwhelming probability.

Because we enumerate all valid substrings and deduplicate by content, the final set size equals the number of distinct good substrings.

## Python Solution

```python
import sys
input = sys.stdin.readline

BASE = 911382323
MOD = 10**18 + 3

def solve():
    s = input().strip()
    good = input().strip()
    k = int(input())

    n = len(s)

    power = [1] * (n + 1)
    prefix = [0] * (n + 1)

    for i in range(n):
        power[i + 1] = (power[i] * BASE) % MOD
        value = ord(s[i]) - ord('a') + 1
        prefix[i + 1] = (prefix[i] * BASE + value) % MOD

    seen = set()

    for l in range(n):
        bad_count = 0

        for r in range(l, n):
            ch = s[r]

            if good[ord(ch) - ord('a')] == '0':
                bad_count += 1

            if bad_count > k:
                break

            current_hash = (
                prefix[r + 1]
                - prefix[l] * power[r - l + 1]
            ) % MOD

            seen.add(current_hash)

    print(len(seen))

solve()
```

The preprocessing section builds polynomial rolling hashes. The recurrence:

```
prefix[i + 1] = prefix[i] * BASE + value
```

treats the string like a number in base `BASE`.

The substring hash formula is the standard prefix subtraction:

```
prefix[r + 1] - prefix[l] * power[length]
```

The modulo operation afterward is important because subtraction may become negative.

The nested loops enumerate all substrings starting from each `l`. Instead of recomputing bad-character counts from scratch, the algorithm updates `bad_count` incrementally while extending `r`.

The `break` is critical. Once the substring already contains too many bad characters, every longer substring from the same starting position is also invalid.

Using a set automatically handles distinctness. Even if `"ab"` appears many times, its hash is inserted only once.

The modulus is intentionally very large to reduce collision probability. For this problem size, a single rolling hash is sufficient in practice.

## Worked Examples

### Sample 1

Input:

```
ababab
01000000000000000000000000
1
```

Only `'b'` is good. `'a'` is bad. We may use at most one bad character.

| l | r | Substring | Bad Count | Valid | Added |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | a | 1 | Yes | a |
| 0 | 1 | ab | 1 | Yes | ab |
| 0 | 2 | aba | 2 | No | stop |
| 1 | 1 | b | 0 | Yes | b |
| 1 | 2 | ba | 1 | Yes | ba |
| 1 | 3 | bab | 1 | Yes | bab |
| 1 | 4 | baba | 2 | No | stop |

The distinct valid substrings become:

```
a, ab, b, ba, bab
```

The answer is 5.

This trace shows why early stopping is correct. Once `"aba"` exceeds the bad limit, every longer substring starting at index 0 also fails.

### Example 2

Input:

```
aaa
00000000000000000000000000
1
```

Every character is bad, and only one bad character is allowed.

| l | r | Substring | Bad Count | Valid | Added |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | a | 1 | Yes | a |
| 0 | 1 | aa | 2 | No | stop |
| 1 | 1 | a | 1 | Yes | duplicate |
| 1 | 2 | aa | 2 | No | stop |
| 2 | 2 | a | 1 | Yes | duplicate |

Only `"a"` remains in the set.

The answer is 1.

This example demonstrates why distinctness matters. There are three valid intervals, but only one distinct substring.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | We examine each valid substring once |
| Space | O(n²) | In the worst case the set may contain all distinct substrings |

The maximum number of substrings for `n = 1500` is about 1.1 million, which is manageable in Python with hashing and early termination. The algorithm comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

BASE = 911382323
MOD = 10**18 + 3

def solve():
    input = sys.stdin.readline

    s = input().strip()
    good = input().strip()
    k = int(input())

    n = len(s)

    power = [1] * (n + 1)
    prefix = [0] * (n + 1)

    for i in range(n):
        power[i + 1] = (power[i] * BASE) % MOD
        value = ord(s[i]) - ord('a') + 1
        prefix[i + 1] = (prefix[i] * BASE + value) % MOD

    seen = set()

    for l in range(n):
        bad_count = 0

        for r in range(l, n):
            if good[ord(s[r]) - ord('a')] == '0':
                bad_count += 1

            if bad_count > k:
                break

            h = (
                prefix[r + 1]
                - prefix[l] * power[r - l + 1]
            ) % MOD

            seen.add(h)

    print(len(seen))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup

    return out.getvalue().strip()

# provided sample
assert run(
"""ababab
01000000000000000000000000
1
"""
) == "5", "sample 1"

# minimum size
assert run(
"""a
11111111111111111111111111
0
"""
) == "1", "single valid character"

# all characters bad
assert run(
"""aaa
00000000000000000000000000
1
"""
) == "1", "distinctness with repeated substrings"

# all substrings valid
assert run(
"""abc
11111111111111111111111111
3
"""
) == "6", "all substrings distinct"

# repeated pattern
assert run(
"""abab
11111111111111111111111111
4
"""
) == "7", "duplicate substrings should merge"

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` with all good letters | `1` | Minimum-size input |
| `aaa` with all bad letters and `k=1` | `1` | Distinct substring handling |
| `abc` with all good letters | `6` | Every substring accepted |
| `abab` with all good letters | `7` | Duplicate substring merging |

## Edge Cases

Consider the situation where no bad characters are allowed.

Input:

```
abc
11111111111111111111111110
0
```

Here only `'z'` is bad, so every substring is valid. The algorithm never triggers the `break`, and all six substrings are inserted into the set:

```
a, b, c, ab, bc, abc
```

The output becomes 6.

Now consider the opposite extreme.

Input:

```
aaa
00000000000000000000000000
1
```

Every character is bad. Starting from any index, the first character creates `bad_count = 1`, which is still valid. Extending by one more character creates `bad_count = 2`, triggering the break immediately.

Only the hash for `"a"` is inserted, so the answer is correctly 1.

Repeated substring structure is another subtle case.

Input:

```
abab
11111111111111111111111111
4
```

Every substring is valid, but several contents repeat:

- `"a"` appears twice
- `"b"` appears twice
- `"ab"` appears twice

Because hashes are stored in a set, duplicates collapse automatically. The final count is 7 instead of 10.

Finally, consider the boundary case where the substring becomes invalid exactly after adding one character.

Input:

```
abca
01111111111111111111111111
1
```

Here `'a'` is bad and every other character is good.

Starting from index 0:

- `"a"` has 1 bad character, valid
- `"ab"` has 1 bad character, valid
- `"abc"` has 1 bad character, valid
- `"abca"` has 2 bad characters, invalid

The algorithm breaks immediately after `"abca"` becomes invalid. No longer substring starting at index 0 could ever become valid again, so the pruning is correct.
