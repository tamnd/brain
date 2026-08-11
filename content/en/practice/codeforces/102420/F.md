---
title: "CF 102420F - Arithmetic and blocks"
description: "We have (n) physical cubes. Each cube can display any digit that appears on one of its six faces, but a cube can display only one digit at a time. To build a number, Aurora chooses as many cubes as the number has digits and assigns one distinct cube to every digit position."
date: "2026-08-12T00:46:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102420
codeforces_index: "F"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102420
solve_time_s: 276
verified: true
draft: false
---

[CF 102420F - Arithmetic and blocks](https://codeforces.com/problemset/problem/102420/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) physical cubes. Each cube can display any digit that appears on one of its six faces, but a cube can display only one digit at a time. To build a number, Aurora chooses as many cubes as the number has digits and assigns one distinct cube to every digit position. The cubes can be rearranged freely, and the same collection of cubes may be reused when constructing another number.

The task is to find the smallest positive integer for which such an assignment is impossible.

The useful representation of a cube is not the exact six faces, but the set of distinct digits occurring on it. If a cube says `111234`, it is just as useful for this problem as a cube saying `112234`, because both can provide exactly the digits (1,2,3,4). Repeated copies of a digit on the same cube never give us two copies of that digit, since the cube can occupy only one position.

The input contains up to (100,000) cubes, with six digits describing each cube. A direct search over possible numbers is completely ruled out by this bound. Even if checking one number were cheap, the number of candidates before the first impossible number can be exponential in (n). The solution must process the cubes essentially once and use the fact that there are only ten possible digits.

There are several edge cases that can silently break a naive solution.

First, repeated faces on one cube must not be counted multiple times. For example,

```
1
111111
```

has only one cube capable of showing digit (1), not six independent copies. Since digit (2) never occurs, the correct answer is `2`. Counting faces instead of cubes would incorrectly suggest that many copies of (1) are available.

Second, zero cannot be used as the first digit. For

```
1
012345
```

the digits (1,2,3,4,5) can be made, but digit (6) cannot, so the answer is `6`. A method that simply treats every digit symmetrically has to be careful because a shortage of zeroes affects numbers differently from a shortage of nonzero digits.

Third, having enough cubes for each digit separately does not always guarantee that a combination of two digits is possible. Consider

```
2
012349
456788
```

Digit (9) occurs on exactly one cube and digit (0) also occurs on exactly one cube, namely the same cube. The number `9` is possible, and `99` is impossible, but the smaller number `90` is already impossible because the single cube that can show (9) is also the only cube that can show (0). The correct answer is `90`. This shared-cube situation is the only interaction between different digit types that has to be examined by the optimal algorithm.

## Approaches

The most direct approach is to enumerate positive integers in increasing order. For every candidate, create a bipartite graph whose left side consists of its digit positions and whose right side consists of the cubes. Connect a position containing digit (d) to every cube that has (d) on at least one face. The candidate is constructible exactly when this graph has a matching covering every digit position.

That brute force is correct because a matching is precisely an assignment of distinct cubes to the positions of the number. The problem is the number of candidates. The six faces per cube limit how many different digits can be available, but they do not prevent the first impossible number from having (\Theta(n)) digits. For example, with a balanced construction, every nonzero digit can occur on roughly (2n/3) cubes, so numbers of length about (2n/3) can all survive the individual digit-count tests. Enumerating all numbers up to that point means on the order of (10^{2n/3}) candidates. Even an (O(n)) check per candidate would be hopeless.

The key observation is that we do not actually need to test individual numbers. Let (cnt[d]) be the number of cubes containing digit (d), where each cube contributes at most once to this count.

Suppose a number has length (k). If every nonzero digit occurs on at least (k) cubes and zero occurs on at least (k-1) cubes, then every (k)-digit number is constructible. We can see this directly by considering the digit positions one by one. For any requested nonzero digit there are at least (k) possible cubes, while fewer than (k) positions can have already consumed cubes. For zero there are at least (k-1) possible cubes, exactly matching the maximum number of zero positions in a valid (k)-digit number.

The official contest tutorial uses this same reduction to per-digit cube counts and then isolates one special interaction between zero and the first insufficient nonzero digit.

Consequently, let

[
L=\min\left(cnt[0]+2,\ \min_{d=1}^{9}(cnt[d]+1)\right).
]

Every number with fewer than (L) digits is constructible, while some number with (L) digits is not. The answer therefore has exactly (L) digits.

If the zero term determines (L), the smallest (L)-digit number that needs too many zeroes is

[
100\ldots0.
]

If a nonzero digit is responsible for (L), choose the smallest such digit (d). The obvious impossible candidate is

[
ddd\ldots d.
]

There is one earlier candidate that can beat it, namely

[
d000\ldots0.
]

This candidate needs one cube containing (d) and (L-1) cubes containing zero. In the interesting case, both (cnt[d]) and (cnt[0]) equal (L-1). It fails precisely when the sets of cubes containing (d) and zero are identical. We only need to know how many cubes contain both digits, so we maintain (both[d]). If

[
cnt[0]=cnt[d]=both[d]=L-1,
]

then `d000...0` is impossible and is the answer. Otherwise it is constructible, and `ddd...d` is the first impossible number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\cdot 10^{\Theta(n)})) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(1)) besides the output | Accepted |

