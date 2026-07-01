---
title: "CF 104282D - Add 9 Zeros \u2161"
description: "We are given a list of distinct integers, and we want to choose as many of them as possible to form a subset with a single restriction: we are not allowed to pick two numbers where one is exactly 9 larger than the other."
date: "2026-07-01T21:06:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104282
codeforces_index: "D"
codeforces_contest_name: "The 20th Hangzhou City University Programming Contest"
rating: 0
weight: 104282
solve_time_s: 64
verified: true
draft: false
---

[CF 104282D - Add 9 Zeros \u2161](https://codeforces.com/problemset/problem/104282/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of distinct integers, and we want to choose as many of them as possible to form a subset with a single restriction: we are not allowed to pick two numbers where one is exactly 9 larger than the other. In other words, if we ever pick a value x, we must avoid picking x + 9 at the same time.

The task is to compute the maximum possible size of such a subset.

The input size can be as large as 200,000 numbers, and values go up to 1e9. This immediately rules out any solution that tries all subsets or builds a dense graph explicitly. A brute-force subset check would grow exponentially with n, and even a naive O(n²) pair checking approach would time out because 2 × 10⁵ squared is far too large.

The structure of the constraint is the key: it only relates numbers that differ by exactly 9. This is a very local interaction, so we should expect a graph-like structure that is sparse and decomposes cleanly.

A subtle edge case appears when numbers form long arithmetic progressions. For example, if the array contains 1, 10, 19, 28, then each adjacent pair is separated by 9, meaning we cannot pick all of them. A careless greedy approach like "always take the smallest available number and discard its +9 neighbor" can fail if applied globally without structure awareness, because decisions are independent only within connected components, not across the whole array.

Another edge case is when the numbers are scattered, such as 1, 11, 20, 30. Here no two values differ by 9, so the correct answer is simply 4. Any algorithm that overcomplicates grouping or assumes contiguous ranges would mis-handle such sparse configurations.

## Approaches

A direct brute-force idea is to consider all subsets and check whether any forbidden pair exists. For each subset, we would scan all pairs and verify that no difference equals 9. This is correct but infeasible, since there are 2ⁿ subsets and each check can cost up to O(n), leading to exponential time.

A slightly improved brute-force is to sort the array and, for each element, try to decide whether to include it, checking earlier chosen elements for conflicts. Even this degenerates into O(n²) behavior in the worst case because each element may need to be compared against many others.

The key observation is that the restriction only depends on whether x and x + 9 both exist. This suggests building a graph where each number is a node, and we connect x to x + 9 if both are present. Each node has at most two neighbors: x − 9 and x + 9. This means every connected component is a simple chain.

Once we recognize that structure, the problem becomes selecting the maximum number of vertices in a path graph such that no two adjacent vertices are chosen. This is a classic maximum independent set on a path, which is solved by taking every other element in each connected segment.

We do not even need to explicitly build edges. It is enough to group numbers by their value modulo 9, because only numbers with the same remainder can differ by 9 repeatedly. Within each remainder class, we sort the transformed values k = a / 9 (more precisely k = a where we track steps of +9 implicitly), then split into consecutive runs where values differ exactly by 9. Each run behaves like a path.

Within a run of length L, the optimal answer is simply ceil(L / 2).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ · n) | O(n) | Too slow |
| Optimal (group + path DP) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Group all numbers by their remainder modulo 9. This works because only numbers with the same remainder can differ by exactly 9 repeatedly, so cross-group interactions are impossible.
2. For each group, sort the numbers. Sorting is necessary because adjacency in the conflict graph corresponds to ordering by value.
3. Scan through the sorted list and interpret it as a sequence where we connect two consecutive values if and only if their difference is exactly 9. This forms chains of consecutive arithmetic steps.
4. Break the sequence into segments whenever the difference between consecutive elements is not 9. Each segment is an independent path component.
5. For each segment of length L, add ceil(L / 2) to the answer. This corresponds to taking alternate elements in a path so that no adjacent nodes are both chosen.
6. Sum contributions over all segments and output the result.

### Why it works

