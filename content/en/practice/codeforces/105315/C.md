---
title: "CF 105315C - Iyaad's Birthday"
description: "We are given several independent experiments. In each experiment, there is a reference integer $D$ that represents the DNA of a specific cat, and a list of other cats represented by integers $ai$. Each integer encodes genetic traits as bits."
date: "2026-06-23T15:05:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105315
codeforces_index: "C"
codeforces_contest_name: "JPC 4.0"
rating: 0
weight: 105315
solve_time_s: 48
verified: true
draft: false
---

[CF 105315C - Iyaad's Birthday](https://codeforces.com/problemset/problem/105315/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent experiments. In each experiment, there is a reference integer $D$ that represents the DNA of a specific cat, and a list of other cats represented by integers $a_i$. Each integer encodes genetic traits as bits.

A cat is considered related to the reference cat if there exists at least one bit position where both $a_i$ and $D$ have a 1. In bitwise terms, this means the bitwise AND of the two numbers is non-zero. The task is simply to count how many values in each test case satisfy this condition.

Each test case can contain up to $2 \cdot 10^5$ numbers, and across all test cases up to $10^6$. This immediately rules out anything quadratic in $n$, since even a linear scan per test case is already the only viable structure. The operation we perform per element must be constant time.

A subtle edge case appears when $a_i = 0$. Since $0 \& D = 0$, such elements are never counted, regardless of $D$. Another edge case occurs when $D = 0$. In that case, no number can share a set bit with $D$, so the answer is always zero, even if all $a_i$ are non-zero. These cases are easy to mishandle if one assumes every positive number automatically shares a bit.

## Approaches

The most direct approach is to check every cat individually. For each $a_i$, compute $a_i \& D$ and increment a counter if the result is non-zero. This is correct because the definition of relatedness is exactly that condition.

The cost of this approach is linear in the total number of integers across all test cases. Each bitwise AND is constant time on 32-bit or 64-bit integers, so the total complexity is $O(\sum n)$, which is at most $10^6$. This is comfortably fast within a one-second limit in Python if implemented with fast input.

There is no deeper structure to exploit because each element is independent. Any attempt to preprocess or group values does not reduce work further, since the condition depends on a fixed bitmask $D$ applied separately to each value. The key realization is that the problem is already minimal: it is a streaming filter over a bit condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (per element AND check) | O(n) per test case | O(1) extra | Accepted |
| Optimal (same idea, fast I/O) | O(total n) | O(1) extra | Accepted |

## Algorithm Walkthrough

We process each test case independently. The goal in each case is to count how many values share at least one set bit with $D$.

1. Read $n$ and $D$ for the test case. This defines the fixed bitmask we will compare against.
2. Initialize a counter to zero. This will accumulate all qualifying cats.
3. Iterate through each value $a_i$ in the list.
4. Compute $a_i \& D$. If the result is not zero, increment the counter. This check directly encodes whether the two bitmasks intersect.
5. After processing all values, output the counter.

Each step is necessary because there is no way to infer the result for one element from another; the condition is purely local to each pair $(a_i, D)$.

### Why it works

The correctness rests on the fact that bitwise AND isolates shared set bits. If two numbers share at least one bit position where both have a 1, their AND must be non-zero. Conversely, if the AND is zero, no bit position is shared, meaning they are unrelated by the problem definition. Since we test every element exactly once and the condition is both necessary and sufficient, the final count is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, D = map(int, input().split())
        arr = list(map(int, input().split()))
        
        ans = 0
        for x in arr:
            if x & D:
                ans += 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution is structured as a straightforward streaming loop over test cases. Fast input via `sys.stdin.readline` is essential because the total number of integers can reach one million. The expression `x & D` is the core operation; it directly encodes the relationship condition without any extra computation.

No additional preprocessing or storage beyond the current test case is needed, which keeps memory usage constant relative to input size.

## Worked Examples

Consider the input:

```
1
4 12
1 6 8 5
```

Here $D = 12$, which in binary is `1100`.

| i | a_i | a_i (binary) | a_i & D | Count |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0001 | 0000 | 0 |
| 2 | 6 | 0110 | 0100 | 1 |
| 3 | 8 | 1000 | 1000 | 2 |
| 4 | 5 | 0101 | 0100 | 3 |

The final answer is 3. This shows that even partial overlap of bits is sufficient, not full containment.

Now consider a second case:

```
1
3 0
7 1 15
```

| i | a_i | a_i & D | Count |
| --- | --- | --- | --- |
| 1 | 7 | 0 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 15 | 0 | 0 |

Since $D = 0$, no number can share a set bit with it. The answer is always zero, even though all $a_i$ are positive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑n) | Each element is checked once with a constant-time bitwise operation |
| Space | O(1) | Only a counter is maintained per test case |

The total input size constraint of $10^6$ integers fits easily within this linear scan approach. Each operation is a single CPU-friendly bitwise AND, so the solution runs comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys

    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue()

def solve():
    t = int(input())
    for _ in range(t):
        n, D = map(int, input().split())
        arr = list(map(int, input().split()))
        ans = 0
        for x in arr:
            if x & D:
                ans += 1
        print(ans)

# provided samples
assert run("1\n4 12\n1 6 8 5\n") == "3\n"
assert run("1\n3 0\n7 1 15\n") == "0\n"

# custom cases
assert run("1\n1 8\n0\n") == "0\n"
assert run("1\n5 7\n1 2 4 8 15\n") == "4\n"
assert run("1\n3 1\n2 4 8\n") == "0\n"
assert run("2\n2 3\n1 2\n3 4\n1 2 3\n") == "2\n0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero with non-zero D | 0 | ensures zero values are never counted |
| mixed bits with small mask | 4 | checks multiple overlapping matches |
| no overlap case | 0 | ensures correct handling when all AND results are zero |
| multiple test cases | 2 0 | verifies per-testcase independence |

## Edge Cases

One important edge case is when $D = 0$. For input:

```
1
4 0
1 2 3 4
```

The algorithm computes $x \& 0 = 0$ for every element. The loop still runs over all elements, but the counter never increases. The output is 0, which matches the definition since no bit overlap is possible.

Another edge case is when all $a_i = 0$:

```
1
3 5
0 0 0
```

Each iteration evaluates `0 & 5 = 0`, so the counter remains zero throughout. The algorithm handles this naturally without special casing.

A final subtle case is when $D$ has only one bit set, for example $D = 1$. Only odd numbers should be counted:

```
1
5 1
2 3 4 5 6
```

The algorithm correctly counts only 3 and 5, since only they have the least significant bit set.
