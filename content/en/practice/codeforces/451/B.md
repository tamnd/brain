---
title: "CF 451B - Sort the Array"
description: "We are given an array of distinct integers. The task is to determine whether the entire array can become sorted in increasing order after reversing exactly one contiguous segment. If it is possible, we must print \"yes\" and one valid segment [l, r] whose reversal sorts the array."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 451
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 258 (Div. 2)"
rating: 1300
weight: 451
solve_time_s: 99
verified: true
draft: false
---

[CF 451B - Sort the Array](https://codeforces.com/problemset/problem/451/B)

**Rating:** 1300  
**Tags:** implementation, sortings  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct integers. The task is to determine whether the entire array can become sorted in increasing order after reversing exactly one contiguous segment.

If it is possible, we must print `"yes"` and one valid segment `[l, r]` whose reversal sorts the array. If it is impossible, we print `"no"`.

The array size can be as large as $10^5$. At this scale, algorithms that repeatedly copy or sort large portions of the array become expensive. A solution with quadratic behavior, such as trying every possible segment and checking the result, would require roughly $10^{10}$ operations in the worst case, which is far beyond the time limit. Linear or $O(n \log n)$ solutions are easily fast enough.

Several edge cases deserve attention.

Consider an already sorted array:

```
5
1 2 3 4 5
```

The correct answer is:

```
yes
1 1
```

Reversing a segment of length one changes nothing, so the requirement is still satisfied. A careless implementation might incorrectly print `"no"` because no decreasing portion exists.

Consider a completely reversed array:

```
3
3 2 1
```

The correct answer is:

```
yes
1 3
```

The whole array forms a single decreasing segment, and reversing it sorts the array.

Consider multiple separated inversions:

```
5
3 1 2 5 4
```

The correct answer is:

```
no
```

There is no single contiguous reversal that fixes both disorder locations. An implementation that only looks at the first inversion could mistakenly accept this case.

Consider a decreasing segment touching an endpoint:

```
5
1 5 4 3 6
```

The correct answer is:

```
yes
2 4
```

Boundary checks around the reversed segment must be handled carefully because one side may not exist.

## Approaches

A straightforward brute-force solution tries every possible segment $[l,r]$. For each choice, reverse that segment, check whether the resulting array is sorted, and stop if a valid segment is found.

This approach is correct because it explicitly examines every allowed operation. The problem is the running time. There are $O(n^2)$ possible segments. Checking whether the resulting array is sorted costs $O(n)$. The total complexity becomes $O(n^3)$, which is completely infeasible for $n=10^5$.

The key observation is that if a single reversal can sort the array, then all disorder must be concentrated in one contiguous decreasing block.

A useful way to see this is to compare the array with its sorted version. Since all values are distinct, every element has a unique correct position. If reversing one segment fixes the array, then the positions where the original array differs from the sorted array must form one continuous interval.

Instead of testing all reversals, we can construct the sorted version of the array. We then find the first position where the arrays differ and the last position where they differ. These positions define the only candidate segment worth reversing.

If reversing that segment produces the sorted array, the answer is `"yes"`. Otherwise, no valid segment exists.

This reduces the problem to one sort and one verification.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the array and create a sorted copy of it.
2. Find all positions where the original array differs from the sorted array.
3. If there are no differing positions, the array is already sorted. Output `"yes"` and the segment `1 1`.
4. Otherwise, let `l` be the first differing position and `r` be the last differing position.
5. Reverse the segment from `l` to `r` in a copy of the original array.
6. Compare the modified array with the sorted array.
7. If they are identical, output `"yes"` and the indices `l+1` and `r+1` because the problem uses 1-based indexing.
8. Otherwise, output `"no"`.

### Why it works

Let $b$ be the sorted version of the array.

Suppose some reversal sorts the array. Outside the reversed segment, elements never move, so those positions must already match $b$. Consequently, every mismatch between the original array and $b$ must lie inside one contiguous interval.

The first mismatch and the last mismatch uniquely determine the smallest interval containing all mismatches. Any valid reversal must cover exactly that interval. Reversing any smaller interval leaves at least one mismatch untouched, and reversing any larger interval changes positions that already match.

The algorithm reverses this only possible candidate interval and directly checks whether the result equals the sorted array. If it does, a valid reversal exists. If it does not, no single reversal can sort the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    b = sorted(a)

    diff = [i for i in range(n) if a[i] != b[i]]

    if not diff:
        print("yes")
        print(1, 1)
        return

    l = diff[0]
    r = diff[-1]

    c = a[:]
    c[l:r + 1] = reversed(c[l:r + 1])

    if c == b:
        print("yes")
        print(l + 1, r + 1)
    else:
        print("no")

solve()
```

The solution begins by creating the fully sorted target array. Since any successful result must equal this sorted version, it serves as the reference throughout the algorithm.

The list `diff` stores every position where the current array disagrees with the sorted array. If this list is empty, the array is already sorted. Reversing a length-one segment is allowed, so the answer is immediately `"yes"` with indices `1 1`.

When mismatches exist, the first and last mismatch define the only candidate segment. Reversing that range moves all potentially misplaced elements while leaving already-correct positions untouched.

The final comparison `c == b` acts as a complete correctness check. This avoids tricky case analysis about boundaries and neighboring values. If the reversed array matches the sorted array exactly, the segment works. Otherwise, no valid segment exists.

The most common implementation mistake is forgetting that the problem uses 1-based indices. Internally we work with Python's 0-based indexing and convert only when printing the answer.

## Worked Examples

### Example 1

Input:

```
3
3 2 1
```

Sorted array:

```
[1, 2, 3]
```

| Step | Value |
| --- | --- |
| Original array | [3, 2, 1] |
| Sorted array | [1, 2, 3] |
| Mismatch positions | [0, 2] |
| l | 0 |
| r | 2 |
| After reversal | [1, 2, 3] |
| Equals sorted array? | Yes |

Output:

```
yes
1 3
```

This example shows the case where the entire array is the segment that must be reversed.

### Example 2

Input:

```
5
1 5 4 3 6
```

Sorted array:

```
[1, 3, 4, 5, 6]
```

| Step | Value |
| --- | --- |
| Original array | [1, 5, 4, 3, 6] |
| Sorted array | [1, 3, 4, 5, 6] |
| Mismatch positions | [1, 3] |
| l | 1 |
| r | 3 |
| After reversal | [1, 3, 4, 5, 6] |
| Equals sorted array? | Yes |

Output:

```
yes
2 4
```

This trace demonstrates a decreasing block in the middle of the array. Reversing exactly that block restores sorted order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the running time |
| Space | $O(n)$ | Sorted copy and auxiliary arrays |

With $n \le 10^5$, an $O(n \log n)$ solution performs comfortably within the limits. The memory usage is linear and easily fits within the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        n = int(input())
        a = list(map(int, input().split()))

        b = sorted(a)

        diff = [i for i in range(n) if a[i] != b[i]]

        out = []

        if not diff:
            out.append("yes")
            out.append("1 1")
            return "\n".join(out)

        l = diff[0]
        r = diff[-1]

        c = a[:]
        c[l:r + 1] = reversed(c[l:r + 1])

        if c == b:
            out.append("yes")
            out.append(f"{l + 1} {r + 1}")
        else:
            out.append("no")

        return "\n".join(out)

    global input
    input = sys.stdin.readline
    return solve()

# provided sample
assert run("3\n3 2 1\n") == "yes\n1 3", "sample"

# already sorted
assert run("5\n1 2 3 4 5\n") == "yes\n1 1", "already sorted"

# middle segment reversal
assert run("5\n1 5 4 3 6\n") == "yes\n2 4", "middle decreasing block"

# impossible case
assert run("5\n3 1 2 5 4\n") == "no", "multiple disorder regions"

# minimum size
assert run("1\n42\n") == "yes\n1 1", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 42` | `yes 1 1` | Minimum array size |
| `1 2 3 4 5` | `yes 1 1` | Already sorted array |
| `1 5 4 3 6` | `yes 2 4` | Reversal entirely inside array |
| `3 1 2 5 4` | `no` | Multiple disorder regions |
| `3 2 1` | `yes 1 3` | Reversal of entire array |

## Edge Cases

Consider an already sorted array:

```
5
1 2 3 4 5
```

The sorted copy is identical to the original array. The mismatch list is empty, so the algorithm immediately outputs:

```
yes
1 1
```

A length-one reversal leaves the array unchanged, satisfying the requirement.

Consider a fully reversed array:

```
3
3 2 1
```

The mismatch positions are the first and last indices. The algorithm selects the entire array as the candidate segment. Reversing it produces the sorted array, yielding:

```
yes
1 3
```

Consider multiple separated inversions:

```
5
3 1 2 5 4
```

The sorted array is:

```
1 2 3 4 5
```

The first mismatch occurs at index 0 and the last mismatch occurs at index 4. Reversing the entire interval gives:

```
4 5 2 1 3
```

which is not sorted. The final comparison fails, so the algorithm correctly prints:

```
no
```

Consider a decreasing segment touching an endpoint:

```
5
5 4 3 2 6
```

The mismatches occupy the prefix. The algorithm chooses indices `0` through `3`, reverses that segment, and obtains:

```
2 3 4 5 6
```

which matches the sorted array. The output is:

```
yes
1 4
```

No special handling is required because the final equality check automatically validates boundary cases.
