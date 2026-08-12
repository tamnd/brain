---
title: "CF 102330E - \u0413\u0435\u043e\u0440\u0433\u0438\u0439 \u0438 \u0432\u043e\u0435\u043d\u043a\u043e\u043c\u0430\u0442"
description: "Есть n человек и k последовательных печатей. Печати расположены в фиксированном порядке: сначала человек должен получить первую, затем вторую и так далее до k-й. Для печати j известна длительность обслуживания t[j]. Человек i приходит в момент a[i]."
date: "2026-08-13T04:02:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102330
codeforces_index: "E"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2019.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102330
solve_time_s: 282
verified: true
draft: false
---

[CF 102330E - \u0413\u0435\u043e\u0440\u0433\u0438\u0439 \u0438 \u0432\u043e\u0435\u043d\u043a\u043e\u043c\u0430\u0442](https://codeforces.com/problemset/problem/102330/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

Есть `n` человек и `k` последовательных печатей. Печати расположены в фиксированном порядке: сначала человек должен получить первую, затем вторую и так далее до `k`-й. Для печати `j` известна длительность обслуживания `t[j]`.

Человек `i` приходит в момент `a[i]`. Сразу после прихода он попадает в очередь первой печати. Если несколько человек пришли одновременно, их порядок определяется исходными номерами. После успешного получения очередной печати человек мгновенно переходит в очередь следующей. Каждая очередь обслуживается в порядке поступления, а сотрудник начинает следующего человека сразу после освобождения.

У каждого человека есть ограничение `b[i]`. При `b[i] = 0` он может ждать неограниченно долго. Иначе момент его ухода равен `a[i] + b[i]`. Если человек не успел закончить нужную процедуру к этому моменту, он покидает военкомат. Если последняя печать завершается ровно в момент ухода, человек считается успевшим, как показывает первый пример.

Нужно для каждого человека вывести `completion - a[i]`, если он получил все `k` печатей. Если он ушел раньше завершения процедуры, нужно вывести `-1`.

Ключевая особенность ограничений состоит в условии `n * k <= 10^5`. Это означает, что нам разрешено обработать каждого человека на каждой печати в среднем константное число раз. Полиномиальные решения вроде `O(n^2 k)` уже слишком велики: при `n = 10^5` и `k = 1` они дают порядка `10^10` операций. Нам нужна обработка порядка `n * k`, плюс сортировка людей перед первой очередью.

В задаче есть несколько границ, на которых легко получить неправильный ответ. Первая возникает при точном совпадении завершения последней печати с дедлайном. Для

```
1 1
1
1 1
```

ответ равен `1`, а не `-1`. Человек заканчивает последнюю печать в момент `2`, ровно через `b = 1` после прихода, и уже успел завершить процедуру.

Вторая граница возникает, если человек точно в момент дедлайна заканчивает не последнюю, а промежуточную печать. Например,

```
1 2
3 1
1 3
```

Первая печать заканчивается в момент `4`, который совпадает с дедлайном человека. Он получает эту печать, но процедура еще не закончена, поэтому сразу после этого покидает военкомат и второй печати уже не получает. Ответ равен `-1`.

Третья ситуация связана с человеком, который уже ждал до дедлайна, пока сотрудник был занят другим человеком. Например,

```
2 1
5
1 5
1 5
```

Первый человек получает печать в момент `6`. Второй все это время ждет и в момент `6` уже должен уйти. Его нельзя начинать обслуживать в тот же момент. Ответ равен `5 -1`.

Наконец, `b[i] = 0` нельзя трактовать как дедлайн `a[i]`. В этом случае человек вообще не ограничен временем ожидания. Например,

```
1 1
7
10 0
```

Ответ равен `7`.

## Approaches

Самый прямой вариант симуляции можно построить буквально по происходящим событиям. Для каждой печати нужно хранить очередь людей, добавлять в нее людей, которые пришли, брать первого человека и выяснять, успеет ли он закончить обслуживание. Такой подход уже близок к правильному решению, но неудачная реализация может для каждого обслуживаемого человека заново искать его позицию в очереди среди всех людей. Тогда для одной печати получится `O(n^2)`, а для всех печатей `O(n^2 k)`. В худшем случае при `n = 100000` и `k = 1` это около `10^10` проверок, что за секунду невозможно.

Причина, по которой не нужно искать следующего человека заново, состоит в строгом FIFO-порядке каждой очереди. Если мы обрабатываем одну печать отдельно, все ее входящие люди уже известны в порядке, в котором они появляются в этой очереди. Для первой печати это порядок `(a[i], i)`. Для следующей печати люди появляются именно в порядке завершения предыдущей печати, а этот порядок уже известен из нашей симуляции.

Значит, каждую печать можно обработать одним проходом. Мы поддерживаем текущий момент, когда сотрудник освобождается, и очередь уже пришедших людей. Если очередь пуста, время переносится к следующему приходу. Если человек находится в начале очереди, мы сравниваем время окончания его обслуживания с его дедлайном. Если он успевает закончить последнюю печать, он покидает военкомат с успешным результатом. Если он не успевает, сотрудник остается занят до момента его ухода, потому что человек может уйти прямо во время постановки печати. После этого очередь продолжает работу.

После обработки печати мы передаем на следующую печать только тех людей, которые действительно смогли продолжить процедуру. Их время прихода в новую очередь равно времени завершения текущей печати.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2 k)` | `O(n)` | Too slow |
| Optimal | `O(n log n + nk)` | `O(n)` | Accepted |

Здесь `nk <= 10^5`, поэтому линейная обработка всех пар человек-печать укладывается в ограничение. Сортировка нужна только один раз, чтобы построить первоначальную очередь.

## Algorithm Walkthrough

1. Сохраняем для каждого человека время прихода `a[i]` и абсолютный момент ухода `a[i] + b[i]`. Для `b[i] = 0` используем достаточно большое значение вместо настоящего дедлайна. Начальная очередь первой печати сортируется по `(a[i], i)`, потому что именно такой порядок задается условием.
2. Обрабатываем печати последовательно, от первой до `k`-й. В начале очереди текущей печати находятся только люди, которые уже успешно прошли предыдущую печать. Для первой печати это все люди.
3. Для текущей печати поддерживаем `cur`, момент, когда сотрудник становится свободен, указатель на еще не добавленных людей и очередь уже прибывших людей. Пока очередь пуста, `cur` переносится к времени следующего прихода. Затем в очередь добавляются все люди с временем прихода не больше `cur`.
4. Берем первого человека из очереди. Если `cur` уже не меньше его дедлайна, человек должен был уйти раньше или прямо сейчас, поэтому обслуживания не происходит. Следующий человек может быть обслужен в тот же `cur`, если он подходит по сроку.
5. Если человек еще находится в военкомате, вычисляем `finish = cur + t[j]`. Если `finish` не превосходит дедлайн, печать успешно поставлена. Если это последняя печать, сохраняем `finish` как окончательное время выхода.
6. Если `finish` превосходит дедлайн, человек не исчезает из модели мгновенно в момент начала обслуживания. Он остается у сотрудника до своего дедлайна и затем уходит, поэтому `cur` нужно установить в дедлайн. Это влияет на всех следующих людей в очереди.
7. Если промежуточная печать заканчивается ровно в дедлайн, человек успел получить эту печать, но процедура еще не завершена. Он сразу уходит и не попадает в очередь следующей печати. Именно поэтому для промежуточных печатей продолжить можно только при `finish < deadline`. Для последней печати допустимо `finish <= deadline`.
8. Все люди, успешно прошедшие текущую печать и имеющие право продолжить процедуру, добавляются в список следующей очереди с временем прихода `finish`. Поскольку длительность каждой печати положительна, времена успешных завершений идут строго по возрастанию, поэтому дополнительная сортировка не требуется.
9. После последней печати для каждого успешно завершившего человека вычисляем `finish - a[i]`. Для всех остальных оставляем `-1`.

### Why it works

Инвариант обработки одной печати заключается в том, что перед каждым выбором из очереди она содержит ровно тех людей, которые уже пришли к текущему моменту и еще не были обработаны, причем в точном FIFO-порядке. Человек, стоящий впереди, обязан либо получить обслуживание, либо уйти, и никто позади него не может быть обслужен раньше него. Если он успевает, мы записываем реальное время завершения. Если не успевает, сотрудник занят до его дедлайна, после чего человек уходит, и `cur` получает точное время, в которое сервер действительно становится доступен. Поэтому после обработки всей очереди получаются ровно те люди и те моменты времени, которые происходят в реальной системе.

После каждой печати список передаваемых людей содержит ровно тех людей, которые получили эту печать и не покинули военкомат из-за ограничения времени. Их время появления в следующей очереди равно времени фактического получения печати. Значит, инвариант переносится на следующую печать. По индукции после `k`-й печати алгоритм точно знает всех людей, завершивших всю процедуру.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def process_station(arrivals, duration, deadlines, last):
    """
    arrivals: list of (arrival_time, person_id), already sorted
    duration: time needed for this stamp
    deadlines: absolute departure times, INF means unlimited
    last: whether this is the final stamp

    Returns:
        list of (completion_time, person_id) for people who may
        continue to the next stamp, or for all successful people
        if this is the last stamp.
    """
    queue = []
    head = 0
    ptr = 0
    cur = 0

    result = []

    while ptr < len(arrivals) or head < len(queue):
        if head == len(queue):
            if ptr >= len(arrivals):
                break
            if cur < arrivals[ptr][0]:
                cur = arrivals[ptr][0]

        while ptr < len(arrivals) and arrivals[ptr][0] <= cur:
            queue.append(arrivals[ptr])
            ptr += 1

        person_arrival, person = queue[head]
        head += 1

        deadline = deadlines[person]

        if cur >= deadline:
            continue

        finish = cur + duration

        if finish > deadline:
            cur = deadline
            continue

        cur = finish

        if last:
            result.append((finish, person))
        else:
            if finish < deadline:
                result.append((finish, person))

    return result

def solve():
    n, k = map(int, input().split())
    t = list(map(int, input().split()))

    a = [0] * n
    deadlines = [INF] * n

    for i in range(n):
        ai, bi = map(int, input().split())
        a[i] = ai
        if bi != 0:
            deadlines[i] = ai + bi

    arrivals = [(a[i], i) for i in range(n)]
    arrivals.sort()

    for station in range(k):
        arrivals = process_station(
            arrivals,
            t[station],
            deadlines,
            station == k - 1
        )

        if not arrivals:
            break

    answer = [-1] * n

    if k == 0:
        return

    for finish, person in arrivals:
        answer[person] = finish - a[person]

    print(*answer)

if __name__ == "__main__":
    solve()
```

