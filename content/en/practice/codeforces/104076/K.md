---
title: "CF 104076K - Stack Sort"
description: "We are given a permutation of the integers from 1 to n. We read the numbers from left to right and, as we see each number, we must immediately place it onto one of m stacks."
date: "2026-07-02T02:50:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104076
codeforces_index: "K"
codeforces_contest_name: "2022 International Collegiate Programming Contest, Jinan Site"
rating: 0
weight: 104076
solve_time_s: 56
verified: true
draft: false
---

[CF 104076K - Stack Sort](https://codeforces.com/problemset/problem/104076/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the integers from 1 to n. We read the numbers from left to right and, as we see each number, we must immediately place it onto one of m stacks. The placement is permanent, so once an element is pushed onto a stack, it stays there until that entire stack is popped.

After all pushes are done, we are allowed to start popping. The rule is that we pick a stack and keep popping from it until it becomes empty, and only then can we switch to another stack. While a stack is being popped, it behaves in the standard last-in-first-out way.

The goal is to choose how to assign elements to stacks and how to order the stack pops so that the global output sequence is exactly 1, 2, 3, up to n. We want the smallest possible number of stacks that makes this achievable.

The constraint n up to 5×10^5 across tests implies an O(n log n) or O(n) per test approach is required. Any solution that tries to simulate all stack assignments or search over partitions will immediately fail, since even O(n^2) is far beyond feasible limits.

A subtle issue is that the popping phase is constrained by stack boundaries. If a stack is chosen, it must be fully emptied before switching. This creates a strong ordering constraint on how elements inside a single stack must relate to each other in value.

A small example that exposes the constraint is the permutation [3, 1, 2]. If we try to put 3 and 1 in the same stack in push order, we get push sequence [3, 1], which will pop as [1, 3]. That cannot appear in the required global order 1, 2, 3 because 3 would appear before 2 in the wrong place relative to other stacks. This type of inversion is the core difficulty.

## Approaches

The brute-force way to think about the problem is to assign each of the n elements to one of m stacks and then simulate the popping phase to check if we can achieve the sorted output. Even for a fixed assignment, verifying correctness requires simulating stack behavior and ensuring that at each step the next required number appears at the top of some stack we choose to empty. The number of assignments is m^n in the worst case, and even restricting m does not make this viable.

The key simplification comes from looking at what structure a single stack enforces. Inside one stack, elements are popped in reverse of their push order. Since the final output must be increasing from 1 to n, the reversed push order inside each stack must itself be increasing. This means that when we look at the push order inside a stack, the values must form a strictly decreasing sequence.

So each stack is forced to contain a subsequence of the permutation that is decreasing in value with respect to time of arrival. The problem becomes a partitioning task: split the permutation into the minimum number of decreasing subsequences.

This is a classical duality result. The minimum number of decreasing subsequences needed to partition a sequence equals the length of the longest increasing subsequence. The intuition is that every increasing chain must be placed into different stacks because a single stack cannot preserve increasing order when reversed.

Thus, instead of explicitly building stacks, we compute the length of the LIS of the given permutation. That value is exactly the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force assignment and simulation | Exponential | O(n) | Too slow |
| LIS via greedy + binary search | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. We process the permutation from left to right and maintain a structure that represents the best possible “stack tops” for decreasing subsequences.
2. For each incoming value x, we want to place it into a stack that keeps that stack’s sequence strictly decreasing. This is equivalent to finding a stack whose current top is greater than x, because placing x below a larger top preserves decreasing order in push sequence.
3. Among all valid stacks, we choose the one with the smallest possible top value that is still greater than x. This greedy choice preserves flexibility for future elements, since it keeps larger tops available for larger future values.
4. If no such stack exists, we start a new stack with x. This corresponds to increasing the number of decreasing subsequences.
5. We maintain an array of stack tops sorted increasingly. Each update replaces a value or appends a new one, which can be implemented using binary search.
6. After processing all elements, the number of stacks is exactly the size of this structure.

The reason this greedy choice works is that each stack represents a decreasing subsequence in the original order. By always placing an element onto the most suitable existing stack, we ensure we do not create unnecessary new stacks when an existing one could still accommodate the element.

### Why it works

At any point, the maintained structure represents the minimal possible set of ending values of decreasing subsequences formed from the processed prefix. Each time we place an element, we either extend a subsequence or replace its ending value with a smaller one, which keeps more room for future extensions. This is exactly the patience sorting invariant for LIS computation applied to the reversed ordering interpretation. The number of stacks required is therefore the length of the longest chain of forced separations, which corresponds to the LIS length of the permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))

        piles = []

        for x in a:
            # we want first pile top > x, so we maintain increasing piles
            # use binary search on piles for first > x
            l, r = 0, len(piles)
            while l < r:
                mid = (l + r) // 2
                if piles[mid] > x:
                    r = mid
                else:
                    l = mid + 1

            if l == len(piles):
                piles.append(x)
            else:
                piles[l] = x

        print(len(piles))

