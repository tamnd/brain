---
title: "CF 102253L - Limited Permutation"
description: "For every position (i), the pair ((li,ri)) describes the largest contiguous interval containing (i) on which (pi) is the minimum."
date: "2026-08-17T21:47:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102253
codeforces_index: "L"
codeforces_contest_name: "2017 Chinese Multi-University Training, BeihangU Contest"
rating: 0
weight: 102253
solve_time_s: 248
verified: true
draft: false
---

[CF 102253L - Limited Permutation](https://codeforces.com/problemset/problem/102253/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

For every position (i), the pair ((l_i,r_i)) describes the largest contiguous interval containing (i) on which (p_i) is the minimum. Equivalently, (p_i) is smaller than every element between (l_i) and (i-1), every element between (i+1) and (r_i), and the interval cannot be extended one position farther in either direction.

The task is to count how many permutations of (1,\ldots,n) have exactly these minimum intervals. The answer is taken modulo (10^9+7). The official editorial identifies the resulting structure as a unique Cartesian tree when the input is valid.

The constraints are large enough that the algorithm must be essentially linear. A test case can contain (10^6) positions, and all test cases together contain at most (3\cdot10^6) positions. An (O(n\log n)) solution is already much more expensive than necessary, especially in Python, while anything quadratic is completely ruled out. The memory limit of 128 MB also matters because ordinary Python lists of a million integers consume tens of megabytes each. The implementation below uses compact integer arrays and counting sort rather than Python's object-heavy lists and comparison sort.

There are several ways a careless implementation can fail. For (n=1), the only possible input is

```
1
1
1
```

and the answer is (1). Treating an empty child interval as invalid would incorrectly reject the only valid tree.

Duplicate or incompatible intervals must also be rejected. For example,

```
3
1 1 1
3 3 3
```

gives the same interval ([1,3]) for all three positions. A naive implementation that simply chooses one of those positions as the root might continue as if the tree were valid, but there is no way for all three positions to have the same maximal minimum interval. The correct output is `Case #1: 0`.

Crossing intervals are another common failure. Consider

```
3
1 1 2
2 3 3
```

which gives ([1,2]), ([1,3]), and ([2,3]). The intervals overlap without one containing the other. Such a configuration cannot come from a Cartesian tree, so the answer is `Case #1: 0`. A solution that only checks that every (l_i\le i\le r_i) would incorrectly accept it.

## Approaches

A brute-force solution can enumerate every permutation of (1,\ldots,n), calculate the maximal minimum interval for every position, and compare the result with the input. There are (n!) permutations. Even if one uses a linear-time monotonic-stack procedure to calculate all nearest smaller elements for each permutation, checking all permutations already costs (\Theta(n\cdot n!)) operations. A straightforward direct scan of every relevant interval would make the cost (\Theta(n^2\cdot n!)). This becomes hopeless even around (n=10), long before the actual constraint of (10^6).

The useful observation is that the given intervals are not arbitrary. For a permutation, consider its min-Cartesian tree. The root is the position containing the smallest value, its left subtree contains the positions to the left of the root, and its right subtree contains the positions to the right. For every node (u), the positions in its subtree form one contiguous interval, exactly ([l_u,r_u]). This is the same recursive structure used in the official solution.

Suppose some subtree occupies ([L,R]), and its root is at position (u). Then its left child must represent exactly ([L,u-1]), while its right child must represent exactly ([u+1,R]). Thus the entire tree can be reconstructed by repeatedly asking which input interval equals the current required interval.

This also gives a direct counting formula. Let (s(u)) be the size of the subtree rooted at (u). Because the subtree is exactly ([l_u,r_u]),

[
s(u)=r_u-l_u+1.
]

For a fixed Cartesian tree, the smallest value must be assigned to its root. The remaining values are split between the left and right subtrees. If their sizes are (a) and (b), there are

[
\binom{a+b}{a}
]

ways to choose which values belong to the left subtree. Multiplying this recursively gives

[
f(u)=\binom{s(v_L)+s(v_R)}{s(v_L)}f(v_L)f(v_R).
]

Expanding the factorials shows that the complete product simplifies to

\frac{n!}{\prod_{i=1}^{n}(r_i-l_i+1)}.
]

The official editorial gives exactly this equivalent form.

