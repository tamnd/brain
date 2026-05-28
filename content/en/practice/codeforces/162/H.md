---
title: "CF 162H - Alternating case"
description: "We are given a single string containing English letters in arbitrary capitalization. The task is to rewrite the string so that characters at odd positions become uppercase and characters at even positions become lowercase. The positions are counted starting from 1, not from 0."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "H"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 1800
weight: 162
solve_time_s: 191
verified: false
draft: false
---

[CF 162H - Alternating case](https://codeforces.com/problemset/problem/162/H)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 3m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single string containing English letters in arbitrary capitalization. The task is to rewrite the string so that characters at odd positions become uppercase and characters at even positions become lowercase. The positions are counted starting from 1, not from 0.

For example, if the input is `Codeforces`, the first character should become uppercase, the second lowercase, the third uppercase again, and so on. The resulting string is `CoDeFoRcEs`.

The constraints are tiny. The string length is at most 100 characters, so even inefficient approaches would run instantly. A linear scan over the string is more than enough. Since each character is processed independently, the natural solution is to iterate once through the string and decide the case based on the position parity.

The main source of mistakes is indexing. Python uses 0-based indices, while the problem describes positions starting from 1. A careless implementation may accidentally invert the pattern.

Consider the input:

```
abcde
```

The correct output is:

```
AbCdE
```

If we incorrectly treat index `0` as an even position in the problem statement sense, we would produce:

```
aBcDe
```

Another easy mistake is forgetting to normalize the original casing before applying the pattern. The input may already contain uppercase letters in arbitrary places.

For example:

```
aBcD
```

The correct output is:

```
AbCd
```

If we only modify characters at odd positions and leave the others unchanged, the result may stay incorrect.

Single-character strings are another boundary case:

```
z
```

The answer must be:

```
Z
```

The first position is always odd, so the character must always become uppercase.

## Approaches

The brute-force way is already straightforward here. We can iterate through the string character by character, check whether the current position is odd or even, and append either the uppercase or lowercase version of the character to the answer.

Since the maximum length is only 100, even repeatedly rebuilding strings would still be fast enough. A naive implementation using string concatenation inside a loop performs at most about 100 concatenations, which is negligible.

The cleaner and more scalable approach uses a list of characters and joins them at the end. This avoids repeated string reallocations and matches standard competitive programming style.

The key observation is that each character is independent from every other character. There is no interaction between positions, no dynamic programming state, and no need for preprocessing. The desired case depends only on whether the position number is odd or even.

That reduces the whole problem to a single linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Create an empty list that will store the transformed characters.
3. Iterate through the string using indices from `0` to `n - 1`.
4. For each character, determine whether its position in 1-based indexing is odd or even.

Since Python indices are 0-based, index `0` corresponds to position `1`, index `1` corresponds to position `2`, and so on.
5. If the index is even, convert the character to uppercase and append it to the answer list.

Even indices correspond to odd positions in the problem statement.
6. Otherwise, convert the character to lowercase and append it.
7. Join all characters from the list into a single string.
8. Print the result.

### Why it works

At every iteration, the algorithm enforces exactly the rule required by the statement. Index `i` corresponds to position `i + 1`.

If `i` is even, then `i + 1` is odd, so the character must be uppercase.

If `i` is odd, then `i + 1` is even, so the character must be lowercase.

Each character is transformed independently according to the correct positional rule, so after processing all positions, the resulting string satisfies the alternating-case requirement everywhere.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

ans = []

for i, ch in enumerate(s):
    if i % 2 == 0:
        ans.append(ch.upper())
    else:
        ans.append(ch.lower())

print("".join(ans))
```

The program starts by reading the input string and removing the trailing newline with `strip()`.

The answer is constructed using a list because appending to a list is efficient. After processing all characters, `"".join(ans)` builds the final string in one operation.

The critical implementation detail is the parity check. The problem uses 1-based positions, but Python indices start from 0. That means index `0` represents position `1`, which is odd and must be uppercase.

This is why the condition checks:

```
if i % 2 == 0
```

instead of checking for odd indices.

Using `upper()` and `lower()` directly guarantees correctness even when the input already contains mixed capitalization.

## Worked Examples

### Example 1

Input:

```
Codeforces
```

| Index `i` | Character | Position `i+1` | Action | Result so far |
| --- | --- | --- | --- | --- |
| 0 | C | 1 | uppercase | C |
| 1 | o | 2 | lowercase | Co |
| 2 | d | 3 | uppercase | CoD |
| 3 | e | 4 | lowercase | CoDe |
| 4 | f | 5 | uppercase | CoDeF |
| 5 | o | 6 | lowercase | CoDeFo |
| 6 | r | 7 | uppercase | CoDeFoR |
| 7 | c | 8 | lowercase | CoDeFoRc |
| 8 | e | 9 | uppercase | CoDeFoRcE |
| 9 | s | 10 | lowercase | CoDeFoRcEs |

Final output:

```
CoDeFoRcEs
```

This trace shows the alternating pattern clearly. Every odd position becomes uppercase, and every even position becomes lowercase.

### Example 2

Input:

```
aBcD
```

| Index `i` | Character | Position `i+1` | Action | Result so far |
| --- | --- | --- | --- | --- |
| 0 | a | 1 | uppercase | A |
| 1 | B | 2 | lowercase | Ab |
| 2 | c | 3 | uppercase | AbC |
| 3 | D | 4 | lowercase | AbCd |

Final output:

```
AbCd
```

This example demonstrates why we must explicitly call `upper()` and `lower()` instead of assuming the input already has the correct capitalization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(n) | The answer list stores the transformed string |

With `n ≤ 100`, the program runs instantly within the limits. The memory usage is also tiny because the algorithm only stores the resulting string.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()

    ans = []

    for i, ch in enumerate(s):
        if i % 2 == 0:
            ans.append(ch.upper())
        else:
            ans.append(ch.lower())

    print("".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("Codeforces\n") == "CoDeFoRcEs", "sample 1"

# minimum size
assert run("z\n") == "Z", "single character"

# already alternating
assert run("AbCdE\n") == "AbCdE", "already correct"

# all lowercase
assert run("abcdef\n") == "AbCdEf", "lowercase input"

# all uppercase
assert run("ABCDEF\n") == "AbCdEf", "uppercase input"

# off-by-one check
assert run("ab\n") == "Ab", "index parity correctness"

# maximum length
assert run(("a" * 100) + "\n") == ("Ab" * 50), "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `z` | `Z` | Minimum-length input |
| `AbCdE` | `AbCdE` | Already-correct pattern |
| `abcdef` | `AbCdEf` | Lowercase normalization |
| `ABCDEF` | `AbCdEf` | Uppercase normalization |
| `ab` | `Ab` | Correct handling of 1-based parity |
| `a * 100` | `AbAb...` | Maximum allowed length |

## Edge Cases

A single-character string is the smallest possible input:

```
z
```

The algorithm processes index `0`. Since `0` is even, the character becomes uppercase. The output is:

```
Z
```

This confirms that the first position is handled correctly.

Mixed capitalization can expose implementations that fail to normalize case properly.

Input:

```
aBcD
```

The algorithm does not trust the existing capitalization. At index `1`, the character `B` is converted to lowercase because it corresponds to position `2`. At index `2`, the character `c` becomes uppercase because it corresponds to position `3`.

The final result is:

```
AbCd
```

Off-by-one errors appear easily when converting between 0-based and 1-based indexing.

Input:

```
ab
```

Index `0` maps to position `1`, so `a` becomes uppercase.

Index `1` maps to position `2`, so `b` becomes lowercase.

The output is:

```
Ab
```

An incorrect parity condition would instead produce `aB`, which violates the problem statement.
