#pragma once

#include <cmath>

constexpr double GRAVITY = 6.6743e-11;  // Newton's Gravitational Constant

struct Particle {
    double x = 0.0;
    double y = 0.0;
    double vx = 0.0;
    double vy = 0.0;
    double ax = 0.0;
    double ay = 0.0;
    double mass = 5.0e6;

    void integrate(const double dt) {
        vx += ax * dt;
        vy += ay * dt;
        x += vx * dt;
        y += vy * dt;
        ax = 0.0;
        ay = 0.0;
    }

    void add_force(const Particle &other) {
        double dx = other.x - x;
        double dy = other.y - y;
        double distance = std::hypot(dx, dy);
        double direction = std::atan2(dy, dx);
        double force = GRAVITY * other.mass / (distance * distance);
        ax += force * std::cos(direction);
        ay += force * std::sin(direction);
    }
};
