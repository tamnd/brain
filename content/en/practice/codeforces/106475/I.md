---
title: "CF 106475I - \u0411\u043b\u0438\u043d\u0447\u0438\u043a \u0438 \u0440\u0438\u0441\u043e\u0432\u0430\u043d\u0438\u0435"
description: "We have n pencil colors. If we draw xi fish with color i, the stars received from this color depend on how many fish share that color. The first fish of color i gives ai stars, the second gives ai - 2, the third gives ai - 4, and so on."
date: "2026-06-25T08:52:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106475
codeforces_index: "I"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u0412\u041a\u041e\u0428\u041f.Junior 2026"
rating: 0
weight: 106475
solve_time_s: 36
verified: true
draft: false
---

[CF 106475I - \u0411\u043b\u0438\u043d\u0447\u0438\u043a \u0438 \u0440\u0438\u0441\u043e\u0432\u0430\u043d\u0438\u0435](https://codeforces.com/problemset/problem/106475/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` pencil colors. If we draw `x_i` fish with color `i`, the stars received from this color depend on how many fish share that color. The first fish of color `i` gives `a_i` stars, the second gives `a_i - 2`, the third gives `a_i - 4`, and so on. A color can be used only until the score of an individual fish would become invalid, which means the number of fish of that color cannot exceed `a_i + 1`.

The task is to choose exactly `m` fish in total, distributing them among colors, so that the sum of all received stars is as large as possible. We must output both the maximum score and one valid distribution.

The constraints force us to avoid anything proportional to `m`. The value of `m` can reach `10^9`, so simulating every fish or every possible choice is impossible. Even `O(m)` would require billions of operations. The number of colors is only `2 * 10^5`, so the intended solution has to work close to `O(n log A)` where `A` is the range of possible star values.

The tricky part is that the best distribution is not simply "use colors with the largest `a_i` first". A color becomes less valuable as more fish are assigned to it. For example, if `a = [5]` and `m = 3`, the three fish give `5`, `3`, and `1` stars, not three times `5`.

A careless solution can also fail on large required counts. For example:

```
Input
1 2
1
```

The only color gives values `1, -1, ...`. The correct output is:

```
0
0 2
```

The two fish together give `1 + (-1) = 0`. A greedy solution that only takes positive contributions might output one fish, but exactly `m` fish must be drawn.

Another edge case is when many colors have equal marginal values:

```
Input
3 9
1 2 3
```

The correct output is:

```
0
2 3 4
```

Different optimal distributions may exist. The algorithm must handle ties without assuming a unique answer.

## Approaches

The direct approach is to look at each possible fish addition. For color `i`, the sequence of gains is:

```
a_i, a_i - 2, a_i - 4, ..., -a_i
```

There are `a_i + 1` possible fish for this color. If we generated every possible gain and selected the largest `m`, the solution would be correct because every fish choice contributes exactly one marginal value. However, `a_i` can be as large as `10^9`, so this sequence can contain billions of values. Expanding all sequences is impossible.

The key observation is that these sequences are sorted arithmetic progressions. We do not need to generate them. We only need to know how many values are at least some threshold.

Suppose we choose a value `x`. For one color, the number of marginal gains at least `x` can be found mathematically. If we can count how many gains are above a threshold in all colors, binary search lets us find the cutoff value among the largest `m` gains.

After finding the threshold `t`, every gain larger than `t` must be taken, and only some gains equal to `t` may be needed to reach exactly `m` fish. Because all gains in a color form a decreasing sequence, the chosen gains for each color always form a prefix, which lets us reconstruct the number of fish of every color.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum(a_i)) | O(sum(a_i)) | Too slow because values can reach 10^9 |
| Optimal | O(n log A) | O(n) | Accepted |

## Algorithm Walkthrough

1. For every color, view the possible fish contributions as a decreasing sequence:

`a_i, a_i - 2, a_i - 4, ... , -a_i`.

The answer is the sum of the largest `m` values among all these sequences.
2. Implement a function that counts how many values in all sequences are at least a given number `x`.

For one color, if `x > a_i`, there are no such values. If `x <= -a_i`, all `a_i + 1` values qualify. Otherwise, solve:

`a_i - 2k >= x`

for the largest possible `k`.
3. Binary search the largest threshold `t` such that there are at least `m` marginal values greater than or equal to `t`.

This threshold is the value of the last selected marginal contribution.
4. Compute all contributions strictly larger than `t`. These contributions must be selected because there are fewer than `m` contributions above the threshold.
5. Add enough contributions equal to `t` to reach exactly `m` fish.

For each color, first assign all fish whose contribution is larger than `t`. Then distribute the remaining fish among colors whose next available contribution equals `t`.
6. Compute the final score as the sum of all selected marginal contributions and output the number of fish assigned to each color.

