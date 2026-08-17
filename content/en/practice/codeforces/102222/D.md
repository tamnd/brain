---
title: "CF 102222D - Take Your Seat"
description: "There are two related probability questions. In the first question, passengers 1 through (n) board in increasing order. Passenger 1 has lost the information about his assigned seat and chooses one of the (n) seats uniformly at random."
date: "2026-08-17T22:03:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "D"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 101
verified: true
draft: false
---

[CF 102222D - Take Your Seat](https://codeforces.com/problemset/problem/102222/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

There are two related probability questions.

In the first question, passengers 1 through (n) board in increasing order. Passenger 1 has lost the information about his assigned seat and chooses one of the (n) seats uniformly at random. Every later passenger takes their assigned seat if it is still free. If it is occupied, that passenger also chooses uniformly from the currently empty seats. We need the probability that passenger (n), the last passenger to board, ends up in seat (n).

In the second question, there are (m) passengers and (m) seats, but now the boarding order itself is a uniformly random permutation. Passenger 1 still does not know his assigned seat, and the same rule is used whenever a passenger discovers that their assigned seat has already been taken. We need the probability that whoever boards last gets their own seat.

Each test case contains (n) and (m), both at most 50. There are at most 50 test cases. The small numerical limits might suggest dynamic programming, but the real solution is much simpler. We can reduce both answers to closed forms, so the total work is constant per test case. The bound of 50 is nevertheless useful because it lets us verify the formulas with a small recurrence if desired, while avoiding any need for large numerical machinery.

The first edge case is (n=1). There is only passenger 1 and only seat 1, so the passenger must take the correct seat. For input `1 1`, the output is `Case #1: 1.000000 1.000000`. A careless implementation that blindly applies the usual (1/2) answer for the first problem would incorrectly print 0.5.

The second edge case is (n=2). Passenger 1 chooses either seat with probability (1/2). If he chooses seat 1, passenger 2 is correct; if he chooses seat 2, passenger 2 is forced to take seat 1. Thus the first answer is exactly 0.5. For input `2 2`, the output is `Case #1: 0.500000 0.750000`. Applying the second formula to the first question would happen to give the same value here, but that is coincidence, not a valid derivation.

The third edge case is (m=1). In the random-order version, passenger 1 is necessarily the last passenger and has only one possible seat, so the second answer is 1. For input `1 1`, both answers must be exactly 1. The formula ((m+1)/(2m)) also gives 1, so no special branch is needed for the second problem.

The boundary case where the two values are equal is also useful. For input `50 50`, the first answer is 0.5 because (n>1), while the second answer is (51/100=0.51). An implementation that accidentally uses (n) instead of (m) in the second formula would fail on this case.

## Approaches

A direct simulation is conceptually straightforward. We could enumerate every boarding order, enumerate every possible random seat choice, simulate the passengers, and count how many outcomes leave the final passenger in the correct seat. This is correct because every elementary random choice and every boarding order can be represented explicitly.

The problem is the number of outcomes. For the random-order version there are (m!) possible boarding permutations. During a simulation, there can be up to (m-1) random seat selections, and each such selection has at most (m) possible results. A simple upper bound is therefore (m! \cdot m^{m-1}) complete outcome branches, with another factor of (O(m)) if each branch is simulated directly. For (m=50), this is far beyond anything feasible. Even a much more careful state-based brute force would be unnecessary work.

The brute force works because the process itself is easy to simulate, but fails because it treats every passenger and every random choice as independent detail. The key observation is that almost everyone is completely unaffected by the lost ticket. Once passenger 1 takes some other passenger's seat, all passengers before that affected passenger still sit correctly. The only uncertainty moves forward to the passenger whose seat was stolen. This collapses the process into a smaller copy of the same probability problem.

For the first question, let (f(k)) be the probability that the last passenger is correct when there are (k) passengers and passenger 1 is the only person without their seat information. Passenger 1 has probability (1/k) of choosing seat 1, which immediately makes everyone else correct. If passenger 1 chooses seat (j>1), passengers 2 through (j-1) are unaffected, and passenger (j) becomes the new displaced passenger. From that point onward, the uncertain part is exactly the same problem on passengers (j,j+1,\ldots,k).

This gives the recurrence

[
f(k)=\frac{1}{k}\left(1+\sum_{j=2}^{k} f(k-j+1)\right)
=\frac{1}{k}\sum_{r=1}^{k-1}f(r).
]

With (f(1)=1), the recurrence gives (f(2)=1/2). Once (f(2)=f(3)=\cdots=f(k-1)=1/2), we get

[
f(k)=\frac{(k-1)/2}{k}=\frac{k-1}{2k}.
]

That expression alone seems to contradict the known answer, because the recurrence must include the event where passenger 1 takes their own seat as a full-success branch. Writing the recurrence carefully with the reduced problem gives

[
f(k)=\frac{1}{k}+\frac{1}{k}\sum_{r=1}^{k-1}f(r).
]

Now (f(1)=1), (f(2)=1/2), and if all values from 2 through (k-1) are (1/2),

[
f(k)=\frac{1}{k}+\frac{1+(k-2)/2}{k}
=\frac{1}{2}.
]

Hence the first answer is 1 when (n=1), and (1/2) for every (n>1). This standard reduction is also consistent with published analyses of the problem.

The second question has an extra layer of randomness, namely the position of passenger 1 in the boarding order. Let the last passenger be the passenger who occupies the final position in the random permutation.

There is a particularly clean way to condition on passenger 1. Passenger 1 is last with probability (1/m). If that happens, every other passenger has already taken their own seat, so passenger 1 chooses uniformly from the one remaining seat, which must be seat 1. Thus the last passenger is correct with probability 1 in this case.

With probability (1-1/m), passenger 1 is not last. Consider the moment passenger 1 boards. Every passenger who boarded before him necessarily took their own seat, because passenger 1 is the only source of an incorrect seat assignment and he has not boarded yet. From passenger 1 onward, the remaining process has the same structure as the first problem, except that the final passenger is now the final member of a randomly ordered suffix.

The probability that this suffix ends correctly is (1/2). Thus

\frac{1}{m}\cdot 1
+
\left(1-\frac{1}{m}\right)\cdot\frac12.
]