В начале `deadlines[i]` хранит абсолютный момент ухода, а не длительность ожидания. Это существенно упрощает проверки, потому что в любой точке симуляции достаточно сравнить `cur` или `finish` с одним числом.

Функция `process_station` получает список прибытий уже в правильном порядке. `ptr` указывает на еще не добавленного человека, а `head` на первого необработанного человека в массиве очереди. Физически удалять элементы из начала списка не нужно, поэтому каждый человек добавляется один раз и извлекается один раз.

Когда очередь пуста, `cur` переносится к следующему приходу. После этого добавляются все люди с `arrival <= cur`. Такое условие особенно полезно, когда сотрудник освобождается в тот же момент, когда несколько людей уже находятся в военкомате.

Проверка `cur >= deadline` означает, что человек уже должен уйти до начала обслуживания. Если же `cur < deadline`, сотрудник начинает работать немедленно. При `finish > deadline` человек не успевает закончить печать и занимает сотрудника только до момента ухода, поэтому `cur = deadline`. Именно эта строка позволяет корректно обработать людей, которые бросают процедуру прямо во время постановки печати.

Проверка `finish < deadline` для промежуточных печатей нужна из-за того, что после получения этой печати процедура еще не закончена. Если `finish == deadline`, человек получает текущую печать, но в тот же момент покидает военкомат и не попадает в следующую очередь. Для последней печати равенство разрешено, поскольку вся процедура уже завершена.

