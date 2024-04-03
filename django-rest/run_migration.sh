i=0
migrateRetry=0
# Wait for termination
sleep 5

while [ $i -le 24 ]
do
    status=$(kubectl get pods -l app=leonardoapi -o jsonpath='{.items[0].status.phase}')
    if [ $status != "Running" ]
    then
        echo "Waiting for service up and running ..."
        sleep 5
    else
        echo "BEGIN - Executing migration ..."
        while [ $migrateRetry -le 3 ]
        do
            export FOO=$(kubectl get pod -l app=leonardoapi -o jsonpath="{.items[0].metadata.name}")
            kubectl exec --stdin $FOO -- ash -c 'DJANGO_CONFIGURATION=Production python manage.py migrate' > migration.log
            cat migration.log
            isInFile=$(cat migration.log | grep -c "Running migrations")
            if [ $isInFile -eq 1 ]; then
                #string is in file at least once
                echo "END - Executing migration ..."
                break
            fi
            migrateRetry=$(expr $migrateRetry + 1)
        done
        break
    fi
    i=$(expr $i + 1)
done