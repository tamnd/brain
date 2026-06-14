---
title: "CF 1546B - AquaMoon and Stolen String"
description: "We are given a multiset of original strings and a second multiset formed after a disturbance process. The disturbance worked in two stages. First, all strings were paired except one special string that stayed unpaired."
date: "2026-06-14T19:40:57+07:00"
tags: ["codeforces", "competitive-programming", "interactive", "math"]
categories: ["algorithms"]
codeforces_contest: 1546
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 732 (Div. 2)"
rating: 1200
weight: 1546
solve_time_s: 448
verified: true
draft: false
---

[CF 1546B - AquaMoon and Stolen String](https://codeforces.com/problemset/problem/1546/B)

**Rating:** 1200  
**Tags:** interactive, math  
**Solve time:** 7m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of original strings and a second multiset formed after a disturbance process. The disturbance worked in two stages. First, all strings were paired except one special string that stayed unpaired. Then, for each pair, the two strings were partially “mixed” by swapping characters at some chosen positions, and finally the unpaired string was removed. The resulting list is shuffled, so order carries no information.

We are also given the full original set and the final corrupted set. The task is to identify which original string disappeared entirely.

The key structural constraint is that $n$ is odd, so exactly one original string has no counterpart in the final set. Every other original string participates in exactly one pair, and each pair only swaps characters position-wise without changing the multiset of characters across the pair at any fixed position. That implies a conservation principle: across each pair, every column contributes the same total character multiset before and after swapping, only redistributed between the two strings.

The bounds are large: total $\sum n \cdot m \le 10^5$. That immediately rules out any solution that compares every original string against every final string, since that would be quadratic in the number of strings. Even hashing full strings per comparison would still require careful linear aggregation rather than pairwise matching.

A subtle failure case appears when one tries greedy matching of identical strings. Consider three strings where two are identical initially but get heavily swapped in pairs. After swaps, they may no longer match each other or any original string exactly, even though they still correspond to valid paired transformations. So equality matching is insufficient; we need a structural invariant that survives swapping.

Another pitfall is assuming frequency of whole strings or per-character counts is enough. Pairwise swaps preserve total character counts globally but not per string, so the stolen string cannot be detected from global frequency alone.

## Approaches

A brute-force idea is to try removing each original string candidate and check whether the remaining $n-1$ original strings can be partitioned into pairs that could produce the final multiset via some valid swap operations. This degenerates into trying to match transformed pairs, effectively requiring checking all pairings and all swap configurations. The number of pairings is factorial in $n$, and even verifying a single pairing requires comparing strings of length $m$. This is far beyond any feasible limit.

The key observation is that we do not need to reconstruct pairings or swaps. Instead, we exploit parity of occurrences across columns. Each swap in a pair affects exactly two strings at a position, so for any fixed position and any character, the number of occurrences across all $n-1$ final strings differs from the original by exactly the contribution of the stolen string. Everything else cancels out pairwise.

So for each position, we compare how characters differ between the original multiset and the final multiset. Since all non-stolen strings appear in both sets (possibly permuted and altered only by swaps inside pairs), their total contribution across all strings cancels out in a structured way, leaving a single consistent residue that corresponds to the missing string.

This suggests maintaining frequency tables per position. For each column $j$, we compute the XOR-like cancellation using counts of letters. The stolen string is the only one that creates a global imbalance across all positions simultaneously. By accumulating per-position differences, we recover the exact characters of the missing string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pairing reconstruction | Exponential | High | Too slow |
| Per-position frequency cancellation | $O(nm)$ | $O(26m)$ or $O(m)$ | Accepted |

## Algorithm Walkthrough

1. Build frequency counts of characters for each position across all original strings. For each position $j$, we store how many times each letter appears in column $j$ among all $n$ strings. This represents the initial state.
2. Build the same frequency counts for the $n-1$ final strings. This represents the post-disturbance state after all swaps and removal.
3. For each position $j$, compute the difference between original and final frequency arrays. Since swaps only permute characters between paired strings at the same position, the total per-position multiset over all non-stolen strings remains consistent. The only discrepancy comes from the missing string.
4. For each position $j$, find the character whose count is larger in the original multiset than in the final multiset. That character must be the character of the stolen string at position $j$, because it is the only contribution not accounted for in the final multiset.
5. Concatenate these characters over all positions to reconstruct the stolen string.

The crucial step is the per-column isolation. Even though swaps scramble characters within pairs, they never move characters across positions, so each column behaves independently as a multiset conservation system.

### Why it works

At every position $j$, consider the multiset of characters across all original strings. After pairing and swapping, every non-stolen string still contributes exactly one character to that column in the final array. Swapping only exchanges these contributions within pairs, preserving the multiset union of paired strings. Therefore, when comparing original vs final columns, all paired contributions cancel perfectly, leaving exactly one unmatched character per column, which must belong to the stolen string. Since the stolen string is consistent across all columns, these unmatched characters assemble into a valid string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        orig = [input().strip() for _ in range(n)]
        final = [input().strip() for _ in range(n - 1)]

        cnt_o = [[0] * 26 for _ in range(m)]
        cnt_f = [[0] * 26 for _ in range(m)]

        for s in orig:
            for j, ch in enumerate(s):
                cnt_o[j][ord(ch) - 97] += 1

        for s in final:
            for j, ch in enumerate(s):
                cnt_f[j][ord(ch) - 97] += 1

        res = []
        for j in range(m):
            for c in range(26):
                if cnt_o[j][c] > cnt_f[j][c]:
                    res.append(chr(c + 97))
                    break

        print("".join(res))

if __name__ == "__main__":
    solve()
```

The solution is implemented by building two column-wise frequency tables. The nested loops over strings and characters directly implement the per-column aggregation. The subtraction logic is implicit: we locate the character whose count decreased by exactly one between original and final states.

A common implementation pitfall is forgetting that each column must be processed independently. Treating strings as whole units loses the cancellation structure introduced by swaps.

## Worked Examples

### Example 1

Input:

```
3 5
aaaaa
bbbbb
ccccc
aaaaa
bbbbb
```

We compute column frequencies.

| Column | Original counts | Final counts | Difference | Chosen char |
| --- | --- | --- | --- | --- |
| 1 | a:3 | a:2 | a:1 | a |
| 2 | b:3 | b:2 | b:1 | b |
| 3 | c:3 | c:2 | c:1 | c |
| 4 | c:3 | c:2 | c:1 | c |
| 5 | c:3 | c:2 | c:1 | c |

This reconstructs `"ccccc"`.

This trace shows that even if swaps occurred, the imbalance per column still isolates the missing contribution.

### Example 2

Input:

```
5 6
abcdef
uuuuuu
kekeke
ekekek
xyzklm
xbcklf
eueueu
ayzdem
ukukuk
```

We again compare column-wise frequencies and extract the missing contributions.

| Column | Chosen character |
| --- | --- |
| 1 | k |
| 2 | e |
| 3 | k |
| 4 | e |
| 5 | k |
| 6 | e |

Result is `"kekeke"`.

This demonstrates that even heavily interleaved swaps across multiple pairs do not affect per-column imbalance detection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | each character is processed once per test case |
| Space | $O(26m)$ | frequency arrays per column |

The total input size constraint $\sum n \cdot m \le 10^5$ ensures the algorithm runs comfortably within limits, since every operation is constant-time per character.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out_lines = []
    for _ in range(t):
        n, m = map(int, input().split())
        orig = [input().strip() for _ in range(n)]
        final = [input().strip() for _ in range(n - 1)]

        cnt_o = [[0]*26 for _ in range(m)]
        cnt_f = [[0]*26 for _ in range(m)]

        for s in orig:
            for j, ch in enumerate(s):
                cnt_o[j][ord(ch)-97] += 1
        for s in final:
            for j, ch in enumerate(s):
                cnt_f[j][ord(ch)-97] += 1

        res = []
        for j in range(m):
            for c in range(26):
                if cnt_o[j][c] > cnt_f[j][c]:
                    res.append(chr(c+97))
                    break

        out_lines.append("".join(res))

    return "\n".join(out_lines)

# provided sample
assert run("""3
3 5
aaaaa
bbbbb
ccccc
aaaaa
bbbbb
3 4
aaaa
bbbb
cccc
aabb
bbaa
5 6
abcdef
uuuuuu
kekeke
ekekek
xyzklm
xbcklf
eueueu
ayzdem
ukukuk
""") == """ccccc
cccc
kekeke"""

# minimum size
assert run("""1
1 1
a
""") == """a"""

# all equal strings
assert run("""1
3 3
aaa
aaa
bbb
aaa
aaa
""") == """bbb"""

# single differing column
assert run("""1
3 3
abc
def
ghi
abc
def
""") == """ghi"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | a | minimal boundary |
| repeated strings | bbb | frequency cancellation correctness |
| structured alphabet grid | ghi | per-column independence |

## Edge Cases

When all strings are identical except the stolen one, the frequency difference becomes concentrated entirely in that repeated pattern. The algorithm still isolates each column independently, so the stolen string is reconstructed exactly even though no pairwise distinction exists.

When swaps in pairs are maximal, meaning every position in every pair is swapped, individual strings become heavily distorted. However, column-wise multisets remain invariant across paired contributions, so the imbalance logic still isolates the missing string without relying on any structural similarity between original and final strings.

When $n = 1$, the final array is empty. Every column frequency difference equals the only original string, so the algorithm directly returns it without ambiguity.
