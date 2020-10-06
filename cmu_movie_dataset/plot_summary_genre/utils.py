import csv
import json

def read_plot_summaries(path_to_plot_summaries):
	"""Reads plot_summaries.txt.

	# Arguments:
		path_to_plot_summaries: str, location of plot_summaries.txt.

	# Returns:
		wiki_movie_ids: list of strings, list of all the movie ids.
		plot_summaries_dict: dict, dictionary that maps movie ids to 
			plot summaries.
	"""
	
	wiki_movie_ids = []
	plot_summaries_dict = {}

	with open(path_to_plot_summaries, 'r') as file:
		reader = csv.reader(file, delimiter='\t')
		for wiki_movie_id, plot_summary in reader:
			wiki_movie_ids.append(wiki_movie_id)
			plot_summaries_dict[wiki_movie_id] = plot_summary

	return wiki_movie_ids, plot_summaries_dict

def read_movie_genre(path_to_movie_metadata):
	"""Reads movie genres from movie.metadata.tsv

	# Arguments:
		path_to_movie_metadata: str, location of movie.metadata.tsv

	# Returns:
		genre_dict: dict, dictionary that maps wiki movie ids
			to movie genres
	"""
	genre_dict = {}
	all_genres = set()

	with open(path_to_movie_metadata, 'r') as file:
		reader = csv.reader(file, delimiter='\t')
		for row in reader:
			wiki_movie_id = row[0]

			genre = json.loads(row[-1])
			genre_values = list(genre.values())

			for genre_value in genre_values:
				if genre_value not in all_genres:
					all_genres.add(genre_value)

			genre_dict[wiki_movie_id] = genre_values


	return genre_dict, sorted(all_genres)
			



if __name__ == "__main__":
	movie_ids, plot_summaries_dict = read_plot_summaries('../../MovieSummaries/plot_summaries.txt')

	genre_dict, all_genres = read_movie_genre('../../MovieSummaries/movie.metadata.tsv')

	# not_found = []

	# for movie_id in movie_ids:
	# 	try:
	# 		{
	# 			'Plot':plot_summaries_dict[movie_id],
	# 			'Genre':genre_dict[movie_id]
	# 			}
	# 	except Exception as e:
	# 		not_found.append(e)

	# print(not_found, len(not_found))



