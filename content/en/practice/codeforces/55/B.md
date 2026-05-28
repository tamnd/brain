---
title: "CF 55B - Smallest number"
description: "We start with four integers on the board. We also know the exact sequence of three operations that must be applied, where each operation is either addition or multiplication."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 55
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 51"
rating: 1600
weight: 55
solve_time_s: 107
verified: true
draft: false
---

[CF 55B - Smallest number](https://codeforces.com/problemset/problem/55/B)

**Rating:** 1600  
**Tags:** brute force  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with four integers on the board. We also know the exact sequence of three operations that must be applied, where each operation is either addition or multiplication. At every step we may pick any two currently available numbers, apply the required operation to them, and place the result back onto the board. After three operations only one number remains.

The task is to find the minimum possible final value.

The tricky part is that the order of operations is fixed, but the choice of which two numbers participate in each operation is completely flexible. Different pairings can produce very different results.

The constraints are extremely small. There are only four numbers, and exactly three operations. Even if we try every possible pairing at every step, the total number of states stays tiny. A brute-force search is completely practical within the time limit.

The numbers are at most 1000, so intermediate products fit comfortably inside 64-bit integers. The largest possible value appears when all numbers are 1000 and all operations are multiplication:

$1000^4 = 10^{12}$

This is well within Python's integer range.

There are several edge cases that can silently break an incorrect implementation.

If multiple equal values exist, we still must treat them as separate positions. Consider:

```
1 1 2 2
+ * +
```

Choosing the first `1` and the second `1` is different from choosing a `1` and a `2`. A careless implementation using sets would lose valid states.

The operation order cannot be rearranged. For example:

```
1 2 3 4
+ * *
```

We must apply `+` first. We are not allowed to multiply before adding, even if that would give a smaller answer.

At each step we may choose any pair, not only adjacent elements. For example:

```
1 10 1 10
* + +
```

The best first move is multiplying the two `1`s to keep the result small. Restricting the search to neighboring elements would miss the optimal answer.

Another subtle point is that addition and multiplication are not interchangeable when zero is present. Consider:

```
0 5 6 7
* + +
```

The optimal move is multiplying `0` with `7` immediately to produce `0`, which keeps the total small later. Greedy strategies based only on current smallest values can fail.

## Approaches

The most direct solution is brute force. At every step we try every possible pair among the currently available numbers. For each pair we apply the required operation, build the next state, and continue recursively.

Initially there are 4 numbers, so there are:

$\binom{4}{2}=6$

possible choices.

After one operation there are 3 numbers left, giving:

$\binom{3}{2}=3$

choices.

Finally there are 2 numbers left, so only 1 choice remains.

The total number of possible execution paths is:

$6 \times 3 \times 1 = 18$

That is tiny. Even a recursive depth-first search exploring every possibility runs instantly.

A naive brute-force implementation could generate all possible parenthesizations and permutations separately, but that quickly becomes messy and duplicates states. The cleaner observation is that the game itself already defines the state transition naturally. At each step we only need the current multiset of numbers and the index of the next operation.

This leads to a compact recursive search:

1. Pick two indices.
2. Apply the current operation.
3. Recurse on the smaller list.
4. Track the minimum final value.

Because the search tree has only 18 leaves, no pruning or dynamic programming is necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with explicit enumeration | O(4! × parenthesizations) | O(1) | Accepted |
| Recursive state search | O(18) | O(3) recursion depth | Accepted |

## Algorithm Walkthrough

1. Read the four initial integers and the three operations.
2. Define a recursive function `dfs(arr, step)` where `arr` is the current list of remaining numbers and `step` tells us which operation must be applied next.
3. If `arr` contains only one number, return it because all operations are finished.
4. Otherwise, try every pair of indices `(i, j)` with `i < j`.
5. Apply the operation `ops[step]` to `arr[i]` and `arr[j]`.

If the operation is `+`, compute their sum.

If the operation is `*`, compute their product.
6. Build the next array by removing the chosen pair and inserting the new result.

The remaining numbers keep their values unchanged. The order does not matter logically, but keeping a consistent construction simplifies the implementation.
7. Recursively compute the smallest possible result from this next state.
8. Take the minimum over all pair choices.
9. Print the final answer returned by the recursive search.

### Why it works

At every step the algorithm explores every legal move allowed by the problem statement. Any valid sequence of operations corresponds to exactly one path in the recursion tree. Since the recursion checks all such paths and returns the minimum final value among them, it cannot miss the optimal answer.

The recursion depth is exactly three because one operation is consumed at each level. Eventually only one number remains, which is the final result produced by that particular sequence of choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

nums = list(map(int, input().split()))
ops = input().split()

def dfs(arr, step):
    if len(arr) == 1:
        return arr[0]

    best = float('inf')

    n = len(arr)

    for i in range(n):
        for j in range(i + 1, n):

            if ops[step] == '+':
                val = arr[i] + arr[j]
            else:
                val = arr[i] * arr[j]

            nxt = []

            for k in range(n):
                if k != i and k != j:
                    nxt.append(arr[k])

            nxt.append(val)

            best = min(best, dfs(nxt, step + 1))

    return best

print(dfs(nums, 0))
```

The recursive function directly mirrors the problem process. The current array represents the numbers still written on the board, while `step` indicates which operation must be used next.

The base case appears when only one number remains. At that moment the whole sequence of operations has already been applied, so the remaining value is the result for that branch.

The nested loops enumerate every unordered pair. Using `i < j` avoids duplicate work because choosing `(a, b)` is identical to choosing `(b, a)` for both addition and multiplication.

The next state is constructed carefully. We copy every number except the two chosen ones, then append the newly computed value. This preserves duplicate numbers correctly. Using sets or removing by value would be dangerous because equal numbers may appear multiple times.

Python integers automatically handle large values, so overflow is not a concern here. In languages with fixed-width integers, 64-bit types are sufficient because the maximum possible value is $10^{12}$.

## Worked Examples

### Example 1

Input:

```
1 1 1 1
+ + *
```

Trace of the optimal path:

| Step | Current numbers | Operation | Chosen pair | Result |
| --- | --- | --- | --- | --- |
| 0 | [1, 1, 1, 1] | + | 1, 1 | [1, 1, 2] |
| 1 | [1, 1, 2] | + | 1, 1 | [2, 2] |
| 2 | [2, 2] | * | 2, 2 | [4] |

This path gives 4, but it is not optimal.

Another path:

| Step | Current numbers | Operation | Chosen pair | Result |
| --- | --- | --- | --- | --- |
| 0 | [1, 1, 1, 1] | + | 1, 1 | [1, 1, 2] |
| 1 | [1, 1, 2] | + | 1, 2 | [1, 3] |
| 2 | [1, 3] | * | 1, 3 | [3] |

The minimum achievable value is 3.

This example shows why trying all pairings matters. Even though the operations are fixed, different intermediate groupings change the final multiplication dramatically.

### Example 2

Input:

```
0 5 6 7
* + +
```

Trace of the optimal path:

| Step | Current numbers | Operation | Chosen pair | Result |
| --- | --- | --- | --- | --- |
| 0 | [0, 5, 6, 7] | * | 0, 7 | [5, 6, 0] |
| 1 | [5, 6, 0] | + | 0, 5 | [6, 5] |
| 2 | [6, 5] | + | 6, 5 | [11] |

Final answer: 11.

If we instead multiply `6 * 7` first, we get:

| Step | Current numbers | Operation | Chosen pair | Result |
| --- | --- | --- | --- | --- |
| 0 | [0, 5, 6, 7] | * | 6, 7 | [0, 5, 42] |
| 1 | [0, 5, 42] | + | 0, 5 | [42, 5] |
| 2 | [42, 5] | + | 42, 5 | [47] |

This demonstrates why greedy local decisions are unreliable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(18) | There are 6 choices at the first step, 3 at the second, and 1 at the third |
| Space | O(3) | Recursion depth never exceeds 3 |

The search space is tiny, so the program runs essentially instantly. Memory usage is also negligible because only a few short arrays exist simultaneously.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    nums = list(map(int, input().split()))
    ops = input().split()

    def dfs(arr, step):
        if len(arr) == 1:
            return arr[0]

        best = float('inf')
        n = len(arr)

        for i in range(n):
            for j in range(i + 1, n):

                if ops[step] == '+':
                    val = arr[i] + arr[j]
                else:
                    val = arr[i] * arr[j]

                nxt = []

                for k in range(n):
                    if k != i and k != j:
                        nxt.append(arr[k])

                nxt.append(val)

                best = min(best, dfs(nxt, step + 1))

        return best

    print(dfs(nums, 0))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
assert run("1 1 1 1\n+ + *\n") == "3", "sample 1"

# all zeros
assert run("0 0 0 0\n* * *\n") == "0", "all zeros"

# large values
assert run("1000 1000 1000 1000\n* * *\n") == "1000000000000", "large multiplication"

# duplicate values
assert run("1 1 2 2\n+ * +\n") == "5", "duplicate handling"

# operation order matters
assert run("1 2 3 4\n+ * *\n") == "14", "fixed operation order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 0 / * * *` | `0` | Correct handling of zeros |
| `1000 1000 1000 1000 / * * *` | `1000000000000` | Large intermediate values |
| `1 1 2 2 / + * +` | `5` | Duplicate numbers handled correctly |
| `1 2 3 4 / + * *` | `14` | Operations must stay in given order |

## Edge Cases

Consider the duplicate-value case:

```
1 1 2 2
+ * +
```

The algorithm treats numbers by index rather than value. During recursion it may choose the two `1`s, or a `1` and a `2`, producing different future states. Because every index pair is explored independently, no valid configuration is lost.

Now examine the fixed-order constraint:

```
1 2 3 4
+ * *
```

The first recursion level always applies `+` because `step = 0`. The algorithm never considers multiplication first. One optimal path is:

```
1 + 2 = 3
3 * 3 = 9
9 * 4 = 36
```

But the minimum path is:

```
1 + 4 = 5
2 * 3 = 6
5 * 6 = 30
```

The recursion guarantees all valid pairings under the required order are checked.

Finally, consider the zero case:

```
0 5 6 7
* + +
```

At the first level, the algorithm explores all six multiplication choices. One branch multiplies `0 * 7`, immediately producing `0`. Later additions keep the total small, leading to the optimal answer 11. Since every possible pair is tested, the beneficial use of zero cannot be missed.
