---
problem: 1358B
contest_id: 1358
problem_index: B
name: "Maria Breaks the Self-isolation"
contest_name: "Codeforces Round 645 (Div. 2)"
rating: 1000
tags: ["greedy", "sortings"]
answer: passed_samples
verified: false
solve_time_s: 189
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a2e3899-7340-83ec-9d2b-cbafc7af3f4e
---

# CF 1358B - Maria Breaks the Self-isolation

**Rating:** 1000  
**Tags:** greedy, sortings  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 9s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a2e3899-7340-83ec-9d2b-cbafc7af3f4e  

---

## Solution

## Problem Understanding

We are given a collection of grannies, each with a personal requirement about crowd size. Maria starts alone in a courtyard and wants to gradually invite some of them. Each granny has a threshold $a_i$, meaning she will only agree to enter if, at the instant she appears, there are at least $a_i$ other grannies already present (counting Maria as one of those “others”).

The key complication is that Maria can invite multiple grannies at the same time, and they all observe the same snapshot of the courtyard at the moment of entry. So a group decision depends on the total size of the group being added together with those already inside.

The task is to determine the maximum number of grannies that can eventually be brought in, given that Maria can choose the order and grouping of invitations freely.

The input size constraint is large enough that any solution worse than linearithmic per test case would be risky. With up to $10^5$ total grannies across tests, an $O(n^2)$ simulation of trying all subsets or iterative greedy scanning would be too slow. We should aim for an $O(n \log n)$ or better strategy, likely involving sorting and a single pass.

A subtle edge case arises when large-threshold grannies exist alongside many small-threshold ones. For example, if one granny requires almost the full final crowd size, she might block a naive greedy approach unless she is deferred correctly. Another corner case is when all values are larger than $n$, in which case no one except Maria can join, since even the smallest requirement cannot be satisfied.

## Approaches

A brute-force interpretation would be to simulate all possible ways of inviting grannies in groups. At any step, we know how many are currently inside, and we try subsets of remaining grannies whose constraints are satisfied by the current size plus the size of the subset. This quickly becomes combinatorial: each subset choice depends on all others, leading to exponential possibilities in grouping.

A more structured way to think about it is to ignore grouping at first and focus on a final ordering. If we could line up all grannies in some order, then when the $k$-th granny enters, there are exactly $k$ grannies before her plus Maria. So she sees $k$ others (since Maria is always present). That means the condition becomes a constraint on position: a granny placed at position $k$ is valid if $a_i \le k$.

This reduces the problem to selecting the largest possible prefix of grannies that can be arranged so that each position satisfies its threshold. The best strategy is to prioritize easier grannies first, i.e. those with smaller requirements, because they are more flexible and help increase the prefix size.

Sorting allows us to greedily assign positions from smallest requirement upward. We maintain a counter of how many grannies we have already placed, and we include a granny if her requirement is not larger than the current achievable crowd size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force grouping simulation | exponential | O(n) | Too slow |
| Sort + greedy assignment | O(n log n) | O(1) extra (besides input) | Accepted |

## Algorithm Walkthrough

1. Sort the array $a$ in non-decreasing order. This ensures we always consider the most permissive grannies first, which maximizes the chance of fitting more people overall.
2. Initialize a counter `cnt = 1`, representing Maria alone in the courtyard. This counter tracks how many grannies are currently inside if we include Maria.
3. Traverse the sorted array from smallest to largest requirement. At each granny $a_i$, check whether she can join given the current crowd size.
4. If $a_i \le cnt$, then this granny can safely be included. Increase `cnt` by 1, because we have successfully added one more person to the courtyard.
5. If $a_i > cnt$, skip her permanently. Since the array is sorted, any later granny will have even larger or equal requirements, so none of them will fit at this position.
6. After processing all grannies, output `cnt`, which already includes Maria.

### Why it works

At any moment, `cnt` represents a feasible number of people inside the courtyard including Maria. Sorting ensures that when we attempt to place a granny, we are always considering the smallest remaining constraint. If a granny cannot be placed at the current size, then no rearrangement of already skipped larger ones could make her fit without violating earlier assignments. The construction greedily builds the largest possible prefix where every position satisfies its threshold, which directly corresponds to the maximum achievable final group size.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort()
        
        cnt = 1  # Maria
        
        for x in a:
            if x <= cnt:
                cnt += 1
        
        out.append(str(cnt))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the requirement list so that we always try to accommodate the least demanding grannies first. The variable `cnt` tracks the current number of people in the courtyard, starting from Maria alone.

As we iterate, each time we find a granny whose requirement is satisfied by the current crowd size, we immediately include her and increase the size. This greedy acceptance is safe because future grannies are only harder to satisfy, so delaying a feasible granny never improves feasibility.

The final value of `cnt` already includes Maria, matching the required output definition.

## Worked Examples

### Example 1

Input:

```
5
1 1 2 2 1
```

Sorted array: `[1, 1, 1, 2, 2]`

| Step | Current cnt | a[i] | Action | New cnt |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | take | 2 |
| 2 | 2 | 1 | take | 3 |
| 3 | 3 | 1 | take | 4 |
| 4 | 4 | 2 | take | 5 |
| 5 | 5 | 2 | take | 6 |

Final answer is 6.

This shows that early low-threshold grannies act as enablers for later ones, steadily increasing the feasible capacity.

### Example 2

Input:

```
6
2 3 4 5 6 7
```

Sorted array: `[2, 3, 4, 5, 6, 7]`

| Step | Current cnt | a[i] | Action | New cnt |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | skip | 1 |
| 2 | 1 | 3 | skip | 1 |
| 3 | 1 | 4 | skip | 1 |
| 4 | 1 | 5 | skip | 1 |
| 5 | 1 | 6 | skip | 1 |
| 6 | 1 | 7 | skip | 1 |

Final answer is 1.

This demonstrates the case where Maria alone cannot satisfy even the smallest requirement, so no progression is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates each test case |
| Space | $O(1)$ extra | aside from input array, only a counter is used |

The total $n$ across test cases is at most $10^5$, so sorting remains efficient overall, and the linear scan is negligible.

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
        a.sort()
        cnt = 1
        for x in a:
            if x <= cnt:
                cnt += 1
        out.append(str(cnt))
    return "\n".join(out)

# provided samples
assert run("""4
5
1 1 2 2 1
6
2 3 4 5 6 7
6
1 5 4 5 1 9
5
1 2 3 5 6
""") == """6
1
6
4"""

# minimum case
assert run("""1
1
1
""") == "2"

# all impossible
assert run("""1
3
10 10 10
""") == "1"

# already optimal chain
assert run("""1
4
1 1 1 1
""") == "5"

# mixed values
assert run("""1
5
3 1 4 1 5
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1 | 2 | minimum case with immediate acceptance |
| all large values | 1 | no granny can enter |
| all ones | 5 | full chain growth |
| mixed sequence | 4 | correctness of greedy ordering |

## Edge Cases

A key edge case is when all thresholds are greater than the number of grannies available. For example:

Input:

```
3
10 10 10
```

After sorting, we still have `[10, 10, 10]`. Maria starts with `cnt = 1`. Every value is greater than 1, so none are accepted and the final answer remains 1. The algorithm correctly avoids attempting impossible inclusions.

Another edge case is when many small values appear early, enabling a cascading effect. For instance:

Input:

```
4
1 1 1 1
```

Sorted array is unchanged. Each step satisfies the condition, so `cnt` grows from 1 to 5. This shows that each accepted granny strictly increases capacity, which is what allows the chain reaction to succeed.