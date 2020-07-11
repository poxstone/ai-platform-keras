#!/bin/sh

INTER_SQL="intermediate.sql";

echo "Run mysql query";
#mysql -u "${DB_USER}" -p"${DB_PASSWD}" -h "${DB_HOST}" -D "${DB_DB}" < "query_a.sql" | sed 's/\t/,/g' > "${INTER_SQL}" && \

echo "Run R scripting";
Rscript main.r;

echo "Run upload query";
#mysql -u "${DB_USER_2}" -p"${DB_PASSWD_2}" -h "${DB_HOST_2}" -D "${DB_DB_2}" -e < "${INTER_SQL}";

echo "Finish Script";