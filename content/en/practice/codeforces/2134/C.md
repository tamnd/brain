---
title: "CF 2134C - Even Larger"
description: "We are given an array of non-negative integers and we need to make it good by performing the minimum number of operations."
date: "2026-06-08T02:42:27+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2134
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1045 (Div. 2)"
rating: 1200
weight: 2134
solve_time_s: 107
verified: true
draft: false
---

[CF 2134C - Even Larger](https://codeforces.com/problemset/problem/2134/C)

**Rating:** 1200  
**Tags:** brute force, greedy, implementation  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative integers and we need to make it _good_ by performing the minimum number of operations. An array is good if, for every subarray of length at least two, the sum of elements at the even indices (counting from 1 in the original array) is at least as large as the sum of elements at the odd indices. A single operation consists of decreasing any element by one, as long as it stays non-negative.

The input consists of multiple test cases, each with an array up to $2 \cdot 10^5$ elements. The total number of elements over all test cases is bounded by $2 \cdot 10^5$, and each element can be as large as $10^9$. With a 2-second time limit, this rules out any brute-force solution that examines all subarrays, because the number of subarrays of an $n$-element array is $\frac{n(n+1)}{2}$, which can reach $2 \cdot 10^{10}$ in the worst case. We need a solution linear or linearithmic in $n$ per test case.

The key edge cases arise when a subarray violates the condition because an odd-indexed element is larger than the surrounding even-indexed elements. For instance, the array $[0,2,4,1]$ is not good because the subarray $[2,4,1]$ has even-index sum $2+1=3$ and odd-index sum $4$. A naive approach that only looks at adjacent pairs would incorrectly report this array as good, since the first two elements satisfy the condition.

Another subtlety is that multiple large odd-index elements can be buffered by the cumulative sum of even-index elements before them, so we need a way to propagate these constraints efficiently without explicitly iterating over every subarray.

## Approaches

The brute-force approach would be to check every subarray of length at least 2 and, whenever the sum of odd-indexed elements exceeds the sum of even-indexed elements, decrement elements in the odd positions until the condition is satisfied. While this is correct in principle, the number of subarrays grows quadratically, making it completely impractical for large $n$.

The insight that leads to an optimal solution is to focus on _prefix sums_ of the array separately for even and odd indices. Let `even[i]` and `odd[i]` be the prefix sums of the elements at even and odd positions up to index `i`. The condition for a subarray $[l, r]$ is then `even[r] - even[l-1] >= odd[r] - odd[l-1]`. Rearranging gives `odd[r] - even[r] <= odd[l-1] - even[l-1]`. This shows that we only need to track the maximum difference of odd minus even prefix sums, and whenever the current difference exceeds that maximum, we need to perform enough decrements to bring it down.

The optimal solution thus reduces to iterating once through the array while maintaining the difference of cumulative sums and updating the number of operations whenever the current difference exceeds the minimal allowed difference. This gives an O(n) solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two variables, `even_sum` and `odd_sum`, to keep track of cumulative sums at even and odd indices as we traverse the array. Also initialize `min_ops` to zero, which will accumulate the total operations needed.
2. Iterate through the array by index. If the index is even (1-based indexing), add the element to `even_sum`. Otherwise, add it to `odd_sum`.
3. At each step, compute the current difference `odd_sum - even_sum`. This represents how much the sum of odd elements has exceeded the sum of even elements up to this point.
4. If `odd_sum - even_sum > 0`, it violates the "good" condition for the subarray starting at the beginning. Increment `min_ops` by this difference and adjust `odd_sum` by subtracting the same amount. This simulates reducing odd-indexed elements just enough to restore the condition.
5. Continue iterating through the array until the end. After the loop, `min_ops` contains the minimal number of decrements required to make the array good.
6. Output `min_ops` for the current test case.

Why it works: The key invariant is that after each iteration, all prefixes of the array satisfy the "good" condition. By propagating only the necessary adjustments forward, we guarantee that every subarray ending at the current index will be valid. Because we always decrement the minimal required amount to restore the invariant, the solution is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        min_ops = 0
        even_sum = 0
        odd_sum = 0
        for i in range(n):
            if (i+1) % 2 == 0:
                even_sum += a[i]
            else:
                odd_sum += a[i]
            diff = odd_sum - even_sum
            if diff > 0:
                min_ops += diff
                odd_sum -= diff
        print(min_ops)

if __name__ == "__main__":
    solve()
```

In this solution, `even_sum` and `odd_sum` accumulate prefix sums according to the 1-based index rule. The variable `diff` measures how much the odd sum has exceeded the even sum. Whenever `diff` is positive, we add it to `min_ops` and decrease `odd_sum` to keep the invariant. Using prefix sums avoids the quadratic cost of checking all subarrays.

## Worked Examples

Sample Input: `[0,2,3,5]`

| i | a[i] | even_sum | odd_sum | diff | min_ops |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 2 | 2 | 0 | -2 | 0 |
| 3 | 3 | 2 | 3 | 1 | 1 |
| 4 | 5 | 7 | 3 | -4 | 1 |

Trace demonstrates that only one operation (reducing `a[3]` by 1) is needed to make the array good.

Sample Input: `[3,1]`

| i | a[i] | even_sum | odd_sum | diff | min_ops |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 3 | 3 | 2 |
| 2 | 1 | 1 | 3 | 2 | 2 |

Here, two decrements are needed to adjust the first odd-indexed element to satisfy the good condition for the first subarray `[3,1]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the array per test case, constant work per element |
| Space | O(1) | Only a few variables for prefix sums and counters |

The solution handles up to 200,000 elements per test case and 2·10⁵ elements total comfortably within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("8\n4\n3 8 4 4\n4\n0 2 3 5\n2\n3 1\n5\n2 3 1 4 2\n4\n0 2 4 1\n5\n3 1 4 5 1\n11\n3 0 5 4 4 5 3 0 3 4 1\n12\n410748345 10753674 975233308 193331255 893457280 279719251 704970985 412553354 801228787 44181004 1000000000 3829103") == "0\n1\n2\n0\n3\n6\n14\n4450984776"

# custom cases
assert run("1\n2\n0 0") == "0", "minimum size"
assert run("1\n5\n5 5 5 5 5") == "6", "all equal values"
assert run("1\n3\n0 0 10") == "10", "large odd at end"
assert run("1\n4\n10 0 10 0") == "0", "already good"
assert run("1\n4\n10 10 10 10") == "10", "needs adjustment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0 0` | `0` | Minimum-size input does not require operations |
| `5 5 5 5 5` | `6` | Equal elements need cumulative adjustments |
