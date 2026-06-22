---
title: "CF 106059L - Lantern Festival"
description: "The problem is essentially asking us to process a row of lanterns along a riverbank, where each lantern is either on or off. The input gives us a sequence of length n, and each position contains either a 0 meaning the lantern is unlit or a 1 meaning it is glowing."
date: "2026-06-22T18:42:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106059
codeforces_index: "L"
codeforces_contest_name: "National Yang Ming Chiao Tung University 2025 Team Selection Programming Contest"
rating: 0
weight: 106059
solve_time_s: 46
verified: true
draft: false
---

[CF 106059L - Lantern Festival](https://codeforces.com/problemset/problem/106059/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is essentially asking us to process a row of lanterns along a riverbank, where each lantern is either on or off. The input gives us a sequence of length n, and each position contains either a 0 meaning the lantern is unlit or a 1 meaning it is glowing. The task is to determine how many lanterns are currently lit, which is equivalent to counting how many values in the sequence are equal to 1.

Although the statement frames this in a festival setting, nothing about positions, adjacency, or structure matters beyond the raw values. The sequence is independent, and each element contributes to the answer without interacting with others.

The constraint n up to 2 × 10^5 tells us we are expected to scan the array in linear time. Any approach that repeatedly processes the same elements or uses nested loops over the array would be too slow. A quadratic solution would imply around 4 × 10^10 operations in the worst case, which is far beyond the time limit. This immediately suggests that a single pass accumulation is the correct direction.

Edge cases here are mostly about input formatting and boundary sizes. If n = 1, we simply return that single value. If all values are 0, the answer is 0. If all values are 1, the answer is n. A subtle issue that can appear in implementations is assuming the second line always comes formatted cleanly or contains exactly n integers separated by spaces, but forgetting that input may span large lines requiring fast parsing.

## Approaches

A straightforward way to solve the problem is to directly iterate through the list of lantern states and count how many are equal to 1. This works because each lantern contributes independently to the final total. We do not need sorting, prefix structures, or any form of preprocessing since there are no range queries or dependencies between positions.

The brute-force interpretation might still be phrased as checking each lantern individually and incrementing a counter when it is lit. That is already optimal in structure. Any attempt to recompute counts repeatedly, for example recomputing sums over prefixes for each query position, would be unnecessary because the problem only asks for a single global count.

The key observation is that the structure of the input is already minimal. There is no transformation required, only aggregation. This reduces the problem to computing the sum of a binary array, since each 1 contributes exactly one unit to the answer and each 0 contributes nothing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute or nested counting) | O(n) or worse O(n^2) | O(1) | Too slow if repeated work is done |
| Optimal (single pass sum) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We scan the sequence once while maintaining a running total of lit lanterns.

1. Read n, the number of lanterns. This determines how many values we will process and ensures we stop exactly after consuming the sequence.
2. Initialize a counter to zero. This counter represents how many lanterns have been seen that are lit so far.
3. Iterate through each of the n values in the input sequence. Each value represents the state of a single lantern.
4. For each value, check whether it is equal to 1. If it is, increment the counter by one. If it is 0, do nothing. This step works because each lantern contributes independently and only lit lanterns matter for the final count.
5. After processing all values, output the counter. At this point, it contains the total number of lanterns that were lit in the input sequence.

### Why it works

The algorithm maintains the invariant that after processing the first k elements, the counter equals the number of 1s among those k elements. Each step preserves this invariant because the only way to change the true count of lit lanterns in a prefix is to include the current element if it is 1. Since every element is processed exactly once and contributes exactly once if and only if it is 1, the final counter equals the total number of lit lanterns in the full sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    cnt = 0
    for x in arr:
        cnt += x
    
    print(cnt)

if __name__ == "__main__":
    solve()
```

The solution reads the size n and then parses the entire second line into an integer list. Since the values are only 0 or 1, summing them directly is equivalent to counting lit lanterns, which is both compact and efficient.

A common pitfall is forgetting to strip or correctly split the input line, especially when n is large. Using `sys.stdin.readline` ensures fast reading. Another subtle point is that summing integers is safe here because values are small and there is no risk of overflow in Python.

## Worked Examples

### Example 1

Input:

```
n = 7
arr = [1, 0, 1, 1, 0, 0, 1]
```

| Step | Current Value | Counter |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 0 | 1 |
| 3 | 1 | 2 |
| 4 | 1 | 3 |
| 5 | 0 | 3 |
| 6 | 0 | 3 |
| 7 | 1 | 4 |

Final output is 4.

This trace shows how each 1 contributes exactly one increment, while 0 values leave the state unchanged. The running total matches the number of lit lanterns at every prefix.

### Example 2

Input:

```
n = 5
arr = [0, 1, 0, 0, 1]
```

| Step | Current Value | Counter |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 0 | 1 |
| 4 | 0 | 1 |
| 5 | 1 | 2 |

Final output is 2.

This confirms that the algorithm does not depend on positions or ordering patterns. Only the number of 1s matters, and their distribution is irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each lantern is processed exactly once in a single pass |
| Space | O(1) | Only a single counter is maintained beyond input storage |

The constraints allow up to 2 × 10^5 elements, and a single linear scan fits comfortably within both time and memory limits in Python, since it performs only a simple integer increment per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    n = int(input().strip())
    arr = list(map(int, input().split()))
    return str(sum(arr))

# provided samples
assert run("7\n1 0 1 1 0 0 1\n") == "4"
assert run("5\n0 1 0 0 1\n") == "2"

# minimum size
assert run("1\n0\n") == "0"
assert run("1\n1\n") == "1"

# all zeros
assert run("5\n0 0 0 0 0\n") == "0"

# all ones
assert run("6\n1 1 1 1 1 1\n") == "6"

# alternating pattern
assert run("8\n1 0 1 0 1 0 1 0\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 0 | 0 | minimum boundary case |
| single 1 | 1 | minimum active case |
| all zeros | 0 | no contributions |
| all ones | n | maximum accumulation |
| alternating | n/2 | mixed distribution correctness |

## Edge Cases

For n = 1 with value 0, the algorithm initializes the counter to 0, reads the single element, finds it is not 1, and outputs 0. This directly matches the expected behavior since there are no lit lanterns.

For n = 1 with value 1, the counter starts at 0, is incremented once, and outputs 1. This confirms correctness at the smallest non-trivial input size.

For a case like all zeros, such as n = 5 and [0, 0, 0, 0, 0], every iteration leaves the counter unchanged, so the final result remains 0, matching the absence of lit lanterns.

For all ones, such as n = 5 and [1, 1, 1, 1, 1], each iteration increments the counter, so it accumulates exactly n. This shows the algorithm scales linearly without any special handling required for dense inputs.
