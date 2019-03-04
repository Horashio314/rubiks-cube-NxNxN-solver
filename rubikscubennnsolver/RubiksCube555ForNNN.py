#!/usr/bin/env python3

from rubikscubennnsolver import wing_strs_all, wing_str_map
from rubikscubennnsolver.RubiksSide import SolveError
from rubikscubennnsolver.misc import pre_steps_to_try
from rubikscubennnsolver.RubiksCube555 import (
    centers_555,
    edges_555,
    edges_partner_555,
    edges_recolor_pattern_555,
    l4e_wings_555,
    moves_555,
    wings_for_edges_pattern_555,
    LFRB_centers_555,
    RubiksCube555,
    LookupTableIDA555UDCentersStage,
    LookupTableIDA555LRCentersStage,
    LookupTableIDA555ULFRBDCentersSolve,
    LookupTable555UDTCenterStage,
    LookupTable555LRTCenterStageOdd,
    LookupTable555LRTCenterStageEven,
    LookupTable555TCenterSolve,
    LookupTable555XPlaneYPlaneEdgesOrientPairOneEdge,
    midges_for_horseshoe_555,
)
from rubikscubennnsolver.LookupTable import (
    LookupTable,
    LookupTableIDA,
    LookupTableHashCostOnly,
    NoSteps,
)
from pprint import pformat
import itertools
import logging
import sys

log = logging.getLogger(__name__)


class HorseShoeSolveError(SolveError):
    pass


class LookupTable555StageFirstSixEdges(LookupTable):
    """
    If we built this table the entire way it would have:
    (24!/(12!*12!)) * (12!/(6!*6!)) = 2,498,640,144 states

    lookup-table-5x5x5-step100-stage-first-six-edges.txt
    ====================================================
    1 steps has 56 entries (0 percent, 0.00x previous step)
    2 steps has 290 entries (0 percent, 5.18x previous step)
    3 steps has 386 entries (0 percent, 1.33x previous step)
    4 steps has 35 entries (0 percent, 0.09x previous step)
    5 steps has 5,581 entries (0 percent, 159.46x previous step)
    6 steps has 36,136 entries (0 percent, 6.47x previous step)
    7 steps has 204,948 entries (0 percent, 5.67x previous step)
    8 steps has 1,251,667 entries (1 percent, 6.11x previous step)
    9 steps has 6,462,383 entries (5 percent, 5.16x previous step)
    10 steps has 21,317,922 entries (19 percent, 3.30x previous step)
    11 steps has 80,163,256 entries (73 percent, 3.76x previous step)

    Total: 109,442,660 entries

    Extrapolating shows the table would roughly look like:

    12 steps has 301,413,842 entries (3.76x previous step)
    13 steps has 1,133,316,045 entries (3.76x previous step)
    14 steps has 954,467,585 entries (0.84x previous step)

    Average: 12.691952042454657
    Total  : 2,498,640,144
    """

    '''
    state_targets = (
        '---------LLL---LLLLLL---LLLLLLLLLLLL---LLLLLL------LLLLLL---LLL---------',
        '----L-L-L------LLLLLL------LLLLLL---LLLLLLLLLLLL---LLLLLL-------L-L-L---',
        '---L-L-L----LLLLLLLLLLLL---LLLLLL------LLLLLL------LLLLLL------L-L-L----',
        '---LLLLLL---LLL------LLL---------LLLLLL------LLL---------LLLLLLLLLLLLLLL',
        '---LLLLLL---LLL------LLL----L-L-L---LLLLLLLLLLLL---L-L-L-------LLLLLL---',
        '---LLLLLL---LLLLLLLLLLLL---L-L-L----LLL------LLL----L-L-L------LLLLLL---',
        'LLL------------LLLLLL------LLLLLL------LLLLLL---LLLLLLLLLLLL---------LLL',
        'LLL------LLL---------LLLLLL------LLL---------LLLLLL------LLLLLLLLLLLLLLL',
        'LLL------LLL----L-L-L---LLLLLLLLLLLL---L-L-L----LLL------LLLLLL------LLL',
        'LLL------LLL---L-L-L----LLL------LLL----L-L-L---LLLLLLLLLLLLLLL------LLL',
        'LLLLLLLLLLLLLLL---------LLL------LLLLLL---------LLL------LLLLLL------LLL',
        'LLLLLLLLLLLLLLL------LLLLLL---------LLL------LLLLLL------------LLLLLL---',
    )
    '''

    state_targets = (
        '0071f8fff1f81f8e00',
        '0a81f81f8fff1f80a8',
        '150fff1f81f81f8150',
        '1f8e07007e07007fff',
        '1f8e070a8fff1501f8',
        '1f8fff150e070a81f8',
        'e001f81f81f8fff007',
        'e07007e07007e07fff',
        'e070a8fff150e07e07',
        'e07150e070a8fffe07',
        'fffe00e07e00e07e07',
        'fffe07e00e07e001f8',
    )

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            'lookup-table-5x5x5-step100-stage-first-six-edges.txt',
            self.state_targets,

            # 10-deep...edges solutions average 43.5 over 10 test cubes
            linecount=28905188,
            filesize=1647595716,

            # 11-deep...edges solutions average 43.8 over 10 test cubes
            #linecount=109442660,
            #filesize=6566560320,
        )

    def state(self, wing_strs_to_stage):
        state = self.parent.state[:]

        for square_index in l4e_wings_555:
            partner_index = edges_partner_555[square_index]
            square_value = state[square_index]
            partner_value = state[partner_index]
            wing_str = wing_str_map[square_value + partner_value]

            if wing_str in wing_strs_to_stage:
                state[square_index] = '1'
                state[partner_index] = '1'
            else:
                state[square_index] = '0'
                state[partner_index] = '0'

        edges_state = ''.join([state[square_index] for square_index in edges_555])
        edges_state = int(edges_state, 2)
        edges_state = self.hex_format % edges_state
        return edges_state


