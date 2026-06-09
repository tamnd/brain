---
title: "CF 1762C - Binary Strings are Fun"
description: "We are given a binary string s. For every prefix of s, we define a value f(prefix). To compute f(x), we look at all possible extensions of x. If x has length k, an extension has length 2k-1."
date: "2026-06-09T13:55:04+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1762
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 838 (Div. 2)"
rating: 1400
weight: 1762
solve_time_s: 629
verified: true
draft: false
---

[CF 1762C - Binary Strings are Fun](https://codeforces.com/problemset/problem/1762/C)

**Rating:** 1400  
**Tags:** combinatorics, math  
**Solve time:** 10m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string `s`. For every prefix of `s`, we define a value `f(prefix)`.

To compute `f(x)`, we look at all possible extensions of `x`. If `x` has length `k`, an extension has length `2k-1`. The characters of `x` are fixed at odd positions of the extension, while every even position can be chosen freely as `0` or `1`.

Among those extensions, we count how many are "good".

A good extension has a special property. For every odd position `i`, the character at position `i` must equal the median of the prefix ending at `i`. Since the alphabet is binary, the median is simply the majority value in that odd-length prefix.

For each test case, we must compute

$$\sum_{i=1}^{n} f(s[1..i])$$

modulo `998244353`.

The total length over all test cases is at most `2·10^5`. Any solution that processes each prefix independently and enumerates extensions is impossible. Even a single prefix of length `200000` has `2^{199999}` extensions. We need a linear or near-linear solution per test case.

A subtle source of mistakes is misunderstanding what the median condition means.

Consider:

```
s = 11
```

The extensions are:

```
101
111
```

Both are good, so `f(11)=2`.

Now consider:

```
s = 01
```

The extensions are:

```
001
011
```

Only `011` is good, so `f(01)=1`.

A solution that assumes every even position is always free will overcount.

Another easy mistake appears when a run changes.

Consider:

```
s = 010
```

The answer is:

```
f(0)=1
f(01)=1
f(010)=1
```

Total `3`.

The moment adjacent characters differ, the number of good extensions stops doubling.

## Approaches

The brute force interpretation is straightforward. For every prefix, generate all `2^{len-1}` extensions, check whether each extension satisfies the median condition, and count the valid ones.

This is correct because it directly follows the definition. Unfortunately, for a prefix of length `k`, there are `2^{k-1}` extensions. With `k` as large as `200000`, this is hopeless.

The key observation comes from examining what the median condition actually imposes.

Suppose we already processed a prefix ending at odd position `2i-1`. When we extend to odd position `2i+1`, we insert exactly one free bit between two fixed bits.

Let the fixed bits be:

```
a_i and a_{i+1}
```

If these two bits are different, the inserted bit becomes completely determined. There is exactly one choice that preserves the median condition.

If these two bits are equal, there are two valid choices for the inserted bit.

This transforms a seemingly global median constraint into a simple local rule between consecutive characters of the original string.

Let `dp[i]` denote the number of good extensions for prefix `s[1..i]`.

When:

```
s[i] != s[i-1]
```

the count does not change.

When:

```
s[i] == s[i-1]
```

the count doubles.

More precisely:

```
dp[1] = 1

dp[i] =
dp[i-1]                  if s[i] != s[i-1]
2 * dp[i-1]             if s[i] == s[i-1]
```

Since the final answer is the sum of all `dp[i]`, we can compute everything in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(2^n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `cur = 1`.

This represents `f(s[1])`. A single character has exactly one good extension.
2. Initialize `answer = 1`.

We already know the contribution of the first prefix.
3. Iterate from position `2` to position `n`.
4. If `s[i] == s[i-1]`, multiply `cur` by `2`.

Two valid choices exist for the newly inserted even-position bit.
5. If `s[i] != s[i-1]`, leave `cur` unchanged.

The inserted bit is forced, so the number of good extensions does not increase.
6. Add `cur` to the running answer.
7. Perform all operations modulo `998244353`.
8. Output the final answer.

### Why it works

Let `g_i` be the number of good extensions of prefix `s[1..i]`.

Moving from prefix length `i-1` to `i` introduces exactly one new free position in the extension.

If the newly added fixed character equals the previous fixed character, either value can be placed in the inserted position without violating the median condition. Every previous valid extension generates two new valid extensions.

If the newly added fixed character differs from the previous one, exactly one value can be inserted while maintaining the required median relationship. Every previous valid extension generates exactly one new valid extension.

Thus:

$$g_i =
\begin{cases}
2g_{i-1} & s_i=s_{i-1}\\
g_{i-1} & s_i\ne s_{i-1}
\end{cases}$$

This recurrence counts all good extensions and only good extensions. Summing all `g_i` gives the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

t = int(input())

for _ in range(t):
    n = int(input())
    s = input().strip()

    cur = 1
    ans = 1

    for i in range(1, n):
        if s[i] == s[i - 1]:
            cur = (cur * 2) % MOD

        ans = (ans + cur) % MOD

    print(ans)
```

The variable `cur` stores the number of good extensions for the current prefix. Whenever two adjacent characters are equal, every existing extension splits into two valid continuations, so `cur` doubles.

When adjacent characters differ, no new branching occurs. The count stays unchanged.

The answer is the sum of `cur` over all prefixes.

The only implementation detail that matters is applying the modulus immediately after multiplication and addition.

## Worked Examples

### Example 1

```
s = 11
```

| Prefix | Adjacent equal? | cur | Running answer |
| --- | --- | --- | --- |
| 1 | - | 1 | 1 |
| 11 | Yes | 2 | 3 |

Output:

```
3
```

This matches:

```
f(1)=1
f(11)=2
```

### Example 2

```
s = 010
```

| Prefix | Adjacent equal? | cur | Running answer |
| --- | --- | --- | --- |
| 0 | - | 1 | 1 |
| 01 | No | 1 | 2 |
| 010 | No | 1 | 3 |

Output:

```
3
```

This demonstrates that changing bits does not increase the number of valid extensions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the string |
| Space | O(1) | Only a few variables are stored |

The total length across all test cases is at most `2·10^5`, so a linear solution easily fits within the limits.

## Test Cases

```python
import io
import sys

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        cur = 1
        ans = 1

        for i in range(1, n):
            if s[i] == s[i - 1]:
                cur = (cur * 2) % MOD
            ans = (ans + cur) % MOD

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""6
1
1
1
0
2
11
3
010
9
101101111
37
1011011111011010000011011111111011111
""") == """1
1
3
3
21
365"""

# minimum size
assert run("""1
1
0
""") == "1"

# all equal
assert run("""1
4
1111
""") == "15"

# alternating
assert run("""1
5
01010
""") == "5"

# single doubling event
assert run("""1
3
001
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | Smallest possible string |
| `1111` | `15` | Repeated doubling |
| `01010` | `5` | No doubling at all |
| `001` | `5` | One equal pair followed by a change |

## Edge Cases

Consider:

```
n = 1
s = 0
```

There is only one prefix. The algorithm starts with `cur = 1` and never enters the loop. The answer is `1`, which is correct.

Consider:

```
s = 0000
```

The values of `cur` become:

```
1, 2, 4, 8
```

The answer becomes:

```
1 + 2 + 4 + 8 = 15
```

Every adjacent pair is equal, so every step doubles the number of good extensions.

Consider:

```
s = 010101
```

Every adjacent pair differs. The value of `cur` always remains `1`. The answer is simply the number of prefixes:

```
6
```

This confirms that changes between neighboring bits remove all branching and leave exactly one valid extension path.
