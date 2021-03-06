environments
============

A collection of environements compatible with the [`learners`](https://github.com/humm/learners) and [`explorers`](https://github.com/humm/explorers) package.

This code was designed and written to conduct scientific experiments. It is probably not fit for any other purpose, and certainly not for production environments. In particular, its maintenance and development depend on the direction of future research. That being said, do not hesitate to submit issues or contact me by mail for questions and comments.

## Open Science License

This software is placed under the [OpenScience license](http://fabien.benureau.com/openscience.html), which includes all provisions of the LGPL, with the additional condition that if you publish scientific results using this code, you have to publish the corresponding modifications of the code.

> If you publicly release any scientific claims or data that were supported or generated by the Program or a modification thereof, in whole or in part, you will release any modifications you made to the Program. This License will be in effect for the modified program.

## Install

```python
pip install environemnts
```

The [`bokeh`](http://bokeh.pydata.org/) plotting library and the [`pygame`](http://www.pygame.org/) library are needed for running some examples

## Design Overview

This overview is available as an jupyter notebook and python script in the `examples/` folder.
The `environments` module expose two classes: `Channel` and `Environment`.

### Channels

```python
from environments import Channel, Environment
```

A `Channel` describes a scalar communication channel. It has a name, and,
optionnally, bounds, that describe - but don't enforce - maximum and minimum on
the value the scalar described can take.

```python
ch_x = Channel('x', bounds=(0, 10))
ch_y = Channel('y', bounds=(5, 15))
ch_a = Channel('a', bounds=(5, 25))
```

Lists of channels describe signals. For instance, if we consider `ch_x` and
`ch_y` to be motor channels, and `ch_a` a sensory channels, we can create motor
and sensory signals:

```python
m_channels = [ch_x, ch_y]
s_channels = [ch_a]

# a motor signal
{'x': 4, 'y': 11}
# a sensory signal
{'a': 15}
```

### Environments

An `Environment` instance possesses two attributes, `m_channels` and
`s_channels` describing its motor and sensory channels respectively, and a
method `execute`, that receives a motor signal and returns environmental
feedback. The environmental feedback contains the executed motor_signal, the
resulting sensory signal, and an uuid - an unique identifier.

```python
# an environmental feedback, also called 'observation'.
{'m_signal': {'x': 4, 'y': 11},
 's_signal': {'a': 15},
 'uuid'    : 0}
```


To inherit from `Environment`, one only needs to override the method
`_execute`, that expects to receive a motor signal and return a sensory
signal. This method is called by `Environment.execute`, that automatically
assign an uuid to the feedback using the standart library `uuid` module. Let's
create a simple environment.

```python
class Sum(Environment):
    """Compute the sum of its motor signal"""

    def __init__(self, cfg):
        """Declare `m_channels` and `s_channels`"""
        super(Sum, self).__init__(cfg)
        self.m_channels = [ch_x, ch_y]
        self.s_channels = [ch_a]

    def _execute(self, m_signal, meta=None):
        """Return a sensory signal"""
        return {'a': m_signal['x'] + m_signal['y']}
```

We can now execute motor commands on the environment.

```python
sum_env = Sum({})

sum_env.execute({'x': 2, 'y': 11})
```

Output:
```
{'m_signal': {'x': 2, 'y': 11},
 's_signal': {'a': 13},
 'uuid': UUID('d70e8c88-ebea-4c86-8568-c03b4e182477')}
```


### Details

#### `__init__()`'s `cfg` parameter
The ``__init__()`` method of an environment expects a `cfg` argument, which
provides configuration parameters to the environment. If you call
`Environment.__init__()`, it expects `cfg` to be a dictionnary or a
`scicfg.SciConfig` instance. In the former case, it will be converted to a
`scicfg.SciConfig` instance and set as the `self.cfg`.

#### `_execute`'s `meta` parameter
The `_execute` command accepts an additional argument, `meta`. If not `None`, it
is assumed to be dictionnary, that can be both use for providing additional
information on how to execute the command, or by the execution add logs and
metadata about how the motor command was executed.

#### `close()` method
Any cleanup needed stopping the environement should be done in the `close()`
method. The best way to create an environment and execute orders is to use a
`try: ... finally:` construction, so that any error or exception still cleans-up
open ports, connections, stops motors, etc.:

```python
    try:
        sum_env = Sum({})
        sum_env.execute({'x': 2, 'y': 11})
    finally:
        sum_env.close()
```
