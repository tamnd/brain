---
title: "CF 106179B - Pseudo Palindrome"
description: "The problem asks whether an array can be rearranged so that every pair of elements placed symmetrically from the two ends is close enough."
date: "2026-06-25T10:54:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106179
codeforces_index: "B"
codeforces_contest_name: "ICPC India Online Prelims (2025 - 2026)"
rating: 0
weight: 106179
solve_time_s: 35
verified: true
draft: false
---

[CF 106179B - Pseudo Palindrome](https://codeforces.com/problemset/problem/106179/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks whether an array can be rearranged so that every pair of elements placed symmetrically from the two ends is close enough. After choosing some permutation of the array, the first and last values must differ by at most `d`, the second and second-last values must differ by at most `d`, and so on. The task is only to decide if such an ordering exists. The original problem is from Codeforces Gym 106179.

The input contains several test cases. Each test case gives the length of the array, the allowed maximum difference `d`, and the values in the array. The output is `YES` if some rearrangement satisfies all symmetric pair conditions, otherwise it is `NO`.

The total number of array elements across all test cases is at most 2000, and an individual array can have length 2000. This means an `O(n^2)` solution is technically possible, but it is useful to search for a simpler structure because the operation being checked is based on ordering. The values themselves can be as large as `10^9`, so solutions should avoid assumptions about small ranges or frequency arrays.

A common mistake is to only check whether the minimum and maximum values are within distance `d`. That condition is necessary but not sufficient. For example:

```
1
4 5
1 4 10 12
```

The minimum and maximum differ by `11`, so this already fails, but a different mistake is possible when the extremes are fine but inner pairs fail. Consider:

```
1
6 5
1 5 6 10 11 12
```

The smallest and largest values differ by `11`, so this one is also clearly impossible. The more useful edge case is a single element:

```
1
1 0
100
```

The answer is `YES`. There is no pair to violate the condition, and any implementation that blindly checks a mirrored index without handling the center position can incorrectly reject it.

Another edge case is when `d` is zero. For example:

```
1
4 0
7 7 7 8
```

The answer is `NO`. Every mirrored pair must contain exactly equal values, and the single `8` cannot be matched. A solution that only checks neighboring differences after sorting may miss this because the array is almost uniform.

## Approaches

A direct approach is to try possible rearrangements and check whether every symmetric pair is valid. This is correct because it examines exactly the condition required by the problem. However, the number of possible orders is `n!`, which becomes impossible even for small arrays.

A more reasonable brute force would sort the array and try to build pairs greedily, or use backtracking on the pairs. The problem is that the number of possible pair assignments still grows too quickly. With `n = 2000`, even an `O(n^2)` approach is already around four million operations, while anything involving exploring many pairings is far beyond the limit.

The key observation is that only the largest distance inside a pair matters. If two values are far apart, they should not be placed together. Sorting reveals the most restrictive pair immediately: the largest element must be paired with some element from the lower end of the array. The smallest element has the same issue.

The optimal arrangement pairs the smallest remaining value with the largest remaining value, repeatedly. This is not just a convenient construction. It gives the smallest possible maximum pair difference among all ways to split the array into mirrored pairs. If this arrangement fails, no other rearrangement can make the extreme values fit because moving either extreme inward would force another value to take its place and create an equal or larger gap.

After sorting the array as `b`, the only check needed is whether:

`b[n - 1 - i] - b[i] <= d`

for every mirrored index `i`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Sorting and checking mirrored pairs | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. Sorting exposes the most extreme possible pairs, which are the pairs that determine whether the arrangement can exist.
2. Compare the smallest element with the largest element. If their difference is greater than `d`, the answer is immediately `NO`, because these two extremes cannot both be placed into valid mirrored positions.
3. Continue inward by comparing the second smallest with the second largest, then the third smallest with the third largest, until reaching the middle. Every comparison represents one possible mirrored pair in the best arrangement.
4. If all mirrored pairs satisfy the distance limit, output `YES`. The sorted mirrored arrangement itself is a valid construction.

Why it works:

After sorting, consider the largest element. It needs a partner within distance `d`. Pairing it with anything except one of the largest remaining possible values can only make the partner smaller and the difference larger. The same argument applies to the smallest element. Removing those two values leaves the same problem on a smaller array, so repeatedly pairing extremes gives the best possible arrangement. If even this arrangement contains an invalid pair, every other arrangement must also contain an invalid pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, d = map(int, input().split())
        a = list(map(int, input().split()))

        a.sort()

        ok = True
        for i in range(n // 2):
            if a[n - 1 - i] - a[i] > d:
                ok = False
                break

        ans.append("YES" if ok else "NO")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is read using `sys.stdin.readline` because there can be many test cases. The solution sorts each array first, which is the only operation that changes the order.

The loop only checks the first half of the sorted array. Each index `i` is paired with `n - 1 - i`, which is its mirrored position in the sorted version. The middle element of an odd-sized array is ignored because it has no partner.

The comparison uses subtraction between Python integers, so large values up to `10^9` are handled safely. The early exit after finding an invalid pair avoids unnecessary checks, although the asymptotic complexity remains the same.

## Worked Examples

Sample 1:

```
3
1 1
1
2 0
1 2
2 1000
1 2
```

| Test | Sorted array | Checked pairs | Result |
| --- | --- | --- | --- |
| 1 | [1] | No pairs | YES |
| 2 | [1, 2] | 2 - 1 = 1 > 0 | NO |
| 3 | [1, 2] | 2 - 1 = 1 <= 1000 | YES |

The first case confirms that a single value always succeeds. The second case shows why equal values are required when `d` is zero. The third case shows that a large enough limit allows the two values to be mirrored.

Sample 2:

Input:

```
1
6 5
1 5 6 10 11 12
```

| Step | Left index | Right index | Difference | State |
| --- | --- | --- | --- | --- |
| 1 | 0 | 5 | 12 - 1 = 11 | Fails |

The first comparison already fails. Since the smallest and largest values cannot be a valid mirrored pair, no rearrangement can solve the test.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the linear scan of mirrored pairs. |
| Space | O(1) extra | The algorithm only stores the input array and uses a few variables. |

The total number of elements over all test cases is only 2000, so sorting is easily within the allowed limits. The approach also works comfortably for much larger arrays.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert run("""3
1 1
1
2 0
1 2
2 1000
1 2
""") == """YES
NO
YES
""", "samples"

assert run("""1
1 0
42
""") == """YES
""", "single element"

assert run("""1
4 0
7 7 7 8
""") == """NO
""", "all equal except one value"

assert run("""1
5 3
1 3 5 7 9
""") == """NO
""", "middle values cannot repair extremes"

assert run("""1
6 10
1 2 5 8 9 10
""") == """YES
""", "larger valid range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | YES | The center case has no mirrored pair. |
| One different value with `d = 0` | NO | Every pair must be identical. |
| Wide range with small `d` | NO | Extreme values decide impossibility. |
| Enough distance for every extreme pair | YES | Correct acceptance of valid sorted pairing. |

## Edge Cases

For the single-element case:

```
1
1 0
42
```

The sorted array is `[42]`. The loop performs zero iterations because `n // 2` is zero. The algorithm outputs `YES`, matching the fact that there is no pair that can violate the condition.

For the zero-distance case:

```
1
4 0
7 7 7 8
```

After sorting, the array is `[7, 7, 7, 8]`. The first mirrored comparison checks `8 - 7 = 1`, which is greater than zero, so the algorithm stops and prints `NO`. The unmatched `8` cannot be hidden by rearranging because it must belong to some mirrored pair.

For a case where only checking the global minimum and maximum is not enough, the algorithm checks every mirrored layer. For example:

```
1
5 3
1 3 5 7 9
```

The sorted array stays the same. The outer pair gives `9 - 1 = 8`, already too large, so the answer is `NO`. Even if the extremes were valid, the inner comparisons would still be checked, preventing incorrect acceptance from a partial condition.
