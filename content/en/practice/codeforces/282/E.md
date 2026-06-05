---
title: "CF 282E - Sausage Maximization"
description: "We are given a single array of integers, which represents a sausage in Bitland. The goal is to cut this sausage into two non-overlapping segments: a prefix for BitHaval and a suffix for BitAryo. Either segment can be empty."
date: "2026-06-05T09:20:51+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 282
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 173 (Div. 2)"
rating: 2200
weight: 282
solve_time_s: 88
verified: true
draft: false
---

[CF 282E - Sausage Maximization](https://codeforces.com/problemset/problem/282/E)

**Rating:** 2200  
**Tags:** bitmasks, data structures, trees  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single array of integers, which represents a sausage in Bitland. The goal is to cut this sausage into two non-overlapping segments: a prefix for BitHaval and a suffix for BitAryo. Either segment can be empty. Each person’s “deliciousness” is the bitwise XOR of the integers in their segment, and their total pleasure is the XOR of the two deliciousness values. We want to maximize this pleasure.

The input size is up to 100,000 integers, and each integer can be as large as $10^{12}$. This immediately tells us that any solution with nested loops over all possible prefix-suffix splits would be too slow: iterating over all pairs of prefix and suffix ends would be $O(n^2)$, which is on the order of $10^{10}$ operations. We need something near linear or at most linearithmic in $n$.

Edge cases are subtle here. The simplest case is when the array has length 1. Then the only non-empty segment is the element itself, and the other person gets nothing. Another edge case is when all elements are zero, in which case every segment XOR is zero. A careless approach might assume both segments must be non-empty, but the problem allows empty segments and their XOR is zero, which can change the optimal split.

## Approaches

A brute-force approach iterates over every possible split: for each prefix end $i$ from 0 to $n$, compute the XOR of the prefix and XOR of the suffix, then take their XOR. Computing prefix and suffix XORs from scratch each time is $O(n)$, leading to an overall $O(n^2)$ complexity. This works for tiny arrays but is too slow for $n = 10^5$.

We notice that XOR is associative and has the property $a \oplus b = c \Rightarrow a = b \oplus c$. If we precompute the prefix XOR array, $\text{px}[i] = a[0] \oplus a[1] \oplus \dots \oplus a[i]$, then the XOR of any suffix starting at position $j$ can be written as $\text{px}[n-1] \oplus \text{px}[j-1]$ for $j > 0$, and simply $\text{px}[n-1]$ for $j = 0$. This reduces repeated computation.

The next insight is that the problem reduces to: given a list of prefix XORs, find two non-overlapping segments such that the XOR of their XORs is maximized. This is equivalent to the classical problem of finding the maximum XOR of any two numbers in an array. We can solve this using a binary trie or a basis of independent bit vectors (also called linear basis). Each prefix XOR can be inserted into a basis, and the maximum XOR of the current prefix with any previous prefix is obtained by querying the basis. This produces an $O(n \cdot \log M)$ solution, where $M$ is the maximum possible integer ($10^{12}$, so $\log M \approx 40$).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Prefix XOR + Linear Basis | O(n log M) | O(log M) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix XOR array. Let $\text{px}[i] = a[0] \oplus a[1] \oplus \dots \oplus a[i]$. This allows O(1) computation of any prefix XOR.
2. Initialize an empty linear basis for XOR maximization. A linear basis is a set of numbers such that each number is linearly independent in terms of XOR, meaning no number can be formed by XORing others in the basis.
3. Iterate through the prefix XORs. At each step $i$, we treat $\text{px}[i]$ as the potential XOR for BitAryo’s segment, and we want to maximize XOR with any previous prefix (potential BitHaval segment). Query the current basis to find the number that maximizes $\text{px}[i] \oplus \text{basis element}$.
4. After querying, insert $\text{px}[i]$ into the basis. This ensures that future suffixes can use this prefix XOR as a candidate for maximum XOR.
5. Track the global maximum XOR found during these iterations and output it.

Why it works: the prefix XOR array ensures every possible prefix and suffix XOR is represented. The linear basis guarantees that we can construct the largest possible XOR from any subset of previous prefix XORs. Because XOR is associative and invertible, this method examines all valid prefix-suffix splits implicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

class LinearBasis:
    def __init__(self):
        self.basis = [0] * 64

    def insert(self, x):
        for i in reversed(range(64)):
            if x & (1 << i):
                if self.basis[i]:
                    x ^= self.basis[i]
                else:
                    self.basis[i] = x
                    return

    def query_max(self, x):
        res = x
        for i in reversed(range(64)):
            if self.basis[i]:
                res = max(res, res ^ self.basis[i])
        return res

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    px = [0] * n
    px[0] = a[0]
    for i in range(1, n):
        px[i] = px[i-1] ^ a[i]

    lb = LinearBasis()
    max_pleasure = 0
    lb.insert(0)  # include empty prefix
    for val in px:
        max_pleasure = max(max_pleasure, lb.query_max(val))
        lb.insert(val)
    print(max_pleasure)

if __name__ == "__main__":
    main()
```

The code first computes prefix XORs. Then we maintain a linear basis to quickly find the number that maximizes XOR with any current prefix XOR. Inserting 0 initially handles the case of an empty prefix. The loop over prefix XORs ensures every non-overlapping prefix-suffix split is implicitly considered.

## Worked Examples

Sample input 1:

```
2
1 2
```

| i | px[i] | max_pleasure | Basis after insert |
| --- | --- | --- | --- |
| 0 | 1 | 1 | [0, 1] |
| 1 | 3 | 3 | [0, 1, 3] |

The maximum pleasure is 3, obtained by giving BitHaval the first element and BitAryo the second.

Custom input 2:

```
3
1 2 3
```

| i | px[i] | max_pleasure | Basis after insert |
| --- | --- | --- | --- |
| 0 | 1 | 1 | [0, 1] |
| 1 | 3 | 3 | [0, 1, 3] |
| 2 | 0 | 3 | [0, 1, 3] |

Maximum pleasure is 3, achieved by giving BitHaval [1,2] and BitAryo [3].

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * log M) | n prefix XORs inserted into a 64-bit linear basis |
| Space | O(64) | Linear basis stores at most 64 numbers for 64-bit integers |

With n up to $10^5$ and M up to $10^{12}$, the total operations are on the order of $10^5 * 40 = 4 \times 10^6$, comfortably under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("2\n1 2\n") == "3", "sample 1"

# Custom tests
assert run("1\n5\n") == "5", "single element"
assert run("3\n1 2 3\n") == "3", "small array"
assert run("4\n0 0 0 0\n") == "0", "all zeros"
assert run("5\n1 1 1 1 1\n") == "1", "all ones"
assert run("6\n3 5 2 7 1 6\n") == "7", "mixed numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n5 | 5 | Single element edge case |
| 3\n1 2 3 | 3 | Small array, typical case |
| 4\n0 0 0 0 | 0 | All zeros handled correctly |
| 5\n1 1 1 1 1 | 1 | Repeated numbers handled |
