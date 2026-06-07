---
title: "CF 2132A - Homework"
description: "We start with a string a. Another string b contains characters that must be inserted one by one, in the order they appear. For every position i in b, the corresponding character c[i] tells us who inserts that character."
date: "2026-06-08T02:49:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 2132
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1043 (Div. 3)"
rating: 800
weight: 2132
solve_time_s: 103
verified: true
draft: false
---

[CF 2132A - Homework](https://codeforces.com/problemset/problem/2132/A)

**Rating:** 800  
**Tags:** brute force, implementation, strings  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a string `a`. Another string `b` contains characters that must be inserted one by one, in the order they appear.

For every position `i` in `b`, the corresponding character `c[i]` tells us who inserts that character. If `c[i] = 'V'`, Vlad inserts `b[i]` at the beginning of the current string. If `c[i] = 'D'`, Dima inserts `b[i]` at the end.

After processing all characters of `b`, we must output the final string.

The constraints are extremely small. Both `a` and `b` have length at most 10, and there are at most 1000 test cases. Even a direct simulation that physically modifies the string after every operation performs only a few dozen character operations per test case. Efficiency is not a concern here. The task is purely about implementing the described process correctly.

The main source of mistakes is handling the insertion order.

Consider:

```
a = "x"
b = "ab"
c = "VV"
```

The operations are:

```
x
ax
bax
```

The answer is:

```
bax
```

A careless solution might collect all characters assigned to Vlad and prepend them in their original order, producing `"abx"`, which is incorrect. Every new Vlad character is placed before everything that already exists.

Another easy mistake is processing all Vlad operations first and all Dima operations later.

Example:

```
a = "ot"
b = "ad"
c = "DV"
```

Correct process:

```
ot
ota
dota
```

Answer:

```
dota
```

If we grouped operations by person instead of respecting their chronological order, we would get a different result.

## Approaches

The most direct idea is to simulate exactly what the statement describes.

We maintain the current string. For each position `i`, if `c[i]` is `'V'`, we place `b[i]` at the front. Otherwise we place it at the back.

Because the strings are tiny, even creating a brand new string after every insertion is completely acceptable. The longest possible string has length at most `n + m ≤ 20`, so each insertion costs at most 20 character copies.

In the worst case, we perform at most 10 insertions, each on a string of length at most 20. That is only a few hundred character operations per test case.

There is a slightly cleaner observation. Characters inserted by Vlad always accumulate on the left side, while characters inserted by Dima always accumulate on the right side.

When Vlad inserts characters at the front, the most recent Vlad character becomes the leftmost one. That means Vlad's characters appear in reverse order of their appearance in `b`.

When Dima inserts characters at the end, their order remains unchanged.

So we can build:

```
left  = all b[i] where c[i] = 'V'
right = all b[i] where c[i] = 'D'
```

Then the final answer is:

```
reverse(left) + a + right
```

Both methods are accepted. The second one avoids repeated string modifications and directly constructs the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m(n+m)) | O(n+m) | Accepted |
| Optimal Construction | O(n+m) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Read the strings `a`, `b`, and `c`.
2. Create two empty strings (or lists), `left` and `right`.
3. Scan all positions of `b`.
4. If `c[i]` is `'V'`, append `b[i]` to `left`.

We only record the character for now. Its final position will be determined later.
5. If `c[i]` is `'D'`, append `b[i]` to `right`.

Dima's characters preserve their original order because each one is appended to the end.
6. Reverse `left`.

Vlad repeatedly inserts at the beginning, so the last Vlad character processed becomes the leftmost character in the final string.
7. Output:

```
reverse(left) + a + right
```

### Why it works

Every Vlad operation inserts a character before the entire current string. Suppose Vlad receives characters:

```
x1, x2, x3
```

in that order.

Their effect is:

```
x1 + ...
x2 + x1 + ...
x3 + x2 + x1 + ...
```

So Vlad's characters appear in reverse order.

Dima's operations always append to the end:

```
... + y1
... + y1 + y2
... + y1 + y2 + y3
```

Thus Dima's characters appear in their original order.

Nothing can move characters from one side of `a` to the other. The final structure is exactly:

```
(reversed Vlad characters) + a + (Dima characters)
```

which is precisely what the algorithm constructs.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = input().strip()

    m = int(input())
    b = input().strip()
    c = input().strip()

    left = []
    right = []

    for ch, who in zip(b, c):
        if who == 'V':
            left.append(ch)
        else:
            right.append(ch)

    ans = ''.join(reversed(left)) + a + ''.join(right)
    print(ans)
