---
title: "CF 1111A - Superhero Transformation"
description: "We are given two lowercase strings representing superhero names. A transformation is allowed if every vowel can be changed into any other vowel, and every consonant can be changed into any other consonant. The actual letters do not matter."
date: "2026-06-12T05:02:15+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1111
codeforces_index: "A"
codeforces_contest_name: "CodeCraft-19 and Codeforces Round 537 (Div. 2)"
rating: 1000
weight: 1111
solve_time_s: 323
verified: false
draft: false
---

[CF 1111A - Superhero Transformation](https://codeforces.com/problemset/problem/1111/A)

**Rating:** 1000  
**Tags:** implementation, strings  
**Solve time:** 5m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two lowercase strings representing superhero names. A transformation is allowed if every vowel can be changed into any other vowel, and every consonant can be changed into any other consonant.

The actual letters do not matter. What matters is whether each position contains a vowel or a consonant. For example, `'a'` can become `'u'` because both are vowels, and `'b'` can become `'z'` because both are consonants. A vowel can never become a consonant, and a consonant can never become a vowel.

The task is to determine whether the first name can be transformed into the second using these rules.

The strings have length at most 1000, which is very small. Even an algorithm that scans the strings several times would be easily fast enough. The only thing that matters is implementing the transformation condition correctly.

A crucial observation is that changing characters never changes the string length. Every operation replaces one character with another character of the same category. If the two names have different lengths, the answer is immediately "No".

There are a few easy-to-miss edge cases.

Consider:

```
a
bb
```

The correct answer is:

```
No
```

A careless solution that only compares vowel/consonant counts might incorrectly accept it. Length equality is mandatory.

Consider:

```
ab
cd
```

The correct answer is:

```
No
```

The first position is vowel versus consonant. Even though both strings contain one vowel and one consonant overall, positions matter.

Consider:

```
ae
io
```

The correct answer is:

```
Yes
```

The letters differ, but every position is vowel versus vowel.

Consider:

```
code
java
```

The correct answer is:

```
No
```

At some positions one string contains a consonant while the other contains a vowel.

## Approaches

A brute-force way to think about the problem is to simulate whether each character could be changed into the corresponding character of the other string. For every position, we could ask whether the source and target characters belong to the same category. If any position violates this rule, transformation is impossible.

Since each string has at most 1000 characters, checking every position directly requires only 1000 comparisons. That is already fast enough.

The key insight is that the actual identity of a letter never matters. The transformation rules allow any vowel to become any vowel and any consonant to become any consonant. This means every character can be reduced to one bit of information: vowel or consonant.

After that observation, the problem becomes very simple. First verify that the lengths are equal. Then scan both strings position by position. At each index, check whether both characters are vowels or both are consonants. If not, the transformation is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

In this problem, the natural brute-force approach is already optimal because the input size is tiny and every character must be examined at least once.

## Algorithm Walkthrough

1. Read the two strings.
2. If their lengths are different, output `"No"` and stop.

A transformation only replaces characters. It never inserts or removes characters.
3. Create a set containing the vowels `{a, e, i, o, u}`.
4. Iterate through all positions of the strings.
5. For each position, determine whether the character from the first string is a vowel and whether the character from the second string is a vowel.
6. If one character is a vowel and the other is a consonant, output `"No"` and stop.

Such a position can never be transformed under the allowed operations.
7. If the entire scan finishes without finding a mismatch, output `"Yes"`.

### Why it works

A transformation is valid exactly when every position can be transformed independently.

At any position there are only two possibilities: vowel or consonant. A vowel may become any vowel, and a consonant may become any consonant. Thus a position is transformable if and only if both characters belong to the same category.

If the strings have different lengths, no sequence of replacements can make them equal. If the lengths are equal and every position has matching categories, we can choose the appropriate replacement at each position and obtain the target string. These conditions are both necessary and sufficient, so the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
t = input().strip()

if len(s) != len(t):
    print("No")
    sys.exit()

vowels = set("aeiou")

for a, b in zip(s, t):
    if (a in vowels) != (b in vowels):
        print("No")
        break
else:
    print("Yes")
```

The first check handles the only global restriction: the lengths must match.

The `vowels` set allows constant-time membership checks. For each pair of characters, the expression

```
(a in vowels) != (b in vowels)
```

is true exactly when one character is a vowel and the other is a consonant. As soon as such a position is found, the answer is known to be `"No"`.

The `for-else` construct is convenient here. The `else` block executes only if the loop finishes without encountering a `break`, meaning every position satisfied the required condition.

## Worked Examples

### Example 1

Input:

```
a
u
```

| Position | s[i] | t[i] | s[i] vowel? | t[i] vowel? | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | a | u | Yes | Yes | Valid |

No mismatches are found. Every position matches by category, so the answer is:

```
Yes
```

This example demonstrates that the exact vowel does not matter. Any vowel can become any other vowel.

### Example 2

Input:

```
ab
cd
```

| Position | s[i] | t[i] | s[i] vowel? | t[i] vowel? | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | a | c | Yes | No | Invalid |

The first position already contains a vowel versus a consonant. The algorithm immediately stops and prints:

```
No
```

This example shows that matching counts of vowels and consonants is irrelevant. Categories must match at every position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is checked once |
| Space | O(1) | Only a small vowel set and a few variables are stored |

The maximum length is only 1000, so a single linear scan is easily within the time limit. Memory usage is constant and negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    s = input().strip()
    t = input().strip()

    if len(s) != len(t):
        print("No")
        return

    vowels = set("aeiou")

    for a, b in zip(s, t):
        if (a in vowels) != (b in vowels):
            print("No")
            return

    print("Yes")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("a\nu\n") == "Yes", "sample 1"

# custom cases
assert run("a\nb\n") == "No", "vowel versus consonant"
assert run("ab\ncd\n") == "No", "position mismatch"
assert run("aeiou\nuoiea\n") == "Yes", "all vowels"
assert run("b\nz\n") == "Yes", "single consonants"
assert run(("a" * 1000) + "\n" + ("e" * 1000) + "\n") == "Yes", "maximum length"
assert run("abc\nab\n") == "No", "different lengths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / b` | `No` | Vowel cannot become consonant |
| `ab / cd` | `No` | Position-wise matching is required |
| `aeiou / uoiea` | `Yes` | Any vowel can become any other vowel |
| `b / z` | `Yes` | Any consonant can become any other consonant |
| Length 1000 vowel strings | `Yes` | Maximum input size |
| `abc / ab` | `No` | Length mismatch |

## Edge Cases

Consider the input:

```
a
bb
```

The algorithm first compares lengths. Since `1 != 2`, it immediately prints:

```
No
```

No character inspection is necessary. This handles the fact that transformations never change string length.

Consider the input:

```
ab
ba
```

At position 0, `'a'` is a vowel while `'b'` is a consonant. The algorithm detects a category mismatch and prints:

```
No
```

This shows why checking only total vowel counts would be incorrect. Positions matter.

Consider the input:

```
ae
io
```

Both strings have length 2.

At position 0, vowel matches vowel.

At position 1, vowel matches vowel.

The scan completes successfully, so the algorithm prints:

```
Yes
```

This confirms that the exact letters are irrelevant. Only the vowel/consonant classification matters.

Consider the input:

```
bcdf
wxyz
```

Every position contains consonant versus consonant. The algorithm never finds a mismatch and prints:

```
Yes
```

This verifies the analogous rule for consonants. Any consonant may be replaced by any other consonant.