class LookupTable555SolveFirstSixEdges(LookupTable):
    """
    lookup-table-5x5x5-step100-solve-first-six-edges.txt
    ====================================================
    2 steps has 1 entries (0 percent, 0.00x previous step)
    5 steps has 10 entries (0 percent, 10.00x previous step)
    6 steps has 93 entries (0 percent, 9.30x previous step)
    7 steps has 360 entries (0 percent, 3.87x previous step)
    8 steps has 755 entries (0 percent, 2.10x previous step)
    9 steps has 5,001 entries (0 percent, 6.62x previous step)
    10 steps has 19,652 entries (0 percent, 3.93x previous step)
    11 steps has 78,556 entries (0 percent, 4.00x previous step)
    12 steps has 400,860 entries (0 percent, 5.10x previous step)
    13 steps has 1,899,168 entries (0 percent, 4.74x previous step)
    14 steps has 8,393,229 entries (3 percent, 4.42x previous step)
    15 steps has 32,970,960 entries (13 percent, 3.93x previous step)
    16 steps has 116,204,620 entries (46 percent, 3.52x previous step)
    17 steps has 90,764,224 entries (36 percent, 0.78x previous step) PARTIAL

    Total: 250,737,489 entries

    How many entries are left?
        12! is 479,001,600
        12! - 159,973,265 = 319,028,335

    How many moves would it take to reach them?
        depth 17 would roughly add 3.5 x 116,204,620 = 406,716,170
        So there might be a few beyond depth 17 but not many at all.
    """
    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            'lookup-table-5x5x5-step100-solve-first-six-edges.txt',
            'OOopPPQQqrRRsSSTTtuUUVVvWWwxXXYYyzZZ',

            linecount=250737489,
            max_depth=17,
            filesize=24823011411)

            #linecount=35665293,
            #max_depth=14,
            #filesize=3174211077)

    def ida_heuristic(self):
        state = edges_recolor_pattern_555(self.parent.state[:])
        edges_state = ''.join([state[index] for index in wings_for_edges_pattern_555])

        #  UB  UL  UR  UF  LB  LF  RF  RB  DF  DL  DR  DB
        # OOo pPP QQq rRR sSS TTt uUU VVv WWw xXX YYy zZZ
        # 000 000 000 011 111 111 112 222 222 222 333 333
        # 012 345 678 901 234 567 890 123 456 789 012 345

        # For the horseshoe patter we only care about UB, UL, UR, UF, DF and DB
        # Treat LB LF RF FB DL DR as paired
        edges_state = edges_state[0:12] + "sSSTTtuUUVVv" + edges_state[24:27] + "xXXYYy" + edges_state[33:36]
        #log.info("%s: edges_state %s" % (self, edges_state))

        cost_to_goal = self.heuristic(edges_state)

        return (edges_state, cost_to_goal)


class LookupTable555StageFirstFourEdges(LookupTable):
    """
    lookup-table-5x5x5-step100-stage-first-four-edges.txt
    =====================================================
    1 steps has 9 entries (0 percent, 0.00x previous step)
    2 steps has 72 entries (0 percent, 8.00x previous step)
    3 steps has 330 entries (0 percent, 4.58x previous step)
    4 steps has 84 entries (0 percent, 0.25x previous step)
    5 steps has 1,152 entries (0 percent, 13.71x previous step)
    6 steps has 10,200 entries (0 percent, 8.85x previous step)
    7 steps has 53,040 entries (0 percent, 5.20x previous step)
    8 steps has 187,296 entries (2 percent, 3.53x previous step)
    9 steps has 1,357,482 entries (18 percent, 7.25x previous step)
    10 steps has 5,779,878 entries (78 percent, 4.26x previous step)

    Total: 7,389,543 entries

    There is no need to build this any deeper...building it to 10-deep
    takes about 2 days on a 12-core machine.
    """
    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            'lookup-table-5x5x5-step100-stage-first-four-edges.txt',
            'TBD',
            linecount=7389543,
            filesize=421203951,
        )

    def state(self, wing_strs_to_stage):
        state = self.parent.state[:]

        for square_index in l4e_wings_555:
            partner_index = edges_partner_555[square_index]
            square_value = state[square_index]
            partner_value = state[partner_index]
            wing_str = wing_str_map[square_value + partner_value]

            if wing_str in wing_strs_to_stage:
                state[square_index] = '1'
                state[partner_index] = '1'
            else:
                state[square_index] = '0'
                state[partner_index] = '0'

        edges_state = ''.join([state[square_index] for square_index in edges_555])
        edges_state = int(edges_state, 2)
        edges_state = self.hex_format % edges_state
        return edges_state


class LookupTable555StageSecondFourEdges(LookupTable):
    """
    lookup-table-5x5x5-step101-stage-second-four-edges.txt
    ======================================================
    5 steps has 32 entries (0 percent, 0.00x previous step)
    6 steps has 304 entries (0 percent, 9.50x previous step)
    7 steps has 1,208 entries (0 percent, 3.97x previous step)
    8 steps has 3,612 entries (1 percent, 2.99x previous step)
    9 steps has 12,856 entries (3 percent, 3.56x previous step)
    10 steps has 42,688 entries (12 percent, 3.32x previous step)
    11 steps has 89,194 entries (26 percent, 2.09x previous step)
    12 steps has 113,508 entries (33 percent, 1.27x previous step)
    13 steps has 74,720 entries (22 percent, 0.66x previous step)

    Total: 338,122 entries

    This should have (16!/(8!*8!)) * (8!/(4!*4!)) or 900,900 entries
    if you built it out the entire way. We do not need to build it that deep
    though, we can try enough edge color combinations to find a hit
    in 13-deep.
    """

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            'lookup-table-5x5x5-step101-stage-second-four-edges.txt',
            'TBD',
            linecount=338122,
            filesize=28740370)

    def state(self, wing_strs_to_stage):
        state = self.parent.state[:]

        for square_index in l4e_wings_555:
            partner_index = edges_partner_555[square_index]
            square_value = state[square_index]
            partner_value = state[partner_index]
            wing_str = wing_str_map[square_value + partner_value]

            if wing_str in wing_strs_to_stage:
                state[square_index] = 'U'
                state[partner_index] = 'U'
            else:
                state[square_index] = 'x'
                state[partner_index] = 'x'

        edges_state = ''.join([state[square_index] for square_index in l4e_wings_555])
        return edges_state


