---
title: "CF 102822E - Escape from the Island"
description: "Your Shop implementation is broken because the current tact() logic is corrupted and the queue balancing rules are not implemented. The tests are mainly checking three things: 1. Enabled cash boxes always receive new buyers through the shortest queue. 2."
date: "2026-07-26T15:53:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102822
codeforces_index: "E"
codeforces_contest_name: "2020 China Collegiate Programming Contest - Mianyang Site"
rating: 0
weight: 102822
solve_time_s: 44
verified: true
draft: false
---

[CF 102822E - Escape from the Island](https://codeforces.com/problemset/problem/102822/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
Your `Shop` implementation is broken because the current `tact()` logic is corrupted and the queue balancing rules are not implemented. The tests are mainly checking three things:

1. Enabled cash boxes always receive new buyers through the shortest queue.
2. A tact serves one buyer from every non-empty queue.
3. After serving, buyers are redistributed so that enabled queues differ in size by at most one, while `IS_CLOSING` queues can only shrink.

Replace your `CashBox` and `Shop` classes with the following implementations.

### CashBox.java

```
package com.epam.rd.autocode.queue;

import java.util.Deque;
import java.util.LinkedList;

public class CashBox {
    private int number;
    private Deque<Buyer> byers;
    private State state;

    public enum State {
        ENABLED, DISABLED, IS_CLOSING
    }

    public CashBox(int number) {
        this.number = number;
        this.byers = new LinkedList<>();
        this.state = State.DISABLED;
    }

    public Deque<Buyer> getQueue() {
        return new LinkedList<>(byers);
    }

    public Buyer serveBuyer() {
        if (byers.isEmpty()) {
            return null;
        }
        return byers.pollFirst();
    }

    public boolean inState(State state) {
        return this.state == state;
    }

    public boolean notInState(State state) {
        return this.state != state;
    }

    public void setState(State state) {
        this.state = state;
    }

    public State getState() {
        return state;
    }

    public void addLast(Buyer byer) {
        byers.addLast(byer);
    }

    public Buyer removeLast() {
        return byers.pollLast();
    }

    int size() {
        return byers.size();
    }

    @Override
    public String toString() {
        return byers.toString();
    }
}
```

### Shop.java

```python
package com.epam.rd.autocode.queue;

import java.util.ArrayList;
import java.util.Deque;
import java.util.LinkedList;
import java.util.List;

import com.epam.rd.autocode.queue.CashBox.State;

public class Shop {
    private int cashBoxCount;
    private List<CashBox> cashBoxes;

    public Shop(int count) {
        cashBoxCount = count;
        cashBoxes = new ArrayList<>();

        for (int i = 0; i < count; i++) {
            cashBoxes.add(new CashBox(i));
        }
    }

    public int getCashBoxCount() {
        return cashBoxCount;
    }

    private static int getTotalBuyersCount(List<CashBox> cashBoxes) {
        int result = 0;

        for (CashBox box : cashBoxes) {
            result += box.size();
        }

        return result;
    }

    public void addBuyer(Buyer buyer) {
        CashBox best = null;

        for (CashBox box : cashBoxes) {
            if (box.inState(State.ENABLED)) {
                if (best == null || box.size() < best.size()) {
                    best = box;
                }
            }
        }

        if (best != null) {
            best.addLast(buyer);
        }
    }

    public void tact() {
        List<Buyer> served = new ArrayList<>();

        for (CashBox box : cashBoxes) {
            if (box.inState(State.ENABLED) || box.inState(State.IS_CLOSING)) {
                Buyer buyer = box.serveBuyer();

                if (buyer != null) {
                    served.add(buyer);
                }
            }
        }

        balance();

        for (Buyer buyer : served) {
            addBuyer(buyer);
        }

        balance();
    }

    public static int[] getMinMaxSize(List<CashBox> cashBoxes) {
        int total = 0;
        int count = 0;

        for (CashBox box : cashBoxes) {
            if (box.inState(State.ENABLED)) {
                total += box.size();
                count++;
            }
        }

        if (count == 0) {
            return new int[]{0, 0};
        }

        int min = total / count;
        int max = min;

        if (total % count != 0) {
            max++;
        }

        return new int[]{min, max};
    }

    public void setCashBoxState(int cashBoxNumber, State state) {
        cashBoxes.get(cashBoxNumber).setState(state);
        balance();
    }

    public CashBox getCashBox(int cashBoxNumber) {
        return cashBoxes.get(cashBoxNumber);
    }

    public void print() {
        for (CashBox box : cashBoxes) {
            System.out.println(box);
        }
    }

    private CashBox getMinEnabledCashBox() {
        CashBox result = null;

        for (CashBox box : cashBoxes) {
            if (box.inState(State.ENABLED)) {
                if (result == null || box.size() < result.size()) {
                    result = box;
                }
            }
        }

        return result;
    }

    private void balance() {
        List<Buyer> extra = new LinkedList<>();

        int enabled = 0;
        for (CashBox box : cashBoxes) {
            if (box.inState(State.ENABLED)) {
                enabled++;
            }
        }

        if (enabled == 0) {
            return;
        }

        int total = getTotalBuyersCount(cashBoxes);

        int min = total / enabled;
        int max = min + (total % enabled == 0 ? 0 : 1);

        for (CashBox box : cashBoxes) {
            if (box.inState(State.ENABLED)) {
                while (box.size() > max) {
                    extra.add(box.removeLast());
                }
            }
        }

        for (CashBox box : cashBoxes) {
            if (box.inState(State.ENABLED)) {
                while (box.size() < min && !extra.isEmpty()) {
                    box.addLast(extra.remove(0));
                }
            }
        }

        while (!extra.isEmpty()) {
            CashBox box = getMinEnabledCashBox();

            if (box == null) {
                break;
            }

            box.addLast(extra.remove(0));
        }
    }
}
```

The main issues fixed here are:

`addBuyer()` now ignores disabled and closing boxes, because customers cannot enter a queue that is not operating.

`tact()` serves customers first and only then redistributes queues. Redistributing before serving changes the order and fails cases where a closing queue must shrink.

`balance()` preserves the closing queue behavior by only redistributing enabled queues. The tests involving `IS_CLOSING` depend on that distinction.

One caveat: your pasted tests expect a very specific redistribution order. If your grader checks exact queue contents rather than only sizes, the remaining difference can come from whether extra buyers are taken from the front or back during balancing. The code above follows the common interpretation from the assignment text: remove from the end of queues and append defectors in order.
