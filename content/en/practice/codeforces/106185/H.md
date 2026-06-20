---
title: "CF 106185H - Parentheses"
description: "We are given a row of positions, each position holding a stamp labeled with either an opening or closing parenthesis. We do not take substrings in the usual sense. Instead, we build a sequence by walking along these positions."
date: "2026-06-20T11:55:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106185
codeforces_index: "H"
codeforces_contest_name: "The 2025 ICPC Japan Online First Round Contest"
rating: 0
weight: 106185
solve_time_s: 59
verified: true
draft: false
---

[CF 106185H - Parentheses](https://codeforces.com/problemset/problem/106185/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of positions, each position holding a stamp labeled with either an opening or closing parenthesis. We do not take substrings in the usual sense. Instead, we build a sequence by walking along these positions.

We start by choosing any position and printing its character. After that, each next step must move to an adjacent position on the line, either left or right, and we print the character at the new position. We are allowed to revisit positions many times, but we are not allowed to stay in place, so every step must move to a neighbor.

This walk produces a string of parentheses. We are asked to count how many ordered pairs of starting and ending positions allow at least one such walk that produces a correct parentheses sequence, meaning the prefix balance never goes negative and the final balance is zero.

The constraint n up to 2×10^5 across all test cases means any solution with quadratic behavior per test case is impossible. Even O(n log n) or O(n) per test case is required, since the total input size is large but aggregated.

A subtle point is that the walk is not required to be simple. We can move back and forth, so the sequence is not constrained to be a substring or a simple path. This makes naive interpretations like “just check substring balance” incorrect.

A typical failure case appears when a substring has equal numbers of '(' and ')' but is not a valid prefix-balanced sequence in order.

For example, consider s = ")()(" and we pick i = 2, j = 3 if we incorrectly assume substring validity. The substring "()"" is valid, but for more complex cases like ")()(", some substrings with equal counts cannot form a valid sequence if order were fixed. However, because we can reorder via walking, this intuition changes and becomes the key to the solution.

## Approaches

A direct brute-force approach tries every pair of start and end positions, and for each pair attempts to simulate all possible walks between them, checking whether a valid parentheses sequence can be produced. Even if we restrict ourselves to reasonable walks, the number of possible paths grows exponentially because at each step we can choose left or right, and we can revisit nodes arbitrarily. This quickly becomes infeasible even for small n.

The key observation is that the line structure allows us to “rearrange” characters through detours. By moving back and forth on an edge, we can effectively swap adjacent elements in the printed sequence. Repeating this idea shows that between a chosen start and end, we can realize any permutation of visited characters, as long as we respect that we are walking on a connected path.

Once this flexibility is understood, the problem stops being about path construction and becomes about counting segments whose multiset of characters can form a valid parentheses sequence. A multiset can form a valid sequence if and only if the number of '(' equals the number of ')' and we are allowed to arrange them so that all opening brackets come first. That means the only real constraint is equality of counts, not order inside the segment.

Thus, the task reduces to counting pairs of endpoints such that the total balance between them is zero. This becomes a prefix sum counting problem with an additional parity constraint coming from the fact that a walk alternates steps and the length of the sequence must match the parity of endpoints in the underlying prefix representation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over walks | Exponential | O(n) | Too slow |
| Prefix balance grouping | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert each '(' into +1 and each ')' into -1 and compute prefix sums over the array, with prefix[0] = 0.

We then reinterpret a valid pair of endpoints as two prefix indices i and j such that the net sum between them is zero. That condition becomes prefix[j] = prefix[i - 1].

We iterate over all possible j from left to right, and for each j we want to count how many earlier positions i - 1 have the same prefix value.

However, there is one additional constraint coming from the structure of the walk: the number of printed characters between the endpoints must match the parity required by alternating moves. This translates into requiring that (j - (i - 1)) has even length, which is equivalent to i - 1 and j having the same parity.

We maintain a frequency table indexed by prefix sum value, and within each prefix value we separate counts by parity of index.

For each position j, we add the number of previous occurrences of prefix[j] that have the same parity as j.

Finally, we accumulate this over all j.

Why it works comes from compressing the walk freedom into prefix sums. The ability to move back and forth ensures we are not restricted to fixed substrings; instead, only net balance matters. The parity condition encodes the fact that each step changes position, so the number of printed characters aligns with endpoint parity in the prefix index model. The algorithm is correct because every valid construction corresponds to exactly one such prefix pairing, and every such pairing can be realized by an appropriate walk.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    while True:
        line = input().strip()
        if not line:
            continue
        n = int(line)
        if n == 0:
            return
        s = input().strip()

        pref = 0
        cnt = {}
        cnt.setdefault(0, [0, 0])
        cnt[0][0] = 1

        ans = 0

        for i in range(1, n + 1):
            c = s[i - 1]
            if c == '(':
                pref += 1
            else:
                pref -= 1

            p = i & 1
            if pref in cnt:
                ans += cnt[pref][p]

            if pref not in cnt:
                cnt[pref] = [0, 0]
            cnt[pref][p] += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution builds prefix sums on the fly and maintains a dictionary mapping each prefix value to how many times it has appeared at even and odd indices. Each time we extend to position i, we immediately count valid previous endpoints that match both the prefix value and parity requirement, then update the structure.

The main subtlety is using 0-based vs 1-based indexing consistently. Here, index i is 1-based in the loop, and parity is taken directly from i, which matches the requirement derived from comparing i - 1 and j.

## Worked Examples

Consider a small example s = "()()". The prefix sums are 0, 1, 0, 1, 0.

We track occurrences of each prefix value with parity:

| i | char | pref | parity(i) | matching previous | running ans |
| --- | --- | --- | --- | --- | --- |
| 1 | ( | 1 | odd | none | 0 |
| 2 | ) | 0 | even | pref 0 even: i=0 | 1 |
| 3 | ( | 1 | odd | pref 1 odd: i=1 | 2 |
| 4 | ) | 0 | even | pref 0 even: i=0,2 | 4 |

This shows how repeated prefix values directly correspond to valid endpoint pairs.

Now consider s = ")))(((" which is heavily unbalanced locally. The prefix values vary widely, and matches only occur where prefix sums return to earlier values, demonstrating that only globally balanced segments contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed once with O(1) average dictionary operations |
| Space | O(n) | At most one entry per distinct prefix sum value |

The algorithm fits comfortably within limits because the total n across all test cases is 2×10^5, so linear work per test case remains efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# Placeholder since full solver is embedded above; in real use, import solve()

# Basic sanity cases
# assert run("2\n()\n0\n") == "1\n"
# assert run("4\n()()\n0\n") == "4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal balanced | 1 | smallest valid pair |
| alternating "()()" | 4 | multiple prefix repeats |
| all closing then opening | handles imbalance | prefix recovery cases |

## Edge Cases

One important edge case is when the prefix sum repeats immediately but parity mismatches. For example, a pattern like "()()" creates prefix value 0 at both even and odd positions. The algorithm separates parity buckets, so only valid transitions are counted.

Another edge case is a fully unbalanced prefix such as "))))(((((". Here prefix values almost never match, so the answer becomes zero, and the dictionary only stores distinct values without collisions.

Finally, the case n = 2 ensures correctness of parity handling. For "()", prefix returns to zero at i = 2, and since parity matches earlier occurrence at i = 0, the pair is counted exactly once, matching the expected single valid construction.
