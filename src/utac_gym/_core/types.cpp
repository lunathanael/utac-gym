#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>

#include "utac/src/types.hpp"

namespace nb = nanobind;

void bind_types(nb::module_ &m) {
    nb::class_<GAMESTATE>(m, "GameState")
        .def_rw("occ", &GAMESTATE::occ)
        .def_rw("board", &GAMESTATE::board)
        .def_rw("game_occ", &GAMESTATE::game_occ)
        .def_rw("main_occ", &GAMESTATE::main_occ)
        .def_rw("main_board", &GAMESTATE::main_board)
        .def_rw("side", &GAMESTATE::side)
        .def_rw("last_square", &GAMESTATE::last_square);
}
