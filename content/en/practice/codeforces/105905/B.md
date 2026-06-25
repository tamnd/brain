---
title: "CF 105905B - \u0423\u0434\u0430\u043b\u0438 \u0441\u0438\u043c\u0432\u043e\u043b\u044b"
description: "We are given a lowercase string. In one operation, we may remove two characters that are mirror images with respect to the current string's ends. In other words, if one character is the k-th character from the left, the other must be the k-th character from the right."
date: "2026-06-25T14:14:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105905
codeforces_index: "B"
codeforces_contest_name: "Ural championship 2025"
rating: 0
weight: 105905
solve_time_s: 83
verified: true
draft: false
---

[CF 105905B - \u0423\u0434\u0430\u043b\u0438 \u0441\u0438\u043c\u0432\u043e\u043b\u044b](https://codeforces.com/problemset/problem/105905/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string. In one operation, we may remove two characters that are mirror images with respect to the current string's ends. In other words, if one character is the k-th character from the left, the other must be the k-th character from the right. The operation is allowed only when those two characters are equal.

After removing the pair, the remaining parts of the string are glued together. We may perform any number of operations and want the minimum possible final length.

The string length can be as large as $10^5$, which immediately rules out any simulation that repeatedly rebuilds strings or explores different operation orders. An $O(n^2)$ solution is already too slow, so we should aim for a single linear scan.

A subtle point is that deleting one mirrored pair changes the current string, so it is tempting to think that new deletion opportunities might appear later. A careless implementation may try to simulate operations dynamically and end up with unnecessary complexity.

Consider the string:

```
abba
```

The mirrored pairs are `(a,a)` and `(b,b)`. Both pairs can be removed, so the answer is:

```
0
```

Now consider:

```
abca
```

The outer pair `(a,a)` can be removed, but `(b,c)` cannot. The minimum length is:

```
2
```

Another important example is:

```
abcde
```

Every mirrored pair contains different letters, so no operation is possible and the answer is:

```
5
```

The key observation is that operations never change which original mirrored positions correspond to each other. That completely determines the solution.

## Approaches

A brute-force idea is to repeatedly search for removable mirrored pairs, delete one of them, rebuild the string, and continue. Since every deletion changes indices, we would need to maintain the current string explicitly. In the worst case, rebuilding strings after every operation leads to quadratic behavior.

The breakthrough comes from looking at the string as a collection of mirrored pairs.

For every position `i` in the left half, there is exactly one mirrored position `n - 1 - i` in the right half. Let us call this a mirrored pair.

Suppose a mirrored pair contains equal characters. Then that pair can eventually be deleted.

Suppose a mirrored pair contains different characters. No operation can ever delete either of them. The reason is that every operation removes one complete mirrored pair. Removing some other mirrored pair does not change the fact that these two characters remain paired with each other.

This means each mirrored pair is completely independent:

If the two characters are equal, both disappear.

If the two characters are different, both remain forever.

For odd-length strings, the middle character has no partner and can never be removed.

So the answer is simply:

```
2 × (number of mismatched mirrored pairs)
+ (1 if the length is odd else 0)
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) or worse | O(n) | Too slow |
| Count Mirrored Mismatches | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the string and let its length be `n`.
2. Initialize a counter `bad = 0`.
3. For every index `i` from `0` to `n // 2 - 1`, compare:

```
s[i]
s[n - 1 - i]
```
4. If the characters are different, increment `bad`.

Each such mirrored pair can never be removed, so both characters must remain in the final string.
5. After processing all mirrored pairs, compute:

```
answer = 2 * bad + (n % 2)
```

The term `2 * bad` counts all characters belonging to mismatched mirrored pairs.

The term `n % 2` accounts for the center character when the length is odd.
6. Output the answer.

### Why it works

Every operation removes exactly one mirrored pair whose characters are equal.

Removing a mirrored pair does not alter the pairing relationship of the remaining mirrored pairs. A pair that started as `(x, y)` remains paired together until the end.

Because of that, every mirrored pair can be analyzed independently.

Equal mirrored pairs can be removed completely.

Unequal mirrored pairs can never be removed.

The middle character of an odd-length string never has a partner, so it always survives.

The algorithm counts exactly the characters that must remain after all possible deletions, which is the minimum achievable length.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)

