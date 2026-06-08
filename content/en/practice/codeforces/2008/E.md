---
title: "CF 2008E - Alternating String"
description: "We are given a string of lowercase letters. An alternating string has a very specific form. All characters at even indices must be identical, all characters at odd indices must be identical, and the final length must be even."
date: "2026-06-08T13:26:54+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 2008
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 970 (Div. 3)"
rating: 1500
weight: 2008
solve_time_s: 124
verified: true
draft: false
---

[CF 2008E - Alternating String](https://codeforces.com/problemset/problem/2008/E)

**Rating:** 1500  
**Tags:** brute force, data structures, dp, greedy, implementation, strings  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of lowercase letters. An alternating string has a very specific form.

All characters at even indices must be identical, all characters at odd indices must be identical, and the final length must be even.

The two parity groups may use the same letter or different letters. For example, `"aaaa"` is alternating because every even position contains `'a'` and every odd position also contains `'a'`.

We may perform any number of replacements, where a character is changed into any other letter. In addition, we may delete at most one character from the string. The goal is to minimize the total number of operations.

The input contains up to $10^4$ test cases, and the sum of all string lengths is at most $2 \cdot 10^5$. This aggregate bound is the real constraint. Any solution that is quadratic in the length of a test case would become far too slow on a string of length $2 \cdot 10^5$. We need something around $O(n \cdot 26)$ or $O(n \log n)$ per test case, since the alphabet size is only 26.

Several edge cases are easy to mishandle.

Consider a single-character string:

```
1
a
```

The answer is 1. We must delete the only character, producing the empty string, which is an alternating string of even length. A solution that assumes the final string must be non-empty would fail.

Consider:

```
3
abc
```

The length is odd. One deletion is mandatory because the final length must be even. A solution that only counts replacements without considering deletion would incorrectly return 2, while the correct answer is 1.

Another subtle case is:

```
5
ababa
```

Deleting the first character gives `"baba"`, which is already alternating. The answer is 1. A greedy strategy that always deletes the character causing the most mismatches can easily miss this.

The hardest pitfall comes from parity shifts after deletion. In

```
5
aabaa
```

deleting the middle character changes the parity of every character to its right. Treating the left and right parts independently without accounting for this shift produces incorrect frequency counts.

## Approaches

Let us first imagine the brute-force solution.

If the length is even, the target string must have the same length. We choose a letter for even positions and a letter for odd positions. There are only $26^2 = 676$ possibilities. For each pair, we count how many positions already match and how many replacements are needed.

If the length is odd, exactly one deletion must occur. We could try every deletion position. After deleting a character, we again try all 676 parity-letter pairs and compute the replacement cost.

The brute-force idea is completely correct. The difficulty is speed. For a string of length $n$, trying all deletion positions and scanning the whole string each time costs $O(n^2)$. With $n = 2 \cdot 10^5$, this is hopeless.

The key observation is that an alternating string only cares about parity classes. For an even-length string, once we choose the letter used on even positions and the letter used on odd positions, every position becomes independent.

Suppose the string length is already even. Let:

- `even[c]` be the number of occurrences of letter `c` on even positions.
- `odd[c]` be the number of occurrences of letter `c` on odd positions.

If we choose letter `x` for even positions and letter `y` for odd positions, then the number of positions already correct is:

$$even[x] + odd[y]$$

To maximize preserved characters, we simply choose the most frequent letter on even positions and the most frequent letter on odd positions. The minimum replacements become:

$$n - \max(even) - \max(odd)$$

The odd-length case is more interesting.

After deleting position $i$, characters before $i$ keep their parity, while characters after $i$ switch parity because everything shifts left by one position.

This suggests maintaining frequency counts on both sides of the deletion point.

Let:

- `pref_even`, `pref_odd` count letters before the deletion.
- `suf_even`, `suf_odd` count letters from the current position onward.

When we delete position $i$:

- characters before $i$ contribute normally;
- characters after $i$ swap parity classes.

For each letter, we can compute how many times it would appear in the new even positions and new odd positions after deletion.

Then the best alternating target again keeps the most common letter in each parity class.

Because the alphabet size is only 26, evaluating one deletion position costs $O(26)$. Scanning all positions costs $O(26n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \cdot 26^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n \cdot 26)$ | $O(26)$ | Accepted |

## Algorithm Walkthrough

### Even-length strings

1. Count the frequency of every letter on even positions.
2. Count the frequency of every letter on odd positions.
3. Choose the most frequent even-position letter and the most frequent odd-position letter.
4. The number of preserved characters equals the sum of those two maxima.
5. The answer is `n - preserved`.

The target alternating string is completely determined by one letter for each parity class, so maximizing preserved characters independently for each parity is optimal.

### Odd-length strings

1. Build frequency tables `suf_even` and `suf_odd` for the entire string.
2. Initialize empty prefix tables `pref_even` and `pref_odd`.
3. Iterate over every position `i` as the deletion candidate.
4. Remove `s[i]` from the appropriate suffix table, since this character is being deleted.
5. For every letter `c`, compute its frequency in the resulting even positions:

$$pref\_even[c] + suf\_odd[c]$$

Characters after the deletion switch parity.

1. For every letter `c`, compute its frequency in the resulting odd positions:

$$pref\_odd[c] + suf\_even[c]$$

1. Let `best_even` and `best_odd` be the largest values from those arrays.
2. The resulting string length is `n - 1`. The number of replacements needed is:

$$(n-1) - best\_even - best\_odd$$

1. Add one more operation for the deletion itself.
2. Keep the minimum answer over all deletion positions.
3. Move `s[i]` into the appropriate prefix table and continue.

### Why it works

For any fixed deletion position, every remaining character belongs to either the even or odd parity class of the resulting string. An alternating string only requires one chosen letter for each class. The optimal choice is always the most frequent letter in that class because every other occurrence must be replaced.

The prefix/suffix decomposition computes the exact parity classes after deletion. Characters before the deletion keep parity, while characters after the deletion swap parity. Every remaining character is counted exactly once in its new class. Since every deletion position is examined, the minimum over all positions is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        if n % 2 == 0:
            even = [0] * 26
            odd = [0] * 26

            for i, ch in enumerate(s):
                idx = ord(ch) - 97
                if i % 2 == 0:
                    even[idx] += 1
                else:
                    odd[idx] += 1

            ans = n - max(even) - max(odd)
            print(ans)
            continue

        suf_even = [0] * 26
        suf_odd = [0] * 26

        for i, ch in enumerate(s):
            idx = ord(ch) - 97
            if i % 2 == 0:
                suf_even[idx] += 1
            else:
                suf_odd[idx] += 1

        pref_even = [0] * 26
        pref_odd = [0] * 26

        ans = n

        for i, ch in enumerate(s):
            idx = ord(ch) - 97

            if i % 2 == 0:
                suf_even[idx] -= 1
            else:
                suf_odd[idx] -= 1

            best_even = 0
            best_odd = 0

            for c in range(26):
                best_even = max(
                    best_even,
                    pref_even[c] + suf_odd[c]
                )
                best_odd = max(
                    best_odd,
                    pref_odd[c] + suf_even[c]
                )

            replacements = (n - 1) - best_even - best_odd
            ans = min(ans, replacements + 1)

            if i % 2 == 0:
                pref_even[idx] += 1
            else:
                pref_odd[idx] += 1

        print(ans)

solve()
```

The even-length branch is straightforward. We count frequencies separately on both parity classes and keep the most common letter in each.

The odd-length branch maintains four frequency arrays. The suffix arrays initially contain counts from the entire string. As we sweep left to right, the current character is removed from the suffix side because it is treated as deleted.

The formulas

```
pref_even[c] + suf_odd[c]
pref_odd[c] + suf_even[c]
```

encode the parity swap after deletion. This is the core detail of the solution. Forgetting the swap is the most common mistake.

The answer for a deletion position consists of two parts. First we count replacements needed in the resulting string of length `n - 1`. Then we add one operation for the deletion itself.

## Worked Examples

### Example 1

Input:

```
5
ababa
```

| i | Deleted | best_even | best_odd | Replacements | Total |
| --- | --- | --- | --- | --- | --- |
| 0 | a | 2 | 2 | 0 | 1 |
| 1 | b | 2 | 1 | 1 | 2 |
| 2 | a | 2 | 2 | 0 | 1 |
| 3 | b | 2 | 1 | 1 | 2 |
| 4 | a | 2 | 2 | 0 | 1 |

The minimum total is 1. Deleting any `'a'` leaves an alternating string immediately.

### Example 2

Input:

```
6
acdada
```

Even positions contain:

```
a d d
```

Odd positions contain:

```
c a a
```

| Parity | Frequencies | Maximum |
| --- | --- | --- |
| Even | a:1, d:2 | 2 |
| Odd | a:2, c:1 | 2 |

The number of preserved characters is:

$$2 + 2 = 4$$

The answer is:

$$6 - 4 = 2$$

Two replacements are sufficient, matching the sample.

This example demonstrates that when the length is already even, deletion is never useful because deleting would make the length odd and violate the definition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 26)$ | Each position is processed once, and odd-length cases evaluate 26 letters |
| Space | $O(26)$ | Only constant-sized frequency arrays are stored |

Since the total length across all test cases is at most $2 \cdot 10^5$, the algorithm performs roughly $26 \cdot 2 \cdot 10^5$ elementary operations, which easily fits within the time limit. The memory usage is constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    out = []

    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        if n % 2 == 0:
            even = [0] * 26
            odd = [0] * 26

            for i, ch in enumerate(s):
                idx = ord(ch) - 97
                if i % 2 == 0:
                    even[idx] += 1
                else:
                    odd[idx] += 1

            out.append(str(n - max(even) - max(odd)))
            continue

        suf_even = [0] * 26
        suf_odd = [0] * 26

        for i, ch in enumerate(s):
            idx = ord(ch) - 97
            if i % 2 == 0:
                suf_even[idx] += 1
            else:
                suf_odd[idx] += 1

        pref_even = [0] * 26
        pref_odd = [0] * 26

        ans = n

        for i, ch in enumerate(s):
            idx = ord(ch) - 97

            if i % 2 == 0:
                suf_even[idx] -= 1
            else:
                suf_odd[idx] -= 1

            be = 0
            bo = 0

            for c in range(26):
                be = max(be, pref_even[c] + suf_odd[c])
                bo = max(bo, pref_odd[c] + suf_even[c])

            ans = min(ans, (n - 1) - be - bo + 1)

            if i % 2 == 0:
                pref_even[idx] += 1
            else:
                pref_odd[idx] += 1

        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run("""10
1
a
2
ca
3
aab
5
ababa
6
acdada
9
ejibmyyju
6
bbccbc
6
abacba
5
bcbca
5
dcbdb
""") == """1
0
1
1
2
6
2
3
1
1"""

# minimum size
assert run("""1
1
a
""") == "1"

# already alternating even length
assert run("""1
4
abab
""") == "0"

# all equal odd length
assert run("""1
5
aaaaa
""") == "1"

# parity shift after deletion
assert run("""1
5
ababa
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, "a"` | `1` | Empty string after deletion |
| `n=4, "abab"` | `0` | Already alternating |
| `n=5, "aaaaa"` | `1` | Deletion only, no replacements |
| `n=5, "ababa"` | `1` | Correct handling of parity shifts |

## Edge Cases

Consider:

```
1
a
```

The string length is odd. Deleting the only character leaves a string of length 0. During the sweep, the only deletion candidate yields `best_even = best_odd = 0`. The replacement cost is 0, and adding the deletion operation gives 1. The algorithm correctly returns 1.

Consider:

```
3
abc
```

Deleting any character produces a string of length 2. The algorithm evaluates all three deletion positions and computes the best parity frequencies after the parity shift. The minimum total cost is 1, achieved by deleting `'b'` to obtain `"ac"`, which is already alternating.

Consider:

```
5
ababa
```

When deleting index 0, all remaining characters shift parity. The formula

$$pref\_even + suf\_odd$$

correctly moves the right side into the opposite parity class. The resulting counts show that all four remaining characters already match an alternating pattern, giving answer 1.

Consider:

```
5
aabaa
```

Deleting the middle character causes every character on the right to swap parity. A naive frequency computation that ignores this shift would count letters in the wrong class and overestimate the number of replacements. The prefix/suffix formulation explicitly performs the swap and produces the correct minimum cost.
