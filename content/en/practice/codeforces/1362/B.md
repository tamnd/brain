---
title: "CF 1362B - Johnny and His Hobbies"
description: "We are given a set of distinct integers. Johnny chooses a positive integer k and replaces every value s in the set with s XOR k. The transformation is applied to every element simultaneously."
date: "2026-06-11T12:34:24+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1362
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 647 (Div. 2) - Thanks, Algo Muse!"
rating: 1200
weight: 1362
solve_time_s: 122
verified: true
draft: false
---

[CF 1362B - Johnny and His Hobbies](https://codeforces.com/problemset/problem/1362/B)

**Rating:** 1200  
**Tags:** bitmasks, brute force  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of distinct integers. Johnny chooses a positive integer `k` and replaces every value `s` in the set with `s XOR k`.

The transformation is applied to every element simultaneously. After the transformation, we want the resulting set to be exactly the same as the original one. Since we are dealing with sets, the order of elements does not matter.

Our task is to find the smallest positive integer `k` for which

$$\{s \oplus k \mid s \in S\} = S$$

or report that no such positive integer exists.

The constraints are unusually small. Every number in the set is less than `1024`, which means it uses at most 10 bits. The number of elements in a test case is at most `1024`, and the total number of elements across all test cases is also at most `1024`.

Those limits immediately suggest that trying many candidate values of `k` may be completely feasible. Since all values lie in the range `[0, 1023]`, any XOR result produced from two such numbers also lies in that range. A search over all possible 10-bit masks costs only about a thousand iterations.

Several edge cases are easy to miss.

Consider a single-element set:

```
1
1
5
```

Any positive `k` changes `5` into a different value, so the set cannot remain unchanged. The correct answer is:

```
-1
```

A careless solution might assume every set has some symmetry and incorrectly return a value.

Another important case is when the answer is large:

```
1
2
0 1023
```

Using `k = 1023` swaps the two elements:

```
0 XOR 1023 = 1023
1023 XOR 1023 = 0
```

The set remains unchanged, so the answer is:

```
1023
```

A solution that only checks masks appearing among the elements themselves would miss this.

One more subtle case is:

```
1
3
1 2 3
```

Trying different masks never reproduces the same set. The correct answer is:

```
-1
```

It is tempting to look only for pairwise relationships, but the entire transformed set must match exactly.

## Approaches

The most direct idea is to test every possible positive integer `k`.

For each candidate, XOR every element of the set with `k`, build the transformed set, and compare it with the original set. If they match, we have found a valid answer.

This brute-force approach is correct because it literally checks the condition from the statement. The question is whether it is fast enough.

The key observation comes from the value range. Every element is smaller than `1024`, so all relevant XOR masks are also smaller than `1024`. There is no reason to test anything outside the range `[1, 1023]`.

For each candidate mask we process at most `n ≤ 1024` elements. The worst-case work per test case is:

$$1023 \times 1024 \approx 10^6$$

operations.

Given that the total sum of `n` over all test cases is only `1024`, this is comfortably within the limit.

The observation that all numbers are 10-bit values turns what would normally look like an enormous search space into a tiny one. Instead of searching over arbitrary integers, we only need to check 1023 possible masks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all integers | Unbounded | O(n) | Impossible |
| Enumerate all masks 1..1023 | O(1024·n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the set of numbers.
2. Store the original elements in a hash set for O(1) membership and equality checks.
3. Iterate through every candidate mask `k` from `1` to `1023`.
4. For the current mask, compute all values `x XOR k` for every element `x` in the set.
5. Build a new set containing those transformed values.
6. Compare the transformed set with the original set.

If they are identical, then applying `k` preserves the set exactly.
7. Since masks are tested in increasing order, the first valid mask is automatically the smallest valid answer. Output it immediately.
8. If no mask works after checking all values from `1` to `1023`, output `-1`.

### Why it works

For any valid answer, `k` must be a 10-bit number because all set elements lie in `[0,1023]`. The algorithm checks every positive mask in that entire range.

For a fixed mask, the transformed set is exactly the set described in the problem statement. Comparing it with the original set directly verifies whether the condition holds.

Since every possible candidate mask is examined and the first valid one is returned, the algorithm cannot miss a solution and cannot return a larger solution when a smaller one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        original = set(arr)

        answer = -1

        for k in range(1, 1024):
            transformed = {x ^ k for x in arr}

            if transformed == original:
                answer = k
                break

        answers.append(str(answer))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm almost literally.

The original numbers are stored in a Python `set`, which allows efficient equality comparison. Two sets are equal if and only if they contain exactly the same elements, which matches the problem definition.

For each candidate mask, a set comprehension generates the transformed values. Because the input already consists of distinct values, the transformed result also remains a set of distinct values. Comparing the two sets directly checks whether the transformation leaves the set unchanged.

The loop over masks starts at `1`, not `0`. The statement asks for a positive integer `k`, so `0` is not allowed even though it would always preserve the set.

The search stops immediately after finding a valid mask because masks are processed in increasing order. This guarantees the smallest valid answer.

## Worked Examples

### Example 1

Input:

```
1
4
1 0 2 3
```

Original set:

```
{0, 1, 2, 3}
```

| k | Transformed Set | Matches? |
| --- | --- | --- |
| 1 | {1,0,3,2} = {0,1,2,3} | Yes |

The first mask already works, so the answer is:

```
1
```

This example demonstrates that XOR can simply permute elements inside the set without changing the set itself.

### Example 2

Input:

```
1
3
1 2 3
```

| k | Transformed Set | Matches? |
| --- | --- | --- |
| 1 | {0,3,2} | No |
| 2 | {3,0,1} | No |
| 3 | {2,1,0} | No |
| ... | ... | ... |
| 1023 | {1022,1021,1020} | No |

No candidate mask reproduces the original set.

Output:

```
-1
```

This example shows that not every set has the required XOR symmetry.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1024·n) | Check 1023 masks, each processes n elements |
| Space | O(n) | Store original and transformed sets |

Since `n ≤ 1024` and the total number of elements across all test cases is at most `1024`, the worst-case work is only around one million XOR operations. This easily fits within the 1-second time limit and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        s = set(arr)

        cur = -1
        for k in range(1, 1024):
            if {x ^ k for x in arr} == s:
                cur = k
                break

        ans.append(str(cur))

    return "\n".join(ans) + "\n"

# provided sample
assert run(
"""6
4
1 0 2 3
6
10 7 14 8 3 12
2
0 2
3
1 2 3
6
1 4 6 10 11 12
2
0 1023
"""
) == """1
4
2
-1
-1
1023
"""

# minimum size
assert run(
"""1
1
0
"""
) == """-1
""", "single element"

# simple swap
assert run(
"""1
2
0 2
"""
) == """2
""", "two elements exchanged by xor 2"

# full 2-bit space
assert run(
"""1
4
0 1 2 3
"""
) == """1
""", "smallest valid mask"

# boundary values
assert run(
"""1
2
0 1023
"""
) == """1023
""", "largest possible answer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `{0}` | `-1` | Single-element set cannot stay unchanged under positive XOR |
| `{0,2}` | `2` | Simple two-element swap |
| `{0,1,2,3}` | `1` | Multiple valid masks exist, smallest must be returned |
| `{0,1023}` | `1023` | Largest possible mask and boundary values |

## Edge Cases

A single-element set has no valid answer:

```
1
1
5
```

The algorithm checks every mask from `1` to `1023`. Every transformation produces a different singleton set:

```
{5 XOR k}
```

which can never equal `{5}` because `k > 0`. The search finishes and outputs:

```
-1
```

For the boundary case

```
1
2
0 1023
```

the algorithm eventually reaches `k = 1023` and computes:

```
0 XOR 1023 = 1023
1023 XOR 1023 = 0
```

The transformed set becomes `{0,1023}`, matching the original. Since no smaller mask works, the output is:

```
1023
```

For a set with no symmetry,

```
1
3
1 2 3
```

every candidate mask produces a different set. The equality test fails each time, so the algorithm correctly returns:

```
-1
```

The direct set comparison prevents false positives that could arise from checking only partial relationships between elements.
