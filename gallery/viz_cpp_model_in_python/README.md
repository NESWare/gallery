# viz-cpp-model-in-python

First install the dependecies in `requirements.txt` into a Python environment. 

Build the C++ model into a Python extension with:

```shell
g++-12 -std=c++20 -O3 -shared -fPIC $(python3 -m pybind11 --includes) particle_model.cpp -o ParticleModel$(python3-config --extension-suffix)
```

Then serve the dashboard with:

```shell
panel serve main.py
```
