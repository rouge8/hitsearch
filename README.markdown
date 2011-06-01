# A `HITS`-based search engine

Google uses PageRank.  HITS is just like PageRank, except it figures out how to automatically deal with spider-traps AND deadends.  Way cool.

This engine is based off the Django framework.  Fortunately we've included the exact version you need in with the repository so you don't need to download it on your own.  Is that violating some copyright laws? Let's hope not.

# How to Run

1. Unpack the dependencies by running `./setup-dependencies.sh`.
2. To run the development server and host it locally for testing. `./syncdb` to setup the database
3. `./runserver` to run the development server
4. .. populate your database, run the webcrawler
5. try a test search! 

# Cleanup

1. Dependencies can be removed with `remove-dependencies.sh`.
