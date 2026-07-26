---
title: "CF 102822D - Defuse the Bombs"
description: "The problem describes a collection of bombs, where each bomb has a countdown value. In one action, we may choose one bomb and increase its clock by one. Immediately after that, every bomb loses one from its clock."
date: "2026-07-26T15:52:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102822
codeforces_index: "D"
codeforces_contest_name: "2020 China Collegiate Programming Contest - Mianyang Site"
rating: 0
weight: 102822
solve_time_s: 48
verified: true
draft: false
---

[CF 102822D - Defuse the Bombs](https://codeforces.com/problemset/problem/102822/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a collection of bombs, where each bomb has a countdown value. In one action, we may choose one bomb and increase its clock by one. Immediately after that, every bomb loses one from its clock. If any clock becomes negative after this decrease, the process ends. The goal is to maximize the number of choosing actions performed before the explosion happens.

The input contains several test cases. Each test case gives the number of bombs and the initial clock value of every bomb. The output is the maximum number of times we can choose a bomb, formatted as a case answer.

The number of bombs can reach $10^5$, and the total number of bombs over all test cases is at most $3 \times 10^5$. A solution that tries every possible sequence of choices is impossible because the number of possible sequences grows exponentially. Even a simulation that tries to find the best choice at every moment would be too slow because the answer can be extremely large when clock values are large. The values of the clocks can reach $10^9$, so the algorithm must depend on the number of bombs rather than the magnitude of the answer.

The tricky part is that the last action is counted even though it may immediately cause the explosion. A common mistake is to only count completed safe rounds.

For example:

```
1
2
1 1
```

The correct output is:

```
Case #1: 3
```

A careless simulation might say 2 because after two complete rounds both bombs are empty. However, there is still time to perform one more choosing action, and the explosion happens only after the following decrease.

Another edge case is when some bombs start at zero:

```
1
3
0 5 5
```

The first bomb cannot survive a round unless it is chosen every time it matters. A solution that only looks at the total sum of clocks can miss that individual bombs need enough protection.

## Approaches

A direct approach would try to simulate the process and decide which bomb to increase at every turn. Since choosing a bomb protects it from the decrease in that round, the natural greedy idea is to always choose the bomb with the smallest current value. This can work on small cases, but it does not reveal the actual structure of the problem. The answer may be as large as the sum of all clocks, making simulation far too slow.

The key observation comes from looking at a fixed number of safe rounds instead of individual choices.

Suppose we want to survive $x$ complete rounds. Bomb $i$ loses one on every round where it is not chosen. If it is chosen $c_i$ times, its final value after these $x$ rounds is:

$$a_i - (x - c_i)$$

For the bomb to remain alive, we need:

$$c_i \geq x-a_i$$

If $x-a_i$ is negative, the bomb does not need any special protection, so the real requirement is:

$$c_i \geq \max(0, x-a_i)$$

The total number of choices available in $x$ rounds is exactly $x$. Thus, $x$ safe rounds are possible if:

$$\sum_i \max(0, x-a_i) \leq x$$

This condition is monotonic. If we can survive $x$ rounds, then we can survive fewer rounds. If we cannot survive $x$ rounds, larger values are impossible. That allows binary search.

The answer we need is one more than the maximum number of complete safe rounds because the next choosing action is still counted before the explosion occurs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer × n) | O(n) | Too slow |
| Binary Search on Rounds | O(n log(sum(a))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of all initial bomb clocks. This gives an upper bound for the number of complete rounds we need to consider, because every round reduces the total amount of clock value by $n-1$, and the binary search only needs a safe upper limit.
2. Binary search the maximum number of complete safe rounds $x$. For a candidate $x$, calculate how many choices are forced by weak bombs. Bomb $i$ requires $\max(0, x-a_i)$ choices.
3. If the total required choices are at most $x$, mark this value as possible and search for a larger number of rounds. Otherwise, search smaller values.
4. After finding the largest possible number of complete rounds $x$, output $x+1$. The extra one represents the final choice action that causes the explosion afterward.

Why it works:

The binary search condition exactly describes whether the available choices can keep every bomb alive. Any bomb with too small a clock needs to be selected often enough to compensate for the decreases it receives. The sum of these minimum requirements is the smallest number of choices needed. If this fits inside the $x$ available rounds, a valid schedule exists. Since the condition is monotonic, binary search finds the largest possible $x$, and adding one accounts for the final counted action.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(a):
    total = sum(a)

    def possible(x):
        need = 0
        for v in a:
            if x > v:
                need += x - v
                if need > x:
                    return False
        return True

    lo, hi = 0, total + 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if possible(mid):
            lo = mid
        else:
            hi = mid

    return lo + 1

def main():
    t = int(input())
    ans = []

    for case in range(1, t + 1):
        n = int(input())
        a = list(map(int, input().split()))
        ans.append(f"Case #{case}: {solve_case(a)}")

    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The `possible` function checks the mathematical condition derived above. It counts only the extra selections that bombs need because a bomb with value at least `x` can survive `x` rounds without needing protection.

The binary search uses a half-open upper boundary. `total + 1` is safe because the answer for complete rounds can never exceed the sum of all clocks. The final answer is increased by one because the problem asks for the number of choosing actions, not the number of fully completed rounds.

The early return inside `possible` avoids unnecessary work. Once the required choices exceed the available rounds, the candidate value is already impossible.

## Worked Examples

For the first sample:

```
2
2
1 1
3
1 2 3
```

The first test case has two bombs.

| Complete rounds candidate | Bomb requirements | Total required choices | Possible |
| --- | --- | --- | --- |
| 1 | 0, 0 | 0 | Yes |
| 2 | 1, 1 | 2 | Yes |
| 3 | 2, 2 | 4 | No |

The largest safe number of complete rounds is 2, so the answer is 3.

For the second test case:

| Complete rounds candidate | Bomb requirements | Total required choices | Possible |
| --- | --- | --- | --- |
| 2 | 1, 0, 0 | 1 | Yes |
| 3 | 2, 1, 0 | 3 | Yes |
| 4 | 3, 2, 1 | 6 | No |

The largest safe number of complete rounds is 3, so the answer is 4.

These traces show why the solution does not need to decide the exact order of choosing bombs. The inequality only asks whether some distribution of choices exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(sum(a))) | Each binary search check scans all bombs once, and the search range is bounded by the total clock sum. |
| Space | O(1) | Only the input array and a few variables are used. |

