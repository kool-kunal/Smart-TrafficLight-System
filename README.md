# Smart-TrafficLight-System

**Code Overview**

- Master
  - Training.py (main.py)
    - Simulation control &amp; training of genome
    - Training info = training\_config.ini
    - Run()
    - Simulation()
  - Simulator.py
    - Sumo Call(with custom parameters)
    - Evaluation of parameters(like genome count, fitness etc)
    - Traci.start (start sumo window)
  - Reporter.py
    - Reporter = callback functions
  - GENEREATOR.PY
    - TrafficGen\_ke\_liyexml :
    - Xml\_SUMO\_refer\_krega
  - Environment
    - Env.net.xml : xml version of intersection made through SUMO GUI
    - Env.rou.xml : Traffic generator
    - Sumo\_config.sumocfg : integrate the above 2 files
  - Config
    - Trianing params
    - Testing Params
    - NEAT\_hyperparams
  - Test.py
    - Standard\_model &amp; Genetic\_best\_model\_comparison
  - Utils.py
    - Param Loader from config file and convert to python readable dictionary
