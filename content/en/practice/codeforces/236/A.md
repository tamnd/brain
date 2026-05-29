---
title: "CF 236A - Boy or Girl"
description: "We are given a username consisting only of lowercase English letters. The task is to count how many different characters appear in the string. The rule is simple. If the number of distinct letters is even, we print CHAT WITH HER!. If the number is odd, we print IGNORE HIM!."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 236
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 146 (Div. 2)"
rating: 800
weight: 236
solve_time_s: 99
verified: true
draft: false
---

[CF 236A - Boy or Girl](https://codeforces.com/problemset/problem/236/A)

**Rating:** 800  
**Tags:** brute force, implementation, strings  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a username consisting only of lowercase English letters. The task is to count how many different characters appear in the string.

The rule is simple. If the number of distinct letters is even, we print `CHAT WITH HER!`. If the number is odd, we print `IGNORE HIM!`.

The input size is extremely small. The username length is at most 100 characters, so even inefficient approaches would finish instantly. This means the real challenge is not optimization, but implementing the logic correctly and avoiding mistakes when counting unique characters.

A common mistake is counting total characters instead of distinct characters. For example:

Input:

```
aaaa
```

The correct number of distinct letters is `1`, not `4`. Since `1` is odd, the correct output is:

```
IGNORE HIM!
```

Another easy mistake is reversing the parity rule. The problem says even means female, odd means male. For example:

Input:

```
ab
```

There are `2` distinct letters, which is even, so the correct output is:

```
CHAT WITH HER!
```

A careless implementation might accidentally print the opposite result.

There is also the edge case where every character is unique.

Input:

```
abcdef
```

There are `6` distinct characters, so the answer is:

```
CHAT WITH HER!
```

And the opposite extreme:

Input:

```
z
```

Only one distinct character exists, so the output is:

```
IGNORE HIM!
```

## Approaches

The most direct brute-force idea is to compare every character against every other character and manually track whether we have already seen it before.

For each character, we scan all previous characters. If it never appeared earlier, we increase the count of distinct letters.

With a string length of at most 100, this works comfortably. The worst case performs roughly `100 * 100 = 10,000` comparisons, which is tiny.

The brute-force works because the constraints are small, but the implementation becomes unnecessarily verbose. We have to manually check duplicates and maintain the distinct count ourselves.

The key observation is that the problem only cares about unique characters. Python already provides a structure designed for exactly this purpose: a set.

A set automatically removes duplicates. If we convert the username into a set, its size becomes the number of distinct letters.

For example:

```
set("wjmzbmr")
```

becomes:

```
{'w', 'j', 'm', 'z', 'b', 'r'}
```

The set size is `6`.

After that, we only need to check whether the count is even or odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the username string from input.
2. Convert the string into a set.

A set stores only unique values, so duplicate letters disappear automatically.
3. Compute the size of the set.

This gives the number of distinct characters in the username.
4. Check whether the count is even or odd.

If the count is even, print `CHAT WITH HER!`. Otherwise, print `IGNORE HIM!`.

### Why it works

The algorithm relies on the property that a set contains each value exactly once. Every repeated character is collapsed into a single copy. Because of this, the size of the set is exactly equal to the number of distinct letters in the username.

The final decision depends only on the parity of that count. Since the algorithm computes the distinct count correctly, the printed result is always correct.

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

The first step reads the username and removes the trailing newline using `strip()`.

The expression `set(s)` creates a set containing only unique characters from the string. Calling `len()` on that set gives the number of distinct letters.

The parity check uses the modulo operator `%`. If the count is divisible by `2`, the count is even, so we print `CHAT WITH HER!`. Otherwise, we print `IGNORE HIM!`.

One subtle implementation detail is using `strip()`. Without it, the newline character `\n` from input could accidentally become part of the set, increasing the distinct count by one and producing the wrong answer.

## Worked Examples

### Example 1

Input:

```
wjmzbmr
```

| Step | Current Character | Distinct Set |
| --- | --- | --- |
| 1 | w | {w} |
| 2 | j | {w, j} |
| 3 | m | {w, j, m} |
| 4 | z | {w, j, m, z} |
| 5 | b | {w, j, m, z, b} |
| 6 | m | {w, j, m, z, b} |
| 7 | r | {w, j, m, z, b, r} |

The final set contains `6` distinct letters. Since `6` is even, the output is:

```
CHAT WITH HER!
```

This example demonstrates how duplicate letters do not affect the distinct count.

### Example 2

Input:

```
xiaodao
```

| Step | Current Character | Distinct Set |
| --- | --- | --- |
| 1 | x | {x} |
| 2 | i | {x, i} |
| 3 | a | {x, i, a} |
| 4 | o | {x, i, a, o} |
| 5 | d | {x, i, a, o, d} |
| 6 | a | {x, i, a, o, d} |
| 7 | o | {x, i, a, o, d} |

The final set contains `5` distinct letters. Since `5` is odd, the output is:

```
IGNORE HIM!
```

This trace confirms that repeated characters are ignored correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is inserted into the set once |
| Space | O(n) | The set may store all characters if they are unique |

Here `n` is the username length, at most `100`. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

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

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("wjmzbmr\n") == "CHAT WITH HER!\n", "sample 1"

# minimum length
assert run("a\n") == "IGNORE HIM!\n", "single character"

# all characters equal
assert run("aaaaaa\n") == "IGNORE HIM!\n", "all equal"

# all characters unique with even count
assert run("abcd\n") == "CHAT WITH HER!\n", "even distinct count"

# all characters unique with odd count
assert run("abc\n") == "IGNORE HIM!\n", "odd distinct count"

# maximum style case
assert run("abcdefghijklmnopqrstuvwxyz\n") == "CHAT WITH HER!\n", "26 unique letters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `IGNORE HIM!` | Minimum-size input |
| `aaaaaa` | `IGNORE HIM!` | Duplicate handling |
| `abcd` | `CHAT WITH HER!` | Even distinct count |
| `abc` | `IGNORE HIM!` | Odd distinct count |
| `abcdefghijklmnopqrstuvwxyz` | `CHAT WITH HER!` | Many unique characters |

## Edge Cases

Consider the case where every character is identical.

Input:

```
aaaaaa
```

The algorithm converts the string into:

```
{'a'}
```

The distinct count becomes `1`, which is odd, so the output is:

```
IGNORE HIM!
```

This case confirms that duplicates are removed correctly.

Now consider a string where every character is unique.

Input:

```
abcd
```

The set becomes:

```
{'a', 'b', 'c', 'd'}
```

The distinct count is `4`, which is even, so the output is:

```
CHAT WITH HER!
```

This verifies that the algorithm correctly handles the maximum possible number of unique characters in a small string.

Finally, consider the smallest valid input.

Input:

```
z
```

The set contains only one character:

```
{'z'}
```

The count is `1`, which is odd, so the output is:

```
IGNORE HIM!
```

This confirms there are no off-by-one mistakes when the string length is minimal.