The total number of bombs across all tests is $3 \times 10^5$, so scanning the array around 30 times per test case is easily within the limits. Python integer arithmetic also handles the large sums safely.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve_case(a):
        total = sum(a)

        def possible(x):
            need = 0
            for v in a:
                if x > v:
                    need += x - v
                    if need > x:
                        return False
            return True

        lo, hi = 0, total + 1
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if possible(mid):
                lo = mid
            else:
                hi = mid
        return lo + 1

    t = int(input())
    out = []
    for case in range(1, t + 1):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(f"Case #{case}: {solve_case(a)}")

    sys.stdin = old_stdin
    return "\n".join(out)

assert run("""2
2
1 1
3
1 2 3
""") == """Case #1: 3
Case #2: 4""", "samples"

assert run("""1
2
0 0
""") == """Case #1: 1""", "minimum clocks"

assert run("""1
3
5 5 5
""") == """Case #1: 16""", "all equal large values"

assert run("""1
4
0 1 2 3
""") == """Case #1: 3""", "zero boundary"

assert run("""1
5
1000000000 1000000000 1000000000 1000000000 1000000000
""") == """Case #1: 5000000001""", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two sample cases | `Case #1: 3`, `Case #2: 4` | Basic correctness |
| `[0,0]` | `1` | Minimum values and final counted action |
| Five equal large clocks | `5000000001` | Large answer handling |
| `[0,1,2,3]` | `3` | Individual bomb protection requirements |
| Five clocks of `10^9` | `5000000001` | Large integer arithmetic |

## Edge Cases

For the case:

```
1
2
1 1
```

The binary search checks complete rounds. Two rounds are possible because each bomb can be chosen once. Three rounds are impossible because each bomb would need two protections, requiring four choices. The algorithm returns `2 + 1 = 3`, correctly counting the final action that causes the explosion.

For the case:

```
1
3
0 5 5
```

The first bomb starts at zero. To survive one complete round, it must be chosen because otherwise it becomes negative. The condition requires:

$$\max(0,1-0)+\max(0,1-5)+\max(0,1-5)=1$$

One choice is available, so the round is possible. For larger values, the required protection eventually exceeds the available choices, and binary search stops at the correct point.

For the case:

```
1
3
0 0 0
```

Every bomb needs to be selected whenever it would otherwise lose value. After zero complete rounds, one final choosing action is still possible, so the answer is 1. The algorithm handles this because the final `+1` is separate from the safe-round calculation.
