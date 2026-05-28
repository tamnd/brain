---
title: "CF 72C - Extraordinarily Nice Numbers"
description: "The problem gives us the root of a binary tree and asks us to count how many nodes are considered \"good\". A node is good if, along the path from the root to that node, no previous node has a value greater than the current node's value."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "math"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "C"
codeforces_contest_name: "Unknown Language Round 2"
rating: 1200
weight: 72
solve_time_s: 134
verified: true
draft: false
---

[CF 72C - Extraordinarily Nice Numbers](https://codeforces.com/problemset/problem/72/C)

**Rating:** 1200  
**Tags:** *special, math  
**Solve time:** 2m 14s  
**Verified:** yes  

## Solution
## LeetCode 1448 - Count Good Nodes in Binary Tree

## Problem Understanding

The problem gives us the root of a binary tree and asks us to count how many nodes are considered "good". A node is good if, along the path from the root to that node, no previous node has a value greater than the current node's value.

Another way to think about it is this: when we travel from the root down to a node, the node is good if its value is greater than or equal to every value we have seen earlier on that path.

For example, consider the path:

```
3 -> 1 -> 3
```

The last node with value `3` is good because no value before it is greater than `3`. The maximum value seen along the path is also `3`.

The input is a standard binary tree structure where each node contains an integer value and pointers to left and right children. The output is a single integer representing how many nodes satisfy the "good" condition.

The constraints are important here. The tree may contain as many as `10^5` nodes, which means inefficient repeated traversals will become too slow. Any solution worse than linear time risks timing out. Since this is a tree traversal problem, depth-first search naturally fits because every node depends on information from its ancestors.

There are several edge cases worth identifying early.

A tree with only one node should always return `1`, because the root is automatically good.

A strictly decreasing path such as:

```
5 -> 4 -> 3 -> 2
```

contains only one good node, the root, because every later node has a larger ancestor.

A strictly increasing path such as:

```
1 -> 2 -> 3 -> 4
```

contains all good nodes, because each node becomes the new maximum on its path.

Negative values also matter. Since node values may be as small as `-10^4`, the implementation cannot assume positive numbers when tracking the maximum value seen so far.

## Approaches

A brute-force approach would examine every node independently. For each node, we could trace the entire path back to the root and check whether any ancestor has a larger value. If no ancestor exceeds the current value, the node is counted as good.

This works correctly because it directly follows the definition of a good node. The problem is efficiency. In the worst case, the tree becomes a linked list with `10^5` nodes. For every node, we may walk through all previous ancestors, producing `O(n^2)` time complexity. That is too slow for the input size.

The key observation is that a node only cares about one piece of information from its ancestors: the maximum value encountered so far on the current root-to-node path.

If we already know the maximum value along the path to the parent, then checking the current node becomes simple:

```
node is good if node.val >= current_max
```

After processing the node, we update the maximum:

```
new_max = max(current_max, node.val)
```

This transforms the problem into a single depth-first traversal where each node is visited exactly once.

| Approach | Time Complexity | Space Complexity | Notes |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(h) | Re-checks ancestor paths repeatedly |
| Optimal DFS | O(n) | O(h) | Tracks maximum value during traversal |

Here, `h` represents the height of the tree.

## Algorithm Walkthrough

1. Start a depth-first traversal from the root node.
2. Pass along the maximum value seen so far on the current root-to-node path. Initially, this value is the root's value.
3. At each node, compare the node's value with the current maximum.

If the node's value is greater than or equal to the maximum seen so far, then this node is good and should be counted.
4. Update the running maximum for future recursive calls.

The updated maximum becomes:

```
max_so_far = max(max_so_far, node.val)
```
5. Recursively process the left child using the updated maximum.
6. Recursively process the right child using the updated maximum.
7. Return the total number of good nodes found in the current subtree.

### Why it works

The algorithm maintains a simple invariant:

```
max_so_far always equals the maximum node value on the path
from the root to the current node.
```

Because this invariant is true for every recursive call, determining whether the current node is good becomes correct and immediate. Every node is checked exactly once using accurate path information, so the final count is correct.

## Python Solution

```
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from typing import Optional

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node: Optional[TreeNode], max_so_far: int) -> int:
            if not node:
                return 0

            good = 1 if node.val >= max_so_far else 0

            updated_max = max(max_so_far, node.val)

            left_count = dfs(node.left, updated_max)
            right_count = dfs(node.right, updated_max)

            return good + left_count + right_count

        return dfs(root, root.val)
```

The implementation uses a recursive DFS helper function. The helper receives two arguments: the current node and the maximum value encountered on the path from the root.

The base case handles `None` nodes by returning `0`, since empty subtrees contain no good nodes.

For each real node, the code checks whether the node value is at least as large as `max_so_far`. If true, the node contributes `1` to the answer.

The maximum path value is then updated before traversing children. This guarantees that descendants receive accurate ancestor information.

Finally, the recursive calls return counts from the left and right subtrees, which are added together with the current node's contribution.

## Go Solution

```
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func goodNodes(root *TreeNode) int {
    var dfs func(node *TreeNode, maxSoFar int) int

    dfs = func(node *TreeNode, maxSoFar int) int {
        if node == nil {
            return 0
        }

        good := 0
        if node.Val >= maxSoFar {
            good = 1
        }

        updatedMax := max(maxSoFar, node.Val)

        leftCount := dfs(node.Left, updatedMax)
        rightCount := dfs(node.Right, updatedMax)

        return good + leftCount + rightCount
    }

    return dfs(root, root.Val)
}

func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}
```

The Go version follows the same recursive structure as the Python solution. Since Go does not provide a built-in `max` function for integers, a helper function is implemented manually.

Go uses `nil` instead of Python's `None` for missing children. Apart from syntax differences, the traversal logic is identical.

## Worked Examples

### Example 1

Input:

```
root = [3,1,4,3,null,1,5]
```

Tree structure:

```
        3
       / \
      1   4
     /   / \
    3   1   5
```

Traversal trace:

| Current Node | max_so_far | Good Node? | Updated Max | Total Good So Far |
| --- | --- | --- | --- | --- |
| 3 | 3 | Yes | 3 | 1 |
| 1 | 3 | No | 3 | 1 |
| 3 | 3 | Yes | 3 | 2 |
| 4 | 3 | Yes | 4 | 3 |
| 1 | 4 | No | 4 | 3 |
| 5 | 4 | Yes | 5 | 4 |

Final answer:

```
4
```

### Example 2

Input:

```
root = [3,3,null,4,2]
```

Tree structure:

```
      3
     /
    3
   / \
  4   2
```

Traversal trace:

| Current Node | max_so_far | Good Node? | Updated Max | Total Good So Far |
| --- | --- | --- | --- | --- |
| 3 | 3 | Yes | 3 | 1 |
| 3 | 3 | Yes | 3 | 2 |
| 4 | 3 | Yes | 4 | 3 |
| 2 | 3 | No | 3 | 3 |

Final answer:

```
3
```

### Example 3

Input:

```
root = [1]
```

Traversal trace:

| Current Node | max_so_far | Good Node? | Updated Max | Total Good So Far |
| --- | --- | --- | --- | --- |
| 1 | 1 | Yes | 1 | 1 |

Final answer:

```
1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited exactly once |
| Space | O(h) | Recursive call stack stores one frame per tree level |

The algorithm performs a single DFS traversal, so every node contributes constant work exactly once.

The auxiliary space depends on the recursion depth. In a balanced tree, the height is `O(log n)`. In the worst case, a skewed tree behaves like a linked list and the recursion stack grows to `O(n)`.

## Test Cases

```
# Definition for testing
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def goodNodes(self, root):
        def dfs(node, max_so_far):
            if not node:
                return 0

            good = 1 if node.val >= max_so_far else 0
            updated_max = max(max_so_far, node.val)

            return (
                good
                + dfs(node.left, updated_max)
                + dfs(node.right, updated_max)
            )

        return dfs(root, root.val)

sol = Solution()

# Example 1
root1 = TreeNode(
    3,
    TreeNode(1, TreeNode(3)),
    TreeNode(4, TreeNode(1), TreeNode(5))
)
assert sol.goodNodes(root1) == 4  # standard mixed tree

# Example 2
root2 = TreeNode(
    3,
    TreeNode(3, TreeNode(4), TreeNode(2))
)
assert sol.goodNodes(root2) == 3  # one node blocked by larger ancestor

# Example 3
root3 = TreeNode(1)
assert sol.goodNodes(root3) == 1  # single-node tree

# Strictly increasing path
root4 = TreeNode(1,
    TreeNode(2,
        TreeNode(3,
            TreeNode(4)
        )
    )
)
assert sol.goodNodes(root4) == 4  # every node becomes new maximum

# Strictly decreasing path
root5 = TreeNode(5,
    TreeNode(4,
        TreeNode(3,
            TreeNode(2)
        )
    )
)
assert sol.goodNodes(root5) == 1  # only root is good

# Negative values
root6 = TreeNode(
    -1,
    TreeNode(-2),
    TreeNode(0)
)
assert sol.goodNodes(root6) == 2  # handles negative values correctly

# Duplicate values
root7 = TreeNode(
    2,
    TreeNode(2),
    TreeNode(2)
)
assert sol.goodNodes(root7) == 3  # equal values are considered good
```

| Test | Why |
| --- | --- |
| Example 1 | Verifies normal mixed tree behavior |
| Example 2 | Checks ancestor blocking logic |
| Example 3 | Confirms single-node handling |
| Increasing path | Ensures every new maximum counts |
| Decreasing path | Ensures smaller descendants are rejected |
| Negative values | Verifies correct handling of negatives |
| Duplicate values | Confirms equality still counts as good |

## Edge Cases

A single-node tree is the smallest valid input. For example:

```
[1]
```

The root has no ancestors, so it must always be considered good. A buggy implementation might accidentally initialize the maximum incorrectly and reject the root. The solution avoids this by starting DFS with `root.val` as the initial maximum.

A strictly decreasing tree is another important edge case:

```
5 -> 4 -> 3 -> 2
```

Every descendant has a larger ancestor. The algorithm correctly keeps `max_so_far = 5` throughout the traversal, so only the root contributes to the count.

Negative values can also expose implementation mistakes. Consider:

```
[-1, -2, 0]
```

If a solution incorrectly initializes the running maximum to `0`, then node `-1` would wrongly fail the comparison. The implementation instead initializes the maximum using the actual root value, making it safe for all allowed integer ranges.

Equal values are another subtle case:

```
2 -> 2 -> 2
```

The problem only disqualifies nodes when an ancestor is strictly greater. Equal values still count as good. The implementation uses `>=` rather than `>`, which handles this correctly.

## Codeforces 72C - Extraordinarily Nice Numbers

## Problem Understanding

We are given a positive integer `x` and must determine whether the number of even divisors of `x` equals the number of odd divisors of `x`.

A divisor of `x` is any positive integer that divides `x` exactly. For example, the divisors of `12` are:

```
1, 2, 3, 4, 6, 12
```

Among these, the odd divisors are `1` and `3`, while the even divisors are `2, 4, 6, 12`.

The task is simply to print `"yes"` if the counts match, otherwise print `"no"`.

The constraint is extremely small, since `x ≤ 1000`. Even a brute-force divisor enumeration would easily fit within the limits. Still, there is a cleaner mathematical observation that solves the problem instantly.

The most important edge case is odd numbers. Consider:

```
x = 3
```

All divisors are odd, so the number of even divisors is zero while the number of odd divisors is positive. The correct answer is `"no"`.

Another subtle case is powers of two. For example:

```
x = 8
```

Divisors are:

```
1, 2, 4, 8
```

There is only one odd divisor, `1`, and three even divisors. A careless assumption that all even numbers work would fail here.

The key special case is numbers divisible by exactly one factor of two. For example:

```
x = 6
```

Divisors:

```
1, 2, 3, 6
```

Odd divisors: `1, 3`

Even divisors: `2, 6`

Counts match, so the answer is `"yes"`.

## Approaches

The brute-force solution enumerates all divisors from `1` to `x`. For every divisor, we check whether it is even or odd and maintain two counters. At the end, we compare the counts.

This works because it directly computes the quantities requested in the statement. With `x ≤ 1000`, the worst-case operation count is only about one thousand iterations, which is trivial.

The mathematical observation comes from factorization. Any positive integer can be written as:

```
x = 2^k * m
```

where `m` is odd.

Every odd divisor must come entirely from `m`, because including any factor of `2` would make the divisor even.

Every even divisor is formed by taking an odd divisor and multiplying it by at least one factor of `2`.

If `k = 0`, the number is odd, so there are no even divisors.

If `k ≥ 2`, there are strictly more even divisors than odd divisors because there are multiple choices for powers of `2`.

The counts become equal only when `k = 1`, meaning the number is divisible by `2` but not by `4`.

So the entire problem reduces to checking:

```
x % 2 == 0 and x % 4 != 0
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `x`.
2. Check whether `x` is even.

If `x` is odd, it cannot have any even divisors, so the answer must be `"no"`.
3. Check whether `x` is divisible by `4`.

Numbers divisible by `4` contain at least two factors of `2`, which creates more even divisors than odd divisors.
4. If `x` is divisible by `2` but not by `4`, print `"yes"`.
5. Otherwise, print `"no"`.

### Why it works

Every divisor can be classified according to how many factors of `2` it contains. When the number has exactly one factor of `2`, every odd divisor corresponds to exactly one even divisor obtained by multiplying by `2`. This creates a perfect one-to-one pairing between odd and even divisors, so their counts are equal.

If there are no factors of `2`, even divisors do not exist. If there are two or more factors of `2`, multiple even divisors correspond to the same odd divisor, making the counts unequal.

## Python Solution

```python
import sys
input = sys.stdin.readline

x = int(input())

if x % 2 == 0 and x % 4 != 0:
    print("yes")
else:
    print("no")
```

The implementation directly encodes the mathematical condition derived earlier.

The expression `x % 2 == 0` checks whether the number is even.

The expression `x % 4 != 0` guarantees that the number contains exactly one factor of `2`.

Both conditions together characterize extraordinarily nice numbers completely.

## Worked Examples

### Example 1

Input:

```
2
```

Trace:

| Variable | Value |
| --- | --- |
| x | 2 |
| x % 2 == 0 | True |
| x % 4 != 0 | True |
| Output | yes |

This demonstrates the smallest valid extraordinarily nice number.

### Example 2

Input:

```
8
```

Trace:

| Variable | Value |
| --- | --- |
| x | 8 |
| x % 2 == 0 | True |
| x % 4 != 0 | False |
| Output | no |

This shows why not all even numbers satisfy the condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are used |
| Space | O(1) | No extra memory proportional to input size |

The solution is constant time and constant space, far below the limits for `x ≤ 1000`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    x = int(input())

    if x % 2 == 0 and x % 4 != 0:
        print("yes")
    else:
        print("no")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run("2\n") == "yes", "sample 1"

# custom cases
assert run("1\n") == "no", "odd number"
assert run("4\n") == "no", "multiple factors of two"
assert run("6\n") == "yes", "exactly one factor of two"
assert run("1000\n") == "no", "large divisible by four"
assert run("10\n") == "yes", "another valid case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `no` | Odd numbers have zero even divisors |
| `4` | `no` | Powers of two beyond `2` fail |
| `6` | `yes` | Exactly one factor of two works |
| `1000` | `no` | Large number divisible by four |
| `10` | `yes` | General valid even number |

## Edge Cases

Consider the input:

```
1
```

The divisors are only `{1}`. There are zero even divisors and one odd divisor, so the counts are unequal. The algorithm checks `x % 2 == 0`, which immediately fails, producing `"no"`.

Now consider:

```
4
```

Prime factorization:

```
4 = 2^2
```

Divisors are:

```
1, 2, 4
```

Odd divisors: `1`

Even divisors: `2, 4`

The counts differ. The algorithm detects that `4 % 4 == 0`, so it correctly prints `"no"`.

Finally, consider:

```
6
```

Prime factorization:

```
6 = 2 * 3
```

Divisors are:

```
1, 2, 3, 6
```

Odd divisors: `1, 3`

Even divisors: `2, 6`

The counts match exactly. The algorithm sees that `6` is divisible by `2` but not by `4`, producing `"yes"` correctly.
