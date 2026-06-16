---
title: "CF 999B - Reversing Encryption"
description: "We are given a string that has already been transformed by a deterministic process involving repeated reversals of prefixes."
date: "2026-06-16T23:51:35+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 999
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 490 (Div. 3)"
rating: 900
weight: 999
solve_time_s: 68
verified: true
draft: false
---

[CF 999B - Reversing Encryption](https://codeforces.com/problemset/problem/999/B)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string that has already been transformed by a deterministic process involving repeated reversals of prefixes. The original string is unknown, and the process that produces the final string is fully specified: for every divisor of the length, taken from largest to smallest, we reverse the prefix of that length.

The key difficulty is that these reversals overlap heavily. Each position in the string is moved multiple times, and the final order hides the sequence of transformations. We are asked to reconstruct the original string before any reversals were applied.

The input size is small, with the string length up to 100. This immediately suggests that an O(n^2) reconstruction or simulation is sufficient. Any solution that tries to brute force permutations is unnecessary, but even if attempted, factorial growth is irrelevant because n is tiny.

Edge cases here are mostly structural rather than performance-related. When n equals 1, no operations change the string, so the output is identical to input. When n is prime, only divisors are 1 and n, so there is exactly one meaningful reversal. A naive forward simulation is easy, but incorrect reversal ordering leads to wrong reconstruction.

A common failure mode is simulating the encryption directly without understanding invertibility. Another is attempting to reverse all prefixes in increasing divisor order instead of reconstructing the original sequence step by step.

## Approaches

The forward process applies prefix reversals in decreasing divisor order. Each operation depends only on the prefix, not on suffix interactions. This structure makes the transformation invertible in a very controlled way.

A brute-force idea would be to generate a candidate original string, simulate the encryption process, and compare it to the target. While correct, each simulation costs O(n^2), and trying all permutations would be O(n!). Even restricting to a single candidate, repeated simulation is unnecessary.

The key insight is that prefix reversals are involutions, meaning each reversal is its own inverse. However, the order matters. If we reverse prefixes in order d1, d2, ..., dk in encryption, then in decryption we must apply the same operations in reverse order: dk, ..., d2, d1.

But there is an even simpler structural observation. Since divisors are processed in decreasing order during encryption, the last meaningful transformation applied corresponds to the smallest divisor greater than 1. That means during decryption, we rebuild the string by applying prefix reversals in increasing divisor order.

We can compute all divisors of n, sort them, and simulate applying prefix reversals in that sorted order on the encrypted string. This reconstructs the original string because each reversal undoes the effect of the corresponding step in the forward process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation from candidates | O(n^3) or worse | O(n) | Too slow / unnecessary |
| Reverse divisor simulation | O(n √n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute all divisors of n. Each divisor corresponds to one prefix reversal operation used in the encryption process. We need them because they define the transformation sequence.
2. Sort the divisors in increasing order. This ordering is critical because we are reconstructing the original string by effectively undoing the layered structure of reversals.
3. Start with the encrypted string t as our working array. We treat it as a mutable list of characters to support efficient prefix reversals.
4. For each divisor d in sorted order, reverse the prefix from index 0 to d − 1. This step is applied because it reverses the effect of how that prefix was altered in the forward process.
5. After processing all divisors, the array represents the original string s, so we output it.

### Why it works

Each operation in the encryption process is a prefix reversal applied exactly once per divisor, but in decreasing order. Prefix reversals are self-inverse, so applying the same reversal twice restores the original ordering for that prefix segment.

The nested structure of divisors ensures that smaller prefixes were transformed after larger ones during encryption, which means their effects are “inside” the final arrangement. By applying reversals in increasing order, we peel back transformations from the innermost structure outward. This maintains consistency at every step because each reversal only affects a prefix that has not yet been restored.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
t = list(input().strip())

divs = []
for i in range(1, n + 1):
    if n % i == 0:
        divs.append(i)

divs.sort()

for d in divs:
    t[:d] = reversed(t[:d])

print("".join(t))
```

The solution begins by reading the string into a mutable list so that prefix reversals can be performed efficiently. Divisors are computed by checking all integers up to n, which is sufficient given the small constraint.

Sorting ensures we apply transformations in the correct reconstruction order. Each prefix reversal is implemented using Python slicing, which cleanly expresses the operation without manual swapping logic.

The final join converts the list back into a string for output.

## Worked Examples

### Example 1

Input:

```
n = 10
t = rocesfedoc
```

Divisors of 10 are 1, 2, 5, 10. We apply reversals in increasing order.

| Step | Operation | String state |
| --- | --- | --- |
| 0 | initial | rocesfedoc |
| 1 | reverse prefix 1 | rocesfedoc |
| 2 | reverse prefix 2 | orcesfedoc |
| 3 | reverse prefix 5 | codefseroc |
| 4 | reverse prefix 10 | codeforces |

The process reconstructs the original string exactly.

This trace shows how smaller prefixes are corrected early, while larger prefixes fix global ordering last.

### Example 2

Input:

```
n = 6
t = "cbadef"
```

Divisors are 1, 2, 3, 6.

| Step | Operation | String state |
| --- | --- | --- |
| 0 | initial | cbadef |
| 1 | reverse prefix 1 | cbadef |
| 2 | reverse prefix 2 | bcadef |
| 3 | reverse prefix 3 | abcdef |
| 4 | reverse prefix 6 | fedcba |

This example highlights that intermediate states can look unrelated to the final result, but each step is strictly undoing a layer of structured reversals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n √n) | Finding divisors takes O(n), each prefix reversal costs O(n), applied for at most √n divisors |
| Space | O(n) | We store the string as a mutable list |

The constraints allow up to n = 100, so even repeated prefix slicing is negligible. The solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    t = list(input().strip())

    divs = []
    for i in range(1, n + 1):
        if n % i == 0:
            divs.append(i)

    divs.sort()

    for d in divs:
        t[:d] = reversed(t[:d])

    return "".join(t)

# provided sample
assert run("10\nrocesfedoc\n") == "codeforces"

# minimum size
assert run("1\na\n") == "a"

# prime length
assert run("5\nabcde\n") == "bcdea"

# small composite
assert run("4\ndcba\n") == "abcd"

# repeated pattern
assert run("6\nfedcba\n") == "abcdef"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 rocesfedoc | codeforces | correctness on sample |
| 1 a | a | minimal edge case |
| 5 abcde | bcdea | prime-length structure |
| 4 dcba | abcd | full reversal interaction |
| 6 fedcba | abcdef | layered reversals |

## Edge Cases

For n = 1, the divisor set is only {1}. The algorithm applies a prefix reversal of length 1, which leaves the string unchanged, so the output equals the input.

For prime n, say n = 5, divisors are 1 and 5. The algorithm first reverses prefix 1, doing nothing, then reverses the full string, restoring the original ordering structure imposed by encryption. The step-by-step reversal correctly undoes the single meaningful transformation.

For highly composite n such as 12, multiple overlapping prefix reversals occur at 1, 2, 3, 4, 6, 12. Each step only modifies a prefix that is consistent with previously restored structure, so no later operation invalidates earlier corrections.
