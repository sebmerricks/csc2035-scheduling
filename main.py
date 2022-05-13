from dataclasses import dataclass
import string
import random
from tabulate import tabulate


@dataclass
class Process:
    id: str
    at: int
    rt: int
    tr: int = 0
    tt: int = 0


def generate_processes(n=5, max_at=5, min_rt=2, max_rt=10):
    alphabet = string.ascii_uppercase
    p = [Process(alphabet[i], random.randint(0, max_at), random.randint(min_rt, max_rt)) for i in range(n)]
    if 0 not in [pr.at for pr in p]:
        p[random.randrange(0, n)].at = 0
    #p = [Process("A", 0, 2), Process("B", 0, 4), Process("C", 0, 1), Process("D", 0, 1), Process("E", 0, 1)]
    return p


def first_come_first_served(p):
    p.sort(key=lambda pr: pr.at)
    t = 0
    for pr in p:
        t += pr.rt
        pr.tt = t - pr.at
    print_table(p)
    print_turnaround(p)


def shortest_job_first(p):
    p.sort(key=lambda pr: (pr.at, pr.rt))
    t = 0
    for pr in p:
        t += pr.rt
        pr.tt = t - pr.at
    print_table(p)
    print_turnaround(p)


def shortest_remaining_time_next(p):
    for pr in p:
        pr.tr = pr.rt
    p.sort(key=lambda pr: (pr.at, pr.rt))
    t = 0
    queue = [pr for pr in p if pr.at <= t]
    processed = []
    while len(queue) > 0:
        queue += [pr for pr in p if pr.at <= t and pr not in processed and pr not in queue]
        queue.sort(key=lambda pr: (pr.tr, pr.at))
        curr = queue[0]
        t += 1
        curr.tr -= 1
        if curr.tr == 0:
            curr.tt = t - curr.at
            processed.append(curr)
            queue.remove(curr)
    print_table(processed)
    print_turnaround(p)


def round_robin(p):
    t = 0
    for pr in p:
        pr.tr = pr.rt
    queue = [pr for pr in p if pr.at <= t]
    processed = []
    while len(queue) > 0:
        t += len(queue)
        for pr in queue:
            pr.tr -= 1
            if pr.tr == 0:
                pr.tt = t
                processed.append(pr)
        for pr in processed:
            if pr in queue:
                queue.remove(pr)
        queue += [pr for pr in p if pr.at <= t and pr not in processed and pr not in queue]
    print_table(p)
    print_turnaround(p)


def print_table(p):
    table = [[pr.id, pr.at, pr.rt, pr.tt] for pr in p]
    print(tabulate(table, headers=["Process", "Arrival Time", "Run Time", "Turnaround Time"]))


def print_turnaround(p):
    ttt = sum([pr.tt for pr in p])
    print(f"Total Turnaround Time = {ttt}")
    print(f"Mean Turnaround Time = {ttt / len(p)}")


if __name__ == '__main__':
    processes = generate_processes(5)
    print_table(processes)
    input("Press enter to see the answer...")
    round_robin(processes)
