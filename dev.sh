#!/bin/bash

function heroku_commands() {
    case $1 in
        "push")
            git push heroku master
            ;;
    esac
}

function git_push() {
    git commit -m $@
    git push
}

case $1 in
    "heroku")
        heroku_commands "${@:2}"
        ;;
    "push")
        git_push "${@:2}"
        ;;
esac

