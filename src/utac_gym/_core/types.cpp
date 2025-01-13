#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>

#include "utac/src/types.hpp"

namespace nb = nanobind;

void bind_types(nb::module_ &m) {
    nb::class_<GAMESTATE>(m, "GameState")
        .def_readwrite("occ", &GAMESTATE::occ)
        .def_readwrite("board", &GAMESTATE::board)
        .def_readwrite("game_occ", &GAMESTATE::game_occ)
        .def_readwrite("main_occ", &GAMESTATE::main_occ)
        .def_readwrite("main_board", &GAMESTATE::main_board)
        .def_readwrite("side", &GAMESTATE::side)
        .def_readwrite("last_square", &GAMESTATE::last_square);
}
