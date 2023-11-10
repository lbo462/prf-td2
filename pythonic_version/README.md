# PRF - TD2, pythonic version

## Requirements

As for every python project, here is the following set-up that you should have :

- Create a Python virtual environment. See the [doc](https://docs.python.org/fr/3/library/venv.html)
```shell
python -m venv venv
```

- Dive into the environment
```shell
source venv/bin/activate  # Linux
.\venv\Scripts\activate.bat  # Windows
```

- Install the dependencies
```shell
pip install -r requirements.txt
```

## Start script

In the virtual env (`source venv/bin/activate`, see the requirements section)

```shell
python main.py
```

Please, take a great look at every comment in the code.
They are essential in order to understand what's going on and what's this script does.

Start reading the file `main.py` to start.

The models are defined in `models.py`, `buffer.py` defines a buffer 
and `event.py` is a bit more complex and defines an event scheduler that handles
the different events that can occurs when running the simulation.

---

**The users on WSL should probably install the package `python3-tk` 
to display the graphs with matplotlib.**

```shell
sudo apt-get install python3-tk
```