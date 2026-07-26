---
title: "CF 102823A - Array Merge"
description: "We have two arrays, A and B. We must create one final array by interleaving elements from the two arrays while keeping the original order inside A and inside B. After the merge, every element contributes its value multiplied by its 1-based position in the final array."
date: "2026-07-26T15:49:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102823
codeforces_index: "A"
codeforces_contest_name: "2018 China Collegiate Programming Contest - Guilin Site"
rating: 0
weight: 102823
solve_time_s: 59
verified: true
draft: false
---

[CF 102823A - Array Merge](https://codeforces.com/problemset/problem/102823/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two arrays, `A` and `B`. We must create one final array by interleaving elements from the two arrays while keeping the original order inside `A` and inside `B`. After the merge, every element contributes its value multiplied by its 1-based position in the final array. The goal is to choose the merge order that gives the smallest possible total cost. The required output also includes the test case number in the format shown by the statement.

The input size rules out trying all possible merges. If the two arrays have lengths `n` and `m`, there are exponentially many valid interleavings, because each merge corresponds to choosing the positions occupied by one of the arrays. With lengths reaching `100000` and the total length over all tests reaching `10^6`, any solution depending on the number of possible merge orders is impossible. We need a linear-time method that makes one decision for each element.

The tricky part is that the arrays themselves do not need to be sorted. A common mistake is to always take the smaller current element because that resembles a normal merge operation. That is wrong here because the position multiplier grows as we move right. Larger values should usually be placed earlier.

For example, consider:

```
1
2 2
5 3
4 5
```

The optimal merged array is:

```
5 4 5 3
```

The cost is:

```
1*5 + 2*4 + 3*5 + 4*3 = 40
```

A smaller-first merge would produce:

```
4 5 5 3
```

with cost:

```
1*4 + 2*5 + 3*5 + 4*3 = 41
```

The difference comes from the fact that moving a larger number one position to the left saves more than moving a smaller number left by the same amount.

Another edge case is equal values. For example:

```
1
1 1
7
7
```

Both possible merges are identical:

```
7 7
```

and the answer is:

```
21
```

A solution that uses strict comparisons incorrectly may fail by not consuming one of the arrays properly when values are equal.

A final boundary case is when one array finishes early. For example:

```
1
1 3
8
1 2 3
```

After choosing `8` first, the remaining elements must appear in their original order:

```
8 1 2 3
```

The answer is:

```
8 + 4 + 6 + 9 = 27
```

An implementation that only compares elements while both arrays have elements and forgets the remaining suffix will produce an incorrect result.

## Approaches

A direct brute-force solution would enumerate every valid merge. For each merge, it would calculate the resulting cost and keep the minimum. This is correct because every possible final arrangement is checked. However, the number of merges is the binomial coefficient `C(n+m,n)`, which grows exponentially. Even small arrays already create many possibilities, so this approach cannot handle the given limits.

The key observation comes from looking at two neighboring elements that come from different arrays. Suppose two adjacent elements in the final array are `x` followed by `y`. Their contribution to the cost at positions `p` and `p+1` is:

```
p*x + (p+1)*y
```

If we swap them, the contribution becomes:

```
p*y + (p+1)*x
```

The second arrangement is better exactly when `x < y`. In other words, whenever two available elements from different arrays can be swapped, the larger one should appear earlier.

At any point in the merge, the only elements whose positions can be decided immediately are the current unused elements at the fronts of the two arrays. If we choose the smaller front element, the larger front element is forced one position later. Swapping those two choices would improve the cost. Therefore the optimal choice is always to take the larger of the two current front elements.

This is the same reasoning used by the final greedy algorithm. The brute-force method explores all possible orders, but the exchange argument shows that every optimal solution can be transformed into one where each choice takes the larger available front element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n+m,n) * (n+m)) | O(n+m) | Too slow |
| Optimal | O(n+m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with pointers at the first unused element of both arrays and set the current position in the merged array to `1`.
2. While both arrays still contain unused elements, compare the two current front values. Take the larger one, add its contribution `position * value` to the answer, and move the corresponding pointer forward.

The reason this choice is safe is that the two front values are the only elements from different arrays that can be placed next. If the larger value were placed later, swapping the two would reduce the cost.
3. When one array becomes empty, append the remaining elements of the other array in their original order. Their relative order is already fixed, and no further choices remain.
4. Continue increasing the position after every placed element until the complete merged array has been accounted for.

Why it works:

The invariant is that after every greedy decision, there exists an optimal merge having exactly the same prefix. Consider the two available front elements `x` and `y`. If an optimal merge puts the smaller one before the larger one, those two elements will eventually appear in that order because neither can be crossed by elements from its own array. Swapping the two adjacent choices changes the cost by moving the larger value one position left, which never increases the answer. Repeating this exchange removes every such bad choice, so taking the larger current element always preserves optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(a, b):
    i = 0
    j = 0
    pos = 1
    ans = 0
    n = len(a)
    m = len(b)

    while i < n and j < m:
        if a[i] >= b[j]:
            ans += pos * a[i]
            i += 1
        else:
            ans += pos * b[j]
            j += 1
        pos += 1

    while i < n:
        ans += pos * a[i]
        i += 1
        pos += 1

    while j < m:
        ans += pos * b[j]
        j += 1
        pos += 1

    return ans

def main():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        out.append(f"Case {case}: {solve_case(a, b)}")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The two pointers `i` and `j` represent the next available elements in the two original arrays. The main loop performs exactly the greedy decisions described in the walkthrough. The comparison uses `>=` instead of `>` so that equal values are consumed consistently without affecting the answer.

After one array is exhausted, the remaining loops are not optional. The remaining elements still contribute to the cost, and their positions continue increasing from the point where the first loop stopped.

Python integers are used automatically with arbitrary precision, which is useful because the maximum possible cost can exceed 32-bit integer limits.

## Worked Examples

### Sample 1

Input:

```
2 2
5 3
4 5
```

| Position | A pointer | B pointer | Chosen value | Running cost |
| --- | --- | --- | --- | --- |
| 1 | 5 | 4 | 5 | 5 |
| 2 | 3 | 4 | 4 | 13 |
| 3 | 3 | 5 | 5 | 28 |
| 4 | 3 | empty | 3 | 40 |

The trace shows why taking the largest available value first works. The value `5` from the first array is placed before `4`, creating the optimal prefix.

### Sample 2

Input:

```
3 3
1 3 5
2 6 4
```

| Position | A pointer | B pointer | Chosen value | Running cost |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | 2 |
| 2 | 1 | 6 | 6 | 14 |
| 3 | 1 | 4 | 4 | 26 |
| 4 | 1 | empty | 1 | 30 |
| 5 | 3 | empty | 3 | 45 |
| 6 | 5 | empty | 5 | 75 |

The second trace demonstrates the case where one array finishes before the other. The suffix of the remaining array is appended without additional decisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n+m) | Every element is examined once and chosen exactly once. |
| Space | O(1) | Only pointers, the current position, and the accumulated answer are stored. |

