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

	return sorted(wiki_movie_ids), plot_summaries_dict

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
			
def combine_plot_summaries_and_genres(wiki_movie_ids, plot_summaries_dict, movie_genres_dict):
	"""Combines plot summaries and respective list of genres into one list.

	# Arguments: 
		wiki_movie_ids: list of strings, list containing wikipedia movie ids.
		plot_summaries_dict: dict, dictionary that maps wiki movie ids to 
			plot summaries.
		movie_genres_dict: dict, dictionary that maps wiki movie ids to 
			genres of that movie

	# Returns:
		plot_summaries_genre_dict: dict, dictionary that maps movie ids to 
			plot and genres

	"""
	plot_summaries_genre_dict = {}

	for movie_id in wiki_movie_ids:
		try:
			plot_summaries_genre_dict[movie_id] =  {
				'plot': plot_summaries_dict[movie_id],
				'genres': movie_genres_dict[movie_id]
			}
		except Exception as e:
			print('WARNING: No movie found with id:', e, 'in movie_genres_dict')

	return plot_summaries_genre_dict



if __name__ == "__main__":
	movie_ids, plot_summaries_dict = read_plot_summaries('../../MovieSummaries/plot_summaries.txt')

	genre_dict, all_genres = read_movie_genre('../../MovieSummaries/movie.metadata.tsv')

	plot_summaries_genre_dict = combine_plot_summaries_and_genres(movie_ids, plot_summaries_dict, genre_dict)

	# print(plot_summaries_genre_dict, len(plot_summaries_genre_dict))

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



