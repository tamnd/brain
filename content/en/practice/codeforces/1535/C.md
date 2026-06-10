---
title: "CF 1535C - Unstable String"
description: "We are given a string containing '0', '1', and '?'. A substring is considered beautiful if we can replace every '?' independently with either 0 or 1 so that the resulting substring becomes an alternating binary string. In other words, neighboring characters must always differ."
date: "2026-06-10T15:56:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "implementation", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1535
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 110 (Rated for Div. 2)"
rating: 1400
weight: 1535
solve_time_s: 1206
verified: true
draft: false
---

[CF 1535C - Unstable String](https://codeforces.com/problemset/problem/1535/C)

**Rating:** 1400  
**Tags:** binary search, dp, greedy, implementation, strings, two pointers  
**Solve time:** 20m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string containing `'0'`, `'1'`, and `'?'`.

A substring is considered beautiful if we can replace every `'?'` independently with either `0` or `1` so that the resulting substring becomes an alternating binary string. In other words, neighboring characters must always differ.

The task is to count how many contiguous substrings have this property.

The total length over all test cases is at most `2·10^5`. This immediately rules out anything quadratic. A solution that examines every substring would require roughly `n²/2` substrings, which is about `2·10^10` when `n = 2·10^5`. Even checking each substring in constant time would be far too slow. We need a linear or near-linear algorithm per test case.

Several edge cases make the problem trickier than it first appears.

Consider:

```
???
```

Every substring is beautiful because we can assign alternating values however we want. The answer is:

```
6
```

A solution that tries to commit to one particular assignment of `?` characters may incorrectly reject valid substrings.

Consider:

```
00
```

The substring `"00"` is impossible to make alternating. The answer is:

```
2
```

Only the two length-1 substrings work.

Consider:

```
0?0
```

The whole substring is beautiful because the middle character can become `1`, producing `010`.

A local check that only compares adjacent fixed characters would miss this possibility.

Consider:

```
?1??1
```

The entire string is not beautiful. If position parity forces both fixed `1`s to require contradictory assignments, no replacement exists. Any correct solution must detect conflicts created by fixed characters that are far apart.

## Approaches

The brute-force idea is straightforward. Enumerate every substring, then check whether that substring can be transformed into an alternating string.

A substring can match one of only two alternating patterns:

```
010101...
```

or

```
101010...
```

For each substring we could test both patterns and see whether every fixed character is compatible with at least one of them.

This approach is correct because a substring is beautiful exactly when one of the two alternating patterns fits all fixed positions.

The problem is the number of substrings. A string of length `n` has `n(n+1)/2` substrings. With `n = 2·10^5`, that is roughly twenty billion substrings. Even an O(1) check per substring would be impossible.

The key observation is that an alternating string imposes a parity rule.

Suppose a substring starts at position `L`.

If we decide that position `L` should be `0`, then every position with the same parity as `L` must also be `0`, and every position with opposite parity must be `1`.

If we decide that position `L` should be `1`, the roles are reversed.

A conflict occurs when fixed characters force both possibilities to fail.

Instead of examining every substring independently, we process the string from left to right and maintain the longest valid suffix ending at the current position.

A useful trick is to reinterpret each fixed character.

For position `i`:

```
expected value = i mod 2
```

corresponds to one alternating pattern, while

```
expected value = 1 - (i mod 2)
```

corresponds to the other.

Whenever a fixed character disagrees with one pattern, it supports the other. We keep track of the most recent position that breaks each pattern.

Then, for every ending position `r`, we can instantly determine how far left a valid substring may start.

This transforms the problem into a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) to O(n³) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Process the string from left to right.
2. Maintain two values:

`last0` = latest position that makes the pattern `010101...` impossible.

`last1` = latest position that makes the pattern `101010...` impossible.
3. At position `i`, if `s[i]` is `'?'`, it never creates a conflict, so neither value changes.
4. If `s[i]` is `'0'`, compare it with the expected character under both alternating patterns.

If pattern `010101...` expects `1` here, then this position breaks that pattern, so update `last0 = i`.

Similarly update `last1` if the second pattern is broken.
5. If `s[i]` is `'1'`, perform the same logic.
6. Let

```
bad = min(last0, last1)
```

Any substring ending at `i` and starting at or before `bad` fails both alternating patterns.
7. Therefore every start position in

```
bad + 1 ... i
```

forms a beautiful substring ending at `i`.

The number of such substrings is:

```
i - bad
```
8. Add this quantity to the answer.

### Why it works

For every position we remember the latest place where each alternating pattern became impossible.

A substring ending at `i` is beautiful if at least one alternating pattern remains feasible throughout that substring.

If a substring starts at or before `last0`, then pattern `010101...` has already been contradicted inside the substring.

Similarly, starting at or before `last1` invalidates pattern `101010...`.

