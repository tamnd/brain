---
title: "CF 49A - Sleuth"
description: "We are given a single sentence that represents a question. The sentence always ends with a question mark, but the answer is determined by the last alphabetic letter before that question mark. If that final letter is a vowel, the correct response is \"YES\"."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 49
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 46 (Div. 2)"
rating: 800
weight: 49
solve_time_s: 81
verified: true
draft: false
---

[CF 49A - Sleuth](https://codeforces.com/problemset/problem/49/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single sentence that represents a question. The sentence always ends with a question mark, but the answer is determined by the last alphabetic letter before that question mark. If that final letter is a vowel, the correct response is `"YES"`. Otherwise, the response is `"NO"`.

The vowels in this problem are slightly unusual because `Y` is also treated as a vowel. Both uppercase and lowercase letters may appear, so the comparison must be case-insensitive.

The input length is at most 100 characters, which is tiny. Even a full scan of the string multiple times would easily fit within the limits. The problem is purely about correctly identifying the last letter and checking whether it belongs to the vowel set.

The tricky part is that the last character is always `?`, but the answer depends on the last letter, not the last character. Spaces also do not count. A careless implementation that checks `s[-1]` would always inspect `?` and fail immediately.

Consider this input:

```
Is it a melon?
```

The last letter is `n`, which is a consonant, so the correct answer is:

```
NO
```

Another easy mistake is forgetting case conversion. For example:

```
A?
```

The last letter is uppercase `A`, which is still a vowel. Without converting to lowercase or handling both cases explicitly, the program could incorrectly print `"NO"`.

Trailing spaces are not present according to the statement, but spaces inside the sentence matter because the final letter may be far from the end. For example:

```
Is this a UFO ?
```

The last meaningful letter is `O`, not the space before `?`.

## Approaches

The most direct approach is to scan backward from the end of the string until we encounter a letter. Once we find it, we check whether it belongs to the vowel set `{a, e, i, o, u, y}`. If it does, we print `"YES"`, otherwise `"NO"`.

A brute-force interpretation would be to examine every character in the string and remember the last alphabetic one seen so far. Since the string length is at most 100, this already runs comfortably fast. The worst case performs only 100 character checks.

We can make the implementation slightly cleaner by exploiting the structure of the input. The string always ends with `?`, and there is guaranteed to be at least one letter. Because of that, scanning backward immediately finds the relevant character without storing anything extra.

The key observation is that only one character matters, the final letter in the sentence. Everything else is irrelevant. Once we isolate that letter, the problem reduces to a simple membership test in a vowel set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the entire input line as a string.
2. Create a set containing all vowels in lowercase:

```
{a, e, i, o, u, y}
```
3. Traverse the string from right to left.
4. Ignore any character that is not an alphabetic letter.

This skips the final `?` and any spaces near the end.
5. When the first letter is found, convert it to lowercase.
6. Check whether this lowercase letter belongs to the vowel set.

If it does, print `"YES"`. Otherwise, print `"NO"`.
7. Stop immediately after processing the first valid letter because only the last letter matters.

### Why it works

The backward scan guarantees that the first alphabetic character we encounter is exactly the last letter of the question. The rules of the game depend only on that letter. Converting to lowercase removes any distinction between uppercase and lowercase input, so membership in the vowel set correctly determines the answer in every case.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

vowels = set("aeiouy")

for ch in reversed(s):
    if ch.isalpha():
        if ch.lower() in vowels:
            print("YES")
        else:
            print("NO")
        break
```

The program begins by reading the entire question as a string. Using `strip()` removes the trailing newline introduced by input reading.

The vowel set is stored in lowercase form. This allows us to normalize each candidate letter with `lower()` before checking membership.

The loop iterates through the string in reverse order. This is the cleanest way to locate the final meaningful letter because the input always ends with `?`.

The `isalpha()` check is essential. Without it, the program would inspect punctuation or spaces instead of letters. As soon as a valid letter is found, the program determines whether it is a vowel and immediately prints the answer.

The `break` statement matters because only the last letter should influence the result. Continuing the scan could accidentally overwrite the correct decision.

## Worked Examples

### Example 1

Input:

```
Is it a melon?
```

| Current Character | Is Letter | Lowercase | Vowel? | Action |
| --- | --- | --- | --- | --- |
| `?` | No | - | - | Skip |
| `n` | Yes | `n` | No | Print `NO` |

The scan skips the question mark and immediately reaches `n`. Since `n` is not in the vowel set, the answer is `"NO"`.

### Example 2

Input:

```
Are YOU happy?
```

| Current Character | Is Letter | Lowercase | Vowel? | Action |
| --- | --- | --- | --- | --- |
| `?` | No | - | - | Skip |
| `y` | Yes | `y` | Yes | Print `YES` |

This example demonstrates two details. First, the algorithm correctly ignores `?`. Second, `y` is treated as a vowel in this problem, so the answer becomes `"YES"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | In the worst case we scan the whole string once |
| Space | O(1) | Only a small vowel set and a few variables are used |

Since the input length never exceeds 100 characters, even a linear scan is effectively instantaneous. The memory usage is constant and far below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s = input().strip()

    vowels = set("aeiouy")

    for ch in reversed(s):
        if ch.isalpha():
            if ch.lower() in vowels:
                print("YES")
            else:
                print("NO")
            break

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
assert run("Is it a melon?\n") == "NO\n", "sample 1"

# custom cases
assert run("A?\n") == "YES\n", "single uppercase vowel"
assert run("b?\n") == "NO\n", "single lowercase consonant"
assert run("Why?\n") == "YES\n", "y treated as vowel"
assert run("Is this a UFO ?\n") == "YES\n", "space before question mark"
assert run(("a" * 99) + "?\n") == "YES\n", "maximum length style case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A?` | `YES` | Uppercase vowel handling |
| `b?` | `NO` | Single consonant case |
| `Why?` | `YES` | `y` counts as vowel |
| `Is this a UFO ?` | `YES` | Ignoring spaces before `?` |
| `aaaa...a?` | `YES` | Long input near maximum size |

## Edge Cases

Consider the input:

```
A?
```

The algorithm scans from the back. It skips `?`, reaches `A`, converts it to lowercase `a`, and finds it in the vowel set. The output becomes:

```
YES
```

This confirms that uppercase letters are handled correctly.

Now consider:

```
Is this a UFO ?
```

The reverse traversal proceeds as follows:

```
? -> skip
(space) -> skip
O -> valid letter
```

After converting `O` to lowercase `o`, the algorithm identifies it as a vowel and prints:

```
YES
```

This case confirms that spaces near the end do not interfere with locating the final letter.

Finally, examine:

```
Why?
```

The last letter is `y`. Some implementations forget that `y` is included among vowels in this problem. The algorithm explicitly stores `y` inside the vowel set, so it correctly prints:

```
YES
```
