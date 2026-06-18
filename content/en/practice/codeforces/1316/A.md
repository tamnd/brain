---
problem: 1316A
contest_id: 1316
problem_index: A
name: "Grade Allocation"
contest_name: "CodeCraft-20 (Div. 2)"
rating: 800
tags: ["implementation"]
answer: passed_samples
verified: true
solve_time_s: 132
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2de51d-4028-83ec-b74f-af94b6e7b900
---

# CF 1316A - Grade Allocation

**Rating:** 800  
**Tags:** implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 12s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2de51d-4028-83ec-b74f-af94b6e7b900  

---

## Solution

## Problem Understanding

We are given a classroom where every student has an integer exam score bounded between zero and some maximum value. The school allows us to freely rewrite all scores, but we must preserve the total sum of scores, since keeping the average unchanged is equivalent to keeping the sum unchanged.

Our goal is focused only on student 1. We want to assign this student the largest possible score after redistribution, while still being able to assign valid integer scores to everyone else, each staying within the range from 0 to m, and keeping the overall sum fixed.

So the problem reduces to a redistribution task: we take a fixed amount of “score mass” equal to the original total sum, and we want to concentrate as much of it as possible into the first position, without exceeding the per-student upper bound m.

The constraints are small enough that even a quadratic or greedy linear scan per test case would pass comfortably. With at most 1000 students per test case and 200 test cases, even O(n^2) would be borderline acceptable, while O(n) or O(n log n) is trivial. This already suggests that the solution should not involve complex optimization structures or search.

A subtle edge case arises when the first student is already close to m but the rest of the array is so small that redistribution could in theory push it higher. However, the hard cap m blocks any such attempt. Another edge case is when all students already have equal scores; in that case, no redistribution changes anything, and the answer is simply m only if total sum permits concentrating everything into one student.

A common incorrect intuition is to think we can always set student 1 to m. This fails when the total sum is too small. For example, if n = 4, m = 10, and the sum is 6, we cannot assign 10 to any single student because we would need at least 10 total units of score mass.

## Approaches

The brute-force way to think about this problem is to simulate redistribution. We try increasing the score of student 1 step by step and check whether the remaining total sum can be distributed among the other students without exceeding m or going below zero. For each candidate value x for student 1, we check feasibility by verifying whether the remaining sum S - x can be split into n - 1 values each between 0 and m. This is correct but inefficient if implemented naively, because for each candidate x we might scan or recompute feasibility conditions repeatedly.

The key observation is that the only real constraints are global: the sum is fixed, and each individual value is independently bounded. There is no coupling between students beyond the sum constraint. That means feasibility is determined entirely by whether the remaining sum fits into the capacity of the other n - 1 students.

Each of those students can hold at most m, so their total capacity is (n - 1) * m. That gives a simple feasibility condition. If we assign x to student 1, the remaining sum S - x must satisfy 0 ≤ S - x ≤ (n - 1) * m. This transforms the problem into a direct inequality bound on x.

We are therefore maximizing x under two constraints: it cannot exceed m, and it cannot exceed S minus the minimum required space for others. Since the others can take at most (n - 1) * m, the maximum feasible x is simply S - 0, but clamped so that the rest still fits.

The final result becomes a direct computation rather than a search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Redistribution | O(n * m) or worse | O(n) | Too slow / unnecessary |
| Optimal Sum-Based Bound | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum S of all student scores. This sum is fixed because redistribution preserves the average.
2. Recognize that after assigning a value x to student 1, the remaining sum becomes S - x.
3. The remaining n - 1 students each can hold at most m, so their total storage capacity is (n - 1) * m.
4. For a choice of x to be valid, the remaining sum must satisfy S - x ≤ (n - 1) * m. Rearranging gives x ≥ S - (n - 1) * m.
5. Also enforce that x cannot exceed m, since each individual score is capped.
6. Since we want the maximum possible x, we take x = min(m, S), but ensure feasibility with others is already satisfied because S - x automatically fits within remaining capacity when x is chosen as large as possible under the cap.

### Why it works

The key invariant is that feasibility depends only on total remaining capacity, not on distribution among individual students. Once student 1 is fixed to x, the rest of the problem reduces to checking whether (n - 1) slots with capacity m can absorb exactly S - x units. Since those slots are independent and identical in capacity, any leftover within range can always be distributed greedily without violating bounds. This removes any need for structured assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    s = sum(a)
    
    # maximum possible for student 1 is bounded by:
    # 1) cannot exceed m
    # 2) cannot exceed total sum (we must leave non-negative for others)
    print(min(m, s))
```

After reading the input, we compute the total sum of all scores. The answer is then constrained by two independent limits: student 1 cannot exceed m, and cannot exceed the total available sum S. Any remaining sum is always assignable to the other n - 1 students because their combined capacity is at least S - m when x is chosen optimally, and the bounds ensure no violation occurs.

The implementation avoids any simulation or redistribution logic. The correctness comes entirely from reducing the problem to a global capacity argument.

## Worked Examples

### Example 1

Input:

n = 4, m = 10

a = [1, 2, 3, 4]

Total sum S = 10

We compute x = min(10, 10) = 10.

| Step | S | m | x |
| --- | --- | --- | --- |
| compute sum | 10 | 10 | - |
| apply bound | 10 | 10 | 10 |

The remaining sum becomes 0, which trivially fits into 3 students. This confirms that full concentration is possible.

### Example 2

Input:

n = 4, m = 5

a = [1, 2, 3, 4]

Total sum S = 10

We compute x = min(5, 10) = 5.

| Step | S | m | x |
| --- | --- | --- | --- |
| compute sum | 10 | 5 | - |
| apply bound | 10 | 5 | 5 |

The remaining sum is 5, and three students can easily absorb it since their total capacity is 15.

This shows that the cap m is the active constraint here rather than the total sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | summing the array dominates |
| Space | O(1) extra | only a running sum is stored |

The constraints allow up to 200k total elements across all tests, so a single linear scan per test case is easily fast enough within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        out.append(str(min(m, sum(a))))
    return "\n".join(out)

# provided samples
assert run("""2
4 10
1 2 3 4
4 5
1 2 3 4
""") == "10\n5"

# minimum case
assert run("""1
1 100
42
""") == "42"

# all equal small values
assert run("""1
5 10
2 2 2 2 2
""") == "10"

# max cap dominates
assert run("""1
3 5
10 10 10
""") == "5"

# tight sum case
assert run("""1
4 3
1 1 1 1
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single student | 42 | n = 1 edge case |
| equal values | 10 | redistribution neutrality |
| large values capped | 5 | m constraint dominance |
| tight sum | 3 | sum-limited scenario |

## Edge Cases

When n = 1, there are no other students to distribute to, so the only constraint is the maximum allowed score m. The algorithm computes min(m, S), and since S equals a1, the result correctly becomes a1, which is the only feasible assignment.

When all students already have values equal to m, the sum is n * m. The formula returns min(m, n * m) = m, which matches the fact that student 1 cannot exceed the per-student cap even though total mass is large enough.

When the total sum is smaller than m, the answer becomes exactly the sum. This corresponds to concentrating all available score mass into student 1 while setting all others to zero, which remains valid because zero is within bounds.

Each of these cases shows that the solution depends only on global capacity and not on individual rearrangements, confirming that no hidden structure affects the result.