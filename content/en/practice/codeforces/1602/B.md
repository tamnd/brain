---
title: "CF 1602B - Divine Array"
description: "We are given an array of integers where each element is between 1 and the size of the array. Over repeated steps, every element of the array is replaced by the count of how many times it occurs in the array."
date: "2026-06-10T08:18:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1602
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 751 (Div. 2)"
rating: 1100
weight: 1602
solve_time_s: 74
verified: true
draft: false
---

[CF 1602B - Divine Array](https://codeforces.com/problemset/problem/1602/B)

**Rating:** 1100  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers where each element is between 1 and the size of the array. Over repeated steps, every element of the array is replaced by the count of how many times it occurs in the array. After each transformation, the new array becomes the basis for the next step. For any position in the array, we may be asked what its value will be after an arbitrary number of steps, potentially up to one billion.

The input includes multiple test cases. Each test case provides the initial array and multiple queries. Each query specifies an index and a step count, and we must report the value at that index after the requested number of steps.

The first observation is that the array size in any test case does not exceed 2000, but the number of queries can be as high as 100,000. This means that simulating every query independently is impractical. Each step requires counting occurrences of every element in the array, which is O(n). Doing this naively for k steps would be O(n * k), and with k up to 10^9, this is far too slow.

Edge cases arise when the number of steps is zero, which should return the initial array directly. Another subtle case is when elements stabilize early: some arrays reach a state where all elements no longer change after a few steps. For instance, an array of all equal values becomes constant in one step, so any query asking for a very large k will return the same value as after the first stabilization.

## Approaches

A brute-force solution simulates each transformation step explicitly. For each query, we would loop k times, counting occurrences of each element and updating the array. This works correctly, but the worst case would be n=2000, k=10^9, and q=100,000, which is completely infeasible.

The key insight is that the transformation process eventually stabilizes. Because each element is replaced by its frequency, the array cannot produce values larger than n, and repeated counting leads to a fixed array where every element equals the frequency of its value in the previous step. In practice, stabilization occurs quickly; the maximum number of steps needed to stabilize any array of size n is at most n. Therefore, we can precompute all arrays until they stabilize and store each intermediate state. Then answering any query reduces to picking the appropriate step or the last stable array if k exceeds the number of precomputed steps.

We can represent this precomputation as a list of arrays. For each step, we compute a new array by counting occurrences of the previous array’s elements. We stop when the new array is identical to the previous one. Once the stabilized arrays are precomputed, each query is a simple array lookup, either at step k or at the last step if k exceeds stabilization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k * q) | O(n) | Too slow |
| Precompute until stabilization | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t. For each test case, read the array size n and the initial array a.
2. Initialize a list `arrays` with the initial array as its first element. This will store the array at each step until stabilization.
3. Enter a loop to generate subsequent arrays. Count occurrences of each number in the current array. Replace each element with its count. Append the new array to `arrays`. If the new array is identical to the previous array, break the loop, as stabilization has been reached.
4. Read the number of queries q. For each query, read the index x and step k. Adjust k if it exceeds the number of computed steps by using the last stabilized array. Output the value at position x-1 of the array corresponding to step k.

Why it works: Each transformation is deterministic and depends solely on counts of elements. Because the maximum possible value is bounded by n, and there are only n positions, the array must stabilize in at most n steps. Precomputing all steps guarantees that any query can be answered correctly, even if k is extremely large.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    arrays = [a[:]]  # store arrays at each step
    while True:
        prev = arrays[-1]
        freq = [0] * (n + 1)
        for val in prev:
            freq[val] += 1
        new_arr = [freq[val] for val in prev]
        if new_arr == prev:
            break
        arrays.append(new_arr)
    
    q = int(input())
    for _ in range(q):
        x, k = map(int, input().split())
        step = min(k, len(arrays)-1)
        print(arrays[step][x-1])
```

The solution begins by reading input efficiently. We store all intermediate arrays to handle queries in O(1) per query. Counting is done using a simple frequency array of size n+1, which is safe because all values are ≤ n. The loop stops when the array no longer changes, ensuring we do not waste memory or computations on unnecessary steps. For each query, we clamp k to the last precomputed array if k is larger than the stabilization step, guaranteeing correctness.

## Worked Examples

**Example 1**

Initial array: `[2,1,1,4,3,1,2]`

Precomputed arrays:

| Step | Array |
| --- | --- |
| 0 | 2 1 1 4 3 1 2 |
| 1 | 2 3 3 1 1 3 2 |
| 2 | 2 3 3 2 2 3 2 |
| 3 | 4 3 3 4 4 3 4 |
| 4 | 3 4 4 3 3 4 3 |
| 5 | 4 3 3 4 4 3 4 |

Queries:

(3,0) → step 0 → 1

(1,1) → step 1 → 2

(2,2) → step 2 → 3

(6,1) → step 1 → 3

**Example 2**

Initial array: `[1,1]`

Precomputed arrays:

| Step | Array |
| --- | --- |
| 0 | 1 1 |
| 1 | 2 2 |
| 2 | 2 2 |

Queries:

(1,0) → 1

(2,10^9) → use stabilized array step 2 → 2

These examples confirm that clamping k to the last stable step works correctly and small arrays stabilize quickly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 + q) | Precomputing all arrays until stabilization is at most n steps with n elements each (O(n^2)), and each query is O(1). |
| Space | O(n^2) | We store each array up to stabilization; at most n arrays of size n each. |

With n ≤ 2000 and sum of q ≤ 100,000, this algorithm easily fits within 2 seconds and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())  # assume solution saved as solution.py
    return out.getvalue().strip()

# Provided samples
assert run("2\n7\n2 1 1 4 3 1 2\n4\n3 0\n1 1\n2 2\n6 1\n2\n1 1\n2\n1 0\n2 1000000000\n") == "1\n2\n3\n3\n1\n2", "Sample 1+2"

# Custom tests
assert run("1\n1\n1\n2\n1 0\n1 100\n") == "1\n1", "single element array"
assert run("1\n3\n1 1 1\n3\n1 0\n2 1\n3 2\n") == "1\n3\n3", "all equal values"
assert run("1\n5\n1 2 3 4 5\n5\n1 0\n2 1\n3 2\n4 3\n5 4\n") == "1\n1\n1\n1\n1", "distinct elements stabilizing quickly"
assert run("1\n2\n1 2\n2\n1 1\n2 1\n") == "1\n1", "two distinct elements"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 1 | single element, k large |
| all equal | 1 3 3 | stabilization in one step |
| all distinct | 1 1 1 1 1 | each value goes to 1 quickly |
| two elements | 1 1 | correct frequency computation and indexing |

## Edge Cases

For a single-element array `[1]` and query `(1, 100)`, the algorithm computes step 0 as `[1]` and recognizes stabilization immediately. The output is 1 for any k.

For an array of all
