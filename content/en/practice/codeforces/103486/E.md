---
title: "CF 103486E - Great Detective TJC"
description: "We are given several independent test cases. In each one, there is an array of positive integers, and the task is to determine whether we can pick two different positions such that the values at those positions differ by exactly one bit in binary, specifically their XOR equals 1."
date: "2026-07-03T06:20:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103486
codeforces_index: "E"
codeforces_contest_name: "The 15th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 103486
solve_time_s: 37
verified: true
draft: false
---

[CF 103486E - Great Detective TJC](https://codeforces.com/problemset/problem/103486/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each one, there is an array of positive integers, and the task is to determine whether we can pick two different positions such that the values at those positions differ by exactly one bit in binary, specifically their XOR equals 1.

Saying $A_i \oplus A_j = 1$ is very restrictive. XOR being 1 means that only the least significant bit differs between the two numbers, and every other bit is identical. In other words, one number must be exactly the other number with its last bit flipped. So valid pairs always look like $x$ and $x \oplus 1$.

The input size can be large across test cases, with up to $5 \times 10^5$ total elements. That immediately rules out any approach that compares all pairs, since even a single worst-case test with $10^5$ elements would already lead to about $10^{10}$ pair checks.

A subtle edge case appears when all numbers are identical. For example, if the array is $[7, 7, 7]$, no pair can work because $7 \oplus 7 = 0$, not 1. Another edge case is when numbers differ by more than one bit, for instance $[2, 3]$, where $2 \oplus 3 = 1$ works, but $[2, 4]$ does not, since $2 \oplus 4 = 6$.

The core difficulty is recognizing that the condition is not about arbitrary XOR structure, but about a very specific neighbor relationship between integers.

## Approaches

The most direct idea is to try all pairs $(i, j)$ and compute their XOR. This is correct because it exhaustively checks every possible candidate pair, and will certainly find a valid one if it exists. However, for $n = 10^5$, this requires roughly $5 \times 10^9$ operations in one test case, which is far beyond any feasible limit.

The key observation is that we do not actually need to compare arbitrary pairs. If a number $x$ participates in a valid pair, its partner must be exactly $x \oplus 1$. This turns the problem into a membership check problem rather than a pairing problem. Instead of searching for both ends by scanning, we can store all values in a hash-based structure and test whether each $x$ has its counterpart $x \oplus 1$ present in the array.

This reduces the problem from quadratic comparisons to constant-time lookups per element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Check | $O(n^2)$ | $O(1)$ | Too slow |
| Hash Set Lookup | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array and insert all elements into a hash set.

This allows constant-time membership queries for any value we might need to check.
2. Iterate through each element $x$ in the array.

For each value, compute $x \oplus 1$, which is the only possible value that can form a valid pair with $x$.
3. Check whether $x \oplus 1$ exists in the set.

If it does, we immediately know a valid pair exists and can stop processing the current test case.
4. If we finish scanning the array without finding any such pair, conclude that no valid indices exist.

The key design choice is to precompute membership in a set rather than attempting to search dynamically inside the array each time, which would repeatedly re-scan the structure.

### Why it works

The condition $A_i \oplus A_j = 1$ uniquely determines one value from the other. For any fixed $x$, there is exactly one candidate partner $x \oplus 1$, and no other value can satisfy the equation with $x$. This means every valid pair must appear as two elements that are direct complements under the transformation $x \mapsto x \oplus 1$. By checking all elements for the presence of their complement, we exhaust all possible valid constructions without duplication or omission.

## Python Solution

```
PythonRun
```

The solution reads each test case independently and builds a hash set of the array values. The crucial operation is the XOR with 1, which directly constructs the only possible partner value for each element. The loop terminates early as soon as a valid pair is found, which keeps runtime efficient in favorable cases.

One subtle point is that we do not need to worry about pairing an element with itself. Since $x \oplus x = 0$, self-pairs can never satisfy the condition, and the set lookup naturally avoids this unless $x \oplus 1 = x$, which never happens for integers.

## Worked Examples

Consider the input:

```

```

| x | x ⊕ 1 | in set? | decision |
| --- | --- | --- | --- |
| 2 | 3 | yes | found |

Here, 2 and 3 form a valid pair immediately because their XOR is 1. The algorithm stops as soon as it detects this relationship.

Now consider:

```
1
3
5 6 7
```

| x | x ⊕ 1 | in set? | decision |
| --- | --- | --- | --- |
| 5 | 4 | no | continue |
| 6 | 7 | yes | found |

In this case, the pair (6, 7) satisfies the condition, so the algorithm detects it when processing 6.

These traces show that we are not searching for arbitrary relationships, but only the single forced neighbor for each element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each element is inserted into a set and checked once |
| Space | $O(n)$ | The set stores all elements of the array |

The total number of elements across all test cases is bounded by $5 \times 10^5$, so the algorithm runs comfortably within limits. Hash-based membership checks keep each operation effectively constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        arr = list(map(int, input().split()))
        s = set(arr)
        ok = False
        for x in arr:
            if (x ^ 1) in s:
                ok = True
                break
        out.append("Yes" if ok else "No")
    return "\n".join(out)

# provided sample (illustrative)
assert run("1\n2\n2 3\n") == "Yes"

# all equal
assert run("1\n4\n7 7 7 7\n") == "No"

# single pair
assert run("1\n2\n4 5\n") == "Yes"

# no pair
assert run("1\n3\n1 2 4\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 7 7 7 | No | duplicates do not create false positives |
| 4 5 | Yes | minimal valid pair |
| 1 2 4 | No | unrelated values fail correctly |
| 2 3 | Yes | direct XOR=1 case |

## Edge Cases

For an array where all elements are identical, such as $[10, 10, 10]$, every check computes $10 \oplus 1 = 11$, which is not present in the set, so the algorithm correctly concludes there is no valid pair.

For a minimal input like $[0, 1]$, the check immediately finds that $0 \oplus 1 = 1$, and since both exist, the algorithm returns Yes without scanning further. This confirms that early t
