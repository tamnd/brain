---
title: "CF 96A - Football"
description: "We are given a string made only of '0' and '1'. Each character represents the team of a football player standing in a line. A dangerous situation happens if at least seven consecutive players belong to the same team."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 96
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 77 (Div. 2 Only)"
rating: 900
weight: 96
solve_time_s: 84
verified: true
draft: false
---

[CF 96A - Football](https://codeforces.com/problemset/problem/96/A)

**Rating:** 900  
**Tags:** implementation, strings  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made only of `'0'` and `'1'`. Each character represents the team of a football player standing in a line. A dangerous situation happens if at least seven consecutive players belong to the same team.

The task is simply to check whether the string contains either seven consecutive `'0'` characters or seven consecutive `'1'` characters. If such a segment exists, we print `"YES"`. Otherwise, we print `"NO"`.

The input size is very small, at most 100 characters. Even an inefficient solution would easily fit within the limits. A quadratic algorithm would perform around 10,000 operations in the worst case, which is trivial for a 2 second limit. Still, the problem naturally admits a linear scan, which is simpler and cleaner.

The tricky part is not performance, it is handling consecutive runs correctly.

One easy mistake is resetting the counter incorrectly when the character changes.

Consider:

```
1111110
```

The correct answer is `"NO"` because the longest run of equal characters has length 6. A careless implementation that checks only the total number of `'1'` characters would incorrectly print `"YES"`.

Another common mistake is checking only exactly seven characters instead of at least seven.

Example:

```
11111111
```

The correct answer is `"YES"` because a run of length 8 still satisfies the condition. If the code checks only for runs equal to 7, it would fail here.

A third edge case appears when the dangerous sequence starts at the beginning or ends at the end of the string.

Example:

```
0000001
```

The correct answer is `"NO"` because the longest run is only 6.

Example:

```
10000000
```

The correct answer is `"YES"` because the final seven characters are all `'0'`.

Implementations that only compare middle positions can accidentally miss boundary runs.

## Approaches

The brute-force idea is to examine every substring of length 7 and check whether all characters inside it are identical.

For every starting position, we can inspect the next seven characters and verify whether they are all `'0'` or all `'1'`. Since the string length is at most 100, this approach is completely fast enough. In the worst case, we examine about 100 windows, each of size 7, so the work is roughly 700 character comparisons.

The brute-force works because the dangerous condition depends only on local consecutive segments. If any valid run exists, then at least one window of length 7 must contain identical characters.

A cleaner observation simplifies the implementation further. Instead of repeatedly checking windows, we can scan the string once while tracking the current streak length.

If the current character matches the previous one, we extend the streak. Otherwise, we reset the streak to 1 because a new run has started. The moment the streak reaches 7, we already know the answer is `"YES"`.

This turns the problem into a straightforward linear traversal with constant memory.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × 7) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Initialize a counter `count = 1` because the first character already forms a streak of length 1.
3. Traverse the string starting from index 1.
4. For each position, compare the current character with the previous character.
5. If they are equal, increment `count` because the consecutive run continues.
6. Otherwise, reset `count = 1` because a new streak starts from the current character.
7. After updating the counter, check whether `count >= 7`.
8. If it is, print `"YES"` and stop immediately because a dangerous situation has been found.
9. If the loop finishes without finding such a streak, print `"NO"`.

### Why it works

The algorithm maintains the invariant that `count` always equals the length of the current consecutive run ending at the current position.

When two adjacent characters match, the run extends naturally by one. When they differ, the previous run ends and a new run of length 1 begins.

Since every consecutive segment in the string is processed exactly once, any run of length at least 7 will eventually cause `count` to reach 7. If the algorithm never reaches that value, then no dangerous segment exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

count = 1

for i in range(1, len(s)):
    if s[i] == s[i - 1]:
        count += 1
    else:
        count = 1

    if count >= 7:
        print("YES")
        break
else:
    print("NO")
```

The program begins by reading the string and removing the trailing newline with `strip()`.

The variable `count` stores the length of the current consecutive sequence. It starts at 1 because a single character already forms a valid run of length one.

The loop starts from index 1 because every comparison uses `s[i - 1]`. Starting at index 0 would cause an invalid access.

When adjacent characters are equal, the streak grows by one. Otherwise, the streak resets because continuity has been broken.

The `if count >= 7` check is placed inside the loop immediately after updating the streak length. This catches runs as soon as they become dangerous.

The `for ... else` structure is useful here. The `else` block executes only if the loop never encounters a `break`. That means we print `"NO"` only when no dangerous segment was found.

## Worked Examples

### Example 1

Input:

```
001001
```

| Index | Character | Previous | Count |
| --- | --- | --- | --- |
| 0 | 0 | - | 1 |
| 1 | 0 | 0 | 2 |
| 2 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 |
| 4 | 0 | 0 | 2 |
| 5 | 1 | 0 | 1 |

The streak length never reaches 7, so the answer is `"NO"`. This example confirms that the algorithm resets correctly whenever the character changes.

### Example 2

Input:

```
00100110111111101
```

| Index | Character | Previous | Count |
| --- | --- | --- | --- |
| 0 | 0 | - | 1 |
| 1 | 0 | 0 | 2 |
| 2 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 |
| 4 | 0 | 0 | 2 |
| 5 | 1 | 0 | 1 |
| 6 | 1 | 1 | 2 |
| 7 | 0 | 1 | 1 |
| 8 | 1 | 0 | 1 |
| 9 | 1 | 1 | 2 |
| 10 | 1 | 1 | 3 |
| 11 | 1 | 1 | 4 |
| 12 | 1 | 1 | 5 |
| 13 | 1 | 1 | 6 |
| 14 | 1 | 1 | 7 |

At index 14, the streak reaches 7 consecutive `'1'` characters. The algorithm immediately prints `"YES"` and terminates early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(1) | Only a few variables are stored |

With a maximum string length of only 100, the solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()

    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            count = 1

        if count >= 7:
            print("YES")
            break
    else:
        print("NO")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("001001\n") == "NO", "sample 1"

# custom cases
assert run("1111111\n") == "YES", "exactly seven consecutive ones"
assert run("0000001\n") == "NO", "six consecutive zeros only"
assert run("10000000\n") == "YES", "seven zeros at the end"
assert run("1010101010\n") == "NO", "alternating characters"
assert run("11111111\n") == "YES", "more than seven consecutive ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1111111` | `YES` | Exact boundary of 7 |
| `0000001` | `NO` | Six consecutive characters is insufficient |
| `10000000` | `YES` | Dangerous streak at the end |
| `1010101010` | `NO` | Frequent resets of the counter |
| `11111111` | `YES` | Runs longer than 7 must also work |

## Edge Cases

Consider the input:

```
1111110
```

The algorithm processes six consecutive `'1'` characters, so `count` reaches 6. At the final character `'0'`, the streak resets to 1. Since `count` never becomes 7, the output is `"NO"`.

Now consider:

```
11111111
```

The streak grows as:

```
1 → 2 → 3 → 4 → 5 → 6 → 7
```

As soon as the seventh consecutive `'1'` is reached, the algorithm prints `"YES"`. The eighth character never causes problems because the condition checks for `>= 7`, not exactly 7.

Finally, consider:

```
10000000
```

The first character creates a streak of length 1. Starting from the second character, the algorithm keeps extending the run of `'0'` characters until the counter reaches 7 at the final position. The output becomes `"YES"`.

This confirms that sequences at the boundary of the string are handled correctly.
