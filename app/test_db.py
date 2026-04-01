import games, reviews, users, random


print(games.get_rating(1))
print(games.get_num_ratings(1))
print(games.get_num_ratings("Wii Sports"))
games.add_rating(random.randint(0,100), 1)


#reviews.make_review("Wii Sports is lit yo?.", 1, 1)
print(reviews.get_review(3))
games.add_review(1, 1);
print(games.get_reviews(1))