class LookupTable555EdgesXPlaneEdgesOnly(LookupTable):
    """
    lookup-table-5x5x5-step301-edges-x-plane-edges-only.txt
    =======================================================
    1 steps has 7 entries (0 percent, 0.00x previous step)
    2 steps has 21 entries (0 percent, 3.00x previous step)
    3 steps has 90 entries (0 percent, 4.29x previous step)
    4 steps has 358 entries (0 percent, 3.98x previous step)
    5 steps has 1,204 entries (2 percent, 3.36x previous step)
    6 steps has 2,656 entries (6 percent, 2.21x previous step)
    7 steps has 6,084 entries (15 percent, 2.29x previous step)
    8 steps has 6,652 entries (16 percent, 1.09x previous step)
    9 steps has 9,016 entries (22 percent, 1.36x previous step)
    10 steps has 7,576 entries (18 percent, 0.84x previous step)
    11 steps has 5,480 entries (13 percent, 0.72x previous step)
    12 steps has 984 entries (2 percent, 0.18x previous step)
    13 steps has 192 entries (0 percent, 0.20x previous step)

    Total: 40,320 entries
    Average: 8.71 moves
    """

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            'lookup-table-5x5x5-step301-edges-x-plane-edges-only.txt',
            '------------sSSTTtuUUVVv------------',
            linecount=40320,
            max_depth=13,
            filesize=3346560)

    def ida_heuristic(self):
        assert self.only_colors and len(self.only_colors) == 4, "You must specify which 4-edges"
        state = edges_recolor_pattern_555(self.parent.state[:], self.only_colors)
        edges_state = ''.join([state[index] for index in wings_for_edges_pattern_555])
        cost_to_goal = self.heuristic(edges_state)
        return (edges_state, cost_to_goal)


class LookupTable555EdgesXPlaneCentersOnly(LookupTable):
    """
    lookup-table-5x5x5-step302-edges-x-plane-centers-only.txt
    =========================================================
    1 steps has 7 entries (0 percent, 0.00x previous step)
    2 steps has 33 entries (1 percent, 4.71x previous step)
    3 steps has 162 entries (6 percent, 4.91x previous step)
    4 steps has 504 entries (20 percent, 3.11x previous step)
    5 steps has 1,182 entries (46 percent, 2.35x previous step)
    6 steps has 632 entries (25 percent, 0.53x previous step)

    Total: 2,520 entries
    Average: 4.87 moves
    """

    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            'lookup-table-5x5x5-step302-edges-x-plane-centers-only.txt',
            'LLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBB',
            linecount=2520,
            max_depth=6,
            filesize=146160)

    def ida_heuristic(self):
        parent_state = self.parent.state
        state = ''.join([parent_state[x] for x in LFRB_centers_555])
        cost_to_goal = self.heuristic(state)
        return (state, cost_to_goal)


class LookupTableIDA555EdgesXPlane(LookupTableIDA):
    """
    lookup-table-5x5x5-step300-edges-x-plane.txt
    ============================================
    1 steps has 7 entries (0 percent, 0.00x previous step)
    2 steps has 33 entries (0 percent, 4.71x previous step)
    3 steps has 230 entries (0 percent, 6.97x previous step)
    4 steps has 1,414 entries (0 percent, 6.15x previous step)
    5 steps has 8,768 entries (2 percent, 6.20x previous step)
    6 steps has 50,346 entries (14 percent, 5.74x previous step)
    7 steps has 280,506 entries (82 percent, 5.57x previous step)

    Total: 341,304 entries
    """

    def __init__(self, parent):
        LookupTableIDA.__init__(
            self,
            parent,
            'lookup-table-5x5x5-step300-edges-x-plane.txt',
            ('LLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBB------------sSSTTtuUUVVv------------', ),
            moves_555,
            # illegal moves
            (),

            linecount=341304,
            max_depth=7,
            filesize=35154312,

            legal_moves = (
                "L2", "F2", "R2", "B2",
                "Uw", "Uw'", "Uw2",
                "Dw", "Dw'", "Dw2",
            )
        )

    def ida_heuristic(self):
        parent_state = self.parent.state
        (edges_state, edges_cost) = self.parent.lt_edges_x_plane_edges_only.ida_heuristic()
        (centers_state, centers_cost) = self.parent.lt_edges_x_plane_centers_only.ida_heuristic()

        lt_state = centers_state + edges_state
        cost_to_goal = max(edges_cost, centers_cost)

        if cost_to_goal > 0:
            steps = self.steps(lt_state)

            if steps:
                cost_to_goal = len(steps)
            else:
                cost_to_goal = max(cost_to_goal, self.max_depth + 1)

        return (lt_state, cost_to_goal)


class LookupTable555EdgesXPlaneCentersSolved(LookupTable):
    """
    lookup-table-5x5x5-step310-edges-x-plane-with-solved-centers.txt
    ================================================================
    1 steps has 1 entries (0 percent, 0.00x previous step)
    5 steps has 10 entries (0 percent, 10.00x previous step)
    6 steps has 45 entries (0 percent, 4.50x previous step)
    7 steps has 196 entries (0 percent, 4.36x previous step)
    8 steps has 452 entries (1 percent, 2.31x previous step)
    9 steps has 1,556 entries (3 percent, 3.44x previous step)
    10 steps has 3,740 entries (9 percent, 2.40x previous step)
    11 steps has 10,188 entries (25 percent, 2.72x previous step)
    12 steps has 16,778 entries (41 percent, 1.65x previous step)
    13 steps has 6,866 entries (17 percent, 0.41x previous step)
    14 steps has 488 entries (1 percent, 0.07x previous step)

    Total: 40,320 entries
    Average: 11.56 moves
    """
    def __init__(self, parent):
        LookupTable.__init__(
            self,
            parent,
            'lookup-table-5x5x5-step310-edges-x-plane-with-solved-centers.txt',
            '------------sSSTTtuUUVVv------------',
            linecount=40320,
            max_depth=14,
            filesize=3427200)

    def ida_heuristic(self):
        assert self.only_colors and len(self.only_colors) == 4, "You must specify which 4-edges"
        state = edges_recolor_pattern_555(self.parent.state[:], self.only_colors)
        edges_state = ''.join([state[index] for index in wings_for_edges_pattern_555])
        cost_to_goal = self.heuristic(edges_state)
        #log.info("%s: edges_state %s" % (self, edges_state))
        return (edges_state, cost_to_goal)



