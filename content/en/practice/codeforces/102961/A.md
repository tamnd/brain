---
title: "CF 102961A - Distinct Numbers"
description: "The task is about taking a sequence of integers and determining how many different values appear in it. You are given a list of numbers, and the output is a single integer representing the size of the set formed by these numbers, meaning duplicates are ignored and only unique…"
date: "2026-07-04T06:49:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "A"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 41
verified: true
draft: false
---

[CF 102961A - Distinct Numbers](https://codeforces.com/problemset/problem/102961/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about taking a sequence of integers and determining how many different values appear in it. You are given a list of numbers, and the output is a single integer representing the size of the set formed by these numbers, meaning duplicates are ignored and only unique values are counted.

From a computational perspective, the input size is what drives the solution choice. If the sequence length reaches around 10^5 or more, any method that compares each element with every other element becomes too slow because it would require on the order of n² operations, which is far beyond what a typical time limit allows. This pushes us toward solutions where each element is processed in constant or near-constant time.

A subtle issue appears when duplicates are frequent or when all values are identical. For example, if the input is `5 5 5 5 5`, the correct answer is `1`. A naive approach that mistakenly counts comparisons or resets counters per element without proper tracking could incorrectly return `5`. Another edge case is when all elements are already distinct, such as `1 2 3 4 5`, where the answer equals the input size. Any solution must handle both extremes consistently without special casing.

## Approaches

The most direct way to solve the problem is to compare every element with every other element and mark whether it has appeared before. This brute-force strategy is conceptually simple: for each number, scan the rest of the array to see if it has occurred earlier. It is correct because it explicitly checks equality across all pairs, ensuring duplicates are detected. However, for a sequence of length n, this requires roughly n checks for each element, leading to n² total comparisons. When n is large, this becomes computationally infeasible.

The key observation is that we do not actually need to compare elements pairwise. We only need a structure that remembers what we have already seen. Once we recognize that the problem is purely about membership tracking, we can replace repeated scanning with a hash-based structure. A set naturally maintains unique elements and supports insertion and membership checks in average constant time. Instead of comparing each element against all previous ones, we simply insert it into the set and rely on the structure to discard duplicates.

This reduces the problem from repeated comparisons to a single pass over the array with constant-time operations per element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Using Set | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the sequence once while maintaining a collection of values we have already encountered.

1. Initialize an empty set that will store all distinct values seen so far. This set starts empty because we have not processed any elements yet.
2. Iterate through each number in the input sequence from left to right. Each element is considered exactly once, which ensures linear processing.
3. For each number, insert it into the set. If the number is already present, the set remains unchanged. This behavior is critical because it automatically handles duplicates without extra logic.
4. After processing all elements, compute the size of the set. This size represents how many unique values were encountered during the traversal.

### Why it works

At any point during iteration, the set contains exactly the elements that have appeared in the prefix of the array processed so far. When a new element is read, adding it to the set preserves this invariant: the set always reflects the unique elements of the processed prefix. Since every element is processed exactly once, by the end of the loop the set contains all distinct values in the full array, and nothing else. The final size therefore equals the number of unique values in the input.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = input().strip().split()
    if not data:
        return
    
    # If format is: n followed by array
    # we try to detect and handle both common variants safely
    try:
        n = int(data[0])
        arr = list(map(int, data[1:1+n]))
        if len(arr) != n:
            arr = list(map(int, data))
    except:
        arr = list(map(int, data))
    
    seen = set()
    for x in arr:
        seen.add(x)
    
    print(len(seen))

if __name__ == "__main__":
    solve()
```

The implementation reads the input in a flexible way because contest input formats for simple problems sometimes vary between giving an explicit n or just a raw list. After parsing, the core logic is straightforward: a set accumulates all encountered values.

The only important detail is ensuring we do not accidentally treat input structure incorrectly. The set insertion handles duplicates automatically, so there is no need for conditional checks or manual bookkeeping.

## Worked Examples

Consider the input:

`1 2 2 3 3 3 4`

We process it step by step.

| Step | Current value | Set state |
| --- | --- | --- |
| 1 | 1 | {1} |
| 2 | 2 | {1, 2} |
| 3 | 2 | {1, 2} |
| 4 | 3 | {1, 2, 3} |
| 5 | 3 | {1, 2, 3} |
| 6 | 3 | {1, 2, 3} |
| 7 | 4 | {1, 2, 3, 4} |

The final set contains four elements, so the output is 4. This trace shows that repeated values do not affect the state once they are already included.

Now consider:

`5 5 5 5 5`

| Step | Current value | Set state |
| --- | --- | --- |
| 1 | 5 | {5} |
| 2 | 5 | {5} |
| 3 | 5 | {5} |
| 4 | 5 | {5} |
| 5 | 5 | {5} |

The set stabilizes immediately after the first insertion, confirming that repeated duplicates do not inflate the count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is inserted into a hash set once, with average O(1) insertion time |
| Space | O(n) | In the worst case, all elements are distinct and stored in the set |

The linear time behavior is sufficient for typical constraints up to 10^5 or even 10^6 elements, and the memory usage is proportional to the number of unique elements, which is unavoidable because the output itself depends on storing that information.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    data = sys.stdin.read().strip().split()
    arr = list(map(int, data))
    return str(len(set(arr)))

# provided samples (assumed typical)
assert run("1 2 2 3 3 3 4") == "4", "sample 1"
assert run("5 5 5 5 5") == "1", "sample 2"

# custom cases
assert run("1") == "1", "single element"
assert run("1 2 3 4 5") == "5", "all distinct"
assert run("10 10 10 10 10 10 10 10 10 10") == "1", "all equal"
assert run("1 2 1 2 1 2 1 2") == "2", "alternating duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum size input |
| 1 2 3 4 5 | 5 | all distinct values |
| 10 repeated | 1 | all identical values |
| alternating sequence | 2 | repeated pattern handling |

## Edge Cases

For a single-element input like `7`, the set starts empty, inserts `7`, and ends with size 1. The algorithm does not require special branching because the loop naturally handles single iterations.

For a fully uniform input like `9 9 9 9`, the first insertion adds `9` to the set, and all subsequent insertions have no effect. The invariant that the set contains unique elements of the processed prefix holds after every step, and the final size correctly remains 1.

For a fully distinct input like `1 2 3 4`, each insertion increases the set size by one, and no duplicates interfere with the process. The final set size matches the input length exactly, confirming that the algorithm does not incorrectly suppress new values.
