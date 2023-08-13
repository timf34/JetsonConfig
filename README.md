# JetsonConfig

This repo contains scripts for setting up the Jetsons initially. 

`initial_jetson_setup.sh`

- Downloads packages and clones repos needed for the Jetson

`set_env_vars.sh`
- Sets environment variables. **Note that we need to manually write these for each Jetson rn**


`requirements.txt`
- General pip requirements for the Jetson

### Running 

**See the `interactive_setup.md` file for stuff that needs to be done before and after running `initial_jetson_setup.sh`**

`set_env_vars.sh`
- Be sure to change the variables!
- Note that this script needs sudo priviledges!
Run the following to run this script:
```bash
chmod +x set_env_vars.sh
./set_env_vars.sh
```

And note that I can run this so I don't have to reboot the Jetson for the env variable to take place:
`export DEVICE_NAME="marvel-fov-2"`


`initial_jetson_setup.sh`:

```
chmod +x initial_jetson_setup.sh
./initial_jetson_setup.sh
```

### Notes 

When I run `initial_jetson_setup.sh` I'll need to input the following:

- Github username and PAT (I should run the github storing thing beforehand so it remembers these)


Note: I'm not sure if pip installing the requirements.txt file is working correctly, so I might need to 
run `pip3 install -r requirements.txt` manually too.