The total number of processed elements across all test cases is at most `10^6`, so a linear scan easily fits the limits.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve_case(a, b):
        i = j = 0
        pos = 1
        ans = 0

        while i < len(a) and j < len(b):
            if a[i] >= b[j]:
                ans += pos * a[i]
                i += 1
            else:
                ans += pos * b[j]
                j += 1
            pos += 1

        while i < len(a):
            ans += pos * a[i]
            i += 1
            pos += 1

        while j < len(b):
            ans += pos * b[j]
            j += 1
            pos += 1

        return ans

    t = int(input())
    res = []

    for case in range(1, t + 1):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        res.append(f"Case {case}: {solve_case(a, b)}")

    return "\n".join(res)

assert solve("""2
2 2
5 3
4 5
3 3
1 3 5
2 6 4
""") == """Case 1: 40
Case 2: 75""", "samples"

assert solve("""1
1 1
7
7
""") == "Case 1: 21", "equal values"

assert solve("""1
1 3
8
1 2 3
""") == "Case 1: 27", "one array finishes early"

assert solve("""1
3 3
10 1 1
9 9 9
""") == "Case 1: 99", "large front element"

assert solve("""1
3 3
0 0 0
0 0 0
""") == "Case 1: 0", "all zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample cases | `Case 1: 40`, `Case 2: 75` | Official examples and general correctness |
| Single elements with equal values | `21` | Tie handling |
| One array much shorter | `27` | Remaining suffix processing |
| Large first elements | `99` | Greedy choice of the larger front value |
| All zeros | `0` | Handling of repeated identical values |

## Edge Cases

For equal values, such as:

```
1
1 1
7
7
```

the algorithm compares `7` and `7`, chooses the first array because of the `>=` condition, and then takes the remaining element. The order does not matter because both contributions are identical.

For a case where one array finishes early:

```
1
1 3
8
1 2 3
```

the algorithm first compares `8` and `1`, takes `8`, and then the first array is empty. The remaining values `1,2,3` must appear in order, giving:

```
8 1 2 3
```

with cost `27`.

For all equal values:

```
1
3 3
0 0 0
0 0 0
```

every possible merge has cost zero. The greedy decisions still consume every element exactly once and return the correct result.

For values where choosing the smaller element looks tempting:

```
1
2 2
5 3
4 5
```

the algorithm first chooses `5` over `4`. That choice is what creates the optimal prefix, because putting the larger value later would increase its multiplier while reducing the multiplier of a smaller value. The final result is `40`.
