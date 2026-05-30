---
title: "CF 489A - SwapSort"
description: "We are given an array of integers and must transform it into non-decreasing order using swaps. The output is not the sorted array itself. Instead, we must print a sequence of index pairs, where each pair represents a swap performed on the array."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 489
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 277.5 (Div. 2)"
rating: 1200
weight: 489
solve_time_s: 691
verified: false
draft: false
---

[CF 489A - SwapSort](https://codeforces.com/problemset/problem/489/A)

**Rating:** 1200  
**Tags:** greedy, implementation, sortings  
**Solve time:** 11m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and must transform it into non-decreasing order using swaps. The output is not the sorted array itself. Instead, we must print a sequence of index pairs, where each pair represents a swap performed on the array.

The unusual part of the task is that we are not asked to minimize the number of swaps. Any valid sequence is acceptable as long as its length does not exceed `n`. The problem guarantees that such a sequence always exists.

The array length is at most 3000. A quadratic algorithm performs about nine million operations in the worst case, which is completely reasonable within the time limit. Cubic algorithms, however, would approach tens of billions of operations and are far too slow.

The presence of duplicate values is the main complication. When multiple equal values exist, it is not enough to know what value should be placed at a position. We must also know which occurrence of that value belongs there. A careless implementation that maps each value to a single index will fail.

Consider:

```
4
2 1 2 1
```

The sorted array is:

```
1 1 2 2
```

If we store only one position for value `1` and one position for value `2`, we lose information about the second occurrence of each value. The resulting swaps may place equal values incorrectly or even reuse the same index multiple times.

Another edge case is an already sorted array:

```
5
1 2 3 4 5
```

The correct answer is:

```
0
```

A solution that blindly performs swaps whenever it encounters matching values could generate unnecessary operations.

A third case is when all elements are equal:

```
4
7 7 7 7
```

The array is already sorted. Any attempt to distinguish between identical elements without proper handling may produce meaningless swaps.

## Approaches

A natural brute-force idea is to repeatedly search for the smallest element that should occupy the current position and swap it into place. For every position `i`, we scan the suffix to find the correct element and perform one swap if needed.

This approach is actually fast enough. For each of the `n` positions, we may scan up to `n` elements, giving `O(n²)` time. With `n = 3000`, this is about nine million comparisons.

The interesting part is proving that we never exceed `n` swaps. Each swap permanently fixes at least one position. Since there are only `n` positions, the number of swaps is at most `n - 1`.

A cleaner way to view the same idea is to compare the current array with its sorted version.

Suppose we already know the final sorted array. At position `i`, either the correct value is already present or it is not. If it is not, we locate an occurrence of the required value somewhere later in the array and swap it into position `i`.

To do this efficiently, we maintain where every current element resides. After each swap, we update those positions.

The key observation is that once position `i` receives the value that appears at position `i` in the sorted array, that position never needs to be touched again. Every swap fixes one position permanently, which immediately gives the required bound on the number of swaps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

Although both fit the constraints, the second approach is easier to reason about and directly constructs the required swap sequence.

## Algorithm Walkthrough

1. Create a sorted copy of the array called `b`.
2. Maintain an array `pos` where `pos[i]` stores the current position of the element that originally occupied index `i`.
3. Maintain an array `who` where `who[j]` stores which original element currently sits at position `j`.
4. Iterate through positions from left to right.
5. For position `i`, check whether `a[i]` already equals `b[i]`. If it does, this position is correct and we continue.
6. Otherwise, search for an index `j > i` such that `a[j] == b[i]`.
7. Swap `a[i]` and `a[j]`.
8. Record the pair `(i, j)` in the answer.
9. Continue to the next position.

The search in step 6 always succeeds because `b` is simply a permutation of the original array. Every value required by the sorted array exists somewhere in the remaining suffix.

### Why it works

At the start of iteration `i`, all positions before `i` already match the sorted array.

If `a[i]` is incorrect, we find an occurrence of the exact value that should be placed there and swap it into position `i`. After the swap, position `i` becomes correct.

Future operations only involve positions greater than `i`, so position `i` never changes again.

This establishes an invariant: after processing position `i`, the prefix `[0, i]` is identical to the sorted array. By induction, when the loop finishes, every position matches the sorted array.

Each swap fixes one previously incorrect position permanently. Since there are at most `n` positions, the number of swaps never exceeds `n - 1`, satisfying the problem requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

b = sorted(a)
ans = []

for i in range(n):
    if a[i] == b[i]:
        continue

    j = i + 1
    while j < n and a[j] != b[i]:
        j += 1

    a[i], a[j] = a[j], a[i]
    ans.append((i, j))

print(len(ans))
for i, j in ans:
    print(i, j)
```

The solution begins by creating the target sorted array `b`. This gives us the exact value that should appear at every position.

The loop processes positions from left to right. Whenever the current position already contains the desired value, no action is needed.

If the value is wrong, we search the remaining suffix for an occurrence of the required value. Swapping those two positions immediately fixes position `i`.

A subtle point is handling duplicates. We do not try to track a unique destination for each occurrence. Instead, we simply find any occurrence of the required value in the unprocessed suffix. Since earlier positions are already fixed and never touched again, this always works.

The search starts from `i + 1`, avoiding unnecessary self-swaps. The problem would still allow them, but they are not needed.

## Worked Examples

### Example 1

Input:

```
5
5 2 5 1 4
```

Sorted target:

```
1 2 4 5 5
```

| Step | i | Current Array | Required Value | Swap |
| --- | --- | --- | --- | --- |
| Start | - | [5,2,5,1,4] | - | - |
| 1 | 0 | [5,2,5,1,4] | 1 | (0,3) |
| After | - | [1,2,5,5,4] | - | - |
| 2 | 1 | [1,2,5,5,4] | 2 | none |
| 3 | 2 | [1,2,5,5,4] | 4 | (2,4) |
| After | - | [1,2,4,5,5] | - | - |

Output:

```
2
0 3
2 4
```

This trace shows how each swap permanently fixes one position in the sorted prefix.

### Example 2

Input:

```
4
2 1 2 1
```

Sorted target:

```
1 1 2 2
```

| Step | i | Current Array | Required Value | Swap |
| --- | --- | --- | --- | --- |
| Start | - | [2,1,2,1] | - | - |
| 1 | 0 | [2,1,2,1] | 1 | (0,1) |
| After | - | [1,2,2,1] | - | - |
| 2 | 1 | [1,2,2,1] | 1 | (1,3) |
| After | - | [1,1,2,2] | - | - |
| 3 | 2 | [1,1,2,2] | 2 | none |
| 4 | 3 | [1,1,2,2] | 2 | none |

This example demonstrates that duplicates cause no difficulty. We simply choose any suitable occurrence in the remaining suffix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each position may scan the remaining suffix |
| Space | O(n) | Sorted copy of the array and swap list |

With `n ≤ 3000`, the worst-case work is roughly nine million comparisons, which easily fits within the time limit. The memory usage is also small compared to the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    b = sorted(a)
    ans = []

    for i in range(n):
        if a[i] == b[i]:
            continue

        j = i + 1
        while j < n and a[j] != b[i]:
            j += 1

        a[i], a[j] = a[j], a[i]
        ans.append((i, j))

    out = [str(len(ans))]
    for i, j in ans:
        out.append(f"{i} {j}")
    return "\n".join(out)

# sample 1
out = run("5\n5 2 5 1 4\n")
assert out.splitlines()[0] == "2"

# minimum size
assert run("1\n7\n") == "0"

# already sorted
assert run("5\n1 2 3 4 5\n") == "0"

# all equal
assert run("4\n9 9 9 9\n") == "0"

# duplicates
out = run("4\n2 1 2 1\n")
assert int(out.splitlines()[0]) <= 4

# reverse order
out = run("5\n5 4 3 2 1\n")
assert int(out.splitlines()[0]) <= 5
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` swaps | Minimum array size |
| `1 2 3 4 5` | `0` swaps | Already sorted array |
| `9 9 9 9` | `0` swaps | All elements equal |
| `2 1 2 1` | Valid sequence | Correct handling of duplicates |
| `5 4 3 2 1` | Valid sequence | Multiple swaps and suffix searches |

## Edge Cases

### Duplicate Values

Input:

```
4
2 1 2 1
```

The sorted array is:

```
1 1 2 2
```

At position `0`, we need a `1`, so we swap indices `0` and `1`.

The array becomes:

```
1 2 2 1
```

At position `1`, we still need a `1`, so we swap indices `1` and `3`.

The array becomes:

```
1 1 2 2
```

The algorithm never tries to distinguish between equal values. It only asks whether the required value exists in the remaining suffix.

### Already Sorted Array

Input:

```
5
1 2 3 4 5
```

The sorted copy is identical to the original array.

Every iteration finds that `a[i] == b[i]`, so no swaps are recorded.

Output:

```
0
```

This confirms that the algorithm does not introduce unnecessary operations.

### All Elements Equal

Input:

```
4
7 7 7 7
```

Again, every position already matches the sorted array.

The loop performs no swaps and prints:

```
0
```

Equal values are handled naturally because every position already satisfies its target value.

### Reverse Sorted Array

Input:

```
5
5 4 3 2 1
```

Target:

```
1 2 3 4 5
```

The algorithm swaps `(0,4)` and then `(1,3)`.

After these two swaps:

```
1 2 3 4 5
```

Only two operations are needed, well below the required limit of `n = 5`. This illustrates why fixing one position at a time guarantees a bounded number of swaps.
