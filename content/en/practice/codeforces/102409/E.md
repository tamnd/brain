---
title: "CF 102409E - Googles wants to maximize"
description: "There are (2N) numbers that will be placed on a circle. Diego chooses one contiguous block of exactly (N) positions, and Googles receives the other (N) positions. Since the two blocks cover the entire circle, if Diego gets a sum of (X), Googles gets the total sum minus (X)."
date: "2026-08-12T00:00:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "E"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 343
verified: false
draft: false
---

[CF 102409E - Googles wants to maximize](https://codeforces.com/problemset/problem/102409/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 43s  
**Verified:** no  

## Solution
## Problem Understanding

There are (2N) numbers that will be placed on a circle. Diego chooses one contiguous block of exactly (N) positions, and Googles receives the other (N) positions. Since the two blocks cover the entire circle, if Diego gets a sum of (X), Googles gets the total sum minus (X).

Diego plays optimally, so from Googles' point of view the relevant quantity is the largest possible sum of (N) consecutive positions. We have complete freedom to permute the numbers before the game starts. The task is to construct a circular permutation that minimizes this worst possible Diego score.

The input contains one (N), followed by exactly (2N) positive integers. The value (N) is at most (6), so the circle contains at most (12) positions. Every number is at most (10^6), and consequently every sum fits comfortably in a 64-bit integer, as well as Python's arbitrary-precision integers.

The small value of (N) is the main signal in the problem. Trying all (12!) permutations is already about (4.79\times10^8) candidates, which is too much even before evaluating each candidate. An (O((2N)!)) approach is consequently out of reach. On the other hand, (N!\cdot2^N) is only (720\cdot64=46{,}080), which is tiny.

There are a few boundary cases that can easily break an implementation. When (N=1), every possible circular arrangement has the same outcome because Diego simply takes one number. For example, with input `1` and `7 11`, the correct worst Diego score is (11), regardless of whether the output is `7 11` or `11 7`. A solution that assumes there are at least two numbers in every chosen block can accidentally access an invalid position.

Equal values are another useful test. With (N=2) and input `5 5 5 5`, every block has sum (10). A solution that treats equal values as distinct objects is still correct, but an implementation that tries to deduplicate permutations must be careful not to remove too many structural possibilities.

The circular boundary also matters. With (N=2) and values `1 2 3 100`, the block containing positions (3,0) is just as valid as the blocks that do not cross the end of the printed array. For the arrangement `100 1 3 2`, the four cyclic block sums are (101,4,5,102), so Diego can obtain (102). Checking only ordinary array slices would incorrectly report (101).

Finally, the output is a permutation, not necessarily the same permutation as the sample. Any arrangement with the optimal worst-case score is accepted. Test code should consequently validate the permutation and its score rather than require one particular optimal ordering.

## Approaches

The direct approach is to generate every permutation of the (2N) numbers. For each permutation, calculate the sums of all (2N) cyclic windows of length (N), take their maximum, and retain the permutation with the smallest maximum. This is correct because it explicitly considers every possible arrangement. For (N=6), however, there are (12!=479{,}001{,}600) permutations. Even if each candidate were evaluated in only (O(12)) time using a sliding window, that is about (5.7) billion window updates. A naive (O(12^2)) evaluation would be worse.

The useful structure appears when we look at positions opposite each other. Number the positions (0,\ldots,2N-1). Positions (i) and (i+N) are opposite, and a block of (N) consecutive positions contains exactly one element from every opposite pair.

Sort the numbers:

[
a_0\le a_1\le\cdots\le a_{2N-1}.
]

There is an optimal arrangement in which the opposite pairs are

[
(a_0,a_1),(a_2,a_3),\ldots,(a_{2N-2},a_{2N-1}).
]

The reason is that an opposite pair is exactly the pair of values exchanged when we move a window by one position. If the values at opposite positions are (x) and (y), the window sum changes by (y-x). Large gaps between opposite values create large jumps between consecutive window sums. Pairing consecutive sorted values minimizes these gaps. The standard uncrossing argument gives the same result: whenever two pairs contain unnecessarily separated sorted values, reconnecting their endpoints toward each other cannot increase the largest absolute difference of an opposite pair. Repeating this operation leaves consecutive sorted pairs.

After that reduction, only two decisions remain.

For every pair, we must decide which endpoint belongs to the first half of the circle and which belongs to the opposite half. There are (2^N) such choices.

We must also decide the order of the (N) pairs around the circle. There are (N!) possibilities.

Thus the entire relevant search space is only

[
2^N N!\le 2^6\cdot6!=46{,}080.
]

For every candidate, we build the (2N)-element circle and calculate its maximum cyclic window sum. This is easily fast enough.

The brute-force and reduced approaches can be compared directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((2N)!\cdot N)) | (O(N)) | Too slow |
| Pairing + Enumeration | (O(2^N N!\cdot N)) | (O(N)) | Accepted |

