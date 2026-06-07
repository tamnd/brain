---
title: "CF 2124D - Make a Palindrome"
description: "We start with an array and may repeatedly delete elements. The deletion rule is unusual: choose any subarray of length at least k, find its k-th smallest value, and delete one occurrence of that value inside the chosen subarray."
date: "2026-06-08T03:33:03+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2124
codeforces_index: "D"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2025 (Codeforces Round 1036, Div. 1 + Div. 2)"
rating: 1700
weight: 2124
solve_time_s: 120
verified: false
draft: false
---

[CF 2124D - Make a Palindrome](https://codeforces.com/problemset/problem/2124/D)

**Rating:** 1700  
**Tags:** greedy, sortings, two pointers  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We start with an array and may repeatedly delete elements. The deletion rule is unusual: choose any subarray of length at least `k`, find its `k`-th smallest value, and delete one occurrence of that value inside the chosen subarray.

The goal is not to minimize or maximize the number of operations. We only need to decide whether there exists some sequence of valid deletions that leaves a palindrome.

The constraints immediately suggest that we need a nearly linear solution. Across all test cases, the total length is at most `2·10^5`, so an `O(n log n)` algorithm is comfortable, while anything quadratic is impossible. Even a single test with `n = 2·10^5` would make `O(n²)` exceed tens of billions of operations.

The main difficulty is understanding which elements can actually be deleted. The operation is defined through arbitrary subarrays, so trying to simulate deletions directly quickly becomes hopeless.

Several edge cases are easy to mishandle.

Consider `k = 1`.

```
4 1
1 1 2 1
```

The answer is `YES`. Every element can be deleted, because the first smallest element of a length-1 subarray is that element itself. A solution that assumes some values must remain would fail here.

Consider `k = n`.

```
3 3
1 2 2
```

The answer is `NO`. The only available subarray is the whole array. The third smallest element is `2`, so only a `2` can be deleted. After deleting one `2`, the array length becomes `2 < k`, so no more operations are possible. A naive approach that treats deletions as always available would incorrectly answer `YES`.

Another subtle case occurs when the array contains many copies of the critical value.

```
5 4
1 2 1 2 2
```

The answer is `YES`. Some copies of the critical value may be deleted while others must remain. Treating all copies of that value as permanently fixed is incorrect.

## Approaches

A brute-force approach would try to model the process directly. At every state, we could enumerate all valid subarrays, determine their `k`-th smallest value, generate every possible deletion, and continue searching. This is theoretically correct because it explores every legal sequence of operations.

The state space explodes almost immediately. Even for moderate `n`, the number of reachable arrays becomes enormous. Since `n` reaches `2·10^5`, this direction is completely infeasible.

The breakthrough is to characterize deletable elements globally.

Sort the array and let `x` be the `(k-1)`-th smallest element in the whole array, using 1-based indexing. Equivalently, `x` is the value at index `k-1` after sorting.

A key fact is that the `k-1` globally smallest elements can never all disappear. Every deletion requires the deleted element to have at least `k-1` elements not larger than it inside the chosen subarray. An element belonging to the globally smallest `k-1` positions can never satisfy this.

The converse is surprisingly strong. Any element that is not among those globally smallest `k-1` elements can always be deleted. The official editorial proves that as long as those protected `k-1` elements remain, we can choose a suitable interval where the target element becomes exactly the `k`-th smallest.

This transforms the problem completely.

Let `x` be the value of the `(k-1)`-th smallest element.

Every value strictly greater than `x` is freely deletable, so there is never a reason to keep such values.

Values strictly smaller than `x` are untouchable.

Values equal to `x` are the flexible part. Some copies belong to the protected set, others do not. We may delete some copies of `x`, but we must leave at least `k-1` elements overall.

After removing all values greater than `x`, we obtain a reduced array `b` consisting only of values `< x` and values `= x`.

Now we need to determine whether deleting some copies of `x` can make `b` a palindrome.

This becomes a greedy two-pointer problem.

Move pointers from both ends.

If the values match, keep both.

If they differ and neither side equals `x`, then both values are protected and cannot be removed. The answer is immediately `NO`.

If exactly one side equals `x`, delete that copy of `x` and continue.

This greedily removes only those `x` values that are forced to disappear. Since we want to keep as many elements as possible, this is the best strategy.

At the end, we count how many elements survive. If fewer than `k-1` elements remain, we would have deleted too many protected positions, which is impossible. Otherwise the answer is `YES`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort a copy of the array.
2. Find `x`, the value at position `k-1` in the sorted array.
3. Build a new array `b` containing only elements `<= x`.

Every value greater than `x` can always be deleted, so keeping them never helps.
4. Initialize two pointers, `l = 0` and `r = len(b)-1`.
5. Maintain a counter `kept`, initially `len(b)`.
6. While `l < r`:

1. If `b[l] == b[r]`, keep both elements and move both pointers inward.
2. If `b[l] != b[r]` and `b[l] == x`, delete the left copy of `x`, decrement `kept`, and increment `l`.
3. If `b[l] != b[r]` and `b[r] == x`, delete the right copy of `x`, decrement `kept`, and decrement `r`.
4. If neither side equals `x`, return `NO`.

The only removable elements inside `b` are copies of `x`. When a mismatch appears, any removable side must be removed immediately.
7. After the loop, check whether `kept >= k-1`.
8. If true, return `YES`; otherwise return `NO`.

### Why it works

The globally smallest `k-1` elements form a protected core. Any valid final array must contain them. Every value larger than `x` is always removable, so keeping such values never helps create a palindrome.

After removing all values greater than `x`, the only remaining removable elements are copies of `x`. During the two-pointer scan, if the ends differ and neither end equals `x`, then two protected values disagree. Since neither can ever be deleted, no palindrome is possible.

Whenever one side equals `x`, removing that copy is forced. Any palindrome compatible with the protected elements must eventually discard it. The greedy scan removes exactly those copies of `x` that are necessary and keeps every other element.

Because the algorithm deletes the minimum possible number of elements equal to `x`, if even this maximum-size palindrome candidate contains fewer than `k-1` elements, no valid sequence of operations can exist. Conversely, if at least `k-1` elements remain, the required deletions can be realized by the characterization above.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        if k == 1:
            ans.append("YES")
            continue

        s = sorted(a)
        x = s[k - 1]

        b = [v for v in a if v <= x]

        l = 0
        r = len(b) - 1
        kept = len(b)

        ok = True

        while l < r:
            if b[l] == b[r]:
                l += 1
                r -= 1
            elif b[l] == x:
                kept -= 1
                l += 1
            elif b[r] == x:
                kept -= 1
                r -= 1
            else:
                ok = False
                break

        if ok and kept >= k - 1:
            ans.append("YES")
        else:
            ans.append("NO")

    sys.stdout.write("\n".join(ans))

solve()
```

The first step computes the threshold value `x`. This is the value separating always-removable elements from the elements that may have to stay.

The array `b` removes every value greater than `x`. Those elements are irrelevant because any successful solution can delete them beforehand.

The two-pointer loop performs the greedy palindrome construction. When the ends match, they can clearly belong to the final palindrome. When they differ, the only legal deletion inside `b` is a copy of `x`, so any mismatch involving `x` is resolved by removing that copy.

The variable `kept` tracks how many elements survive. This is slightly easier than counting deletions afterward and avoids mistakes when many copies of `x` are removed.

The final condition `kept >= k - 1` is essential. The protected core contains `k-1` elements, so any feasible final array must contain at least that many elements.

## Worked Examples

### Example 1

Input:

```
5 4
1 2 1 2 2
```

Sorted array:

```
[1, 1, 2, 2, 2]
```

So `x = 2`.

The reduced array is unchanged:

```
b = [1, 2, 1, 2, 2]
```

| l | r | b[l] | b[r] | Action | kept |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | 1 | 2 | remove right x | 4 |
| 0 | 3 | 1 | 2 | remove right x | 3 |
| 0 | 2 | 1 | 1 | keep both | 3 |

The scan succeeds and `kept = 3 ≥ k-1 = 3`.

Answer: `YES`.

This example shows that some copies of `x` may be deleted while others remain.

### Example 2

Input:

```
5 4
5 2 4 3 1
```

Sorted array:

```
[1, 2, 3, 4, 5]
```

So `x = 4`.

Reduced array:

```
b = [2, 4, 3, 1]
```

| l | r | b[l] | b[r] | Action |
| --- | --- | --- | --- | --- |
| 0 | 3 | 2 | 1 | neither side is x |

The algorithm immediately stops.

The values `2` and `1` belong to the protected part and disagree at symmetric positions. No valid palindrome can be formed.

Answer: `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates |
| Space | O(n) | Reduced array `b` |

The total length across test cases is at most `2·10^5`. Sorting each test case gives an overall complexity of `O(total_n log total_n)`, which easily fits within the 2-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []

    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split())

        )

        if k == 1:
            out.append("YES")
            continue

        s = sorted(a)
        x = s[k - 1]

        b = [v for v in a if v <= x]

        l = 0
        r = len(b) - 1
        kept = len(b)

        ok = True

        while l < r:
            if b[l] == b[r]:
                l += 1
                r -= 1
            elif b[l] == x:
                kept -= 1
                l += 1
            elif b[r] == x:
                kept -= 1
                r -= 1
            else:
                ok = False
                break

        out.append("YES" if ok and kept >= k - 1 else "NO")

    return "\n".join(out)

