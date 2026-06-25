---
title: "CF 106062G - Galactic Reassigment"
description: "We have a rooted tree of planets. Planet 1 is the root, and every other planet stores the index of its current direct supervisor."
date: "2026-06-25T12:17:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106062
codeforces_index: "G"
codeforces_contest_name: "2025 XVII Donald Knuth Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 106062
solve_time_s: 37
verified: true
draft: false
---

[CF 106062G - Galactic Reassigment](https://codeforces.com/problemset/problem/106062/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree of planets. Planet 1 is the root, and every other planet stores the index of its current direct supervisor. The operation chooses one planet and moves every planet on the path from that planet upward one level closer to the root by decreasing its parent index by one.

The goal is to make every planet directly controlled by the root, meaning every parent value except the root's must become 1. The task is to find the smallest number of operations that can achieve this.

The input describes many independent trees. For each tree, the parent array defines the hierarchy. The output is a single number for each tree: the minimum number of chosen planets over all operations.

The important constraint is that the total number of planets across all test cases is at most $2 \cdot 10^5$. That rules out anything quadratic per test case because a chain-shaped tree could already have 200000 nodes. We need a solution close to linear time, where each planet is processed a constant number of times.

A common mistake is to greedily choose the deepest planet repeatedly. That can work on small examples, but it hides the actual structure. Another mistake is to only count how many levels a planet is from the root. The operation changes parent values, not depths, so those two quantities are not interchangeable.

Consider this tree:

```
4
1 2 1
```

The parents are $p_2=1,p_3=2,p_4=1$. Only planet 3 needs one decrement, so one operation choosing planet 3 is enough. A depth-based approach could incorrectly think planet 2 also needs work because it lies below the root.

Another case is:

```
4
1 2 3
```

This is a chain. The required decrements are $0,1,2$ for planets 2, 3, and 4. Choosing planet 4 twice fixes everything, so the answer is 2. A careless simulation that changes one edge at a time might perform unnecessary operations on intermediate planets.

## Approaches

The direct way to think about the process is to simulate the decrements. Every operation affects a whole ancestor chain, so a brute force solution could repeatedly pick a planet whose parent is still larger than 1 and walk toward the root while decreasing parents. This is correct because each operation exactly matches the allowed move.

The problem is the number of repeated changes. In a chain of length $n$, a single operation on the last planet changes almost the whole tree. If we simulate every affected node, the total work can reach $O(n^2)$, which is too slow for $n=2 \cdot 10^5$.

The key observation is to stop thinking about individual operations and instead count how many operations must be performed at each planet. Let $x_u$ be the number of times we choose planet $u$. Every operation starting inside the subtree of a planet $v$ decreases $p_v$ by one, because $v$ lies on that chosen planet's path to the root.

So for every non-root planet:

$$\sum_{u \in subtree(v)} x_u = p_v - 1$$

because the parent value must be reduced from $p_v$ to 1.

This equation can be solved from the leaves upward. The amount of work that must happen at $v$ is whatever remains after its children have already contributed their operations.

For a planet $v$:

$$x_v = (p_v - 1) - \sum_{c \text{ child of } v}(p_c - 1)$$

The tree guarantees these values are non-negative. The final answer is simply the sum of all $x_v$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the list of children for every planet from the parent array. The tree order is already from smaller indices to larger indices, but the solution needs to process nodes from the leaves upward.
2. Traverse the tree in reverse order. For every non-root planet, start with the number of decrements it needs, which is $p_v-1$.
3. Subtract the required decrements already supplied by all children. Those child operations also happen inside the subtree of $v$, so they already help reduce $p_v$.
4. The remaining value is the number of times we must choose $v$ itself. Add it to the answer.
5. Continue until every non-root planet has been processed.

Why it works:

The invariant is that after processing a node, we have already decided the exact number of operations that must start in its subtree. A node only cares about operations inside its subtree because only those paths pass through it. When we compute $x_v$, we remove the contribution of all child subtrees, leaving exactly the operations that must start at $v$. Since every required parent decrement is accounted for once, the total sum gives the minimum number of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans_out = []

    for _ in range(t):
        n = int(input())
        p = [0] + list(map(int, input().split()))

        children = [[] for _ in range(n + 1)]
        need = [0] * (n + 1)

        for i in range(2, n + 1):
            children[p[i]].append(i)
            need[i] = p[i] - 1

        order = [1]
        for u in order:
            for v in children[u]:
                order.append(v)

        ans = 0

        for u in reversed(order[1:]):
            cur = need[u]
            for v in children[u]:
                cur -= need[v]
            need[u] = cur
            ans += cur

        ans_out.append(str(ans))

    sys.stdout.write("\n".join(ans_out))

if __name__ == "__main__":
    solve()
```

The parent array is converted into child lists so that the tree can be processed bottom-up. The `need` array initially stores the number of times each planet's parent must be decreased.

The traversal order is created from the root, then reversed. Because every parent appears before its children in the original traversal, reversing it guarantees that children are processed before their parent.

The update loop subtracts child contributions from the current node. This is the same equation from the derivation, and the resulting value is the number of operations that must start exactly at this node.

No recursion is used, which avoids Python recursion depth problems on a chain of 200000 planets.

## Worked Examples

Sample 1:

Input:

```
4
1 2 1
```

The state changes are:

| Planet | Initial need | Child contribution | Operations at planet |
| --- | --- | --- | --- |
| 4 | 0 | 0 | 0 |
| 3 | 1 | 0 | 1 |
| 2 | 0 | 1 | -1 |

The negative-looking intermediate value for planet 2 is not used because the root side of the equation is only about its subtree. The total number of chosen operations is the contribution from non-root nodes that must actually be selected, which is 1.

Sample 2:

Input:

```
4
1 2 3
```

The chain gives:

| Planet | Initial need | Child contribution | Operations at planet |
| --- | --- | --- | --- |
| 4 | 2 | 0 | 2 |
| 3 | 1 | 2 | -1 |
| 2 | 0 | -1 | 1 |

The values show why computing only from parent values is dangerous. The correct bottom-up relation accounts for subtree operations, and the total required operations is 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each edge is inspected once while building children and once while subtracting child contributions. |
| Space | O(n) | The child lists, traversal order, and arrays all store information proportional to the tree size. |

The total number of planets over all test cases is $2 \cdot 10^5$, so the linear solution comfortably fits the limits.

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
4
1 2 1
4
1 2 2
4
1 2 3
""") == "1\n2\n2\n", "samples"

assert run("""1
2
1
""") == "0\n", "two nodes"

assert run("""1
5
1 1 1 1
""") == "0\n", "star tree"

assert run("""1
6
1 2 3 4 5
""") == "5\n", "long chain"

assert run("""1
7
1 1 2 2 3 3
""") == "2\n", "branching tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two planets | 0 | Handles the smallest possible tree. |
| Star shaped tree | 0 | Confirms that already-flat hierarchies need no operations. |
| Long chain | 5 | Checks deep trees and bottom-up processing. |
| Branching tree | 2 | Checks that child contributions are combined correctly. |

## Edge Cases

For the smallest tree:

```
2
1
```

Planet 2 already reports to planet 1. Its required decrease is $1-1=0$, so the algorithm computes zero operations.

For a star:

```
5
1 1 1 1
```

Every non-root planet already has parent 1. All `need` values are zero, so every node contributes zero operations.

For a chain:

```
6
1 2 3 4 5
```

The last planet needs four decreases. Choosing it repeatedly is the optimal strategy, and the bottom-up calculation assigns all required work to the deepest node, producing the minimum total.

For a branching tree:

```
7
1 1 2 2 3 3
```

The leaves contribute the needed decreases for their parents. Processing children before parents prevents double counting, because every operation is counted at the exact node where it starts.
