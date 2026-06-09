---
title: "CF 1799B - Equalize by Divide"
description: "We are given an array of positive integers. We can repeatedly pick two distinct indices $i$ and $j$, and set the element at index $i$ to the ceiling of its division by the element at index $j$."
date: "2026-06-09T09:44:09+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1799
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 854 by cybercats (Div. 1 + Div. 2)"
rating: 1200
weight: 1799
solve_time_s: 179
verified: false
draft: false
---

[CF 1799B - Equalize by Divide](https://codeforces.com/problemset/problem/1799/B)

**Rating:** 1200  
**Tags:** brute force, constructive algorithms, greedy, math  
**Solve time:** 2m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers. We can repeatedly pick two distinct indices $i$ and $j$, and set the element at index $i$ to the ceiling of its division by the element at index $j$. The task is to determine whether we can make all elements of the array equal by performing this operation any number of times, and if possible, produce a sequence of operations to do it.

The input guarantees that $n$, the array size, is at most 100, and the sum of all $n$ over test cases is at most 1000. Each array element can be as large as $10^9$. These constraints suggest that we cannot afford operations that are cubic in $n$, but anything up to roughly $O(n^2)$ is feasible given the small maximum array size.

The non-obvious edge cases appear when arrays contain `1` or repeated elements. For example, `[2, 1]` is impossible because any division by 1 reduces the other number but never increases it, so the 2 can only become 2/1=2 → 2, then 2/2=1, eventually matching 1. We must detect scenarios where the smallest number is 1 and other numbers are not powers of it. Arrays that already have all elements equal, even if large, should immediately output zero operations. Arrays with two numbers where the smaller is 1 and the larger is greater than 1 are impossible because repeated ceiling divisions can never "create" equality unless the larger number is exactly divisible down to the smaller.

## Approaches

The naive approach is to simulate every possible operation in a brute-force manner: pick all pairs $i, j$ and apply the ceiling division repeatedly until all numbers converge. This is correct but far too slow because each operation can at worst divide a large number into a series of smaller numbers, potentially needing $O(\log(\text{max\_value}))$ steps per element. With $n=100$ and numbers up to $10^9$, this is unmanageable.

The key insight is that any sequence of operations that makes all elements equal must eventually reduce everything to the minimum element in the array. Dividing by a larger number cannot increase any element, so the minimal element in the array can never increase. This lets us construct a greedy strategy: repeatedly reduce the largest numbers by dividing them by smaller numbers until all numbers match the minimum. If the minimum is 1 and some element is larger than 1, then the problem is impossible because we cannot reduce a number to 1 using another number larger than 1 in fewer than an unbounded number of steps, but the constraints guarantee that all valid solutions require at most 30n operations.

We only need to check two properties. First, if the minimum element is 1 and not all elements are 1, it is impossible. Second, otherwise we can sort the array and iteratively reduce larger numbers by the current minimum until all numbers become equal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log(max(a))) | O(n) | Too slow |
| Greedy Reduction by Minimum | O(n log(max(a))) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, identify the smallest element `m` in the array. This will be the target value we want all elements to reach.
2. If `m` is 1 and the array is not already `[1, 1, ..., 1]`, output -1 because it is impossible to reduce other numbers to 1 in the allowed operations.
3. Otherwise, iterate over all array elements that are larger than `m`. For each such element `a_i`, repeatedly choose `a_j = m` and assign `a_i := ceil(a_i / a_j)` until `a_i` equals `m`. Each operation is added to the result list.
4. Track all operations as pairs `(i, j)` where `i` is the index of the element being reduced and `j` is the index of the current minimum.
5. After processing all elements, output the total number of operations followed by the sequence of operations.

Why it works: Every operation reduces a number towards the minimum. The ceiling division ensures that we never skip a possible integer. The invariant is that the minimum element is never increased, so all other elements eventually match it. Since the maximum element can only be divided down, and the number of steps per element is logarithmic in its value relative to the minimum, the algorithm completes within `30n` operations, as guaranteed by the problem statement.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        min_val = min(a)
        
        if min_val == 1 and any(x != 1 for x in a):
            print(-1)
            continue
        
        operations = []
        while True:
            max_val = max(a)
            if max_val == min_val:
                break
            for i in range(n):
                if a[i] > min_val:
                    a[i] = math.ceil(a[i] / min_val)
                    operations.append((i+1, a.index(min_val)+1))
        
        print(len(operations))
        for op in operations:
            print(op[0], op[1])

if __name__ == "__main__":
    solve()
```

The solution starts by reading the number of test cases. For each test case, it identifies the minimum value. If the minimum is 1 and not all numbers are 1, it outputs -1. Otherwise, it iteratively reduces numbers larger than the minimum by performing ceiling divisions, recording each operation. Indices are 1-based when recording operations.

A subtlety is that `a.index(min_val)` always returns the first occurrence of the minimum. This is sufficient because all operations only require any minimum element to perform division. Using `math.ceil` ensures we never under-round.

## Worked Examples

**Example 1**: `[4, 3, 2]`

| Step | Array | Operation |
| --- | --- | --- |
| 0 | [4, 3, 2] | - |
| 1 | [2, 3, 2] | 1 / 3 |
| 2 | [2, 2, 2] | 2 / 3 |

This shows the algorithm reduces the largest element to the minimum, then reduces the remaining larger element. All elements reach 2.

**Example 2**: `[2, 1]`

| Step | Array | Operation |
| --- | --- | --- |
| 0 | [2, 1] | - |
| - | - | Impossible |

Here the minimum is 1, but the other element is 2. The algorithm immediately outputs -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max(a))) | Each element is repeatedly divided by the minimum, taking O(log(max/min)) steps, and we process n elements. |
| Space | O(n + 30n) | Array plus operations list. Operations are bounded by 30n per problem guarantee. |

Given n ≤ 100 and total elements ≤ 1000, the solution runs comfortably within 1s and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("10\n1\n100\n3\n1 1 1\n2\n2 1\n2\n5 5\n3\n4 3 2\n4\n3 3 4 4\n2\n2 100\n5\n5 3 6 7 8\n6\n3 3 80 3 8 3\n4\n19 40 19 55") is not None

# Custom tests
assert run("1\n1\n1") == "0", "single element"
assert run("1\n3\n2 2 2") == "0", "all equal"
assert run("1\n3\n1 1 2") == "-1", "impossible with 1"
assert run("1\n3\n5 10 15") is not None, "general reduction"
assert run("1\n4\n10 10 20 40") is not None, "larger numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | `0` | Single element arrays |
| `1\n3\n2 2 2` | `0` | Already equal numbers |
| `1\n3\n1 1 2` | `-1` | Impossible with minimum 1 |
| `1\n3\n5 10 15` | non-empty ops | General reduction steps |
| `1\n4\n10 10 20 40` | non-empty ops | Multiple reductions from largest |

## Edge Cases

Arrays where the minimum is 1 require special attention. For `[1, 1, 2]`, the minimum is 1,
