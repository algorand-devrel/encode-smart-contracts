Simple PyTeal Talk
-------------------------

## Python Requirements

Once you've cloned this repo down, cd to this directory and run

```sh
python -m venv .venv
source .venv/bin/activate
pip install pyteal
```

## Run Demos Against Sandbox Dev Mode

The primary example is main.py in the py folder. You must have sandbox installed and running in dev mode before the example will work.

```sh
cd py
python main.py
```

The goal folder shows a simple teal example and illustrates debugging. It can be executed using

```sh
cd goal
./createsimple.sh
```

The contracts folder contains the simple math example pyteal contract created in the presentation.
It can be compiled using the following commands

```sh
cd contracts
python simplemath.py
```


