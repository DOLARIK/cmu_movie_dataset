import csv

def read_plot_summaries(path_to_plot_summaries):
	"""Reads plot summaries.

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


if __name__ == "__main__":
	movie_ids, plot_summaries_dict = read_plot_summaries('../MovieSummaries/plot_summaries.txt')



