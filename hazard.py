"""
Structural Hazards - In this code, we are assuming that the cache for memory and
instruction are separate. So, we will not have Structural hazards.

Data Hazards - this code solves for Data hazards

Control Hazards  - We always add 1 stall cycle (if no forwarding unit available) to the next instruction after bne
"""
instructions = [
    "add r1 r2 r3",
    "sub r5 r6 r7",
    "add r9 r1 r7",
    "sub r1 r2 r3",
]


def inst_parser(inst):
    arr = inst.split()
    res = []
    for a in arr:
        if a.startswith("0"):
            res.append(a[2:len(a) - 1])
        else:
            res.append(a)
    return res


default = ["F", "D", "X", "M", "W"]

hazards = []


def check_conflict_and_stall(
        res,
        instr,
        add_stall=False
):
    # Check data hazard
    new_inst_split = inst_parser(instr)
    new_inst_type = new_inst_split[0]

    # print(new_inst_split)
    care_about_regs = new_inst_split[2:]
    if new_inst_type == "sw":
        care_about_regs = new_inst_split[1:]
    if new_inst_type == "bne":
        care_about_regs = new_inst_split[1:]

    i = len(res) - 1
    prev_inst = res[i][0]
    # fdxmw_array = res[i][1]

    prev_inst_split = inst_parser(prev_inst)
    prev_inst_type = prev_inst_split[0]

    if prev_inst_type == "bne":
        hazards.append((prev_inst, instr, "Control hazard"))
        if add_stall:
            new_instr_cycles = ["S", "F", "D", "X", "M", "W"]
            return new_instr_cycles
        else:
            return ["F", "D", "X", "M", "W"]

    # Check for data hazards
    if prev_inst_type in ["add", "sub", "lw"]:
        reg_modified = prev_inst_split[1]
    elif prev_inst_type == "sw":
        reg_modified = prev_inst_split[2]

    # print("care about registers")
    # print(care_about_regs)
    # print("regs modified")
    # print(reg_modified)

    # Check if previous instr is bne, then add 1 stall cycle and return

    # if conflict, add 2 stall cycles and return
    if reg_modified.startswith("r") and reg_modified in care_about_regs:
        hazards.append((prev_inst, instr, "Data Hazard"))
        if add_stall:
            new_instr_cycles = ["F", "S", "S", "D", "X", "M", "W"]
            return new_instr_cycles

    i = len(res) - 2
    if i >= 0:
        prev_inst = res[i][0]
        # fdxmw_array = res[i][1]

        prev_inst_split = inst_parser(prev_inst)
        prev_inst_type = prev_inst_split[0]

        # Check for data hazards
        if prev_inst_type in ["add", "sub", "lw"]:
            reg_modified = prev_inst_split[1]
        elif prev_inst_type == "sw":
            reg_modified = prev_inst_split[2]

        # if conflict, add 1 stall cycle and return
        if reg_modified.startswith("r") and reg_modified in care_about_regs:
            hazards.append((prev_inst, instr, "Data Hazard"))
            if add_stall:
                new_instr_cycles = ["F", "S", "D", "X", "M", "W"]
                return new_instr_cycles

    return ["F", "D", "X", "M", "W"]


def check_conflict_and_stall_with_forwarding_unit(
        res,
        instr
):
    # Check data hazard
    new_inst_split = inst_parser(instr)
    new_inst_type = new_inst_split[0]

    i = len(res) - 1
    prev_inst = res[i][0]

    prev_inst_split = inst_parser(prev_inst)
    prev_inst_type = prev_inst_split[0]

    if prev_inst_type not in ["lw", "sw"]:
        last = res[len(res) - 1][1]
        if last == ["F", "D", "S", "X", "M", "W"]:
            return ["F", "S", "D", "X", "M", "W"]
        return ["F", "D", "X", "M", "W"]

    # print(new_inst_split)
    care_about_new_regs = new_inst_split[2:]
    if new_inst_type == "sw":
        care_about_new_regs = new_inst_split[1:]
    if new_inst_type == "bne":
        care_about_new_regs = new_inst_split[1:]

    if prev_inst_type == "lw":
        prev_reg_modified = prev_inst_split[1]
    elif prev_inst_type == "sw":
        prev_reg_modified = prev_inst_split[2]

    # print("care about new registers")
    # print(care_about_new_regs)
    # print("prev regs modified")
    # print(prev_reg_modified)

    # if conflict, add 1 stall cycle  and return
    if prev_reg_modified in care_about_new_regs:
        hazards.append((prev_inst, instr, "Data Hazard"))
        new_instr_cycles = ["F", "D", "S", "X", "M", "W"]
        return new_instr_cycles

    last = res[len(res) - 1][1]
    if last == ["F", "D", "S", "X", "M", "W"]:
        return ["F", "S", "D", "X", "M", "W"]
    return ["F", "D", "X", "M", "W"]


def format_res(res):
    for i in range(1, len(res)):
        fdxmw_arr = res[i][1]
        fdxmw_arr_1 = res[i-1][1]
        j = 0
        while True:
            if fdxmw_arr_1[j] in ["-", "F", "S"]:
                fdxmw_arr.insert(j, "-")
            else:
                break
            j = j + 1

        res[i] = (res[i][0], fdxmw_arr)


# Part 1
res_1 = [(instructions[0], default)]
for i in range(1, len(instructions)):
    fdxmw = check_conflict_and_stall(res_1, instructions[i], add_stall=False)
    res_1.append((instructions[i], fdxmw))
format_res(res_1)
print("Answer Part 1")
print("Printing clock cycles")
print(res_1)
print("---------------------------------------------------------------------------------------------------")
print("Hazard instructions are ")
print(hazards)

print("---------------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------------")

# Part 2
res_2 = [(instructions[0], default)]
hazards = []
for i in range(1, len(instructions)):
    fdxmw = check_conflict_and_stall(res_2, instructions[i], add_stall=True)
    res_2.append((instructions[i], fdxmw))
format_res(res_2)
print("Answer Part 2")
print("Printing clock cycles")
print(res_2)
print("---------------------------------------------------------------------------------------------------")
print("Hazard instructions are ")
print(hazards)

print("---------------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------------")

# Part 3
res_3 = [(instructions[0], default)]
hazards = []
for i in range(1, len(instructions)):
    fdxmw = check_conflict_and_stall_with_forwarding_unit(res_3, instructions[i])
    res_3.append((instructions[i], fdxmw))
format_res(res_3)
print("Answer Part 3")
print("Printing clock cycles")
print(res_3)
print("---------------------------------------------------------------------------------------------------")
print("Hazard instructions are ")
print(hazards)

print("---------------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------------")
