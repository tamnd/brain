---
title: "CF 1729F - Kirei and the Linear Function"
description: "We are given a digit string. For every query, we look at one substring of the original string, namely s[l..r], and compute its numeric value modulo 9. Separately, we may choose any two different substrings of fixed length w. Let their starting positions be L1 and L2."
date: "2026-06-09T18:47:58+07:00"
tags: ["codeforces", "competitive-programming", "hashing", "math"]
categories: ["algorithms"]
codeforces_contest: 1729
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 820 (Div. 3)"
rating: 1900
weight: 1729
solve_time_s: 108
verified: true
draft: false
---

[CF 1729F - Kirei and the Linear Function](https://codeforces.com/problemset/problem/1729/F)

**Rating:** 1900  
**Tags:** hashing, math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a digit string. For every query, we look at one substring of the original string, namely `s[l..r]`, and compute its numeric value modulo `9`.

Separately, we may choose any two different substrings of fixed length `w`. Let their starting positions be `L1` and `L2`. The query asks for positions satisfying

$$v(L_1,L_1+w-1)\cdot v(l,r)+v(L_2,L_2+w-1)\equiv k \pmod 9$$

Among all valid pairs, we must minimize `L1`, and among those, minimize `L2`.

The first thing that stands out is that the actual numbers can be extremely large. A substring may contain up to `2·10^5` digits, so constructing the number directly is impossible. Fortunately, the condition only cares about the remainder modulo `9`.

The total length over all test cases is at most `2·10^5`, and the total number of queries is also at most `2·10^5`. Any algorithm that examines all pairs of length-`w` substrings for every query is hopeless. Even a single test case can contain roughly `2·10^5` candidate substrings, so quadratic work would be around `4·10^{10}` operations.

The solution must preprocess all length-`w` substrings once and then answer each query in nearly constant time.

A subtle point is that the answer is not just any valid pair. Lexicographic minimization matters. Consider a situation where residue class `3` contains starting positions `[2,7,20]` and residue class `5` contains `[4,8]`. If both `(2,8)` and `(7,4)` satisfy the modular equation, the correct answer is `(2,8)` because `L1` is smaller. A careless implementation that stops at the first valid residue combination may return the wrong pair.

Another easy mistake is forgetting that `L1` and `L2` must be different positions. Suppose every length-`w` substring has the same residue and there is only one occurrence of that residue. Then using the same position twice is forbidden.

For example:

```
s = "111"
w = 2
```

The only length-2 substrings start at positions `1` and `2`. Any logic that allows reusing a single occurrence of a residue may incorrectly produce `(1,1)`.

Leading zeros are also relevant. The substring `"000"` represents the number `0`, not an invalid value. Since we only need modulo `9`, digit sums handle this naturally.

## Approaches

The brute force idea is straightforward. For every query, enumerate every possible length-`w` substring as the first choice and every possible length-`w` substring as the second choice. Check whether

$$(a\cdot x+b)\bmod 9=k$$

where `a` is the query substring value modulo `9`, and `x`, `b` are the residues of the chosen length-`w` substrings.

There are roughly `n-w+1` candidates. In the worst case this is about `2·10^5`, so checking all pairs costs roughly

$$(2\cdot10^5)^2 = 4\cdot10^{10}$$

operations per query. That is completely infeasible.

The key observation is that modulo `9` collapses the search space dramatically.

For any decimal number,

$$value \bmod 9 = (\text{sum of digits}) \bmod 9.$$

Every length-`w` substring belongs to one of only nine residue classes, `0` through `8`.

Instead of remembering every substring value, we only care about its residue modulo `9`. For each residue `r`, we store the starting positions of all length-`w` substrings whose value modulo `9` equals `r`.

Now consider a query. Let

$$a = v(l,r)\bmod 9.$$

We need residues `x` and `y` such that

$$(a\cdot x+y)\bmod 9 = k.$$

There are only `9×9=81` residue pairs to check.

For each candidate residue pair, we can determine the lexicographically smallest valid positions immediately from the stored lists. Since 81 is constant, each query becomes `O(81)`.

The remaining task is computing substring residues efficiently. Using prefix sums of digits, the digit sum of any substring is available in `O(1)`, hence its modulo `9` value is also available in `O(1)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m·n²) | O(n) | Too slow |
| Optimal | O(n + 81m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array of digit values.

Let `pref[i]` be the sum of the first `i` digits. Then the digit sum of any substring is

$$pref[r]-pref[l-1].$$
2. Enumerate every length-`w` substring.

For each starting position `i`, compute the digit sum of `s[i..i+w-1]` using the prefix sums and take it modulo `9`.
3. Group starting positions by residue.

Create nine lists. If a length-`w` substring has residue `r`, append its starting position to list `pos[r]`.

Because we scan left to right, positions inside each list are automatically sorted.
4. Process each query.

Compute

$$a=v(l,r)\bmod 9.$$

Again, digit sums give this in `O(1)`.
5. Enumerate all residue pairs `(x,y)`.

Check whether

$$(a\cdot x+y)\bmod 9 = k.$$

Only such pairs can contribute to an answer.
6. For a valid residue pair, determine the smallest usable positions.

If `x != y`, the best choice is the first element of `pos[x]` and the first element of `pos[y]`.

If `x == y`, we need two distinct substrings, so the residue class must contain at least two positions. The best choice is the first two positions in that list.
7. Among all candidate answers, keep the lexicographically smallest pair.

Compare first by `L1`, then by `L2`.
8. Output the stored pair, or `-1 -1` if no candidate exists.

### Why it works

Every length-`w` substring is represented solely by its residue modulo `9`. The query condition depends only on these residues:

$$(v_1\cdot a+v_2)\bmod 9 = ((v_1\bmod9)\cdot(a\bmod9)+(v_2\bmod9))\bmod9.$$

So replacing each substring by its residue loses no information.

For a fixed residue pair `(x,y)`, the lexicographically smallest usable positions are always obtained from the earliest occurrences stored in the corresponding lists. Any later occurrence would only increase `L1` or `L2`.

The algorithm checks every possible residue pair. Since every substring belongs to exactly one residue class, every valid answer corresponds to one of the examined pairs. Among all feasible candidates, the lexicographically smallest one is selected, which matches the problem requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        s = input().strip()
        n = len(s)

        w, m = map(int, input().split())

        pref = [0] * (n + 1)
        for i, ch in enumerate(s, 1):
            pref[i] = pref[i - 1] + int(ch)

        pos = [[] for _ in range(9)]

        for start in range(1, n - w + 2):
            end = start + w - 1
            rem = (pref[end] - pref[start - 1]) % 9
            pos[rem].append(start)

        for _ in range(m):
            l, r, k = map(int, input().split())

            a = (pref[r] - pref[l - 1]) % 9

            best = None

            for x in range(9):
                if not pos[x]:
                    continue

                for y in range(9):
                    if (a * x + y) % 9 != k:
                        continue

                    if x != y:
                        if not pos[y]:
                            continue
                        cand = (pos[x][0], pos[y][0])
                    else:
                        if len(pos[x]) < 2:
                            continue
                        cand = (pos[x][0], pos[x][1])

                    if best is None or cand < best:
                        best = cand

            if best is None:
                print(-1, -1)
            else:
                print(best[0], best[1])

solve()
```

The prefix sum array stores digit sums rather than numeric values. Modulo `9`, digit sums and numbers are equivalent, which avoids dealing with enormous integers.

The preprocessing phase computes the residue of every length-`w` substring. Each starting position is inserted into one of nine buckets. Because positions are processed in increasing order, the first element of a bucket is automatically the smallest starting position having that residue.

During query processing, the residue of `s[l..r]` is obtained from the same prefix sums. The double loop over `x` and `y` examines all 81 possible residue combinations. Whenever a pair satisfies the modular equation, the earliest valid positions are extracted from the corresponding buckets.

The special case `x == y` requires care. We need two different substrings, so a bucket with only one position cannot be used. The first two positions provide the lexicographically smallest valid pair.

Python tuple comparison conveniently implements the required ordering: `(a,b) < (c,d)` exactly means smaller `L1`, and if equal, smaller `L2`.

## Worked Examples

### Example 1

Input:

```
s = 1003004
w = 4
query = (1,2,1)
```

Length-4 substrings:

| Start | Substring | Digit Sum | Residue |
| --- | --- | --- | --- |
| 1 | 1003 | 4 | 4 |
| 2 | 0030 | 3 | 3 |
| 3 | 0300 | 3 | 3 |
| 4 | 3004 | 7 | 7 |

Stored lists:

| Residue | Positions |
| --- | --- |
| 3 | [2, 3] |
| 4 | [1] |
| 7 | [4] |

Query substring:

| l | r | Value | Residue |
| --- | --- | --- | --- |
| 1 | 2 | 10 | 1 |

We need:

$$(1\cdot x+y)\bmod9=1$$

One valid residue pair is `(3,7)` because

$$3+7=10\equiv1\pmod9.$$

This yields positions `(2,4)`.

| x | y | Candidate |
| --- | --- | --- |
| 3 | 7 | (2,4) |

The answer is:

```
2 4
```

This example demonstrates how actual substring values disappear from the problem. Only residues matter.

### Example 2

Input:

```
s = 111
w = 2
query = (2,2,6)
```

Length-2 substrings:

| Start | Substring | Digit Sum | Residue |
| --- | --- | --- | --- |
| 1 | 11 | 2 | 2 |
| 2 | 11 | 2 | 2 |

Stored lists:

| Residue | Positions |
| --- | --- |
| 2 | [1,2] |

Query substring residue:

| l | r | Residue |
| --- | --- | --- |
| 2 | 2 | 1 |

Required equation:

$$(1\cdot x+y)\bmod9=6$$

Choosing `x=y=2` gives

$$2+2=4$$

which does not work.

Checking all 81 residue pairs finds no solution.

Output:

```
-1 -1
```

This trace shows that the algorithm correctly rejects residue combinations even when enough occurrences exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 81m) | Preprocessing is linear, each query checks 81 residue pairs |
| Space | O(n) | Stores all length-`w` starting positions |

