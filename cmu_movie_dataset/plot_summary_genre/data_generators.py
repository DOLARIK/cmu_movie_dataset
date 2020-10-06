from tensorflow.keras.utils import Sequence
import os

from utils import (read_plot_summaries, 
				   read_movie_genre,
				   combine_plot_summaries_and_genres,
				   clean_plot_summary)

class BaseDataGenerator(Sequence):
	def __init__(self,
				 movie_ids
				 plot_summary_genre_dict,
				 tokenizer = None,
				 batch_size = 32,
				 shuffle = True,
				 max_length = 128,
				 padding = 'max_length',
				 truncation = True,
				 custom_transform = None,
				 target_encoder = None,
				 validation_split = 0,
				 seed = None,
				 ):
		
		self.movie_ids = movie_ids
		self.plot_summary_genre_dict = plot_summary_genre_dict

		self.batch_size = batch_size
		self.shuffle = shuffle

		self.validation_split = validation_split
		self.seed = seed

		self.custom_transform = custom_transform
		self.target_encoder = target_encoder
		
		self.max_length = max_length
		self.padding = padding
		self.truncation = truncation

		self.tokenizer = self.set_tokenizer(tokenizer)

	@classmethod
	def from_directory(cls, path_to_directory, **kwargs):
		path_to_plot_summaries = os.path.join(path_to_directory, 'plot_summaries.txt')
		path_to_movie_metadata = os.path.join(path_to_directory, 'movie.metadata.tsv')

		wiki_movie_ids, plot_summaries_dict = read_plot_summaries(path_to_plot_summaries)
		movie_genres_dict = read_movie_genre(path_to_movie_metadata)

		plot_summaries_genres_dict = combine_plot_summaries_and_genres(wiki_movie_ids, 
																plot_summaries_dict, movie_genres_dict)

		return cls(wiki_movie_ids, plot_summaries_genres_dict, **kwargs)

	



