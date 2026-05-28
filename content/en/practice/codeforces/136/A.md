---
title: "CF 136A - Presents"
description: "We are given a party scenario where Petya invited n friends, each of whom gave exactly one gift to another friend. The input lists, for each friend in order, the friend they gave a gift to."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 136
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 97 (Div. 2)"
rating: 800
weight: 136
solve_time_s: 73
verified: true
draft: false
---

[CF 136A - Presents](https://codeforces.com/problemset/problem/136/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a party scenario where Petya invited _n_ friends, each of whom gave exactly one gift to another friend. The input lists, for each friend in order, the friend they gave a gift to. Our task is to invert this mapping: for each friend, we want to know who gave a gift to them.

Formally, the input consists of an integer _n_ and an array `p` of length _n_, where `p[i]` is the number of the friend who received a gift from friend `i + 1`. The output is an array `q` of length _n_ where `q[i]` is the friend who gave a gift to friend `i + 1`.

The constraint `1 ≤ n ≤ 100` is small, which means even an O(n²) solution would be fast enough. However, correctness is more subtle than efficiency. Each friend gives and receives exactly one gift, so the array `p` represents a permutation of the numbers 1 through _n_. This guarantees that the inverse mapping exists.

A common edge case is when a friend gives a gift to themselves. For instance, if `n = 3` and `p = [1, 2, 3]`, then each friend receives their own gift. The correct output should also reflect that each friend gave a gift to themselves: `q = [1, 2, 3]`. A naive approach that assumes no self-gifting could produce an incorrect mapping or fail to handle indices properly.

## Approaches

A brute-force approach iterates over all friends for each recipient. For friend `i`, we search through `p` to find the index `j` where `p[j] = i`. This works because each value in `p` is unique, guaranteeing a match. The time complexity is O(n²), which is acceptable for `n ≤ 100`. This method is conceptually simple but inefficient for larger arrays.

The key insight to optimize comes from recognizing that `p` is a permutation. Permutations can be inverted directly: if friend `i` gives a gift to friend `p[i]`, then friend `p[i]` received a gift from friend `i`. We can create an array `q` of size _n_ and assign `q[p[i] - 1] = i + 1` for all `i`. This approach is O(n) and only requires a single pass over the array, eliminating unnecessary nested loops.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted for this problem, inefficient for larger n |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of friends `n` and the array `p` representing who each friend gave a gift to.
2. Initialize an array `q` of length `n` to store the inverse mapping.
3. Iterate over all friends `i` from 0 to n - 1.
4. For each friend `i`, assign `q[p[i] - 1] = i + 1`. This step places the giver `i + 1` at the index corresponding to the receiver `p[i] - 1`.
5. After filling `q`, print it as space-separated integers.

This algorithm works because each friend gives exactly one gift and receives exactly one gift. The assignment `q[p[i] - 1] = i + 1` ensures that every position in `q` is filled once and correctly maps recipients to their givers. The uniqueness of the permutation guarantees no overwriting occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
p = list(map(int, input().split()))

q = [0] * n
for i in range(n):
    q[p[i] - 1] = i + 1

print(*q)
```

We read the number of friends and the permutation array using fast I/O. The array `q` is initialized with zeroes to store the inverse mapping. The loop assigns the correct giver for each recipient using 1-based indexing. Finally, we print the result with unpacking to match the required output format.

## Worked Examples

For input:

```
4
2 3 4 1
```

We initialize `q = [0, 0, 0, 0]`.

| i | p[i] | q after assignment |
| --- | --- | --- |
| 0 | 2 | [0, 1, 0, 0] |
| 1 | 3 | [0, 1, 2, 0] |
| 2 | 4 | [0, 1, 2, 3] |
| 3 | 1 | [4, 1, 2, 3] |

The output is `4 1 2 3`. Each value at index `i` correctly indicates who gave a gift to friend `i + 1`.

Another input:

```
3
1 3 2
```

| i | p[i] | q after assignment |
| --- | --- | --- |
| 0 | 1 | [1, 0, 0] |
| 1 | 3 | [1, 0, 2] |
| 2 | 2 | [1, 3, 2] |

Output: `1 3 2`, correctly mapping givers to recipients.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the array of length n to construct the inverse permutation |
| Space | O(n) | Array `q` of length n to store results |

For n ≤ 100, this algorithm is extremely fast and memory-efficient. The O(n) solution easily fits within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    p = list(map(int, input().split()))
    q = [0] * n
    for i in range(n):
        q[p[i] - 1] = i + 1
    return ' '.join(map(str, q))

# Provided samples
assert run("4\n2 3 4 1\n") == "4 1 2 3", "sample 1"
assert run("3\n1 3 2\n") == "1 3 2", "sample 2"

# Custom cases
assert run("1\n1\n") == "1", "single friend self-gift"
assert run("5\n1 2 3 4 5\n") == "1 2 3 4 5", "all self-gifts"
assert run("5\n5 4 3 2 1\n") == "5 4 3 2 1", "reversed permutation"
assert run("6\n2 1 4 3 6 5\n") == "2 1 4 3 6 5", "pair swaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 1 | Single friend gifting themselves |
| 5\n1 2 3 4 5 | 1 2 3 4 5 | All friends give gifts to themselves |
| 5\n5 4 3 2 1 | 5 4 3 2 1 | Fully reversed permutation |
| 6\n2 1 4 3 6 5 | 2 1 4 3 6 5 | Multiple swaps, ensuring correct mapping |

## Edge Cases

For a single friend, input `1\n1`, the algorithm initializes `q = [0]` and assigns `q[0] = 1`, producing output `1`. The algorithm correctly handles the minimal boundary.

For self-gifting, input `5\n1 2 3 4 5`, each `q[i]` is assigned `i + 1`, producing the same array as output. No off-by-one errors occur because we carefully adjust for 0-based indexing in Python versus 1-based friend numbers.

For reversed or swapped permutations, the direct assignment `q[p[i] - 1] = i + 1` reliably maps the giver to the receiver without searching, confirming correctness for all permutations.