Since the total `n` and total `m` across all test cases are both at most `2·10^5`, the complexity is effectively linear. The constant factor from the 81 residue pairs is tiny, making the solution easily fit within the 3-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup = sys.stdout
    sys.stdout = out

    def solve():
        input = sys.stdin.readline

        t = int(input())
        for _ in range(t):
            s = input().strip()
            n = len(s)

            w, m = map(int, input().split())

            pref = [0] * (n + 1)
            for i, ch in enumerate(s, 1):
                pref[i] = pref[i - 1] + int(ch)

            pos = [[] for _ in range(9)]

            for st in range(1, n - w + 2):
                rem = (pref[st + w - 1] - pref[st - 1]) % 9
                pos[rem].append(st)

            for _ in range(m):
                l, r, k = map(int, input().split())

                a = (pref[r] - pref[l - 1]) % 9
                best = None

                for x in range(9):
                    if not pos[x]:
                        continue

                    for y in range(9):
                        if (a * x + y) % 9 != k:
                            continue

                        if x != y:
                            if not pos[y]:
                                continue
                            cand = (pos[x][0], pos[y][0])
                        else:
                            if len(pos[x]) < 2:
                                continue
                            cand = (pos[x][0], pos[x][1])

                        if best is None or cand < best:
                            best = cand

                if best is None:
                    print("-1 -1")
                else:
                    print(best[0], best[1])

    solve()

    sys.stdout = backup
    return out.getvalue()

