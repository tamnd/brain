---
title: "CF 113A - Grammar Lessons"
description: "We are given a single line containing several lowercase words separated by spaces. Every valid word in Petya's language belongs to exactly one grammatical category and exactly one gender, determined entirely by its suffix."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 113
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 86 (Div. 1 Only)"
rating: 1600
weight: 113
solve_time_s: 281
verified: true
draft: false
---

[CF 113A - Grammar Lessons](https://codeforces.com/problemset/problem/113/A)

**Rating:** 1600  
**Tags:** implementation, strings  
**Solve time:** 4m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single line containing several lowercase words separated by spaces. Every valid word in Petya's language belongs to exactly one grammatical category and exactly one gender, determined entirely by its suffix.

There are only six legal suffixes:

- `lios` for masculine adjectives
- `liala` for feminine adjectives
- `etr` for masculine nouns
- `etra` for feminine nouns
- `initis` for masculine verbs
- `inites` for feminine verbs

A valid sentence has a very rigid structure. It may contain:

- zero or more adjectives,
- followed by exactly one noun,
- followed by zero or more verbs.

All words must have the same gender.

The task is to decide whether the entire input line forms exactly one valid sentence.

The total input size is at most $10^5$ characters, so the solution must process the string in linear time. Any approach that repeatedly scans prefixes or recomputes classifications for the same word would still probably pass in practice, but there is no need for anything beyond a single left-to-right pass. A clean $O(n)$ solution is enough.

The tricky part is not performance, it is getting the grammar validation exactly right.

One easy mistake is accepting inputs with multiple nouns. A sentence must contain exactly one noun.

For example:

```
etr etr
```

The correct output is:

```
NO
```

A careless implementation that only checks suffix validity and gender consistency would incorrectly accept it.

Another subtle case is ordering. Adjectives must come before the noun, and verbs must come after it.

Example:

```
initis etr
```

The correct output is:

```
NO
```

Even though both words are masculine and individually valid, the verb appears before the noun.

Mixed genders must also be rejected immediately.

Example:

```
lios etra
```

The adjective is masculine while the noun is feminine, so the answer is:

```
NO
```

A final edge case is that a single word is itself a valid sentence, as long as that word belongs to the language.

Example:

```
inites
```

This is valid because one verb alone still fits the grammar: zero adjectives, zero nouns? No. A statement requires exactly one noun, but the problem also says a sentence may be exactly one valid language word. Since `inites` is a valid word, the answer is:

```
YES
```

This special rule is easy to overlook.

## Approaches

The most direct brute-force approach is to classify every word, then try every possible position as the noun. For each candidate noun position, we would verify that all earlier words are adjectives, all later words are verbs, and every word has the same gender.

If there are $n$ words, this requires checking up to $n$ noun positions, and each check may scan the entire sentence again. The total complexity becomes $O(n^2)$.

With $10^5$ characters, the number of words can also be large. Quadratic behavior is unnecessary and risks timing issues in Python if the input contains many short words.

The key observation is that the grammar defines a strict order among the three parts of speech:

```
adjective < noun < verb
```

A valid sentence must contain exactly one noun, and the sequence of types must never decrease.

Once each word is classified into:

- gender,
- grammatical type,

the problem becomes a simple linear scan.

We process words from left to right while checking three conditions simultaneously:

- every word belongs to the language,
- all genders match,
- grammatical types appear in nondecreasing order and contain exactly one noun.

This reduces the problem to $O(n)$ time with constant extra memory.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split the input line into words.

Each word must be analyzed independently because its suffix fully determines its role in the language.
2. For every word, determine whether it matches one of the six legal suffixes.

If no suffix matches, the entire sentence is invalid immediately.
3. Convert every word into two properties:

- gender: masculine or feminine,
- type: adjective, noun, or verb.

We can encode the types numerically:

- adjective = 0
- noun = 1
- verb = 2

This makes order checking very simple.
4. If the sentence contains exactly one word and that word is valid, print `"YES"`.

The problem explicitly allows a single valid word to be a complete sentence, regardless of whether it is a noun.
5. Otherwise, verify that all words share the same gender.

If even one word differs, print `"NO"`.
6. Count how many nouns appear.

A multiword statement must contain exactly one noun.
7. Scan the sequence of grammatical types from left to right.

The types must never decrease. In other words:

- adjectives may be followed by adjectives or the noun,
- the noun may be followed by verbs,
- verbs may only be followed by verbs.

If a smaller type appears after a larger one, the grammar order is broken.
8. If all checks pass, print `"YES"`.

### Why it works

Every valid statement in the language has exactly this structure:

```
(adjectives) noun (verbs)
```

Encoding adjective, noun, and verb as `0`, `1`, and `2` transforms the grammar rule into a monotonicity condition. A valid sentence corresponds exactly to a nondecreasing sequence containing one noun.

The gender rule is independent and global, so checking that all words share the same gender is sufficient.

The single-word exception is handled separately because the grammar allows any individual valid word to form a sentence, even without a noun.

Since every possible invalidity is detected by one of these checks, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    words = input().split()

    suffixes = [
        ("lios", "M", 0),
        ("liala", "F", 0),
        ("etr", "M", 1),
        ("etra", "F", 1),
        ("initis", "M", 2),
        ("inites", "F", 2),
    ]

    parsed = []

    for word in words:
        found = False

        for suf, gender, typ in suffixes:
            if word.endswith(suf):
                parsed.append((gender, typ))
                found = True
                break

        if not found:
            print("NO")
            return

    if len(words) == 1:
        print("YES")
        return

    genders = [g for g, _ in parsed]
    types = [t for _, t in parsed]

    if len(set(genders)) != 1:
        print("NO")
        return

    if types.count(1) != 1:
        print("NO")
        return

    for i in range(1, len(types)):
        if types[i] < types[i - 1]:
            print("NO")
            return

    print("YES")

solve()
```

The first part of the implementation classifies every word by checking which suffix it ends with. Since the suffix list is tiny and fixed, a simple loop is sufficient.

The `parsed` array stores pairs of `(gender, type)` for each word. Using integers for types simplifies ordering checks later.

The single-word special case must appear before the noun-count validation. Otherwise words like `inites` or `lios` would incorrectly fail because they are not nouns.

The gender check uses a set. If more than one distinct gender exists, the sentence is invalid.

The noun count must be exactly one for multiword statements. This catches cases like two nouns or no nouns.

Finally, the ordering condition is verified by checking that the type sequence never decreases. This compactly enforces the grammar structure without explicitly splitting the sentence into adjective, noun, and verb segments.

## Worked Examples

### Example 1

Input:

```
petr
```

| Word | Suffix Match | Gender | Type |
| --- | --- | --- | --- |
| petr | etr | M | noun |

The sentence contains only one valid word, so it is automatically accepted.

Output:

```
YES
```

This example demonstrates the single-word rule. Even though the general statement grammar requires exactly one noun surrounded by optional adjectives and verbs, the problem separately allows any valid word to form a sentence.

### Example 2

Input:

```
lios lios etr initis
```

| Word | Suffix Match | Gender | Type |
| --- | --- | --- | --- |
| lios | lios | M | adjective |
| lios | lios | M | adjective |
| etr | etr | M | noun |
| initis | initis | M | verb |

The extracted type sequence is:

```
0 0 1 2
```

This sequence is nondecreasing and contains exactly one noun.

Output:

```
YES
```

This trace confirms the central invariant of the solution. Valid statements correspond to a nondecreasing sequence of grammatical categories.

### Example 3

Input:

```
etr lios
```

| Word | Suffix Match | Gender | Type |
| --- | --- | --- | --- |
| etr | etr | M | noun |
| lios | lios | M | adjective |

The type sequence is:

```
1 0
```

The sequence decreases, meaning an adjective appears after the noun.

Output:

```
NO
```

This example shows why checking only gender and noun count is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each word is classified once |
| Space | O(n) | stores parsed word information |

Here, $n$ is the number of words in the sentence. Since the total input length is at most $10^5$, a linear scan easily fits within the time limit. Memory usage is also small because we store only a few integers and strings per word.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        words = input().split()

        suffixes = [
            ("lios", "M", 0),
            ("liala", "F", 0),
            ("etr", "M", 1),
            ("etra", "F", 1),
            ("initis", "M", 2),
            ("inites", "F", 2),
        ]

        parsed = []

        for word in words:
            found = False

            for suf, gender, typ in suffixes:
                if word.endswith(suf):
                    parsed.append((gender, typ))
                    found = True
                    break

            if not found:
                return "NO"

        if len(words) == 1:
            return "YES"

        genders = [g for g, _ in parsed]
        types = [t for _, t in parsed]

        if len(set(genders)) != 1:
            return "NO"

        if types.count(1) != 1:
            return "NO"

        for i in range(1, len(types)):
            if types[i] < types[i - 1]:
                return "NO"

        return "YES"

    return solve()

# provided sample
assert run("petr\n") == "YES", "sample 1"

# custom cases
assert run("inites\n") == "YES", "single valid non-noun word"

assert run("lios etr initis\n") == "YES", "valid full sentence"

assert run("etr etr\n") == "NO", "multiple nouns"

assert run("etr lios\n") == "NO", "wrong grammatical order"

assert run("lios etra\n") == "NO", "mixed genders"

assert run("abc\n") == "NO", "invalid suffix"

long_input = " ".join(["lios"] * 50000 + ["etr"]) + "\n"
assert run(long_input) == "YES", "large input stress test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `inites` | `YES` | single-word exception |
| `lios etr initis` | `YES` | valid adjective-noun-verb structure |
| `etr etr` | `NO` | exactly one noun required |
| `etr lios` | `NO` | ordering constraint |
| `lios etra` | `NO` | gender consistency |
| `abc` | `NO` | invalid language word |
| large repeated adjectives | `YES` | linear performance |

## Edge Cases

Consider the input:

```
etr etr
```

The algorithm classifies both words as masculine nouns, producing the type sequence:

```
1 1
```

The ordering condition passes because the sequence is nondecreasing. The crucial check is the noun count. Since there are two nouns instead of one, the algorithm correctly prints:

```
NO
```

Now consider:

```
initis etr
```

The types become:

```
2 1
```

During the left-to-right scan, the algorithm detects that `1 < 2`, meaning the sequence decreases. This violates the required adjective-noun-verb ordering, so the answer is:

```
NO
```

For mixed genders:

```
lios etra
```

The parsed representation is:

```
(M, adjective)
(F, noun)
```

The gender set contains both `M` and `F`, so the sentence is rejected immediately.

Finally, examine the special single-word case:

```
inites
```

The word is recognized as a feminine verb. Normally, a statement would require a noun, but the problem separately allows any single valid word to be a sentence. The algorithm checks `len(words) == 1` before enforcing the noun count, producing the correct answer:

```
YES
```
