// particle_system.h
#pragma once

#include <random>
#include <vector>
#include "particle.h"

struct ParticleSystem {
    ParticleSystem(const int num_particles, const double bounds, const int seed=1337) {
        std::mt19937 eng(seed);
        std::uniform_real_distribution<double> dis(-bounds, bounds);
        particles.reserve(num_particles);
        for (auto i = 0; i < num_particles-1; ++i) {
            particles.emplace_back(dis(eng), dis(eng));
        }
        particles.emplace_back(0, 0, 0, 0, 0, 0, 1e12);
    }

    void update(const double time_delta) {
        for (auto &p1 : particles) {
            for (const auto &p2 : particles) {
                if (&p1 == &p2) continue;
                p1.add_force(p2);
            }
        }
        for (auto &p1 : particles) {
            p1.integrate(time_delta);
        }
    }

    std::vector<Particle> particles;
};