---
title: "CF 221A - Little Elephant and Function"
description: "We are given a recursive procedure that operates on a permutation of numbers from 1 to n. The function behaves like this: For f(x), it first recursively processes the first x - 1 elements, then swaps positions x - 1 and x."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 221
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 136 (Div. 2)"
rating: 1000
weight: 221
solve_time_s: 70
verified: true
draft: false
---

[CF 221A - Little Elephant and Function](https://codeforces.com/problemset/problem/221/A)

**Rating:** 1000  
**Tags:** implementation, math  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a recursive procedure that operates on a permutation of numbers from `1` to `n`.

The function behaves like this:

For `f(x)`, it first recursively processes the first `x - 1` elements, then swaps positions `x - 1` and `x`.

If we call `f(n)`, the recursion eventually performs these swaps in order:

- swap positions `(1, 2)`
- swap positions `(2, 3)`
- swap positions `(3, 4)`
- ...
- swap positions `(n - 1, n)`

The task is not to simulate sorting. Instead, we must construct an initial permutation such that after all these swaps are executed, the final array becomes sorted in increasing order.

The constraint `n ≤ 1000` is very small. Even quadratic simulation would fit comfortably inside the limits. The real challenge is recognizing the pattern hidden inside the recursive process.

A common mistake is assuming the answer must somehow resemble a reversed array. For example, with `n = 4`, starting from:

```
4 3 2 1
```

the swaps produce:

```
3 4 2 1
3 2 4 1
3 2 1 4
```

which is not sorted.

Another easy mistake is misunderstanding the order of swaps. The recursion does not repeatedly bubble elements around. Each adjacent pair is swapped exactly once, from left to right.

For `n = 3`, the swaps are:

```
swap(1,2)
swap(2,3)
```

If the initial array is:

```
2 1 3
```

then after the swaps:

```
1 2 3
1 3 2
```

the result is incorrect. A careless implementation that does not trace the actual swap order can easily produce such invalid constructions.

The smallest edge case is `n = 1`. No swaps happen at all, so the only valid answer is:

```
1
```

Any solution relying on shifting elements without handling this separately may accidentally produce an empty array or invalid indexing.

## Approaches

The most direct brute-force idea is to try every permutation of numbers from `1` to `n`, simulate the recursive process, and check whether the final array becomes sorted.

This works because the recursive function is deterministic. Once a starting permutation is fixed, the resulting array after all swaps is uniquely determined.

For each permutation, we perform `n - 1` swaps, so checking one candidate costs `O(n)`. The problem is the number of permutations. There are `n!` possibilities.

Even for `n = 10`, this already becomes:

```
10! = 3,628,800
```

Trying all permutations quickly becomes impossible.

The key observation is that the recursive function performs a very simple transformation. Every element shifts one position to the left, except the first element, which moves to the end.

For example:

```
[a1, a2, a3, a4]
```

after the swaps becomes:

```
[a2, a3, a4, a1]
```

We can verify this directly:

```
swap(1,2): [a2, a1, a3, a4]
swap(2,3): [a2, a3, a1, a4]
swap(3,4): [a2, a3, a4, a1]
```

Now the problem becomes easy.

We want the final array to be:

```
1 2 3 ... n
```

Since the operation rotates the array left by one position, the initial permutation must be the sorted array rotated right by one position:

```
n 1 2 3 ... n-1
```

After the recursive swaps:

```
1 2 3 ... n
```

This construction is immediate and runs in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · n!) | O(n) | Too slow |
| Optimal | O(n) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Construct the permutation beginning with `n`.

This element must move to the last position after all swaps, because the recursive process rotates the array left by one step.
3. Append all integers from `1` to `n - 1` in increasing order.

After the left rotation caused by the swaps, these elements shift into their correct sorted positions.
4. Print the resulting permutation.

### Why it works

The recursive function performs adjacent swaps from left to right exactly once. This sequence transforms:

```
[a1, a2, a3, ..., an]
```

into:

```
[a2, a3, ..., an, a1]
```

which is a left rotation by one position.

If we want the final array to become:

```
[1, 2, 3, ..., n]
```

