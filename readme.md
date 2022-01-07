# Shepherding Program

Public Shepherding Program for Multiple Steering Agents

# Usage

Use this command for usage help .

```bash
python3 main.py -h
```

## Run

You can set parameter of similation using config files.

For instance, use this command to run the program by a default config.

```bash
python3 main.py -p "config/default.json"
```

## Config File

You can make own config files.

An example is here.

``` json:config/default.json
{
    "shepherd_model": "farthest",
    "process_number": 40,
    "trial_number": 5,
    "n_iter": 3000,
    "goal": [50,50],
    "goal_radius": 20,
    "sheep_number": [50,50],
    "shepherd_number": [1,5],
    "sheep_initial_pos_base":[0,0],
    "sheep_initial_pos_radius": 80,
    "shepherd_initial_pos_base": [-50,-50],
    "shepherd_initial_pos_radius": 60,
    "shepherd_initial_pos_vacuum": 40,
    "shepherd_initial_direction": "bottom_left",
    "sheep_param": [100,0.5,2,400],
    "shepherd_param": [2.5,100,1,2]
}
```

## Acknowledgements

We developed this program from labmate Mr. Himo.

We will release the core algorithm and graph analysis sooner with a paper.
## License

"Public Shepherding Program" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).