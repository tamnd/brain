---
title: "CF 102348L - Printer"
description: "We have two rows of n tables, one row for each floor. A 1 at position i means a team occupies that table, while 0 means the table is free. The printer may be installed on any table, including an occupied one. Suppose the printer is at position p on one chosen floor."
date: "2026-08-13T01:13:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "L"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 197
verified: true
draft: false
---

[CF 102348L - Printer](https://codeforces.com/problemset/problem/102348/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two rows of `n` tables, one row for each floor. A `1` at position `i` means a team occupies that table, while `0` means the table is free. The printer may be installed on any table, including an occupied one.

Suppose the printer is at position `p` on one chosen floor. A team on that same floor only walks horizontally, so its inconvenience is `|i - p|`. A team on the other floor must first walk from its table to the staircase, spend `k` time changing floors, and then walk to the printer, giving inconvenience `i + k + p`.

The task is to choose both the floor and the table for the printer so that the largest inconvenience of any participating team is as small as possible. We output that minimum value and one printer position achieving it.

The value `n` is at most `1000`, so even a quadratic algorithm performs only about one million iterations per floor. With two possible printer floors, a completely direct enumeration of all printer positions and all teams performs at most `4n² = 4,000,000` team-position evaluations. That is already small enough for these constraints, although it is unnecessary work. The structure of the inconvenience formula lets us reduce the computation to linear time.

The most common implementation errors come from empty floors and from confusing the input order with the floor numbers. The second input string describes floor 2, while the third describes floor 1. For example, with

```
1 1
1
0
```

the only team is on floor 2, so placing the printer at floor 2, table 1 gives answer `0`, not `3`. A careless implementation that assumes both floors contain a team may incorrectly add the cross-floor cost.

Another boundary case is a team at the last table. For

```
4 2
0001
0001
```

placing the printer on floor 1 at table 1 gives maximum inconvenience `4 + 2 + 1 = 7`, and this is optimal. The term for the other floor uses the largest occupied index, not the smallest one, because `i + k + p` increases with `i`. Using the wrong extreme would underestimate the answer.

A third case is when all tables on the chosen floor are occupied. For

```
5 3
11111
11111
```

if the printer is on floor 1 at table 1, the opposite floor contributes `5 + 3 + 1 = 9`. The fact that the chosen floor also has teams does not change the cross-floor expression. Treating the two floors symmetrically inside the same formula would give an incorrect result.

Finally, a printer is allowed on a free table. For

```
5 7
00000
10001
```

the best printer position is floor 1, table 3, giving maximum same-floor distance `2`. Restricting the printer to occupied tables would miss the optimum.

## Approaches

The most direct solution tries every possible printer position. There are `2n` choices because the printer can be put on any table of either floor. For each choice, we inspect every occupied table, compute its inconvenience using either the same-floor or cross-floor formula, and keep the maximum. This is correct because every legal printer placement is explicitly considered, and every team's contribution is evaluated exactly.

The cost is `O(n²)`. In the worst case there are `2n` printer positions and up to `2n` occupied teams, giving `4n²` evaluations. At `n = 1000`, that is at most four million evaluations, so this brute-force method is actually feasible under the stated constraints, especially in C++. It is nevertheless useful to derive the linear solution because the same reasoning becomes necessary if the number of tables is increased.

The key observation is that once the printer floor is fixed, we do not need every team's position. For teams on the printer's floor, the largest value of `|i - p|` is determined entirely by the leftmost and rightmost occupied tables. If those positions are `L` and `R`, the same-floor contribution is

`max(p - L, R - p)`.

For teams on the opposite floor, the expression is `i + k + p`, which grows as `i` grows. Consequently, only the rightmost occupied table on the opposite floor matters. If that position is `M`, the entire opposite floor contributes

`M + k + p`.

So for a fixed printer floor and position `p`, the whole set of teams collapses to at most three numbers: the leftmost and rightmost occupied positions on the chosen floor, and the rightmost occupied position on the other floor.

We can obtain these extrema by scanning each input string once. After that, every possible printer position can be evaluated in constant time. There are only `2n` positions, so the total running time is `O(n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted for `n <= 1000`, but unnecessarily expensive |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two floor descriptions and remember that the second input string represents floor 2, while the third represents floor 1. This mapping must be preserved when printing the answer.
2. For each floor, find its leftmost occupied table, rightmost occupied table, and rightmost occupied table in general. The first two are needed when the printer is on that floor. The rightmost position is needed when that floor is the opposite floor.
3. Consider putting the printer on floor 1 at table `p`. If floor 1 contains teams, their maximum inconvenience is `max(p - L1, R1 - p)`. If floor 1 is empty, this contribution is zero because there are no teams to consider.
4. Teams on floor 2 are all reached through the staircase. Their inconvenience is `i + k + p`, and this is largest for the rightmost team on floor 2. Thus their contribution is `R2 + k + p` if floor 2 is nonempty, and zero otherwise.
5. Take the maximum of those two contributions. This gives the exact maximum inconvenience for printer position `(1, p)`.
6. Repeat the same calculation for every `p` from `1` through `n` on floor 2. When the printer is on floor 2, the same-floor term uses the extrema of floor 2, while the cross-floor term uses the rightmost team on floor 1.
7. Maintain the best maximum inconvenience seen so far. Update the stored answer only when the new value is strictly smaller. Since any optimal placement is acceptable, keeping the first placement that reaches the minimum is sufficient.
8. Print the best inconvenience followed by its floor and table number. All positions are maintained as one-based indices, matching the problem's numbering.

### Why it works

For a fixed printer floor, every same-floor team contributes a distance to `p`. Among all such teams, the maximum distance must come from one of the two extreme occupied tables, so the entire same-floor set is represented exactly by its minimum and maximum positions. Every opposite-floor team contributes `i + k + p`, which is strictly increasing in `i`, so only the rightmost opposite-floor team can determine the maximum. Hence the formula evaluated for each candidate printer position is exactly its true maximum inconvenience. Since the algorithm evaluates every possible floor and every possible table, the smallest value it records is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    floor2 = input().strip()
    floor1 = input().strip()

    floors = [floor1, floor2]

    # For each floor:
    # left[i]  = leftmost occupied table, or 0 if empty
    # right[i] = rightmost occupied table, or 0 if empty
    left = [0, 0]
    right = [0, 0]

    for f in range(2):
        for pos, ch in enumerate(floors[f], 1):
            if ch == '1':
                if left[f] == 0:
                    left[f] = pos
                right[f] = pos

    best_value = 10**18
    best_floor = 1
    best_pos = 1

    for f in range(2):
        other = 1 - f

        for p in range(1, n + 1):
            same = 0
            if right[f] != 0:
                same = max(p - left[f], right[f] - p)

            other_floor = 0
            if right[other] != 0:
                other_floor = right[other] + k + p

            cur = max(same, other_floor)

            if cur < best_value:
                best_value = cur
                best_floor = f + 1
                best_pos = p

    print(best_value)
    print(best_floor, best_pos)

if __name__ == "__main__":
    solve()
```

The two input strings are reordered into `floors = [floor1, floor2]` so that index `0` corresponds to output floor 1 and index `1` corresponds to output floor 2. This avoids repeatedly remembering that the input itself lists floor 2 first.

The first scan records the leftmost and rightmost occupied tables. When a `1` is encountered for the first time, it becomes `left[f]`; every occupied position is assigned to `right[f]`, so after the scan `right[f]` is automatically the last occupied table.

The value `0` is used to represent an empty floor. Since all real table indices are at least `1`, it cannot be confused with a valid occupied position. The checks against zero prevent an empty floor from accidentally producing a fake team at table zero.

For a candidate printer position `p`, `same` is initialized to zero. If the chosen floor contains teams, the two extreme distances are computed. The maximum of those two is exactly the worst inconvenience on that floor.

The opposite-floor contribution is also initialized to zero. If the opposite floor contains at least one team, its rightmost position is used in `right[other] + k + p`. There is no need to inspect any other team because every smaller table index produces a smaller cross-floor inconvenience.

The loop uses `range(1, n + 1)`, so `p` directly represents the problem's one-based table index. This avoids an off-by-one conversion when printing the answer. Python integers also handle the largest possible values comfortably, although the maximum answer here is only on the order of `2n + k`.

The strict comparison `cur < best_value` deliberately keeps the first optimal position encountered. This makes the output deterministic and also naturally produces the first sample's printer position at floor 1, table 1.

## Worked Examples

For Sample 1, the input is

```
3 2
001
001
```

Floor 1 has one team at table 3, and floor 2 also has one team at table 3. The following table traces the candidates on floor 1 first, which is enough to establish the optimum.

| Floor | `p` | Same-floor maximum | Opposite-floor maximum | `cur` | Best after candidate |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 6 | 6 | `(6, 1, 1)` |
| 1 | 2 | 1 | 7 | 7 | `(6, 1, 1)` |
| 1 | 3 | 0 | 8 | 8 | `(6, 1, 1)` |
| 2 | 1 | 2 | 6 | 6 | `(6, 1, 1)` |
| 2 | 2 | 1 | 7 | 7 | `(6, 1, 1)` |
| 2 | 3 | 0 | 8 | 8 | `(6, 1, 1)` |

At floor 1, table 1, the same-floor team is two tables away, while the opposite-floor team has inconvenience `3 + 2 + 1 = 6`. Moving the printer right increases the cross-floor cost, so no later position can improve the value. The symmetric floor 2 positions give the same values, but the strict update rule keeps the first optimum, producing `6` and `1 1`.

For Sample 2,

```
10 2
0001011011
1000000000
```

Floor 2 contains teams at tables `4, 6, 7, 9, 10`, while floor 1 contains a single team at table `1`. Consider floor 2, where the optimum is found.

| Floor | `p` | Same-floor maximum | Opposite-floor maximum | `cur` | Best on floor 2 |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 9 | 4 | 9 | `(9, 1)` |
| 2 | 2 | 8 | 5 | 8 | `(8, 2)` |
| 2 | 3 | 7 | 6 | 7 | `(7, 3)` |
| 2 | 4 | 6 | 7 | 7 | `(7, 3)` |
| 2 | 5 | 5 | 8 | 8 | `(7, 3)` |
| 2 | 6 | 4 | 9 | 9 | `(7, 3)` |

The same-floor contribution decreases as the printer moves from table 1 toward the occupied interval, while the opposite-floor contribution increases with `p`. Their balance reaches `7` at tables 3 and 4. The algorithm encounters table 3 first and keeps it, giving the sample output `7` and `2 3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The two floor strings are scanned once, then `2n` printer positions are evaluated in constant time each. |
| Space | O(1) | Only the two input strings and a constant number of extrema and answer variables are stored. |

With `n <= 1000`, the linear solution is far below the 1 second time limit and uses negligible memory compared with the 256 MB limit. Even the straightforward quadratic enumeration would fit these particular bounds, but the linear formulation directly captures the mathematical structure of the problem.

## Test Cases

The test harness below calls the same `solve` function used by the submitted program. Because the problem permits multiple optimal printer positions, the custom cases are chosen so that the deterministic scan order produces a known unique or first-optimal answer.

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    floor2 = input().strip()
    floor1 = input().strip()

    floors = [floor1, floor2]

    left = [0, 0]
    right = [0, 0]

    for f in range(2):
        for pos, ch in enumerate(floors[f], 1):
            if ch == '1':
                if left[f] == 0:
                    left[f] = pos
                right[f] = pos

    best_value = 10**18
    best_floor = 1
    best_pos = 1

    for f in range(2):
        other = 1 - f

        for p in range(1, n + 1):
            same = 0
            if right[f] != 0:
                same = max(p - left[f], right[f] - p)

            other_floor = 0
            if right[other] != 0:
                other_floor = right[other] + k + p

            cur = max(same, other_floor)

            if cur < best_value:
                best_value = cur
                best_floor = f + 1
                best_pos = p

    print(best_value)
    print(best_floor, best_pos)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("""3 2
001
001
""") == """6
1 1
""", "sample 1"

# Provided sample 2
assert run("""10 2
0001011011
1000000000
""") == """7
2 3
""", "sample 2"

# Minimum-size input, one team and one table
assert run("""1 1
1
0
""") == """0
2 1
""", "minimum size"

# Only one floor has teams, so the printer should sit on that floor
assert run("""5 3
00000
11111
""") == """2
1 3
""", "empty opposite floor"

# Teams at both extreme tables, checking the left/right extrema
assert run("""5 7
00000
10001
""") == """2
1 3
""", "extreme occupied tables"

# Maximum n, all tables occupied on both floors
assert run("1000 1000\n" + "1" * 1000 + "\n" + "1" * 1000 + "\n") == \
       """2001
1 1
""", "maximum size and all occupied"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 / 0` | `0 / 2 1` | Minimum size and an empty opposite floor |
| `5 3 / 00000 / 11111` | `2 / 1 3` | Printer may be placed at a free table and the chosen floor can be the only occupied floor |
| `5 7 / 00000 / 10001` | `2 / 1 3` | Correct use of both leftmost and rightmost occupied positions |
| `1000 1000 / 1000 ones / 1000 ones` | `2001 / 1 1` | Maximum input size, all tables occupied, and large values |

## Edge Cases

For an empty opposite floor, consider

```
1 1
1
0
```

The floor 2 string contains the only team, so placing the printer on floor 2 at table 1 gives same-floor inconvenience `|1 - 1| = 0`. During preprocessing, floor 2 gets `left = right = 1`, while floor 1 keeps `right = 0`. When evaluating floor 2, the same-floor term is `0` and the opposite-floor term remains `0` because floor 1 is empty. The resulting answer is `0 2 1`. This prevents a nonexistent team from contributing an artificial cross-floor distance.

For a team at the last table, consider

```
4 2
0001
0001
```

If the printer is on floor 1 at table `p`, the opposite floor has its rightmost team at table 4, so the cross-floor contribution is `4 + 2 + p`. This is minimized at `p = 1`, giving `7`. At `p = 2`, it becomes `8`, and larger positions are worse. The same-floor team is only three tables away at `p = 1`, so the maximum remains `7`. The algorithm records `7 1 1`, demonstrating why the rightmost position must be used for the cross-floor term.

When the chosen floor contains many teams, only its two extremes matter. For

```
5 3
11111
11111
```

floor 1 has `L = 1` and `R = 5`, while floor 2 has `R = 5`. At printer position 1, the same-floor maximum is `4` and the cross-floor maximum is `5 + 3 + 1 = 9`, so the objective is `9`. Moving right makes the cross-floor term increase, reaching `10` at position 2. Thus the first position is already optimal, and the algorithm outputs `9 1 1`.

For occupied tables only at the two boundaries,

```
5 7
00000
10001
```

the chosen floor has `L = 1` and `R = 5`. At `p = 3`, the same-floor distances are `2` to both occupied tables, so the maximum is `2`. The other floor is empty, so there is no cross-floor contribution. Positions 2 and 4 give maximum distance `3`, while positions 1 and 5 give `4`. The algorithm consequently finds `2 1 3`, showing that the optimum may lie on a free table and that both extrema are necessary.