```

The solution separates characters according to who inserts them.

Characters assigned to Vlad are stored in `left`. They are collected in the same order as they appear in `b`, but their final order must be reversed because every new Vlad insertion happens at the front.

Characters assigned to Dima are stored in `right`. Their order does not change because appending to the end preserves chronology.

Finally, the answer is assembled from three parts: the reversed Vlad segment, the original string `a`, and the Dima segment.

Using lists and `''.join()` is standard practice in Python and avoids unnecessary intermediate string creations.

## Worked Examples

### Example 1

Input:

```
a = "ot"
b = "ad"
c = "DV"
```

| Step | Character | Owner | left | right |
| --- | --- | --- | --- | --- |
| Start | - | - | "" | "" |
| 1 | a | D | "" | "a" |
| 2 | d | V | "d" | "a" |

Final construction:

```
reverse("d") + "ot" + "a"
= "dota"
```

Output:

```
dota
```

This example shows that operation order matters. Dima acts first, then Vlad inserts in front of the entire current string.

### Example 2

Input:

```
a = "biz"
b = "abon"
c = "VVDD"
```

| Step | Character | Owner | left | right |
| --- | --- | --- | --- | --- |
| Start | - | - | "" | "" |
| 1 | a | V | "a" | "" |
| 2 | b | V | "ab" | "" |
| 3 | o | D | "ab" | "o" |
| 4 | n | D | "ab" | "on" |

Final construction:

```
reverse("ab") + "biz" + "on"
= "ba" + "biz" + "on"
= "babizon"
```

Output:

```
babizon
```

This trace demonstrates why Vlad's characters must be reversed while Dima's must not.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One scan through the strings and one reversal of at most `m` characters |
| Space | O(n + m) | Storage for the answer and the temporary character lists |

Since `n` and `m` are both at most 10, the running time is tiny. Even across 1000 test cases, the total work remains negligible compared to the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = input().strip()

        m = int(input())
        b = input().strip()
        c = input().strip()

        left = []
        right = []

        for ch, who in zip(b, c):
            if who == "V":
                left.append(ch)
            else:
                right.append(ch)

        out.append("".join(reversed(left)) + a + "".join(right))

    return "\n".join(out)

# provided sample
assert run(
"""4
2
ot
2
ad
DV
3
efo
7
rdcoecs
DVDVDVD
3
aca
4
bbaa
DVDV
3
biz
4
abon
VVDD
"""
) == "\n".join([
    "dota",
    "codeforces",
    "abacaba",
    "babizon"
]), "sample"

# minimum sizes
assert run(
"""1
1
a
1
b
V
"""
) == "ba"

# all Dima
assert run(
"""1
1
x
4
abcd
DDDD
"""
) == "xabcd"

# all Vlad
assert run(
"""1
1
x
4
abcd
VVVV
"""
) == "dcbax"

# mixed boundary case
assert run(
"""1
1
m
5
abcde
VDDVD
"""
) == "eambcd"
```

### Custom Test Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a`, `b`, `V` | `ba` | Smallest valid instance |
| All `D` operations | `xabcd` | Right-side insertions preserve order |
| All `V` operations | `dcbax` | Left-side insertions reverse order |
| Mixed `VDDVD` case | `eambcd` | Combination of both behaviors |

## Edge Cases

Consider the case where every inserted character belongs to Vlad.

Input:

```
1
1
x
4
abcd
VVVV
```

Processing order:

```
x
ax
bax
cbax
dcbax
```

The algorithm stores:

```
left = "abcd"
right = ""
```

After reversing `left`:

```
"dcba"
```

Final answer:

```
dcbax
```

which matches the direct simulation.

Now consider the opposite case.

Input:

```
1
1
x
4
abcd
DDDD
```

Every character is appended:

```
x
xa
xab
xabc
xabcd
```

The algorithm builds:

```
left = ""
right = "abcd"
```

and returns:

```
xabcd
```

with no reversal affecting Dima's characters.

Finally, consider alternating operations.

Input:

```
1
1
z
3
abc
VDV
```

Simulation:

```
z
az
azb
cazb
```

Algorithm:

```
left = "ac"
right = "b"
```

Result:

```
reverse("ac") + "z" + "b"
= "ca" + "z" + "b"
= "cazb"
```

This confirms that separating characters by side and reversing only Vlad's portion reproduces the exact effect of the chronological insertions.
