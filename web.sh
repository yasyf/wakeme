if [ "$dev" == "True" ]; then
        python wakeme.py
else
		gunicorn wakeme:app
fi