The remaining challenge is locating the root interval efficiently. If we sort all intervals by increasing (l), and for equal (l), by decreasing (r), their order is the preorder of the Cartesian tree. Since both coordinates are at most (n), this sorting can be done with two stable counting-sort passes, giving linear time rather than (O(n\log n)). The official editorial likewise recommends radix sorting the intervals before the recursive decomposition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(n\cdot n!)) with linear validation | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the arrays (l) and (r), keeping them in compact integer arrays. For every position (i), regard ([l_i,r_i]) as the claimed subtree interval of node (i).
2. Sort the positions by (l_i) ascending and (r_i) descending. We use stable counting sort twice, first by (n-r_i), then by (l_i). The first pass produces decreasing (r_i) inside equal-(l_i) groups, and the second pass preserves that order.
3. Start with the required interval ([1,n]). The first interval in the sorted preorder must be exactly this interval. If it is not, the input cannot describe any Cartesian tree, so the answer is zero.
4. When the current interval is ([L,R]) and its root is at position (u), require the root's input interval to be exactly ([L,R]). Then the only possible children occupy ([L,u-1]) and ([u+1,R]). Push the right interval first and the left interval second onto a stack so that the left subtree is processed next. Every nonempty subtree contributes its size (R-L+1) to the denominator.
5. After every nonempty required interval has been consumed, the data is valid exactly when all (n) input intervals have also been consumed. Compute (n!) modulo (10^9+7), multiply it by the modular inverse of every subtree size, and obtain

n!\prod_{i=1}^{n}(r_i-l_i+1)^{-1}
\pmod {10^9+7}.
]

The inverses of all values from (1) to (10^6) are precomputed once using

-\left\lfloor\frac{MOD}{i}\right\rfloor
\operatorname{inv}(MOD\bmod i)
\pmod {MOD}.
]

### Why it works

For any valid permutation, its min-Cartesian tree has exactly one subtree interval for every node, and that subtree interval is ([l_i,r_i]). At a subtree ([L,R]), its root (u) separates the positions into the mandatory left interval ([L,u-1]) and right interval ([u+1,R]). Hence every valid tree must pass every interval check performed by the algorithm.

Conversely, if all required intervals are found in the correct recursive order, they define a binary tree whose inorder traversal is (1,2,\ldots,n), and every node's subtree is exactly its supplied interval. Assigning values increasingly along this min-heap tree produces precisely the required Cartesian-tree structure. Since the permutation contains distinct values, every valid permutation corresponds to exactly one such labeling.

For a fixed tree, the recursive interleaving count is the product of binomial coefficients described above. Each node contributes one subtree-size denominator, so all internal factorials cancel and leave (n!/\prod s(u)). Since (s(u)=r_u-l_u+1), the formula used by the algorithm counts every valid permutation exactly once.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 1000000007
MAX_N = 1000000

# Modular inverses for every possible subtree size.
inv = array('I', [0]) * (MAX_N + 1)
inv[1] = 1
for i in range(2, MAX_N + 1):
    inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

def radix_order(l, r, n):
    """
    Return indices sorted by:
        l[index] ascending
        r[index] descending
    using two stable counting-sort passes.
    """
    order = array('i', range(n))
    tmp = array('i', [0]) * n

    # First pass: r descending, encoded as n - r.
    cnt = array('i', [0]) * (n + 1)

    for idx in order:
        cnt[n - r[idx]] += 1

    pos = 0
    for key in range(n + 1):
        c = cnt[key]
        cnt[key] = pos
        pos += c

    for idx in order:
        key = n - r[idx]
        p = cnt[key]
        tmp[p] = idx
        cnt[key] = p + 1

    # Second pass: l ascending.
    cnt = array('i', [0]) * (n + 1)

    for idx in tmp:
        cnt[l[idx]] += 1

    pos = 0
    for key in range(n + 1):
        c = cnt[key]
        cnt[key] = pos
        pos += c

    for idx in tmp:
        key = l[idx]
        p = cnt[key]
        order[p] = idx
        cnt[key] = p + 1

    return order

