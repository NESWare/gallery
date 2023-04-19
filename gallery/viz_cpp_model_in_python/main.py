"""main.py

Defines a Panel dashboard for visualizing the native ParticleModel extension
"""

import holoviews as hv  # for plotting
import numpy as np      # for some data manipulations
import pandas as pd     # for setting up our data
import panel as pn      # for dashboarding
import param as pr      # for a typehint
from holoviews.streams import Pipe        # for continuously streaming data to the plot

from ParticleModel import ParticleSystem  # our C++ model!

def update_model() -> None:
    """Callback that is executed by periodic callback managed by the dashboard.
    
    Update the model by a single step using the time delta. Once updated the
    model data is packed into a dataframe and sent through the pipe.
    """
    model.update(time_delta_slider.value)
    particle_data = pd.DataFrame([[particle.x, particle.y] for particle in model.particles], columns=['x','y'])
    entity_pipe.send(particle_data)

def visualize_model(data: pd.DataFrame) -> hv.Points:
    """Callback that is executed whenever data is streamed through the pipe.

    From the model state (as sent from update_model) a scatter plot is created,
    plotting the x-position against the y-position, giving a bird's-eye view of
    the simulation.

    We also set the dimensions of the plot and the dimensions of the data, as
    well as enable the grid.

    Arguments:
        data: single state of the simulation

    Returns:
        HoloViews Points element; a scatter plot of the model state
    """
    return hv.Points(data, kdims=['x', 'y']).opts(
        height=640,
        width=640,
        xlim=(-bounds_slider.value, bounds_slider.value),
        ylim=(-bounds_slider.value, bounds_slider.value),
        show_grid=True
    )

def play(event: pr.parameterized.Event) -> None:
    """Callback to play the simulation.

    Configures a periodic callback to execute our update_model callback
    approximately 30 frames-per-second. If the callback is already scheduled
    then disable it. Also changes the button name to indicate the state.

    Arguments:
        event: the click event that triggered the callback
    """
    global periodic_callback
    if periodic_callback is None or not periodic_callback.running:
        play_button.name = 'Stop'
        # set the periodic to call our run_model callback at 30 frames per second
        periodic_callback = pn.state.add_periodic_callback(update_model, period=1000//30)
    elif periodic_callback.running:
        play_button.name = 'Play'
        periodic_callback.stop()

def reset(event: pr.parameterized.Event | None) -> None:
    """Callback to reset the simulation.

    Stops periodic callback if active; remove the period callback, recreate the
    model, and stream the initial model state through the pipe.

    Arguments:
        event: the click event (or None when initialized) that triggered the
        callback
    """
    global model, periodic_callback
    if periodic_callback is not None and periodic_callback.running:
        play_button.name = 'Play'
        periodic_callback.stop()
    periodic_callback = None
    model = ParticleSystem(num_particles_slider.value, bounds_slider.value)
    for particle in model.particles:
        r = np.hypot(particle.x, particle.y)
        if r > 1.0e-8:
            particle.vx = -particle.y / r
            particle.vy = particle.x / r
    particle_data = pd.DataFrame([[particle.x, particle.y] for particle in model.particles], columns=['x','y'])
    entity_pipe.send(particle_data)

# create a global for the model
model = None

# we use a pipe so that we can stream data from an asynchronous periodic callback
entity_pipe = Pipe(data=[])

# create a global periodic callback - with it being global and persisted we can
# start and stop it at will
periodic_callback = None

# play button, with the play callback attached to the on-click event of the button 
play_button = pn.widgets.Button(name='Play')
play_button.on_click(play)

# reset button, with the reset callback attached to the on-click event of the button 
reset_button = pn.widgets.Button(name='Reset')
reset_button.on_click(reset)

# input sliders for various options
num_particles_slider = pn.widgets.FloatSlider(name='Number of Particles', start=1, end=1000, step=1, value=100)
bounds_slider = pn.widgets.FloatSlider(name='Bounds', start=25, end=2500, value=100, step=25)
time_delta_slider = pn.widgets.FloatSlider(name='Time Delta (s)', start=0.1, end=1.0, value=0.1, step=0.1)

# upon loading the dashboard, reset the model and view
pn.state.onload(lambda: reset(None))

# assemble everything in one of the built-in templates
pn.template.MaterialTemplate(
    site="Particle Model ",
    main=[
        # this is important! the DynamicMap ties the plotting callback to the pipe!
        hv.DynamicMap(visualize_model, streams=[entity_pipe]).opts(framewise=True)
    ],
    sidebar=[
        num_particles_slider,
        bounds_slider,
        time_delta_slider,
        play_button,
        reset_button
    ]
).servable() # set the template as servable so that we can... serve it!