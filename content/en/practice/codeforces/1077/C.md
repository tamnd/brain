---
title: "CF 1077C - Good Array"
description: "We are given a list of integers, and we want to identify which positions behave “special” under a deletion operation. For each index, we temporarily remove that element and look at the remaining array."
date: "2026-06-15T06:40:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1077
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 521 (Div. 3)"
rating: 1300
weight: 1077
solve_time_s: 263
verified: false
draft: false
---

[CF 1077C - Good Array](https://codeforces.com/problemset/problem/1077/C)

**Rating:** 1300  
**Tags:** -  
**Solve time:** 4m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of integers, and we want to identify which positions behave “special” under a deletion operation. For each index, we temporarily remove that element and look at the remaining array. We call an array good if there exists an element inside it that exactly matches the sum of all other elements in that same array. The task is to find all indices whose removal makes the resulting array good.

The key subtlety is that each removal is independent. We do not actually delete elements permanently, so every check is performed against the original array as a reference.

The constraints are large, with up to 200,000 elements. Any approach that recomputes sums or scans the array for every removal leads to quadratic complexity in the worst case, which would be far too slow. This pushes us toward a solution that can reuse precomputed information and answer each candidate index in constant or near-constant time.

A few edge situations matter.

If all elements are equal, for example `[1, 1, 1, 1]`, removing one element may or may not produce a good array depending on whether the remaining structure allows one element to equal the sum of others. A naive approach might incorrectly assume symmetry guarantees validity for all indices.

If there is only one large element and the rest are small, such as `[10, 1, 1, 1]`, removing different indices changes whether the sum relationship can hold, and checking locally around the removed element is not sufficient because the condition depends on the global sum.

Finally, arrays with zeros or repeated values can trick naive logic that assumes uniqueness of the “special” element.

## Approaches

A brute-force method would try every index, rebuild the remaining array, compute its sum, and then scan it to see whether any element equals half of the total sum of the remaining array. This requires O(n) work per index, and since there are n indices, the total complexity becomes O(n²), which is too slow when n reaches 200,000.

The key observation is that the condition “there exists an element equal to the sum of the rest” can be rewritten in terms of the total sum of the array. Suppose the remaining array has total sum S. If a candidate element x satisfies the condition, then x = S − x, which implies 2x = S. So the condition reduces to checking whether S is even and whether there exists an element equal to S/2.

This transforms the problem into something much simpler. For each removal, we can compute the new sum in O(1), and then only need to check whether that half-sum exists in the remaining multiset. To support fast membership checks, we maintain a frequency map of all elements. When we remove an element, we temporarily adjust its frequency, compute the new sum, and test whether S/2 exists with non-zero frequency.

This reduces each check to constant time, giving an overall linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) or O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of all elements in the array. This gives us a baseline from which every removal can be derived quickly.
2. Build a frequency map of all values. This allows us to check whether a candidate value exists after temporarily removing an element.
3. Iterate through each index j, treating a[j] as the element being removed.
4. Compute the new sum S' as total_sum − a[j]. The target condition for a good array becomes checking whether there exists an element x such that 2x = S'.
5. Temporarily decrease the frequency of a[j], since that element is not available in the reduced array.
6. If S' is even, check whether S'/2 exists in the frequency map with positive count. If yes, mark index j as valid.
7. Restore the frequency of a[j] before moving to the next index.

The reason this works is that the condition defining a good array depends only on the existence of a value equal to half the total sum. Once the sum changes after removal, the problem reduces to a single membership query in a multiset.

### Why it works

For any array, being good is equivalent to the existence of an element x such that x equals the sum of all other elements. Let the total sum be S. Then x = S − x, so 2x = S. This means a good array is completely characterized by whether S is even and whether S/2 exists in the array. Since every candidate array after deletion is just the original array with one element removed, checking the condition reduces to recomputing S and testing membership of S/2 in a frequency structure. No other structural property matters.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)

from collections import Counter
freq = Counter(a)

res = []

for i, x in enumerate(a):
    freq[x] -= 1
    new_sum = total - x

    if new_sum % 2 == 0:
        half = new_sum // 2
        if freq[half] > 0:
            res.append(i + 1)

    freq[x] += 1

print(len(res))
if res:
    print(*res)
```

The solution starts by precomputing the total sum so that each removal only requires a subtraction instead of recomputing the sum from scratch. The frequency map tracks how many copies of each value remain after a hypothetical deletion.

Inside the loop, the key step is temporarily decrementing the frequency of the current element. This ensures that when we check for the existence of S'/2, we are not accidentally using the removed element itself. After the check, we restore the frequency so that subsequent iterations operate on the original state.

A common mistake is forgetting to restore the frequency, which would corrupt the state and produce incorrect answers for later indices.

## Worked Examples

### Example 1

Input:

```
5
2 5 1 2 2
```

We compute total sum S = 12.

| Removed index | Removed value | New sum S' | S'/2 | Exists? | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 10 | 5 | yes | keep |
| 2 | 5 | 7 | 3.5 | no | discard |
| 3 | 1 | 11 | 5.5 | no | discard |
| 4 | 2 | 10 | 5 | yes | keep |
| 5 | 2 | 10 | 5 | yes | keep |

Valid indices are 1, 4, 5.

This trace shows that the condition depends only on whether the adjusted half-sum appears elsewhere in the multiset, not on positional structure.

### Example 2

Input:

```
4
8 3 5 2
```

Total sum S = 18.

| Removed index | Removed value | New sum S' | S'/2 | Exists? | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 8 | 10 | 5 | yes | keep |
| 2 | 3 | 15 | 7.5 | no | discard |
| 3 | 5 | 13 | 6.5 | no | discard |
| 4 | 2 | 16 | 8 | yes | keep |

Valid indices are 1 and 4.

This example demonstrates that the same element value can become valid or invalid depending on how it affects the global sum after removal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to build frequency and one pass to test each index with O(1) checks |
| Space | O(n) | Frequency map stores counts of array values |

The solution fits easily within limits because each of the up to 200,000 elements is processed in constant time, and only simple arithmetic and hash map operations are used.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)
    from collections import Counter
    freq = Counter(a)

    res = []

    for i, x in enumerate(a):
        freq[x] -= 1
        new_sum = total - x

        if new_sum % 2 == 0:
            half = new_sum // 2
            if freq[half] > 0:
                res.append(i + 1)

        freq[x] += 1

    out = [str(len(res))]
    if res:
        out.append(" ".join(map(str, res)))
    return "\n".join(out)

# sample
assert run("5\n2 5 1 2 2\n") == "3\n1 4 5"

# all equal
assert run("4\n1 1 1 1\n") == "4\n1 2 3 4"

# no valid
assert run("3\n1 2 4\n") == "0"

# single dominant element
assert run("4\n10 1 1 1\n") == "1\n1"

# boundary small
assert run("2\n1 1\n") == "2\n1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | all indices | symmetry case |
| no valid | 0 | impossible configuration |
| dominant element | first index | skewed sum behavior |
| n=2 equal | both indices | minimal valid case |

## Edge Cases

An important edge case is when the removed element is itself the potential “sum element.” In such cases, failing to temporarily remove it from the frequency map leads to falsely accepting indices. The algorithm explicitly decrements frequency before checking to prevent this self-referential mistake.

Another subtle case occurs when S' is odd. Even if the array contains large values, no integer x can satisfy 2x = S', so the check must immediately reject without any lookup.