В Python целые числа имеют произвольную точность, поэтому суммы вроде `a[i] + b[i]` и последовательные времена окончания не переполняются. Значение `10**30` намного больше любого возможного времени в тесте и безопасно используется как обозначение отсутствия дедлайна.

## Worked Examples

### Sample 1

Вход:

```
1 1
1
1 1
```

Здесь есть одна печать, поэтому это сразу последняя стадия.

| arrival | person | cur before | deadline | finish | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 2 | completed |

Человек начинает обслуживание в момент `1`, печать занимает одну единицу времени и заканчивается в `2`. Его дедлайн также равен `2`, а последняя печать разрешает завершение ровно в дедлайн. Время пребывания равно `2 - 1 = 1`.

Ответ:

```
1
```

Этот пример проверяет главную границу `finish == deadline` на последней печати.

### Sample 2

Вход:

```
6 1
17
10 100
3 30
80 59
24 86
59 76
69 15
```

Все люди проходят только одну, последнюю, печать. Начальная очередь сортируется по времени прихода, поэтому порядок такой: человек 2, человек 1, человек 4, человек 5, человек 6, человек 3.

| person | arrival | deadline | cur before | finish / departure | result |
| --- | --- | --- | --- | --- | --- |
| 2 | 3 | 33 | 3 | 20 | success |
| 1 | 10 | 110 | 20 | 37 | success |
| 4 | 24 | 110 | 37 | 54 | success |
| 5 | 59 | 135 | 59 | 76 | success |
| 6 | 69 | 84 | 76 | 84 | leaves |
| 3 | 80 | 139 | 84 | 101 | success |

