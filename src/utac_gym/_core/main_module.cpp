#include <nanobind/nanobind.h>

namespace nb = nanobind;

void bind_state(nb::module_ &m);

NB_MODULE(_core, m) {
    bind_state(m);
}