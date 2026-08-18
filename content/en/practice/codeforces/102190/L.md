---
title: "CF 102190L - standard input/output"
description: "We have groups of friends whose sizes are from 1 through 6. A bench has exactly six seats, and every group must occupy a single bench. Different groups may share a bench as long as their total size does not exceed six."
date: "2026-08-19T06:08:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102190
codeforces_index: "L"
codeforces_contest_name: "2019 ECNU Campus Invitational Contest"
rating: 0
weight: 102190
solve_time_s: 149
verified: true
draft: false
---

[CF 102190L - standard input/output](https://codeforces.com/problemset/problem/102190/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have groups of friends whose sizes are from 1 through 6. A bench has exactly six seats, and every group must occupy a single bench. Different groups may share a bench as long as their total size does not exceed six.

For each test case, the six input numbers give the number of groups of sizes 1, 2, 3, 4, 5, and 6. The task is to minimize the number of benches.

The total number of people is positive and at most 10,000 for one test case. There are at most 1,000 test cases. Since every group has at least one person, there are also at most 10,000 groups in one test case. This is small enough for a linear scan over all groups, but the structure of the problem lets us do much better: the optimal solution can be computed using only a constant number of arithmetic operations. A quadratic or exponential search over possible groupings is completely unnecessary.

The main edge cases come from groups that nearly fill a bench. For example, with

```
1
1 0 0 0 0 0
```

the answer is 1, because the single group needs one bench.

With

```
1
0 0 0 1 1 0
```

the answer is also 1, because a group of four and a group of two exactly fill one bench. A careless solution based only on the total number of people would still get this case right, but a solution that handles each group size independently could use two benches.

Another boundary case is

```
1
0 0 1 0 0 1
```

which needs 2 benches. A group of six cannot share a bench with anyone, while the group of three needs another bench.

The opposite mistake happens with small groups. For

```
1
8 0 0 0 0 0
```

there are eight groups of one person, so the answer is 2, not 8. Six groups can share one bench, and the remaining two share another.

## Approaches

A direct brute-force solution would treat every group as an item and recursively try every possible bench assignment. When processing a group, we could put it into any compatible existing bench or open a new one. This is correct because every possible seating arrangement is represented by some branch of the search.

The problem is the number of arrangements. If there are (n) groups, assigning them to arbitrary sets of benches is related to enumerating set partitions, whose count is the Bell number (B_n). With as many as 10,000 groups, even a much smaller upper bound such as (n^n = 10000^{10000}) is already hopeless. The brute-force approach is not merely too slow for the given limits, it is infeasible even for relatively small inputs.

The structure that makes the problem easy is the fixed bench capacity of six. Large groups have very few possible partners. A group of six has no partner at all. A group of five can only be paired with a group of one. A group of four can use a group of two, or two groups of one. A group of three can pair with another three, or use smaller groups to fill its remaining seats. Finally, groups of two can be packed at most three per bench, and groups of one fill whatever seats remain.

This gives a greedy strategy. Handle larger groups first, always using the largest useful complementary groups. Once the larger groups have been placed, the remaining problem consists only of groups of size two and one, where the optimal packing is immediate.

The key is not simply "put large groups first". Each greedy choice can be justified by the fact that a larger group has fewer possible placements than a smaller group. A group of five cannot use a group of two or three, so spending a group of one on it can never be worse than leaving that one for a group that has other choices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(B_n)) | (O(n)) | Too slow |
| Optimal Greedy | (O(1)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the counts of groups of sizes 1 through 6. Let them be (c_1,c_2,\ldots,c_6).
2. Put every group of size 6 on its own bench. Such a group has no remaining capacity that another group can use, so these benches are forced.
3. Handle groups of size 5. Each such group needs five seats and can only share with one group of size 1. Pair as many 5-groups as possible with 1-groups, and put any remaining 1-groups aside.
4. Handle groups of size 4. First pair them with groups of size 2. A (4+2) combination fills a bench exactly. If there are more 4-groups after all useful 2-groups have been used, put up to two 1-groups with each remaining 4-group.

Pairing a 4 with a 2 is safe even when two 1-groups are also available. In either case the 4-group already requires a bench, and the alternative arrangement does not reduce the number of benches needed for the other groups.
5. Pair groups of size 3 with each other. Every pair of 3-groups exactly fills one bench, so (\lfloor c_3/2\rfloor) benches are forced.
6. If one 3-group remains, open one more bench for it. If a 2-group is available, put it with the 3-group. If a 1-group is also available, it can join the same bench, producing (3+2+1=6). If there is no 2-group, fill the remaining seats with up to three 1-groups.

Using one remaining 2-group with an unmatched 3-group never increases the answer. Removing one 2-group changes the number of benches required for all remaining 2-groups from (\lceil b/3\rceil) to (\lceil(b-1)/3\rceil), which can only stay the same or decrease.
7. The only remaining groups now have sizes 1 and 2. Pack the 2-groups three per bench. If (b) 2-groups remain, they require (\lceil b/3\rceil) benches. These benches have (6\lceil b/3\rceil-2b) unused seats, so fill those seats with as many 1-groups as possible.
8. Any 1-groups still left require one bench for every six groups, rounded upward. Add this number to the answer and print it.

### Why it works

The invariant is that after processing group sizes from largest to smallest, every processed group is placed in a way that cannot increase the minimum number of benches needed for the unprocessed groups.

A size-6 group has no choice. A size-5 group can only use a size-1 group, so that pairing is forced whenever a 1-group exists. A size-4 group can use either a 2-group or two 1-groups, and using a 2-group first never costs an additional bench later. Size-3 groups are optimally paired with each other, with at most one unmatched 3-group remaining. After that, only sizes 2 and 1 remain, and three 2-groups are the maximum possible in one bench, so (\lceil c_2/3\rceil) benches are necessary. Filling their unused seats with 1-groups cannot hurt, since those seats would otherwise be empty. The remaining 1-groups then need exactly (\lceil c_1/6\rceil) benches.

Every decision is thus either forced or replaces a possible packing with another packing using no more benches. The final count is consequently optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(c):
    c1, c2, c3, c4, c5, c6 = c

    ans = c6

    # Groups of 5 can only share with groups of 1.
    use = min(c1, c5)
    c1 -= use
    ans += c5

    # Groups of 4 should use groups of 2 first.
    use = min(c2, c4)
    c2 -= use
    remaining4 = c4 - use
    ans += c4

    # Remaining groups of 4 can take two groups of 1 each.
    use = min(c1, 2 * remaining4)
    c1 -= use

    # Pair groups of 3.
    ans += c3 // 2

    # One group of 3 may remain.
    if c3 % 2:
        ans += 1

        if c2 > 0:
            c2 -= 1
            if c1 > 0:
                c1 -= 1
        else:
            c1 -= min(c1, 3)

    # Pack groups of 2, three per bench.
    benches2 = (c2 + 2) // 3
    ans += benches2

    # Use the unused seats on those benches for groups of 1.
    free = 6 * benches2 - 2 * c2
    c1 = max(0, c1 - free)

    # Remaining groups of 1, six per bench.
    ans += (c1 + 5) // 6

    return ans

def main():
    t = int(input())
    out = []

    for _ in range(t):
        c = list(map(int, input().split()))
        out.append(str(solve_case(c)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The first three lines inside `solve_case` unpack the six group counts. The answer starts with all size-6 groups because each of them consumes an entire bench.

For size 5, `min(c1, c5)` gives exactly how many 5-groups can receive a 1-group. The remaining 1-groups are saved for smaller groups.

For size 4, the code first removes as many 2-groups as possible. `remaining4` is the number of 4-groups that could not get a 2-group, so each has room for two 1-groups. The expression `2 * remaining4` is the total number of those available seats.

The size-3 handling uses integer division to pair 3-groups. The `% 2` branch handles the single possible unmatched group. The code prefers a remaining 2-group because a 3-group plus a 2-group uses capacity that would otherwise be harder to place. If a 1-group is also available, the bench becomes exactly full.

For the remaining 2-groups, `(c2 + 2) // 3` is the integer form of (\lceil c_2/3\rceil). The number of free seats on those benches is computed directly as `6 * benches2 - 2 * c2`. Any remaining 1-groups are then grouped six per bench.

All values are non-negative, and Python integers do not overflow. The use of `min` and `max` also prevents the remaining counts from becoming negative.

## Worked Examples

The first sample consists of six independent test cases, each containing exactly one group.

| Input groups (c_1,c_2,c_3,c_4,c_5,c_6) | Main action | Benches |
| --- | --- | --- |
| 1 0 0 0 0 0 | One group of 1 | 1 |
| 0 1 0 0 0 0 | One group of 2 | 1 |
| 0 0 1 0 0 0 | One group of 3 | 1 |
| 0 0 0 1 0 0 | One group of 4 | 1 |
| 0 0 0 0 1 0 | One group of 5 | 1 |
| 0 0 0 0 0 1 | One group of 6 | 1 |

This confirms that every individual group size is handled correctly. In particular, the size-6 case never tries to combine the group with another group.

For the first test case of the second sample, the counts are `6 9 5 8 3 2`.

| Stage | (c_1) | (c_2) | (c_3) | Benches added | Total |
| --- | --- | --- | --- | --- | --- |
| Start | 6 | 9 | 5 | 0 | 0 |
| Size 6 | 6 | 9 | 5 | 2 | 2 |
| Size 5 | 3 | 9 | 5 | 3 | 5 |
| Size 4 | 3 | 1 | 5 | 8 | 13 |
| Pair size 3 | 3 | 1 | 1 | 2 | 15 |
| Remaining size 3 | 2 | 0 | 0 | 1 | 16 |
| Remaining size 1 | 2 | 0 | 0 | 1 | 17 |

The final answer is 17. There are 98 people in total, so at least (\lceil98/6\rceil=17) benches are required. The greedy construction reaches that lower bound exactly.

For the second test case of the second sample, the counts are `2 2 5 1 3 8`.

| Stage | (c_1) | (c_2) | (c_3) | Benches added | Total |
| --- | --- | --- | --- | --- | --- |
| Start | 2 | 2 | 5 | 0 | 0 |
| Size 6 | 2 | 2 | 5 | 8 | 8 |
| Size 5 | 0 | 2 | 5 | 2 | 10 |
| Size 4 | 0 | 1 | 5 | 1 | 11 |
| Pair size 3 | 0 | 1 | 1 | 2 | 13 |
| Remaining size 3 | 0 | 0 | 0 | 1 | 14 |
| Remaining size 2 | 0 | 0 | 0 | 1 | 15 |

The answer is 15. The unmatched 3-group consumes the last remaining 2-group, leaving no small groups afterward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) per test case | Only a fixed number of arithmetic operations are performed |
| Space | (O(1)) | Only six counters and a few temporary variables are stored |

The constraints allow up to 1,000 test cases, so the entire program performs only a constant amount of work per test case. The maximum number of people, 10,000 per case, has no effect on the running time of this implementation.

## Test Cases

```python
# helper: run the solution logic on an input string
import sys
import io

def solve_case(c):
    c1, c2, c3, c4, c5, c6 = c

    ans = c6

    use = min(c1, c5)
    c1 -= use
    ans += c5

    use = min(c2, c4)
    c2 -= use
    remaining4 = c4 - use
    ans += c4

    use = min(c1, 2 * remaining4)
    c1 -= use

    ans += c3 // 2

    if c3 % 2:
        ans += 1
        if c2 > 0:
            c2 -= 1
            if c1 > 0:
                c1 -= 1
        else:
            c1 -= min(c1, 3)

    benches2 = (c2 + 2) // 3
    ans += benches2

    free = 6 * benches2 - 2 * c2
    c1 = max(0, c1 - free)

    ans += (c1 + 5) // 6

    return ans

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    t = int(sys.stdin.readline())
    out = []

    for _ in range(t):
        c = list(map(int, sys.stdin.readline().split()))
        out.append(str(solve_case(c)))

    sys.stdin = old_stdin
    return "\n".join(out)

# Provided sample 1
sample1 = """\
6
1 0 0 0 0 0
0 1 0 0 0 0
0 0 1 0 0 0
0 0 0 1 0 0
0 0 0 0 1 0
0 0 0 0 0 1
"""

assert run(sample1) == """\
1
1
1
1
1
1
""", "sample 1"

# Provided sample 2
sample2 = """\
19
6 9 5 8 3 2
2 2 5 1 3 8
1 2 0 4 0 0
4 1 5 5 2 8
8 6 6 0 0 0
4 8 8 6 0 3
2 2 2 9 5 2
8 1 7 6 3 10
8 9 7 10 6 6
7 3 8 5 2 1
3 5 5 8 6 10
9 2 6 3 9 5
10 8 5 2 0 5
3 7 1 1 4 4
0 9 2 0 5 8
5 5 1 10 6 2
1 5 5 10 3 5
2 5 7 0 1 9
5 3 9 1 4 5
"""

assert run(sample2) == """\
17
15
4
18
5
14
17
24
26
13
27
20
14
12
17
19
21
14
15
""", "sample 2"

# Minimum-size input
assert run("""\
1
1 0 0 0 0 0
""") == "1", "single group"

# Maximum number of people, all in groups of one
assert run("""\
1
10000 0 0 0 0 0
""") == "1667", "10000 groups of one"

# All groups have size three, with 9999 people
assert run("""\
1
0 0 3333 0 0 0
""") == "1667", "3333 groups of three"

# Exact-fit and near-exact-fit cases
assert run("""\
4
2 2 0 1 0 0
1 0 1 1 0 0
0 1 1 0 0 0
5 0 0 0 5 0
""") == """\
2
2
1
5
""", "boundary cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0 0 0 0` | `1` | Minimum non-empty input |
| `10000 0 0 0 0 0` | `1667` | Maximum people count and ceiling division |
| `0 0 3333 0 0 0` | `1667` | All groups equal and odd group counts |
| `2 2 0 1 0 0` | `2` | Exact (4+2) packing and remaining small groups |
| `1 0 1 1 0 0` | `2` | A size-4 group competing with a size-3 group |
| `0 1 1 0 0 0` | `1` | Exact (3+2+1) style packing after the unmatched 3 |
| `5 0 0 0 5 0` | `5` | Size-5 groups consuming size-1 groups |

## Edge Cases

For a single group of one, the input is `1 0 0 0 0 0`. The algorithm skips all larger groups, reaches the final size-1 calculation, and computes `(1 + 5) // 6 = 1`. The result is exactly one bench.

For a group of six, the input is `0 0 0 0 0 1`. The initial `ans = c6` immediately contributes one bench. No other operation can combine anything with this group because its capacity is already full.

For the exact-fit case `0 1 0 1 0 0`, the size-4 group consumes the size-2 group. The algorithm adds one bench for the 4-group and removes the 2-group, producing the correct answer of 1.

For an unmatched group of three with a group of two and a group of one, the input `1 1 1 0 0 0` is handled by the size-3 branch. The remaining 3-group consumes the 2-group and the 1-group, giving one completely filled bench with six seats.

For many groups of one, the input `10000 0 0 0 0 0` reaches only the final stage. Six groups fit on each bench, so the answer is (\lceil10000/6\rceil=1667). The ceiling is implemented as `(c1 + 5) // 6`, avoiding floating-point arithmetic.

The most delicate case is when a 3-group remains but no 1-group exists. For example, `0 1 1 0 0 0` gives one 3-group and one 2-group. The algorithm puts them together, leaving one unused seat. That is still optimal because separating them would require two benches, while using the 2-group on the existing 3-group cannot increase the number of benches required for the remaining 2-groups.
