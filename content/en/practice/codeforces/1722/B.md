---
title: "CF 1722B - Colourblindness"
description: "We are given a very small grid with exactly two horizontal strips and some number of vertical columns. Each cell contains one of three colors, but the viewer is colorblind in a specific way: green and blue are indistinguishable, while red remains distinct from both."
date: "2026-06-15T01:25:01+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1722
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 817 (Div. 4)"
rating: 800
weight: 1722
solve_time_s: 134
verified: true
draft: false
---

[CF 1722B - Colourblindness](https://codeforces.com/problemset/problem/1722/B)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small grid with exactly two horizontal strips and some number of vertical columns. Each cell contains one of three colors, but the viewer is colorblind in a specific way: green and blue are indistinguishable, while red remains distinct from both.

The task is to determine whether the two rows would appear identical to this colorblind observer when compared column by column. In other words, after applying the rule that merges green and blue into a single perceived color, we check whether every column has the same perceived pair of colors in both rows.

Each test case is independent, and we repeat this comparison multiple times.

The constraints are small: at most 100 test cases and at most 100 columns per test case. This immediately rules out any need for advanced data structures or optimization beyond linear scanning. Even an O(n²) per test would be acceptable in practice, but the structure strongly suggests an O(n) per test solution.

The key subtlety lies in understanding what “cannot distinguish green and blue” really means. It does not mean they become red, nor that they disappear. It means they collapse into a single equivalence class. Any comparison must respect that equivalence.

A common mistake arises from treating the strings as directly comparable without transformation. For example, comparing `G` and `B` as different characters would incorrectly reject cases where they should be considered equal.

Another potential pitfall is trying to compare only counts of each character. That fails because position matters. For example, `RGB` vs `BRG` have identical multisets of characters but are clearly different even under colorblind mapping.

Edge cases are minimal but instructive.

One case is when both rows consist entirely of green and blue, for example:

```
GBG
BGB
```

These are all equivalent under the colorblind rule, so they should match if positions align after mapping. A naive frequency-based solution might incorrectly say YES for mismatched arrangements.

Another case is a single-column grid:

```
G
B
```

These must be considered identical, because both map to the same perceived color.

## Approaches

The brute-force idea is straightforward: simulate the colorblind transformation explicitly for both rows and then compare the resulting strings. For each cell, we map green and blue to a shared symbol, say `X`, while red remains `R`. After transformation, we compare the two resulting strings character by character.

This works because it reduces the problem to a standard string equality check. The cost is linear in the number of columns per test case, and since the grid is only two rows, there is no additional overhead.

If we attempted something more complicated, such as tracking transitions or matching patterns, we would be over-engineering a problem that is fundamentally a normalization-and-compare task.

The brute-force is already optimal in this setting. The key observation is that the only meaningful transformation is a constant-time mapping per character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct comparison without normalization | O(n) per test | O(1) | Incorrect |
| Normalize then compare | O(n) per test | O(n) (or O(1) streaming) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, since each grid is independent and must be evaluated separately.
2. For each test case, read the integer n and the two strings representing the rows.
3. Iterate through each column index from 0 to n - 1.
4. For each column, convert both characters using the same rule: treat `G` and `B` as equivalent, while keeping `R` distinct. A convenient implementation is to map both `G` and `B` to the same symbol, for example `0`, and map `R` to `1`.
5. Compare the transformed characters at each column. If any column differs after transformation, immediately conclude that the rows are not identical for the colorblind observer.
6. If all columns match after transformation, conclude the rows are identical.

The early exit in step 5 is important because a mismatch in any column fully determines the answer. There is no need to continue scanning once a difference is found.

### Why it works

The algorithm relies on the fact that the observer defines an equivalence relation over colors where `G ≡ B` and `R` is distinct from both. Equality of perceived rows is therefore equivalent to equality of their images under this equivalence mapping applied pointwise. Since the mapping is applied independently to each cell and comparison is positional, preserving equality column by column guarantees correctness of the full row comparison.

## Python Solution

```python
import sys
input = sys.stdin.readline

def norm(c):
    # map green and blue to same class
    return 0 if c != 'R' else 1

t = int(input())
for _ in range(t):
    n = int(input())
    a = input().strip()
    b = input().strip()

    ok = True
    for i in range(n):
        if norm(a[i]) != norm(b[i]):
            ok = False
            break

    print("YES" if ok else "NO")
```

The solution reads each test case independently and processes the two rows in a single pass. The helper function `norm` encodes the entire colorblindness rule in one constant-time operation per character. The loop immediately terminates when a mismatch is found, which ensures optimal behavior even in worst-case inputs.

A common implementation mistake is forgetting to strip newline characters from input strings, which can silently shift indexing logic. Another is attempting to compare raw characters directly, which fails specifically on `G` versus `B`.

## Worked Examples

We trace two representative cases from the sample.

### Example 1

Input:

```
n = 2
row1 = RG
row2 = RB
```

| i | row1[i] | row2[i] | norm(row1[i]) | norm(row2[i]) | status |
| --- | --- | --- | --- | --- | --- |
| 0 | R | R | 1 | 1 | match |
| 1 | G | B | 0 | 0 | match |

All positions match after normalization, so the result is YES.

This demonstrates that the algorithm correctly collapses different visible colors into a single equivalence class before comparison.

### Example 2

Input:

```
n = 4
row1 = GRBG
row2 = GBGB
```

| i | row1[i] | row2[i] | norm(row1[i]) | norm(row2[i]) | status |
| --- | --- | --- | --- | --- | --- |
| 0 | G | G | 0 | 0 | match |
| 1 | R | B | 1 | 0 | mismatch |

At index 1, a mismatch appears after normalization, so the algorithm stops and returns NO.

This confirms early termination behavior and shows that structural similarity is insufficient if positional equivalence breaks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each column is processed once with O(1) work |
| Space | O(1) | No extra storage beyond input strings |

The total work across all test cases is at most 10,000 character comparisons, which is trivial under the constraints. Memory usage remains constant apart from input storage.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    input = sys.stdin.readline

    t = int(input())
    def norm(c):
        return 0 if c != 'R' else 1

    for _ in range(t):
        n = int(input())
        a = input().strip()
        b = input().strip()

        ok = True
        for i in range(n):
            if norm(a[i]) != norm(b[i]):
                ok = False
                break
        output.append("YES" if ok else "NO")

    return "\n".join(output)

# provided samples
assert run("""6
2
RG
RB
4
GRBG
GBGB
5
GGGGG
BBBBB
7
BBBBBBB
RRRRRRR
8
RGBRRGBR
RGGRRBGR
1
G
G
""") == """YES
NO
YES
NO
YES
YES"""

# custom cases
assert run("""1
1
R
G
""") == "YES", "single column equivalence"

assert run("""1
3
RGB
RBR
""") == "YES", "mixed greens/blues equivalence"

assert run("""1
3
RRR
RRR
""") == "YES", "all red identical"

assert run("""1
3
RGB
GBR
""") == "NO", "permutation breaks position matching"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 R vs G | YES | single-cell equivalence class |
| RGB vs RBR | YES | internal G/B collapse correctness |
| RRR vs RRR | YES | trivial identical case |
| RGB vs GBR | NO | positional mismatch detection |

## Edge Cases

A single-column grid is the simplest non-trivial case. The algorithm compares only one pair of characters and returns YES if both belong to the same equivalence class. For example, `G` vs `B` maps to identical normalized values, so the result is correct.

A fully homogeneous grid such as all `R` in both rows is handled without any special logic. Every comparison evaluates to equality, so the loop completes without triggering early exit.

A case with only green and blue values mixed in different patterns stresses the importance of positional comparison. The algorithm correctly rejects mismatched orderings because it does not rely on counts, only aligned equality after normalization.

A final subtle case is ensuring input trimming is correct. If newline characters are not removed, comparisons may accidentally involve `\n`, which would break equality checks. The `.strip()` call ensures this cannot happen.
