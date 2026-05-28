---
title: "CF 43B - Letter"
description: "We are given two strings. The first string is the newspaper headline, and the second string is the anonymous letter Vasya wants to build from it."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 43
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 42 (Div. 2)"
rating: 1100
weight: 43
solve_time_s: 91
verified: true
draft: false
---
[CF 43B - Letter](https://codeforces.com/problemset/problem/43/B)

**Rating:** 1100  
**Tags:** implementation, strings  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings. The first string is the newspaper headline, and the second string is the anonymous letter Vasya wants to build from it.

Every non-space character from the headline can be used at most once. Spaces are special, they do not consume anything. If the letter text contains spaces, Vasya can simply leave gaps between characters without needing actual space characters from the headline.

The task is to determine whether every required letter in the target text can be supplied by the headline with enough frequency. Uppercase and lowercase letters are treated as different characters, so `'A'` and `'a'` are not interchangeable.

The strings are short, at most 200 characters long. Even an inefficient solution would fit comfortably inside the limits, because a quadratic scan over 200 characters performs only about 40,000 operations. This means the problem is not about advanced optimization, but about handling character counts correctly.

The tricky part is that spaces must be ignored completely. A careless implementation might count spaces as normal characters and incorrectly reject valid answers.

Consider this input:

```
abc
a c
```

The correct answer is:

```
YES
```

The headline does not contain a space, but spaces do not need to be cut out, so the letter is still possible.

Case sensitivity is another common source of bugs.

```
Abc
abc
```

The correct answer is:

```
NO
```

The headline contains uppercase `A`, but the letter requires lowercase `a`.

Another subtle case appears when a character exists in the headline, but not enough times.

```
hello
helloo
```

The correct answer is:

```
NO
```

A solution that only checks whether each character appears at least once would fail here because the target needs two `'o'` characters.

## Approaches

The most direct brute-force method is to process the target string character by character. For every non-space character in the letter, scan through the headline until a matching unused character is found. Once used, mark that character so it cannot be reused later.

This works because each letter in the target explicitly consumes one matching letter from the source. The problem is that every lookup may scan almost the entire headline. If both strings have length `n`, this leads to `O(n^2)` time complexity.

With `n ≤ 200`, even this approach passes easily. In the worst case, we do about `200 × 200 = 40,000` comparisons. Still, the method is clumsy because it spends time repeatedly searching for characters we could count once.

The better observation is that only frequencies matter. The order of letters in the headline is irrelevant. If the letter needs three `'a'` characters, the headline must contain at least three `'a'` characters somewhere.

That turns the problem into a counting task. We count how many times each non-space character appears in the headline, then walk through the target text and consume one occurrence for every required character. If at any point a character is unavailable, the answer is immediately `"NO"`.

This reduces the logic to linear time because every character is processed once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the headline string and the target letter string.
2. Create a frequency map for characters in the headline.

We only count non-space characters because spaces are free and do not need to be cut from the newspaper.
3. Traverse the target letter one character at a time.
4. If the current character is a space, skip it.

Spaces never consume anything from the headline.
5. For every non-space character, check whether its frequency in the map is positive.

If the count is zero, the headline does not contain enough copies of that character, so print `"NO"` and stop immediately.
6. Otherwise, decrease the frequency of that character by one.

This models using one cut-out letter from the headline.
7. If the entire target string is processed successfully, print `"YES"`.

### Why it works

The algorithm maintains the invariant that the frequency map always represents the remaining unused letters available from the headline.

Whenever the target needs a character, we consume one matching occurrence. If a required character is unavailable, then no arrangement could possibly construct the target because every usable character has already been accounted for exactly once.

Since spaces are ignored and every other character is matched against available supply, the algorithm accepts exactly the constructible letters and rejects all impossible ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

headline = input().rstrip('\n')
letter = input().rstrip('\n')

freq = {}

for ch in headline:
    if ch != ' ':
        freq[ch] = freq.get(ch, 0) + 1

for ch in letter:
    if ch == ' ':
        continue

    if freq.get(ch, 0) == 0:
        print("NO")
        break

    freq[ch] -= 1
else:
    print("YES")
```

The first part reads both lines exactly as entered. Using `rstrip('\n')` is important because we want to remove only the trailing newline added by input, not internal or leading spaces that belong to the string.

The dictionary `freq` stores how many unused copies of each character remain in the headline. Spaces are skipped because they are irrelevant to construction.

The second loop processes the target letter. Whenever a space appears, the algorithm ignores it immediately. For normal characters, the dictionary lookup checks whether at least one unused copy still exists.

The `for ... else` structure is convenient here. The `else` block executes only if the loop finishes without hitting `break`. That means the answer is `"YES"` exactly when no character shortage was detected.

A subtle implementation detail is the use of `freq.get(ch, 0)`. Without the default value `0`, querying a character that never appeared in the headline would raise an error.

## Worked Examples

### Example 1

Input:

```
Instead of dogging Your footsteps it disappears but you dont notice anything
where is your dog
```

Trace:

| Current Character | Available Before | Available After | Result |
| --- | --- | --- | --- |
| w | 0 | 0 | Fail |
| remaining chars | not processed | not processed | NO |

The algorithm fails immediately because lowercase `'w'` does not appear in the headline. The headline contains uppercase letters and many lowercase letters, but not lowercase `'w'`.

This example demonstrates that the algorithm stops as soon as impossibility is detected, instead of scanning unnecessarily.

### Example 2

Input:

```
hello world
hello
```

Trace:

| Current Character | Available Before | Available After | Result |
| --- | --- | --- | --- |
| h | 1 | 0 | continue |
| e | 1 | 0 | continue |
| l | 3 | 2 | continue |
| l | 2 | 1 | continue |
| o | 2 | 1 | continue |

Final output:

```
YES
```

This trace shows how repeated characters are handled correctly. The count for `'l'` decreases twice because the target requires two copies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each string is scanned once |
| Space | O(n) | The frequency map stores character counts |

The input length is at most 200 characters, so the solution runs instantly within the limits. Even Python dictionary operations are effectively constant time for this scale.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    headline = input().rstrip('\n')
    letter = input().rstrip('\n')

    freq = {}

    for ch in headline:
        if ch != ' ':
            freq[ch] = freq.get(ch, 0) + 1

    for ch in letter:
        if ch == ' ':
            continue

        if freq.get(ch, 0) == 0:
            print("NO")
            return

        freq[ch] -= 1

    print("YES")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
    "Instead of dogging Your footsteps it disappears but you dont notice anything\n"
    "where is your dog\n"
) == "NO\n", "sample 1"

# minimum-size input
assert run(
    "a\n"
    "a\n"
) == "YES\n", "single character"

# spaces should not matter
assert run(
    "abc\n"
    "a c\n"
) == "YES\n", "spaces ignored"

# case sensitivity
assert run(
    "Abc\n"
    "abc\n"
) == "NO\n", "uppercase and lowercase differ"

# insufficient frequency
assert run(
    "hello\n"
    "helloo\n"
) == "NO\n", "repeated character shortage"

# large repeated input
assert run(
    "a" * 200 + "\n" +
    "a" * 200 + "\n"
) == "YES\n", "maximum equal strings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a` | YES | Smallest valid case |
| `abc / a c` | YES | Spaces do not consume characters |
| `Abc / abc` | NO | Case sensitivity |
| `hello / helloo` | NO | Frequency counting |
| 200 `'a'` characters | YES | Maximum-length handling |

## Edge Cases

Consider the case where the target contains spaces but the headline does not.

Input:

```
abc
a b c
```

The algorithm builds this frequency map:

```
a:1, b:1, c:1
```

While scanning the target, spaces are skipped entirely. Only `'a'`, `'b'`, and `'c'` consume counts. All counts remain valid, so the output becomes:

```
YES
```

This confirms that spaces are correctly ignored.

Now consider case sensitivity.

Input:

```
A
a
```

The frequency map contains only uppercase `'A'`.

When the algorithm checks lowercase `'a'`, `freq.get('a', 0)` returns `0`. The algorithm immediately prints:

```
NO
```

This demonstrates that uppercase and lowercase letters are treated as different symbols.

Finally, consider repeated-character shortages.

Input:

```
banana
bananaa
```

Initial frequencies:

| Character | Count |
| --- | --- |
| b | 1 |
| a | 3 |
| n | 2 |

The target requires four `'a'` characters. After consuming the first three, the remaining count becomes zero. When the algorithm reaches the fourth `'a'`, it detects the shortage and prints:

```
NO
```

This verifies that the algorithm tracks exact frequencies rather than simple existence.
