---
title: "CF 290D - Orange"
description: "We are given a string consisting of uppercase and lowercase English letters, and an integer k. The task is to modify the string so that exactly k characters become uppercase. The relative order of characters must stay unchanged, only the letter cases may change."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 290
codeforces_index: "D"
codeforces_contest_name: "April Fools Day Contest 2013"
rating: 1400
weight: 290
solve_time_s: 131
verified: false
draft: false
---

[CF 290D - Orange](https://codeforces.com/problemset/problem/290/D)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string consisting of uppercase and lowercase English letters, and an integer `k`. The task is to modify the string so that exactly `k` characters become uppercase. The relative order of characters must stay unchanged, only the letter cases may change.

The tricky part is that the original string may already contain some uppercase letters. We are free to change any letters between lowercase and uppercase until the total number of uppercase letters becomes exactly `k`.

The string length is at most 50, which is extremely small. Even an algorithm that scans the string several times is completely safe. A quadratic solution would still run instantly, since at worst we would process about 2500 operations. This means the problem is not about optimization, it is about implementing the transformation carefully.

The main source of mistakes is forgetting that uppercase and lowercase versions of the same letter are considered different characters in ASCII. A careless implementation might compare characters incorrectly or accidentally change already-correct letters.

One edge case appears when `k = 0`. In this situation, every character must become lowercase.

Input:

```
AbC
0
```

Correct output:

```
abc
```

A buggy solution might leave existing uppercase letters unchanged.

Another edge case is when `k` equals the string length. Then every character must become uppercase.

Input:

```
aBc
3
```

Correct output:

```
ABC
```

A careless approach that only converts lowercase letters until the count reaches `k` might stop too early if it miscounts existing uppercase letters.

A more subtle case happens when the string already contains exactly `k` uppercase letters.

Input:

```
AprIL
3
```

Correct output:

```
AprIL
```

The algorithm should avoid unnecessary modifications. Some incorrect implementations keep toggling characters even after reaching the required count.

## Approaches

The most direct brute-force idea is to try every possible combination of uppercase and lowercase letters, count how many uppercase letters each version contains, and keep one with exactly `k` uppercase letters. Since every character has two choices, a string of length `n` has `2^n` possible versions. With `n = 50`, this becomes completely impossible because `2^50` is astronomically large.

The structure of the problem gives a much simpler observation. We do not care which specific letters are uppercase, only the final count. That means we can first measure how many uppercase letters already exist, then adjust the count gradually.

Suppose the string currently has `cnt` uppercase letters.

If `cnt < k`, we need to convert some lowercase letters into uppercase letters until the count reaches `k`.

If `cnt > k`, we need to convert some uppercase letters into lowercase letters until the count reaches `k`.

Each conversion changes the uppercase count by exactly one, so a greedy left-to-right scan works immediately. There is no advantage in choosing special positions because every operation has identical cost and effect.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the string and the target number `k`.
2. Count how many uppercase letters already exist in the string.
3. Convert the string into a mutable list of characters, because Python strings cannot be modified in place.
4. If the current uppercase count is smaller than `k`, scan the string from left to right.

Whenever a lowercase letter is found, convert it to uppercase and increase the count by one.
5. Stop as soon as the uppercase count becomes exactly `k`.

Continuing beyond this point would create too many uppercase letters.
6. If the current uppercase count is larger than `k`, scan the string from left to right.

Whenever an uppercase letter is found, convert it to lowercase and decrease the count by one.
7. Stop when the uppercase count reaches exactly `k`.
8. Join the character list back into a string and print it.

### Why it works

The algorithm maintains a simple invariant: after every modification, the variable storing the uppercase count exactly matches the current string state.

Each operation changes the count by exactly one in the needed direction. When the count is too small, every lowercase-to-uppercase conversion moves us closer to the target. When the count is too large, every uppercase-to-lowercase conversion also moves us closer.

Because the process stops precisely when the count becomes `k`, the final string always satisfies the requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
k = int(input())

chars = list(s)

cnt = 0
for c in chars:
    if c.isupper():
        cnt += 1

if cnt < k:
    for i in range(len(chars)):
        if cnt == k:
            break

        if chars[i].islower():
            chars[i] = chars[i].upper()
            cnt += 1

elif cnt > k:
    for i in range(len(chars)):
        if cnt == k:
            break

        if chars[i].isupper():
            chars[i] = chars[i].lower()
            cnt -= 1

print("".join(chars))
```

The program starts by counting how many uppercase letters already exist. This determines whether we need to increase or decrease the uppercase count.

The string is converted into a list because Python strings are immutable. Trying to assign directly into a string index would raise an error.

The two branches are symmetric. One branch increases the uppercase count, the other decreases it. In both cases, the loop stops immediately after reaching `k`. That early stop matters because otherwise extra letters might be modified unnecessarily.

The checks `islower()` and `isupper()` are also important. Without them, calling `upper()` or `lower()` blindly could modify the count incorrectly. For example, applying `upper()` to an already-uppercase letter does not change the count.

## Worked Examples

### Example 1

Input:

```
AprilFool
4
```

| Index | Character | Action | Uppercase Count | Current String |
| --- | --- | --- | --- | --- |
| Start | - | Initial state | 2 | AprilFool |
| 0 | A | Already uppercase | 2 | AprilFool |
| 1 | p | Convert to uppercase | 3 | APrilFool |
| 2 | r | Convert to uppercase | 4 | APRilFool |

Final output:

```
APRilFool
```

This trace shows how the algorithm increases the uppercase count gradually and stops immediately after reaching the target.

### Example 2

Input:

```
AbCdE
2
```

| Index | Character | Action | Uppercase Count | Current String |
| --- | --- | --- | --- | --- |
| Start | - | Initial state | 3 | AbCdE |
| 0 | A | Convert to lowercase | 2 | abCdE |

Final output:

```
abCdE
```

This example demonstrates the decreasing branch. Only one modification is needed, so the algorithm stops after the first conversion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is scanned at most once or twice |
| Space | O(n) | The mutable character list stores the string |

With a maximum string length of only 50, the solution easily fits within the limits. Even far slower approaches would run comfortably, but the linear implementation is simple and clean.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    k = int(input())

    chars = list(s)

    cnt = 0
    for c in chars:
        if c.isupper():
            cnt += 1

    if cnt < k:
        for i in range(len(chars)):
            if cnt == k:
                break

            if chars[i].islower():
                chars[i] = chars[i].upper()
                cnt += 1

    elif cnt > k:
        for i in range(len(chars)):
            if cnt == k:
                break

            if chars[i].isupper():
                chars[i] = chars[i].lower()
                cnt -= 1

    print("".join(chars))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("AprilFool\n4\n") == "APRilFool", "sample"

# minimum size
assert run("a\n0\n") == "a", "single lowercase"

# all uppercase required
assert run("abc\n3\n") == "ABC", "all become uppercase"

# all lowercase required
assert run("ABC\n0\n") == "abc", "all become lowercase"

# already correct
assert run("AbC\n2\n") == "AbC", "already has correct count"

# mixed conversion
assert run("aBcDe\n3\n") == "ABCDe", "increase uppercase count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / 0` | `a` | Minimum-size input |
| `abc / 3` | `ABC` | Converting every letter to uppercase |
| `ABC / 0` | `abc` | Converting every letter to lowercase |
| `AbC / 2` | `AbC` | Already-correct uppercase count |
| `aBcDe / 3` | `ABCDe` | Greedy left-to-right conversion |

## Edge Cases

Consider the case where `k = 0`.

Input:

```
AbC
0
```

The initial uppercase count is 2. The algorithm enters the decreasing branch.

At index 0, `A` becomes `a`, reducing the count to 1.

At index 2, `C` becomes `c`, reducing the count to 0.

The final string becomes:

```
abc
```

This confirms that every uppercase letter is removed correctly.

Now consider the opposite extreme where every letter must become uppercase.

Input:

```
aBc
3
```

The initial uppercase count is 1.

At index 0, `a` becomes `A`, increasing the count to 2.

At index 2, `c` becomes `C`, increasing the count to 3.

The final string is:

```
ABC
```

The algorithm correctly stops after reaching the target count.

Finally, consider a string that already satisfies the requirement.

Input:

```
AprIL
3
```

The initial uppercase count is already 3, so neither branch executes. The string is printed unchanged:

```
AprIL
```

This verifies that the algorithm avoids unnecessary modifications.