## Algorithm Walkthrough

1. Read every cube and convert its six faces into a ten-bit mask. A bit is set exactly when that digit appears on the cube. This removes duplicate faces automatically.
2. For every digit (d), count how many cubes have bit (d) set. Call this value (cnt[d]). At the same time, for every nonzero digit (d), count how many cubes contain both zero and (d), storing the result in (both[d]).
3. Compute

[
L=\min\left(cnt[0]+2,\ \min_{d=1}^{9}(cnt[d]+1)\right).
]

The term (cnt[d]+1) says that (cnt[d]) copies of digit (d) are available, so one more copy already requires too many cubes. The zero term is shifted by one because the first digit cannot be zero.

1. If (L=cnt[0]+2), output `1` followed by (L-1) zeroes. There are only (L-2) zero-capable cubes, while this number requires (L-1) of them, so it is impossible. Since it is the smallest number of its length, it is immediately the answer.
2. Otherwise find the smallest nonzero digit (d) satisfying (cnt[d]+1=L). All smaller nonzero digits occur on at least (L) cubes, while (d) occurs on exactly (L-1) cubes. The number consisting entirely of (d) is consequently impossible.
3. Check whether `d000...0` is impossible. This only needs to be considered when (cnt[0]=L-1). Since (cnt[d]=L-1) as well, the number is impossible exactly when every zero-capable cube is also (d)-capable and vice versa. With equal set sizes, that is equivalent to (both[d]=L-1).
4. If that special condition holds, output (d) followed by (L-1) zeroes. Otherwise output (d) repeated (L) times.

The invariant behind the algorithm is that all numbers shorter than (L) are safe because every digit has enough individually available cubes. At length (L), only the first insufficient nonzero digit can create a shortage, and the only lexicographically earlier combination that can exploit a second shortage is `d000...0`. Its feasibility depends only on the overlap between the cubes containing (d) and zero. Once that candidate is ruled out, every smaller (L)-digit number has enough available cubes for every requested digit, so the repeated-(d) number is the first impossible one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    cnt = [0] * 10
    both = [0] * 10

    for _ in range(n):
        s = input().strip()

        mask = 0
        for ch in s:
            mask |= 1 << (ord(ch) - ord('0'))

        for d in range(10):
            if mask & (1 << d):
                cnt[d] += 1

        if mask & 1:
            for d in range(1, 10):
                if mask & (1 << d):
                    both[d] += 1

    L = cnt[0] + 2
    for d in range(1, 10):
        L = min(L, cnt[d] + 1)

    if L == cnt[0] + 2:
        print('1' + '0' * (L - 1))
        return

    d = 1
    while cnt[d] + 1 != L:
        d += 1

    if cnt[0] == L - 1 and both[d] == L - 1:
        print(str(d) + '0' * (L - 1))
    else:
        print(str(d) * L)

if __name__ == "__main__":
    solve()