# sample
assert run("""1
1003004
4 1
1 2 1
""") == "2 4\n"

# minimum size
assert run("""1
10
1 1
1 1 1
""") == "1 2\n"

# all zeros
assert run("""1
0000
1 1
1 4 0
""") == "1 2\n"

# no solution
assert run("""1
111
2 1
2 2 6
""") == "-1 -1\n"

# same residue requires two occurrences
assert run("""1
000
1 1
1 3 0
""") == "1 2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10`, `w=1` | `1 2` | Smallest legal instance |
| `0000`, `w=1` | `1 2` | Leading zeros and residue 0 |
| `111`, `w=2` | `-1 -1` | Correct rejection when equation impossible |
| `000`, `w=1` | `1 2` | Distinct positions required for same residue |

## Edge Cases

Consider:

```
1
0000
1 1
1 4 0
```

Every length-1 substring has residue `0`. The bucket is:

```
pos[0] = [1,2,3,4]
```

The query substring also has residue `0`, so the equation becomes:

$$0\cdot x+y\equiv0\pmod9.$$

Choosing `x=y=0` is valid. Since the residues are equal, the algorithm requires two distinct positions and returns the first two occurrences, `(1,2)`. This correctly handles leading zeros.

Now consider:

```
1
12
1 1
1 1 5
```

The residue buckets are:

```
pos[1] = [1]
pos[2] = [2]
```

The algorithm checks all 81 residue pairs. If none satisfy the equation, `best` remains `None` and `-1 -1` is printed. No accidental answer is produced.

Finally, consider a case where the same residue must be used twice:

```
1
000
1 1
1 3 0
```

Here:

```
pos[0] = [1,2,3]
```

The residue pair `(0,0)` satisfies the equation. The algorithm does not use `(1,1)`. Instead it explicitly takes the first two positions, producing `(1,2)`, which respects the requirement that the chosen substrings be different.
