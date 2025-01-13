#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>

#include "utac/src/state.hpp"

namespace nb = nanobind;
using namespace nb::literals;

void bind_state(nb::module_ &m) {
    nb::class_<State>(m, "State")
        .def(nb::init<>())
        .def("make_move", &State::make_move)
        .def("get_obs", &State::get_obs)
        .def("get_valid_moves", &State::get_valid_moves)
        .def("get_valid_mask", &State::get_valid_mask)
        .def("is_terminal", &State::is_terminal)
        .def("terminal_value", &State::terminal_value)
        .def("print", &State::print);
}