for p in prob-*.py ; do
    python $p | tail -n 1 | grep "Complete" > /dev/null
    if [[ "$?" -ne 0 ]]; then
        echo $p "error"
        # exit 1
    else
        echo $p ok
    fi
done