then the initial array must be the inverse transformation, a right rotation of the sorted array:

```
[n, 1, 2, ..., n-1]
```

Applying the recursive swaps to this permutation produces the sorted order.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

ans = [n] + list(range(1, n))

print(*ans)
```

The implementation directly follows the mathematical observation.

The array starts with `n` because the recursive process moves the first element to the end. All remaining numbers are already in sorted order, so after the left rotation they become:

```
1 2 3 ... n
```

The expression:

```
list(range(1, n))
```

correctly generates numbers from `1` through `n - 1`.

One subtle boundary condition appears when `n = 1`.

In that case:

```
list(range(1, 1))
```

produces an empty list, so the final result becomes:

```
[1]
```

which is exactly correct.

No simulation of swaps is necessary. The recursive behavior is completely captured by the rotation observation.

## Worked Examples

### Example 1

Input:

```
1
```

Constructed permutation:

| Step | Array |
| --- | --- |
| Initial construction | [1] |

No swaps occur because the recursion stops immediately.

Final array:

```
1
```

This example confirms the smallest boundary case works correctly.

### Example 2

Input:

```
4
```

Constructed permutation:

```
4 1 2 3
```

Now trace the recursive swaps.

| Operation | Array State |
| --- | --- |
| Initial | [4, 1, 2, 3] |
| swap(1,2) | [1, 4, 2, 3] |
| swap(2,3) | [1, 2, 4, 3] |
| swap(3,4) | [1, 2, 3, 4] |

The process demonstrates the left-rotation behavior clearly. The first element gradually moves to the end while every other element shifts left by one position.

### Example 3

Input:

```
5
```

Constructed permutation:

```
5 1 2 3 4
```

Trace:

| Operation | Array State |
| --- | --- |
| Initial | [5, 1, 2, 3, 4] |
| swap(1,2) | [1, 5, 2, 3, 4] |
| swap(2,3) | [1, 2, 5, 3, 4] |
| swap(3,4) | [1, 2, 3, 5, 4] |
| swap(4,5) | [1, 2, 3, 4, 5] |

This trace confirms that the construction works for larger arrays as well.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We construct and print one array of size `n` |
| Space | O(n) | The output array stores `n` integers |

With `n ≤ 1000`, linear complexity is trivial for the given limits. The solution easily fits inside both the time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    ans = [n] + list(range(1, n))

    print(*ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("1\n") == "1\n", "sample 1"

# custom cases
assert run("2\n") == "2 1\n", "smallest non-trivial case"

assert run("3\n") == "3 1 2\n", "checks left-rotation logic"

assert run("5\n") == "5 1 2 3 4\n", "general case"

expected = "1000 " + " ".join(str(i) for i in range(1, 1000)) + "\n"
assert run("1000\n") == expected, "maximum size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum size boundary |
| `2` | `2 1` | Single swap behavior |
| `3` | `3 1 2` | Correct rotation construction |
| `5` | `5 1 2 3 4` | General correctness |
| `1000` | `1000 1 2 ... 999` | Maximum constraint handling |

## Edge Cases

### Edge Case 1: `n = 1`

Input:

```
1
```

The algorithm constructs:

```
[1]
```

The recursive function immediately stops because `x = 1`.

Final result:

```
1
```

This case confirms the implementation correctly handles the empty suffix produced by:

```
range(1, 1)
```

### Edge Case 2: Smallest Non-Trivial Case

Input:

```
2
```

Constructed permutation:

```
2 1
```

Execution trace:

| Operation | Array |
| --- | --- |
| Initial | [2, 1] |
| swap(1,2) | [1, 2] |

Final array becomes sorted.

This case verifies the indexing logic for the first adjacent swap.

### Edge Case 3: Verifying Rotation Behavior

Input:

```
4
```

Constructed permutation:

```
4 1 2 3
```

Execution trace:

| Operation | Array |
| --- | --- |
| Initial | [4, 1, 2, 3] |
| swap(1,2) | [1, 4, 2, 3] |
| swap(2,3) | [1, 2, 4, 3] |
| swap(3,4) | [1, 2, 3, 4] |

This demonstrates the core invariant: the recursive process is exactly one left rotation.