Why it works: the marginal contribution of each additional fish of a fixed color only decreases, so any optimal choice from one color must take a prefix of its sequence. The whole problem becomes selecting the largest `m` elements from sorted sequences. The threshold found by binary search separates selected values from unselected values. All values above the threshold are mandatory, and filling the remaining positions with values equal to the threshold cannot reduce the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    def count_ge(x):
        res = 0
        for v in a:
            if x > v:
                continue
            if x <= -v:
                res += v + 1
            else:
                res += (v - x) // 2 + 1
        return res

    def sum_ge(x):
        res = 0
        for v in a:
            if x > v:
                continue
            if x <= -v:
                c = v + 1
            else:
                c = (v - x) // 2 + 1
            last = v - 2 * (c - 1)
            res += c * (v + last) // 2
        return res

    lo = -10**9 - 1
    hi = 10**9 + 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if count_ge(mid) >= m:
            lo = mid
        else:
            hi = mid

    threshold = lo

    ans = sum_ge(threshold + 1)
    used = [0] * n
    taken = 0

    for i, v in enumerate(a):
        if threshold + 1 > v:
            continue
        if threshold + 1 <= -v:
            c = v + 1
        else:
            c = (v - (threshold + 1)) // 2 + 1
        used[i] = c
        taken += c

    need = m - taken

    for i, v in enumerate(a):
        if need == 0:
            break
        nxt = v - 2 * used[i]
        if nxt == threshold:
            used[i] += 1
            need -= 1
            ans += threshold

    print(ans)
    print(*used)

if __name__ == "__main__":
    solve()
```

The `count_ge` function is the core of the binary search. It never constructs the sequences, because each color can be counted using arithmetic progression formulas.

The `sum_ge` function uses the same counting logic, but also sums the selected arithmetic progression. The first value is always `a_i`, and the last selected value is found by subtracting `2` for every step.

After finding the threshold, the reconstruction phase takes every contribution strictly above it. The remaining positions must all have value exactly equal to the threshold, so checking the next unused contribution of each color is enough. The sequence order guarantees that adding one more fish is always the next available marginal value.

All arithmetic is done with Python integers, so the large products involved in summing contributions do not overflow.

## Worked Examples

### Example 1

Input:

```
5 8
3 1 4 1 5
```

The marginal sequences are:

```
Color 1: 3 1 -1 -3
Color 2: 1 -1
Color 3: 4 2 0 -2 -4
Color 4: 1 -1
Color 5: 5 3 1 -1 -3 -5
```

The eight largest values are:

```
5, 4, 3, 3, 2, 1, 1, 1
```

| Step | Threshold | Fish chosen | Score |
| --- | --- | --- | --- |
| Initial | none | all sequences | 0 |
| Select values above cutoff | 2 | Color 5 gets 2, Color 3 gets 2 | 17 |
| Add values equal to cutoff | 1 | Three more colors receive fish | 20 |

The output distribution can be:

```
1 1 2 1 3
```

The trace shows that equal marginal values can be assigned to any compatible colors.

### Example 2

Input:

```
3 8
3 2 2
```

The sequences are:

```
Color 1: 3 1 -1 -3
Color 2: 2 0 -2
Color 3: 2 0 -2
```

| Step | Threshold | Fish chosen | Score |
| --- | --- | --- | --- |
| Binary search | 0 | Count values >= 0 is enough | 11 |
| Take values above 0 | 1 | 3, 2, 2, 1 | 8 |
| Fill remaining zeros | 0 | Add four zero contributions | 8 |

A valid distribution is:

```
3 3 2
```

The important point is that zero and negative contributions are sometimes necessary because the picture must contain exactly `m` fish.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Binary search checks about 31 thresholds, and each check scans all colors |
| Space | O(n) | Only the input array and the resulting counts are stored |

The value range is around two billion, so the binary search needs only about 31 iterations. With `n = 2 * 10^5`, this gives roughly six million operations, which fits comfortably in the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

# provided samples
assert run("""5 8
3 1 4 1 5
""").split()[0] == "20"

assert run("""3 8
3 2 2
""").split()[0] == "5"

# custom cases
assert run("""1 1
10
""").split()[0] == "10"

assert run("""1 2
1
""").split()[0] == "0"

assert run("""3 9
1 2 3
""").split()[0] == "0"

assert run("""5 14
2 2 3 2 2
""").split()[0] == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 10` | `10` | Minimum size and first marginal value |
| `1 2 / 1` | `0` | Negative marginal values are sometimes required |
| `3 9 / 1 2 3` | `0` | Maximum use of capacities and boundary handling |
| `5 14 / 2 2 3 2 2` | `5` | Many equal values and threshold reconstruction |

## Edge Cases

For the case:

```
1 2
1
```

the only sequence is:

```
1, -1
```

The binary search finds the threshold `-1`. The algorithm takes the value above `-1`, which is `1`, then adds one value equal to `-1`. The final score is `0`, and the only valid distribution is two fish of the same color.

For:

```
3 9
1 2 3
```

the capacities are `2`, `3`, and `4`, so all fish must be used. The selected marginal values are:

```
1, -1
2, 0, -2
3, 1, -1, -3
```

Their sum is zero. The algorithm reaches this naturally because the threshold becomes the lowest required contribution and it still respects the exact fish count.

For colors with the same values, such as:

```
5 14
2 2 3 2 2
```

many marginal contributions are identical. The binary search only determines the value boundary, not the exact colors. During reconstruction, any colors with the needed next contribution are acceptable, which is why the method can output any optimal distribution.
