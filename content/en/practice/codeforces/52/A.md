---
title: "CF 52A - 123-sequence"
description: "We are given a list of integers where every number is either 1, 2, or 3. The goal is to transform the sequence so that all numbers are the same, and we want to do this using the smallest number of replacements possible."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 52
codeforces_index: "A"
codeforces_contest_name: "Codeforces Testing Round 1"
rating: 900
weight: 52
solve_time_s: 98
verified: true
draft: false
---

[CF 52A - 123-sequence](https://codeforces.com/problemset/problem/52/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers where every number is either 1, 2, or 3. The goal is to transform the sequence so that all numbers are the same, and we want to do this using the smallest number of replacements possible. Each replacement consists of changing a number to any of the other two values. The input starts with an integer `n` specifying the length of the sequence, followed by `n` integers. The output is a single integer representing the minimum number of changes required.

Looking at the constraints, `n` can be as large as one million. This immediately rules out algorithms that iterate over all possible sequences of replacements or try every combination of transformations because their time complexity would explode. A linear-time approach is acceptable here since `n` is up to 10^6 and operations on the order of 10^6 to 10^7 will run comfortably under a 2-second time limit.

Edge cases to consider include a sequence where all numbers are already the same, a sequence where each number appears exactly the same number of times, and sequences with just one element. For example, if the sequence is `[2]`, no replacements are needed and the answer is `0`. If the sequence is `[1, 2, 3]`, then the best choice is to make all numbers 1, 2, or 3, requiring two changes.

## Approaches

The brute-force approach is straightforward. You could try making all numbers equal to 1, then all equal to 2, and finally all equal to 3, counting the number of changes needed in each case, then take the minimum. This method is correct because one of these three target values will necessarily produce the minimum number of replacements. The cost for this method is proportional to `3 * n` because for each target number, we must scan the entire array to count mismatches. This is acceptable in this problem because `3 * 10^6` operations are manageable, but in a stricter time setting or with larger ranges of numbers, this approach would become inefficient.

The key insight to optimize the problem further is to realize that we do not need to simulate changing the sequence at all. What matters is how many times each number appears. If we know the counts of 1s, 2s, and 3s, the minimum number of replacements is the total length minus the maximum count. That is because the optimal choice is to transform all elements to the number that already occurs most frequently. This reduces the problem to a simple counting problem, which can be solved in a single pass of the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3 * n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize three counters, one for each number: `count1`, `count2`, and `count3`. Each will keep track of how many times 1, 2, and 3 appear in the sequence. This is the minimal information we need to decide the optimal replacement strategy.
2. Iterate over each number in the sequence. If the number is 1, increment `count1`. If it is 2, increment `count2`. Otherwise increment `count3`. Counting like this ensures we have a complete frequency map in one linear pass.
3. Determine the maximum frequency among the three counts. This represents the number we should convert the rest of the sequence to. Let `max_count` be the largest of `count1`, `count2`, and `count3`.
4. The minimum replacements required is the total length of the sequence minus this maximum count, `n - max_count`. This works because the maximum count elements are already correct, and the remaining elements must be changed to match.

Why it works: At each point, we maintain a count of occurrences of each possible value. Since we can change any number to any other, the optimal strategy is always to pick the value that occurs most frequently and convert the rest. No other strategy can require fewer changes because any deviation from the most frequent number would necessarily require changing more elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

count1 = count2 = count3 = 0
for num in a:
    if num == 1:
        count1 += 1
    elif num == 2:
        count2 += 1
    else:
        count3 += 1

max_count = max(count1, count2, count3)
print(n - max_count)
```

The code begins by reading the input efficiently using `sys.stdin.readline` for large input sizes. It then initializes counters for each possible value in the sequence. During iteration, each number increments the appropriate counter, ensuring no off-by-one errors occur. After counting, we compute the maximum count and subtract it from `n` to get the minimum number of replacements. The algorithm avoids unnecessary data structures, ensuring O(1) space.

## Worked Examples

### Sample Input 1

```
9
1 3 2 2 2 1 1 2 3
```

| num | count1 | count2 | count3 |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 3 | 1 | 0 | 1 |
| 2 | 1 | 1 | 1 |
| 2 | 1 | 2 | 1 |
| 2 | 1 | 3 | 1 |
| 1 | 2 | 3 | 1 |
| 1 | 3 | 3 | 1 |
| 2 | 3 | 4 | 1 |
| 3 | 3 | 4 | 2 |

`max_count = 4`, `n - max_count = 9 - 4 = 5`. Correct output is 5.

### Custom Input 2

```
5
2 2 2 2 2
```

| num | count1 | count2 | count3 |
| --- | --- | --- | --- |
| 2 | 0 | 1 | 0 |
| 2 | 0 | 2 | 0 |
| 2 | 0 | 3 | 0 |
| 2 | 0 | 4 | 0 |
| 2 | 0 | 5 | 0 |

`max_count = 5`, `n - max_count = 5 - 5 = 0`. Correct output is 0.

These traces confirm the counting approach correctly identifies the optimal number of replacements, handles sequences already uniform, and scales to larger sequences efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One linear pass through the sequence to count occurrences |
| Space | O(1) | Only three counters used regardless of sequence size |

The algorithm fits well within the constraints. For `n = 10^6`, one linear pass is feasible, and only three integers are stored, so memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    count1 = count2 = count3 = 0
    for num in a:
        if num == 1:
            count1 += 1
        elif num == 2:
            count2 += 1
        else:
            count3 += 1
    return str(n - max(count1, count2, count3))

# Provided sample
assert run("9\n1 3 2 2 2 1 1 2 3\n") == "5", "sample 1"

# Custom cases
assert run("1\n1\n") == "0", "single element"
assert run("5\n2 2 2 2 2\n") == "0", "all equal"
assert run("3\n1 2 3\n") == "2", "all different"
assert run("6\n1 1 2 2 3 3\n") == "4", "equal counts"
assert run("10\n3 3 3 3 3 3 3 3 3 3\n") == "0", "all 3s"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 0 | Single-element sequence |
| 5\n2 2 2 2 2 | 0 | Already uniform sequence |
| 3\n1 2 3 | 2 | Sequence with all distinct values |
| 6\n1 1 2 2 3 3 | 4 | Sequence with equal counts |
| 10\n3 3 3 3 3 3 3 3 3 3 | 0 | Sequence with all maximum-length repeated values |

## Edge Cases

For a sequence with a single element, such as `[1]`, the algorithm counts `count1 = 1` and the others zero. The maximum count is 1
