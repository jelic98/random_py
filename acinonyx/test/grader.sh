#!/bin/bash
wd=$(pwd) && cd $1
for i in `find . ! -path . -type d | sort`; do
    rm -f "$i/gen" "$i/src" "$i/src.o" && ok=true
    fpc "$i/src.pas" &> /dev/null
    make "$i/gen" &> /dev/null
    for j in {1..5}; do
        t="$i/$j" src=$("$i/src" <"$t.in") gen=$("$i/gen" <"$t.in") out=$(<"$t.out")
        if [ "$src" != "$out" ] || [ "$gen" != "$out" ]; then
            printf "$t\tERROR\n\nIN\n$(<"$t.in")\n\nSRC\n$src\n\nGEN\n$gen\n\nOUT\n$out\n"
            ok=false && break
        fi
    done
    $ok && printf "$i\tOK\n"
done
cd $wd
