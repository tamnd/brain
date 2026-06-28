---
title: "CF 104772F - First Solved, Last Coded"
description: "We are given two sequences of length n that describe the same multiset of problem topics. The first sequence describes the order in which solutions become available, one by one, and each new solution is placed onto a stack."
date: "2026-06-28T15:40:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104772
codeforces_index: "F"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104772
solve_time_s: 64
verified: true
draft: false
---

[CF 104772F - First Solved, Last Coded](https://codeforces.com/problemset/problem/104772/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of length n that describe the same multiset of problem topics. The first sequence describes the order in which solutions become available, one by one, and each new solution is placed onto a stack. The second sequence describes the exact order in which these solutions must be taken from the stack and processed.

At each moment we either push the next available element from the first sequence onto the stack, or pop the top of the stack and output it as the next required element of the second sequence. The goal is to decide whether it is possible to perform a sequence of exactly n pushes and n pops so that the popped sequence matches the second array exactly, and if so, construct such a sequence of operations.

The constraint n ≤ 100 means any solution that is quadratic or even simple simulation with linear stack operations is easily fast enough. There is no need for advanced data structures or optimizations beyond a straightforward greedy simulation. The only subtlety is correctness under duplicates, since values are not distinct and the usual “stack permutation of 1 to n” intuition must be adapted carefully.

A naive attempt might try to backtrack over all possible interleavings of pushes and pops. That approach branches at every step, leading to an exponential number of states. Even for n = 100 this becomes completely infeasible.

A more subtle incorrect approach is to always push everything first and then try to pop in order. That clearly fails when the desired output requires early pops before later elements are pushed.

The key edge case pattern is when the next required output is deeper in the future input sequence, but a different element is currently blocking it on the stack. If we pop the wrong element early, we may permanently block the required order.

## Approaches

The brute force approach considers every sequence of S and C operations, maintaining the current stack and checking whether the produced output matches the target. Since each of the 2n positions can be either S or C with constraints, the number of valid sequences grows combinatorially. In the worst case this explores on the order of Catalan-number-like structures, which grows exponentially with n. This quickly becomes impossible even for n = 30.

The key observation is that the process has a strong greedy structure. Once an element is on the top of the stack and it matches the next required output, delaying its removal never helps. Any other choice would only bury it deeper and risk blocking future required elements. This implies that whenever the stack top matches the next needed element, we must pop immediately.

With that idea, the entire process becomes a single left-to-right scan of the input sequence, simulating pushes, while continuously popping whenever possible. This reduces the problem to maintaining a stack and a pointer into the target sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^{2n}) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We simulate the process using a stack, two pointers, and a result string.

1. Initialize an empty stack, and set a pointer j = 0 for the target sequence.
2. Iterate i from 0 to n − 1 over the source sequence. For each element, push it onto the stack and record an 'S' operation. The push is necessary because we can only access elements through the stack structure, and we must make the current source element available for potential future matches.
3. After each push, repeatedly check the top of the stack. While the stack is not empty and the top equals the current target element b[j], pop it from the stack, record a 'C', and increment j. This greedy removal ensures we never delay an available correct match, since delaying only adds blocking elements above it.
4. Continue this process until all source elements have been pushed.
5. After finishing all pushes, if we have successfully matched all elements in the target sequence (j == n), the recorded operations form a valid solution. Otherwise, it is impossible.

### Why it works

The invariant is that at any point in the simulation, the stack represents exactly the set of elements that have been pushed but not yet output, and their relative order is fixed by insertion time. Whenever the top of the stack matches the next required output, it is always safe and optimal to remove it immediately because leaving it would only postpone a valid match while potentially introducing new blocking elements above it. If the process ends with unmatched elements in the target sequence, it means some required element was never exposed at the top of the stack at the correct time, which cannot be fixed by reordering operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    stack = []
    res = []
    j = 0
    
    for x in a:
        stack.append(x)
        res.append('S')
        
        while stack and j < n and stack[-1] == b[j]:
            stack.pop()
            res.append('C')
            j += 1
    
    if j == n:
        print("YES")
        print("".join(res))
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. The stack stores all currently held solutions. After each push, the inner loop greedily removes any elements that immediately satisfy the next required output. The pointer j ensures we never skip or reorder the target sequence. The final check ensures all required outputs were produced; otherwise, some element was blocked permanently by stack ordering.

A subtle point is that duplicates are handled naturally. Since matching is done by value and not by identity, multiple identical values are treated interchangeably, and the greedy rule still holds because correctness depends only on stack order, not on uniqueness.

## Worked Examples

### Example 1

Input:

n = 4

a = [4, 1, 2, 2]

b = [1, 2, 4, 2]

| Step | Action | Stack | j | Output |
| --- | --- | --- | --- | --- |
| 1 | Push 4 | [4] | 0 | S |
| 2 | Push 1 | [4,1] | 0 | SS |
| 3 | Pop 1 | [4] | 1 | SSC |
| 4 | Push 2 | [4,2] | 1 | SSCS |
| 5 | Pop 2 | [4] | 2 | SSCSC |
| 6 | Push 2 | [4,2] | 2 | SSCSCS |
| 7 | Pop 2 | [4] | 3 | SSCSCSC |
| 8 | Pop 4 | [] | 4 | SSCSCCSC |

This trace shows how immediate popping whenever the top matches the target ensures no unnecessary blocking occurs. Every time a match appears, it is resolved instantly.

### Example 2

Input:

n = 3

a = [2, 3, 1]

b = [1, 2, 3]

We push 2 (stack [2]), push 3 (stack [2,3]), and then must eventually output 1. However, 1 never appears on top of the stack at the right time; it arrives too late after 2 and 3 are already blocking it. The process ends with stack [2,3,1], but we cannot pop 1 before 3 and 2, making the required order impossible.

This demonstrates that even though both sequences contain the same multiset, stack constraints can make ordering infeasible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is pushed once and popped at most once |
| Space | O(n) | Stack holds at most n elements |

The linear complexity is easily sufficient for n ≤ 100. The algorithm performs a constant amount of work per element, and no nested search or backtracking is involved.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n = int(input().strip())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    stack = []
    res = []
    j = 0
    
    for x in a:
        stack.append(x)
        res.append('S')
        while stack and j < n and stack[-1] == b[j]:
            stack.pop()
            res.append('C')
            j += 1
    
    if j == n:
        return "YES\n" + "".join(res)
    return "NO"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("""4
4 1 2 2
1 2 4 2
""") == "YES\nSSCSCCSC"

assert run("""3
2 3 1
1 2 3
""") == "NO"

# custom cases
assert run("""1
1
1
""") == "YES\nSC"

assert run("""2
1 2
2 1
""") == "YES\nSSCC"

assert run("""3
1 1 1
1 1 1
""") == "YES\nSCSC SC".replace(" ", "")

assert run("""4
1 2 3 4
4 3 2 1
""") == "YES\nSSSSCCCC"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element identical | SC | Minimum size correctness |
| 1 2 → 2 1 | SSCC | Basic reversal stack behavior |
| all ones | SCSC… | Handling duplicates |
| reversed sequence | SSSSCCCC | Extreme stack depth |

## Edge Cases

A subtle edge case arises when many identical values appear. The algorithm still behaves correctly because equality comparison does not depend on position, and every occurrence is indistinguishable in terms of feasibility. The stack structure alone determines correctness.

Another case is when the target sequence requires an element before it is pushed. In that situation, the greedy simulation will push everything until it either becomes accessible at the top or remain blocked. If it never reaches the correct position at the top, the final pointer j will not reach n, correctly signaling impossibility.
