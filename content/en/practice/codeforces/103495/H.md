---
title: "CF 103495H - Reverse the String"
description: "We are given a string consisting only of lowercase English letters. In one move, we are allowed to pick a contiguous segment of the string and reverse it, or we may choose to leave the string unchanged."
date: "2026-07-03T06:10:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103495
codeforces_index: "H"
codeforces_contest_name: "2021 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 103495
solve_time_s: 53
verified: true
draft: false
---

[CF 103495H - Reverse the String](https://codeforces.com/problemset/problem/103495/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting only of lowercase English letters. In one move, we are allowed to pick a contiguous segment of the string and reverse it, or we may choose to leave the string unchanged. The goal is to obtain the lexicographically smallest string that can be produced using at most one such reversal.

Lexicographical order here behaves like dictionary order: we compare two strings from left to right and the first position where they differ determines which one is smaller, with earlier alphabet characters being smaller.

The input contains multiple test cases, and the total length of all strings across test cases is large, up to about 1.5 million characters. This immediately rules out any approach that tries every possible reversal explicitly, since enumerating all substrings is quadratic per test case and would exceed time limits by several orders of magnitude.

A naive mistake comes from thinking only about swapping or local improvements. For example, on input `ba`, reversing the whole string produces `ab`, which is optimal, but on something like `abac`, reversing arbitrary segments without a global strategy can miss that moving a small character far to the left is sometimes beneficial even if it disturbs the middle.

Another subtle failure case appears when a locally good reversal is not globally optimal. For instance, in `cab`, reversing only `ca` gives `acb`, which is optimal, but in longer strings a greedy choice of an early improvement can block a better later improvement unless the strategy guarantees global minimality.

The core difficulty is that a single reversal simultaneously affects three regions: the prefix before the segment, the reversed segment itself, and the suffix after it. The suffix is untouched, but the reversed segment changes order internally, which makes brute reasoning over all substrings expensive.

## Approaches

A brute-force solution would try all pairs `(l, r)` and compute the resulting string after reversing that segment, then pick the minimum. There are $O(n^2)$ such pairs and each reversal costs $O(n)$ to materialize, so the total complexity becomes $O(n^3)$ if done literally or at least $O(n^2)$ with careful simulation. With $n$ up to $10^5$, this is impossible.

Even if we optimize by only comparing candidates without fully rebuilding strings, we still face $O(n^2)$ candidates, and each comparison may take linear time in the worst case. So we need a way to avoid enumerating segments entirely.

The key observation is that lexicographical order is decided as early as possible. We only care about improving the first position where the string can become smaller. That suggests we should focus on the earliest index where a better character can be brought forward by a single reversal.

If we fix a position `i`, the only useful operation is to bring some character from the suffix `[i+1, n-1]` to position `i` by reversing a segment ending at that character. After reversal, that chosen character becomes the new value at position `i`.

So the strategy becomes: for each position, ask whether there exists a smaller character later in the string. If yes, we want the smallest such character, and among its occurrences we prefer the rightmost one, because reversing to the rightmost occurrence maximizes lexicographical improvement of earlier positions without restricting future choices.

This reduces the problem to tracking, for every suffix, the smallest character and a position where it occurs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all reversals) | O(n³) or O(n²) | O(n) | Too slow |
| Suffix-min + single optimal reversal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the answer by deciding whether we should perform a reversal, and if so, where.

1. Precompute for every position `i` the smallest character in the suffix starting at `i`, along with the last position where this smallest character appears. This is done from right to left so that we can maintain both the minimum character and a representative index. This gives us immediate access to the best character we could bring forward if we start a reversal at position `i`.
2. Scan the string from left to right. At position `i`, compare `s[i]` with the smallest character in the suffix starting at `i + 1`. If the suffix contains a strictly smaller character, then position `i` is improvable by bringing that smaller character forward.
3. Once we find the first position `i` where an improvement is possible, we fix the decision that the optimal string must differ from the original starting at this position. This is because any lexicographically smaller result must reduce the earliest possible mismatch point.
4. Let the best character in the suffix be `c`, and let `j` be the last occurrence of `c`. We reverse the substring from `i` to `j`. This moves `c` to position `i` and shifts everything in between one step to the right in reversed order.
5. Output the resulting string after performing this single reversal. If no position `i` can be improved, we output the original string.

