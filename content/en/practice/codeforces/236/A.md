---
title: "CF 236A - Boy or Girl"
description: "We are given a username consisting only of lowercase English letters. The task is to count how many different characters appear in that username. The decision rule is simple. If the number of distinct characters is even, we print \"CHAT WITH HER!\"."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 236
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 146 (Div. 2)"
rating: 800
weight: 236
solve_time_s: 207
verified: true
draft: false
---

[CF 236A - Boy or Girl](https://codeforces.com/problemset/problem/236/A)

**Rating:** 800  
**Tags:** brute force, implementation, strings  
**Solve time:** 3m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a username consisting only of lowercase English letters. The task is to count how many different characters appear in that username.

The decision rule is simple. If the number of distinct characters is even, we print `"CHAT WITH HER!"`. If the number is odd, we print `"IGNORE HIM!"`.

The input size is tiny. The username length is at most 100 characters, so even relatively inefficient approaches would run comfortably within the time limit. A quadratic solution would perform at most around 10,000 character comparisons, which is trivial for modern hardware. This means the problem is not about optimization pressure, it is about implementing the logic correctly and cleanly.

The main source of mistakes is misunderstanding what “distinct characters” means. We only count each unique letter once, regardless of how many times it appears.

Consider the input:

```
aaaa
```

The correct number of distinct characters is `1`, not `4`. Since `1` is odd, the correct output is:

```
IGNORE HIM!
```

A careless implementation that simply checks the total string length would incorrectly print `"CHAT WITH HER!"`.

Another easy mistake is forgetting repeated characters that appear far apart in the string.

For example:

```
abac
```

The distinct letters are `a`, `b`, and `c`, so the count is `3`. The correct output is:

```
IGNORE HIM!
```

If we only compare neighboring characters, we would incorrectly count `a` twice.

There is also a boundary case with a single-character username:

```
z
```

There is exactly one distinct character, so the answer is:

```
IGNORE HIM!
```

This checks whether the implementation handles the smallest valid input correctly.

## Approaches

The most direct brute-force approach is to examine every character and manually check whether we have seen it before. For each position, we scan all previous positions to determine whether the character is new.

For a string of length `n`, this performs roughly:

```
1 + 2 + 3 + ... + n = O(n²)
```

comparisons in the worst case.

With `n ≤ 100`, this is still perfectly acceptable. Even 10,000 operations is negligible.

The brute-force idea works because the alphabet is small and the input size is tiny. Still, there is a cleaner observation available. We do not actually care about the order of characters or their frequencies. We only care about the set of unique letters.

Python already provides a built-in `set` structure that automatically stores only distinct elements. Converting the string into a set immediately removes duplicates.

For example:

```
set("wjmzbmr")
```

becomes:

```
{'w', 'j', 'm', 'z', 'b', 'r'}
```

The size of this set is exactly the number of distinct characters. Once we know that count, we simply check whether it is even or odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the username string from input.
2. Convert the string into a set.

A set automatically removes duplicate characters, leaving only distinct letters.
3. Compute the size of the set.

This gives the number of unique characters in the username.
4. Check whether this count is even or odd.

If the count is even, print `"CHAT WITH HER!"`.

Otherwise, print `"IGNORE HIM!"`.

### Why it works

The algorithm relies on the property that a set contains each value at most once. After converting the username into a set, every repeated occurrence of a character disappears automatically. The size of the set is therefore exactly equal to the number of distinct characters in the username.

The problem’s rule depends only on the parity of this count. Checking `count % 2` correctly determines whether the number of distinct characters is even or odd, so the algorithm always produces the required output.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

distinct_count = len(set(s))

if distinct_count % 2 == 0:
    print("CHAT WITH HER!")
else:
    print("IGNORE HIM!")
```

The first line reads the username and removes the trailing newline using `strip()`.

The expression `set(s)` creates a collection containing only unique characters from the string. Calling `len()` on this set gives the number of distinct letters.

The final condition checks the parity of that count. If the remainder after division by `2` is zero, the count is even and we print `"CHAT WITH HER!"`. Otherwise, we print `"IGNORE HIM!"`.

One subtle implementation detail is the use of `strip()`. Without it, the newline character `\n` from the input could accidentally become part of the set, increasing the distinct character count by one and producing the wrong answer.

## Worked Examples

### Example 1

Input:

```
wjmzbmr
```

| Step | Current Character | Distinct Characters |
| --- | --- | --- |
| 1 | w | {w} |
| 2 | j | {w, j} |
| 3 | m | {w, j, m} |
| 4 | z | {w, j, m, z} |
| 5 | b | {w, j, m, z, b} |
| 6 | m | {w, j, m, z, b} |
| 7 | r | {w, j, m, z, b, r} |

The final set contains 6 distinct characters. Since 6 is even, the output is:

```
CHAT WITH HER!
```

This example demonstrates that repeated characters such as `m` are counted only once.

### Example 2

Input:

```
xiaodao
```

| Step | Current Character | Distinct Characters |
| --- | --- | --- |
| 1 | x | {x} |
| 2 | i | {x, i} |
| 3 | a | {x, i, a} |
| 4 | o | {x, i, a, o} |
| 5 | d | {x, i, a, o, d} |
| 6 | a | {x, i, a, o, d} |
| 7 | o | {x, i, a, o, d} |

The final set contains 5 distinct characters. Since 5 is odd, the output is:

```
IGNORE HIM!
```

This trace confirms that multiple repeated letters do not affect the distinct count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is inserted into the set once |
| Space | O(n) | The set may store all distinct characters |

The maximum username length is only 100, so this solution easily fits within the time and memory limits. Even a slower quadratic approach would pass, but the set-based solution is both cleaner and more scalable.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()

    if len(set(s)) % 2 == 0:
        print("CHAT WITH HER!")
    else:
        print("IGNORE HIM!")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("wjmzbmr\n") == "CHAT WITH HER!", "sample 1"

# custom cases
assert run("a\n") == "IGNORE HIM!", "single character"
assert run("aaaa\n") == "IGNORE HIM!", "all characters equal"
assert run("ab\n") == "CHAT WITH HER!", "small even distinct count"
assert run("abcdefghijklmnopqrstuvwxyz\n") == "CHAT WITH HER!", "maximum distinct letters"
assert run("abac\n") == "IGNORE HIM!", "non-adjacent duplicate characters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `IGNORE HIM!` | Minimum-size input |
| `aaaa` | `IGNORE HIM!` | Repeated characters counted once |
| `ab` | `CHAT WITH HER!` | Small even distinct count |
| `abcdefghijklmnopqrstuvwxyz` | `CHAT WITH HER!` | Maximum possible distinct letters |
| `abac` | `IGNORE HIM!` | Duplicate letters appearing far apart |

## Edge Cases

A common mistake is confusing string length with the number of distinct characters.

Consider:

```
aaaa
```

The algorithm converts the string into:

```
{'a'}
```

The distinct count is `1`, which is odd, so the output becomes:

```
IGNORE HIM!
```

This correctly ignores repeated occurrences of the same character.

Another tricky case is when duplicate letters are separated.

Input:

```
abac
```

The set evolves as:

```
{'a'}
{'a', 'b'}
{'a', 'b'}
{'a', 'b', 'c'}
```

The final count is `3`, so the output is:

```
IGNORE HIM!
```

This confirms that the algorithm tracks uniqueness globally, not just between neighboring characters.

The smallest valid input also works correctly.

Input:

```
z
```

The set becomes:

```
{'z'}
```

The count is `1`, which is odd, so the algorithm prints:

```
IGNORE HIM!
```

This verifies correct handling of boundary-size input.
