---
title: "CF 412C - Pattern"
description: "Each pattern is a string made of lowercase English letters and the wildcard character ?. A wildcard can represent any lowercase letter. Two patterns intersect if there exists at least one concrete string that matches both of them. For example, a?"
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 412
codeforces_index: "C"
codeforces_contest_name: "Coder-Strike 2014 - Round 1"
rating: 1200
weight: 412
solve_time_s: 120
verified: false
draft: false
---

[CF 412C - Pattern](https://codeforces.com/problemset/problem/412/C)

**Rating:** 1200  
**Tags:** implementation, strings  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

Each pattern is a string made of lowercase English letters and the wildcard character `?`. A wildcard can represent any lowercase letter.

Two patterns intersect if there exists at least one concrete string that matches both of them. For example, `a?c` and `abc` intersect because the string `abc` satisfies both patterns. On the other hand, `ab` and `ac` do not intersect because no string can simultaneously have `b` and `c` at the second position.

We are given several patterns of equal length. We must construct another pattern that intersects with every given pattern while using as few `?` characters as possible.

The key detail is that the answer does not need to match all patterns simultaneously. It only needs to intersect with each one individually.

The total input size is at most `10^5`, which immediately rules out anything quadratic in the total number of characters. We can afford a single linear scan over all positions of all strings, but repeatedly comparing every pair of patterns would become too expensive.

A common mistake is misunderstanding what “intersects with every pattern” means.

Consider this input:

```
2
ab
ac
```

The answer cannot be `ab` because it does not intersect with `ac`. It also cannot be `ac` for the symmetric reason. The correct answer is `a?`.

A careless approach might try to pick letters greedily from one pattern without checking compatibility with the others.

Another subtle case appears when every pattern already allows many letters at some position.

```
3
?
a
b
```

No fixed letter works for both `a` and `b`, so the answer must contain `?`. The correct output is `?`.

An incorrect implementation might pick the first concrete letter it sees and output `a`, which fails to intersect with `b`.

One more important edge case is when all patterns contain only `?` at some position.

```
2
??
??
```

Any concrete letter works there, so using `?` would be unnecessary. An optimal answer is `aa`.

A naive interpretation might think “if the input has `?`, the answer should also have `?`”, but that wastes wildcard characters.

## Approaches

The brute-force way to think about the problem is position by position. For each index, we want to decide what character to place in the answer.

Suppose we try every possible output character independently at each position. The output character can either be one of the 26 letters or `?`. For each choice, we check whether it intersects with every pattern at that position.

A character `c` intersects with a pattern character `p` if either `p == '?'` or `p == c`. Similarly, `?` intersects with everything.

This brute-force idea is already reasonably fast because the alphabet is constant sized. For every position, we test at most 27 candidates against all `n` patterns. If the string length is `m`, the complexity becomes `O(27 * n * m)`, which is effectively linear.

The interesting part is discovering what the optimal character must look like.

At one position, collect all concrete letters appearing there among the patterns. Three situations can occur.

If no concrete letters appear, every pattern has `?` there. Then any fixed letter works, and using a letter is strictly better than using `?`.

If exactly one distinct concrete letter appears, that letter is forced. Using it intersects with every pattern because all remaining patterns have `?`.

If at least two different concrete letters appear, no single fixed letter can intersect with all patterns. The only possible choice is `?`.

This observation removes the need to test candidates explicitly. We can determine the answer for each position directly from the set of distinct letters appearing there.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(27nm) | O(1) | Accepted |
| Optimal | O(nm) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read all patterns and store them in a list.
2. Let `m` be the common length of the patterns. We will construct the answer one position at a time.
3. For each position `i`, collect all concrete letters appearing at that index across every pattern.

Ignore `?` because it imposes no restriction.
4. If the set of collected letters is empty, append an arbitrary letter such as `'a'`.

Every pattern has `?` at this position, so any fixed letter intersects with all of them. Using a letter avoids an unnecessary wildcard.
5. If the set contains exactly one letter, append that letter.

Any other fixed letter would fail to intersect with the patterns containing this letter.
6. If the set contains at least two different letters, append `?`.

No single fixed letter can match all those patterns simultaneously, so `?` is the only valid option.
7. Print the constructed string.

### Why it works

At each position, the constraints are completely independent from other positions. A pattern intersects with the answer if every position can be made compatible independently.

If two different concrete letters appear at one index, any fixed choice fails for at least one pattern, so `?` becomes necessary.

If zero or one concrete letters appear, a fixed letter always works, and replacing it with `?` would only increase the wildcard count without adding any benefit.

Because we minimize the number of `?` independently at every position, the whole constructed pattern is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    patterns = [input().strip() for _ in range(n)]

    m = len(patterns[0])
    ans = []

    for i in range(m):
        letters = set()

        for s in patterns:
            if s[i] != '?':
                letters.add(s[i])

        if len(letters) == 0:
            ans.append('a')
        elif len(letters) == 1:
            ans.append(next(iter(letters)))
        else:
            ans.append('?')

    print(''.join(ans))

solve()
```

The implementation follows the exact reasoning from the algorithm section.

For each position, we build a set containing all non-`?` letters found there. The size of this set fully determines the optimal character.

Using a Python `set` keeps the logic simple and efficient. Since there are only 26 possible letters, the set never grows large.

The branch for `len(letters) == 0` is easy to overlook. In that case, every pattern already accepts any letter, so using `'a'` avoids wasting a wildcard.

The line:

```
next(iter(letters))
```

extracts the single element from the set when its size is exactly one. Any equivalent method would work.

The solution performs one scan over every character of the input, which fits comfortably within the limits.

## Worked Examples

### Example 1

Input:

```
2
?ab
??b
```

| Position | Characters Seen | Distinct Letters | Chosen Character |
| --- | --- | --- | --- |
| 0 | `?`, `?` | `{}` | `a` |
| 1 | `a`, `?` | `{a}` | `a` |
| 2 | `b`, `b` | `{b}` | `b` |

Final answer:

```
aab
```

This trace shows the “empty set” case at position `0`. Since both patterns allow any letter there, we choose a concrete character instead of `?`.

### Example 2

Input:

```
3
ab?
a?c
adc
```

| Position | Characters Seen | Distinct Letters | Chosen Character |
| --- | --- | --- | --- |
| 0 | `a`, `a`, `a` | `{a}` | `a` |
| 1 | `b`, `?`, `d` | `{b, d}` | `?` |
| 2 | `?`, `c`, `c` | `{c}` | `c` |

Final answer:

```
a?c
```

This example demonstrates the only situation where `?` becomes necessary. At position `1`, the patterns require both `b` and `d`, so no fixed letter can intersect with all of them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every character of every pattern is processed once |
| Space | O(1) excluding output | The temporary set stores at most 26 letters |

Here, `n` is the number of patterns and `m` is their length. Since the total input size is at most `10^5`, a linear scan is easily fast enough for the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())
        patterns = [input().strip() for _ in range(n)]

        m = len(patterns[0])
        ans = []

        for i in range(m):
            letters = set()

            for s in patterns:
                if s[i] != '?':
                    letters.add(s[i])

            if len(letters) == 0:
                ans.append('a')
            elif len(letters) == 1:
                ans.append(next(iter(letters)))
            else:
                ans.append('?')

        return ''.join(ans)

    return solve()

# provided sample
assert run("2\n?ab\n??b\n") == "aab", "sample 1"

# minimum size
assert run("1\n?\n") == "a", "single wildcard"

# all equal patterns
assert run("3\nabc\nabc\nabc\n") == "abc", "identical strings"

# conflicting letters force wildcard
assert run("2\nab\nac\n") == "a?", "conflict at one position"

# all positions unrestricted
assert run("2\n??\n??\n") == "aa", "replace unnecessary wildcards"

# mixed case with several conflicts
assert run("3\nab?\na?c\nadc\n") == "a?c", "multiple position handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / ?` | `a` | Minimum input size |
| Three identical strings | Same string | No unnecessary `?` inserted |
| `ab` and `ac` | `a?` | Conflict handling |
| Two strings of only `?` | `aa` | Replacing wildcards with letters |
| Mixed constraints example | `a?c` | Independent processing per position |

## Edge Cases

Consider the conflicting-letter scenario:

```
2
ab
ac
```

At position `0`, the only concrete letter is `a`, so the algorithm places `a`.

At position `1`, the set becomes `{b, c}`. Since the size exceeds one, the algorithm places `?`.

The output is:

```
a?
```

This correctly intersects with both input patterns.

Now consider the unrestricted-position case:

```
2
??
??
```

At both positions, the set of concrete letters is empty. The algorithm inserts `'a'` each time and produces:

```
aa
```

This pattern still intersects with every input pattern while using zero wildcards, which is optimal.

Finally, examine the mixed wildcard case:

```
3
?
a
b
```

The set of concrete letters becomes `{a, b}`. A fixed letter cannot satisfy both constraints, so the algorithm outputs:

```
?
```

Any implementation that simply chooses the first visible letter would fail here because `a` does not intersect with the pattern `b`.
