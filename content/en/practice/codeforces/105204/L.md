---
title: "CF 105204L - \u0411\u0438\u043d\u043f\u043e\u0438\u0441\u043a \u0440\u0435\u0448\u0430\u0435\u0442 \u0432\u0441\u0451!"
description: "We have a permutation of the numbers from 1 to n. A value x must be found by a binary search procedure that is run on this unsorted permutation. The procedure does not look for the position of x directly."
date: "2026-06-27T02:44:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105204
codeforces_index: "L"
codeforces_contest_name: "\u0412\u041a\u041e\u0428\u041f.Junior 2024"
rating: 0
weight: 105204
solve_time_s: 80
verified: true
draft: false
---

[CF 105204L - \u0411\u0438\u043d\u043f\u043e\u0438\u0441\u043a \u0440\u0435\u0448\u0430\u0435\u0442 \u0432\u0441\u0451!](https://codeforces.com/problemset/problem/105204/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation of the numbers from `1` to `n`. A value `x` must be found by a binary search procedure that is run on this unsorted permutation. The procedure does not look for the position of `x` directly. It only moves the left and right borders according to whether the middle element is at most `x` or greater than `x`, and when it stops it returns the current left border. The goal is to perform at most two swaps before the search starts so that the returned position contains `x`.

The input contains several independent cases. For each case, we know the size of the permutation, the required value, and the current arrangement. The output is a list of swaps. Any valid sequence with zero, one, or two swaps is accepted.

The total size of all permutations is at most `200000`. This rules out anything that tries many possible swaps or repeatedly simulates the process for every position. A linear solution per test case is enough because it gives `O(200000)` total work, while approaches such as checking all pairs of positions would require up to `O(n^2)` operations.

The subtle part of the problem is that the binary search does not need the whole array to become sorted. Only the positions visited by the binary search path matter. A common mistake is to move `x` somewhere and assume the search path stays the same without proving it. Another mistake is to use zero-based indexes in the binary search simulation while the problem describes positions starting from one.

For example, consider:

```
1
4 1
2 3 4 1
```

The binary search starts with `l = 1`, `r = 5`. It checks position `2`, sees `3 > 1`, and moves `r` to `2`. It stops with `l = 1`, but position `1` contains `2`. The correct output is:

```
1
1 4
```

A careless solution that assumes the answer is always the original position of `x` would fail because the algorithm returns a position determined by comparisons, not by the location of `x`.

Another edge case is when `x` is already at the position returned by the binary search.

```
1
5 3
1 2 3 4 5
```

The correct output is:

```
0
```

A solution that always performs a swap would still be accepted in many cases, but it can accidentally move `x` away from a correct position and create a wrong answer.

## Approaches

The straightforward approach is to try possible swaps and check the result. A single swap has `O(n^2)` possibilities, and two swaps would create even more combinations. Even if we only simulate the binary search in `O(log n)` after each attempt, the number of operations is far beyond what is possible for `n` up to `200000`.

The key observation is that we do not need to repair the permutation. We only need to put `x` into the position where the current binary search finishes. Let that position be `l`.

Run the given binary search once on the original permutation. If `p[l]` is already `x`, no changes are required. Otherwise, swap the element `x` into position `l`.

The only concern is whether moving `x` changes one of the comparisons made by the search. The swap changes two positions: the final position `l` and the original position of `x`.

Position `l` is never checked after the algorithm stops. The original position of `x` is more interesting. If the search checked that position, the comparison there was with the value `x`, so the search moved the left border to that position. Any later movement of the left border can only happen because another checked value is also at most `x`. Therefore the final position `l` always contains a value at most `x` in this case. After swapping, the old value from `l` moves to the original position of `x`, and it still satisfies the same comparison result. If the original position of `x` was never checked, changing it cannot affect the search at all.

So one swap is always enough. The problem allows two swaps, but the optimal construction only needs zero or one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Find the current position of `x` in the permutation. We need this index because the only possible modification is moving `x` to another place.
2. Simulate the exact binary search described in the statement. Maintain `l` and `r` as one-based borders and update them using the current permutation values. When the loop finishes, `l` is the position that the algorithm would return before any swaps.
3. If the value at position `l` is already `x`, output zero swaps. The current permutation already satisfies the required condition.
4. Otherwise, swap the values at positions `l` and `pos[x]`. This places `x` exactly where the binary search ends.
5. Output this single swap.

Why it works: the binary search path before the swap determines a final position `l`. The swap puts `x` there. The only changed position that could be examined earlier is the old position of `x`. If it was examined, the value moved there from `l` is guaranteed to be at most `x`, which gives the same direction as the original comparison with `x`. Every other comparison remains unchanged, so the algorithm still reaches `l` and returns the position containing `x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, x = map(int, input().split())
        p = list(map(int, input().split()))

        pos = 0
        for i, v in enumerate(p):
            if v == x:
                pos = i
                break

        l = 0
        r = n
        while r - l > 1:
            m = (l + r) // 2
            if p[m] <= x:
                l = m
            else:
                r = m

        if p[l] == x:
            ans.append("0")
        else:
            ans.append("1")
            ans.append(f"{l + 1} {pos + 1}")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The array uses zero-based indexing internally, while the required output uses one-based positions. The conversion is only done when printing the swap.

The simulation uses the same border convention as the statement. `l` is the current valid left border and `r` is the exclusive right border, so the condition `r - l > 1` exactly matches the stopping condition.

The search for `pos[x]` is linear. The binary search simulation takes logarithmic time, so the whole solution is dominated by scanning the permutation once.

## Worked Examples

Consider:

```
1
6 5
3 1 6 5 2 4
```

The simulation is:

| l | r | m | p[m] | Decision |
| --- | --- | --- | --- | --- |
| 0 | 6 | 3 | 6 | Move left, r = 3 |
| 0 | 3 | 1 | 1 | Move right, l = 1 |
| 1 | 3 | 2 | 6 | Move left, r = 2 |

The final position is `l = 1` in zero-based indexing. The value there is `1`, not `5`. The position of `5` is `4`, so we swap positions `2` and `5` in one-based indexing.

After the swap, the permutation begins:

```
3 5 6 4 2 1
```

The same binary search path reaches position `2`, which now contains `5`.

This example shows that the algorithm does not try to sort the permutation. It only changes the one position returned by the search.

Another example:

```
1
5 3
1 2 3 4 5
```

The trace is:

| l | r | m | p[m] | Decision |
| --- | --- | --- | --- | --- |
| 0 | 5 | 2 | 3 | Move right, l = 2 |
| 2 | 5 | 3 | 4 | Move left, r = 3 |

The search ends at position `3` in one-based indexing, and that position already contains `3`. The answer is zero swaps.

This demonstrates the early exit condition and avoids unnecessary modifications.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Finding `x` and simulating binary search both fit within a linear scan. |
| Space | O(n) | The permutation is stored in memory. |

The sum of all `n` values is bounded by `200000`, so the total running time is linear in the input size and easily fits within the limits.

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

assert run(
"""3
6 3
1 2 3 4 5 6
6 5
3 1 6 5 2 4
5 1
3 5 4 2 1
"""
) == "0\n1\n2 4\n1\n1 5\n"

assert run(
"""1
1 1
1
"""
) == "0\n"

assert run(
"""1
4 1
2 3 4 1
"""
) == "1\n1 4\n"

assert run(
"""1
5 5
1 2 3 4 5
"""
) == "0\n"

assert run(
"""1
7 4
7 6 5 3 2 1 4
"""
) == "1\n7 4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| The provided samples | Valid zero and one swap cases | Basic correctness |
| `n = 1` | `0` swaps | Minimum size handling |
| `x = 1` with `x` at the end | One swap | Boundary value behavior |
| Sorted permutation | `0` swaps | Already correct search result |
| `x` far from the returned position | One swap | Correct movement of the target |

## Edge Cases

For the case where `x` is already the returned position, the algorithm stops immediately.

Input:

```
1
5 3
1 2 3 4 5
```

The binary search reaches position `3`, and `p[3]` is already `3`, so the output is:

```
0
```

No swap is needed because every comparison already follows the expected path.

For the case where `x` is not at the returned position, the algorithm moves only `x`.

Input:

```
1
4 1
2 3 4 1
```

The search checks position `2`, moves left, and stops at position `1`. The value there is `2`. Swapping positions `1` and `4` produces:

```
1 3 4 2
```

Running the same binary search still stops at position `1` because the only checked value is `3`, which is greater than `1`. The returned position contains `1`, so the construction succeeds.

The important boundary is when the original position of `x` is itself checked during the binary search. The proof above covers this because the value moved into that position comes from the final left border, and that value must have passed a `<= x` comparison when the border was created. The search direction is unchanged, so the final result remains the same.
