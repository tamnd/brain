---
problem: 987A
contest_id: 987
problem_index: A
name: "Infinity Gauntlet"
contest_name: "Codeforces Round 485 (Div. 2)"
rating: 800
tags: ["implementation"]
answer: passed_samples
verified: false
solve_time_s: 76
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a33a990-3914-83ec-a201-26b6a39a5516
---

# CF 987A - Infinity Gauntlet

**Rating:** 800  
**Tags:** implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 16s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a33a990-3914-83ec-a201-26b6a39a5516  

---

## Solution

## Problem Understanding

We are given a small set of colored stones placed into a fixed structure: an Infinity Gauntlet that always has exactly six possible slots. Each slot corresponds to one unique Infinity Gem, and each gem is uniquely identified by its color.

The input tells us how many gems Thanos currently has, and then lists the colors of those gems. From this partial information, we must determine which gems are missing by comparing against the full fixed set of six possible colors. The output is the count of missing gems followed by their names.

The important structural detail is that the universe of possibilities is constant and tiny. There are always exactly six colors, and all input colors are distinct. This immediately removes any need for complex searching or optimization. The task reduces to set subtraction between two fixed sets.

The constraint on n is at most 6, meaning even the most naive approach of checking membership repeatedly is trivially fast. Any solution that loops over a constant list or uses a set will run in constant time.

The only edge cases come from boundary values of n. When n is 0, we must output all six gems. When n is 6, we output none. A subtle failure case in careless implementations is forgetting to maintain the correct mapping between color names and gem names, or mismatching capitalization, since output format requires capitalized gem names while input colors are lowercase strings.

## Approaches

A brute-force approach would treat this as a general membership problem. We could store the input colors in a list and, for each of the six possible colors, scan the list to check whether it exists. Each membership check costs O(n), and we perform a constant six checks, leading to O(6n), which is still constant in this problem.

However, even this is unnecessary overhead. The structure of the problem suggests a direct mapping between colors and gem names. Since the universe is fixed, we can simply store all six pairs in a dictionary or list, then remove those that appear in the input.

The key observation is that we are not solving a dynamic query problem. We are not asked to handle updates or multiple test cases with large variation. We are simply filtering a fixed catalog. This makes a direct set difference the cleanest approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(1) | O(1) | Accepted |
| Direct Set Mapping | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We solve the problem by maintaining a fixed mapping between colors and gem names, then removing those that appear in the input.

1. Build a reference table of all six gems, pairing each color with its corresponding gem name. This represents the full complete set before any observation.
2. Read all input colors and store them in a set. Using a set is not strictly necessary, but it ensures fast membership checks and avoids accidental duplicates if input assumptions are violated.
3. Iterate through the full list of six possible colors.
4. For each color, check whether it appears in the input set.
5. If it does not appear, append the corresponding gem name to the answer list.
6. After processing all six, output the number of missing gems followed by their names.

The reason we iterate over the full fixed list instead of iterating over the input is that we are asked to find missing elements, not present ones. This direction of iteration guarantees we never forget to consider absent gems.

### Why it works

The algorithm relies on the invariant that every valid gem is uniquely associated with exactly one color, and the universe of possible colors is fixed and complete. At every step, we classify each possible gem into exactly one of two states: observed or not observed. Since the input contains no duplicates and only valid colors, no ambiguity arises. Therefore, every missing gem must be precisely one whose color does not appear in the input set, guaranteeing correctness of the subtraction logic.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    color_to_name = {
        "purple": "Power",
        "green": "Time",
        "blue": "Space",
        "orange": "Soul",
        "red": "Reality",
        "yellow": "Mind"
    }
    
    present = set()
    for _ in range(n):
        present.add(input().strip())
    
    missing = []
    for color, name in color_to_name.items():
        if color not in present:
            missing.append(name)
    
    print(len(missing))
    for x in missing:
        print(x)

if __name__ == "__main__":
    solve()
```

The solution centers around the dictionary `color_to_name`, which encodes the fixed bijection between input colors and output gem names. This avoids any conditional logic or manual mapping inside loops.

We store input colors in a set to ensure constant-time membership checks. Even though n is at most 6, this makes the logic clean and robust.

The iteration over the dictionary ensures we always check all possible gems exactly once, regardless of input size.

## Worked Examples

### Example 1

Input:

```
4
red
purple
yellow
orange
```

We track the process:

| Step | Color Checked | In Input Set | Action | Missing List |
| --- | --- | --- | --- | --- |
| 1 | purple | yes | skip | [] |
| 2 | green | no | add Time | ["Time"] |
| 3 | blue | no | add Space | ["Time", "Space"] |
| 4 | orange | yes | skip | ["Time", "Space"] |
| 5 | red | yes | skip | ["Time", "Space"] |
| 6 | yellow | yes | skip | ["Time", "Space"] |

Output:

```
2
Time
Space
```

This trace shows that the algorithm is insensitive to input order and correctly accumulates only absent elements.

### Example 2

Input:

```
0
```

| Step | Color Checked | In Input Set | Action | Missing List |
| --- | --- | --- | --- | --- |
| 1 | purple | no | add Power | ["Power"] |
| 2 | green | no | add Time | ["Power", "Time"] |
| 3 | blue | no | add Space | ["Power", "Time", "Space"] |
| 4 | orange | no | add Soul | ["Power", "Time", "Space", "Soul"] |
| 5 | red | no | add Reality | ["Power", "Time", "Space", "Soul", "Reality"] |
| 6 | yellow | no | add Mind | ["Power", "Time", "Space", "Soul", "Reality", "Mind"] |

Output:

```
6
Power
Time
Space
Soul
Reality
Mind
```

This case confirms that the algorithm correctly handles the empty input set and returns the full universe.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | We always process exactly six fixed items regardless of input size |
| Space | O(1) | Only a constant-size dictionary and set are used |

The computation is bounded by a constant universe of six elements, so it trivially satisfies all constraints. Memory usage is also fixed and independent of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    color_to_name = {
        "purple": "Power",
        "green": "Time",
        "blue": "Space",
        "orange": "Soul",
        "red": "Reality",
        "yellow": "Mind"
    }

    n = int(input().strip())
    present = set(input().strip() for _ in range(n))

    missing = [name for color, name in color_to_name.items() if color not in present]

    out = [str(len(missing))] + missing
    return "\n".join(out)

# provided sample
assert run("4\nred\npurple\nyellow\norange\n") == "2\nTime\nSpace"

# all missing
assert run("0\n") == "6\nPower\nTime\nSpace\nSoul\nReality\nMind"

# all present
assert run("6\npurple\ngreen\nblue\norange\nred\nyellow\n") == "0"

# single element
assert run("1\nblue\n") == "5\nPower\nTime\nSoul\nReality\nMind"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 gems | all six gems | full absence case |
| 6 gems | 0 | full presence case |
| 1 blue | 5 missing | partial filtering correctness |
| sample case | 2 Time Space | mixed membership correctness |

## Edge Cases

For the empty input case `n = 0`, the algorithm initializes the input set as empty. Every iteration over the fixed six-color list fails the membership check, so all six gem names are appended. The output correctly becomes the full set of gems.

For the full input case `n = 6`, the set contains all colors. Each lookup succeeds, so no gem is added to the missing list. The algorithm outputs zero and an empty list, matching the required format.

In both cases, correctness comes from the fact that the iteration space is fixed and independent of input size, so boundary values only affect membership checks, not control flow structure.