if __name__ == "__main__":
    solve()
```

The implementation maintains an array `piles` where each entry represents the current smallest possible top value of a stack ending a decreasing subsequence. The binary search finds the first pile whose top is greater than the current value, which is the correct place to extend that subsequence.

If no such pile exists, a new stack is created. This is the only case where the answer increases.

## Worked Examples

### Example 1: permutation [3, 2, 1]

We track the pile tops after each insertion.

| Step | x | piles before | position chosen | piles after |
| --- | --- | --- | --- | --- |
| 1 | 3 | [] | new pile | [3] |
| 2 | 2 | [3] | replace 3 | [2] |
| 3 | 1 | [2] | replace 2 | [1] |

Final number of piles is 1.

This shows that a fully decreasing permutation fits into one stack because it directly matches the required push-order constraint.

### Example 2: permutation [1, 4, 2, 5, 3]

| Step | x | piles before | position chosen | piles after |
| --- | --- | --- | --- | --- |
| 1 | 1 | [] | new | [1] |
| 2 | 4 | [1] | new | [1, 4] |
| 3 | 2 | [1, 4] | replace 4 | [1, 2] |
| 4 | 5 | [1, 2] | new | [1, 2, 5] |
| 5 | 3 | [1, 2, 5] | replace 5 | [1, 2, 3] |

Final answer is 3.

This demonstrates how intermediate replacements preserve structure, preventing unnecessary creation of new stacks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | each element uses binary search on pile tops |
| Space | O(n) | storing pile tops in worst case |

The sum of n over all test cases is 5×10^5, so an O(n log n) solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    def solve():
        T = int(input())
        for _ in range(T):
            n = int(input())
            a = list(map(int, input().split()))
            piles = []
            for x in a:
                l, r = 0, len(piles)
                while l < r:
                    mid = (l + r) // 2
                    if piles[mid] > x:
                        r = mid
                    else:
                        l = mid + 1
                if l == len(piles):
                    piles.append(x)
                else:
                    piles[l] = x
            output.append(str(len(piles)))
        print("\n".join(output))

    solve()
    return "\n".join(output)

# provided samples (conceptual, since formatting was unclear)
assert run("1\n3\n3 2 1\n") == "1", "sample 1"

# all increasing requires n stacks
assert run("1\n4\n1 2 3 4\n") == "4", "strict increasing"

# alternating pattern
assert run("1\n5\n1 3 2 5 4\n") == "3", "mixed structure"

# already decreasing
assert run("1\n5\n5 4 3 2 1\n") == "1", "fully decreasing"

# single element
assert run("1\n1\n1\n") == "1", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 3 / 3 2 1 | 1 | fully decreasing fits one stack |
| 1 4 / 1 2 3 4 | 4 | worst-case increasing forces new stacks |
| 1 5 / 1 3 2 5 4 | 3 | non-trivial LIS structure |
| 1 1 / 1 | 1 | minimal input |

## Edge Cases

A fully decreasing permutation like [5, 4, 3, 2, 1] produces a single pile throughout. Every new element can replace the previous top, so no additional stack is ever created.

A fully increasing permutation like [1, 2, 3, 4] forces the algorithm to create a new pile at every step because no existing stack top is greater than the current element. This directly corresponds to needing n stacks, since no two elements can coexist in the same decreasing subsequence.

A mixed case such as [2, 1, 4, 3] shows how replacements avoid unnecessary stack creation. The element 1 replaces 2, and later 3 replaces 4, keeping the number of stacks minimal at 2, which matches the LIS structure of the sequence.