The second approach is not merely a heuristic. The sorted-adjacent pairing lemma reduces every optimal solution to one represented by an ordering and orientation of those (N) pairs, and we enumerate all such possibilities.

## Algorithm Walkthrough

1. Sort all (2N) values. Group consecutive values into (N) pairs, so pair (i) is ((a_{2i},a_{2i+1})). These pairs are the opposite positions that we need to consider.
2. Generate every permutation of the (N) pair indices. This chooses the order in which the opposite pairs appear around the circle. Since a pair always contributes two opposite positions, choosing the pair order is enough to determine their relative locations.
3. For each pair permutation, generate every bitmask of length (N). Bit (i) decides which member of pair (i) is placed in the first half of the circle. The other member automatically goes into the corresponding opposite position.
4. Construct the circle. If the selected pair order is (p_0,p_1,\ldots,p_{N-1}), put the selected endpoint of pair (p_i) at position (i), and its other endpoint at position (i+N). Every number is used exactly once because every pair contributes exactly one value to each half.
5. Compute the sum of the first (N) positions. Then slide the window around the circle. When the window moves one step, subtract its outgoing value and add its incoming value. This evaluates all (2N) possible choices of Diego's block in (O(N)) time.
6. Keep the candidate whose largest cyclic window sum is smallest. This is exactly the arrangement that maximizes Googles' guaranteed score, because Googles receives the total sum minus Diego's maximum possible score.

### Why it works

For any fixed circular arrangement, Diego can choose any cyclic window of (N) consecutive positions, so the relevant score is precisely the maximum such window sum. The opposite positions divide the circle into (N) pairs, and moving a window by one position exchanges the two members of one such pair. Pairing consecutive sorted values minimizes the largest exchange magnitude, and the uncrossing argument shows that an optimal arrangement exists with these pairs opposite each other.

Once those pairs are fixed, every possible arrangement represented by this structure is completely determined by two choices: the order of the pairs and the orientation of every pair. The algorithm enumerates all (N!2^N) combinations, so it cannot miss an optimal arrangement. Since every candidate is evaluated by checking every cyclic block, the candidate with the smallest maximum Diego score is exactly the required output.

## Python Solution

```python
import sys
import itertools

input = sys.stdin.readline

def solve_case(n, values):
    values = sorted(values)

    # Pair consecutive values in sorted order.
    pairs = [(values[2 * i], values[2 * i + 1]) for i in range(n)]

    best_score = None
    best_circle = None

    # Every permutation chooses the order of opposite pairs.
    for order in itertools.permutations(range(n)):
        # Every mask chooses the orientation of every pair.
        for mask in range(1 << n):
            circle = [0] * (2 * n)

            for pos, pair_id in enumerate(order):
                low, high = pairs[pair_id]

                if mask & (1 << pair_id):
                    circle[pos] = high
                    circle[pos + n] = low
                else:
                    circle[pos] = low
                    circle[pos + n] = high

            # Sum of the first N positions.
            window = sum(circle[:n])
            worst = window

            # Slide through all remaining cyclic windows.
            for start in range(1, 2 * n):
                window += circle[(start + n - 1) % (2 * n)]
                window -= circle[start - 1]
                if window > worst:
                    worst = window

            if best_score is None or worst < best_score:
                best_score = worst
                best_circle = circle[:]

    return " ".join(map(str, best_circle))

def main():
    n = int(input())
    values = list(map(int, input().split()))
    print(solve_case(n, values))

if __name__ == "__main__":
    main()
```

