---
problem: 965A
contest_id: 965
problem_index: A
name: "Paper Airplanes"
contest_name: "Codeforces Round 476 (Div. 2) [Thanks, Telegram!]"
rating: 800
tags: ["math"]
answer: passed_samples
verified: true
solve_time_s: 65
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a3281e5-4e50-83ec-8a25-9981e3e4dcdf
---

# CF 965A - Paper Airplanes

**Rating:** 800  
**Tags:** math  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 5s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a3281e5-4e50-83ec-8a25-9981e3e4dcdf  

---

## Solution

## Problem Understanding

A group of people wants to produce identical paper airplanes, but the only way to make airplanes is indirectly through sheets of paper. Each sheet can be folded into a fixed number of airplanes, and paper is sold only in packs, each pack containing a fixed number of sheets.

The requirement is simple in structure but layered in constraints. Every person must independently be able to build a fixed number of airplanes. Since multiple airplanes come from a single sheet, we first convert the airplane requirement into a sheet requirement per person, then scale it by the number of people, and finally convert sheets into packs because buying fractional packs is not possible.

The key quantity is how many sheets are needed in total. If each sheet produces `s` airplanes, then each person needs `ceil(n / s)` sheets, since partial sheets do not exist. Across `k` people, the total sheet requirement becomes `k * ceil(n / s)`. Once we know the number of sheets, we convert it into packs of size `p` using another ceiling division.

The constraints are small enough that any constant-time arithmetic solution is sufficient. All variables are at most 10^4, so even direct multiplication reaches only 10^8, which is comfortably within integer range for Python and requires no optimization beyond O(1) computation.

The main place where mistakes occur is in handling rounding correctly. If a person needs, for example, 5 airplanes and each sheet produces 2 airplanes, then 2 sheets produce only 4 airplanes, which is insufficient. A naive integer division would incorrectly assign 2 sheets instead of 3. The same issue appears again when converting sheets into packs.

Another subtle mistake is applying ceiling division too late or too early. For instance, rounding after multiplying by `k` instead of per person still works here due to linearity, but rounding at the wrong stage when implementing carelessly often leads to off-by-one errors.

## Approaches

A brute-force way to think about the problem is to simulate purchasing packs one by one, distributing sheets, and checking whether all people can produce enough airplanes. After each additional pack, we would recompute how many airplanes can be produced and verify the requirement. While conceptually straightforward, this approach is inefficient because the number of packs might grow large, and each check requires recomputing total production across all sheets, leading to a repeated O(k) evaluation per candidate number of packs.

The structure of the problem, however, removes any need for simulation. Each pack contributes a fixed number of sheets, each sheet contributes a fixed number of airplanes, and each person has an identical requirement. This turns the problem into a deterministic conversion pipeline: airplanes per person to sheets per person, then to total sheets, then to packs.

The key observation is that all transformations are linear except for rounding up at division boundaries. Once we realize that we only need to satisfy a global minimum number of sheets, the problem reduces to computing a single ceiling division twice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(answer · k) | O(1) | Too slow |
| Direct Math | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many sheets one person needs to make `n` airplanes. Since each sheet makes `s` airplanes, we compute `need_per_person = ceil(n / s)`. This ensures no person is under-supplied even if airplanes do not divide evenly per sheet.
2. Convert this per-person requirement into a total requirement by multiplying by the number of people: `total_sheets = k * need_per_person`. This aggregation works because each person’s requirement is independent and identical.
3. Convert sheets into packs. Each pack contains `p` sheets, so the number of packs is `packs = ceil(total_sheets / p)`. This ensures we never buy partial packs.
4. Print the computed number of packs.

The main subtlety is ensuring that both divisions are ceiling divisions, not floor divisions. A single missed rounding step underestimates requirements and produces invalid solutions.

### Why it works

The algorithm works because every constraint is monotonic and linear: more sheets never reduce the ability to produce airplanes, and each transformation preserves feasibility. The only discontinuities come from indivisibility of sheets per airplane and packs per sheets, and both are handled exactly via ceiling division. Once both rounding points are accounted for, the computed number is the minimal value satisfying all constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

k, n, s, p = map(int, input().split())

need_per_person = (n + s - 1) // s
total_sheets = k * need_per_person
packs = (total_sheets + p - 1) // p

print(packs)
```

The first line computes the ceiling division for airplanes per sheet. The second aggregates across all people. The final line converts sheets into packs using the same ceiling pattern. The expression `(x + d - 1) // d` is a standard integer trick for ceiling division in Python, avoiding floating-point arithmetic and preserving correctness for all integer ranges in the constraints.

## Worked Examples

### Example 1

Input:

```
5 3 2 3
```

Here each sheet makes 2 airplanes, so each person needs `ceil(3 / 2) = 2` sheets.

| Step | Value |
| --- | --- |
| n | 3 |
| s | 2 |
| sheets per person | 2 |
| k | 5 |
| total sheets | 10 |
| p | 3 |
| packs | 4 |

Each pack gives 3 sheets, so 10 sheets require `ceil(10 / 3) = 4` packs. This confirms the necessity of rounding up at both stages.

### Example 2

Input:

```
1 10 3 5
```

Each sheet gives 3 airplanes, so one person needs `ceil(10 / 3) = 4` sheets.

| Step | Value |
| --- | --- |
| k | 1 |
| sheets per person | 4 |
| total sheets | 4 |
| p | 5 |
| packs | 1 |

Even though only 4 sheets are needed, they must buy a whole pack. This shows how the second ceiling dominates when pack size exceeds demand.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The solution comfortably fits within limits since it performs constant-time integer arithmetic regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    k, n, s, p = map(int, input().split())
    need_per_person = (n + s - 1) // s
    total_sheets = k * need_per_person
    packs = (total_sheets + p - 1) // p
    return str(packs)

# provided sample
assert run("5 3 2 3") == "4"

# minimum values
assert run("1 1 1 1") == "1"

# exact division no rounding needed
assert run("2 4 2 2") == "2"

# requires ceiling in first step
assert run("3 5 2 10") == "1"

# requires ceiling in second step
assert run("1 3 2 2") == "2"

# large balanced case
assert run("10000 10000 1 10000") == "10000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 1 | minimal edge case |
| 2 4 2 2 | 2 | no rounding needed |
| 3 5 2 10 | 1 | ceiling in first step |
| 1 3 2 2 | 2 | ceiling in pack conversion |
| 10000 10000 1 10000 | 10000 | maximum scale handling |

## Edge Cases

One edge case is when a single sheet already suffices for a person. For input:

```
k=4, n=1, s=10, p=3
```

Each person needs `ceil(1/10)=1` sheet. Total sheets are 4, and packs are `ceil(4/3)=2`. The algorithm correctly avoids underestimating due to fractional sheets.

Another edge case is when pack size is larger than total sheet requirement. For input:

```
k=1, n=5, s=2, p=100
```

We get `ceil(5/2)=3` sheets, so total is 3 sheets. Even though only 3 sheets are needed, one full pack must be bought. The algorithm produces `ceil(3/100)=1`, correctly handling oversupply caused by pack granularity.