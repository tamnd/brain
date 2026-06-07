---
title: "CF 489A - SwapSort"
description: "We are given an array of integers and must transform it into non-decreasing order by performing swaps of array positions. The interesting part is that we do not need the minimum number of swaps. Any valid sequence containing at most n swaps is accepted."
date: "2026-06-07T17:35:50+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 489
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 277.5 (Div. 2)"
rating: 1200
weight: 489
solve_time_s: 154
verified: false
draft: false
---

[CF 489A - SwapSort](https://codeforces.com/problemset/problem/489/A)

**Rating:** 1200  
**Tags:** greedy, implementation, sortings  
**Solve time:** 2m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and must transform it into non-decreasing order by performing swaps of array positions. The interesting part is that we do not need the minimum number of swaps. Any valid sequence containing at most `n` swaps is accepted.

The output consists of the swap operations themselves. After applying them in the printed order, the array must become sorted.

The array length is at most 3000. This is small enough that an `O(n²)` solution is perfectly acceptable because `3000² = 9,000,000` operations, which easily fits within the limits. There is no need for sophisticated data structures or `O(n log n)` techniques.

The main challenge comes from duplicate values. If all values were distinct, we could simply map each value to its target position in the sorted array. With duplicates, several positions may contain the same value, so a careless mapping can assign one occurrence to multiple target locations.

Consider:

```
3
2 1 2
```

The sorted array is:

```
1 2 2
```

If we only map the value `2` to "its position in the sorted array", there are two valid positions. Treating them as interchangeable without tracking individual occurrences can produce incorrect swaps.

Another edge case is an already sorted array:

```
4
1 2 3 4
```

The correct answer is:

```
0
```

Some implementations unnecessarily perform swaps even though none are required.

A third case is when all elements are equal:

```
5
7 7 7 7 7
```

Again, the answer should contain zero swaps. Any logic based solely on value comparisons must avoid inventing movements for identical elements.

## Approaches

A brute-force idea is to repeatedly find the smallest element that should appear at each position and swap it into place. For position `i`, we scan the suffix `i...n-1`, find the correct element, and perform one swap if needed.

This approach is correct because after fixing position `i`, that position never changes again. Unfortunately, it requires an `O(n)` scan for each of the `n` positions, resulting in `O(n²)` time.

Interestingly, `O(n²)` is already fast enough here. The real observation is not about improving asymptotic complexity, but about producing at most `n` swaps while handling duplicate values cleanly.

The key idea is to sort a copy of the array and maintain the current position of every element. When position `i` does not already contain its final value, we locate a position holding the value that should be here and swap the two positions.

Each swap permanently fixes one position. Since there are only `n` positions, the total number of swaps is at most `n-1`.

To make locating elements easy, we sort pairs `(value, original_index)`. This gives every occurrence of a duplicated value a unique identity. Then each element knows exactly which final position it belongs to.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store every element together with its original index as `(value, index)`.
2. Sort these pairs by value. After sorting, position `i` of this array represents the element that should eventually occupy position `i` in the sorted order.
3. Create an array `pos` where `pos[original_index]` stores the current position of that element in the working array.
4. Create another array `cur` where `cur[position]` stores which original element currently occupies that position.
5. Process positions from left to right.
6. At position `i`, check whether the correct element is already there. The correct element is the one whose original index appears in the sorted pair list at position `i`.
7. If the correct element is already at position `i`, continue.
8. Otherwise, find its current position using `pos`.
9. Swap the two positions in `cur`, update their entries in `pos`, and record the swap.
10. Continue until every position contains its designated element.

Every swap places the correct element into its final position. That position never changes again.

### Why it works

The sorted list of `(value, original_index)` pairs assigns every occurrence of every value a unique destination. Even duplicates become distinguishable because their original indices differ.

At step `i`, if the correct element is not already present, we move exactly that element into position `i`. After the swap, position `i` contains the element designated for it by the sorted ordering.

Since later operations only affect positions greater than or equal to `i+1`, position `i` remains correct forever. Repeating this argument for every position eventually produces the fully sorted array.

Because each swap fixes at least one new position, the number of swaps never exceeds `n-1`, satisfying the problem requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    sorted_pairs = sorted((a[i], i) for i in range(n))

    cur = list(range(n))
    pos = list(range(n))

    swaps = []

    for i in range(n):
        target_id = sorted_pairs[i][1]

        if cur[i] == target_id:
            continue

        j = pos[target_id]

        swaps.append((i, j))

        x = cur[i]
        y = cur[j]

        cur[i], cur[j] = cur[j], cur[i]
        pos[x], pos[y] = pos[y], pos[x]

    print(len(swaps))
    for i, j in swaps:
        print(i, j)

solve()
```

The solution never directly rearranges the values. Instead, it rearranges identifiers representing the original positions of elements.

The array `sorted_pairs` determines where each original element belongs in the final sorted order. The array `cur` tells us which original element currently occupies each position, while `pos` provides the inverse mapping.

When a swap occurs, both structures must be updated consistently. Forgetting to update either `cur` or `pos` is the most common implementation mistake and immediately breaks future lookups.

The algorithm fixes positions from left to right. Once a position is fixed, it is never touched again.

## Worked Examples

### Example 1

Input:

```
5
5 2 5 1 4
```

Sorted order of pairs:

```
(1,3) (2,1) (4,4) (5,0) (5,2)
```

| Step | i | Required original index | Current position | Swap | cur after swap |
| --- | --- | --- | --- | --- | --- |
| Start | - | - | - | - | [0,1,2,3,4] |
| 1 | 0 | 3 | 3 | (0,3) | [3,1,2,0,4] |
| 2 | 1 | 1 | 1 | none | [3,1,2,0,4] |
| 3 | 2 | 4 | 4 | (2,4) | [3,1,4,0,2] |
| 4 | 3 | 0 | 3 | none | [3,1,4,0,2] |
| 5 | 4 | 2 | 4 | none | [3,1,4,0,2] |

Output:

```
2
0 3
2 4
```

This example shows how each swap permanently fixes one position. After the first swap, position 0 already contains the smallest element and never changes again.

### Example 2

Input:

```
4
4 3 2 1
```

Sorted order of pairs:

```
(1,3) (2,2) (3,1) (4,0)
```

| Step | i | Required original index | Current position | Swap | cur after swap |
| --- | --- | --- | --- | --- | --- |
| Start | - | - | - | - | [0,1,2,3] |
| 1 | 0 | 3 | 3 | (0,3) | [3,1,2,0] |
| 2 | 1 | 2 | 2 | (1,2) | [3,2,1,0] |
| 3 | 2 | 1 | 2 | none | [3,2,1,0] |
| 4 | 3 | 0 | 3 | none | [3,2,1,0] |

Output:

```
2
0 3
1 2
```

This trace demonstrates that one swap can fix multiple elements simultaneously, which is why the total number of swaps stays below `n`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Sorting costs O(n log n), the fixing loop is O(n), and all operations are constant time. The accepted editorial classification is O(n²) or better. |
| Space | O(n) | Arrays `cur`, `pos`, and the swap list store linear information. |

With `n ≤ 3000`, both time and memory usage are comfortably within the limits. Even several million operations execute quickly in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    def solve():
        input = sys.stdin.readline

        n = int(input())
        a = list(map(int, input().split()))

        sorted_pairs = sorted((a[i], i) for i in range(n))

        cur = list(range(n))
        pos = list(range(n))
        swaps = []

        for i in range(n):
            target_id = sorted_pairs[i][1]

            if cur[i] == target_id:
                continue

            j = pos[target_id]

            swaps.append((i, j))

            x = cur[i]
            y = cur[j]

            cur[i], cur[j] = cur[j], cur[i]
            pos[x], pos[y] = pos[y], pos[x]

        print(len(swaps))
        for x, y in swaps:
            print(x, y)

    solve()

    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample
assert run("5\n5 2 5 1 4\n").splitlines()[0] == "2"

# minimum size
assert run("1\n42\n") == "0"

# already sorted
assert run("4\n1 2 3 4\n") == "0"

# all equal
assert run("5\n7 7 7 7 7\n") == "0"

# duplicates
res = run("3\n2 1 2\n")
assert int(res.splitlines()[0]) <= 3

# reverse order
res = run("4\n4 3 2 1\n")
assert int(res.splitlines()[0]) == 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 42` | `0` swaps | Minimum array size |
| `1 2 3 4` | `0` swaps | Already sorted input |
| `7 7 7 7 7` | `0` swaps | Duplicate handling |
| `2 1 2` | Valid answer | Correct treatment of repeated values |
| `4 3 2 1` | `2` swaps | Typical permutation cycle |

## Edge Cases

Consider the duplicate-value case:

```
3
2 1 2
```

The sorted pair list becomes:

```
(1,1) (2,0) (2,2)
```

The two occurrences of value `2` remain distinguishable because their original indices are different. The algorithm assigns one copy to position 1 and the other to position 2. No ambiguity exists, so the resulting array is correctly sorted.

Consider an already sorted array:

```
4
1 2 3 4
```

The sorted pair list matches the current arrangement. For every position `i`, `cur[i]` already equals the required original index. No swaps are recorded, and the output is simply:

```
0
```

Consider all elements equal:

```
5
7 7 7 7 7
```

Sorting the `(value, index)` pairs preserves their order because the indices are distinct. Every position already contains its designated element, so again no swaps occur. The algorithm naturally outputs zero operations.

These cases illustrate why assigning each occurrence a unique identity through its original index is the crucial detail that makes the solution correct.
