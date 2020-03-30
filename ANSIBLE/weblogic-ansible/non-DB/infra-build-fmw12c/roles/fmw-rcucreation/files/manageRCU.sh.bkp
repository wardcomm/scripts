#! /bin/bash

# set -x

export JAVA_HOME={{ JAVA_HOME }}

pwf=/tmp/.passwdFile

echo "{{ SYS_PASSWORD }}" > $pwf # sys password
yes "{{ SCHEMA_PASSWORD }}" | head -100 >> $pwf # schema password...as many as needed

SCHEMA_PREFIX=$1

dbArgs=" -databaseType ORACLE -connectString {{ RCU_URL }} -dbUser {{ DB_USER }} -dbRole {{ DB_ROLE }} -schemaPrefix $SCHEMA_PREFIX " 

oArgs="-component MDS -component OPSS -component ESS -component STB -component IAU_APPEND -component IAU_VIEWER -component IAU -component WLS -component UCSUMS -component SOAINFRA -f " # list them all explicitly anyway

echo "Dropping Schemas.."
{{ RCU }} -silent -dropRepository $dbArgs $oArgs < $pwf
rc=$?
echo "Schema drop return code (ignored): [$rc]"

echo "Creating Schemas.."
{{ RCU }} -silent -createRepository -selectDependentsForComponents -useSamePasswordForAllSchemaUsers true $dbArgs $oArgs < $pwf # but still catch dependencies
rc=$?
echo "Schema creation return code: [$rc]"

rm $pwf

exit $rc
