#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;

#include "particle_system.h"

PYBIND11_MODULE(ParticleModel, m) {
    py::class_<ParticleSystem>(m, "ParticleSystem")
        .def(py::init<const int, const double>())
        .def(py::init<const int, const double, const int>())
        .def("update", &ParticleSystem::update)
        .def_readwrite("particles", &ParticleSystem::particles);

    py::class_<Particle>(m, "Particle")
        .def_readwrite("x", &Particle::x)
        .def_readwrite("y", &Particle::y)
        .def_readwrite("vx", &Particle::vx)
        .def_readwrite("vy", &Particle::vy);
}
