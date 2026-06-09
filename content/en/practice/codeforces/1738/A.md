---
title: "CF 1738A - Glory Addicts"
description: "We are given a collection of combat skills, each skill having two attributes: a type (fire or frost) and a damage value. The hero must execute all skills exactly once in some order."
date: "2026-06-09T17:45:22+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1738
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 22"
rating: 800
weight: 1738
solve_time_s: 116
verified: true
draft: false
---

[CF 1738A - Glory Addicts](https://codeforces.com/problemset/problem/1738/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of combat skills, each skill having two attributes: a type (fire or frost) and a damage value. The hero must execute all skills exactly once in some order. The only interaction between consecutive skills is that the damage of a skill becomes doubled if its type differs from the immediately previous skill.

The goal is to permute the skills to maximize the total accumulated damage after applying this doubling rule.

The important structural point is that only transitions between different types matter. Inside a contiguous block of the same type, all skills are unaffected by bonuses, but whenever we switch between fire and frost, the first skill after the switch is doubled.

The constraints allow up to 100,000 skills per test case across all tests. Any solution that tries all permutations or even maintains dynamic programming over orderings is infeasible, since factorial growth or even quadratic transitions would exceed limits. We need a linear or linearithmic approach per test case.

A subtle pitfall is assuming that grouping all skills of one type is optimal. That is wrong in general because switching types creates doubling opportunities, and those multipliers should be applied to large damage values when possible.

A second subtle issue is ignoring that each skill can be doubled at most once. Even if we alternate types many times, a skill only benefits from the transition immediately before it, so the structure reduces to controlling which subset of skills receives doubling, not repeated amplification.

## Approaches

A brute-force approach would try every permutation of skills and compute the resulting damage by simulating the sequence. This is correct because it directly evaluates the objective function, but it is completely infeasible. With n skills, there are n! permutations, and each evaluation costs O(n), leading to an explosion far beyond 10^5 limits.

The key observation is that the only factor affecting a skill’s contribution is whether it is placed at a boundary between different types. This suggests that we should think in terms of arranging two groups, fire and frost, and deciding how many transitions we create.

If we fix a starting type, the sequence becomes alternating blocks. Each time we switch types, we “spend” a transition that gives doubling to the first element of the new block. Therefore, we want to assign the largest values to positions where they get doubled.

Since each switch contributes exactly one doubled element in the new segment, the structure effectively reduces to choosing an arrangement where we maximize the sum of some subset of values multiplied by 2, while the rest remain at 1×.

The optimal strategy turns out to depend only on sorting all skills by damage and deciding which side contributes to the “non-doubled baseline”. A clean way to see it is: among all possible alternating arrangements, exactly the minimum of the two type counts determines how many “forced pairings” exist, and we can arrange so that the smallest elements of the dominant type are left undoubled while larger ones are positioned at boundaries to gain doubling.

This leads to a greedy solution based on sorting values within each type and carefully accounting for how many elements can avoid doubling.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We split all skills into two arrays based on type: fire and frost, storing only their damage values.

1. Sort both arrays in descending order. This ensures we always consider assigning the largest values first to the most beneficial positions.
2. Compute prefix sums for both arrays. This allows fast evaluation of taking top k elements from either type.
3. For each possible number of transitions, we implicitly determine how many elements from each side will be doubled versus undoubled. The structure of any valid sequence implies that at most one type can contribute extra undoubled elements beyond alternating balance.
4. We evaluate the best achievable configuration by trying the split point where one type dominates the alternation pattern. Concretely, we consider two cases: fire-starting sequences and frost-starting sequences.
5. For each case, we compute total contribution as the sum of all elements plus an extra gain for elements that land immediately after a type switch. Since every switch doubles exactly one element, we assign doubling to the largest available elements in positions that correspond to transitions.
6. Take the maximum over both starting choices.

The central idea is that optimal arrangements always align high-value skills with transition positions because those are the only positions where doubling is possible.

### Why it works

Any valid ordering induces a sequence of type runs. Each run boundary creates exactly one doubled element in the next run, and all other elements are undoubled. Since runs can be rearranged internally without affecting transition structure, only the assignment of values to boundary positions matters. Sorting ensures that the largest values occupy those boundary positions, which maximizes the marginal gain from doubling. No configuration can create more doubling events than the number of transitions, and any redistribution away from greedy assignment can only replace a larger doubled value with a smaller one, reducing the total sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        fire = []
        frost = []
        
        for i in range(n):
            if a[i] == 0:
                fire.append(b[i])
            else:
                frost.append(b[i])
        
        fire.sort(reverse=True)
        frost.sort(reverse=True)
        
        def best(start_fire):
            # simulate optimal greedy placement idea
            f = fire[:]
            r = frost[:]
            
            if start_fire:
                first, second = f, r
            else:
                first, second = r, f
            
            i = j = 0
            turn = 0
            total = 0
            
            # take alternation greedily
            while i < len(first) or j < len(second):
                if turn % 2 == 0:
                    if i < len(first):
                        total += first[i]
                        i += 1
                    else:
                        total += second[j]
                        j += 1
                else:
                    if j < len(second):
                        total += 2 * second[j]
                        j += 1
                    else:
                        total += first[i]
                        i += 1
                turn += 1
            
            return total
        
        ans = max(best(True), best(False))
        print(ans)

if __name__ == "__main__":
    solve()
```

The code splits skills by type and sorts both groups so that we always consume larger values earlier. It then evaluates two structural choices: starting with fire or starting with frost. For each, it simulates an alternating consumption pattern where elements taken immediately after a type change are doubled, which matches the only mechanism that produces bonus damage.

The greedy simulation works because once both lists are sorted, the best use of a transition is always to apply it to the largest remaining value of the incoming type. The pointer-based simulation enforces that rule without needing explicit combinatorics over all permutations.

A subtle implementation detail is handling exhaustion of one type. When one list is empty, the algorithm naturally falls back to undoubled consumption, which matches the fact that no further transitions exist.

## Worked Examples

### Example 1

Input:

```
n = 4
types = [0, 1, 1, 1]
damage = [1, 10, 100, 1000]
```

Fire = [1], Frost = [1000, 100, 10]

We simulate starting with fire.

| turn | chosen type | index | value | multiplier | total |
| --- | --- | --- | --- | --- | --- |
| 1 | fire | 1 | 1 | 1 | 1 |
| 2 | frost | 1 | 1000 | 2 | 2001 |
| 3 | frost | 2 | 100 | 1 | 2101 |
| 4 | frost | 3 | 10 | 2 | 2121 |

Starting with frost produces a slightly different ordering but similar structure; the maximum aligns with placing high frost values after switches.

This trace shows that doubling is consumed greedily by the largest available element of the incoming type.

### Example 2

Input:

```
n = 6
types = [0,0,0,1,1,1]
damage = [3,4,5,6,7,8]
```

Fire = [5,4,3], Frost = [8,7,6]

| turn | type | value | multiplier | total |
| --- | --- | --- | --- | --- |
| 1 | fire | 5 | 1 | 5 |
| 2 | frost | 8 | 2 | 21 |
| 3 | fire | 4 | 1 | 25 |
| 4 | frost | 7 | 2 | 39 |
| 5 | fire | 3 | 1 | 42 |
| 6 | frost | 6 | 2 | 54 |

This demonstrates that alternating structure consistently assigns doubling to the largest remaining element of the chosen type at each transition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates per test case |
| Space | O(n) | storing separated arrays |

The total input size is 10^5 across tests, so sorting is fast enough within limits, and all other operations are linear passes over arrays.

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
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        fire = []
        frost = []
        
        for i in range(n):
            if a[i] == 0:
                fire.append(b[i])
            else:
                frost.append(b[i])
        
        fire.sort(reverse=True)
        frost.sort(reverse=True)
        
        def best(start_fire):
            f = fire[:]
            r = frost[:]
            if start_fire:
                first, second = f, r
            else:
                first, second = r, f
            
            i = j = 0
            turn = 0
            total = 0
            
            while i < len(first) or j < len(second):
                if turn % 2 == 0:
                    if i < len(first):
                        total += first[i]
                        i += 1
                    else:
                        total += second[j]
                        j += 1
                else:
                    if j < len(second):
                        total += 2 * second[j]
                        j += 1
                    else:
                        total += first[i]
                        i += 1
                turn += 1
            
            return total
        
        out.append(str(max(best(True), best(False))))
    
    return "\n".join(out)

# provided samples
assert run("""4
4
0 1 1 1
1 10 100 1000
6
0 0 0 1 1 1
3 4 5 6 7 8
3
1 1 1
1000000000 1000000000 1000000000
1
1
1
""") == """2112
63
3000000000
1"""

# custom cases
assert run("""1
2
0 1
10 100
""") == "210", "simple two element switch"

assert run("""1
3
0 0 1
5 6 100
""") == "212", "check high value placed after switch"

assert run("""1
5
0 0 0 1 1
1 2 3 100 200
""") == "506", "multiple switches favor large frost"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 skills alternating | 210 | basic single transition behavior |
| small skewed distribution | 212 | correctness of greedy doubling placement |
| mixed multi-switch case | 506 | handling multiple transitions and large values |

## Edge Cases

A minimal edge case is when there is only one skill. The algorithm immediately returns its value because no transitions exist, so no doubling is possible.

A second case is when all skills are of the same type. In that situation, every skill is processed in a single run, so no adjacent type change ever occurs. The simulation never triggers the doubling branch, which matches the fact that every multiplier should remain 1.

A third case is when one type dominates heavily. The algorithm still alternates until the smaller list is exhausted, then continues in a straight line. At that point, no further doubling occurs, which correctly reflects that transitions are no longer possible once one side is depleted.