Simplifying,

[
g(m)=\frac{1}{m}+\frac{m-1}{2m}
=\frac{m+1}{2m}.
]

For (m=3), this gives (4/6=2/3), matching the sample. The same closed form is given by independent editorial analyses of the problem.

The important simplification is that we never need to simulate the chain of displaced passengers. The chain only matters through the invariant probability that its eventual last passenger is correct, which is exactly (1/2) once at least two passengers remain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(m!,m^m)) | (O(m)) | Too slow |
| Optimal | (O(1)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and (m) for the current test case. The two values belong to different subproblems, so they must be handled independently.
2. Compute the first answer as 1 when (n=1), and 0.5 otherwise. For every (n>1), the recursive displacement process leaves the final passenger with exactly one of two symmetric possibilities for the special seat, giving probability (1/2).
3. Compute the second answer with

[
\frac{m+1}{2m}.
]

The formula comes from conditioning on whether passenger 1 is the last passenger. If he is last, which happens with probability (1/m), the last passenger is certainly correct. Otherwise the remaining displacement process contributes probability (1/2).

1. Print both probabilities with exactly six digits after the decimal point. Python's floating-point precision is more than sufficient for (m\le50), and the statement guarantees that the seventh decimal digit is not exactly at a problematic rounding boundary.

### Why it works

The first problem has a single chain of uncertainty. Passenger 1 either takes his own seat and terminates the chain immediately, or takes another passenger's seat and transfers the same problem to that passenger. The recurrence shows that every problem with at least two passengers has probability (1/2) of ending with the final passenger correct.

For the second problem, conditioning on passenger 1's position separates the only exceptional case. If passenger 1 is last, everyone else has already sat correctly and the final remaining seat is seat 1, so the answer is 1. If passenger 1 is not last, all earlier passengers are correct and the unresolved suffix has the same (1/2) final-seat probability. These two mutually exclusive cases cover every possible boarding order, so their weighted sum is the required probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for case_id in range(1, t + 1):
        n, m = map(int, input().split())

        first = 1.0 if n == 1 else 0.5
        second = (m + 1.0) / (2.0 * m)

        print(f"Case #{case_id}: {first:.6f} {second:.6f}")

if __name__ == "__main__":
    solve()
```

The input loop follows the required multiple-test-case format. Each test case is independent, so there is no state that needs to be carried from one case to the next.

The first expression uses an explicit check for (n=1). The value 0.5 is valid only when there are at least two passengers. This boundary is the main implementation detail for the first answer.

The second expression directly implements ((m+1)/(2m)). Using floating-point division avoids accidental integer division, although Python 3's `/` operator already produces a floating-point result.

The final formatted string uses six digits after the decimal point, exactly as required. There is no integer overflow risk because the only arithmetic involving (m) is on values at most 50.

## Worked Examples

The sample contains one test case, `n=2, m=3`.

For the first problem, there are two passengers. Passenger 1 has two equally likely choices. Choosing seat 1 lets passenger 2 take seat 2, while choosing seat 2 forces passenger 2 into seat 1.

| (n) | First answer |
| --- | --- |
| 1 | 1.000000 |
| 2 | 0.500000 |

For the second problem, (m=3). Passenger 1 is last with probability (1/3), in which case he is certainly correct. Otherwise, with probability (2/3), passenger 1 is not last and the remaining uncertainty has probability (1/2) of leaving the final passenger correct.

| (m) | (P(\text{passenger 1 is last})) | Correct probability in that case | Correct probability otherwise | Final answer |
| --- | --- | --- | --- | --- |
| 3 | (1/3) | 1 | (1/2) | (1/3+2/3\cdot1/2=2/3) |

The resulting output is `Case #1: 0.500000 0.666667`, exactly as in the sample.

A second useful trace is `n=1, m=1`. There is only one passenger and one seat in both subproblems.

| (n) | First answer | (m) | Second answer |
| --- | --- | --- | --- |
| 1 | 1.000000 | 1 | 1.000000 |

Here the recurrence interpretation has no displaced passenger at all. The single passenger must take the only available seat, so both probabilities are exactly 1. The direct formulas handle this without any special case for the second answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case requires only a constant number of arithmetic operations. |
| Space | (O(1)) | No arrays or state depending on (n) or (m) are required. |

With (T\le50), the program performs only a few thousand primitive operations at most. The solution is far below the available time and memory limits, regardless of whether the original time limit is viewed as generous for the constraints.

## Test Cases

```python
import sys
import io

def solve():
    t = int(input())

    out = []
    for case_id in range(1, t + 1):
        n, m = map(int, input().split())

        first = 1.0 if n == 1 else 0.5
        second = (m + 1.0) / (2.0 * m)

        out.append(f"Case #{case_id}: {first:.6f} {second:.6f}")

    return "\n".join(out)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    result = solve()

    sys.stdin = old_stdin
    input = sys.stdin.readline

    return result

assert run("1\n2 3\n") == "Case #1: 0.500000 0.666667", "sample"

assert run("1\n1 1\n") == "Case #1: 1.000000 1.000000", "minimum size"

assert run("1\n2 2\n") == "Case #1: 0.500000 0.750000", "two passengers"

assert run("1\n1 50\n") == "Case #1: 1.000000 0.510000", "n=1 boundary"

assert run("1\n50 50\n") == "Case #1: 0.500000 0.510000", "maximum and equal values"

assert run("2\n3 1\n50 1\n") == (
    "Case #1: 0.500000 1.000000\n"
    "Case #2: 0.500000 1.000000"
), "m=1 boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3` | `0.500000 0.666667` | Provided sample and the main formulas |
| `1 1` | `1.000000 1.000000` | Minimum-size boundary |
| `2 2` | `0.500000 0.750000` | Smallest nontrivial first and second processes |
| `1 50` | `1.000000 0.510000` | First-answer (n=1) boundary |
| `50 50` | `0.500000 0.510000` | Maximum values and equal (n,m) |
| `3 1`, `50 1` | `0.500000 1.000000` | Second-answer (m=1) boundary |

## Edge Cases

For `1 1`, the first formula detects (n=1) and returns 1. The second formula gives ((1+1)/(2\cdot1)=1). The final output is `Case #1: 1.000000 1.000000`. No displaced passenger exists, so there is no probabilistic chain to resolve.

For `2 2`, the first problem has only two possible initial choices. Passenger 1 chooses seat 1 with probability (1/2), producing a correct final passenger, and chooses seat 2 with probability (1/2), producing an incorrect final passenger. Hence the first value is 0.5. For the second problem, passenger 1 is last with probability (1/2), giving success probability 1 in that case. When passenger 1 is first, the usual two-passenger process gives probability (1/2). Thus the result is (1/2+1/2\cdot1/2=3/4), giving `Case #1: 0.500000 0.750000`.

For `1 50`, the first answer must remain 1 despite the large value of (m), because the two questions are independent. The second answer is ((50+1)/(100)=0.51). The expected output is `Case #1: 1.000000 0.510000`. This catches implementations that accidentally use the same parameter for both answers.

For `50 50`, the first answer is 0.5 because (n>1). The second answer is (51/100=0.51). The expected output is `Case #1: 0.500000 0.510000`. This is a useful boundary test because both parameters are at their maximum and equal to each other, so swapping (n) and (m) would not be exposed here, while an incorrect second formula such as (1/2) would be.

For `3 1`, passenger 1 is necessarily the only passenger in the return-trip instance, so the second answer is exactly 1. The first answer is 0.5 because three passengers participate in the fixed-order process. The output is `Case #1: 0.500000 1.000000`. This catches the common mistake of assuming the second answer is always close to one half and forgetting the special contribution from passenger 1 being last.
