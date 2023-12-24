"""
All flows are right to left

===>

    1           2          3
   ===         ===        ===
       \     /      \    /
       4\   /5      6\  /7 
         \ /          \/
  8:O          9:O        10:O  
      \      /     \      / 
     11\    /12   13\    /14
        \  /         \  /
   ===         ===        ===  
    15          16         17

"""


class Path:
    def __init__(self, path, tags, excludes):
        self.path = path
        self.tags = tags
        self.excludes = set(excludes)


shaft_paths = {
    1: [
        Path(path=[15, 16, 14, 10], tags=[14], excludes=[8, 11, 12, 13]),
        Path(path=[1, 2, 6, 10], tags=[6, 4, 5], excludes=[7]),
    ],
    2: [
        Path(path=[15, 12, 9, 13, 17], tags=[12, 13], excludes=[8, 11, 14]),
        Path(path=[15, 12, 9, 7, 3], tags=[12, 7], excludes=[8, 11, 6]),
        Path(path=[1, 4, 9, 13, 17], tags=[4, 13], excludes=[5, 14]),
        Path(path=[1, 4, 9, 7, 3], tags=[4, 7], excludes=[5, 6]),
    ],
    3: [
        Path(path=[8, 11, 16, 17], tags=[8, 11], excludes=[12, 13, 14]),
        Path(path=[8, 5, 2, 3], tags=[8, 5], excludes=[6]),
    ],
    4: [
        Path(path=[15, 16, 17], tags=[], excludes=[8, 11, 12, 13, 14]),
        Path(path=[1, 2, 3], tags=[4, 5, 6, 7], excludes=[]),
    ],
}


def find_threading_for_shaft(last_head, tagged, t):
    paths = shaft_paths[t]
    for p in paths:
        # print("tagged is %s" %(tagged,))
        if not p.excludes.intersection(tagged) and p.path[0] <= last_head:
            tagged.update(p.tags)
            return p.path[0], tagged, p.path
    return 18, set(), None


wheres = {
    1: "h3: right slot",
    2: "h2: right slot",
    3: "h1: right slot",
    8: "h3: hole",
    9: "h2: hole",
    10: "h1: hole",
    15: "h3: left slot",
    16: "h2: left slot",
    17: "h1: left slot",
}

h1_slot_bumps = {
    3: (0, 0,1), 
    10: (0,1,0),
    17: (1, 0,0)
    }


def find_threading(threadlist):
    tagged = set()
    last_head = 18
    hole = 0
    slots = [0, 0, 0]
    threads = [[], [], []]

    for ind, t in enumerate(threadlist):
        last_head, tagged, path = find_threading_for_shaft(last_head, tagged, t)

        if path is None:
            print("Next hole--------------")
            slots.append(0)
            slots.append(0)
            hole += 2
            threads.append([])
            threads.append([])
            last_head, tagged, path = find_threading_for_shaft(last_head, tagged, t)

        print("Path for %d is:" % (t,))
        for x in [wheres[i] for i in path if wheres.get(i)]:
            print("  " + x)

        print("slots before:" + str(slots[hole + 1]) + ":" + str(slots[hole]))
        for i in path:
            bumps = h1_slot_bumps.get(i)
            if bumps:
                r, h, l = bumps
                if r:
                    threads[hole].append(t)
                if h:
                    threads[hole + 1].append("hole:" + str(t))
                if l:
                    threads[hole + 2].append(t)
                slots[hole] += r
                slots[hole + 1] += l
        print("slots after:" + str(slots[hole + 1]) + ":" + str(slots[hole]))

    print(slots)
    for ind, tl in enumerate(threads):
        print("%s: %r" % (slots[ind], tl))


# find_threading([2,4,1,3,2,4])
# find_threading([4,1,2,1,4])
# find_threading([1, 2, 3, 2, 1, 2, 3])
# find_threading([1,2,3,4,1,2,3,4])

# find_threading([4, 3, 2, 1, 4, 3, 2, 1,4,3,2,1])
# point twill
find_threading(
    [3,4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4]
)

# twill
# find_threading([1,2,3,4,1,2,3,4,1,2,3,4])

# rev twill
# find_threading([4,3,2,1,4,3,2,1,4,3,2,1])
