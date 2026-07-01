---
title: "CF 104285A - ATCG"
description: "We are given a DNA strand written as a string over the alphabet {A, T, C, G}. Biology gives us a precise transformation rule for constructing the complementary strand: first reverse the original sequence because the two strands run in opposite directions, then replace each…"
date: "2026-07-01T20:54:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104285
codeforces_index: "A"
codeforces_contest_name: "PCCA Winter Camp Contest 2023"
rating: 0
weight: 104285
solve_time_s: 46
verified: true
draft: false
---

[CF 104285A - ATCG](https://codeforces.com/problemset/problem/104285/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a DNA strand written as a string over the alphabet `{A, T, C, G}`. Biology gives us a precise transformation rule for constructing the complementary strand: first reverse the original sequence because the two strands run in opposite directions, then replace each nucleotide using fixed pairing rules `A ↔ T` and `C ↔ G`.

The task is to simulate exactly that transformation for each test case. The input provides multiple independent DNA strings, and for each one we must output the complementary strand in the same left-to-right direction as it would appear from the 5′-end to the 3′-end.

The constraints are small enough that any linear transformation per test case is sufficient. Each string has length at most 100 and there are at most 2000 test cases, so even a straightforward O(n) per case solution runs comfortably within limits. The total number of characters processed is at most 200000, which is trivial for Python.

The only subtle point that can trip up an implementation is forgetting the reversal step. A naive solution that only applies the substitution without reversing produces a valid-looking DNA string, but in the wrong orientation.

For example, if `s = "ATCG"`, substituting directly gives `"TAGC"`, but the correct procedure reverses first:

`"GCTA"` then substitutes to `"CGAT"`.

Another possible mistake is applying reversal after substitution. That also gives the wrong result because complementing changes symbols, not positions, so the order of operations is fixed.

## Approaches

A brute-force interpretation would explicitly construct the reverse string and then iterate again applying the mapping rules. This is already linear time and works because the transformation is purely local: each character maps independently once its position in the reversed string is known.

We can also think of it as a single pass if we directly iterate the string from the end to the beginning and build the result on the fly. This removes the need for an explicit reversed copy.

The key observation is that the transformation decomposes into two independent components: a permutation of indices (reverse order) and a substitution on characters. Since both are O(1) per element and do not depend on each other beyond ordering, we can fuse them into a single pass.

The brute-force method performs two linear scans per string. The optimized version performs one, but asymptotically both are O(n). The improvement is mostly constant-factor simplification.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (reverse + map) | O(n) | O(n) | Accepted |
| Optimal (single reverse iteration) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the string `s`. This string represents one DNA strand from its 5′-end to its 3′-end.
2. Prepare a mapping between nucleotides: `A → T`, `T → A`, `C → G`, `G → C`. This encodes the biological pairing rule and is applied independently to each character.
3. Traverse the string from the last character to the first. This implicitly performs the reversal step without constructing a new reversed string.
4. For each character encountered during the reverse traversal, replace it using the mapping and append the result to an output buffer.
5. After processing all characters, output the constructed string.

The reason we iterate in reverse order rather than reversing explicitly is that it avoids an extra memory allocation while preserving correctness. Since each position is independent after reversal, streaming the transformation is equivalent.

### Why it works

The DNA transformation is a composition of two functions: a permutation `P` that reverses indices and a substitution `C` that maps each character. Because `C` acts pointwise and does not depend on neighbors or global structure, the composition `C(P(s))` can be computed by applying both operations in a single traversal over the permuted index order. This ensures every character is transformed exactly once in its correct final position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    mp = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }

    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        res = []
        for i in range(n - 1, -1, -1):
            res.append(mp[s[i]])
        out.append("".join(res))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution builds a direct character mapping and processes each string from right to left. The loop over `i = n-1 ... 0` performs the reversal implicitly. Each character is transformed once using the dictionary lookup, which is O(1). The result is accumulated in a list for efficiency and joined once per test case.

The use of `strip()` ensures no trailing newline interferes with indexing. The output is buffered to avoid repeated writes.

## Worked Examples

### Example 1

Input string: `ACGT`

We process it from the end:

| Step | Index | Character | Mapped |
| --- | --- | --- | --- |
| 1 | 3 | T | A |
| 2 | 2 | G | C |
| 3 | 1 | C | G |
| 4 | 0 | A | T |

Result builds as `A C G T`, giving `"ACGT"`.

This example is symmetric under complement and reversal, which confirms correctness when the original string equals its own reverse complement structure.

### Example 2

Input string: `ATGGCT`

| Step | Index | Character | Mapped |
| --- | --- | --- | --- |
| 1 | 5 | T | A |
| 2 | 4 | C | G |
| 3 | 3 | G | C |
| 4 | 2 | G | C |
| 5 | 1 | T | A |
| 6 | 0 | A | T |

Final output: `"AGCCAT"`

This demonstrates that both reversal and substitution are necessary. Direct substitution would produce `TACCG A` in the original order, which is incorrect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is visited exactly once in reverse order |
| Space | O(n) per test case | Output string storage for each transformed sequence |

The total work across all test cases is proportional to the total input size, which is at most 200000 characters. This is well within typical time limits for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided sample
assert run("""1
4
ACGT
""") == "ACGT"

# reverse check
assert run("""1
4
ATCG
""") == "CGAT"

# single character
assert run("""1
1
A
""") == "T"

# all same type pattern
assert run("""1
3
AAA
""") == "TTT"

# mixed case
assert run("""1
6
ATGGCT
""") == "AGCCAT"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ACGT | ACGT | symmetric case |
| ATCG | CGAT | reversal correctness |
| A | T | minimum size |
| AAA | TTT | repeated mapping stability |
| ATGGCT | AGCCAT | full transformation correctness |

## Edge Cases

For a single-character input like `A`, the algorithm reads index 0, maps it directly to `T`, and produces `"T"`. Since reversal has no effect on a single element, correctness depends only on the mapping table, which remains valid.

For an input like `ATCG`, the traversal order becomes `G → C → T → A`. Each character is mapped independently, producing `C → G`, `G → C`, `T → A`, `A → T`, which concatenates to `"CGAT"`. This confirms that the reversal is handled implicitly by iteration direction and does not require a separate array.