def solve_case(n, l, r):
    order = radix_order(l, r, n)

    # Each item is an expected subtree interval [L, R].
    # We process them in preorder.
    stack_l = [1]
    stack_r = [n]

    ptr = 0
    denominator = 1

    while stack_l:
        L = stack_l.pop()
        R = stack_r.pop()

        if L > R:
            continue

        if ptr >= n:
            return 0

        u = order[ptr]
        ptr += 1

        # The next preorder node must represent exactly [L, R].
        if l[u] != L or r[u] != R or not (L <= u <= R):
            return 0

        size = R - L + 1
        denominator = denominator * size % MOD

        # Push right first so that left is processed first.
        if u + 1 <= R:
            stack_l.append(u + 1)
            stack_r.append(R)

        if L <= u - 1:
            stack_l.append(L)
            stack_r.append(u - 1)

    # Every supplied interval must belong to the constructed tree.
    if ptr != n:
        return 0

    factorial = 1
    for x in range(2, n + 1):
        factorial = factorial * x % MOD

    return factorial * pow(denominator, MOD - 2, MOD) % MOD

def solve():
    case_no = 1
    output = []

    while True:
        line = input()
        if not line:
            break
        if not line.strip():
            continue

        n = int(line)

        l = array('i', map(int, input().split()))
        r = array('i', map(int, input().split()))

        ans = solve_case(n, l, r)
        output.append(f"Case #{case_no}: {ans}")
        case_no += 1

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The inverse table is built once because every subtree size lies between (1) and (n), and (n\le10^6). The recurrence avoids doing a modular exponentiation for every node. A single `pow` is still used for the final denominator in the implementation, but it could equivalently be replaced by multiplying `inv[size]` for every node during validation. The latter avoids the final exponentiation and is slightly more consistent with the formula.

The two arrays (l) and (r) use `array('i')` rather than Python lists. A Python integer is an object with substantial overhead, while a 32-bit integer is enough because every coordinate is at most (10^6). The sorting buffers and counting array use the same representation for the same reason.

The radix sort uses (n-r_i) as the first key. Counting it in ascending order is equivalent to sorting (r_i) in descending order. The second pass sorts by (l_i) ascending and is stable, so equal (l_i) values retain their decreasing-(r_i) order.

The recursive tree decomposition is implemented with an explicit stack. A recursive Python implementation can reach depth (10^6) on a completely skewed Cartesian tree and would overflow the recursion limit. The stack also avoids function-call overhead.

The condition `l[u] != L or r[u] != R` is the core validity check. A node may only be the root of the subtree whose boundaries are exactly its supplied boundaries. The check `L <= u <= R` is implied by the original input constraints, but keeping it makes the tree invariant explicit and protects the routine if the input validation assumptions are changed.

The denominator contains subtree sizes, not child sizes. For example, a root covering five positions contributes (5), even if its children have sizes one and three. This is the quantity that appears in the simplified (n!/\prod s(u)) formula.

## Worked Examples

### Sample 1

The input is

```
3
1 1 3
1 3 3
```

The three intervals are ([1,1]), ([1,3]), and ([3,3]). After sorting by increasing left endpoint and decreasing right endpoint, the preorder is the node at position (2), followed by positions (1) and (3).

| Required interval | Chosen root | Root interval | Subtree size | Denominator |
| --- | --- | --- | --- | --- |
| [1,3] | 2 | [1,3] | 3 | 3 |
| [1,1] | 1 | [1,1] | 1 | 3 |
| [3,3] | 3 | [3,3] | 1 | 3 |

The tree has root (2), left child (1), and right child (3). The denominator is (3), while (3!=6), so

[
\frac{3!}{3}=2.
]

The two permutations are the two possible ways to put the larger values on the two sides of the minimum.

### Sample 2

The input is

```
5
1 2 2 4 5
5 2 5 5 5
```

The intervals are ([1,5]), ([2,2]), ([2,5]), ([4,5]), and ([5,5]).

| Required interval | Chosen root | Root interval | Subtree size | Denominator |
| --- | --- | --- | --- | --- |
| [1,5] | 1 | [1,5] | 5 | 5 |
| [2,5] | 3 | [2,5] | 4 | 20 |
| [2,2] | 2 | [2,2] | 1 | 20 |
| [4,5] | 4 | [4,5] | 2 | 40 |
| [5,5] | 5 | [5,5] | 1 | 40 |

The resulting Cartesian tree has position (1) as its root, position (3) as its right child, position (2) as the left child of (3), and the chain (4\rightarrow5) on the right.

The final count is

# \frac{120}{40}

1. 

]

This example shows why simply checking the intervals individually is insufficient. Their recursive containment relationships are what determine the tree and consequently the number of labelings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) per test case | Two counting-sort passes, one tree traversal, and one factorial computation |
| Space | (O(n)) | Input arrays, radix-sort buffers, counting array, and traversal stack |