Для шестого человека печать длится до `93`, но его дедлайн равен `84`. Он поэтому занимает сотрудника с `76` до `84`, после чего уходит. Человек 3 уже стоял в очереди с момента `80`, поэтому начинает ровно в `84` и заканчивает в `101`.

Итоговые времена пребывания равны `27, 17, 21, 30, 17, -1`, что показывает, почему недостаточно просто выкинуть человека, не успевающего закончить печать. Его время до ухода продолжает занимать сотрудника и сдвигает всех следующих людей.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n + nk)` | Первая очередь сортируется, затем каждый человек обрабатывается не более одного раза на каждой печати |
| Space | `O(n)` | Храним данные людей и текущую очередь, размер которой не превышает `n` |

Условие `n * k <= 10^5` ограничивает суммарное число обработок человек-печать величиной `10^5`. Сортировка занимает не более `O(n log n)`, а все последующие проходы линейны. Используемая память линейна по числу людей и значительно меньше лимита в 256 МБ.

## Test Cases

```python
import io
import sys

INF = 10**30

def solve_instance(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    k = int(next(it))

    t = [int(next(it)) for _ in range(k)]

    a = [0] * n
    deadlines = [INF] * n

    for i in range(n):
        ai = int(next(it))
        bi = int(next(it))
        a[i] = ai
        if bi != 0:
            deadlines[i] = ai + bi

    arrivals = [(a[i], i) for i in range(n)]
    arrivals.sort()

    for station in range(k):
        duration = t[station]
        last = station == k - 1

        queue = []
        head = 0
        ptr = 0
        cur = 0
        nxt = []

        while ptr < len(arrivals) or head < len(queue):
            if head == len(queue):
                if ptr >= len(arrivals):
                    break
                cur = max(cur, arrivals[ptr][0])

            while ptr < len(arrivals) and arrivals[ptr][0] <= cur:
                queue.append(arrivals[ptr])
                ptr += 1

            _, person = queue[head]
            head += 1

            deadline = deadlines[person]

            if cur >= deadline:
                continue

            finish = cur + duration

            if finish > deadline:
                cur = deadline
                continue

            cur = finish

            if last:
                nxt.append((finish, person))
            elif finish < deadline:
                nxt.append((finish, person))

        arrivals = nxt

        if not arrivals:
            break

    answer = [-1] * n

    for finish, person in arrivals:
        answer[person] = finish - a[person]

    return " ".join(map(str, answer))

# Provided sample 1
assert solve_instance("""\
1 1
1
1 1
""") == "1", "sample 1"

# Provided sample 2
assert solve_instance("""\
6 1
17
10 100
3 30
80 59
24 86
59 76
69 15
""") == "27 17 21 30 17 -1", "sample 2"

# Minimum size and unlimited waiting
assert solve_instance("""\
1 1
7
10 0
""") == "7", "minimum size and b=0"

# All equal arrival times, with one person missing the deadline
assert solve_instance("""\
2 1
5
1 5
1 5
""") == "5 -1", "equal arrivals and exact waiting boundary"

# Exact deadline on an intermediate stamp
assert solve_instance("""\
1 2
3 1
1 3
""") == "-1", "intermediate stamp ends exactly at deadline"

# All values equal, multiple stamps
assert solve_instance("""\
3 2
2 3
1 100
1 100
1 100
""") == "9 12 15", "equal arrivals and equal deadlines"

# Maximum n*k = 100000, n=100000, k=1.
# Every person can wait forever and all arrive together.
n = 100000
parts = [f"{n} 1", "1"]
parts.extend(["1 0"] * n)
max_input = "\n".join(parts) + "\n"

max_output = solve_instance(max_input).split()
assert len(max_output) == n
assert max_output[0] == "1"
assert max_output[-1] == str(n)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7 / 10 0` | `7` | Minimum instance and unlimited waiting |
| `2 1 / 5 / 1 5 / 1 5` | `5 -1` | Equal arrivals and a person whose deadline is exactly the moment the previous service ends |
| `1 2 / 3 1 / 1 3` | `-1` | Completion of an intermediate stamp exactly at the deadline must not be propagated |
| `3 2 / 2 3 / 1 100 / 1 100 / 1 100` | `9 12 15` | Equal arrivals, repeated FIFO processing, and several stamps |
| `100000 1 / 1 / 100000 identical arrivals` | First answer `1`, last answer `100000` | Maximum allowed value of `n * k` and linear performance |

## Edge Cases

### Unlimited waiting

For

```
1 1
7
10 0
```

the deadline is represented by `INF`. The person starts at `10`, finishes at `17`, and is accepted. The algorithm never applies a finite-deadline comparison to this person, so the result is `7`.

### Last stamp finishes exactly at the deadline

For

```
1 1
1
1 1
```

the absolute deadline is `2`. The calculated finish time is also `2`. Since this is the last stamp, the condition `finish <= deadline` succeeds, and the answer is `2 - 1 = 1`.

### Intermediate stamp finishes exactly at the deadline

For

```
1 2
3 1
1 3
```

the first stamp starts at `1` and finishes at `4`, exactly at the person's deadline. The first stamp itself is completed, but the person cannot continue because the procedure is not finished. The algorithm deliberately requires `finish < deadline` before adding a person to the next queue, so the person disappears after the first stamp and the final answer remains `-1`.

### A person leaves while being served

For

```
6 1
17
10 100
3 30
80 59
24 86
59 76
69 15
```

person 6 starts at `76`, while the deadline is `84`. The required service would end at `93`, so the service is interrupted by departure at `84`. The algorithm sets `cur = 84` rather than `cur = 93`. Person 3, who arrived at `80`, can then start at `84` and finishes at `101`. This is exactly why person 3 spends `21` time units in the office instead of `30`.

### Equal arrivals

For

```
2 1
5
1 5
1 5
```

both people enter the first queue at time `1`, and person 1 has priority because of the smaller index. Person 1 finishes at `6`, exactly at their deadline, so they succeed because this is the last stamp. Person 2 has been waiting until `6`, which is also their deadline, so they leave without being served. The output is `5 -1`.

The queue representation preserves this ordering automatically because the initial list is sorted by `(arrival_time, person_id)`, while every later queue inherits the order of successful completions from the previous stamp.