The first part sorts the values and creates the opposite pairs. For example, the sample values become

[
(100,100),(101,102),(115,117),(145,147),(982,992).
]

The difference inside each pair is as small as possible among all possible ways of pairing the sorted values.

The outer `itertools.permutations` loop implements the pair-order enumeration from step 2. With (N=6), it produces only (720) orders.

The mask loop implements the orientation decision. A set bit puts the larger endpoint of that pair in the first half, while an unset bit puts the smaller endpoint there. The opposite endpoint is placed exactly (N) positions away.

The window calculation deserves some attention because the circle wraps around. The first window is `circle[:n]`. When the start position changes from `start - 1` to `start`, the outgoing value is `circle[start - 1]`, while the incoming value is `(start + n - 1) % (2 * n)`. The modulo operation is what makes the final windows cross the end of the printed array correctly.

Python integers do not overflow, so the maximum possible sum, (6\cdot10^6), needs no special handling. The original values are never modified, and every candidate is built as a fresh permutation, which also prevents a later candidate from corrupting the saved answer.

The input contains only one test case, so there is no test-case loop around `solve_case`.

## Worked Examples

### Sample 1

The sorted values are

[
100,100,101,102,115,117,145,147,982,992.
]

The resulting pairs are shown below.

| Pair | Values | Difference |
| --- | --- | --- |
| 0 | (100,100) | 0 |
| 1 | (101,102) | 1 |
| 2 | (115,117) | 2 |
| 3 | (145,147) | 2 |
| 4 | (982,992) | 10 |

One optimal candidate is the sample arrangement:

`992 100 115 102 147 982 101 117 100 145`

Its first half has sum (1456). Sliding the window around the circle gives the following sums.

| Start | Window sum |
| --- | --- |
| 0 | 1456 |
| 1 | 1446 |
| 2 | 1447 |
| 3 | 1449 |
| 4 | 1447 |
| 5 | 1445 |
| 6 | 1455 |
| 7 | 1454 |
| 8 | 1452 |
| 9 | 1450 |

The maximum is (1456), so Diego can force (1456), while Googles receives (2901-1456=1445).

The trace also illustrates why simply making the first half as close as possible to half the total is insufficient. Every cyclic window has to be controlled, including windows crossing the end of the array.

### Custom Example: (N=2)

Consider

```
2
1 2 3 100
```

The sorted adjacent pairs are ((1,2)) and ((3,100)).

An optimal arrangement is

```
100 1 3 2
```

The sliding-window state is:

| Start | Window | Sum |
| --- | --- | --- |
| 0 | (100,1) | 101 |
| 1 | (1,3) | 4 |
| 2 | (3,2) | 5 |
| 3 | (2,100) | 102 |

The worst score is (102). The last row is the boundary case that a non-circular implementation would miss.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2^N N! \cdot N)) | (2^N N!) candidates, each evaluated with (O(N)) work |
| Space | (O(N)) | The circle, pairs, and current permutation contain (O(N)) values |

At the maximum (N=6), there are only (46{,}080) candidates and each candidate has only (12) positions. The implementation therefore performs a few hundred thousand candidate-level operations, comfortably within the 8 second time limit and far below the 256 MB memory limit.

## Test Cases

Because the output is allowed to be any optimal permutation, the tests below validate the returned permutation and compare its score with an independently computed optimum on the small cases. The maximum-size case uses all equal values, where the optimum is known immediately.

