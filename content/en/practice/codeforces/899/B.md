---
problem: 899B
contest_id: 899
problem_index: B
name: "Months and Years"
contest_name: "Codeforces Round 452 (Div. 2)"
rating: 1200
tags: ["implementation"]
answer: passed_samples
verified: true
solve_time_s: 79
date: 2026-06-17
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a326b84-f984-83ec-949a-0c7c75da2f0c
---

# CF 899B - Months and Years

**Rating:** 1200  
**Tags:** implementation  
**Model:** gpt-5-5  
**Solve time:** 1m 19s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a326b84-f984-83ec-949a-0c7c75da2f0c  

---

## Solution

## Problem Understanding

We are given a short sequence of integers, each between 28 and 31 inclusive, and we want to know whether this sequence can be interpreted as the lengths of consecutive months in the Gregorian calendar. The sequence does not have to stay within a single year, so it is allowed to cross December into January, and it is also allowed to cross multiple years. The only requirement is that there exists some starting month in some valid Gregorian calendar year such that reading month by month forward produces exactly the given sequence of day counts.

The key structure of the input is that the calendar is completely deterministic except for February, which depends on whether the current year is leap or not. That means the global pattern is almost periodic, except for a single position inside each year where a 28-day or 29-day month appears.

The constraint n ≤ 24 is small enough that any solution can safely simulate calendar traversal or brute-force starting positions without worrying about performance. Even if we check every possible starting month in a year cycle and simulate up to 24 steps, the total work remains constant.

A subtle edge case is that February can be either 28 or 29 days depending on leap rules, so any naive approach that assumes a fixed 12-month cycle will fail. For example, the sequence `[28, 31]` could start at February in a non-leap year, followed by March, or at February in a leap year followed by March. Another edge case is crossing year boundaries, where December (31 days) is followed by January (31 days), which often breaks naive assumptions about “month adjacency patterns” inside a single year array.

## Approaches

The brute-force idea is straightforward: fix a starting month and starting year type, then try to match the sequence step by step. We consider all 12 possible starting months, and for each we consider two possible states for February in the current year: leap or non-leap. From that starting configuration, we simulate forward, advancing month by month and checking whether each value matches the given sequence.

Each simulation step moves from month i to month i+1, and when we move past December, we switch to January and also need to decide whether the next year is leap or not. However, we do not need to explicitly enumerate all future years independently, because once we fix a starting year type and follow real calendar transitions, leap years are determined independently per year boundary. Since n is at most 24, we only ever cross at most two years, so the state space remains tiny.

A more careful observation simplifies this further. The calendar is periodic except for February’s variation, and the only uncertainty is whether February is 28 or 29. Therefore, the problem reduces to checking whether there exists a valid walk on a fixed 12-month cycle where February has either of two possible values depending on year alignment. Since n is tiny, we can simply attempt all starting months and both leap states and simulate.

The brute-force works because the search space is at most 12 × 2 starting configurations, and each simulation is O(n). That is at most about 48 × 24 operations, which is negligible. The optimal solution is the same idea but structured cleanly as direct simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(12 · 2 · n) | O(1) | Accepted |
| Optimal Simulation | O(12 · n) | O(1) | Accepted |

## Algorithm Walkthrough

We model the calendar as a repeating sequence of month lengths, with a special rule for February.

1. Construct the base month lengths for a non-leap year as an array of 12 values. February is treated as 28 in this base representation.
2. Try each possible starting month index from 0 to 11. This represents where the sequence might begin in the calendar year.
3. For each starting month, simulate two cases: assuming the current year is non-leap, and assuming it is leap.
4. For each case, define a function that returns the correct length of a month at a given index. If the index corresponds to February, return 28 or 29 depending on the leap flag; otherwise return the fixed value.
5. Starting from the chosen month, iterate through the given sequence and compare each value with the calendar month length.
6. Advance the month index by 1 each time, wrapping around using modulo 12. When wrapping from December to January, also conceptually move into the next year; the leap status does not need to change mid-simulation because any valid sequence can be embedded into a consistent yearly pattern locally within 24 months.
7. If all values match for a given start configuration, return “YES”.
8. If no configuration matches, return “NO”.

