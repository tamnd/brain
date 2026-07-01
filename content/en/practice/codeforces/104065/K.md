---
title: "CF 104065K - Pattern Matching in A Minor ``Low Space''"
description: "We are given two strings: a pattern string s and a text string t. The task is to count how many starting positions in t produce an occurrence of s as a contiguous substring. Overlaps are allowed, so every valid match contributes to the answer independently."
date: "2026-07-02T03:20:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104065
codeforces_index: "K"
codeforces_contest_name: "2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite"
rating: 0
weight: 104065
solve_time_s: 49
verified: true
draft: false
---

[CF 104065K - Pattern Matching in A Minor ``Low Space''](https://codeforces.com/problemset/problem/104065/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings: a pattern string `s` and a text string `t`. The task is to count how many starting positions in `t` produce an occurrence of `s` as a contiguous substring. Overlaps are allowed, so every valid match contributes to the answer independently.

A direct way to view this is that we slide `s` across every possible alignment in `t` and check whether all characters match. The output is the total number of alignments that match completely.

The constraints are extreme: both strings can be as long as $10^7$. That rules out any solution that compares characters repeatedly in a nested way. Even a linear scan per alignment would imply up to $10^{14}$ character comparisons in the worst case, which is far beyond feasible.

Memory is also tight in spirit, even though the nominal limit is large. The note about sequential access and the “low space” framing suggests that we should avoid storing large auxiliary structures like full prefix-function tables for very large concatenations or multi-pass preprocessing that requires random access patterns.

A subtle edge case comes from highly repetitive strings. If `s = "aaaaa"` and `t = "aaaaaaaaaa"`, every alignment is valid in overlapping fashion. A naive mismatch-early-exit strategy may still degrade to quadratic behavior because mismatches are rare and comparisons repeatedly restart.

Another edge case is when `s` has length 1. Then every character in `t` is an independent match check, and the answer is simply the frequency of that character. This often exposes off-by-one errors in sliding implementations.

## Approaches

The brute-force idea is straightforward. For every position `i` in `t` from `0` to `m - n`, we compare `s` with the substring `t[i:i+n]` character by character. If all characters match, we increment the answer.

This is correct because it directly enforces the definition of substring equality. The failure mode is performance. Each alignment may require up to `n` comparisons, and there are `m - n + 1` alignments, giving a worst-case complexity of $O(nm)$. With both up to $10^7$, this becomes completely infeasible.

The key observation is that we do not need to re-compare characters from scratch at every shift. The structure of repeated prefix information in the pattern allows us to reuse partial matches. When a mismatch happens, we want to know how far we can “fall back” in the pattern without restarting from zero.

This is exactly what the prefix-function from the Knuth-Morris-Pratt algorithm captures. It encodes the longest proper prefix of `s` that is also a suffix for every prefix of `s`. With this information, we can scan `t` once and maintain how many characters of `s` we have currently matched. Each character in `t` causes at most a constant number of pointer adjustments in `s`.

The memory concern is addressed because the prefix array is size `n`, which is acceptable, and the scan is purely sequential.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| KMP | $O(n + m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We use KMP to count pattern occurrences in a single pass over the text.

### Steps

1. Compute the prefix function `pi` for string `s`.

For each position `i`, `pi[i]` stores the longest proper prefix of `s[:i+1]` that is also a suffix of this substring. This structure tells us how far we can continue matching after a mismatch without restarting from zero.
2. Initialize a pointer `j = 0`, representing how many characters of `s` are currently matched against `t`.
3. Scan the text `t` from left to right using index `i`. For each character `t[i]`, attempt to extend the current match.
4. If `t[i] != s[j]`, repeatedly fall back using `j = pi[j-1]` until either `j == 0` or a match is found.

This ensures we always keep the longest valid partial match instead of restarting from scratch.
5. If `t[i] == s[j]`, increment `j` by 1, extending the matched prefix.
6. If `j == n`, a full match of `s` ends at position `i`. Increment the answer and reset `j = pi[j-1]` to allow overlapping matches.

### Why it works

At every position in `t`, the variable `j` represents the length of the longest prefix of `s` that matches a suffix of the processed prefix of `t`. The prefix-function guarantees that after a mismatch, any shorter prefix that could still match is already encoded in `pi`, so we never miss a valid alignment. Every full match is detected exactly once at the moment `j` reaches `n`, ensuring correctness without duplication or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_pi(s):
    n = len(s)
    pi = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def solve():
    n, m = map(int, input().split())
    s = input().strip()
    t = input().strip()

    pi = build_pi(s)

    j = 0
    ans = 0

    for ch in t:
        while j > 0 and ch != s[j]:
            j = pi[j - 1]
        if ch == s[j]:
            j += 1
        if j == n:
            ans += 1
            j = pi[j - 1]

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation splits naturally into prefix-function construction and the streaming match phase. The prefix array is built once over `s`, and then reused during the scan of `t`.

The main scan maintains only two variables, the current index in `s` and the answer counter. The fallback loop is essential: it ensures that mismatches do not cause us to restart unnecessarily.

A common pitfall is forgetting to reset `j` after finding a match. Without `j = pi[j - 1]`, overlapping matches are lost. Another issue is indexing: `s[j]` is only valid when `j < n`, so the equality check must occur before accessing beyond bounds, which is ensured by checking `j == n` immediately after increment.

## Worked Examples

### Example 1

Input:

```
s = "aba"
t = "abababc"
```

| i | t[i] | j before | action | j after | match |
| --- | --- | --- | --- | --- | --- |
| 0 | a | 0 | match | 1 | no |
| 1 | b | 1 | match | 2 | no |
| 2 | a | 2 | match → full | 3 → 1 | yes |
| 3 | b | 1 | match | 2 | no |
| 4 | a | 2 | match → full | 3 → 1 | yes |
| 5 | b | 1 | match | 2 | no |
| 6 | c | 2 | fallback then stop | 0 | no |

Answer = 2.

This trace shows overlapping matches are handled correctly via the fallback reset to `pi[j-1]`.

### Example 2

Input:

```
s = "a"
t = "abracadabra"
```

| i | t[i] | j before | action | j after | match |
| --- | --- | --- | --- | --- | --- |
| all positions | any char | 0 | compare | 1 or 0 | count when 'a' |

Every `'a'` increments the answer immediately since `n = 1`.

Answer = 5.

This confirms the algorithm naturally reduces to character counting in the single-character pattern case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | prefix-function construction is linear in `n`, and each character in `t` is processed with amortized constant fallback steps |
| Space | $O(n)$ | prefix array stores one integer per position in `s` |

The constraints allow up to $10^7$ total input sizes, so a linear-time streaming algorithm with a single pass over `t` fits comfortably, provided implementation avoids heavy overhead operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# We redefine solve-safe runner
def run(inp: str) -> str:
    import sys, io
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = backup_stdin
        sys.stdout = backup_stdout

# provided samples
assert run("3 7\naba\nabababc\n") == "2"
assert run("1 11\na\nabracadabra\n") == "5"

# custom cases
assert run("1 5\na\naaaaa\n") == "5"
assert run("2 4\naa\naaaa\n") == "3"
assert run("3 3\nabc\nabc\n") == "1"
assert run("3 3\nabc\ndef\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single repeated char | 5 | maximal overlap handling |
| repeated prefix pattern | 3 | overlapping matches correctness |
| exact match | 1 | base correctness |
| no match | 0 | failure path |

## Edge Cases

One important edge case is when the pattern has heavy self-overlap. For example, `s = "aaaa"` and `t = "aaaaaaaa"`. During scanning, `j` repeatedly reaches 4 and resets to `pi[3] = 3`, allowing immediate continuation. This ensures every valid alignment is counted, including those that overlap almost completely.

Another case is a completely mismatching text, such as `s = "abc"` and `t = "zzz..."`. Here `j` repeatedly stays at zero, and the algorithm performs only simple comparisons without entering fallback loops, demonstrating the amortized constant behavior of KMP.

A third case is a single-character pattern. The algorithm degenerates cleanly into counting occurrences without any prefix structure, since `j` is always either 0 or 1 and `pi` is trivial.
