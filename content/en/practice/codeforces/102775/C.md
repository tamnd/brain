---
title: "CF 102775C - \u0422\u0430\u043a\u0438\u0435 \u0440\u0430\u0437\u043d\u044b\u0435 \u0441\u0442\u0440\u043e\u043a\u0438"
description: "We are given a single lowercase Latin string. A string is considered good if it never contains three consecutive vowels and never contains three consecutive consonants. If either of these situations appears anywhere in the string, the string is bad."
date: "2026-07-28T03:03:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102775
codeforces_index: "C"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 20), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102775
solve_time_s: 77
verified: true
draft: false
---

[CF 102775C - \u0422\u0430\u043a\u0438\u0435 \u0440\u0430\u0437\u043d\u044b\u0435 \u0441\u0442\u0440\u043e\u043a\u0438](https://codeforces.com/problemset/problem/102775/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single lowercase Latin string. A string is considered good if it never contains three consecutive vowels and never contains three consecutive consonants. If either of these situations appears anywhere in the string, the string is bad.

The task is simply to determine which category the input string belongs to. If a forbidden sequence exists, print `BAD`. Otherwise, print `GOOD`.

The string length is at most `100000`, which immediately suggests that every character should be processed only once. An algorithm that repeatedly rescans parts of the string, such as checking every substring independently, would perform far too many operations in the worst case. A linear scan, on the other hand, performs only about one hundred thousand character checks, which easily fits within the limits.

Several edge cases deserve attention.

A string shorter than three characters can never contain three consecutive vowels or consonants. For example:

```
ab
```

The correct output is:

```
GOOD
```

A careless implementation that blindly inspects triples without checking the length may access characters outside the string.

The sequence must be consecutive. For example:

```
ababa
```

The correct output is:

```
GOOD
```

Although there are many vowels and many consonants overall, they are constantly interrupted, so no run reaches length three.

Runs may appear at the very beginning or the very end of the string. For example:

```
aaab
```

The correct output is:

```
BAD
```

Similarly,

```
baaa
```

is also `BAD`. An implementation that only checks the middle of the string could miss these cases.

The letter `y` is a vowel in this problem. For example:

```
yyy
```

must produce:

```
BAD
```

Treating `y` as a consonant would produce the wrong answer.

## Approaches

The most direct solution is to examine every group of three consecutive characters. For each triple, determine whether all three are vowels or all three are consonants. If either condition holds, the answer is immediately `BAD`; otherwise continue until the end of the string.

This method is already correct because every forbidden pattern consists of exactly three consecutive letters. Any longer run, such as four consecutive vowels, necessarily contains a triple inside it.

A much less efficient brute-force idea would be to enumerate every substring and inspect whether it contains three consecutive vowels or consonants. A string of length `100000` has about `5 × 10^9` substrings, making such an approach completely impractical.

The key observation is that only the current consecutive run matters. Whenever the current character has the same type, vowel or consonant, as the previous one, the run length increases. Otherwise the run length resets to one. As soon as either run reaches three, we already know the answer is `BAD`, and no further processing is necessary.

This allows the string to be processed in one left-to-right pass using only a few variables.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store all vowels in a set containing `a`, `e`, `i`, `o`, `u`, and `y`. Membership checks in a set are constant time.
2. Initialize two counters, one for the current consecutive vowels and one for the current consecutive consonants. Both start at zero.
3. Scan the string from left to right.
4. If the current character is a vowel, increase the vowel counter by one and reset the consonant counter to zero. This reflects that any consonant run has been interrupted.
5. If the current character is a consonant, increase the consonant counter by one and reset the vowel counter to zero.
6. After updating the counters, check whether either counter has reached three. If so, print `BAD` immediately because a forbidden run has been found.
7. If the scan finishes without either counter reaching three, print `GOOD`.

### Why it works

At every position, the vowel counter equals the length of the current suffix consisting entirely of consecutive vowels, and the consonant counter equals the length of the current suffix consisting entirely of consecutive consonants. These values are maintained correctly because exactly one counter increases while the other is reset whenever a new character is processed. Since every forbidden pattern is exactly a run of at least three consecutive letters of the same type, reaching a counter value of three is both necessary and sufficient for declaring the string bad.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    vowels = set("aeiouy")

    vowel_run = 0
    consonant_run = 0

    for ch in s:
        if ch in vowels:
            vowel_run += 1
            consonant_run = 0
        else:
            consonant_run += 1
            vowel_run = 0

        if vowel_run >= 3 or consonant_run >= 3:
            print("BAD")
            return

    print("GOOD")

if __name__ == "__main__":
    solve()
```

The solution begins by creating a set of vowels so that each character can be classified in constant time.

The two counters represent the current run lengths. Exactly one of them grows on each iteration, while the other is reset because the current run has been interrupted.

The check for a run of length three happens immediately after updating the counters. This allows the program to terminate early as soon as the answer is known.

Using `strip()` removes the trailing newline from the input while leaving the actual string unchanged. No indexing is used, so there are no boundary issues when the string has fewer than three characters.

## Worked Examples

### Sample 1

Input:

```
good
```

| Character | Type | Vowel Run | Consonant Run | Decision |
| --- | --- | --- | --- | --- |
| g | Consonant | 0 | 1 | Continue |
| o | Vowel | 1 | 0 | Continue |
| o | Vowel | 2 | 0 | Continue |
| d | Consonant | 0 | 1 | Continue |

The scan finishes without either counter reaching three, so the answer is `GOOD`. This demonstrates that switching between vowels and consonants correctly resets the opposite counter.

### Sample 2

Input:

```
bad
```

| Character | Type | Vowel Run | Consonant Run | Decision |
| --- | --- | --- | --- | --- |
| b | Consonant | 0 | 1 | Continue |
| a | Vowel | 1 | 0 | Continue |
| d | Consonant | 0 | 1 | Continue |

Neither counter reaches three, so the answer is `GOOD`. This example confirms that isolated vowels and consonants do not accumulate across interruptions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed exactly once. |
| Space | O(1) | Only a fixed-size vowel set and two counters are stored. |

The algorithm performs a single pass over the string and uses constant additional memory. This easily satisfies the constraints even for strings of length `100000`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    s = input().strip()
    vowels = set("aeiouy")

    vowel_run = 0
    consonant_run = 0

    for ch in s:
        if ch in vowels:
            vowel_run += 1
            consonant_run = 0
        else:
            consonant_run += 1
            vowel_run = 0

        if vowel_run >= 3 or consonant_run >= 3:
            print("BAD")
            return

    print("GOOD")

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

# provided samples
assert run("good\n") == "GOOD", "sample 1"
assert run("bad\n") == "GOOD", "sample 2"
assert run("zashtsheeshtschayjushtsheekhsya\n") == "BAD", "sample 3"
assert run("dlinnosheee\n") == "BAD", "sample 4"

# custom cases
assert run("a\n") == "GOOD", "single character"
assert run("yyy\n") == "BAD", "y is a vowel"
assert run("bcdf\n") == "BAD", "four consecutive consonants"
assert run(("ab" * 50000) + "\n") == "GOOD", "maximum length alternating pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `GOOD` | Minimum possible length |
| `yyy` | `BAD` | Correct treatment of `y` as a vowel |
| `bcdf` | `BAD` | Detection of long consonant runs |
| `ab` repeated 50000 times | `GOOD` | Maximum input size with no forbidden run |

## Edge Cases

Consider the input:

```
ab
```

The algorithm processes `a`, then `b`. The counters become `(1, 0)` and then `(0, 1)`. Neither reaches three, so the output is `GOOD`. Since the algorithm never assumes the string has at least three characters, there are no boundary problems.

Now consider:

```
ababa
```

The counters alternate between one vowel and one consonant throughout the scan. Every type change resets the opposite counter, so neither run ever exceeds one. The output is correctly `GOOD`.

For the input:

```
aaab
```

The vowel counter evolves as `1`, `2`, `3`. The moment it reaches three, the algorithm immediately prints `BAD` without scanning the remaining characters. This correctly detects a forbidden prefix.

Finally, consider:

```
yyy
```

Since `y` belongs to the vowel set, the vowel counter becomes `1`, `2`, `3`, and the algorithm outputs `BAD`. This matches the problem's definition of vowels and avoids the common mistake of treating `y` as a consonant.