bad = 0

for i in range(n // 2):
    if s[i] != s[n - 1 - i]:
        bad += 1

print(2 * bad + (n % 2))
```

The implementation follows the mathematical observation directly.

The loop only visits the left half of the string. For each position, it compares the character with its mirrored partner on the right side.

Every mismatch contributes exactly two unavoidable characters to the answer. Every matching pair contributes zero because both characters can be removed.

The expression `n % 2` handles the center character automatically. For even lengths it contributes zero, while for odd lengths it contributes one.

There are no off-by-one issues because the loop runs exactly over the mirrored pairs and never touches the center position.

## Worked Examples

### Example 1

Input:

```
abba
```

| i | Left Character | Right Character | Mismatch Count |
| --- | --- | --- | --- |
| 0 | a | a | 0 |
| 1 | b | b | 0 |

Final answer:

```
2 * 0 + 0 = 0
```

Output:

```
0
```

This example shows that every mirrored pair matches, so the entire string can disappear.

### Example 2

Input:

```
aabaa
```

| i | Left Character | Right Character | Mismatch Count |
| --- | --- | --- | --- |
| 0 | a | a | 0 |
| 1 | a | a | 0 |

The length is odd, so the center character survives.

Final answer:

```
2 * 0 + 1 = 1
```

Output:

```
1
```

This demonstrates the role of the middle character. Even when every mirrored pair disappears, the center remains.

### Example 3

Input:

```
abcde
```

| i | Left Character | Right Character | Mismatch Count |
| --- | --- | --- | --- |
| 0 | a | e | 1 |
| 1 | b | d | 2 |

Final answer:

```
2 * 2 + 1 = 5
```

Output:

```
5
```

No mirrored pair matches, so nothing can be deleted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass over half of the string |
| Space | O(1) | Only a few counters are used |

With $n \le 10^5$, a linear scan is easily fast enough for the time limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    s = input().strip()
    n = len(s)

    bad = 0
    for i in range(n // 2):
        if s[i] != s[n - 1 - i]:
            bad += 1

    print(2 * bad + (n % 2))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided samples
assert run("abba\n") == "0\n", "sample 1"
assert run("abcde\n") == "5\n", "sample 2"
assert run("aabaa\n") == "1\n", "sample 3"

# custom cases
assert run("a\n") == "1\n", "single character"
assert run("aa\n") == "0\n", "smallest removable pair"
assert run("ab\n") == "2\n", "single mismatched pair"
assert run("aaaaaa\n") == "0\n", "all equal characters"
assert run("abccba\n") == "0\n", "full palindrome"
assert run("abcdef\n") == "6\n", "all mirrored pairs mismatch"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `1` | Odd length center survives |
| `aa` | `0` | Single removable mirrored pair |
| `ab` | `2` | Single mismatched mirrored pair |
| `aaaaaa` | `0` | All pairs removable |
| `abccba` | `0` | General palindrome |
| `abcdef` | `6` | No deletions possible |

## Edge Cases

Consider:

```
a
```

There are no mirrored pairs at all. The algorithm finds `bad = 0`, and since the length is odd:

```
answer = 0 + 1 = 1
```

The only character remains, which is correct.

Consider:

```
ab
```

The only mirrored pair is `(a,b)`, which is different.

The algorithm counts one mismatch:

```
bad = 1
answer = 2
```

Neither character can ever be removed, so the result is correct.

Consider:

```
aabaa
```

Both mirrored pairs match and can be deleted. The center character has no partner.

The algorithm computes:

```
bad = 0
answer = 1
```

which matches the optimal sequence of deletions.

Consider:

```
abcde
```

Both mirrored pairs are mismatches and the center survives:

```
(a,e) -> mismatch
(b,d) -> mismatch
center = c
```

The algorithm returns:

```
2 * 2 + 1 = 5
```

No operation is possible, so the entire string remains. This confirms the correctness of the mismatch-counting interpretation.
