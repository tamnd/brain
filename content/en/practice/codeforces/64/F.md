---
title: "CF 64F - Domain"
description: "We need to decide whether a given string can be interpreted as a valid domain name under a simplified set of rules. The string may only contain lowercase English letters, digits, and dots. Dots separate the string into segments."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "expression-parsing"]
categories: ["algorithms"]
codeforces_contest: 64
codeforces_index: "F"
codeforces_contest_name: "Unknown Language Round 1"
rating: 2000
weight: 64
solve_time_s: 97
verified: true
draft: false
---

[CF 64F - Domain](https://codeforces.com/problemset/problem/64/F)

**Rating:** 2000  
**Tags:** *special, expression parsing  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to decide whether a given string can be interpreted as a valid domain name under a simplified set of rules.

The string may only contain lowercase English letters, digits, and dots. Dots separate the string into segments. The string cannot start with a dot or end with a dot, and two dots cannot appear consecutively. After splitting by dots, the final segment must have length exactly 2 or 3.

The input length is at most 100, which is tiny. Even an inefficient solution would run comfortably within the time limit. The real challenge is not optimization but carefully implementing every rule without missing corner cases.

A common mistake is checking only the allowed characters while forgetting structural constraints involving dots. For example:

Input:

```
abc..com
```

Correct output:

```
NO
```

The string uses only valid characters, but consecutive dots create an empty segment, which is forbidden.

Another easy bug is forgetting that the domain cannot start or end with a dot.

Input:

```
.google
```

Correct output:

```
NO
```

A careless split-based solution might produce `["", "google"]` and accidentally accept it.

The last segment length restriction also causes subtle failures.

Input:

```
abc.c
```

Correct output:

```
NO
```

The final segment has length 1, while only lengths 2 and 3 are allowed.

Similarly:

Input:

```
abc.comm
```

Correct output:

```
NO
```

The last segment length is 4.

Another trap is uppercase letters. The statement allows only lowercase letters.

Input:

```
Codeforces.com
```

Correct output:

```
NO
```

A solution using `isalnum()` directly would incorrectly accept uppercase characters.

## Approaches

The most direct brute-force idea is to simulate the definition exactly. We scan the string character by character and verify every rule independently.

We can first check that every character belongs to the allowed set. Then we verify that the string neither starts nor ends with a dot. Next we check that no adjacent pair of characters contains two dots. Finally we split the string by dots and inspect the last segment length.

This already runs in linear time, because each pass touches the string once. With length at most 100, even repeatedly scanning the string is negligible.

Another possible brute-force interpretation would be generating all possible ways to split the string into domain segments and checking validity manually. That approach becomes unnecessarily complicated and grows exponentially with the number of positions. Even though the constraints are small enough that it could still pass, the problem structure gives a much cleaner route.

The key observation is that every rule is local. Allowed characters depend on individual positions, consecutive-dot validity depends only on neighboring characters, and the suffix condition depends only on the final segment. No global search or parsing is required. A single left-to-right scan combined with one final suffix check fully determines validity.

Because of that, the optimal solution is simply a direct validator.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Exhaustive splitting/search | O(2^n) | O(n) | Unnecessarily slow |
| Direct validation scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Check whether the string starts or ends with a dot.

A valid domain cannot have empty segments at the beginning or end.
3. Scan every character in the string.

If a character is not a lowercase letter, digit, or dot, immediately reject the string.
4. During the same scan, check adjacent characters.

If two consecutive characters are both dots, reject the string because this creates an empty segment.
5. Split the string using dots as separators.
6. Take the final segment and check its length.

The length must be either 2 or 3.
7. If every check passes, print `"YES"`. Otherwise print `"NO"`.

### Why it works

The algorithm directly encodes every condition from the definition of a valid domain. The character scan guarantees that no forbidden symbols appear. The boundary checks prevent empty segments at the start or end. The consecutive-dot check prevents empty segments in the middle. Splitting by dots exposes the final segment so its length constraint can be verified exactly. Since every rule is checked explicitly and rejection happens immediately when a rule fails, the algorithm accepts exactly the valid domain names and rejects all invalid ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    if s[0] == '.' or s[-1] == '.':
        print("NO")
        return

    for i, ch in enumerate(s):
        valid = (
            ('a' <= ch <= 'z') or
            ('0' <= ch <= '9') or
            ch == '.'
        )

        if not valid:
            print("NO")
            return

        if i > 0 and s[i] == '.' and s[i - 1] == '.':
            print("NO")
            return

    parts = s.split('.')
    last_len = len(parts[-1])

    if last_len == 2 or last_len == 3:
        print("YES")
    else:
        print("NO")

solve()
```

The first condition handles boundary dots immediately. This avoids accidental acceptance of empty leading or trailing segments after splitting.

The main loop combines two checks into one pass. First it validates characters using explicit range comparisons instead of helpers like `isalnum()`. That matters because `isalnum()` would incorrectly allow uppercase letters.

The adjacency check starts only when `i > 0`, preventing an out-of-bounds access on the first character.

After validation, the string is split by dots. Since we already rejected consecutive dots and boundary dots, every segment is guaranteed to be non-empty. The only remaining condition is the size of the last segment.

The implementation never uses extra data structures beyond the split result, and every operation is linear in the string length.

## Worked Examples

### Example 1

Input:

```
codeforces.com
```

| Step | Current State | Result |
| --- | --- | --- |
| Boundary check | first=`c`, last=`m` | valid |
| Character scan | all chars are lowercase/dot | valid |
| Consecutive dots | none found | valid |
| Split | `["codeforces", "com"]` | valid |
| Last segment length | `len("com") = 3` | valid |

Output:

```
YES
```

This example demonstrates the standard successful path. Every structural condition holds, and the top-level domain length is acceptable.

### Example 2

Input:

```
abc..com
```

| Step | Current State | Result |
| --- | --- | --- |
| Boundary check | first=`a`, last=`m` | valid |
| Character scan | all chars allowed | valid |
| Consecutive dots | found `".."` at indices 3 and 4 | invalid |

Output:

```
NO
```

This trace shows why checking only allowed characters is insufficient. The structure created by dots also matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The string is scanned a constant number of times |
| Space | O(n) | The split operation stores the segments |

With `n ≤ 100`, the runtime is tiny. Even a much slower solution would fit comfortably within the limits, but the linear validator is both simpler and cleaner.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        s = input().strip()

        if s[0] == '.' or s[-1] == '.':
            return "NO"

        for i, ch in enumerate(s):
            valid = (
                ('a' <= ch <= 'z') or
                ('0' <= ch <= '9') or
                ch == '.'
            )

            if not valid:
                return "NO"

            if i > 0 and s[i] == '.' and s[i - 1] == '.':
                return "NO"

        parts = s.split('.')
        last_len = len(parts[-1])

        if last_len == 2 or last_len == 3:
            return "YES"

        return "NO"

    return solve()

# provided sample
assert run("codeforces.com\n") == "YES", "sample 1"

# custom cases
assert run("a.a\n") == "NO", "last segment too short"

assert run(".abc.com\n") == "NO", "leading dot"

assert run("abc..com\n") == "NO", "consecutive dots"

assert run("abc.comm\n") == "NO", "last segment too long"

assert run("a" * 97 + ".ru\n") == "YES", "maximum length style case"

assert run("Codeforces.com\n") == "NO", "uppercase letters forbidden"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a.a` | `NO` | Last segment length 1 |
| `.abc.com` | `NO` | Leading dot rejection |
| `abc..com` | `NO` | Consecutive dots rejection |
| `abc.comm` | `NO` | Last segment length greater than 3 |
| `aaaa...aaa.ru` | `YES` | Large valid input near maximum length |
| `Codeforces.com` | `NO` | Uppercase letters are invalid |

## Edge Cases

Consider the input:

```
.google
```

The algorithm checks the first character immediately and sees that it is a dot. It rejects the string before any splitting occurs. This prevents accidental acceptance of an empty first segment.

Now consider:

```
abc..com
```

During the scan, when the algorithm reaches the second dot, it compares it with the previous character and detects `".."`. The string is rejected instantly. No later processing can override this failure.

For the input:

```
abc.c
```

All character and dot-structure checks succeed. After splitting, the final segment is `"c"`, whose length is 1. Since only lengths 2 and 3 are accepted, the algorithm prints `"NO"`.

Finally, consider:

```
Codeforces.com
```

When scanning the first character `'C'`, the lowercase range check fails because `'C'` is outside `'a'` to `'z'`. The algorithm rejects the string immediately, correctly enforcing the lowercase-only rule.