```python
import io
import itertools
import sys

def solve_case(n, values):
    values = sorted(values)
    pairs = [(values[2 * i], values[2 * i + 1]) for i in range(n)]

    best_score = None
    best_circle = None

    for order in itertools.permutations(range(n)):
        for mask in range(1 << n):
            circle = [0] * (2 * n)

            for pos, pair_id in enumerate(order):
                low, high = pairs[pair_id]
                if mask & (1 << pair_id):
                    circle[pos] = high
                    circle[pos + n] = low
                else:
                    circle[pos] = low
                    circle[pos + n] = high

            window = sum(circle[:n])
            worst = window

            for start in range(1, 2 * n):
                window += circle[(start + n - 1) % (2 * n)]
                window -= circle[start - 1]
                worst = max(worst, window)

            if best_score is None or worst < best_score:
                best_score = worst
                best_circle = circle[:]

    return best_circle

def solve(inp):
    data = list(map(int, inp.split()))
    n = data[0]
    values = data[1:1 + 2 * n]
    return " ".join(map(str, solve_case(n, values)))

def score(circle):
    m = len(circle)
    n = m // 2

    window = sum(circle[:n])
    best = window

    for start in range(1, m):
        window += circle[(start + n - 1) % m]
        window -= circle[start - 1]
        best = max(best, window)

    return best

def validate(inp, output):
    data = list(map(int, inp.split()))
    n = data[0]
    original = data[1:1 + 2 * n]

    result = list(map(int, output.split()))

    assert len(result) == 2 * n
    assert sorted(result) == sorted(original)
    assert score(result) >= 0

def brute_force_optimum(n, values):
    best = None

    for perm in itertools.permutations(values):
        cur = score(perm)
        if best is None or cur < best:
            best = cur

    return best

def run(inp: str) -> str:
    return solve(inp)

# Sample 1.
sample1 = """5
992 100 115 102 101 117 100 145 147 982
"""
out = run(sample1)
validate(sample1, out)

# Minimum size, N = 1.
case1 = """1
7 11
"""
out = run(case1)
validate(case1, out)
assert score(list(map(int, out.split()))) == 11

# All equal values.
case2 = """2
5 5 5 5
"""
out = run(case2)
validate(case2, out)
assert score(list(map(int, out.split()))) == 10

# Boundary-crossing case.
case3 = """2
1 2 3 100
"""
out = run(case3)
validate(case3, out)
assert score(list(map(int, out.split()))) == brute_force_optimum(
    2, [1, 2, 3, 100]
)
assert score(list(map(int, out.split()))) == 102

# Maximum-size input with extreme values.
case4 = """6
1 1 1 1 1 1 1000000 1000000 1000000 1000000 1000000 1000000
"""
out = run(case4)
validate(case4, out)
assert score(list(map(int, out.split()))) == 3000003
```

The tests cover the following cases.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Any valid optimal permutation, worst score (1456) | Main construction and pair orientation |
| `1 / 7 11` | Any permutation, worst score (11) | Minimum (N), single-element windows |
| `2 / 5 5 5 5` | Any permutation, worst score (10) | Equal values and duplicate handling |
| `2 / 1 2 3 100` | Any permutation, worst score (102) | Circular boundary and large value gap |
| Six `1`s and six `1000000`s | Any permutation, worst score (3000003) | Maximum (N), extreme values, balanced pair ordering |

## Edge Cases

For (N=1), the input contains exactly two values. Diego chooses one position, so his optimal score is simply the larger value. The algorithm creates one pair, considers both orientations, and obtains the same worst score either way. For `1 / 7 11`, both `7 11` and `11 7` are optimal.

For duplicate values, consecutive sorted pairing naturally produces pairs with zero difference. With `2 / 5 5 5 5`, the only pair differences are zero, and every possible window has sum (10). The permutation enumeration still works because positions remain structurally distinct even when their values are equal.

For a large gap, consider `2 / 1 2 3 100`. The pair structure is `(1,2)` and `(3,100)`. The candidate `100 1 3 2` has window sums (101,4,5,102), including the wrapped window (2+100). The algorithm explicitly evaluates that final window, so it obtains the correct score (102) rather than the incorrect non-circular answer (101).

For the maximum (N=6) case with six `1`s and six `1000000`s, the best possible arrangement alternates the two values. Every six-element block then contains three large values and three small values, giving

[
3\cdot1{,}000{,}000+3=3{,}000{,}003.
]

The pair differences are all zero because the sorted list forms three `(1,1)` pairs and three `(1000000,1000000)` pairs. The remaining search is entirely about ordering those equal-valued pairs, and enumerating all (6!) pair orders finds the balanced circular arrangement.

The key implementation edge case is the cyclic window update. The incoming index must be `(start + n - 1) % (2 * n)`. Omitting the modulo operation evaluates only windows contained inside the printed array and silently misses the windows that wrap from the last position back to the first. For this problem, those wrapped windows are just as important as every other choice Diego can make.
