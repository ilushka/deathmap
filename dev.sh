#!/bin/bash

set -e

BIN_NAME=$(basename $0)

show_usage() {
    case $1 in
        "heroku")
            printf "Usage: ${BIN_NAME} heroku <"
            cat ${BIN_NAME} | awk 'BEGIN { FS = "\""; ORS = "|"; } /\"[a-z]+\"\) # heroku-arg/ { print $2; }'
            printf ">\n"
            ;;
        *)
            printf "Usage: ${BIN_NAME} <"
            cat ${BIN_NAME} | awk 'BEGIN { FS = "\""; ORS = "|"; } /\"[a-z]+\"\) # first-level-arg/ { print $2; }'
            printf ">\n"
            ;;
    esac
}

show_readme() {
    printf "
## Quick Start
"
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

function start_local() {
    DATABASE_URL="postgresql://deathmap:password@localhost/deathmap" \
        python deathmap.py
}

function heroku_commands() {
    case $1 in
        "push") # heroku-arg;
            git push heroku master
            ;;
        "dbpush") # heroku-arg;
            heroku pg:push postgresql://deathmap:password@localhost/deathmap DATABASE_URL
            ;;
        "dbpull") # heroku-arg;
            heroku pg:pull DATABASE_URL postgresql://deathmap:password@localhost/deathmap
            ;;
    esac
}

case $1 in
    "heroku") # first-level-arg;
        heroku_commands "${@:2}"
        ;;
    "push") # first-level-arg;
        git_push "${@:2}"
        ;;
    "status") # first-level-arg;
        status
        ;;
    "start") # first-level-arg;
        start_local
        ;;
    "help") # first-level-arg;
        show_usage "${@:2}"
        ;;
    "readme") # first-level-arg;
        show_readme
        ;;
    *)
        show_usage
        ;;
esac
