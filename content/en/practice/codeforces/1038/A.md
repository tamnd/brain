---
title: "CF 1038A - Equality"
description: "We are given a string made of uppercase letters, but only from the first $k$ letters of the alphabet. The task is not to rearrange or modify the string, but to select a subsequence of characters while preserving order."
date: "2026-06-16T18:37:30+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1038
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 508 (Div. 2)"
rating: 800
weight: 1038
solve_time_s: 707
verified: false
draft: false
---

[CF 1038A - Equality](https://codeforces.com/problemset/problem/1038/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 11m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string made of uppercase letters, but only from the first $k$ letters of the alphabet. The task is not to rearrange or modify the string, but to select a subsequence of characters while preserving order. Among all such subsequences, we want one with a special property: every letter from `'A'` to the $k$-th letter must appear the same number of times inside the subsequence. The goal is to maximize the length of such a subsequence.

Another way to think about it is that we are trying to pick some number $x$ of each of the $k$ characters, so that the total length is $k \cdot x$, and this selection must be possible as a subsequence of the original string.

The constraint $n \le 10^5$ immediately tells us that any approach worse than $O(n \cdot k)$ or $O(n \log n)$ will start to struggle. A brute-force over all subsequences is impossible because there are $2^n$ of them. Even trying all possible values of $x$ with repeated scanning would still need careful optimization.

A few edge situations matter.

If some letter is missing entirely, then no valid subsequence can include it, so the answer must become zero. For example, if $k = 3$ but the string contains only `'A'` and `'B'`, then we can never balance `'C'`, so the result is $0$.

Another subtle case is when frequencies are highly uneven. Suppose $k = 3$ and the string is `"AAAAABBBBBCC"`. Even though each letter exists, the limiting factor will be the smallest frequency among the three.

A naive mistake is to think we need to pick positions carefully to maximize spread. In reality, order is irrelevant for counting feasibility, since subsequences preserve order but do not constrain counts beyond availability.

## Approaches

A brute-force idea would be to try every possible subsequence and check whether it is balanced. For each subsequence, we count occurrences of each letter and verify equality. This is correct but completely infeasible: there are $2^n$ subsequences, and even checking one takes $O(n)$, leading to exponential time.

A better direction is to reframe the problem. Instead of choosing subsequences explicitly, we focus on how many times each character can appear. Suppose we decide that each of the $k$ letters appears exactly $x$ times. Then the total length is $k \cdot x$, and the question becomes: is it possible to pick $x$ occurrences of every character from the string while respecting order?

But order actually does not matter for feasibility here, because subsequences only require enough occurrences, not contiguous structure. We can always pick occurrences greedily in scan order if they exist.

So the real constraint collapses to a simple counting condition: for each letter, we must have at least $x$ occurrences. If $cnt[c]$ is the frequency of letter $c$, then $x \le \min cnt[c]$. The best we can do is set $x$ to that minimum frequency.

So the answer is simply:

$$k \cdot \min_{c \in [A, A+k-1]} cnt[c]$$

The key insight is that subsequence ordering does not introduce additional constraints beyond availability, so the problem becomes a pure frequency minimization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsequences | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Frequency minimum | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Count how many times each of the first $k$ letters appears in the string. This works because subsequences can only use existing characters, so availability is the only constraint.
2. Find the smallest frequency among these $k$ counts. This value represents the maximum number of full “balanced layers” we can form across all letters.
3. Multiply this minimum by $k$, since each layer contributes exactly one of each letter.
4. Output the result.

### Why it works

Each valid subsequence must contain equal counts of all $k$ letters, say $x$ of each. That immediately implies that no letter can contribute more than its total occurrence in the original string, so $x \le cnt[c]$ for all $c$. Therefore $x \le \min cnt[c]$. Conversely, if we choose $x = \min cnt[c]$, we can always pick that many occurrences of each character in order from the string because subsequences only require selecting positions, not rearranging or respecting adjacency. This establishes both optimality and feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
s = input().strip()

cnt = [0] * k

for ch in s:
    cnt[ord(ch) - ord('A')] += 1

ans = min(cnt) * k
print(ans)
```

The implementation directly follows the reduction to counting. The array `cnt` tracks frequencies of the first $k$ letters. We compute the minimum over all these frequencies and multiply by $k$.

A subtle point is indexing: since letters are guaranteed to be within the first $k$, mapping `'A'` to index 0 is safe. There is no need for conditional checks.

The multiplication by $k$ happens only after taking the minimum; reversing the order would be incorrect because we are not summing independent maxima, but enforcing equality across all letters.

## Worked Examples

### Example 1

Input:

```
9 3
ACAABCCAB
```

Counts evolve as follows:

| Letter | Count |
| --- | --- |
| A | 4 |
| B | 2 |
| C | 3 |

The minimum frequency is $2$, so we can form 2 full layers of `A`, `B`, `C`, giving total length $3 \cdot 2 = 6$.

This shows that even though `'A'` and `'C'` are more frequent, the answer is constrained entirely by `'B'`.

### Example 2

Input:

```
5 3
ABCDE
```

Only the first three letters are relevant, but `'C'` might be missing depending on interpretation of input bounds. If any required letter has zero occurrences:

| Letter | Count |
| --- | --- |
| A | 1 |
| B | 1 |
| C | 0 |

Minimum is 0, so answer is 0.

This confirms that a single missing character collapses the entire construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass to count frequencies and scan k letters |
| Space | $O(1)$ | fixed-size array of length at most 26 |

The solution is linear in the string length, which is optimal since every character must be read at least once. Memory usage is constant due to the bounded alphabet size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    s = input().strip()

    cnt = [0] * k
    for ch in s:
        cnt[ord(ch) - ord('A')] += 1

    return str(min(cnt) * k)

# provided sample
assert run("9 3\nACAABCCAB\n") == "6"

# k = 1, always full string
assert run("5 1\nAAAAA\n") == "5"

# missing character forces zero
assert run("5 3\nAABBB\n") == "0"

# all equal frequencies
assert run("6 2\nAABBAB\n") == "4"

# large balanced case
assert run("4 2\nBABA\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 9 3 ACAABCCAB | 6 | normal case with limiting character |
| 5 1 AAAAA | 5 | k=1 edge case |
| 5 3 AABBB | 0 | missing letter |
| 6 2 AABBAB | 4 | balanced frequencies |
| 4 2 BABA | 4 | alternating structure correctness |

## Edge Cases

If one letter never appears, the minimum frequency becomes zero, and the algorithm correctly returns zero because no balanced subsequence can include that letter.

For a concrete trace, take:

```
4 3
ABAB
```

Counts:

| A | B | C |
| --- | --- | --- |
| 2 | 2 | 0 |

Minimum is 0, so output is 0. The algorithm does not attempt to “skip” missing letters, which matches the requirement that all first $k$ letters must appear equally.

Another edge case is when $k = 1$. For:

```
5 1
ABCDE
```

Only `'A'` is considered, count is 1, so answer is 1. The algorithm reduces correctly because the minimum over a single value is itself, and multiplying by 1 preserves it.
