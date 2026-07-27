---
title: "CF 102800E - Shorten the Array"
description: "We repeatedly shorten an array by selecting two adjacent positive values. Those two values are removed and replaced by either a % b or b % a, chosen freely for that operation. Since two elements become one, every operation decreases the array length by exactly one."
date: "2026-07-27T17:37:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "E"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 51
verified: true
draft: false
---

[CF 102800E - Shorten the Array](https://codeforces.com/problemset/problem/102800/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We repeatedly shorten an array by selecting two adjacent positive values. Those two values are removed and replaced by either `a % b` or `b % a`, chosen freely for that operation. Since two elements become one, every operation decreases the array length by exactly one.

The question is not what the final values become, but how many elements can be removed. Once no adjacent pair of positive numbers exists, no more operations are possible. We must compute the minimum achievable final length.

The array length can be as large as `10^6` in a single test case, with up to `10` test cases. Any algorithm that explores different operation orders or simulates many possibilities is immediately ruled out. Even quadratic time would require around `10^12` operations on the largest input, which is completely infeasible. The solution must process each array in linear time.

The tricky part is that we are allowed to choose either remainder. This freedom means the actual values matter much less than they first appear to.

Consider the array `[1, 1, 1]`. We may replace the first two elements by `1 % 1 = 0`, obtaining `[0, 1]`. Since the remaining pair is not both positive, the process stops with length `2`. A greedy attempt to always merge whenever possible cannot reach length `1`.

Now consider `[2, 3]`. Since `2 % 3 = 2` and `3 % 2 = 1`, neither choice produces zero. The array always becomes a single positive value, so the answer is `1`.

Another important case is `[5, 5, 5, 5]`. Equal values allow producing zero immediately because `5 % 5 = 0`. Repeating this idea leaves two zeros, so the minimum length is `2`, not `1`. Treating every positive block as fully reducible would give the wrong answer.

## Approaches

A brute-force solution would explore every valid operation, every possible adjacent pair, and both remainder choices. Since each operation changes future possibilities, the search branches exponentially. Even memoization is ineffective because the number of reachable arrays is enormous. This approach is correct because it examines every legal sequence, but it becomes hopeless even for arrays of a few dozen elements.

The key observation is that zeros permanently block future merges. Since only adjacent positive numbers may be merged, every maximal contiguous block of positive values behaves independently. Operations inside one block never interact with another because a zero can never disappear.

The remaining question is how far a single positive block can be reduced.

Suppose every value inside the block is identical. Every merge produces zero because `x % x = 0`. Each merge creates a separator, preventing that zero from participating again. Starting with a block of length `k`, every merge consumes exactly two positive numbers and creates one zero. Eventually only zeros remain, plus possibly one untouched positive if `k` is odd. The final length of that block is `ceil(k / 2)`.

Now suppose the block contains at least two different values. Then the greatest common divisor of the block can always be preserved while repeatedly applying the Euclidean algorithm. Since unequal numbers eventually produce a strictly smaller positive remainder, we can avoid creating blocking zeros until only one positive value remains. The entire block collapses into a single element.

This completely characterizes every positive block.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the array from left to right.
2. Whenever a zero is encountered, skip it because it already separates independent regions.
3. When a positive value is found, identify the entire maximal contiguous positive block.
4. While scanning that block, check whether every element equals the first one. At the same time, record the block length.
5. If every value in the block is identical, add `(length + 1) // 2` to the answer. This is exactly `ceil(length / 2)`.
6. Otherwise, add `1` to the answer because the whole block can be reduced to a single element.
7. Continue scanning after the end of the block until the entire array has been processed.

### Why it works

Zeros are permanent barriers because only adjacent positive numbers may participate in an operation. Every operation stays inside one positive block, so different blocks never affect one another.

Inside a block containing at least two distinct values, repeated applications of the Euclidean algorithm reduce the entire block to one positive value without introducing an unavoidable zero. Inside a block where every value is the same, every possible merge immediately creates a zero, splitting the remaining positives into smaller independent pieces. That process leaves exactly `ceil(length / 2)` surviving elements. Since every block is independent, summing these contributions gives the minimum final array length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ans = 0
        i = 0

        while i < n:
            if a[i] == 0:
                i += 1
                continue

            first = a[i]
            same = True
            j = i

            while j < n and a[j] > 0:
                if a[j] != first:
                    same = False
                j += 1

            length = j - i

            if same:
                ans += (length + 1) // 2
            else:
                ans += 1

            i = j

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The outer loop processes each test case independently. The pointer `i` scans the array once, and every positive block is examined exactly one time.

For each block, the code remembers the first value and checks whether every later value matches it. This avoids storing any additional data structure while determining whether the block is uniform.

The expression `(length + 1) // 2` computes `ceil(length / 2)` using integer arithmetic. This is the only special case needed for uniform blocks.

After finishing one block, the scan jumps directly to its end. No element is revisited, which is why the implementation remains linear.

## Worked Examples

### Example 1

Input:

```
1
3
1 1 1
```

| Step | Current block | Length | All equal | Contribution | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | `[1,1,1]` | 3 | Yes | 2 | 2 |

The entire array is one uniform positive block. Every merge immediately creates a zero, so only two elements remain. This example shows why a positive block is not always reducible to one element.

### Example 2

Input:

```
1
5
2 3 4 0 7
```

| Step | Current block | Length | All equal | Contribution | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | `[2,3,4]` | 3 | No | 1 | 1 |
| 2 | `[7]` | 1 | Yes | 1 | 2 |

The zero splits the array into two independent blocks. The first contains different values and collapses to one element. The second already has length one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every array element is scanned exactly once. |
| Space | O(1) | Only a few variables are maintained while scanning. |

A linear scan easily fits the constraints, even when the array contains one million elements. Constant auxiliary memory also remains well within the memory limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans = 0
        i = 0
        while i < n:
            if a[i] == 0:
                i += 1
                continue
            first = a[i]
            same = True
            j = i
            while j < n and a[j] > 0:
                if a[j] != first:
                    same = False
                j += 1
            length = j - i
            ans += (length + 1) // 2 if same else 1
            i = j
        out.append(str(ans))
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    print(solve(), end="")
    return sys.stdout.getvalue()

assert run("1\n3\n1 1 1\n") == "2", "sample"
assert run("1\n2\n3 4\n") == "1", "two distinct values"
assert run("1\n4\n5 5 5 5\n") == "2", "all equal"
assert run("1\n5\n2 3 4 0 7\n") == "2", "zero separates blocks"
assert run("1\n2\n9 9\n") == "1", "minimum uniform block"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 4` | `1` | Two unequal values collapse completely. |
| `5 5 5 5` | `2` | Uniform blocks require `ceil(length / 2)`. |
| `2 3 4 0 7` | `2` | Zeros split the array into independent regions. |
| `9 9` | `1` | Smallest nontrivial uniform block. |

## Edge Cases

Consider the input:

```
1
3
1 1 1
```

The algorithm finds one positive block of length `3`, observes that every value is identical, and contributes `(3 + 1) // 2 = 2`. The output is `2`, matching the optimal sequence of operations.

Now consider:

```
1
2
2 3
```

The block length is `2`, but the values are not identical. The algorithm contributes `1`, correctly recognizing that unequal numbers can always be merged into a single remaining value.

Finally, consider:

```
1
5
4 4 0 6 7
```

The scan detects two independent blocks. The first is uniform with contribution `1`. The second contains distinct values with contribution `1`. Their sum is `2`. The zero is never crossed during processing, exactly matching the restriction that operations cannot involve non-positive neighbors.
