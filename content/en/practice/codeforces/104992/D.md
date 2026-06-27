---
title: "CF 104992D - \u0421\u043a\u043e\u043b\u044c\u043a\u043e \u043e\u0448\u0438\u0431\u043e\u043a?"
description: "The training session consists of a sequence of attempts where the same underlying task may appear multiple times. Each attempt produces two strings: what Grisha wrote first, and the correct answer provided by the owl afterward."
date: "2026-06-28T03:32:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104992
codeforces_index: "D"
codeforces_contest_name: "qual VKOSHP Junior 24"
rating: 0
weight: 104992
solve_time_s: 72
verified: false
draft: false
---

[CF 104992D - \u0421\u043a\u043e\u043b\u044c\u043a\u043e \u043e\u0448\u0438\u0431\u043e\u043a?](https://codeforces.com/problemset/problem/104992/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

The training session consists of a sequence of attempts where the same underlying task may appear multiple times. Each attempt produces two strings: what Grisha wrote first, and the correct answer provided by the owl afterward. A task is considered “solved” only when the owl accepts Grisha’s submission. If it is accepted, that task disappears from further training; if it is rejected, the same task reappears later and Grisha tries again.

The key quantity is not the number of wrong attempts, but the number of distinct tasks for which Grisha made at least one mistake before eventually getting it accepted. A task can appear multiple times, but we only care whether its first attempt was incorrect.

The input gives us a sequence of 2n strings arranged as n pairs in chronological order. Each pair corresponds to one attempt of a task that is currently active. We must determine how many distinct tasks had their first appearance as a mismatch.

The constraints allow up to 40,000 attempts and total string length up to 200,000, which means average string length is small. Any solution must run in essentially linear time over the input size. This immediately rules out anything involving repeated full comparisons across many pairs or any quadratic matching between attempts.

A subtle point is that the same task is not explicitly identified by an ID. The only way to recognize repetition is by comparing the correctness condition. This means we must reconstruct a notion of task identity implicitly from the strings.

The important edge cases come from repeated failures of the same task before success. For example, if the same incorrect answer appears multiple times before the correct version is eventually accepted, we must count it only once.

Another corner case is when a task is correct on its first appearance. Even if it appears again later (which it should not according to the process), we must ensure it is not counted.

## Approaches

A direct simulation would process the pairs sequentially, and for each pair decide whether Grisha’s answer matches the correct one. If we only cared about whether each attempt was correct, we could simply compare strings.

However, the question is more global: we must count how many distinct tasks ever had a failed first attempt. This requires grouping attempts belonging to the same task.

The naive idea would be to treat each pair independently and compare it against all previous correct answers to see if it belongs to a known task. In the worst case, each attempt could require scanning all previous attempts, leading to quadratic behavior.

The key observation is that task identity is fully determined by the correct answer string. Once a correct answer appears, it defines a canonical representation of that task. Every earlier mismatch associated with that same correct answer corresponds to the same task.

So we can maintain a mapping from correct answer string to whether this task has already been solved, and whether it has already been counted as having a first-error. When we see a pair, we compare strings; if they differ, we mark that task as having had an error before its successful resolution.

This reduces the problem to a hash-based bookkeeping task over strings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | O(n² · L) | O(nL) | Too slow |
| Hash Map by Correct String | O(n · L) | O(n · L) | Accepted |

## Algorithm Walkthrough

We process the input in chronological order, reading pairs of strings.

1. Read the correct answer string and use it as the identifier of a task. If this task has never been seen before, initialize its state as “not yet solved” and “no error recorded”.
2. Compare Grisha’s submitted string with the correct one. If they are identical, the task is solved immediately and we mark it as solved.
3. If they differ, we record that this task had a wrong attempt before being solved. We also ensure that we only count this task once, even if it appears again later with more mistakes.
4. If the task later appears again and is eventually solved, we do not increase the answer again.

The essential structure is a dictionary keyed by the correct answer string. Each entry stores two flags: whether the task has been solved, and whether we have already counted an initial mistake for it.

The correctness relies on the fact that every task is uniquely identified by its correct answer text. Even if Grisha produces different wrong strings across attempts, they all map back to the same correct answer key.

### Why it works

Every task is completely determined by its correct answer string. Any incorrect submission paired with that same correct answer must belong to that task. The first time we see a mismatch for a given correct string, it corresponds exactly to “this task had at least one error before being solved”. Subsequent mismatches do not change the answer because the task is already marked. This guarantees that each task is counted at most once and exactly when its first attempt is incorrect.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    first_wrong = set()
    solved = set()
    
    for _ in range(n):
        grisha = input().rstrip("\n")
        correct = input().rstrip("\n")
        
        # If already solved, ignore
        if correct in solved:
            continue
        
        if grisha == correct:
            solved.add(correct)
        else:
            # first time we see a wrong attempt for this task
            first_wrong.add(correct)
    
    print(len(first_wrong))

if __name__ == "__main__":
    solve()
```

The solution relies on treating the correct answer string as the canonical identifier for each task. The `solved` set ensures we never reconsider completed tasks. The `first_wrong` set ensures we only count a task once even if multiple incorrect attempts occur before success.

A subtle implementation detail is stripping only the newline character. The input guarantees raw strings without extra formatting, so no normalization beyond this is required.

## Worked Examples

### Example 1

Input:

```
4
Who possted this photo
Who posted this photo
You are welcome
You are welcome
Who posted this foto
Who posted this photo
Who posted this phota
Who posted this photo
```

We track state per correct string.

| Step | Grisha | Correct | Match | Solved set | First wrong set |
| --- | --- | --- | --- | --- | --- |
| 1 | Who possted this photo | Who posted this photo | No | {} | {photo} |
| 2 | You are welcome | You are welcome | Yes | {welcome} | {photo} |
| 3 | Who posted this foto | Who posted this photo | No | {welcome} | {photo} |
| 4 | Who posted this phota | Who posted this photo | No | {welcome} | {photo} |

Final answer is 1 because only “Who posted this photo” had an initial mismatch before being solved.

This trace shows that multiple failures for the same task do not increase the count.

### Example 2

Input:

```
3
abc
abc
def
def
ghi
ghi
```

All answers are correct immediately. No entry ever enters `first_wrong`, so the output is 0. This confirms that tasks solved on first attempt are never counted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L) | Each pair is processed once and compared using string equality |
| Space | O(k · L) | Stores distinct correct strings in hash sets |

The total input size is bounded by 200,000 characters, so linear scanning and hashing fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else _run_capture(inp)

def _run_capture(inp: str) -> str:
    import sys, io
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.strip()

# sample
assert _run_capture("""4
Who possted this photo
Who posted this photo
You are welcome
You are welcome
Who posted this foto
Who posted this photo
Who posted this phota
Who posted this photo
""") == "1"

# all correct
assert _run_capture("""2
a
a
b
b
""") == "0"

# all wrong then correct
assert _run_capture("""2
a
b
b
b
""") == "1"

# repeated wrong before correct
assert _run_capture("""3
x
y
x
y
x
y
""") == "1"

# minimal
assert _run_capture("""1
a
b
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all correct | 0 | no false positives |
| wrong then correct | 1 | counting only once per task |
| repeated wrong | 1 | deduplication of errors |
| minimal mismatch | 1 | smallest edge case |

## Edge Cases

A key edge case is repeated failures for the same task before success. For example:

```
1
a
b
a
b
```

Here the task “b” appears twice incorrectly before being accepted. The algorithm inserts “b” into `first_wrong` on the first mismatch and ignores subsequent ones, because sets naturally deduplicate entries. When the correct version is finally accepted, the task is already counted exactly once.

Another edge case is tasks that are always correct:

```
1
hello
hello
```

The comparison succeeds immediately, so we only insert “hello” into `solved` and never touch `first_wrong`, yielding output 0.

Finally, tasks that appear correct early but fail later are impossible under the process rules described, but even if simulated, the solution remains stable because once a task is marked solved, it is never reconsidered.