Why it works comes down to controlling the first differing position. Any valid optimal answer must agree with the original string up to some position `i` and then either keep `s[i]` or replace it with something smaller. The earliest index where replacement is possible is therefore the only meaningful decision point. Once we choose to improve position `i`, we want the smallest possible character that can occupy it, and placing it from its rightmost occurrence ensures we do not accidentally prevent even better configurations earlier in the string. Any alternative reversal that changes an earlier index or uses a larger character cannot produce a lexicographically smaller outcome than this construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(s: str) -> str:
    n = len(s)
    if n <= 1:
        return s

    suf_min = [''] * n
    suf_pos = [0] * n

    suf_min[-1] = s[-1]
    suf_pos[-1] = n - 1

    for i in range(n - 2, -1, -1):
        if s[i] < suf_min[i + 1]:
            suf_min[i] = s[i]
            suf_pos[i] = i
        elif s[i] > suf_min[i + 1]:
            suf_min[i] = suf_min[i + 1]
            suf_pos[i] = suf_pos[i + 1]
        else:
            suf_min[i] = s[i]
            suf_pos[i] = suf_pos[i + 1]

    s = list(s)

    for i in range(n - 1):
        if suf_min[i + 1] < s[i]:
            j = suf_pos[i + 1]
            s[i:j + 1] = reversed(s[i:j + 1])
            return ''.join(s)

    return ''.join(s)

def main():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        print(solve(s))

if __name__ == "__main__":
    main()
```

The solution builds a suffix structure that tracks both the smallest character available to the right of each position and a position where it occurs. This avoids recomputing scans for every index.

The scan for the first improvement point is crucial because lexicographical minimization depends on the earliest position where we can reduce a character. Once found, we immediately apply the reversal and stop, since any later modification would leave a larger prefix unchanged and therefore be worse.

The reversal itself uses Python slicing on a list, which is efficient enough because it happens at most once per test case.

## Worked Examples

### Example 1: `abbcabaac`

We compute suffix minima and scan left to right until we find the first improvable position.

| i | s[i] | suffix min after i | decision |
| --- | --- | --- | --- |
| 0 | a | b | no change |
| 1 | b | a | improvement found |

At index 1, we see a smaller character exists later, namely `a`. The last occurrence of `a` in the suffix determines the reversal boundary, which is the farthest `a` we can use.

After reversing that segment, the string becomes `aaabacbbc`.

This shows that the algorithm does not just pick the nearest smaller character but stretches the reversal to the last occurrence, ensuring maximal improvement at the first decision point.

### Example 2: `cbad`

We track the process:

| i | s[i] | suffix min after i | decision |
| --- | --- | --- | --- |
| 0 | c | a | improvement found |

The smallest suffix character is `a`, so we reverse from index 0 to the last `a`, which is index 2. Reversing `cba` gives `abc`, producing `abdc` after appending the untouched suffix.

This demonstrates how the algorithm prioritizes bringing the globally smallest reachable character as early as possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is processed a constant number of times during suffix computation and at most one reversal is performed |
| Space | O(n) | Suffix arrays and mutable string representation |

The total input size across test cases is bounded by $1.5 \times 10^6$, so a linear solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve(s: str) -> str:
        n = len(s)
        if n <= 1:
            return s

        suf_min = [''] * n
        suf_pos = [0] * n

        suf_min[-1] = s[-1]
        suf_pos[-1] = n - 1

        for i in range(n - 2, -1, -1):
            if s[i] < suf_min[i + 1]:
                suf_min[i] = s[i]
                suf_pos[i] = i
            elif s[i] > suf_min[i + 1]:
                suf_min[i] = suf_min[i + 1]
                suf_pos[i] = suf_pos[i + 1]
            else:
                suf_min[i] = s[i]
                suf_pos[i] = suf_pos[i + 1]

        s = list(s)

        for i in range(n - 1):
            if suf_min[i + 1] < s[i]:
                j = suf_pos[i + 1]
                s[i:j + 1] = reversed(s[i:j + 1])
                return ''.join(s)

        return ''.join(s)

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve(input().strip()))
    return "\n".join(out)

# provided samples
assert run("1\nabbcabaac\n") == "aaabacbbc", "sample 1"

# custom cases
assert run("1\na\n") == "a", "single char"
assert run("1\nba\n") == "ab", "simple swap"
assert run("1\nabc\n") == "abc", "already optimal"
assert run("1\ncba\n") == "abc", "full reversal best"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | minimal length edge case |
| `ba` | `ab` | single reversal improvement |
| `abc` | `abc` | no-op correctness |
| `cba` | `abc` | full reversal behavior |

## Edge Cases

A single-character string such as `a` never triggers the reversal condition because there is no suffix to improve against. The algorithm returns it immediately since the suffix-min structure is trivial and the loop over positions is empty.

In a string like `ba`, the suffix minimum at index 0 is `a`, which is smaller than `b`. The algorithm selects the segment `[0, 1]`, reverses it, and produces `ab`. The suffix tracking ensures that even this simplest case is handled consistently with larger inputs.

For a fully decreasing string like `cba`, every position can be improved immediately. The algorithm chooses the first index `0`, identifies `a` as the smallest suffix character, and reverses the whole string. This produces `abc`, which matches the global optimum since any partial reversal would leave a larger prefix unchanged and result in a worse lexicographic outcome.
