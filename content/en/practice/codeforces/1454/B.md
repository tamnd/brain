---
title: "CF 1454B - Unique Bid Auction"
description: "We are asked to determine the winner of a simplified \"Unique Bid Auction.\" Each participant chooses a number, and the winner is the participant who picked a number that no one else picked, and that is the smallest among all such unique numbers."
date: "2026-06-11T02:51:52+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1454
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 686 (Div. 3)"
rating: 800
weight: 1454
solve_time_s: 83
verified: true
draft: false
---

[CF 1454B - Unique Bid Auction](https://codeforces.com/problemset/problem/1454/B)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine the winner of a simplified "Unique Bid Auction." Each participant chooses a number, and the winner is the participant who picked a number that no one else picked, and that is the smallest among all such unique numbers. If there is no unique number, the result is -1. The input provides multiple test cases, each with a number of participants and their chosen numbers, and we must return the 1-based index of the winning participant for each case.

The constraints are critical. Each participant's number is at most `n`, and there can be up to `2·10^5` participants across all test cases. This rules out any solution that compares every pair of numbers (`O(n^2)`), because in the worst case, that could require `4·10^10` operations, which is far beyond what can run in one second. We need a linear or near-linear solution per test case, ideally `O(n)`.

Non-obvious edge cases include situations where all numbers are duplicates, a single participant exists, or the smallest number is repeated but a slightly larger number is unique. For example, for input `[1,1,2]`, the winner is the participant who chose `2`, not `1`, because `1` is not unique. Similarly, if all numbers are `[1,1,2,2]`, there is no winner. These are subtle because a naive approach that only looks for the smallest number without checking uniqueness will fail.

## Approaches

The brute-force approach is straightforward: for each number, count how many times it occurs, then scan all numbers to find the smallest number that occurs exactly once. Counting can be done with nested loops or repeated scans. This works correctly because it explicitly implements the problem definition. However, it is too slow. Counting the frequency for each number with `O(n)` scans for each test case results in `O(n^2)` per test case, which is unacceptable for the upper limits of `n`.

The key insight is that we only need the frequency of each number, not its position during the first scan. We can use a dictionary to map numbers to their occurrence counts. Once we have the frequency map, we can filter for numbers that occur exactly once and select the minimum among them. Then, a single pass over the original list identifies the 1-based index of the winner. This approach is linear: one pass to build the count map and one pass to find the index, `O(n)` per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty dictionary to count occurrences of each number.
2. Iterate through the participant numbers, incrementing the count of each number in the dictionary. This creates a frequency map of how many times each number appears.
3. Identify all numbers with a count of exactly one. If there are no such numbers, immediately return -1 for this test case.
4. Find the smallest number among those unique numbers. This is the winning number.
5. Iterate through the original list of numbers and find the index of the first occurrence of the winning number. Because the winning number is unique, there will be exactly one such occurrence.
6. Output the index, adjusting for 1-based indexing.

Why it works: the dictionary ensures accurate frequency counts, and scanning for the minimal unique number guarantees that we are following the problem's rules. Because we then scan for the index of that number, we correctly map the value back to the participant.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        count = {}
        for num in a:
            count[num] = count.get(num, 0) + 1
        # collect unique numbers
        unique_numbers = [num for num, freq in count.items() if freq == 1]
        if not unique_numbers:
            print(-1)
            continue
        winner_value = min(unique_numbers)
        # find 1-based index
        for i, num in enumerate(a):
            if num == winner_value:
                print(i + 1)
                break

if __name__ == "__main__":
    main()
```

The code first reads the number of test cases. For each case, it reads the number of participants and their numbers. The `count` dictionary stores the frequency of each number. The list comprehension filters out numbers that are unique. If there are no unique numbers, we output -1. Otherwise, we find the smallest unique number and scan the original array to find the participant's index. The use of `enumerate` ensures 1-based indexing is straightforward by adding one to the loop index.

## Worked Examples

### Sample 1: `[2,1,3]`

| Step | Variable | Value |
| --- | --- | --- |
| Count frequencies | count | {2:1,1:1,3:1} |
| Unique numbers | unique_numbers | [2,1,3] |
| Smallest unique | winner_value | 1 |
| Index scan | i,num | i=0,num=2 → skip; i=1,num=1 → match → print 2 |

This shows that the smallest unique number is found correctly and the correct 1-based index is returned.

### Sample 2: `[1,1,5,5,4,4]`

| Step | Variable | Value |
| --- | --- | --- |
| Count frequencies | count | {1:2,5:2,4:2} |
| Unique numbers | unique_numbers | [] |
| No unique number | - | print -1 |

This demonstrates handling of no-unique-number case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to count, one pass to find minimum, one pass to locate index |
| Space | O(n) | Frequency dictionary stores up to n keys |

Given the sum of all `n` does not exceed `2·10^5`, this solution runs efficiently under the time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# Provided samples
assert run("6\n2\n1 1\n3\n2 1 3\n4\n2 2 2 3\n1\n1\n5\n2 3 2 4 2\n6\n1 1 5 5 4 4\n") == "-1\n2\n4\n1\n2\n-1", "samples"

# Custom cases
assert run("1\n1\n1\n") == "1", "single participant"
assert run("1\n5\n5 5 5 5 5\n") == "-1", "all equal numbers"
assert run("1\n6\n1 2 3 4 5 6\n") == "1", "all unique numbers"
assert run("1\n5\n2 3 3 2 1\n") == "5", "smallest unique is last"
assert run("1\n7\n1 1 2 2 3 3 4\n") == "7", "last element unique"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 participant `[1]` | 1 | smallest and only number |
| all equal `[5 5 5 5 5]` | -1 | no unique number |
| all unique `[1 2 3 4 5 6]` | 1 | picks smallest unique correctly |
| last element unique `[2 3 3 2 1]` | 5 | finds correct index at end |
| last unique `[1 1 2 2 3 3 4]` | 7 | handles uniqueness at last element |

## Edge Cases

If the input contains only one participant, e.g., `[1]`, the algorithm correctly counts one occurrence, recognizes it as unique, and returns index 1. For all-equal arrays, e.g., `[5,5,5,5,5]`, the frequency map has no value with count 1, triggering the output -1. In cases where the smallest unique number is at the end of the array, e.g., `[2,3,3,2,1]`, the algorithm correctly identifies `1` as the winner and finds its index. These edge cases confirm that the algorithm handles boundaries, single elements, duplicates, and array positions correctly.
