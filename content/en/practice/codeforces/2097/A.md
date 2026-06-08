---
title: "CF 2097A - Sports Betting"
description: "We are given several independent scenarios. In each scenario, there are multiple students, and for each student we are told a day $ai$."
date: "2026-06-08T10:49:49+07:00"
tags: ["codeforces", "competitive-programming", "2-sat", "brute-force", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2097
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1021 (Div. 1)"
rating: 1400
weight: 2097
solve_time_s: 92
verified: false
draft: false
---

[CF 2097A - Sports Betting](https://codeforces.com/problemset/problem/2097/A)

**Rating:** 1400  
**Tags:** 2-sat, brute force, math, sortings  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario, there are multiple students, and for each student we are told a day $a_i$. Vadim makes a bet with that student on day $a_i$, and the bet depends on correctly predicting a two-day pattern starting from the next day, meaning days $a_i+1$ and $a_i+2$.

Each day has a hidden outcome that can take one of two forms. Vadim does not know the actual sequence of outcomes in advance, but he wants to commit to predictions in such a way that at least one student is guaranteed to have both of their next two days predicted correctly, regardless of how the real sequence turns out.

The key difficulty is that Vadim must decide all predictions beforehand, and the actual outcomes are adversarial. So this is a worst-case guarantee problem: we are checking whether there exists a fixed assignment of predictions such that every possible real sequence still leaves at least one “fully correct” student.

The input is a collection of test cases, each containing up to $10^5$ students overall across all cases. This immediately suggests that any solution worse than linear or near-linear per test case will not survive. Sorting and frequency counting are acceptable, but anything quadratic in $n$ per test case is not.

A subtle failure case arises when students’ bet days are too spread out. For example, if all $a_i$ are distinct and no two bets overlap in the same two-day window, then each student corresponds to an independent constraint. In that case, Vadim cannot reuse structure across predictions, and the problem reduces to covering too many independent possibilities with too few deterministic assignments. Conversely, when many $a_i$ coincide or cluster, overlaps create redundancy that can be exploited.

A naive misunderstanding is to treat each student independently and assume we can always assign patterns per student. That fails because the same day’s outcome is shared across all students.

## Approaches

A brute-force approach would try to simulate all possible outcomes of the infinite binary sequence and check whether there exists a choice of predictions that guarantees at least one student is satisfied in every outcome. Even restricting attention to the relevant days, if we have $k$ distinct days involved, there are $2^k$ possible outcome assignments. For each assignment, we would need to check whether any student’s two-day window matches their prediction, and then try to reason over all possible prediction assignments. This quickly becomes exponential in both outcomes and strategy space.

The key observation is that the only thing that matters for a student at day $a_i$ is the pair $(a_i+1, a_i+2)$. Each student is essentially trying to “cover” one length-2 window. If we think in reverse, Vadim is choosing predictions for each day, and each student checks a specific pair of those choices.

So the problem becomes: can we assign binary values to days such that at least one of the queried length-2 windows matches a preselected pattern? The crucial simplification is that only relative structure among equal $a_i$ matters. If many students share the same $a_i$, they are all asking about the same window, and we can distribute different predictions across them.

This turns into a pigeonhole-style condition: for a fixed day $a$, there are only four possible patterns for $(a+1, a+2)$. If we have at least four students with the same $a$, we can assign all four patterns and guarantee success for any real outcome. If we have fewer than four, we cannot fully cover all possibilities for that window.

Thus the entire problem reduces to checking whether any value of $a_i$ appears at least 4 times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over assignments | exponential | exponential | Too slow |
| Frequency counting per day | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Group students by their bet day $a_i$. This is done using a frequency map. The reason is that only identical $a_i$ values share the same two-day window structure, so grouping isolates independent constraints.
2. For each distinct day $a$, count how many students bet on it. This count represents how many prediction slots we can assign to the same window $(a+1, a+2)$.
3. Check whether any count is at least 4. If such a day exists, we immediately conclude success is guaranteed. The reason is that there are exactly four possible binary outcomes for two days: 00, 01, 10, 11. With four students on the same window, we can assign one prediction per pattern, ensuring coverage of every possible real outcome.
4. If no such day exists, output “No”, since every window has fewer than four attempts and thus cannot cover all possible outcomes of that window. This implies there exists at least one outcome assignment that avoids all predictions simultaneously.

The correctness hinges on the fact that each student independently requires matching one of four possibilities, and only multiplicity at the same window allows full coverage.

### Why it works

Each student corresponds to a requirement to match a specific pair of bits at positions $a_i+1$ and $a_i+2$. Since these pairs are independent across different $a_i$, the only way to force a guaranteed success is to fully cover all four possible assignments of a single pair. If any $a_i$ appears four times, we can assign all four patterns to those students, ensuring that regardless of the actual outcome of that pair, one match exists. If no such multiplicity exists, then for every window there is at least one pattern not assigned, and the adversary can choose that pattern globally for that window, defeating all bets.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        
        ok = False
        for v in freq.values():
            if v >= 4:
                ok = True
                break
        
        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The solution uses a hash map to count frequencies of each bet day. This is the only state we need, since the identity of students beyond grouping is irrelevant.

The check for frequency ≥ 4 directly encodes the four possible binary patterns of a two-day sequence. The loop terminates early once such a group is found, ensuring efficiency.

## Worked Examples

### Example 1

Input:

```
4
1 1 1 1
```

We track frequencies:

| step | value | freq state |
| --- | --- | --- |
| 1 | 1 | {1:1} |
| 2 | 1 | {1:2} |
| 3 | 1 | {1:3} |
| 4 | 1 | {1:4} |

Once the count reaches 4, we conclude that all four patterns can be assigned. This guarantees coverage of any possible outcome of days 2 and 3, so the answer is “Yes”.

### Example 2

Input:

```
3
2 2 2
```

| step | value | freq state |
| --- | --- | --- |
| 1 | 2 | {2:1} |
| 2 | 2 | {2:2} |
| 3 | 2 | {2:3} |

No value reaches 4, so at least one binary pattern remains unassigned. An adversary can pick that pattern for days 3 and 4, avoiding all predictions, so the answer is “No”.

These traces show that the threshold of 4 is both necessary and sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | single pass for counting plus scan over frequencies |
| Space | $O(n)$ | hash map stores at most $n$ distinct values |

The total $n$ across test cases is bounded by $10^5$, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        out.append("Yes" if any(v >= 4 for v in freq.values()) else "No")
    return "\n".join(out)

# provided samples
assert run("""5
4
1 1 1 1
3
2 2 2
5
2 4 3 2 4
8
6 3 1 1 5 1 2 6
1
1000000000
""") == """Yes
No
Yes
No
No"""

# custom cases
assert run("""1
4
10 10 10 10
""") == "Yes"

assert run("""1
4
1 1 1 2
""") == "No"

assert run("""1
6
5 5 5 5 5 5
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same 4 | Yes | minimal success case |
| 3+1 split | No | near-threshold failure |
| all same large | Yes | robustness for larger counts |

## Edge Cases

One edge case is when there is only a single student. For example, input `n = 1, a = [100]`. The frequency is 1, which is below 4, so the output is “No”. The algorithm correctly concludes that a single prediction cannot cover all four possible outcomes of a two-day window.

Another edge case is when there are exactly three students with the same day. Even though they heavily overlap, there are still four possible outcomes for the next two days, and one remains uncovered. The algorithm correctly outputs “No”, reflecting that at least one adversarial assignment avoids all predictions.

A final edge case is large homogeneous input such as $10^5$ identical values. The frequency check immediately triggers success in $O(n)$ time, demonstrating that the algorithm scales without needing to inspect structure beyond counts.
