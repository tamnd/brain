---
title: "CF 1969A - Two Friends"
description: "Each friend is assigned exactly one other friend as their “best friend”, and this assignment forms a permutation of size $n$. The key rule is that a friend only attends the party if both they and their assigned best friend are invited."
date: "2026-06-08T17:42:52+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1969
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 165 (Rated for Div. 2)"
rating: 800
weight: 1969
solve_time_s: 83
verified: true
draft: false
---

[CF 1969A - Two Friends](https://codeforces.com/problemset/problem/1969/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation, math  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

Each friend is assigned exactly one other friend as their “best friend”, and this assignment forms a permutation of size $n$. The key rule is that a friend only attends the party if both they and their assigned best friend are invited.

This creates a dependency graph where every vertex has exactly one outgoing edge, and every node also has exactly one incoming edge. The structure is therefore a disjoint union of directed cycles. Each cycle represents a closed group of mutual dependencies.

We are allowed to send invitations to any subset of friends. Among those invited, only some will actually show up: a friend $i$ appears in the final attendance only if both $i$ and $p_i$ are in the invited set. The goal is to ensure that at least two friends end up attending, while minimizing how many invitations are sent.

The constraints are small, with $n \le 50$, so even cubic or exponential reasoning per test case would be acceptable. However, the number of test cases can be large, up to 5000, so the solution must be linear or near-linear per test case.

A naive but important failure case comes from assuming that inviting two friends is always enough. Consider a 4-cycle like $1 \to 2 \to 3 \to 4 \to 1$. If we invite only two nodes that are not mutual best friends, say 1 and 2, no one attends because 1 needs 2 and 2 needs 3. So the actual attendance is empty. This shows that “inviting two people” is not equivalent to “getting two attendees”.

Another subtle case is when there is a 2-cycle. For example $1 \leftrightarrow 2$. Inviting just 1 and 2 is sufficient, and both attend. This suggests that small cycles behave differently from longer ones, and cycle structure is the core of the problem.

## Approaches

The brute-force idea is to try every subset of invited friends, simulate who attends, and take the smallest subset that yields at least two attendees. For each subset, we check every friend to see whether both them and their best friend are present. This is $O(2^n \cdot n)$, which is already infeasible even for $n = 50$, since $2^{50}$ is astronomically large.

The key observation is that attendance is completely determined by cycles in the permutation. Since each node points to exactly one other node and all nodes are distinct, the graph decomposes into cycles. Within a cycle, attendance is constrained by adjacency along that cycle.

For a cycle of length 2, inviting both nodes immediately yields 2 attendees. For any cycle of length greater than 2, a single invited node does not propagate attendance, because its neighbor must also be invited, and that neighbor depends on another node, creating a chain that cannot close unless the entire cycle is considered.

The crucial simplification is that the answer depends only on the smallest cycle size, but with a special distinction: a 2-cycle gives answer 2, while any cycle of length at least 3 allows us to get 2 attendees by inviting any 3 consecutive nodes in the cycle. That ensures a chain where two adjacent dependencies are satisfied simultaneously.

Thus, the problem reduces to finding all cycle lengths and taking the minimum possible way to produce at least two attendees, which becomes either 2 (if any 2-cycle exists) or 3 otherwise.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Cycle decomposition | $O(n)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently and extract the permutation cycles.

1. Build a visited array of size $n$, initially all false. This ensures we do not revisit nodes already assigned to a cycle.
2. Iterate over every node $i$. If it is not visited, start following the chain $i \to p_i \to p_{p_i} \to \dots$ until we return to a visited node. All nodes encountered form one cycle. Mark them visited.
3. Record the length of each cycle. This is sufficient because the permutation structure guarantees no branching, so every node belongs to exactly one cycle.
4. If any cycle has length exactly 2, immediately return 2. This is because a 2-cycle allows mutual dependency satisfaction with exactly two invitations, one per node.
5. If no 2-cycle exists, return 3. Any longer cycle always allows constructing a valid configuration with 3 invitations that produces at least two attendees.

The correctness hinges on the fact that the best friend relationship is symmetric in cycles only of length 2. Longer cycles require breaking dependency chains, and the smallest stable configuration that produces attendance requires three consecutive nodes.

### Why it works

The permutation decomposes into independent cycles, and attendance constraints are local to edges. A 2-cycle is the only structure where two nodes can satisfy each other without involving any third node. Every cycle of length at least 3 forces at least one intermediate dependency, so two invitations are insufficient to guarantee two attendees unless the cycle itself is exactly size 2. Once all 2-cycles are ruled out, the minimal construction that activates two adjacent dependency relations requires three nodes, which is always achievable inside any longer cycle.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = [0] + list(map(int, input().split()))
        
        vis = [False] * (n + 1)
        has_two_cycle = False

        for i in range(1, n + 1):
            if not vis[i]:
                cur = i
                cycle = []
                while not vis[cur]:
                    vis[cur] = True
                    cycle.append(cur)
                    cur = p[cur]

                if len(cycle) == 2:
                    has_two_cycle = True

        if has_two_cycle:
            print(2)
        else:
            print(3)

if __name__ == "__main__":
    solve()
```

The code directly implements cycle decomposition of the permutation. The array is 1-indexed to match the problem definition, which avoids off-by-one mistakes when following $p_i$. Each cycle is collected by walking until a previously visited node is encountered, and its length is used only to detect whether a 2-cycle exists. The answer depends only on whether any cycle of length two appears.

A subtle point is that we never need to simulate invitations or attendance explicitly. The cycle structure fully determines feasibility, so tracking only cycle lengths is sufficient.

## Worked Examples

### Example 1

Input:

```
5
3 1 2 5 4
```

| Start node | Cycle discovered | Cycle length | 2-cycle found |
| --- | --- | --- | --- |
| 1 | 1 → 3 → 2 → 1 | 3 | No |
| 4 | 4 → 5 → 4 | 2 | Yes |

This shows that although a 3-cycle exists, the presence of a 2-cycle dominates the answer. Once a mutual pair exists, inviting just those two yields two attendees, which is optimal.

### Example 2

Input:

```
4
2 3 4 1
```

| Start node | Cycle discovered | Cycle length | 2-cycle found |
| --- | --- | --- | --- |
| 1 | 1 → 2 → 3 → 4 → 1 | 4 | No |

Since no 2-cycle exists, the best possible construction requires 3 invitations. Any attempt with 2 invitations fails because every node depends on another node outside the chosen set.

This confirms that longer cycles cannot achieve two attendees with only two invitations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each node is visited exactly once while forming cycles |
| Space | $O(n)$ | Visited array and temporary cycle storage |

The constraints allow up to 5000 test cases, but each test case is linear in $n \le 50$, so the total work remains small. The solution easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n = int(input())
        p = [0] + list(map(int, input().split()))
        
        vis = [False] * (n + 1)
        has_two_cycle = False

        for i in range(1, n + 1):
            if not vis[i]:
                cur = i
                cycle = []
                while not vis[cur]:
                    vis[cur] = True
                    cycle.append(cur)
                    cur = p[cur]
                if len(cycle) == 2:
                    has_two_cycle = True

        print(2 if has_two_cycle else 3)

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("3\n5\n3 1 2 5 4\n4\n2 3 4 1\n2\n2 1") == "2\n3\n2"

# all nodes in 2-cycles
assert run("1\n2\n2 1") == "2"

# single large cycle
assert run("1\n5\n2 3 4 5 1") == "3"

# mixture with 2-cycle
assert run("1\n4\n2 1 4 3") == "2"

# minimum n
assert run("1\n2\n2 1") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 2 | smallest possible cycle |
| 5-cycle | 3 | absence of 2-cycle forces 3 |
| mixed cycles | 2 | dominance of 2-cycle condition |

## Edge Cases

A key edge case is when the permutation consists entirely of cycles longer than 2. For example $1 \to 2 \to 3 \to 4 \to 1$. The algorithm correctly identifies a single cycle of length 4 and sets no 2-cycle flag, producing output 3. Any attempt to reduce to 2 invitations fails because no pair can satisfy mutual dependency.

Another case is when multiple cycles exist and only one of them is a 2-cycle, such as $1 \leftrightarrow 2$ and $3 \to 4 \to 5 \to 3$. The algorithm detects the 2-cycle in the first component and immediately concludes the answer is 2. This is correct because cycles are independent, and one valid pair is sufficient to meet the requirement of at least two attendees.

A final subtle case is when $n = 2$. The only possible permutation is a 2-cycle, so the answer is always 2. The algorithm naturally handles this without special casing since the cycle detection logic marks the length-two cycle directly.
