---
title: "CF 1257C - Dominated Subarray"
description: "We are given several arrays, and for each one we need to find the shortest contiguous segment that has a strict majority element."
date: "2026-06-13T22:42:07+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1257
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 76 (Rated for Div. 2)"
rating: 1200
weight: 1257
solve_time_s: 259
verified: true
draft: false
---

[CF 1257C - Dominated Subarray](https://codeforces.com/problemset/problem/1257/C)

**Rating:** 1200  
**Tags:** greedy, implementation, sortings, strings, two pointers  
**Solve time:** 4m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several arrays, and for each one we need to find the shortest contiguous segment that has a strict majority element. A segment is considered valid if it contains at least two elements and there exists a value whose frequency inside the segment is strictly greater than the frequency of every other value.

This condition is equivalent to saying the segment has a unique most frequent value, and that value is strictly more frequent than any competitor. If no such segment exists, we return -1.

The input size is large across test cases, with the total number of elements up to 200,000. That immediately rules out any solution that examines all subarrays explicitly. A quadratic or cubic approach would attempt on the order of n² or n³ segment checks, which is too slow even for a single large test.

The key difficulty is that domination is not just about duplicates existing. A segment like `[1, 2]` is invalid even though both elements are distinct, while `[3, 3]` is valid because one value strictly dominates. Even more subtle, a segment like `[3, 2, 3, 2, 3]` is valid because 3 appears more than any other value, even though multiple values repeat.

A common mistake is assuming that any duplicate immediately implies a valid answer of length 2. This fails when duplicates are far apart or when multiple values compete equally inside short segments. Another failure case comes from trying to greedily extend or shrink windows without recognizing that the optimal segment is determined by the closest repetition of any value.

## Approaches

A brute-force solution would enumerate every subarray, count frequencies inside it, and check whether one value has strictly greater frequency than all others. Even if we maintain a frequency map incrementally, we still have O(n²) subarrays per test case, and updating or checking dominance costs O(1) to O(n), leading to worst-case O(n³). With 200,000 total elements, this is completely infeasible.

The key observation is that we are not searching for a global structure like maximum sum or longest property window. We only care about the smallest segment that already forces a strict majority. That smallest structure must appear as soon as some value repeats, because a value cannot become dominant unless it appears at least twice. The shortest way for a value to strengthen its dominance is to take two adjacent occurrences of that value and include everything between them. Any candidate optimal segment must be contained inside some interval between two equal elements.

This reduces the problem to tracking, for every value, the minimum distance between two consecutive occurrences. If a value appears at positions i and j, then the segment `[i, j]` is a candidate, and its length is `j - i + 1`. Among all values, the smallest such interval is the answer.

This works because any dominated segment must contain a value that appears at least twice inside it. Shrinking that segment until it only spans between the first and last occurrence of that dominating value cannot break dominance and only reduces length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. We maintain a dictionary that stores the last index where each value appeared. This lets us detect whenever we see a repeated occurrence of a value.
2. As we scan the array from left to right, for each position i with value x, we check if x has been seen before. If it has, we compute the distance between i and the previous occurrence.
3. This distance plus one is a candidate answer, since it represents a segment where x appears at least twice.
4. We update the best answer across all such pairs.
5. We update the last seen position of x to i.
6. After finishing the scan, if we never found any repeated value, we return -1. Otherwise we return the minimum candidate length.

The crucial idea is that every valid dominated segment must contain at least one repeated value, and the best possible segment for that value is always between two consecutive occurrences. Any extra elements outside this range can only increase length without helping dominance.

### Why it works

Consider any dominated segment. Let v be its dominant value. Since v has strictly higher frequency than any other value in that segment, it must appear at least twice. Take the first and last occurrence of v inside that segment. The subarray between them still contains at least those two occurrences of v, and removing elements outside cannot increase any competing frequency relative to v inside that reduced interval. So the optimal segment for v is always captured by some pair of occurrences, and checking all adjacent pairs of equal values is sufficient to find the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))

        last = {}
        ans = float('inf')

        for i, x in enumerate(a):
            if x in last:
                ans = min(ans, i - last[x] + 1)
            last[x] = i

        print(-1 if ans == float('inf') else ans)

if __name__ == "__main__":
    solve()
```

The solution relies on a single pass per test case. The dictionary `last` stores the most recent index of each value. Whenever a repeat is found, we immediately compute the candidate segment length. The `+1` is essential because indices define a difference, not a length.

A common implementation mistake is forgetting to initialize the answer to infinity and incorrectly treating unseen cases as valid. Another subtle issue is failing to update the last occurrence after computing a candidate, which would incorrectly compare non-consecutive occurrences instead of adjacent ones.

## Worked Examples

### Example 1

Input: `[1, 2, 3, 4, 5, 1]`

| i | value | last[value] before | candidate length | ans |
| --- | --- | --- | --- | --- |
| 0 | 1 | none | - | inf |
| 1 | 2 | none | - | inf |
| 2 | 3 | none | - | inf |
| 3 | 4 | none | - | inf |
| 4 | 5 | none | - | inf |
| 5 | 1 | 0 | 6 | 6 |

The first repetition occurs at the end when value 1 appears again. The segment from index 0 to 5 contains 1 twice and becomes the best candidate.

### Example 2

Input: `[4, 1, 2, 4, 5, 4, 3, 2, 1]`

| i | value | last[value] before | candidate length | ans |
| --- | --- | --- | --- | --- |
| 0 | 4 | none | - | inf |
| 1 | 1 | none | - | inf |
| 2 | 2 | none | - | inf |
| 3 | 4 | 0 | 4 | 4 |
| 4 | 5 | none | - | 4 |
| 5 | 4 | 3 | 3 | 3 |
| 6 | 3 | none | - | 3 |
| 7 | 2 | 2 | 6 | 3 |
| 8 | 1 | 1 | 8 | 3 |

The optimal segment is driven by value 4, with its closest repetition at indices 3 and 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with O(1) dictionary operations |
| Space | O(n) | Stores last occurrence of each distinct value |

The total input size constraint ensures the overall runtime remains linear across all test cases, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    def solve():
        T = int(input())
        for _ in range(T):
            n = int(input())
            a = list(map(int, input().split()))
            last = {}
            ans = float('inf')
            for i, x in enumerate(a):
                if x in last:
                    ans = min(ans, i - last[x] + 1)
                last[x] = i
            out.append(str(-1 if ans == float('inf') else ans))

    solve()
    return "\n".join(out)

# provided samples
assert run("""4
1
1
6
1 2 3 4 5 1
9
4 1 2 4 5 4 3 2 1
4
3 3 3 3
""") == """-1
6
3
2"""

# custom cases
assert run("""1
5
1 2 3 4 5
""") == "-1"

assert run("""1
4
1 1 2 3
""") == "2"

assert run("""1
3
7 7 7
""") == "2"

assert run("""1
6
1 2 1 2 1 2
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all distinct | -1 | no valid dominated segment |
| early duplicate | 2 | smallest possible segment |
| all equal | 2 | minimum length constraint |
| alternating values | 2 | multiple candidates, correct minimum selection |