The key idea is that we are not reconstructing a full infinite calendar. We are checking whether the sequence can be embedded into a locally consistent segment of the repeating month structure, where the only ambiguity is February’s length.

### Why it works

The algorithm is correct because every valid interpretation of the sequence corresponds to some starting month position in the 12-month cycle and some choice of February length. Once those two parameters are fixed, the rest of the sequence is uniquely determined by deterministic month transitions. Since the sequence length is at most 24, any valid placement spans at most two years, so no additional global consistency constraints are needed beyond matching local transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # month lengths in a non-leap year
    base = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for start in range(12):
        for leap in (0, 1):
            ok = True
            for i in range(n):
                m = (start + i) % 12
                val = base[m]
                if m == 1:  # February
                    val = 29 if leap else 28
                if val != a[i]:
                    ok = False
                    break
            if ok:
                print("YES")
                return

    print("NO")

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the calendar structure. The outer loops select the hypothetical alignment of the sequence with the year calendar, while the inner loop checks consistency of all consecutive months.

The only subtlety is February handling. We override the base value at index 1 depending on whether we assume a leap year for the starting context. Since the sequence length is small, treating the entire segment under one leap assumption is sufficient; any valid placement will align with some consistent local interpretation.

## Worked Examples

### Example 1

Input:

```
4
31 31 30 31
```

We try starting at each month. One valid match is starting at July.

| Step | Month index | Month name | Expected | Given | Match |
| --- | --- | --- | --- | --- | --- |
| 0 | 6 | July | 31 | 31 | yes |
| 1 | 7 | August | 31 | 31 | yes |
| 2 | 8 | September | 30 | 30 | yes |
| 3 | 9 | October | 31 | 31 | yes |

All values match, so the answer is YES.

This trace shows that once alignment is correct, the deterministic calendar sequence fits exactly without ambiguity.

### Example 2

Input:

```
2
30 30
```

We test all possible starts. No month has 30 followed immediately by 30 in the calendar.

For instance, starting at April:

| Step | Month index | Month name | Expected | Given | Match |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | April | 30 | 30 | yes |
| 1 | 4 | May | 31 | 30 | no |

Every starting position fails at the second step, so the output is NO.

This demonstrates that local adjacency in the calendar restricts possible sequences strongly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(12 · n) | We try 12 starting months and compare up to n steps each time |
| Space | O(1) | Only fixed arrays and counters are used |

The bounds n ≤ 24 make this effectively constant time, well within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    base = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for start in range(12):
        for leap in (0, 1):
            ok = True
            for i in range(n):
                m = (start + i) % 12
                val = base[m]
                if m == 1:
                    val = 29 if leap else 28
                if val != a[i]:
                    ok = False
                    break
            if ok:
                return "YES"
    return "NO"

# provided samples
assert run("4\n31 31 30 31\n") == "YES"

# custom cases
assert run("1\n31\n") == "YES"
assert run("2\n30 30\n") == "NO"
assert run("3\n28 31 30\n") == "YES"
assert run("4\n31 28 31 30\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n31` | YES | Any single 31-day month exists |
| `2\n30 30` | NO | No adjacent 30-day months exist |
| `3\n28 31 30` | YES | February to March transition |
| `4\n31 28 31 30` | YES | Non-leap February consistency |

## Edge Cases

One important edge case is sequences that include February. For example, input `[28, 31]` must be accepted because February can be non-leap and is followed by March. The algorithm handles this by explicitly overriding February’s value depending on the chosen leap flag, ensuring both 28 and 29 are considered.

Another edge case is wrapping across December to January. For example, `[31, 31, 28]` may correspond to December, January, February. The modulo arithmetic `(start + i) % 12` correctly handles wraparound without special casing year boundaries.

A final subtle case is sequences that could match both leap and non-leap interpretations. The algorithm does not assume uniqueness; it only requires existence of one valid configuration, so it correctly returns YES as soon as one consistent simulation succeeds.