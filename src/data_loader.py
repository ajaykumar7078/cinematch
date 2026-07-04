"""
Movie data loader - loads and preprocesses the movie dataset.
Uses a built-in sample dataset so the project is self-contained.
"""
import pandas as pd
import io

SAMPLE_MOVIES_CSV = """movieId,title,genres,overview
1,Toy Story,Animation|Children|Comedy,"A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boys bedroom."
2,Jumanji,Adventure|Children|Fantasy,"When two kids find and play a magical board game, they release a man trapped in it for decades and a host of dangers that can only be stopped by finishing the game."
3,Grumpy Old Men,Comedy|Romance,"A lifelong feud between two neighbors since childhood only gets worse when a new female neighbor moves across the street."
4,Waiting to Exhale,Comedy|Drama|Romance,"Based on Terry McMillans novel, this film follows four very different African-American women and their relationships with men."
5,Father of the Bride Part II,Comedy,"Banks is about to become a grandfather and his wife is pregnant at the same time - chaos ensues."
6,Heat,Action|Crime|Thriller,"A group of professional bank robbers start to feel the heat from police when they unknowingly leave a clue at their latest heist."
7,Sabrina,Comedy|Romance,"An ugly duckling having undergone a remarkable change still harbors feelings for her crush - a carefree playboy."
8,Twister,Action|Adventure|Drama,"Two storm chasers on the brink of divorce must work together to create an advanced weather alert system by putting themselves in the cross-hairs of violent tornadoes."
9,The Godfather,Crime|Drama,"The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant youngest son."
10,The Dark Knight,Action|Crime|Drama,"When the menace known as the Joker wreaks havoc on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
11,Inception,Action|Sci-Fi|Thriller,"A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO."
12,Interstellar,Adventure|Drama|Sci-Fi,"When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot is tasked with piloting a spacecraft to find a new planet for humans."
13,Pulp Fiction,Crime|Drama|Thriller,"The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
14,Fight Club,Drama|Thriller,"An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much more."
15,Forrest Gump,Comedy|Drama|Romance,"The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man with an IQ of 75."
16,The Matrix,Action|Sci-Fi,"When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth - the life he knows is the elaborate deception of an evil cyber-intelligence."
17,Goodfellas,Crime|Drama,"The story of Henry Hill and his life in the mob, covering his relationship with his wife and his mob partners Jimmy Conway and Tommy DeVito."
18,The Shawshank Redemption,Drama,"Over the course of several years, two convicts form a friendship, seeking consolation and eventual redemption through basic compassion."
19,The Silence of the Lambs,Crime|Drama|Thriller,"A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer."
20,Schindlers List,Drama|History,"In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution."
21,Parasite,Comedy|Drama|Thriller,"Greed and class discrimination threaten the symbiotic relationship between the wealthy Park family and the destitute Kim clan."
22,Spirited Away,Adventure|Animation|Fantasy,"During her familys move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits where humans are changed into beasts."
23,The Social Network,Drama,"As Harvard student Mark Zuckerberg creates the social networking site that would become Facebook, he is sued by the twins who claim he stole their idea."
24,Whiplash,Drama|Music,"A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a students potential."
25,La La Land,Comedy|Drama|Music|Romance,"While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future."
26,Get Out,Horror|Mystery|Thriller,"A young African-American visits his white girlfriends parents for the weekend, where his uneasiness about their reception of him reaches a boiling point."
27,Mad Max Fury Road,Action|Adventure|Sci-Fi,"In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners and a drifter named Max."
28,Coco,Adventure|Animation|Comedy|Music,"Aspiring musician Miguel, confronted with his familys ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer."
29,Your Name,Animation|Drama|Fantasy|Romance,"Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart?"
30,Joker,Crime|Drama|Thriller,"In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime."
"""

def load_movies():
    """Load the movie dataset from built-in CSV data."""
    df = pd.read_csv(io.StringIO(SAMPLE_MOVIES_CSV))
    df['combined_features'] = df['genres'].str.replace("|", " ") + " " + df['overview']
    return df

def get_movie_by_title(df, title):
    """Find a movie by exact or partial title match."""
    match = df[df['title'].str.lower() == title.lower()]
    if match.empty:
        match = df[df['title'].str.lower().str.contains(title.lower(), na=False)]
    return match.iloc[0] if not match.empty else None

def get_all_titles(df):
    """Return sorted list of all movie titles."""
    return sorted(df['title'].tolist())
