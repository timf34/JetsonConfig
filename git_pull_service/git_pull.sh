#!/bin/bash

USER_NAME="fov"

# the function to check the internet connection
function check_internet() {
    wget -q --spider https://google.com

    if [ $? -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# the function to pull the FOVCamerasWebApp git repo
function git_pull() {
    cd /home/$USER_NAME/Desktop/FOVCamerasWebApp
    git stash
    git pull
}

# the function to pull the JetsonConfig git repo
function git_pull_jwm() {
    cd /home/$USER_NAME/Desktop/JetsonConfig
    git stash
    git pull
}

# check for internet connection once after boot
check_internet
while [ $? -ne 0 ]; do
    sleep 10
    check_internet
done

# Pull when device is initially connected to the internet
git_pull
git_pull_jwm

# check for updates every 1 hour
while true; do
    check_internet
    if [ $? -eq 0 ]; then
        git_pull
        git_pull_jwm
    fi
    sleep 3600
done
