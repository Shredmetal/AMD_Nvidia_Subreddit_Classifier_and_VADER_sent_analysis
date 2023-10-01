import praw
import time
import pandas as pd

# ask the user which subreddit to scrape and how many posts to scrape, use input validation to handle exceptions

validator_1 = False
validator_2 = False

while validator_1 is False or validator_2 is False:
    SUB = input("Which subreddit do you want to scrape (amd/nvidia)? ").lower()
    NO_POSTS = input("How many posts do you want to scrape? ")

    if SUB == "nvidia" or SUB == "amd":
        validator_1 = True
    else:
        print("Invalid subreddit input. Try again.")

    try:
        int(NO_POSTS)
    except ValueError:
        print("Invalid number of posts to scrape. Try again.")
    else:
        validator_2 = True

# Instantiate praw instance to scrape [sensitive information removed, operational version has them as env var]

reddit = praw.Reddit(client_id="",
                     client_secret="",
                     username="",
                     password="!",
                     user_agent="",
                     )

# get the correct subreddit using the user's input

subreddit = reddit.subreddit(SUB)

# get the nubmer of posts using the user's input

new_nv = subreddit.new(limit=int(NO_POSTS))

# use a counter to get progress from the terminal, and count the number of errors

counter = 0
exceptions_handled = 0

# instantiate list for data

data = []

# scraper for loop based on praw documentation

for submission in new_nv:

    # try to place the scraped information in the data list

    try:
        date = submission.created_utc
        if submission.stickied is False:
            submission_text = {
                'title': submission.title,
                'selftext': submission.selftext,
                }

            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comment_text = comment.body.encode("utf-8", errors='ignore').decode("utf-8", errors='ignore')
                comment_data = submission_text.copy()
                comment_data['comment'] = comment_text
                data.append(comment_data)
        counter += 1
        print(counter)

    # if an error is encountered (most likely a rate-limit error which will raise a custom exception with praw)
    # handle the exception and wait a minute before trying again

    except Exception as e:
        exceptions_handled += 1
        time.sleep(60)
        print(f"Exception {e} handled. {exceptions_handled} exceptions handled.")
        pass

# Create a DataFrame
df = pd.DataFrame(data)

# Save the dataframe to a csv file for subsequent access
df.to_csv(f"{SUB}_scrape.csv", index=False)
