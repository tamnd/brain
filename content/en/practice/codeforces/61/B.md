---
title: "CF 61B - Hard Work"
description: "We are given three original strings. A student's answer is considered correct if it can be formed by concatenating these three strings in any order, after ignoring two kinds of differences. The first difference is letter casing."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 61
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 57 (Div. 2)"
rating: 1300
weight: 61
solve_time_s: 395
verified: true
draft: false
---

[CF 61B - Hard Work](https://codeforces.com/problemset/problem/61/B)

**Rating:** 1300  
**Tags:** strings  
**Solve time:** 6m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three original strings. A student's answer is considered correct if it can be formed by concatenating these three strings in any order, after ignoring two kinds of differences.

The first difference is letter casing. Uppercase and lowercase versions of the same letter should be treated as equal.

The second difference is the presence of the special characters `-`, `;`, and `_`. These characters are completely ignored. A student may insert extra ones, remove existing ones, or place them anywhere.

For every student answer, we must print `ACC` if the cleaned answer matches some permutation of the three cleaned original strings. Otherwise we print `WA`.

The constraints are tiny. Each original string has length at most 100, and there are only three of them. Every student answer has length at most 600, and there are at most 1000 answers. Even an approach that tries all permutations directly is easily fast enough because there are only `3! = 6` possible orders.

The tricky part is not performance, it is normalization. A careless implementation may compare raw strings and reject answers that differ only by ignored characters or case.

Consider this example:

```
Original strings:
Ab
Cd
Ef

Student answer:
__efABcd;;
```

The correct result is `ACC` because after removing signs and converting to lowercase, the answer becomes `efabcd`, which is exactly one valid concatenation.

Another common mistake is forgetting that signs inside the original strings must also be ignored.

```
Original strings:
A_B
C
D

Student answer:
abcd
```

The correct output is `ACC`. If we only clean student answers but not the original strings, we would incorrectly expect `a_bd` instead of `ab`.

One more subtle case is partial matching.

```
Original strings:
ab
cd
ef

Student answer:
abcdefg
```

This must be `WA`. Even though the answer contains a valid concatenation as a prefix, the entire cleaned string must match exactly.

## Approaches

The most direct idea is to generate every possible concatenation order of the three strings, normalize each one, and compare every student answer against these valid results.

Since there are only three strings, there are exactly six permutations. For each permutation, we concatenate the strings, remove all signs, and convert everything to lowercase. Then each student answer is normalized in the same way and checked against the six valid strings.

This brute-force approach is already completely acceptable. The amount of work is tiny:

- Six permutations.
- Each concatenated string has length at most 300 before cleaning.
- At most 1000 student answers.

The total operations stay far below a few million character operations.

The key observation is that the order count is fixed and extremely small. If the number of strings were large, generating all permutations would explode factorially. Here, `3!` is just 6, so precomputing all valid normalized concatenations is the simplest and cleanest solution.

A slightly cleaner version stores the six valid normalized strings inside a set. Then each query becomes a constant-time membership check after normalization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force by checking all permutations directly per query | O(6 × L × n) | O(1) | Accepted |
| Optimal with precomputed normalized set | O(6 × L + n × L) | O(1) | Accepted |

Here, `L` represents the maximum string length involved in normalization.

## Algorithm Walkthrough

1. Read the three original strings.
2. Define a normalization function.

This function removes every occurrence of `-`, `;`, and `_`, then converts the remaining letters to lowercase. Two strings are considered equivalent exactly when their normalized forms are equal.
3. Generate all six permutations of the three strings.

For each permutation, concatenate the strings in that order and normalize the result.
4. Store all normalized concatenations inside a set.

Using a set makes membership checks fast and avoids duplicate entries automatically.
5. Read each student's answer.
6. Normalize the student's answer using the same normalization function.

Using identical processing for both originals and answers guarantees fair comparison.
7. Check whether the normalized answer exists in the set of valid concatenations.

If it exists, print `ACC`. Otherwise print `WA`.

### Why it works

The normalization function removes every distinction that the statement tells us to ignore. After normalization, two strings are equal exactly when they should be considered equivalent by the problem rules.

Every valid answer must correspond to one of the six possible concatenation orders of the three original strings. Since we generate and normalize all six possibilities beforehand, the set contains every correct answer and nothing else.

A student's answer is accepted if and only if its normalized form matches one of these normalized valid concatenations.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def normalize(s):
    res = []
    
    for ch in s:
        if ch not in "-;_":
            res.append(ch.lower())
    
    return "".join(res)

def solve():
    arr = [input().strip() for _ in range(3)]

    valid = set()

    for p in permutations(arr):
        combined = p[0] + p[1] + p[2]
        valid.add(normalize(combined))

    n = int(input())

    for _ in range(n):
        ans = normalize(input().strip())

        if ans in valid:
            print("ACC")
        else:
            print("WA")

solve()
```

The `normalize` function is the core of the solution. It removes all ignored signs and converts letters to lowercase. Using the same function for both the original strings and student answers prevents inconsistencies.

The permutations are generated using `itertools.permutations`. Since there are only three strings, this produces exactly six orders.

The valid normalized concatenations are stored in a set. Membership testing in a set is efficient and keeps the checking logic simple.

One subtle implementation detail is stripping newline characters with `.strip()` before processing. Forgetting this would leave trailing `\n` characters inside the strings and break comparisons.

Another important detail is cleaning the original strings as well as the answers. The statement allows signs to appear anywhere in both.

## Worked Examples

### Example 1

Input:

```
Iran_
Persian;
W_o;n;d;e;r;f;u;l;
WonderfulPersianIran
```

After normalization:

| Step | Value |
| --- | --- |
| Original 1 | `iran` |
| Original 2 | `persian` |
| Original 3 | `wonderful` |
| Student answer | `wonderfulpersianiran` |

One valid permutation is:

| Permutation | Normalized result |
| --- | --- |
| Wonderful + Persian + Iran | `wonderfulpersianiran` |

The student's normalized answer matches a valid normalized concatenation, so the output is:

```
ACC
```

This example demonstrates that signs are ignored everywhere, including inside the original strings.

### Example 2

Input:

```
ab
cd
ef
abcdefg
```

Normalization changes nothing here.

| Step | Value |
| --- | --- |
| Valid concatenation example | `abcdef` |
| Student answer | `abcdefg` |

The answer contains an extra character `g`, so it does not exactly match any valid concatenation.

Output:

```
WA
```

This example confirms that the comparison must be exact after normalization, not substring-based.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × L) | Each answer is normalized once, and only six valid strings are precomputed |
| Space | O(L) | The set stores at most six normalized concatenations |

Here, `L` is the maximum string length after concatenation. Since the total input size is very small, this solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def normalize(s):
        res = []

        for ch in s:
            if ch not in "-;_":
                res.append(ch.lower())

        return "".join(res)

    arr = [input().strip() for _ in range(3)]

    valid = set()

    for p in permutations(arr):
        valid.add(normalize(p[0] + p[1] + p[2]))

    n = int(input())

    out = []

    for _ in range(n):
        ans = normalize(input().strip())

        if ans in valid:
            out.append("ACC")
        else:
            out.append("WA")

    return "\n".join(out)

# provided sample
assert run(
"""Iran_
Persian;
W_o;n;d;e;r;f;u;l;
7
WonderfulPersianIran
wonderful_PersIAN_IRAN;;_
WONDERFUL___IRAN__PERSIAN__;;
Ira__Persiann__Wonderful
Wonder;;fulPersian___;I;r;a;n;
__________IranPersianWonderful__________
PersianIran_is_Wonderful
"""
) == "\n".join([
    "ACC",
    "ACC",
    "ACC",
    "WA",
    "ACC",
    "ACC",
    "WA"
]), "sample 1"

# minimum-size strings
assert run(
"""a
b
c
2
abc
acb
"""
) == "\n".join([
    "ACC",
    "ACC"
]), "minimum size"

# case insensitivity
assert run(
"""Ab
Cd
Ef
2
abcdef
EFABCD
"""
) == "\n".join([
    "ACC",
    "ACC"
]), "case handling"

# ignored signs
assert run(
"""a_b
c;d
-e
2
abcde
ab_cd_e
"""
) == "\n".join([
    "ACC",
    "ACC"
]), "sign removal"

# incorrect extra character
assert run(
"""ab
cd
ef
1
abcdefg
"""
) == "WA", "extra characters must fail"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a b c` with `abc` and `acb` | `ACC ACC` | Minimum-size valid permutations |
| Mixed uppercase answers | `ACC` | Case-insensitive comparison |
| Strings containing signs | `ACC` | Correct removal of ignored characters |
| Extra trailing character | `WA` | Exact matching after normalization |

## Edge Cases

Consider the case where ignored signs appear inside the original strings.

```
Input:
A_B
C
D
1
abcd
```

The algorithm normalizes the originals into:

```
ab
c
d
```

One generated concatenation becomes `abcd`. The student's answer also normalizes to `abcd`, so the output is:

```
ACC
```

This works because normalization is applied symmetrically to both sides.

Now consider mixed casing.

```
Input:
Ab
Cd
Ef
1
eFaBcD
```

The valid permutation `Ef + Ab + Cd` normalizes to:

```
efabcd
```

The student's answer also normalizes to:

```
efabcd
```

The set lookup succeeds, so the answer is accepted.

Finally, consider a near match with extra characters.

```
Input:
ab
cd
ef
1
abcdefx
```

The valid normalized strings all have length 6. The student's normalized answer has length 7:

```
abcdefx
```

Since the algorithm compares complete normalized strings, not prefixes, the answer is rejected correctly with:

```
WA
```