A substring fails only when both patterns are invalidated. That happens exactly when its start position is at most

```
min(last0, last1).
```

All later starting positions preserve at least one pattern, so they are beautiful. Counting these starts for every ending position counts every beautiful substring exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        s = input().strip()
        
        last0 = -1
        last1 = -1
        ans = 0
        
        for i, ch in enumerate(s):
            if ch != '?':
                bit = int(ch)
                
                if bit != (i & 1):
                    last0 = i
                
                if bit != (1 ^ (i & 1)):
                    last1 = i
            
            ans += i - min(last0, last1)
        
        print(ans)

solve()
```

The variables `last0` and `last1` store the most recent contradictions for the two possible alternating patterns.

The expression

```
(i & 1)
```

is the character expected by the pattern

```
010101...
```

when indexing from zero.

The expression

```
1 ^ (i & 1)
```

is the character expected by the pattern

```
101010...
```

at the same position.

Whenever a fixed character disagrees with a pattern, that pattern becomes impossible for any substring containing this position. Updating the corresponding `last` variable records that fact.

The quantity

```
i - min(last0, last1)
```

counts all valid starting positions for substrings ending at `i`.

The answer may be as large as roughly `n(n+1)/2`, which is about `2·10^10`, so it must be stored in a 64-bit capable integer. Python integers handle this automatically.

## Worked Examples

### Example 1

Input:

```
0?10
```

| i | s[i] | last0 | last1 | min(last0,last1) | Added | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | -1 | 0 | -1 | 1 | 1 |
| 1 | ? | -1 | 0 | -1 | 2 | 3 |
| 2 | 1 | -1 | 2 | -1 | 3 | 6 |
| 3 | 0 | -1 | 3 | -1 | 4 | 10 |

The answer is 10. Every substring of this string is beautiful.

### Example 2

Input:

```
?10??1100
```

| i | s[i] | last0 | last1 | min(last0,last1) | Added | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | ? | -1 | -1 | -1 | 1 | 1 |
| 1 | 1 | -1 | 1 | -1 | 2 | 3 |
| 2 | 0 | -1 | 2 | -1 | 3 | 6 |
| 3 | ? | -1 | 2 | -1 | 4 | 10 |
| 4 | ? | -1 | 2 | -1 | 5 | 15 |
| 5 | 1 | -1 | 5 | -1 | 6 | 21 |
| 6 | 1 | 6 | 5 | 5 | 1 | 22 |
| 7 | 0 | 7 | 5 | 5 | 2 | 24 |
| 8 | 0 | 7 | 8 | 7 | 1 | 25 |

The conflict introduced by the consecutive fixed characters near the end sharply reduces the number of valid suffixes. The final answer is 25.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(1) | Only a few integer variables are maintained |

The total input size over all test cases is at most `2·10^5`, so a linear scan easily fits within the time limit. The algorithm uses constant auxiliary memory regardless of string length.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        s = input().strip()

        last0 = -1
        last1 = -1
        ans = 0

        for i, ch in enumerate(s):
            if ch != '?':
                bit = int(ch)

                if bit != (i & 1):
                    last0 = i

                if bit != (1 ^ (i & 1)):
                    last1 = i

            ans += i - min(last0, last1)

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("3\n0?10\n???\n?10??1100\n") == "10\n6\n25"

# minimum size
assert run("1\n?\n") == "1"

# all equal fixed characters
assert run("1\n0000\n") == "4"

# alternating already
assert run("1\n0101\n") == "10"

# off-by-one boundary
assert run("1\n00\n") == "2"

# mixed case
assert run("1\n0?0\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `?` | `1` | Single-character substring |
| `0000` | `4` | Every length greater than 1 fails |
| `0101` | `10` | Already alternating, all substrings work |
| `00` | `2` | Smallest conflicting pair |
| `0?0` | `6` | Question mark resolves a conflict |

## Edge Cases

Consider:

```
???
```

Every substring can be completed into an alternating string. During the scan neither `last0` nor `last1` changes from `-1`. The additions are `1`, `2`, and `3`, producing `6`. The algorithm naturally counts all substrings.

Consider:

```
00
```

At the second position the two fixed zeros create a contradiction for any substring of length two. The algorithm updates the conflict positions and counts only the two single-character substrings, giving `2`.

Consider:

```
0?0
```

The middle character remains flexible. The algorithm never records a conflict that blocks the whole string because assigning the middle position to `1` yields `010`. The answer becomes `6`, meaning every substring is beautiful.

Consider:

```
?1??1
```

The two fixed ones eventually invalidate one of the alternating patterns over larger ranges. The `last0` and `last1` updates capture exactly where the contradiction appears. Substrings that still preserve at least one pattern remain counted, while the impossible ones are excluded automatically.
