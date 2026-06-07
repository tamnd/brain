---
title: "CF 2118A - Equal Subsequences"
description: "We are asked to construct a binary string of length $n$, containing exactly $k$ ones, with an additional structural constraint involving subsequences of length three. Among all triples of indices $i < j < k$, we count how many form the pattern “101” and how many form “010”."
date: "2026-06-08T04:00:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2118
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1030 (Div. 2)"
rating: 800
weight: 2118
solve_time_s: 87
verified: false
draft: false
---

[CF 2118A - Equal Subsequences](https://codeforces.com/problemset/problem/2118/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a binary string of length $n$, containing exactly $k$ ones, with an additional structural constraint involving subsequences of length three. Among all triples of indices $i < j < k$, we count how many form the pattern “101” and how many form “010”. The goal is to produce a string where these two counts are equal.

A subsequence here means we are free to skip characters, so what matters is not adjacency but relative ordering. This makes the condition sensitive to global placement of zeros and ones rather than local patterns.

The constraints are small: $n \le 100$ and $t \le 500$. This immediately tells us we do not need anything asymptotically tight beyond $O(n^2)$ per test case, and even cubic reasoning is acceptable for understanding. However, the construction problem suggests a greedy or structural pattern rather than counting explicitly.

Edge cases appear when $k = 0$, $k = n$, or when $k = 1$ or $k = n-1$. In these cases, one of the patterns is impossible because at least one of “101” or “010” requires both symbols to appear twice in alternating positions. For example, if all characters are identical, both counts are zero, so any uniform string is valid. A careless approach might try to “balance” subsequences by alternating too aggressively, but that is unnecessary and may violate the required number of ones.

Another subtle edge case is when ones are very sparse or very dense. For instance, if $k = 1$, any string with a single 1 has zero occurrences of both patterns, so any placement works. Similarly for $k = n-1$.

## Approaches

A brute-force idea would be to generate all binary strings of length $n$ with exactly $k$ ones, and for each one compute the number of “101” and “010” subsequences by iterating over all triples of indices. Counting subsequences directly takes $O(n^3)$, and there are $\binom{n}{k}$ candidate strings. Even for $n = 100$, this is astronomically large, making brute force completely infeasible.

The key observation is that the problem does not actually require controlling the exact difference between the two counts. We only need them equal. A strong structural simplification is that we can force both counts to be zero. This happens if we eliminate all alternating patterns of length three entirely.

A binary string has no “101” or “010” subsequence if and only if it never alternates twice between 0 and 1 in order. This is guaranteed if the string is monotone in blocks: all zeros followed by all ones, or all ones followed by all zeros. In such a string, any triple either contains only one symbol type or has at most one transition, so neither pattern can appear.

This reduces the task to a pure construction problem: place $k$ ones and $n-k$ zeros in a single contiguous block structure. Both “000…111…” and “111…000…” work, and both satisfy the required equality since both subsequence counts are zero.

This is the critical reduction: instead of balancing two combinatorial counts, we avoid both simultaneously.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration and counting | $O(\binom{n}{k} \cdot n^3)$ | $O(n)$ | Too slow |
| Monotone block construction | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$ and $k$. These define how many ones must appear in the final string and its total length.
2. Construct a string consisting of $k$ consecutive ‘1’ characters. This ensures the count constraint is satisfied immediately without needing later correction.
3. Append $n-k$ consecutive ‘0’ characters. This creates a single transition boundary between symbols.
4. Output the resulting string.

The choice of putting all ones first is arbitrary. Putting all zeros first is equally valid because the condition depends only on subsequences of alternating form, not on absolute ordering.

### Why it works

The constructed string has at most one transition between symbols. Any subsequence of length three that alternates between 0 and 1 would require at least two transitions in order, either 0→1→0 or 1→0→1. Since only one transition exists in the entire string, neither pattern can be formed. Therefore both counts are zero, and they are equal.

The construction also trivially enforces the exact number of ones, since we explicitly place them without rearrangement.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    # place all 1s first, then 0s
    print("1" * k + "0" * (n - k))
```

The code directly implements the monotone block construction. The only subtle point is ensuring the counts match exactly: the string length is fixed, so once $k$ ones are placed, the remaining positions must be zeros.

No further validation or computation is needed because the structure guarantees the subsequence condition automatically.

## Worked Examples

### Example 1

Input: $n = 4, k = 2$

We construct:

| Step | String state |
| --- | --- |
| Start | "" |
| Place 1s | "11" |
| Place 0s | "1100" |

The resulting string contains exactly two ones and has a single transition from 1 to 0, so no alternating subsequence of length three exists. Therefore counts of “101” and “010” are both zero.

### Example 2

Input: $n = 5, k = 3$

| Step | String state |
| --- | --- |
| Start | "" |
| Place 1s | "111" |
| Place 0s | "11100" |

This again creates only one boundary between symbols. Any triple either lies fully inside one block or crosses the boundary once, never twice, so neither forbidden subsequence appears.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | We construct a string of length $n$ directly |
| Space | $O(1)$ extra | Only the output string is stored |

The total work across all test cases is at most $500 \cdot 100$, which is negligible under the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        out.append("1" * k + "0" * (n - k))
    return "\n".join(out) + "\n"

# provided samples
assert run("""5
4 2
5 3
5 5
6 2
1 1
""") == """1100
11100
11111
110000
1
"""

# custom cases
assert run("""3
1 0
1 1
2 1
""") == """0
1
10
"""

assert run("""2
6 0
6 6
""") == """000000
111111
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element cases | 0 / 1 | minimal boundary correctness |
| all zeros / all ones | uniform strings | extreme density correctness |
| mixed small n | 10 | simplest non-trivial structure |

## Edge Cases

When $k = 0$, the algorithm outputs $n$ zeros. There are no ones, so both “101” and “010” subsequences are impossible. The construction produces an empty one-block followed by zeros, which still satisfies the invariant of at most one transition.

When $k = n$, the output is $n$ ones. Again, no zeros exist, so both subsequence counts are zero. The structure degenerates to a single block with no transitions.

When $k = 1$, the string is “1000…0”. Any subsequence of length three cannot alternate because there is only one occurrence of 1, so both patterns are absent. The same reasoning applies symmetrically for $k = n-1$.