class RubiksCube555ForNNN(RubiksCube555):
    """
    5x5x5 strategy
    - stage UD centers to sides U or D (use IDA)
    - stage LR centers to sides L or R...this in turn stages FB centers to sides F or B
    - solve all centers (use IDA)
    - pair edges
    - solve as 3x3x3
    """

    def lt_init(self):
        if self.lt_init_called:
            return
        self.lt_init_called = True

        self.lt_UD_centers_stage = LookupTableIDA555UDCentersStage(self)
        self.lt_LR_centers_stage = LookupTableIDA555LRCentersStage(self)
        self.lt_ULFRBD_centers_solve = LookupTableIDA555ULFRBDCentersSolve(self)
        self.lt_UD_T_centers_stage = LookupTable555UDTCenterStage(self)
        self.lt_LR_T_centers_stage_odd = LookupTable555LRTCenterStageOdd(self)
        self.lt_LR_T_centers_stage_even = LookupTable555LRTCenterStageEven(self)
        self.lt_ULFRBD_t_centers_solve = LookupTable555TCenterSolve(self)

        # No need to preload these, they use binary_seach_multiple
        self.lt_edges_stage_first_four = LookupTable555StageFirstFourEdges(self)
        self.lt_edges_stage_second_four = LookupTable555StageSecondFourEdges(self)
        self.lt_edges_stage_first_six = LookupTable555StageFirstSixEdges(self)
        self.lt_edges_solve_first_six = LookupTable555SolveFirstSixEdges(self)

        self.lt_edges_x_plane_centers_solved = LookupTable555EdgesXPlaneCentersSolved(self)

    def verify_horse_shoe(self, horse_shoe_edges):

        horse_shoe_edges_555 = (
            2, 3, 4,
            6, 11, 16,
            10, 15, 20,
            22, 23, 24,
            127, 128, 129,
            147, 148, 149
        )
        horse_shoe_wing_strs = set()

        for square_index in horse_shoe_edges_555:
            partner_index = edges_partner_555[square_index]
            square_value = self.state[square_index]
            partner_value = self.state[partner_index]
            wing_str = wing_str_map[square_value + partner_value]
            horse_shoe_wing_strs.add(wing_str)

        if len(horse_shoe_wing_strs) != 6:
            raise SolveError("{} is not a horse_shoe...{}".format(horse_shoe_edges, horse_shoe_wing_strs))

    def rotate_horse_shoe(self, wing_strs):
        """
        rotate the cube so that the horse-shoe pattern has 4 unpaired edges on side U
        and the other two at DF DB
        """
        horse_shoe_edges = []

        for square_index in midges_for_horseshoe_555:
            partner_index = edges_partner_555[square_index]
            square_value = self.state[square_index]
            partner_value = self.state[partner_index]
            wing_str = wing_str_map[square_value + partner_value]

            if wing_str in wing_strs:
                horse_shoe_edges.append(square_index)

        horse_shoe_edges.sort()

        if horse_shoe_edges == [23, 36, 40, 86, 90, 128]:
            self.rotate("x")
            self.rotate("y")

        elif horse_shoe_edges == [3, 23, 128, 136, 140, 148]:
            self.rotate("x")
            self.rotate("x")

        elif horse_shoe_edges == [3, 11, 15, 23, 128, 148]:
            pass

        elif horse_shoe_edges == [3, 11, 15, 23, 136, 140]:
            self.rotate("y")

        elif horse_shoe_edges == [11, 15, 86, 90, 136, 140]:
            self.rotate("z'")
            self.rotate("y")

        elif horse_shoe_edges == [11, 15, 36, 40, 136, 140]:
            self.rotate("z")
            self.rotate("y")

        elif horse_shoe_edges == [15, 36, 40, 86, 90, 140]:
            self.rotate("z'")

        elif horse_shoe_edges == [11, 36, 40, 86, 90, 136]:
            self.rotate("z")

        elif horse_shoe_edges == [11, 15, 128, 136, 140, 148]:
            self.rotate("x")
            self.rotate("x")
            self.rotate("y")

        elif horse_shoe_edges == [3, 36, 40, 86, 90, 148]:
            self.rotate("x'")
            self.rotate("y")

        elif horse_shoe_edges == [3, 23, 40, 86, 128, 148]:
            self.rotate("x")

        elif horse_shoe_edges == [3, 23, 36, 90, 128, 148]:
            self.rotate("x'")

        #elif horse_shoe_edges == [23, 36, 40, 90, 136, 140]:
        #    self.rotate("")
        #    self.rotate("")

        else:
            #self.print_horse_shoe()
            self.print_cube()
            self.print_cube_layout()
            log.info("Add horse shoe support for {}".format(horse_shoe_edges))
            sys.exit(0)

        self.verify_horse_shoe(horse_shoe_edges)

    def print_horse_shoe(self, wing_strs):

        # Remember what things looked like
        original_state = self.state[:]

        self.nuke_corners()
        self.nuke_centers()

        for square_index in edges_555:
            partner_index = edges_partner_555[square_index]
            square_value = self.state[square_index]
            partner_value = self.state[partner_index]

            if square_value == "L" and partner_value == "L":
                pass
            else:
                wing_str = wing_str_map[square_value + partner_value]
                if wing_str in wing_strs:
                    pass
                else:
                    self.state[square_index] = "-"
                    self.state[partner_index] = "-"

        self.print_cube()
        self.state = original_state[:]

    def stage_first_six_edges_555(self, max_pre_steps_length):
        """
        There are 12!/(6!*6!) or 924 different permutations of 6-edges out of 12-edges, use the one
        that gives us the shortest solution for getting 6-edges staged.
        """
        log.info("%s: stage_first_six_edges_555 called with max_pre_steps_length %d" % (self, max_pre_steps_length))

        # Remember what things looked like
        original_state = self.state[:]
        original_solution = self.solution[:]
        original_solution_len = len(self.solution)

        min_solution_len = None
        min_solution_steps = None
        min_wing_strs = None
        states_to_find = set()
        state_to_wing_str_combo = {}
        state_to_pre_steps = {}

        for pre_steps in pre_steps_to_try:

            if len(pre_steps) > max_pre_steps_length:
                break

            self.state = original_state[:]
            self.solution = original_solution[:]

            #log.info("")
            #log.info("")
            #log.info("%s: pre_steps %s" % (self, " ".join(pre_steps)))
            for step in pre_steps:
                self.rotate(step)

            #post_pre_steps_state = self.state[:]
            #post_pre_steps_solution = self.solution[:]

            for wing_strs in itertools.combinations(wing_strs_all, 6):
                # Uncomment to test a specific wing_str
                '''
                exit_now = False

                for x in ('UF', 'UL', 'UB', 'UR', 'DF', 'DB'):
                    if x not in wing_strs:
                        exit_now = True
                        break

                if exit_now:
                    continue
                '''

                state = self.lt_edges_stage_first_six.state(wing_strs)
                state_to_wing_str_combo[state] = wing_strs
                state_to_pre_steps[(wing_strs, state)] = pre_steps
                states_to_find.add(state)
                #assert state.count("L") == 36
                #assert state.count("-") == 36

        states_to_find = sorted(list(states_to_find))
        log.info("%s: %d states_to_find" % (self, len(states_to_find)))
        #log.info("%s: states_to_find\n%s\n" % (self, "\n".join(states_to_find)))
        results = self.lt_edges_stage_first_six.binary_search_multiple(states_to_find)
        len_results = len(results)
        log.info("%s: %d/%d states found" % (self, len(results), len(states_to_find)))
        #log.info("%s: results\n%s\n" % (self, pformat(results)))

        # We sort the keys of the dict so that the order is the same everytime, this isn't
        # required but makes troubleshooting easier.
        for (line_number, key) in enumerate(sorted(results.keys())):

            if key in self.lt_edges_stage_first_six.state_targets:
                steps = ""
            else:
                steps = results[key]

            #self.state = post_pre_steps_state[:]
            #self.solution = post_pre_steps_solution[:]
            self.state = original_state[:]
            self.solution = original_solution[:]
            wing_strs = state_to_wing_str_combo[key]
            pre_steps = state_to_pre_steps[(wing_strs, key)]

            for step in pre_steps:
                self.rotate(step)

            for step in steps.split():
                self.rotate(step)

            self.rotate_horse_shoe(wing_strs)
            #self.print_horse_shoe(wing_strs)

            solution_steps = self.solution[original_solution_len:]

            try:
                self.pair_first_six_edges_555(False)

                if not self.edges_paired():
                    if min_solution_len:
                        solve_steps = self.solution[original_solution_len:]
                        #solution_len = len(solve_steps)
                        solution_len = self.get_solution_len_minus_rotates(solve_steps)
                        if solution_len + 1 >= min_solution_len:
                            log.info("%s: %d/%d SKIP solution_len is %d but min_solution_len is %d" % (
                                self, line_number+1, len_results, solution_len, min_solution_len))
                            continue

                    self.rotate("z")

                    # It doesn't appear to matter much if you do D2 R2 vs U2 L2
                    self.rotate("D2")
                    self.rotate("R2")
                    #self.rotate("U2")
                    #self.rotate("L2")
                    self.pair_first_six_edges_555(False)

            except NoSteps as e:
                #log.info("%s: %d/%d 1st 6-edges can be staged in %d steps but we do not have an entry to solve them (16-deep for now)" % (
                #    self, line_number+1, len_results, self.get_solution_len_minus_rotates(solution_steps)))
                continue

            solve_steps = self.solution[original_solution_len:]
            solution_len = self.get_solution_len_minus_rotates(solve_steps)
            #solution_len = len(solve_steps)

            if min_solution_len is None or solution_len < min_solution_len:
                log.warning("%s: %d/%d 1st 6-edges can be staged in %d steps %s (NEW MIN)" % (
                    self, line_number+1, len_results, solution_len, ' '.join(solution_steps)))
                min_solution_len = solution_len
                min_solution_steps = solution_steps
                min_wing_strs = wing_strs
            else:
                log.info("%s: %d/%d 1st 6-edges can be staged in %d steps" % (
                    self, line_number+1, len_results, solution_len))

        # For some cubes we sometimes find long solutions when max_pre_steps_length is 0, if this is
        # the case pretend we did not find a solution at all so that we will try again with
        # max_pre_steps_length of 1 which will give us way more options to choose from. Even though
        # we add one pre_step it finds a shorter overall solution.
        if max_pre_steps_length is 0 and min_solution_len is not None and min_solution_len >= 46:
            min_solution_len = None

        if min_solution_len is not None:
            self.state = original_state[:]
            self.solution = original_solution[:]

            for step in min_solution_steps:
                self.rotate(step)

            self.print_horse_shoe(min_wing_strs)

            if min_solution_steps:
                log.info("%s: 1st 6-edges staged to horseshoe via %s" % (self, " ".join(min_solution_steps)))
                horseshoe_len = self.get_solution_len_minus_rotates(self.solution[original_solution_len:])
                self.solution.append("COMMENT_%d_steps_555_horseshoe_staged" % self.get_solution_len_minus_rotates(self.solution[original_solution_len:]))
                log.info("%s: 1st 6-edges staged to horseshoe, %d steps in" % (self, self.get_solution_len_minus_rotates(self.solution)))
            else:
                log.info("%s: 1st 6-edges already staged to horseshoe" % self)

        else:
            self.state = original_state[:]
            self.solution = original_solution[:]
            raise HorseShoeSolveError("Could not pair horseshoe edges")

    def pair_first_six_edges_555(self, print_the_cube):

        # Remember what things looked like
        original_state = self.state[:]
        original_solution = self.solution[:]
        original_solution_len = len(self.solution)

        # Recolor the edges to they are all oriented using their original orientation.
        # We do this because our tables were built with all edges at their original orientation.
        self.edges_flip_to_original_orientation()

        # Now we can solve
        self.lt_edges_solve_first_six.solve()

        # Put the cube back the way it was (to undo all of the recoloring we did) and apply the solution
        six_edges_solution = self.solution[original_solution_len:]
        self.state = original_state[:]
        self.solution = original_solution[:]

        for step in six_edges_solution:
            self.rotate(step)

        if print_the_cube:
            self.print_cube()
            self.solution.append("COMMENT_%d_steps_555_six_edges_paired" %\
                self.get_solution_len_minus_rotates(self.solution[original_solution_len:]))
            log.info("%s: 6-edges paired in %d steps, %d steps in" %\
                (self, len(six_edges_solution), self.get_solution_len_minus_rotates(self.solution)))

    def stage_first_four_edges_555(self):
        """
        There are 495 different permutations of 4-edges out of 12-edges, use the one
        that gives us the shortest solution for getting 4-edges staged to LB, LF, RF, RB
        """

        # return if they are already staged
        if self.x_plane_edges_are_l4e():
            log.info("%s: first L4E group in x-plane" % self)
            return

        if self.y_plane_edges_are_l4e():
            log.info("%s: first L4E group in y-plane, moving to x-plane" % self)
            self.rotate("z")
            return

        if self.z_plane_edges_are_l4e():
            log.info("%s: first L4E group in z-plane, moving to x-plane" % self)
            self.rotate("x")
            return

        min_solution_len = None
        min_solution_steps = None

        # The table for staging the 1st 4-edges would have 364,058,145 if built to completion.
        # Building that table the entire way is difficult though because this is a table where
        # the centers must be kept solved...so this involves building out a HUGE table and only
        # keeping the entries where the centers are solved.  To build one deep enough to find
        # all 364,058,145 entries needed that also have solved centers would probably take a
        # few months and more drive space than I have access to.
        #
        # To avoid building such a massive table we only build the table out 10-deep which gives
        # us a few million entries.  We then try all 495 permutations of 4-edges out of 12-edges
        # looking for one that does have a hit.  Most of the time this is all that is needed and
        # we can find a hit.  On the off chance that we cannot though we need a way to find a solution
        # so what we do is try all outer layer moves up to 3 moves deep and see if any of those
        # sequences put the cube in a state such that one of the 495 edge permutations does find
        # a hit. I have yet to find a cube that cannot be solved with this approach but if I did
        # the pre_steps_to_try could be expanded to 4-deep.

        # Remember what things looked like
        original_state = self.state[:]
        original_solution = self.solution[:]
        original_solution_len = len(self.solution)

        min_solution_len = None
        min_solution_steps = None

        for pre_steps in pre_steps_to_try:
            self.state = original_state[:]
            self.solution = original_solution[:]

            #log.info("")
            #log.info("")
            #log.info("%s: pre_steps %s" % (self, " ".join(pre_steps)))
            for step in pre_steps:
                self.rotate(step)

            post_pre_steps_state = self.state[:]
            post_pre_steps_solution = self.solution[:]
            states_to_find = []

            for wing_strs in itertools.combinations(wing_strs_all, 4):
                states_to_find.append(self.lt_edges_stage_first_four.state(wing_strs))

            log.info("%s: %d states_to_find" % (self, len(states_to_find)))
            results = self.lt_edges_stage_first_four.binary_search_multiple(states_to_find)
            len_results = len(results)
            log.info("%s: %d states found" % (self, len(results)))

            # We sort the keys of the dict so that the order is the same everytime, this isn't
            # required but makes troubleshooting easier.
            for (line_number, key) in enumerate(sorted(results.keys())):
                steps = results[key]
                self.state = post_pre_steps_state[:]
                self.solution = post_pre_steps_solution[:]

                for step in steps.split():
                    self.rotate(step)

                self.stage_final_four_edges_in_x_plane()
                solution_steps = self.solution[original_solution_len:]
                solution_len = self.get_solution_len_minus_rotates(solution_steps)

                # Technically we only need 4 edges to be pairable for the next phase but 5 is nice because it gives
                # the next phase some wiggle room...it can choose the best 4-edge tuple.
                if min_solution_len is None or solution_len < min_solution_len:
                    log.info("%s: %d/%d 1st 4-edges can be staged in %d steps %s (NEW MIN)" % (
                        self, line_number+1, len_results, solution_len, ' '.join(solution_steps)))
                    min_solution_len = solution_len
                    min_solution_steps = solution_steps
                else:
                    log.info("%s: %d/%d 1st 4-edges can be staged in %d steps" % (
                        self, line_number+1, len_results, solution_len))

            if min_solution_len is not None:
                self.state = original_state[:]
                self.solution = original_solution[:]

                for step in min_solution_steps:
                    self.rotate(step)
                break

        if not self.x_plane_edges_are_l4e():
            raise SolveError("There should be an L4E group in x-plane but there is not")

        #self.print_cube()
        self.solution.append("COMMENT_%d_steps_555_first_L4E_edges_staged" % self.get_solution_len_minus_rotates(self.solution[original_solution_len:]))
        log.info("%s: 1st 4-edges staged to x-plane, %d steps in" % (self, self.get_solution_len_minus_rotates(self.solution)))

    def stage_second_four_edges_555(self):
        """
        The 1st 4-edges have been staged to LB, LF, RF, RB. Stage the next four
        edges to UB, UF, DF, DB (this in turn stages the final four edges).

        Since there are 8-edges there are 70 different combinations of edges we can
        choose to stage to UB, UF, DF, DB. Walk through all 70 combinations and see
        which one leads to the shortest solution.
        """

        # return if they are already staged
        if self.y_plane_edges_are_l4e() and self.z_plane_edges_are_l4e():
            return

        first_four_wing_strs = list(self.get_x_plane_wing_strs())
        wing_strs_for_second_four = []

        log.info("first_four_wing_strs %s" % pformat(first_four_wing_strs))

        for wing_str in wing_strs_all:
            if wing_str not in first_four_wing_strs:
                wing_strs_for_second_four.append(wing_str)

        log.info("wing_strs_for_second_four %s" % pformat(wing_strs_for_second_four))
        assert len(wing_strs_for_second_four) == 8

        # Remember what things looked like
        original_state = self.state[:]
        original_solution = self.solution[:]
        original_solution_len = len(self.solution)

        min_solution_len = None
        min_solution_steps = None

        for pre_steps in pre_steps_to_try:
            self.state = original_state[:]
            self.solution = original_solution[:]

            for step in pre_steps:
                self.rotate(step)

            post_pre_steps_state = self.state[:]
            post_pre_steps_solution = self.solution[:]
            states_to_find = []

            for wing_strs in itertools.combinations(wing_strs_for_second_four, 4):
                states_to_find.append(self.lt_edges_stage_second_four.state(wing_strs))

            log.info("%s: %d states_to_find" % (self, len(states_to_find)))
            results = self.lt_edges_stage_second_four.binary_search_multiple(states_to_find)
            len_results = len(results)
            #log.info(results)
            log.info("%s: %d states found" % (self, len(results)))

            # We sort the keys of the dict so that the order is the same everytime, this isn't
            # required but makes troubleshooting easier.
            for (line_number, key) in enumerate(sorted(results.keys())):
                steps = results[key]
                self.state = post_pre_steps_state[:]
                self.solution = post_pre_steps_solution[:]

                for step in steps.split():
                    self.rotate(step)

                solution_steps = self.solution[original_solution_len:]
                solution_len = len(solution_steps)

                if min_solution_len is None or solution_len < min_solution_len:
                    log.info("%s: %d/%d 2nd 4-edges can be staged in %d steps %s (NEW MIN)" % (
                        self, line_number+1, len_results, solution_len, ' '.join(solution_steps)))
                    min_solution_len = solution_len
                    min_solution_steps = solution_steps
                else:
                    log.info("%s: %d/%d 2nd 4-edges can be staged in %d steps" % (
                        self, line_number+1, len_results, solution_len))

            if min_solution_len is not None:
                self.state = original_state[:]
                self.solution = original_solution[:]

                for step in min_solution_steps:
                    self.rotate(step)
                break

        self.state = original_state[:]
        self.solution = original_solution[:]

        if min_solution_len is None:
            raise SolveError("Could not find 4-edges to stage")
        else:
            for step in min_solution_steps:
                self.rotate(step)

        self.solution.append("COMMENT_%d_steps_555_second_L4E_edges_staged" % self.get_solution_len_minus_rotates(self.solution[original_solution_len:]))
        log.info("%s: 2nd 4-edges staged to x-plane, %d steps in" % (self, self.get_solution_len_minus_rotates(self.solution)))

    def stage_final_four_edges_in_x_plane(self):
        original_state = self.state[:]
        original_solution = self.solution[:]

        # Traverse a table of moves that place L4E in one of three planes
        # and then rotate that plane to the x-plane
        for pre_steps in pre_steps_to_try:
            self.state = original_state[:]
            self.solution = original_solution[:]
            steps = None

            for step in pre_steps:
                self.rotate(step)

            if self.x_plane_edges_are_l4e() and self.x_plane_edges_unpaired_count() > 0:
                #if pre_steps:
                #    log.info("%s: %s puts L4E group in x-plane" % (self, "".join(pre_steps)))
                #else:
                #    log.info("%s: L4E group in x-plane" % self)
                break

            elif self.y_plane_edges_are_l4e() and self.y_plane_edges_unpaired_count() > 0:
                #if pre_steps:
                #    log.info("%s: %s puts L4E group in y-plane, moving to x-plane" % (self, "".join(pre_steps)))
                #else:
                #    log.info("%s: L4E group in y-plane, moving to x-plane" % self)
                self.rotate("z")
                break

            elif self.z_plane_edges_are_l4e() and self.z_plane_edges_unpaired_count() > 0:
                #if pre_steps:
                #    log.info("%s: %s puts L4E group in z-plane" % (self, "".join(pre_steps)))
                #else:
                #    log.info("%s: L4E group in z-plane, moving to x-plane" % self)
                self.rotate("x")
                break
        else:
            raise SolveError("Could not stage L4E in x-plane")

        #log.info("%s: final four edges placed in x-plane, %d steps in" % (self, self.get_solution_len_minus_rotates(self.solution)))

    def pair_x_plane_edges_in_l4e(self):

        if not self.x_plane_edges_are_l4e():
            raise SolveError("There must be a L4E group of edges in the x-plane")

        if self.x_plane_edges_paired():
            log.info("%s: x-plane edges already paired, %d steps in" % (self, self.get_solution_len_minus_rotates(self.solution)))
            return

        original_state = self.state[:]
        original_solution = self.solution[:]
        original_solution_len = len(self.solution)
        original_paired_edges_count = self.get_paired_edges_count()

        # The 4 paired edges are in the x-plane
        only_colors = []
        for square_index in (36, 40, 86, 90):
            partner_index = edges_partner_555[square_index]
            square_value = self.state[square_index]
            partner_value = self.state[partner_index]
            wing_str = wing_str_map[square_value + partner_value]
            only_colors.append(wing_str)

        # Old way where we would IDA
        '''
        self.lt_edges_x_plane_edges_only.only_colors = only_colors
        self.lt_edges_x_plane.only_colors = only_colors

        # Recolor the centers in the x-plane to LFRB since LFRB was used to build our tables
        centers_recolor = {
            self.state[38] : "L",
            self.state[63] : "F",
            self.state[88] : "R",
            self.state[113] : "B",
        }

        for x in LFRB_centers_555:
            self.state[x] = centers_recolor[self.state[x]]

        # Recolor the edges to they are all oriented using their original orientation.
        # We do this because our tables were built with all edges at their original orientation.
        self.edges_flip_to_original_orientation()

        # Now we can solve
        self.lt_edges_x_plane.solve()
        '''

        # Recolor the edges to they are all oriented using their original orientation.
        # We do this because our tables were built with all edges at their original orientation.
        self.edges_flip_to_original_orientation()

        # Now we can solve
        self.lt_edges_x_plane_centers_solved.only_colors = only_colors
        self.lt_edges_x_plane_centers_solved.solve()

        # Put the cube back the way it was (to undo all of the recoloring we did) and apply the solution
        l4e_solution = self.solution[original_solution_len:]
        self.state = original_state[:]
        self.solution = original_solution[:]

        for step in l4e_solution:
            self.rotate(step)

        #self.print_cube()
        assert self.x_plane_edges_paired(), "4-edges in x-plane should have paired"
        self.solution.append("COMMENT_%d_steps_555_L4E_paired" % self.get_solution_len_minus_rotates(self.solution[original_solution_len:]))
        log.info("%s: x-plane edges paired in %d steps, %d steps in" % (self, len(l4e_solution), self.get_solution_len_minus_rotates(self.solution)))

    def pair_all_three_l4e(self):

        # Remember what things looked like
        original_state = self.state[:]
        original_solution = self.solution[:]
        original_solution_len = len(self.solution)

        min_solution_len = None
        min_solution_steps = None

        # The three edges can be paired in one of 6 orders:
        for opening_rotations in (
            "x y z",
            "x z y",
            "y x z",
            "y z x",
            "z x y",
            "z y x",
            ):

            if opening_rotations == "x y z":
                self.pair_x_plane_edges_in_l4e()
                self.rotate("z")
                self.pair_x_plane_edges_in_l4e()
                self.rotate("x")
                self.pair_x_plane_edges_in_l4e()

            elif opening_rotations == "x z y":
                self.pair_x_plane_edges_in_l4e()
                self.rotate("x")
                self.pair_x_plane_edges_in_l4e()
                self.rotate("z")
                self.pair_x_plane_edges_in_l4e()

            elif opening_rotations == "y x z":
                self.rotate("z")
                self.pair_x_plane_edges_in_l4e()
                self.rotate("z'")
                self.pair_x_plane_edges_in_l4e()
                self.rotate("x")
                self.pair_x_plane_edges_in_l4e()

            elif opening_rotations == "y z x":
                self.rotate("z")
                self.pair_x_plane_edges_in_l4e()
                self.rotate("x"),
                self.pair_x_plane_edges_in_l4e()
                self.rotate("z")
                self.pair_x_plane_edges_in_l4e()

            elif opening_rotations == "z x y":
                self.rotate("x")
                self.pair_x_plane_edges_in_l4e()
                self.rotate("x'"),
                self.pair_x_plane_edges_in_l4e()
                self.rotate("z")
                self.pair_x_plane_edges_in_l4e()

            elif opening_rotations == "z y x":
                self.rotate("x")
                self.pair_x_plane_edges_in_l4e()
                self.rotate("z"),
                self.pair_x_plane_edges_in_l4e()
                self.rotate("x")
                self.pair_x_plane_edges_in_l4e()

            else:
                raise Exception("Add support for {}".format(opening_rotations))

            solution_len = self.get_solution_len_minus_rotates(self.solution[original_solution_len:])

            if min_solution_len is None or solution_len < min_solution_len:
                min_state = self.state[:]
                min_solution = self.solution[:]
                min_solution_len = solution_len
                log.info("{}: opening_rotations {}, solution len {} (NEW MIN)\n".format(self, opening_rotations, min_solution_len))
            else:
                log.info("{}: opening_rotations {}, solution len {}\n".format(self, opening_rotations, solution_len))

            self.state = original_state[:]
            self.solution = original_solution[:]

        self.state = min_state[:]
        self.solution = min_solution[:]
        assert self.edges_paired()

    def reduce_333(self):
        """
        This is used to pair the inside orbit of edges for 7x7x7
        """
        self.lt_init()

        if not self.centers_staged():
            self.group_centers_stage_UD()
            self.group_centers_stage_LR()

        if not self.centers_solved():
            tmp_solution_len = len(self.solution)
            self.lt_ULFRBD_centers_solve.solve()
            self.print_cube()
            self.solution.append("COMMENT_%d_steps_555_centers_solved" % self.get_solution_len_minus_rotates(self.solution[tmp_solution_len:]))
            log.info("%s: centers solved, %d steps in" % (self, self.get_solution_len_minus_rotates(self.solution)))

        log.info("%s: kociemba %s" % (self, self.get_kociemba_string(True)))
        self.solution.append('CENTERS_SOLVED')

        if not self.edges_paired():

            # 10 cubes, starting at 0 pre-step, took 20s, avg edges is 43.5, avg overall was 96.4
            # 10 cubes, starting at 1 pre-step, took 50s, avg edges is 42.4, avg overall was 95.6
            # The name of the game here is speed so start with 0
            for x in range(3):
                try:
                    self.stage_first_six_edges_555(x)
                    break
                except HorseShoeSolveError:
                    continue
            else:
                raise HorseShoeSolveError("Could not pair horseshoe edges")

            self.pair_first_six_edges_555(True)
            tmp_solution_len = len(self.solution)

            if not self.edges_paired():
                self.rotate("z")
                self.rotate("D2")
                self.rotate("R2")
                #self.rotate("U2")
                #self.rotate("L2")

            horseshoe_len = self.get_solution_len_minus_rotates(self.solution[tmp_solution_len:])

            if horseshoe_len:
                self.solution.append("COMMENT_%d_steps_555_horseshoe_staged" % horseshoe_len)

            self.print_cube()

            if not self.edges_paired():
                self.pair_first_six_edges_555(True)

            '''
            self.stage_first_four_edges_555()
            self.stage_second_four_edges_555()
            self.pair_all_three_l4e()
            self.print_cube()
            '''

        self.solution.append('EDGES_GROUPED')
