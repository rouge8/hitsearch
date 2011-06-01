# A `HITS`-based search engine

Google uses PageRank.  HITS is just like PageRank, except it figures out how to automatically deal with spider-traps AND deadends.  Way cool.

This engine is based off the Django framework.  Fortunately we've included the exact version you need in with the repository so you don't need to download it on your own.  Is that violating some copyright laws? Let's hope not.

# How to Run

1. Unpack the dependencies by running `./setup-dependencies.sh`.
2. To run the development server and host it locally for testing. `python hitsearch/manage.py runserver` to launch the server!
3. Go to `http://localhost:8000/`  You'll see some stuff!
4. Cool, now run `python hitsearch/manage.py syncdb` to setup the database stuff

# Cleanup

1. Dependencies can be removed with `remove-dependencies.sh`.
