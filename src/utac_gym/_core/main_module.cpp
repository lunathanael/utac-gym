#include <nanobind/nanobind.h>

namespace nb = nanobind;

void bind_types(nb::module_ &m);
void bind_gamestate(nb::module_ &m);
void bind_score(nb::module_ &m);
void bind_hand(nb::module_ &m);

NB_MODULE(_core, m) {
    bind_types(m);
    bind_gamestate(m);
    bind_score(m);
    bind_hand(m);
}