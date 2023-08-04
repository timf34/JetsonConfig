# JetsonConfig

This repo contains scripts for setting up the Jetsons initially. 

`initial_jetson_setup.sh`

- Downloads packages and clones repos needed for the Jetson

`set_env_vars.sh`
- Sets environment variables. **Note that we need to manually write these for each Jetson rn**


`requirements.txt`
- General pip requirements for the Jetson

### Running 

`set_env_vars.sh`
- Be sure to change the variables!
- Note that this script needs sudo priviledges!
Run the following to run this script:
```bash
chmod +x set_env_vars.sh
./set_env_var.sh
```