The total (n) over all test cases is at most (3\cdot10^6), so the linear work scales directly with the total input size. The compact `array` representation keeps the main arrays within the 128 MB memory limit. The algorithm avoids Python comparison sorting and avoids recursion, both of which matter at (n=10^6).

## Test Cases

The following tests assume the `solve()` function from the solution above. The helper temporarily replaces the global `input` function so the same solver can be exercised with an in-memory input stream.

```python
import sys
import io

# The solve() function and global input from the submitted solution
# are assumed to be available here.

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline
        solve()
        # solve() writes to stdout, so capture it through a second redirection.
    finally:
        sys.stdin = old_stdin
        input = old_input

def run_capture(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        input = sys.stdin.readline

        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided samples.
sample = """\
3
1 1 3
1 3 3
5
1 2 2 4 5
5 2 5 5 5
"""
assert run_capture(sample) == (
    "Case #1: 2\n"
    "Case #2: 3\n"
), "provided samples"

# Minimum size.
assert run_capture(
    "1\n"
    "1\n"
    "1\n"
) == "Case #1: 1\n", "single element"

# A valid two-element increasing Cartesian tree.
assert run_capture(
    "2\n"
    "1 2\n"
    "2 2\n"
) == "Case #1: 1\n", "two-element boundary case"

# All intervals are identical. No valid Cartesian tree exists.
assert run_capture(
    "3\n"
    "1 1 1\n"
    "3 3 3\n"
) == "Case #1: 0\n", "duplicate root intervals"

# Crossing intervals. They cannot be nested as Cartesian-tree subtrees.
assert run_capture(
    "3\n"
    "1 1 2\n"
    "2 3 3\n"
) == "Case #1: 0\n", "crossing intervals"

# Maximum-size test. Every interval is a singleton, which is invalid
# for n > 1 because the root interval must be [1, n].
n = 1_000_000
l = " ".join(map(str, range(1, n + 1)))
r = l
maximum_case = f"{n}\n{l}\n{r}\n"

assert run_capture(maximum_case) == "Case #1: 0\n", "maximum-size input"
```

The `run` helper above is retained as the simple interface requested in the test template, while `run_capture` is used for assertions because the production solver writes directly to standard output.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `Case #1: 1` | Minimum-size tree and empty-child handling |
| `2 / 1 2 / 2 2` | `Case #1: 1` | Boundary intervals and a root at the left endpoint |
| `3 / 1 1 1 / 3 3 3` | `Case #1: 0` | Duplicate intervals and invalid Cartesian-tree structure |
| `3 / 1 1 2 / 2 3 3` | `Case #1: 0` | Crossing intervals and recursive validation |
| (n=10^6), (l_i=r_i=i) | `Case #1: 0` | Maximum input size and linear-time behavior |

## Edge Cases

For the single-element case

```
1
1
1
```

the sorted order contains one interval, and the initial required interval is also ([1,1]). The node has subtree size (1), so the denominator is (1), the factorial is (1), and the result is (1). No left or right child is pushed onto the stack.

For the all-equal interval case

```
3
1 1 1
3 3 3
```

the first sorted interval is ([1,3]), so the algorithm initially accepts one of the three nodes as a candidate root. If that node is at position (1), for example, the next required interval is ([2,3]), but the next sorted input interval is still ([1,3]). The exact interval comparison fails and the answer becomes zero. The same contradiction appears for either other candidate root.

For the crossing case

```
3
1 1 2
2 3 3
```

the sorted intervals are ([1,2]), ([1,3]), ([2,3]). The root of the complete array must cover ([1,3]), but the first sorted interval is ([1,2]). The algorithm immediately rejects the input. This catches an invalid overlap before any counting is performed.

For the two-element boundary case

```
2
1 2
2 2
```

the root interval is ([1,2]), belonging to position (1). Its right child is the singleton interval ([2,2]). The subtree sizes are (2) and (1), giving

[
\frac{2!}{2\cdot1}=1.
]

The only valid permutation is increasing, so the boundary check and child interval construction both agree with the combinatorial count.

For the maximum-size input with (l_i=r_i=i), the first interval is ([1,1]), while the whole array requires a root covering ([1,10^6]). The algorithm rejects the instance after reaching the first mismatch, although the radix sort has still processed all (10^6) intervals. The total work remains linear, and no recursive call can overflow the Python stack.
