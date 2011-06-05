# A `HITS`-based search engine

Google uses PageRank.  HITS is just like PageRank, except it figures out how to automatically deal with spider-traps AND deadends.  Way cool.

This engine is based off the Django framework.  Fortunately we've included the exact version you need in with the repository so you don't need to download it on your own.  Is that violating some copyright laws? Let's hope not.

# How to Use

Go to the `hitsearch` directory in your terminal and run `./install`.  This will setup all the dependencies and setup the database.  Also,you will be asked to create an administrator account for the database.

Now you can run the server with the command `./runserver`, or populate the database with pages by running `./crawl <url>`.


# Cleanup

1. Dependencies can be removed with `remove-dependencies.sh`.
