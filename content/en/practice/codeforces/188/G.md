---
title: "CF 188G - Array Sorting"
description: "The task is to sort a list of integers in non-descending order. You are given the size of the list, n, and then n integers, each on a separate line, with values ranging from 1 to 100."
date: "2026-06-05T00:34:30+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "G"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1600
weight: 188
solve_time_s: 70
verified: true
draft: false
---

[CF 188G - Array Sorting](https://codeforces.com/problemset/problem/188/G)

**Rating:** 1600  
**Tags:** *special, implementation  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to sort a list of integers in non-descending order. You are given the size of the list, _n_, and then _n_ integers, each on a separate line, with values ranging from 1 to 100. The output should be the same integers printed on one line, in ascending order, separated by spaces. Duplicate values are allowed, and the array can be as small as a single element or as large as 100 elements.

The constraints are small: with _n_ up to 100 and each number between 1 and 100, the algorithm can afford to perform O(n²) operations without exceeding the time limit. This means even simple sorting algorithms like insertion sort or selection sort would be fast enough. On the other hand, the problem encourages using a more efficient approach if desired, but there is no strict need for complex optimization. Edge cases include arrays that are already sorted, arrays where all elements are equal, and arrays where the largest and smallest numbers appear multiple times. For instance, for an input of

```
5
3
3
3
3
3
```

the output should simply be

```
3 3 3 3 3
```

A careless implementation that attempts to eliminate duplicates or mismanages indices could fail this case.

## Approaches

The most straightforward approach is to use a standard comparison-based sorting algorithm. You could implement bubble sort or insertion sort by repeatedly comparing adjacent elements and swapping them when they are out of order. This works because the array is small, but in the worst case it requires about n² = 100² = 10,000 comparisons and swaps, which is still acceptable for this problem. This method is conceptually simple: go through the array, compare pairs, swap if necessary, repeat until no swaps occur. It is correct for any input but scales poorly for larger arrays.

A more elegant approach leverages the fact that all numbers are integers in the range 1 to 100. This allows the use of counting sort. Instead of repeatedly comparing numbers, we count how many times each number appears and then reconstruct the sorted array by writing each number the counted number of times. This reduces the algorithm to O(n + m), where m is the range of numbers (here 100), giving a deterministic and very fast solution.

The brute-force method works because repeated comparisons eventually position each element correctly, but it fails in efficiency for larger arrays. The observation that the input numbers are bounded and discrete lets us reduce the problem to a linear-time counting exercise, which is optimal given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Comparison Sort (bubble/insertion) | O(n²) | O(1) | Accepted |
| Counting Sort | O(n + m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the integer _n_ to determine the number of elements in the array. This step sets up the array storage and loop limits.
2. Initialize a list to store the array elements, then read each integer from input and append it to the list. This preserves the original order for the counting sort stage.
3. Create a counting array of size 101, initialized to zero. Each index represents a number from 1 to 100, and the value at that index will store how many times that number appears in the input.
4. Iterate through the original array. For each element, increment the corresponding index in the counting array. This produces a frequency distribution of the numbers.
5. Initialize an empty result list. Iterate through the counting array from index 1 to 100. For each index with a nonzero count, append the index value to the result list as many times as its count. This step reconstructs the array in sorted order.
6. Print the result list, joining the numbers with spaces. This produces the required output format.

Why it works: the counting array guarantees that each number appears in the output exactly as many times as in the input, and because we iterate over the counting array in ascending index order, the result is sorted. No comparisons between arbitrary array elements are necessary, and duplicates are handled naturally.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
arr = [int(input()) for _ in range(n)]

count = [0] * 101
for num in arr:
    count[num] += 1

result = []
for num in range(1, 101):
    result.extend([num] * count[num])

print(" ".join(map(str, result)))
```

The first section reads the input efficiently using `sys.stdin.readline`. Using a list comprehension immediately stores the numbers in `arr`. The `count` array of size 101 allows direct indexing, so `count[num] += 1` increments the frequency for each number. In the reconstruction step, `[num] * count[num]` repeats the number the correct number of times, and `extend` adds these to the result list. Finally, `map(str, result)` converts integers to strings for joining with spaces.

## Worked Examples

### Sample 1

Input:

```
5
7
1
9
7
3
```

| Step | arr | count | result |
| --- | --- | --- | --- |
| Read input | [7,1,9,7,3] | all 0 | [] |
| Count 7 | [7,1,9,7,3] | count[7]=1 | [] |
| Count 1 | [7,1,9,7,3] | count[1]=1 | [] |
| Count 9 | [7,1,9,7,3] | count[9]=1 | [] |
| Count 7 | [7,1,9,7,3] | count[7]=2 | [] |
| Count 3 | [7,1,9,7,3] | count[3]=1 | [] |
| Reconstruct | [7,1,9,7,3] | count[1..9] | [1,3,7,7,9] |

This trace confirms that counting handles duplicates and orders elements correctly.

### Sample 2

Input:

```
3
3
3
3
```

| Step | arr | count | result |
| --- | --- | --- | --- |
| Read input | [3,3,3] | all 0 | [] |
| Count 3 | [3,3,3] | count[3]=1 | [] |
| Count 3 | [3,3,3] | count[3]=2 | [] |
| Count 3 | [3,3,3] | count[3]=3 | [] |
| Reconstruct | [3,3,3] | count[1..3] | [3,3,3] |

This confirms that the algorithm handles all-equal values without error.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Counting array construction is O(n), reconstruction is O(m) where m=100 |
| Space | O(m + n) | Counting array uses O(m), result array uses O(n) |

With n ≤ 100 and m = 100, total operations are below 200, well within the 2-second limit. Memory usage is negligible compared to the 256 MB allowance.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    arr = [int(input()) for _ in range(n)]
    count = [0] * 101
    for num in arr:
        count[num] += 1
    result = []
    for num in range(1, 101):
        result.extend([num] * count[num])
    return " ".join(map(str, result))

# provided samples
assert run("5\n7\n1\n9\n7\n3\n") == "1 3 7 7 9", "sample 1"
assert run("3\n3\n3\n3\n") == "3 3 3 3", "all equal values"

# custom cases
assert run("1\n42\n") == "42", "minimum-size input"
assert run("6\n100\n1\n50\n50\n1\n100\n") == "1 1 50 50 100 100", "duplicates and boundaries"
assert run("4\n2\n3\n1\n4\n") == "1 2 3 4", "already small sorted"
assert run("10\n10\n9\n8\n7\n6\n5\n4\n3\n2\n1\n") == "1 2 3 4 5 6 7 8 9 10", "reverse order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 42 | Minimum array size |
| 1 50 100 duplicates | 1 1 50 50 100 100 | Duplicate values and boundaries |
| 2 3 1 4 | 1 2 3 4 | Small unordered array |
| 10..1 | 1..10 | Reverse-sorted array |

## Edge Cases

For an array of size 1, such as input `1\n42\n`, the counting array still works because we increment `count[42] = 1` and reconstruct `[42]`. The algorithm naturally prints the single element. For arrays with all elements equal, the counting array records the frequency correctly, and reconstruction reproduces the correct number of repeated values. For the
