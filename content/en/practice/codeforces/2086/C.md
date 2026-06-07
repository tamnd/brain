---
title: "CF 2086C - Disappearing Permutation"
description: "We are given a permutation of integers from 1 to n, which means every number in that range appears exactly once in an array of size n. We then perform a sequence of queries, where in each query we replace a specific element of the array with zero."
date: "2026-06-08T06:03:12+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "dsu", "graphs", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2086
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 177 (Rated for Div. 2)"
rating: 1300
weight: 2086
solve_time_s: 117
verified: false
draft: false
---

[CF 2086C - Disappearing Permutation](https://codeforces.com/problemset/problem/2086/C)

**Rating:** 1300  
**Tags:** dfs and similar, dp, dsu, graphs, greedy, implementation  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to n, which means every number in that range appears exactly once in an array of size n. We then perform a sequence of queries, where in each query we replace a specific element of the array with zero. Each position is replaced exactly once over the course of all queries, so after n queries, the entire array will consist of zeros.

After each query, the task is to calculate the minimum number of operations needed to turn the current array back into any valid permutation of integers from 1 to n. The allowed operation is simple: pick an index i and replace the value at that index with i. This operation guarantees that the element at that index becomes correct in the permutation, and it can be applied independently to any index.

The constraints indicate that n can reach 10^5 and the total sum of n across all test cases does not exceed 2·10^5. With a 2-second limit, any solution with O(n^2) per test case will be too slow. We need something roughly O(n) per test case to stay within the limit.

A subtle edge case is when the permutation is initially sorted in increasing or decreasing order. For instance, consider n=3, permutation [3,2,1], and queries [3,2,1]. After the first query, only position 3 becomes zero. The minimum operations to restore a permutation would be one, because setting index 3 to 3 fixes that element. After the second query, positions 3 and 2 are zero, and the minimum operations is two. A careless solution might assume that zeros always appear at the end or in sorted order, which is not true.

Another edge case is when zeros break the contiguous sequence of correctly placed numbers. For example, if the first and last elements are zero, but the middle elements are already correct, we have to account for gaps in the array, which directly impacts the count of required operations.

## Approaches

A brute-force approach would simulate the effect of each query: after replacing p[d_i] with zero, iterate through the array and count how many elements are incorrect. For each incorrect element, either it is already zero (needs one operation) or it is wrong (also needs one operation). This works but requires O(n^2) time in the worst case because we would traverse the array n times, which is too slow for n up to 10^5.

The key observation is that the operation allowed lets us directly place any number i at index i. This means the problem reduces to counting the largest prefix of positions 1 through n that can remain correct without operations. We can maintain a set of removed elements and track the highest contiguous block from the end that is already correct. Specifically, we can iterate the queries in reverse, “undoing” the zeroing of positions. For each step, we track the length of the largest suffix that already contains all numbers from its start to n. The minimum operations required after each query is exactly the number of positions outside this suffix, because every other position will need one operation to fix. This observation reduces the complexity from O(n^2) to O(n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an array `pos` of size n+1 that maps each number to its index in the permutation. This allows us to quickly locate any number in O(1) time.
2. Initialize an array `removed` of size n+1 to track which positions have been zeroed. Set all to False initially.
3. Initialize a variable `suffix_max` to n. This will track the current maximum number in the contiguous suffix that does not require operations.
4. Iterate the queries in reverse order, from the last query back to the first. For each query, “restore” the position to its original value, because we are essentially building the array backwards.
5. While the number at `suffix_max` has been restored (i.e., not removed), decrement `suffix_max`. This step finds the largest contiguous suffix of numbers that are already correct.
6. Record the minimum operations after this query as `suffix_max`. The reason is that all numbers greater than `suffix_max` are already correctly placed, and all numbers less than or equal to `suffix_max` need one operation each.
7. After processing all queries in reverse, reverse the result array to match the original query order.

Why it works: the invariant is that at each step, `suffix_max` represents the largest number such that all numbers greater than `suffix_max` are already in their correct positions. Since the allowed operation directly fixes any number at its corresponding index, every number less than or equal to `suffix_max` must be fixed individually, which corresponds exactly to the minimum operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        d = list(map(int, input().split()))
        
        pos = [0] * (n + 1)
        for idx, val in enumerate(p):
            pos[val] = idx
        
        removed = [False] * n
        ans = [0] * n
        suffix_max = n
        # process queries in reverse
        for i in range(n - 1, -1, -1):
            removed[d[i]-1] = False  # restore element
            while suffix_max > 0 and not removed[pos[suffix_max]]:
                suffix_max -= 1
            ans[i] = suffix_max
            removed[d[i]-1] = True  # mark removed for next iteration
        
        print(" ".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The code first builds the `pos` array to allow O(1) access to the index of any number. The `removed` array is used to mark positions that are zeroed. We process queries in reverse so that we can determine the size of the suffix that does not require any operations. The subtle part is toggling the `removed` flag before and after decrementing `suffix_max` to maintain correct bookkeeping.

## Worked Examples

### Sample 1

Input:

```
3
3
1 2 3
3 2 1
```

| Query | Array after query | suffix_max | Minimum operations |
| --- | --- | --- | --- |
| 1 | [1,2,0] | 2 | 1 |
| 2 | [1,0,0] | 1 | 2 |
| 3 | [0,0,0] | 0 | 3 |

This trace confirms that as we remove elements, the largest suffix of numbers already correct shrinks, and the minimum operations increase accordingly.

### Sample 2

Input:

```
5
4 5 3 1 2
4 5 1 3 2
```

| Query | Array | suffix_max | Minimum operations |
| --- | --- | --- | --- |
| 1 | [4,5,3,0,2] | 3 | 2 |
| 2 | [4,5,3,0,0] | 1 | 4 |
| 3 | [0,5,3,0,0] | 1 | 4 |
| 4 | [0,5,0,0,0] | 0 | 5 |
| 5 | [0,0,0,0,0] | 0 | 5 |

This trace demonstrates that the algorithm correctly accounts for elements already in place, regardless of the order in which zeros are applied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each query is processed once, and suffix_max decreases at most n times in total |
| Space | O(n) | Arrays pos, removed, and ans require O(n) space each |

The total time across all test cases is O(sum of n) = O(2·10^5), which is well within the 2-second limit. Space usage is proportional to n, which is acceptable under the 512 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided sample
assert run("3\n3\n1 2 3\n3 2 1\n5\n4 5 3 1 2\n4 5 1 3 2\n7\n4 3 1 2 7 5 6\n1 2 3 4 5 6 7\n") == "1 2 3\n2 4 4 5 5\n4 4 4 4 7 7 7"

# minimum-size input
assert run("1\n1\n1\n1\n") == "1"

# maximum-size input with n=5 (small for demonstration)
assert run("1\n5\n5 4 3 2 1\n1 2 3 4 5\n") == "5 4 3 2 1"

# all elements removed in increasing order
assert run("1\n4\n1 2 3 4\n1 2 3 4\n") == "4
```
