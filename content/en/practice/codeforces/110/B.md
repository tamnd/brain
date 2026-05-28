---
title: "CF 110B - Lucky String"
description: "We need to build a lowercase string of length n that satisfies a special condition on repeated letters. For every character, we look at all positions where it appears."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "strings"]
categories: ["algorithms"]
codeforces_contest: 110
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 84 (Div. 2 Only)"
rating: 1100
weight: 110
solve_time_s: 178
verified: true
draft: false
---

[CF 110B - Lucky String](https://codeforces.com/problemset/problem/110/B)

**Rating:** 1100  
**Tags:** constructive algorithms, strings  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to build a lowercase string of length `n` that satisfies a special condition on repeated letters.

For every character, we look at all positions where it appears. If a character appears multiple times, the difference between consecutive positions must always be a lucky number. In this problem, lucky numbers are integers whose decimal representation contains only digits `4` and `7`.

The task is not just to construct any valid string. Among all valid strings of length `n`, we must output the lexicographically smallest one.

The constraints are small enough that constructing the answer directly is the intended direction. With `n ≤ 10^5`, we can easily afford linear time or even `O(n log n)`, but anything exponential or based on brute force search over strings is impossible. Even trying all strings over a tiny alphabet explodes immediately, since there are `26^n` possible lowercase strings.

The key difficulty is lexicographic minimality. A naive greedy choice can accidentally create an invalid future state. We need a pattern that is both always valid and provably minimal.

One easy-to-miss edge case appears when `n < 4`. Since the smallest lucky number is `4`, no letter can repeat before distance `4`. For example:

Input:

```
3
```

Correct output:

```
abc
```

A careless solution that repeats letters too early might produce `"aba"`, but the two `'a'` positions differ by `2`, which is not lucky.

Another subtle case is when the string length is exactly `5`.

Input:

```
5
```

Correct output:

```
abcda
```

The repeated `'a'` positions are `1` and `5`, difference `4`, which is lucky. If we tried `"abcab"` instead, the `'a'` positions differ by `3`, invalid.

A third trap is assuming we need many lucky distances. In practice, distance `4` alone is enough to build the entire answer. Some solutions overcomplicate the construction by mixing `4` and `7`, but that is unnecessary.

## Approaches

The brute force idea is straightforward. Generate strings in lexicographic order and check whether each one satisfies the condition. To verify a string, we store all positions for each character and ensure every adjacent difference is lucky.

The verification itself is cheap, roughly `O(n)`. The problem is the number of candidate strings. Even over a small alphabet like `{a,b,c,d}`, there are already `4^100000` possibilities, which is completely infeasible.

The next observation changes the problem entirely. We do not actually need arbitrary lucky distances. The smallest lucky number is `4`, and if every repeated occurrence of a letter is exactly `4` positions apart, the condition is automatically satisfied.

That suggests a repeating block of length `4`.

Consider the pattern:

```
abcdabcdabcd...
```

Every `'a'` appears at positions differing by `4`. The same holds for `'b'`, `'c'`, and `'d'`. Since `4` is lucky, the string is valid.

Now we must show why this pattern is lexicographically minimal.

To minimize lexicographically, at every position we want the smallest possible character that does not violate the condition. The first character should clearly be `'a'`. The second cannot be `'a'` because distance `1` is not lucky, so it becomes `'b'`. The third cannot be `'a'` or `'b'`, so it becomes `'c'`. The fourth becomes `'d'`.

At the fifth position, we may reuse `'a'` because the previous `'a'` was exactly `4` positions earlier. Since `'a'` is the smallest valid choice, we take it. The same reasoning repeats forever, producing the periodic string `"abcd"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create the repeating base pattern `"abcd"`.
2. Build the answer character by character.
3. For position `i`, append `pattern[i % 4]`.

This repeats the sequence:

```
a b c d a b c d ...
```
4. Print the resulting string.

The reason this works is that every repeated occurrence of the same character is exactly `4` positions apart. Since `4` is a lucky number, all adjacency differences inside each character list are valid.

### Why it works

The construction maintains two properties simultaneously.

First, validity. Every character repeats only after exactly `4` positions. Consecutive equal letters for `'a'`, `'b'`, `'c'`, and `'d'` always differ by `4`, which is lucky.

Second, lexicographic minimality. At every position, we choose the smallest character that does not break the rule. The first four positions must all be distinct because distances `1`, `2`, and `3` are not lucky. That forces `"abcd"`. After that, reusing the character from four positions ago is valid, and choosing anything smaller is impossible. By induction, the periodic `"abcd"` pattern is the smallest valid string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pattern = "abcd"

    ans = []
    for i in range(n):
        ans.append(pattern[i % 4])

    print("".join(ans))

solve()
```

The implementation is intentionally simple because the construction itself is the whole solution.

The variable `pattern` stores the repeating block. For every position `i`, we take `pattern[i % 4]`, which cycles through indices `0, 1, 2, 3`.

Using a list and `"".join()` is the standard efficient way to build large strings in Python. Repeated string concatenation inside a loop can become quadratic.

The indexing is easy to get wrong if using one-based reasoning mentally. The modulo operation works naturally with zero-based indices:

| i | i % 4 | character |
| --- | --- | --- |
| 0 | 0 | a |
| 1 | 1 | b |
| 2 | 2 | c |
| 3 | 3 | d |
| 4 | 0 | a |

That produces exactly the intended periodic sequence.

## Worked Examples

### Example 1

Input:

```
5
```

Construction trace:

| Position (0-based) | i % 4 | Character | Current String |
| --- | --- | --- | --- |
| 0 | 0 | a | a |
| 1 | 1 | b | ab |
| 2 | 2 | c | abc |
| 3 | 3 | d | abcd |
| 4 | 0 | a | abcda |

Output:

```
abcda
```

The repeated `'a'` positions are `1` and `5`, difference `4`, which is lucky.

### Example 2

Input:

```
10
```

Construction trace:

| Position (0-based) | i % 4 | Character | Current String |
| --- | --- | --- | --- |
| 0 | 0 | a | a |
| 1 | 1 | b | ab |
| 2 | 2 | c | abc |
| 3 | 3 | d | abcd |
| 4 | 0 | a | abcda |
| 5 | 1 | b | abcdab |
| 6 | 2 | c | abcdabc |
| 7 | 3 | d | abcdabcd |
| 8 | 0 | a | abcdabcda |
| 9 | 1 | b | abcdabcdab |

Output:

```
abcdabcdab
```

This trace demonstrates the invariant clearly. Every repeated letter appears exactly four positions after its previous occurrence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We generate exactly one character per position |
| Space | O(n) | The answer string stores `n` characters |

With `n ≤ 10^5`, linear complexity is easily fast enough. The memory usage is also tiny compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    pattern = "abcd"

    ans = []
    for i in range(n):
        ans.append(pattern[i % 4])

    print("".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout
    return out.getvalue().strip()

# provided sample
assert run("5\n") == "abcda", "sample 1"

# minimum size
assert run("1\n") == "a", "single character"

# small boundary
assert run("4\n") == "abcd", "first full block"

# repeat begins
assert run("8\n") == "abcdabcd", "two full blocks"

# off-by-one check
assert run("9\n") == "abcdabcda", "correct modulo cycling"

# large input
res = run("100000\n")
assert len(res) == 100000, "maximum size length"
assert res[:8] == "abcdabcd", "pattern consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `a` | Minimum possible size |
| `4` | `abcd` | First complete non-repeating segment |
| `8` | `abcdabcd` | Valid periodic repetition |
| `9` | `abcdabcda` | Modulo indexing correctness |
| `100000` | Large periodic string | Performance at maximum constraint |

## Edge Cases

When `n = 1`, the algorithm outputs:

```
a
```

There are no repeated characters, so the condition is vacuously true. The construction handles this naturally because it simply takes the first character of the pattern.

When `n = 3`, the algorithm outputs:

```
abc
```

Trace:

| Position | Character |
| --- | --- |
| 0 | a |
| 1 | b |
| 2 | c |

No character repeats, which avoids invalid distances like `1`, `2`, or `3`. A careless greedy solution that reused `'a'` too early would fail here.

When `n = 5`, the output becomes:

```
abcda
```

The two `'a'` positions are `1` and `5`, difference `4`. This is the first moment where repetition becomes legal, and the algorithm immediately takes advantage of it to stay lexicographically minimal.

For very large inputs such as `100000`, the pattern continues periodically without any extra logic. Every repeated occurrence still differs by exactly `4`, so correctness does not depend on the string length.
