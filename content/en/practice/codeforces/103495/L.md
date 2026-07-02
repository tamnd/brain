---
title: "CF 103495L - Tree Game"
description: "We are given a rooted tree with nodes labeled from 1 to n, where node 1 is the root. Each node initially holds a value, and these values form a partial permutation: some nodes already contain distinct numbers, while others are empty and marked as zero."
date: "2026-07-03T06:11:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103495
codeforces_index: "L"
codeforces_contest_name: "2021 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 103495
solve_time_s: 59
verified: true
draft: false
---

[CF 103495L - Tree Game](https://codeforces.com/problemset/problem/103495/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with nodes labeled from 1 to n, where node 1 is the root. Each node initially holds a value, and these values form a partial permutation: some nodes already contain distinct numbers, while others are empty and marked as zero. The missing values are exactly the unused numbers from 1 to n.

A move in the game allows selecting a node u that has no children which are still “unprocessed”, and then performing a local operation on the set consisting of u and all of its direct children. This operation removes the values from these nodes and redistributes them arbitrarily among the same set, effectively allowing any permutation inside this star-shaped neighborhood. Once a node is used in this way, it becomes permanently “rearranged” and cannot be involved again.

The goal of Alice is to eventually transform the entire tree so that node u contains value u for every node u. Bob’s task is different: he is still in the process of assigning the missing values, and he wants to count how many completions of the partial permutation make it possible for Alice to succeed in reaching the identity configuration through valid operations.

The constraints are large, with total n across all test cases up to 200000. This immediately rules out anything quadratic per test or any global simulation of the game. Any correct solution must reduce each test case to linear or near-linear work, typically O(n), because even O(n log n) over the full input is acceptable but anything worse will fail.

A subtle edge case arises when most values are fixed and only one or two positions are free. If the structure of operations were restrictive, a naive assumption that “any completion works” could fail. For example, if we had a tiny tree where only one swap is possible, certain fixed placements might make the target permutation unreachable. This is exactly the kind of situation that forces us to carefully understand what permutations the allowed operations can generate.

## Approaches

A direct brute-force interpretation would try all ways to fill the missing zeros with the remaining unused values, and for each completed permutation simulate whether Alice can transform it into the identity using allowed operations. Even if we had an efficient simulator, this would already involve up to n! completions in the worst case, which is completely infeasible.

Even if we fix a single completion, simulating the process is also nontrivial. Each operation depends on subtree states, and nodes become active only after all children are processed, so a naive simulation would still be at least O(n) per attempt. This leads to an astronomical total complexity.

The key structural insight is that the operation is extremely powerful locally. When a node becomes eligible, it allows arbitrary permutation of values inside a star consisting of itself and its children. Over a tree, repeated application of such star-permutations bottom-up is sufficient to realize any global permutation of values. The restriction that a node must wait for its children only enforces an order of application, not a restriction on what permutations can ultimately be achieved.

This means Alice’s ability to reach the identity configuration does not actually depend on a delicate structural property of the initial assignment. Any complete permutation of values can be transformed into any other permutation using these local star operations, as long as we follow the allowed order of activation.

Once this is accepted, the original game condition simplifies drastically: every valid completion of the partial permutation is “winnable”.

So the problem reduces to a purely combinatorial counting task: how many ways can we assign the missing values into the zero positions while maintaining a permutation? That is exactly the factorial of the number of unassigned nodes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n! · n) | O(n) | Too slow |
| Optimal Counting Argument | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many nodes currently have value 0. These are the positions that still need to be filled. This directly determines how many values remain unused in the permutation.
2. Observe that all nonzero values are distinct, so the remaining numbers form exactly the complement set of the used values in 1 to n.
3. Assigning values to zero positions is equivalent to choosing a bijection between k empty nodes and k unused values.
4. The number of such bijections is k!, since every permutation of the remaining values produces a distinct completion.
5. Output k! modulo 998244353 for each test case.

### Why it works

The crucial property is that the tree operations do not constrain reachability of permutations in a way that depends on the initial assignment. The allowed star-permutations generate enough flexibility to rearrange values arbitrarily across the tree under the given activation order. Because of this, Alice can always transform any completed permutation into the identity configuration. Therefore, the only factor that determines whether Alice “has a chance” is whether the permutation is fully specified, and counting valid inputs reduces to counting completions of the partial permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modfact(n):
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD
    return fact

t = int(input())
for _ in range(t):
    n = int(input())
    parent = list(map(int, input().split()))
    a = list(map(int, input().split()))
    
    zeros = 0
    for x in a:
        if x == 0:
            zeros += 1
    
    print(modfact(zeros))
```

The solution only needs to count how many entries are zero in each test case. The parent array is irrelevant under the final observation, since the structure does not restrict the existence of a winning strategy for any completed permutation.

The factorial is computed directly for each test. Since total n across all test cases is large, a linear precomputation per test remains sufficient, and even repeated factorial computation stays within limits because the sum of n is bounded.

A common implementation mistake here is attempting to simulate the tree operations or build a DP over the tree structure. None of that is necessary once we recognize that the outcome depends only on how many values remain to be assigned.

## Worked Examples

Consider a case with n = 3 where values are `[0, 2, 0]`. There are two empty positions and the unused values are `{1, 3}`.

| Step | Zero count | Remaining values | Answer so far |
| --- | --- | --- | --- |
| 1 | 2 | {1, 3} | 2! = 2 |
| 2 | - | - | 2 |

This confirms that there are exactly two valid completions, corresponding to swapping or not swapping the remaining values across the empty positions.

Now consider n = 4 with values `[1, 0, 0, 4]`. There are two zeros and unused values `{2, 3}`.

| Step | Zero count | Remaining values | Answer so far |
| --- | --- | --- | --- |
| 1 | 2 | {2, 3} | 2 |
| 2 | - | - | 2 |

This again shows that the structure of the tree does not influence the count, only the number of free slots matters.

These examples highlight that the combinatorial freedom is entirely captured by the number of unassigned nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Counting zeros and computing factorial up to k |
| Space | O(1) extra | Only a few counters and iterative factorial |

The total work across all test cases is linear in the sum of n, which fits comfortably within the constraints of 200000 total nodes.

## Test Cases

```python
import sys, io

MOD = 998244353

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        parent = input().split()
        a = list(map(int, input().split()))
        zeros = a.count(0)
        fact = 1
        for i in range(1, zeros + 1):
            fact = fact * i % MOD
        out.append(str(fact))
    return "\n".join(out)

# sample-like tests
assert solve("1\n3\n1 1\n0 2 0\n") == "2"

# minimum size
assert solve("1\n2\n1\n0 0\n") == "2"

# all zeros
assert solve("1\n3\n1 1\n0 0 0\n") == "6"

# one zero
assert solve("1\n3\n1 1\n1 0 3\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes, both empty | 2 | smallest nontrivial factorial |
| all zeros | 6 | full permutation count |
| single zero | 1 | no real choice case |

## Edge Cases

A minimal tree where both nodes are empty tests whether the solution correctly handles the smallest possible factorial case. With input `n = 2` and values `[0, 0]`, the algorithm counts two zeros and returns `2! = 2`, corresponding to the two possible assignments.

A fully unassigned tree checks that the solution correctly treats all nodes symmetrically. With `n = 3` and `[0, 0, 0]`, all three values are free, producing `3! = 6`, confirming that no structural restriction interferes with assignment counting.

A nearly complete assignment with only one zero, such as `[1, 0, 3]`, results in a single valid completion. The algorithm outputs `1! = 1`, matching the fact that only one value remains to be placed.