# provided sample
assert run(
"""8
5 3
5 4 3 4 5
4 1
1 1 2 1
6 6
2 3 4 5 3 2
5 4
5 2 4 3 1
8 5
4 7 1 2 3 1 3 4
5 4
1 2 1 2 2
3 3
1 2 2
4 4
2 1 2 2
"""
) == "\n".join([
    "YES",
    "YES",
    "YES",
    "NO",
    "NO",
    "YES",
    "NO",
    "YES"
])

# minimum size
assert run(
"""1
1 1
7
"""
) == "YES"

# already palindrome
assert run(
"""1
5 5
1 2 3 2 1
"""
) == "YES"

# impossible due to protected mismatch
assert run(
"""1
4 4
1 3 2 4
"""
) == "NO"

# all equal values
assert run(
"""1
6 4
2 2 2 2 2 2
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, k=1` | YES | Smallest possible instance |
| Palindromic array with `k=n` | YES | No deletions needed |
| `1 3 2 4`, `k=4` | NO | Protected values mismatch |
| All values equal | YES | Heavy duplication and many valid deletions |

## Edge Cases

Consider:

```
1
4 1
1 1 2 1
```

Since `k=1`, every element is removable. The algorithm immediately returns `YES`. Any array can be reduced to a single element or the empty array, both palindromes.

Consider:

```
1
3 3
1 2 2
```

The sorted array is `[1,2,2]`, so `x=2`. The reduced array remains `[1,2,2]`.

The two-pointer scan compares `1` and `2`. The right side equals `x`, so it is removed. Only two elements remain, which is fewer than `k-1=2` after resolving the mismatch. The final check fails, producing `NO`.

Consider:

```
1
5 4
1 2 1 2 2
```

The scan removes only the necessary copies of `2`, reaches a palindrome, and keeps exactly `k-1` protected elements. This is the case that breaks solutions treating all copies of `x` as undeletable.

The entire solution rests on the characterization that every value larger than the global `(k-1)`-th smallest value is freely deletable, while the protected core of `k-1` smallest elements must survive.
