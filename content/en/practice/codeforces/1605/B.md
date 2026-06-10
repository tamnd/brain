---
title: "CF 1605B - Reverse Sort"
description: "We are given a binary string and want to transform it into sorted order, which for a binary string means that all 0s appear before all 1s. One operation allows us to choose a subsequence whose values are non-increasing."
date: "2026-06-10T08:09:22+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1605
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 754 (Div. 2)"
rating: 1000
weight: 1605
solve_time_s: 793
verified: false
draft: false
---

[CF 1605B - Reverse Sort](https://codeforces.com/problemset/problem/1605/B)

**Rating:** 1000  
**Tags:** greedy, sortings  
**Solve time:** 13m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string and want to transform it into sorted order, which for a binary string means that all `0`s appear before all `1`s.

One operation allows us to choose a subsequence whose values are non-increasing. Since the string contains only `0` and `1`, such a subsequence can only look like some number of `1`s followed by some number of `0`s. We then reverse the chosen subsequence in place.

The task is not only to determine the minimum number of operations, but also to output one valid sequence of operations achieving that minimum.

The constraints are very small. The total length of all strings is at most 1000, so even quadratic work per test case would be acceptable. The real challenge is discovering the structure of the operation.

A subtle point is that we are working with subsequences, not substrings. The chosen positions do not need to be consecutive.

Consider the string `0011111`. It is already sorted. Any solution that always performs an operation would be incorrect because the minimum number of operations is zero.

Consider `10100`. The misplaced characters are the leftmost `1` that should move right and the rightmost `0`s that should move left. A naive strategy that swaps adjacent characters would work but would not respect the operation defined in the problem.

Consider `111000`. The string is far from sorted, but a single carefully chosen operation is enough. Missing this observation leads to solutions that use unnecessarily many operations.

## Approaches

A brute-force viewpoint is to think about repeatedly fixing inversions. An inversion is a pair where a `1` appears before a `0`. One could try to move characters around until the string becomes sorted. Such approaches are unnecessary and do not exploit the special structure of the operation.

The key observation comes from examining what a valid subsequence looks like in a binary string. Since the subsequence must be non-increasing, it can contain any collection of `1`s and any collection of `0`s that appear later. When that subsequence is reversed, every chosen `1` moves toward the right side and every chosen `0` moves toward the left side.

Now compare the string with its sorted version. Every position where the current string contains `1` but the sorted string contains `0` is a misplaced `1`. Similarly, every position where the current string contains `0` but the sorted string contains `1` is a misplaced `0`.

All misplaced `1`s occur before all misplaced `0`s. If we collect exactly those positions into one subsequence, then the subsequence consists of some `1`s followed by some `0`s, which satisfies the operation requirement. Reversing it places every selected character into a correct position immediately.

This means that every non-sorted string can be fixed in exactly one operation. If the string is already sorted, we need zero operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulate inversion fixing | O(n²) | O(n) | Unnecessary |
| Compare with sorted string | O(n log n) | O(n) | Accepted |

Since the alphabet is only `{0,1}`, even the sorting step can be replaced by counting zeros, but the standard implementation with sorting is already more than fast enough.

## Algorithm Walkthrough

1. For the current string, create its sorted version.
2. Find every index where the original string differs from the sorted string.
3. Store all such indices.
4. If there are no differing indices, the string is already sorted. Output `0`.
5. Otherwise, output `1` because one operation is sufficient.
6. Output the collected indices as the chosen subsequence.

The reason step 6 works is that every mismatched position on the left side contributes a `1` that must move right, while every mismatched position on the right side contributes a `0` that must move left. The collected subsequence is therefore a sequence of `1`s followed by `0`s, which is valid for the operation.

### Why it works

Let `t` be the sorted version of the string.

Whenever `s[i] != t[i]`, the character at position `i` must participate in any successful transformation. Since the number of `0`s and `1`s is unchanged, mismatched positions naturally split into two groups: positions containing extra `1`s and positions containing extra `0`s.

All extra `1`s lie before all extra `0`s. Therefore the characters at the mismatched positions form a non-increasing subsequence. Reversing this subsequence swaps the two groups and places every mismatched position into its correct value. After the reversal, the entire string becomes equal to `t`.

Thus one operation is sufficient whenever the string is not already sorted, and zero operations are necessary when it is already sorted. This is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        target = ''.join(sorted(s))

        pos = []
        for i in range(n):
            if s[i] != target[i]:
                pos.append(i + 1)

        if not pos:
            print(0)
        else:
            print(1)
            print(len(pos), *pos)

solve()
```

The solution first builds the sorted target string. Every position where the original string differs from the target must be corrected. Those positions are exactly the indices used in the single operation.

The indices are printed in increasing order, which is required because they form a subsequence. The problem uses one-based indexing, so each position is reported as `i + 1`.

The most common implementation mistake is forgetting the one-based conversion. Another common mistake is trying to output multiple operations even though one operation is always enough for every non-sorted binary string.

## Worked Examples

### Example 1

Input string:

`10100`

Sorted version:

`00011`

| Position | Original | Sorted | Different? |
| --- | --- | --- | --- |
| 1 | 1 | 0 | Yes |
| 2 | 0 | 0 | No |
| 3 | 1 | 0 | Yes |
| 4 | 0 | 1 | Yes |
| 5 | 0 | 1 | Yes |

Chosen indices:

`[1, 3, 4, 5]`

Output:

`1`

`4 1 3 4 5`

The selected characters are `1 1 0 0`, which is non-increasing. Reversing them produces `0 0 1 1`, fixing all mismatches at once.

### Example 2

Input string:

`0011111`

Sorted version:

`0011111`

| Position | Original | Sorted | Different? |
| --- | --- | --- | --- |
| 1 | 0 | 0 | No |
| 2 | 0 | 0 | No |
| 3 | 1 | 1 | No |
| 4 | 1 | 1 | No |
| 5 | 1 | 1 | No |
| 6 | 1 | 1 | No |
| 7 | 1 | 1 | No |

There are no mismatches.

Output:

`0`

This demonstrates the minimum-operation case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the binary string |
| Space | O(n) | Target string and mismatch indices |

The total input size is at most 1000 characters across all test cases. Even an O(n²) solution would fit comfortably, so O(n log n) is easily within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    data = io.StringIO(inp)

    def input():
        return data.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        target = ''.join(sorted(s))
        pos = [i + 1 for i in range(n) if s[i] != target[i]]

        if not pos:
            out.append("0")
        else:
            out.append("1")
            out.append(str(len(pos)) + " " + " ".join(map(str, pos)))

    return "\n".join(out)

# sample-style checks
assert run("1\n7\n0011111\n") == "0"

# already sorted
assert run("1\n1\n0\n") == "0"

# all ones
assert run("1\n5\n11111\n") == "0"

# reverse-sorted binary string
assert run("1\n6\n111000\n").splitlines()[0] == "1"

# alternating pattern
assert run("1\n4\n1010\n").splitlines()[0] == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `0 operations` | Minimum size |
| `11111` | `0 operations` | All equal characters |
| `111000` | `1 operation` | Maximum mismatch concentration |
| `1010` | `1 operation` | Alternating pattern |
| `0011111` | `0 operations` | Already sorted string |

## Edge Cases

Consider the input `1` followed by the string `0`. The sorted version is identical, so the mismatch set is empty. The algorithm outputs zero operations immediately.

Consider the string `111000`. The sorted version is `000111`. Every position differs, so all six indices are selected. The chosen subsequence is `1 1 1 0 0 0`, which is non-increasing. Reversing it directly produces the sorted string.

Consider the string `001011`. The sorted version is `000111`. The mismatches occur only at the middle positions. Selecting exactly those positions avoids touching characters that are already correct, and one reversal fixes the string completely.

These cases illustrate the central invariant: the mismatch positions always form a valid non-increasing subsequence, and reversing that subsequence resolves every mismatch simultaneously.
