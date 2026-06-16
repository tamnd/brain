---
title: "CF 978A - Remove Duplicates"
description: "We are given a sequence of integers and asked to compress it by removing duplicates, but with a specific rule: for every distinct value, only its last occurrence in the array must remain."
date: "2026-06-17T01:22:28+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 978
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 481 (Div. 3)"
rating: 800
weight: 978
solve_time_s: 82
verified: true
draft: false
---

[CF 978A - Remove Duplicates](https://codeforces.com/problemset/problem/978/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and asked to compress it by removing duplicates, but with a specific rule: for every distinct value, only its last occurrence in the array must remain. The final output is not just a set of unique values, but a filtered version of the original sequence where earlier appearances of repeated numbers disappear while the last appearance stays in place.

The key constraint is that the array size is at most 50. This immediately rules out any performance concerns. Even an approach that checks each element against all others would run in well under the time limit because the total number of operations would be on the order of a few thousand at worst. This means we can focus entirely on clarity and correctness rather than optimization pressure.

A subtle issue in problems of this type is that “keeping last occurrence” is direction-dependent. A naive forward scan that keeps the first time we see a value would produce the wrong answer. For example, in the array `[1, 2, 1]`, keeping first occurrences yields `[1, 2]`, but the correct output is `[2, 1]` because the second `1` is the one that must remain. Another failure case arises if we delete elements on the fly while scanning forward, since index shifting can cause later elements to be skipped or processed incorrectly. For instance, removing duplicates of `5` in `[5, 5, 6]` while iterating left-to-right can accidentally skip checks depending on implementation.

The correct reasoning must be anchored on the notion of “rightmost occurrence,” which is inherently easier to reason about when scanning from the end rather than the beginning.

## Approaches

A brute-force strategy would consider each element and search to the right to determine whether it appears again. If it does not appear later, we keep it; otherwise we discard it. This is logically correct because it directly encodes the definition of “last occurrence.” However, for each of the `n` elements, we may scan up to `n` positions ahead, leading to a worst-case complexity of about `n^2` checks.

While `n ≤ 50` makes this trivial in practice, the structure of the problem suggests a more elegant approach. Instead of repeatedly searching forward, we can reverse our perspective: process the array from right to left while recording which values we have already included. The first time we encounter a value in this reversed traversal is exactly its last occurrence in the original array. This observation removes the need for repeated scanning entirely.

We maintain a set of seen values. As we move from the end of the array to the beginning, we only take an element if it has not been seen before. This guarantees that each value is added exactly once, at the point corresponding to its last appearance. After collecting the result in reverse order, we reverse it back to restore the correct output order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (scan right for each element) | O(n²) | O(1) | Accepted |
| Optimal (reverse scan with set) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We build the answer by scanning from the end of the array so that we encounter each value at its last appearance first.

1. Start from the last element of the array and move leftward toward the first element. This direction ensures that the first time we see a value is its rightmost occurrence in the original sequence.
2. Maintain a set that stores values we have already included in the result. This set represents all values whose last occurrence has already been accounted for.
3. For each element during the backward scan, check whether it is already in the set.

If it is not present, this means we are currently at its last occurrence, so we add it to the result and insert it into the set.
4. If the element is already in the set, skip it because its last occurrence was encountered earlier in the scan.
5. After finishing the backward traversal, the collected result is in reverse order relative to the desired output, so reverse it once before printing.

### Why it works

The invariant is that at any point during the backward scan, the set contains exactly those values whose rightmost occurrence in the original array has already been processed and stored. Because we traverse from right to left, the first time we encounter a value corresponds precisely to its last position in the original array. This guarantees that each value is added exactly once, and never before its final occurrence. Reversing the collected sequence restores the original relative order among those last occurrences, since their ordering in the backward traversal is the reverse of their ordering in the original array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    seen = set()
    res = []
    
    for i in range(n - 1, -1, -1):
        if a[i] not in seen:
            seen.add(a[i])
            res.append(a[i])
    
    res.reverse()
    
    print(len(res))
    print(*res)

if __name__ == "__main__":
    solve()
```

The solution reads the array, then iterates from right to left. The `seen` set ensures we only keep the first time each value appears in this reversed traversal, which corresponds to its last occurrence in the original array. The result list is built in reverse order, so a final reversal restores the correct output ordering.

The only subtle implementation detail is that the reversal step is mandatory. Without it, the output would list elements in the order of their last occurrences from right to left, which is not the required format.

## Worked Examples

### Example 1

Input:

```
6
1 5 5 1 6 1
```

We scan from right to left.

| Index | Value | Seen before? | Action | Result so far |
| --- | --- | --- | --- | --- |
| 5 | 1 | no | add 1 | [1] |
| 4 | 6 | no | add 6 | [1, 6] |
| 3 | 1 | yes | skip | [1, 6] |
| 2 | 5 | no | add 5 | [1, 6, 5] |
| 1 | 5 | yes | skip | [1, 6, 5] |
| 0 | 1 | yes | skip | [1, 6, 5] |

After reversal:

```
5 6 1
```

This shows that each value is captured exactly at its last position, and earlier duplicates are ignored.

### Example 2

Input:

```
5
2 3 2 4 3
```

| Index | Value | Seen before? | Action | Result so far |
| --- | --- | --- | --- | --- |
| 4 | 3 | no | add 3 | [3] |
| 3 | 4 | no | add 4 | [3, 4] |
| 2 | 2 | no | add 2 | [3, 4, 2] |
| 1 | 3 | yes | skip | [3, 4, 2] |
| 0 | 2 | yes | skip | [3, 4, 2] |

After reversal:

```
2 4 3
```

This trace confirms that the algorithm preserves ordering of last occurrences while eliminating earlier duplicates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once during the reverse traversal, with O(1) average set operations |
| Space | O(n) | The set and result list together store at most n elements |

Given that `n ≤ 50`, this is well within constraints, but the linear approach remains the cleanest and most general solution.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        
        seen = set()
        res = []
        
        for i in range(n - 1, -1, -1):
            if a[i] not in seen:
                seen.add(a[i])
                res.append(a[i])
        
        res.reverse()
        print(len(res))
        print(*res)
    
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("6\n1 5 5 1 6 1\n") == "3\n5 6 1"

# custom cases
assert run("1\n7\n") == "1\n7"
assert run("4\n1 1 1 1\n") == "1\n1"
assert run("5\n1 2 3 4 5\n") == "5\n1 2 3 4 5"
assert run("5\n5 4 3 2 1\n") == "5\n5 4 3 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | itself | minimum input handling |
| all equal | one element | duplicate collapse |
| already unique increasing | unchanged | no removals needed |
| reverse ordered | preserves order | ordering stability |

## Edge Cases

For a single-element array like `[7]`, the reverse scan immediately adds `7` to the result because it is unseen. No further elements exist, so the output remains `[7]`, which matches the requirement that a single value is trivially its own last occurrence.

For an array where all elements are identical, such as `[1, 1, 1, 1]`, the backward scan adds `1` at the last position and then skips all earlier occurrences because they are already in the `seen` set. The result contains exactly one element, which is correct because only the rightmost occurrence must remain.

For a strictly increasing array like `[1, 2, 3, 4]`, every element is first encountered during the backward scan at its only occurrence, so all are included. Reversing restores the original order unchanged, confirming that the algorithm does not remove elements unnecessarily.
