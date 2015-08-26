#!/bin/bash

function heroku_commands() {
    case $1 in
        "push")
            git push heroku master
            ;;
    esac
}

function git_push() {
    if [[ "${1}_" == "_" ]]; then
        printf "Missing commit message\n"
        exit 1
    fi
    git add .
    git commit -m "$@"
    git push
}

function status() {
    git status
    heroku ps   
}

case $1 in
    "heroku")
        heroku_commands "${@:2}"
        ;;
    "push")
        git_push "${@:2}"
        ;;
    "status")
        status
        ;;
esac

