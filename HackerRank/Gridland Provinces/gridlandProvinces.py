# https://www.hackerrank.com/contests/june-world-codesprint/challenges/gridland-provinces
# Read data

file_name = 'test case 1bis'


class Data:
    l = 0
    P = 0
    provinces = []
    c_province = []

    def __str__(self):
        return "l: " + str(self.l) \
               + " P: " + str(self.P) \
               + " provinces: " + str(self.provinces) \
               + " c_province: " + str(self.c_province)


data = Data()


def process_line_input(data_line, _data):
    # print("process_line_input", data_line, _data)
    _data.l += 1
    if _data.l == 1:
        _data.P = int(data_line[0])

    elif _data.l > 1:
        if _data.l % 3 == 0:
            _data.c_province = [data_line.rstrip()]
        if _data.l % 3 == 1:
            _data.c_province.append(data_line.rstrip())
            _data.provinces.append(_data.c_province)

###################################
# On local PC
with open(file_name, 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        process_line_input(line, data)
    print("data input", data)


# On HackerRank
# import fileinput
# for line in fileinput.input():
# 	process_line_input(line, data)

# Algo
# print("provinces:", provinces)

# pos = (provinceRow, provinceCol)
# s = pos at start (provinceRow, provinceCol, direction)
###################################

def print_province(_prov):
    paths = set([])

    for i, c in enumerate(_prov[0]):
        add_paths(paths, _prov, (0, i, -1), (0, i, -1), "")
        add_paths(paths, _prov, (0, i, 1), (0, i, 1), "")
    for i, c in enumerate(_prov[1]):
        add_paths(paths, _prov, (1, i, -1), (1, i, -1), "")
        add_paths(paths, _prov, (1, i, 1), (1, i, 1), "")

    print("len of paths", len(paths), _prov)
    print_province_paths(paths)


def add_paths_tail(paths, _prov, s, pos, path, just_changed_row, just_moved_forward, has_moved_forward_twice):
    # print("addPathsTail", s, pos, path)
    col = pos[1]

    if path == "auuabuubb":
        test = 1

    if not (in_borders(col, _prov)):
        return

    if is_final_path(path, _prov):
        paths.add(path)
        return

    turn_around = False
    direction = pos[2]

    # same row
    will_move_forward_twice = has_moved_forward_twice
    next_col = col + direction
    if in_borders(next_col, _prov):
        # test_position(_prov, (pos[0], next_col, direction))
        if just_moved_forward:
            will_move_forward_twice = True

        sm_dir_path = path + _prov[pos[0]][next_col]
        # print("same row", pos[0], next_col, sm_dir_path)
        add_paths_tail(paths, _prov, s, (pos[0], next_col, direction), sm_dir_path,
                       False, True, will_move_forward_twice)

    # turn around
    else:
        direction = -direction
        turn_around = True

    # change row
    other_row = 1 - pos[0]
    if (not just_changed_row) and (turn_around or not has_moved_forward_twice):
        ch_dir_path = path + _prov[other_row][col]
        # print("change row", other_row, col, ch_dir_path)
        add_paths_tail(paths, _prov, s, (other_row, col, direction), ch_dir_path,
                       True, False, has_moved_forward_twice)


def get_first_loop(_prov, s, pos, path):
    col = pos[1]
    # print("getFirstLoop", _prov, s, pos)

    path += _prov[pos[0]][col]

    # forward
    go_forth = False
    while in_borders(col + s[2], _prov):
        # print("forward", col)
        col += s[2]
        path += _prov[pos[0]][col]
        go_forth = True

    if not go_forth:
        return path, pos

    # turn around
    other_row = 1 - pos[0]
    other_direction = -pos[2]

    # backward
    while col != s[1] and in_borders(col, _prov):
        # print("backward", col)
        path += _prov[other_row][col]
        col += other_direction

    # adjust
    path += _prov[other_row][col]

    if is_final_path(path, _prov):
        return path, (other_row, col, other_direction)

    if in_borders(col + other_direction, _prov):
        col += other_direction
        path += _prov[other_row][col]

    return path, (other_row, col, other_direction)


def add_paths(paths, _prov, s, pos, path):
    (path, pos) = get_first_loop(_prov, s, pos, path)
    # print("got FirstLoop", _prov, s, pos, path)
    add_paths_tail(paths, _prov, s, pos, path, False, False, False)


def in_borders(col, _prov):
    return 0 <= col < len(_prov[0])


def is_final_path(path, _prov):
    return len(path) == 2 * len(_prov[0])


def test_position(_prov, pos):
    if pos[0] > 1 or pos[0] < 0:
        print("pos[0] out of boundaries", pos[0])
    if not len(_prov[0]) == len(_prov[1]):
        print("_prov uneven", _prov)
    if not in_borders(pos[1], _prov):
        print("not in borders", pos[1], len(_prov[0]))


def print_province_paths(_paths):
    print("province paths")
    for path in _paths:
        print(path)

# printProvince(provinces[1])
for prov in data.provinces:
    print_province(prov)
