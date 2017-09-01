test:
	python3 -m unittest tests.test_core
upload:
	# python3 -c "import pickle; pickle.dump({}, open('banditvis/user_defaults.pkl', 'wb'))"
	# add tests here in the future
	-/usr/local/bin/python3 setup.py register sdist upload
	# python3 -c "import pickle; pickle.dump({'out':'Output', 'data':'Data'}, open('banditvis/user_defaults.pkl', 'wb'))"


