#!/bin/bash



SB=/Users/jason/sandbox/sandbox/sandbox
GOAL="$SB goal"

accts=(`$GOAL account list | awk '{print $3}'`)
creator=${accts[0]}

app_name=simple.teal
clear_name=clear.teal

$SB copyTo $app_name
$SB copyTo $clear_name 

echo "$app_name"

echo "Creating application"
app_id=`$GOAL app create --creator $creator \
    --approval-prog $app_name \
    --clear-prog $clear_name \
    --global-byteslices 0 \
    --global-ints 0 \
    --local-ints 0 \
    --local-byteslices 0  | grep 'Created app' |awk '{print $6}' | tr -d '\r'`

echo "App ID: $app_id"


$GOAL app method --app-id $app_id \
 --method "add(uint64,uint64)uint64" \
 --arg 1 --arg 1 --from ${accts[1]} --out=dump.dr --dryrun-dump



$SB copyFrom dump.dr
tealdbg debug simple.teal -d dump.dr --remote-debugging-port 9399
