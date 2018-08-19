
#ifndef _IDA_SEARCH_666_H
#define _IDA_SEARCH_666_H

#define NUM_OBLIQUE_EDGES_666 48
#define NUM_LEFT_OBLIQUE_EDGES_666 24
#define NUM_RIGHT_OBLIQUE_EDGES_666 24

#define NUM_LFRB_INNER_X_CENTERS_666 16
#define NUM_LFRB_INNER_X_CENTERS_AND_OBLIQUE_EDGES_666 48

unsigned long get_UD_oblique_edges_stage_666(char *cube);
unsigned long ida_heuristic_UD_oblique_edges_stage_666(char *cube);
int ida_search_complete_UD_oblique_edges_stage_666(char *cube);

unsigned long get_LR_inner_x_centers_and_oblique_edges_stage(char *cube);
unsigned long ida_heuristic_LR_inner_x_centers_and_oblique_edges_stage_666(char *cube, struct key_value_pair **LR_inner_x_centers_and_oblique_edges_666, char *LR_inner_x_centers_cost_666);
int ida_search_complete_LR_inner_x_centers_and_oblique_edges_stage(char *cube);

#endif /* _IDA_SEARCH_666_H */
