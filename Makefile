freshdesk-data:
	rm -f test.db
	sqlite3 test.db < sql/schema.sql
	python3 ticket_gen.py -n 1000 -o activities.json
	python3 data_insert.py -i activities.json -d test.db
	sqlite3 test.db < sql/update_data.sql
	sqlite3 test.db -header  < sql/ticket_summary.sql