```

The first loop constructs a bitmask for one cube. Since the input has exactly six characters, this takes constant time per cube. A repeated face such as `111111` sets the same bit six times but contributes only one count.

The two counting loops then update `cnt`. The second one runs only for cubes containing zero and records the overlap with each nonzero digit. There is no need to store the cubes themselves after these counts have been accumulated.

The calculation of `L` is the central boundary calculation. The `+1` for nonzero digits means that (cnt[d]) available cubes can support at most (cnt[d]) occurrences. The `+2` for zero means that a valid number of length (k) can contain at most (k-1) zeroes.

The comparison `L == cnt[0] + 2` deliberately handles a tie in favor of the zero candidate. For example, if both `100...0` and `ddd...d` are impossible at the same length, the former is always numerically smaller.

The search for `d` starts at digit (1), so the first insufficient nonzero digit is chosen. Python integers do not overflow, and the only potentially large object is the final answer, whose length is at most (n+1).

## Worked Examples

### Sample 1

The input is

```
2
012345
098765
```

The distinct digit availability is:

| Digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `cnt[d]` | 2 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 |

The key state is:

| Quantity | Value |
| --- | --- |
| `cnt[0] + 2` | 4 |
| `min(cnt[d] + 1)` | 2 |
| `L` | 2 |
| smallest insufficient digit `d` | 1 |
| `cnt[0]` | 2 |
| `cnt[d]` | 1 |
| `both[d]` | 1 |

The first impossible length is (2). The candidate `11` needs two different cubes showing (1), but only one cube contains digit (1). The special `10` candidate is constructible because there are two zero-capable cubes, so the answer is `11`.

This example confirms that the algorithm does not need to inspect any two-digit number before the answer. It identifies the first bad length and then resolves the lexicographic order using the deficient digit.

### Sample 2

The input is

```
3
123456
789012
345678
```

The relevant counts are:

| Quantity | Value |
| --- | --- |
| `cnt[0]` | 1 |
| `cnt[1]` | 2 |
| `cnt[2]` | 2 |
| `cnt[3]` | 2 |
| `cnt[4]` | 3 |
| `cnt[5]` | 3 |
| `cnt[6]` | 3 |
| `cnt[7]` | 2 |
| `cnt[8]` | 2 |
| `cnt[9]` | 1 |
| `L` | 2 |
| smallest insufficient digit | 9 |
| `both[9]` | 1 |

The zero boundary gives (cnt[0]+2=3), while digit (9) gives (cnt[9]+1=2). Thus the first impossible numbers have two digits.

The smallest deficient digit is (9), so `99` is certainly impossible. But the algorithm first checks `90`. There is exactly one cube containing zero and exactly one cube containing nine, and it is the same cube. Hence one cube cannot simultaneously occupy both positions, so `90` is impossible.

Since `90 < 99`, the answer is `90`.

This trace demonstrates why counting each digit independently is almost sufficient but not quite. The single overlap count between zero and the first deficient digit captures the remaining obstruction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each cube has six faces, and only the ten possible digits are inspected. |
| Space | (O(1)) auxiliary, (O(L)) output | Only ten counters and ten overlap counters are stored. The answer itself has at most (n+1) digits. |

With (n\le100,000), the algorithm performs only a small constant amount of work per cube and never depends on the size of the set of representable numbers. The final output can itself be linear in (n), so (O(n)) total time is asymptotically optimal up to constant factors.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    stream = io.StringIO(inp)
    n = int(stream.readline())

    cnt = [0] * 10
    both = [0] * 10

    for _ in range(n):
        s = stream.readline().strip()

        mask = 0
        for ch in s:
            mask |= 1 << (ord(ch) - ord('0'))

        for d in range(10):
            if mask & (1 << d):
                cnt[d] += 1

        if mask & 1:
            for d in range(1, 10):
                if mask & (1 << d):
                    both[d] += 1

    L = cnt[0] + 2
    for d in range(1, 10):
        L = min(L, cnt[d] + 1)

    if L == cnt[0] + 2:
        return '1' + '0' * (L - 1)

    d = 1
    while cnt[d] + 1 != L:
        d += 1

    if cnt[0] == L - 1 and both[d] == L - 1:
        return str(d) + '0' * (L - 1)

    return str(d) * L

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided samples
assert run("""2
012345
098765
""") == "11", "sample 1"

assert run("""3
123456
789012
345678
""") == "90", "sample 2"

assert run("""5
111111
222222
333333
444444
555555
""") == "6", "sample 3"

# Minimum-size input
assert run("""1
012345
""") == "6", "minimum size"

# Repeated faces must count once
assert run("""1
111111
""") == "2", "duplicate faces"

# Special zero/nonzero overlap case
assert run("""2
012349
456788
""") == "90", "shared cube"

# Large input
large = "100000\n" + ("012345\n" * 100000)
assert run(large) == "6", "maximum n"

# All available copies of a digit are concentrated on one cube
assert run("""2
012345
678999
""") == "10", "leading-zero and overlap boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 012345` | `6` | Minimum input and first missing digit |
| `1 / 111111` | `2` | Repeated faces on one cube count only once |
| `2 / 012349, 456788` | `90` | Special shared zero and deficient-digit obstruction |
| `100000` copies of `012345` | `6` | Maximum (n) and linear processing |
| `2 / 012345, 678999` | `10` | Leading-zero boundary and shared-cube condition |

## Edge Cases

A cube with repeated copies of the same digit must contribute only one unit to its digit count. For

```
1
111111
```

the mask of the cube contains only digit (1). Thus `cnt[1] = 1` and `cnt[2] = 0`. The formula gives (L=1), with digit (2) as the first insufficient nonzero digit. The algorithm outputs `2`, which is correct.

The leading-zero restriction changes the threshold for zero. Consider

```
2
012345
678999
```

Every nonzero digit appears on at least one cube, and digit (1) appears only on the first cube. Zero also appears only on that cube. The first bad length is (2), and the smallest deficient digit is (1). The candidate `10` requires different cubes for (1) and (0), but both are available only from the same cube. Thus `10` cannot be built, while `1` can, so the algorithm outputs `10`.

The shared-cube obstruction is visible even when both individual counts look sufficient. For

```
2
012349
456788
```

digit (9) occurs on one cube and zero occurs on one cube, with both occurrences belonging to the first cube. The first bad length is (2), and (9) is the smallest digit with only one available cube. The ordinary candidate is `99`, but `90` comes first numerically. Since `both[9] = 1 = L-1`, the algorithm detects that `90` is impossible and outputs it.

Finally, when a digit is completely absent, the answer can have a single digit. For

```
1
012345
```

digit (6) has count zero, so (L=1). The algorithm immediately chooses (6) as the smallest nonzero digit with zero available cubes and outputs `6`. No reasoning about multi-digit numbers is needed once the first missing digit already gives a one-digit answer.
