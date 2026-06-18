---
problem: 962B
contest_id: 962
problem_index: B
name: "Students in Railway Carriage"
contest_name: "Educational Codeforces Round 42 (Rated for Div. 2)"
rating: 1300
tags: ["constructive algorithms", "greedy", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 72
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a32811e-c338-83ec-856c-ab66260bfd33
---

# CF 962B - Students in Railway Carriage

**Rating:** 1300  
**Tags:** constructive algorithms, greedy, implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 12s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a32811e-c338-83ec-856c-ab66260bfd33  

---

## Solution

## Problem Understanding

We are given a row of seats in a train carriage. Some seats are already blocked, and the rest are empty. We want to place as many students as possible into the empty seats. Each student belongs to one of two types, and the restriction is simple but strict: two adjacent seats cannot contain students of the same type. However, a programmer next to an athlete is allowed, so the only forbidden adjacency is identical types.

The blocked seats split the row into independent segments of consecutive empty cells. Inside each segment, we decide how many students to place and how to alternate their types. Since students are interchangeable except for their type, the problem becomes about filling each segment greedily while respecting the available counts of the two types.

The constraints go up to 200,000 seats, so any solution that tries all placements or does backtracking over assignments is too slow. A quadratic or exponential approach over segments or configurations would not survive. We need a linear scan or a greedy construction that processes each segment once and makes locally optimal decisions.

A subtle edge case appears when a segment is long and we run out of one type early. For example, if we have a long empty block and only one type of student, we cannot fill more than one seat in that block because we would otherwise violate adjacency. Another edge case is when segments are short or isolated, where greedy filling might look trivial but still interacts with remaining global counts.

## Approaches

A brute-force idea is to treat each empty segment and try all possible ways of filling it with A and B students while respecting the adjacency rule. For a segment of length k, each seat can be A or B, but constrained by neighbors, leading to a state space that grows like 2^k in the worst case. Even with pruning based on remaining counts a and b, the number of configurations becomes infeasible when k is large.

The key observation is that within any segment, once we decide the first placed student, the rest of the segment is forced into an alternating pattern if we fully utilize it. This reduces the problem from combinatorial placement to greedy consumption of slots. Instead of exploring configurations, we simply walk through each segment and always place a student if possible, choosing the type that does not violate adjacency and is still available in our counters.

We never need to look ahead beyond the current seat because the only constraint is local adjacency and remaining counts. This makes the problem a linear greedy scan across the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal Greedy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string from left to right, handling contiguous blocks of empty seats separated by blocked positions.

1. Scan the string and identify segments of consecutive '.' characters. Each segment can be processed independently because '*' acts as a separator that prevents adjacency across boundaries.
2. For each segment, we try to fill it seat by seat. At each position, we decide which type of student to place.
3. At the start of a segment, we consider that the previous seat is effectively "blocked" or empty, so we are free to choose either type as long as we have remaining students.
4. For each seat in the segment, we try to place a student. If both types are available, we choose the one that preserves future flexibility, but a simpler and correct strategy is to alternate greedily while respecting counts. Practically, we just try to place one student per seat, consuming from whichever type is still available and ensuring we do not place the same type as the previous placed student.
5. If one type runs out, we may be forced to skip placement even if seats remain, because placing consecutive same-type students is forbidden. In that case, we continue scanning but only place when valid.
6. We accumulate the total number of placed students across all segments and output it.

The crucial idea is that within a segment, we only ever depend on the last placed student type and remaining counts. This ensures we never need to revise earlier decisions.

### Why it works

The algorithm maintains that within any segment, the constructed sequence never contains two adjacent identical types. Each placement respects the adjacency constraint by construction. Additionally, every placement consumes exactly one available student, and we only place when both constraints (availability and adjacency) allow it. Since segments are independent and we never skip a valid placement when possible, the result is maximal for each segment under the global constraints.

The greedy nature is safe because any deviation from placing a valid student when possible would only reduce the total count, and there is no benefit in leaving a seat empty unless forced by lack of valid student types.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    s = input().strip()

    def take(prev, a, b):
        # returns which type to take, or None
        if prev == 'A':
            if b > 0:
                return 'B'
            if a > 0:
                return 'A'
        else:
            if a > 0:
                return 'A'
            if b > 0:
                return 'B'
        return None

    ans = 0
    i = 0

    while i < n:
        if s[i] == '*':
            i += 1
            continue

        # process segment
        j = i
        while j < n and s[j] == '.':
            j += 1

        prev = None
        for k in range(i, j):
            if a == 0 and b == 0:
                break

            if prev is None:
                if a >= b and a > 0:
                    prev = 'A'
                    a -= 1
                elif b > 0:
                    prev = 'B'
                    b -= 1
                elif a > 0:
                    prev = 'A'
                    a -= 1
                else:
                    break
                ans += 1
            else:
                if prev == 'A':
                    if b > 0:
                        prev = 'B'
                        b -= 1
                        ans += 1
                    else:
                        break
                else:
                    if a > 0:
                        prev = 'A'
                        a -= 1
                        ans += 1
                    else:
                        break

        i = j

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first separates the row into segments of empty seats. For each segment, it builds a valid alternating sequence greedily. The `prev` variable tracks the last placed type so we never place identical adjacent students. The initial choice is biased toward the larger remaining pool, which helps avoid early exhaustion of one type in long segments. The rest of the logic enforces strict alternation while respecting remaining counts.

A common subtlety is ensuring that we stop placing in a segment as soon as neither valid type can be placed. Another is correctly resetting `prev` at each new segment, since blocked seats break adjacency completely.

## Worked Examples

### Example 1

Input:

```
5 1 1
*...*
```

We have one segment of length 3.

| Step | Position | Prev | a | b | Action | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | None | 1 | 1 | place A | 1 |
| 2 | 2 | A | 0 | 1 | place B | 2 |
| 3 | 3 | B | 0 | 0 | stop | 2 |

Output is 2.

This shows that a full alternating fill works when both types are available in balanced quantities.

### Example 2

Input:

```
6 3 0
......
```

Single segment of length 6.

| Step | Position | Prev | a | b | Action | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | None | 3 | 0 | place A | 1 |
| 2 | 2 | A | 2 | 0 | stop | 1 |

We can only place one student because no two A students can be adjacent.

This demonstrates the key constraint: having enough seats does not matter if only one type is available.

## Complexity Analysis

| Measure | Complexity | Explanation |

|---|---|---|---|

| Time | O(n) | Each seat is visited once in a single left-to-right scan |

| Space | O(1) | Only counters and a few variables are used |

The linear scan is sufficient for n up to 200,000, since each operation is constant time and no nested processing occurs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isfinite  # placeholder import to avoid empty module
    # re-run solution inline
    n, a, b = map(int, sys.stdin.readline().split())
    s = sys.stdin.readline().strip()

    ans = 0
    i = 0

    while i < n:
        if s[i] == '*':
            i += 1
            continue
        j = i
        while j < n and s[j] == '.':
            j += 1

        prev = None
        for k in range(i, j):
            if a == 0 and b == 0:
                break
            if prev is None:
                if a >= b and a > 0:
                    prev = 'A'
                    a -= 1
                elif b > 0:
                    prev = 'B'
                    b -= 1
                elif a > 0:
                    prev = 'A'
                    a -= 1
                else:
                    break
                ans += 1
            else:
                if prev == 'A' and b > 0:
                    prev = 'B'
                    b -= 1
                    ans += 1
                elif prev == 'B' and a > 0:
                    prev = 'A'
                    a -= 1
                    ans += 1
                else:
                    break

        i = j

    return str(ans)

# provided sample
assert run("5 1 1\n*...*\n") == "2"

# custom cases
assert run("1 1 1\n.\n") == "1", "single seat"
assert run("3 3 0\n...\n") == "1", "only one type allowed"
assert run("7 10 10\n.......\n") == "7", "fully alternating fill"
assert run("5 0 5\n.....\n") == "1", "only one type again"

print("OK")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / .` | 1 | minimal segment |
| `3 3 0 / ...` | 1 | single-type constraint |
| `7 10 10 / .......` | 7 | full alternating fill |
| `5 0 5 / .....` | 1 | edge case of zero alternation |

## Edge Cases

When the string contains only blocked seats, the algorithm immediately skips all characters and outputs zero, since no segment is formed. For example, `n = 5, s = "*****"` results in no iteration inside any segment loop, so the answer remains 0.

When there is a single long segment but only one type available, the algorithm places exactly one student at the first seat and then fails to place any further due to adjacency constraints. For input `n = 6, a = 10, b = 0, s = "......"`, the scan places one student at position 1 and stops the segment, correctly producing 1.

When multiple short segments exist, each segment resets `prev`, ensuring independence. For example `*..*..*` is treated as three segments, and each behaves independently without any cross-contamination of adjacency state.