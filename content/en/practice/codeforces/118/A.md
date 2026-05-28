---
title: "CF 118A - String Task"
description: "We receive a single string containing uppercase and lowercase English letters. The task is to transform this string according to three rules. First, every vowel must be removed. The vowels in this problem are A, O, Y, E, U, I in both uppercase and lowercase forms."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 118
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 89 (Div. 2)"
rating: 1000
weight: 118
solve_time_s: 98
verified: true
draft: false
---

[CF 118A - String Task](https://codeforces.com/problemset/problem/118/A)

**Rating:** 1000  
**Tags:** implementation, strings  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We receive a single string containing uppercase and lowercase English letters. The task is to transform this string according to three rules.

First, every vowel must be removed. The vowels in this problem are `A, O, Y, E, U, I` in both uppercase and lowercase forms.

Second, every remaining character is a consonant, and we must convert it to lowercase.

Third, before each consonant we insert a dot `.`.

For example, the string `Codeforces` becomes `.c.d.f.r.c.s` because the vowels `o`, `e`, and `o` are removed, while the remaining consonants are lowercased and prefixed with dots.

The input length is at most 100 characters. That is extremely small, so performance is not a concern here. Even an inefficient solution would run instantly. Still, the cleanest approach is a single linear scan over the string.

The tricky part is not complexity, but correctness. Several small details can easily produce wrong answers if handled carelessly.

One common mistake is forgetting uppercase vowels. Consider:

```
Input:
aBAcAba
```

The correct output is:

```
.b.c.b
```

If we only check lowercase vowels, the uppercase `A` characters would incorrectly remain in the answer.

Another easy mistake is adding dots before every character before checking whether it is a vowel. For example:

```
Input:
tour
```

The correct output is:

```
.t.r
```

A careless implementation might produce:

```
.t.o.u.r
```

because it inserts dots before vowels instead of skipping them entirely.

A third subtle case is handling uppercase consonants correctly. For example:

```
Input:
QWERTY
```

The correct output is:

```
.q.w.r.t
```

The letters `E` and `Y` are vowels in this problem and must disappear, while the remaining consonants must become lowercase.

## Approaches

The most direct approach is to process the string character by character. For each character, we check whether it is a vowel. If it is not, we append a dot and the lowercase version of the character to the answer.

This already runs in linear time, because every character is examined once.

A more naive version could repeatedly rebuild strings using concatenation like:

```
ans = ans + "." + ch.lower()
```

Python strings are immutable, so every concatenation creates a new string. In the worst case this leads to quadratic behavior. With only 100 characters, even that would still pass comfortably, but it is not ideal practice.

The better approach is to build a list of pieces and join them once at the end. Appending to a list is efficient, and the final `"".join(...)` creates the answer in linear time.

The key observation is that every character is processed independently. Whether one letter survives depends only on whether that specific letter is a vowel. There are no interactions between positions, so a single pass is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Create a set containing all vowels in lowercase form:

`{'a', 'o', 'y', 'e', 'u', 'i'}`.

Using lowercase vowels lets us normalize characters before checking them.
3. Create an empty list to store parts of the final answer.
4. Iterate through each character in the string.
5. Convert the current character to lowercase.

This handles uppercase and lowercase letters uniformly.
6. Check whether the lowercase character is a vowel.

If it is a vowel, skip it completely.
7. If it is a consonant, append `"." + character` to the answer list.
8. After processing all characters, join the list into one string and print it.

### Why it works

At every step, the algorithm maintains the invariant that the answer list contains the correctly transformed version of all processed characters.

When we encounter a vowel, the problem requires it to disappear, so skipping it preserves correctness.

When we encounter a consonant, the problem requires two operations: convert it to lowercase and place a dot before it. Appending `"." + lowercase_character` performs exactly those operations.

Since every character is processed once and according to the problem rules, the final joined string is exactly the required output.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

vowels = set("aoyeui")
result = []

for ch in s:
    ch = ch.lower()

    if ch not in vowels:
        result.append("." + ch)

print("".join(result))
```

The program begins by reading the input string and removing the trailing newline with `strip()`.

The vowel set contains only lowercase letters. Instead of checking both uppercase and lowercase variants separately, the code converts every character to lowercase before any comparison. This keeps the logic simple and avoids duplication.

The `result` list stores transformed consonants. Using a list is preferable to repeated string concatenation because Python strings are immutable. Appending to a list is efficient, and joining once at the end avoids unnecessary copying.

Inside the loop, each character is normalized with `lower()`. If the character is not a vowel, the code appends a dot followed by the lowercase consonant.

The final output is produced with `"".join(result)`.

One subtle detail is the order of operations. We must lowercase the character before checking membership in the vowel set. Otherwise uppercase vowels like `E` or `Y` would incorrectly survive.

## Worked Examples

### Example 1

Input:

```
tour
```

| Current Character | Lowercase | Vowel? | Result List |
| --- | --- | --- | --- |
| t | t | No | [".t"] |
| o | o | Yes | [".t"] |
| u | u | Yes | [".t"] |
| r | r | No | [".t", ".r"] |

Final output:

```
.t.r
```

This example shows that vowels are completely removed rather than transformed.

### Example 2

Input:

```
Codeforces
```

| Current Character | Lowercase | Vowel? | Result List |
| --- | --- | --- | --- |
| C | c | No | [".c"] |
| o | o | Yes | [".c"] |
| d | d | No | [".c", ".d"] |
| e | e | Yes | [".c", ".d"] |
| f | f | No | [".c", ".d", ".f"] |
| o | o | Yes | [".c", ".d", ".f"] |
| r | r | No | [".c", ".d", ".f", ".r"] |
| c | c | No | [".c", ".d", ".f", ".r", ".c"] |
| e | e | Yes | [".c", ".d", ".f", ".r", ".c"] |
| s | s | No | [".c", ".d", ".f", ".r", ".c", ".s"] |

Final output:

```
.c.d.f.r.c.s
```

This trace demonstrates that uppercase consonants are converted correctly and vowels disappear regardless of case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed exactly once |
| Space | O(n) | The result list stores the transformed output |

The maximum input size is only 100 characters, so the algorithm easily fits within the limits. Even slower approaches would pass, but the linear solution is both clean and efficient.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()

    vowels = set("aoyeui")
    result = []

    for ch in s:
        ch = ch.lower()

        if ch not in vowels:
            result.append("." + ch)

    print("".join(result))

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
assert run("tour\n") == ".t.r", "sample 1"

# custom cases
assert run("a\n") == "", "single vowel should disappear"
assert run("b\n") == ".b", "single consonant"
assert run("Codeforces\n") == ".c.d.f.r.c.s", "mixed uppercase and lowercase"
assert run("QWERTY\n") == ".q.w.r.t", "uppercase vowels removed correctly"
assert run("abcdefghijklmnopqrstuvwxyz\n") == ".b.c.d.f.g.h.j.k.l.m.n.p.q.r.s.t.v.w.x.z", "full alphabet case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | empty string | Single vowel removal |
| `b` | `.b` | Single consonant formatting |
| `Codeforces` | `.c.d.f.r.c.s` | Mixed casing and multiple vowels |
| `QWERTY` | `.q.w.r.t` | Uppercase vowel handling |
| `abcdefghijklmnopqrstuvwxyz` | `.b.c.d.f.g.h.j.k.l.m.n.p.q.r.s.t.v.w.x.z` | Full traversal and all vowel removals |

## Edge Cases

Consider the input:

```
A
```

The algorithm converts `A` to lowercase `a`. Since `a` is a vowel, it is skipped. The result list remains empty, so the output is an empty string. This confirms uppercase vowels are handled correctly.

Consider the input:

```
BCDF
```

The processing steps are:

`B -> b -> append ".b"`

`C -> c -> append ".c"`

`D -> d -> append ".d"`

`F -> f -> append ".f"`

The final output becomes:

```
.b.c.d.f
```

This confirms that every consonant receives exactly one leading dot.

Consider the input:

```
Yy
```

Both characters become lowercase `y`. Since `y` is treated as a vowel in this problem, both are skipped. The output is empty.

A common mistake is forgetting that `Y` counts as a vowel here even though many other problems classify it differently.

Finally, consider:

```
Input:
aBAcAba
```

The processing sequence is:

`a -> vowel -> skip`

`B -> b -> append ".b"`

`A -> a -> skip`

`c -> c -> append ".c"`

`A -> a -> skip`

`b -> b -> append ".b"`

`a -> a -> skip`

The final output is:

```
.b.c.b
```

This example confirms that uppercase vowels are removed before consonant formatting happens.