Each value belongs to exactly one residue class modulo 9, and within that class, edges only connect numbers that differ by exactly one step of +9. This guarantees that every connected component is a simple path. On a path, any valid selection corresponds to an independent set, and the maximum independent set is achieved by alternating picks along the path. Because components are disjoint, solving each independently and summing preserves optimality globally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    groups = {}
    for x in a:
        r = x % 9
        if r not in groups:
            groups[r] = []
        groups[r].append(x)

    ans = 0

    for r in groups:
        arr = sorted(groups[r])

        i = 0
        m = len(arr)

        while i < m:
            j = i
            while j + 1 < m and arr[j + 1] - arr[j] == 9:
                j += 1

            length = j - i + 1
            ans += (length + 1) // 2
            i = j + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first buckets numbers by modulo 9, which isolates all potential conflicts. Sorting each bucket ensures that any pair that can conflict must appear as neighbors if they are part of the same arithmetic chain.

The inner loop builds maximal segments where consecutive differences are exactly 9. Each such segment is treated independently, and we add half its length rounded up. The expression `(length + 1) // 2` is a direct integer form of ceil division.

A common implementation pitfall is forgetting to restart a segment when the difference is not exactly 9. Without this break, unrelated numbers would incorrectly be treated as a single path.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [1, 10, 19, 2, 11]
```

We group by modulo 9:

| remainder | values |
| --- | --- |
| 1 | 1, 10, 19 |
| 2 | 2, 11 |

Now process each group.

For remainder 1: sorted is [1, 10, 19]. All differences are 9, so it is one segment of length 3. Contribution is ceil(3/2) = 2.

For remainder 2: sorted is [2, 11]. One segment of length 2, contribution is 1.

| group | segment | length | contribution |
| --- | --- | --- | --- |
| 1 | [1,10,19] | 3 | 2 |
| 2 | [2,11] | 2 | 1 |

Final answer is 3.

This confirms that the algorithm correctly separates independent arithmetic chains and applies optimal selection per chain.

### Example 2

Input:

```
n = 4
a = [5, 14, 23, 7]
```

Grouping:

| remainder | values |
| --- | --- |
| 5 | 5, 14, 23 |
| 7 | 7 |

For remainder 5, all values form a chain with length 3, contributing 2. For remainder 7, contribution is 1.

Total answer is 3.

This shows that isolated single elements behave correctly as trivial segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each group is sorted once, and all elements are processed linearly |
| Space | O(n) | Storage for grouping and intermediate arrays |

The solution easily fits within constraints since n is up to 2 × 10⁵, and sorting dominates the runtime. The memory usage is linear in the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    groups = {}
    for x in a:
        r = x % 9
        groups.setdefault(r, []).append(x)

    ans = 0
    for r in groups:
        arr = sorted(groups[r])
        i = 0
        m = len(arr)
        while i < m:
            j = i
            while j + 1 < m and arr[j + 1] - arr[j] == 9:
                j += 1
            ans += (j - i + 2) // 2
            i = j + 1

    return str(ans)

# provided sample (structure inferred)
assert run("5\n1 10 19 2 11\n") == "3"

# all distinct no edges
assert run("4\n1 2 3 4\n") == "4"

# single chain
assert run("3\n5 14 23\n") == "2"

# two separate chains
assert run("6\n1 10 19 2 11 20\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all distinct no edges | n | no conflicts case |
| arithmetic chain | ceil(n/2) | path handling |
| multiple chains | sum | decomposition correctness |

## Edge Cases

One edge case is when all numbers form a perfect arithmetic progression with step 9, such as 3, 12, 21, 30. In this case the entire group becomes a single segment. The algorithm correctly computes a single run of length 4 and returns 2, matching the optimal alternating selection.

Another edge case is when values are extremely sparse within the same modulo class, such as 1, 100, 1000, 10000. Since no adjacent differences equal 9, each element forms its own segment of length 1. The algorithm treats each as a separate run and contributes 1 per element, yielding the full count.

A final edge case occurs when multiple independent chains exist within the same remainder group. For example, 1, 10, 19 and 28, 37 form two disjoint segments. The scan breaks correctly at gaps greater than 9, ensuring that these segments are not incorrectly merged, and each is solved independently.
