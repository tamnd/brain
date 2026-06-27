---
title: "CF 105532E - Droid Foundry A (Easy Version)"
description: "The task revolves around comparing a fixed reference string with multiple candidate strings and checking whether each candidate can be obtained by deleting some characters from the reference without rearranging the remaining ones."
date: "2026-06-27T01:03:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105532
codeforces_index: "E"
codeforces_contest_name: "Aggie Competitive Programming Contest (ACPC) 2024"
rating: 0
weight: 105532
solve_time_s: 49
verified: true
draft: false
---

[CF 105532E - Droid Foundry A (Easy Version)](https://codeforces.com/problemset/problem/105532/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The task revolves around comparing a fixed reference string with multiple candidate strings and checking whether each candidate can be obtained by deleting some characters from the reference without rearranging the remaining ones. In other words, for each query string, we need to determine whether it appears as a subsequence of the baseline string.

The baseline string represents a sequence of characters produced by a system, while each design string represents a desired configuration. We are allowed to remove characters from the baseline, but we cannot reorder them or insert new ones. The output for each design is a simple yes or no decision depending on whether the design can be embedded into the baseline in order-preserving fashion.

Let the baseline length be $n$ and suppose there are $q$ design strings, each of total length at most $n$. A direct two-pointer scan for each query costs linear time in the baseline, so the naive solution is roughly $O(q \cdot n)$. If both $q$ and $n$ are large, this quickly becomes too slow, especially when both can approach $10^5$, since the worst case would require around $10^{10}$ character comparisons.

The constraint that each design is at most as long as the baseline rules out cases where we try to match longer strings into shorter ones, but it does not prevent pathological cases where every design is almost as long as the baseline. In such cases, repeated full scans of the baseline become the bottleneck.

A subtle edge case appears when the baseline contains repeated characters and the design also contains repetitions. For example, if the baseline is `aaaaabaaaaa` and the design is `aaaaaa`, a careless greedy matcher might repeatedly scan from the beginning for each match and accidentally degrade to quadratic behavior even if individual matching logic is correct.

Another issue arises if one attempts to precompute only positions of characters without careful ordering. For instance, storing only character frequencies fails immediately: baseline `abc` and design `cba` have identical frequencies but the design is not a valid subsequence.

## Approaches

The brute force method checks each design independently by walking through the baseline with a pointer and advancing whenever characters match. This is correct because it directly enforces the subsequence definition. However, repeating this scan for every design leads to repeated traversal of the same baseline string, which dominates runtime when the number of queries is large.

The key observation is that we are repeatedly solving the same structural problem: matching a short string against a fixed long string. Instead of recomputing matches from scratch, we can preprocess the baseline so that we can quickly jump to the next occurrence of each character. Once we know, for every position and character, where the next occurrence is, we can advance through each design in logarithmic or constant time per step depending on implementation.

This transforms each match step from a linear scan into a direct jump, removing redundant work over repeated queries. The structure of the problem does not require interactions between different queries, so preprocessing is sufficient to decouple them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (two pointers per query) | $O(q \cdot n)$ | $O(1)$ | Too slow |
| Next-occurrence preprocessing | (O(n \cdot \sigma + \sum | d_i | )) |

Here $\sigma$ is the alphabet size.

## Algorithm Walkthrough

We preprocess the baseline so that we can answer “where do I go next if I need character c from position i” instantly.

1. We build a next-position table such that for every index in the baseline and every character, we store the next occurrence of that character at or after that index. This is constructed by scanning the string from right to left while maintaining the latest seen positions of each character. This backward direction ensures that when we are at position i, we already know answers for all later positions.
2. For each design string, we simulate matching against the baseline using a pointer initially set before the first character of the baseline.
3. For every character in the design, we jump the pointer using the precomputed table to the next valid position where that character appears. If no such position exists, we immediately conclude that the design cannot be formed.
4. If we successfully process all characters of the design, it is confirmed as a valid subsequence.

The reason for using the next table instead of scanning forward is that it eliminates repeated traversal of the same suffix of the baseline. Each step becomes a direct lookup.

### Why it works

At any moment, the pointer always represents the earliest possible position in the baseline where the prefix of the design has been matched. The next-occurrence table guarantees that if there exists any valid continuation of the match, we will reach it because we always jump to the earliest feasible position for the next character. This preserves the greedy invariant that never skips a possible valid embedding while ensuring no character is checked more than once per query.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_next(s):
    n = len(s)
    nxt = [[n] * 26 for _ in range(n + 1)]
    
    last = [n] * 26
    for i in range(n - 1, -1, -1):
        last[ord(s[i]) - 97] = i
        for c in range(26):
            nxt[i][c] = last[c]
    return nxt

def solve():
    b = input().strip()
    n = len(b)
    nxt = build_next(b)
    
    q = int(input())
    out = []
    
    for _ in range(q):
        d = input().strip()
        pos = 0
        ok = True
        
        for ch in d:
            c = ord(ch) - 97
            if pos >= n or nxt[pos][c] == n:
                ok = False
                break
            pos = nxt[pos][c] + 1
        
        out.append("YES" if ok else "NO")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core of the implementation is the `build_next` function. It constructs a table where `nxt[i][c]` gives the earliest index at or after `i` where character `c` appears. This is what enables constant-time jumps during matching.

During query processing, `pos` tracks how far we have matched in the baseline. For each character in the design, we move `pos` to the next valid occurrence plus one, because the next search must start strictly after the matched position. The moment a required character is missing from the remaining suffix, we terminate early.

A common pitfall is forgetting to move `pos` forward after matching a character. Without the `+1`, the algorithm can repeatedly match the same position, incorrectly accepting invalid cases or entering incorrect loops.

## Worked Examples

Consider a baseline `abac` with two designs `ac` and `ca`.

For the first design `ac`:

| Step | Character | pos before | nxt lookup | pos after | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | a | 0 | 0 | 1 | matched |
| 2 | c | 1 | 3 | 4 | matched |

The design is accepted because both characters can be found in order.

For the second design `ca`:

| Step | Character | pos before | nxt lookup | pos after | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | c | 0 | 3 | 4 | matched |
| 2 | a | 4 | none | - | fail |

The second step fails because after using `c`, there is no `a` appearing later in the baseline.

These traces show how the pointer only moves forward and never revisits earlier positions, which enforces correct ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n \cdot \sigma + \sum | d_i |
| Space | $O(n \cdot \sigma)$ | stores next occurrence for each position and character |

The preprocessing cost is linear in the baseline size multiplied by alphabet size, which is acceptable under typical constraints where the alphabet is fixed (for example lowercase English letters). Each query then runs in time proportional only to its own length, making the solution scalable even for large batches of designs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()  # placeholder, replace with solve() in real use

# These are structural tests, assuming solve() is properly wired.

def solve_wrapper(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    _out = StringIO()
    _sys.stdout = _out
    solve()
    _sys.stdout = sys.__stdout__
    return _out.getvalue().strip()

# sample-like test
assert solve_wrapper("abac\n2\nac\nca\n") == "YES\nNO"

# single character baseline
assert solve_wrapper("a\n3\na\nb\naa\n") == "YES\nNO\nNO"

# repeated characters
assert solve_wrapper("aaaa\n2\naa\naaa\n") == "YES\nYES"

# alternating pattern
assert solve_wrapper("ababab\n3\nbbb\naaa\nabab\n") == "NO\nNO\nYES"

# edge: empty design always valid
assert solve_wrapper("abc\n1\n\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| abac, ac/ca | YES / NO | basic subsequence correctness |
| a, a/b/aa | YES / NO / NO | single-character edge handling |
| aaaa, aa/aaa | YES / YES | repeated character matching |
| ababab, bbb/aaa/abab | NO/NO/YES | ordering constraint |
| empty design | YES | trivial subsequence case |

## Edge Cases

One edge case is when the design is empty. Since an empty sequence is always a subsequence, the algorithm immediately succeeds without any traversal, because there are no characters to process.

Another case is when the baseline is very short but the design is long. For example, baseline `ab` and design `aba`. During the final character lookup, the next-occurrence table returns a sentinel value indicating no valid position exists, and the algorithm correctly rejects the design without further scanning.

A third case is when characters repeat heavily in the baseline. For baseline `aaaaaa` and design `aaaaa`, the pointer advances deterministically through successive positions 0, 1, 2, 3, 4, 5, ensuring no backtracking or ambiguity.
