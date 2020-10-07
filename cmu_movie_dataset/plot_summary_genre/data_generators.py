from tensorflow.keras.utils import Sequence
import tensorflow as tf

import os
from abc import abstractmethod

from .utils import (read_plot_summaries, 
				   read_movie_genre,
				   combine_plot_summaries_and_genres,
				   clean_plot_summary, 
				   movie_ids_subset)

from transformers import (BertTokenizer)

import numpy as np

class BaseDataGenerator(Sequence):
	def __init__(self,
				 movie_ids,
				 plot_summary_genre_dict,
				 all_genres,
				 genre_indices,
				 indices_genre,
				 tokenizer = None,
				 batch_size = 32,
				 shuffle = True,
				 max_length = 128,
				 padding = 'max_length',
				 truncation = True,
				 custom_transforms = None,
				 target_encoder = None,
				 validation_split = 0,
				 subset = None,
				 seed = None,
				 ):

		if validation_split > 0:
			subset = 'training' if subset is None else subset

			if subset == 'training':
				split = (0, 1 - validation_split)
			elif subset == 'validation':
				split = (1 - validation_split, 1)

		
		self.movie_ids = movie_ids_subset(movie_ids, split)
		self.plot_summary_genre_dict = plot_summary_genre_dict
		self.all_genres = all_genres

		self.genre_indices = genre_indices
		self.indices_genre = indices_genre

		self.num_samples = len(self.movie_ids)

		self.batch_size = batch_size
		self.shuffle = shuffle

		self.validation_split = validation_split
		self.seed = seed

		self.custom_transforms = custom_transforms
		self.target_encoder = target_encoder

		self.index_array = None
		self.total_batches_seen = 0
		
		self.max_length = max_length
		self.padding = padding
		self.truncation = truncation

		self.tokenizer = self.set_tokenizer()

	@classmethod
	def from_directory(cls, path_to_directory, **kwargs):
		path_to_plot_summaries = os.path.join(path_to_directory, 'plot_summaries.txt')
		path_to_movie_metadata = os.path.join(path_to_directory, 'movie.metadata.tsv')

		wiki_movie_ids, plot_summaries_dict = read_plot_summaries(path_to_plot_summaries)
		movie_genres_dict, all_genres, genre_indices, indices_genre = read_movie_genre(path_to_movie_metadata)

		wiki_movie_ids, plot_summaries_genres_dict = combine_plot_summaries_and_genres(wiki_movie_ids, 
																plot_summaries_dict, movie_genres_dict)

		return cls(wiki_movie_ids, plot_summaries_genres_dict, 
			all_genres, genre_indices, indices_genre, **kwargs)

	def set_index_array(self):
		self.index_array = np.arange(self.num_samples)
		if self.shuffle:
			self.index_array = np.random.permutation(self.num_samples)

	def __len__(self):
		return (self.num_samples + self.batch_size + 1)//self.batch_size

	def __getitem__(self, idx):
		if self.seed is not None:
			np.random.seed(self.seed + self.total_batches_seen)

		self.total_batches_seen += 1

		if self.index_array is None:
			self.set_index_array()

		index_array = self.index_array[self.batch_size*idx : self.batch_size*(idx + 1)]

		return self._get_batches(index_array)

	def _get_batches(self, index_array):
		batch_x, batch_y = self._get_sample_batches(index_array)
		batch_x, batch_y = self._encode_sample_batches(batch_x, batch_y)

		return batch_x, batch_y

	def _get_sample_batches(self, index_array):
		batch_x, batch_y = [], []

		for x, y in self._get_sample_pair(index_array):
			batch_x.append(x)
			batch_y.append(y)

		return batch_x, batch_y

	def _get_sample_pair(self, index):
		for i in index:
			plot_summary = self.plot_summary_genre_dict[self.movie_ids[i]]['plot']
			genres = self.plot_summary_genre_dict[self.movie_ids[i]]['genres']

			if self.custom_transforms:
				for custom_transform in self.custom_transforms:
					plot_summary = custom_transform(plot_summary)
			else:
				plot_summary = clean_plot_summary(plot_summary)

			yield plot_summary, genres

	def _encode_sample_batches(self, batch_x, batch_y):
		batch_x = self._encode_features(batch_x)
		batch_y = self._encode_targets(batch_y)

		return batch_x, batch_y

	@abstractmethod
	def _encode_features(self):
		raise NotImplementedError

	@abstractmethod
	def _encode_targets(self):
		raise NotImplementedError

	@abstractmethod
	def set_tokenizer(self):
		raise NotImplementedError

class BertDataGenerator(BaseDataGenerator):
	def __init__(self, *args, **kwargs):
		super(BertDataGenerator, self).__init__(*args, **kwargs)

	def _encode_features(self, batch_x):
		return dict(self.tokenizer(batch_x, 
								max_length = self.max_length,
								padding = self.padding,
								truncation = self.truncation,
								return_tensors = 'tf'))

	def _encode_targets(self, batch_y):
		if self.target_encoder is not None:
			return self.target_encoder(batch_y)
		else:
			def func_map(target):
				encoded_target = np.zeros(len(self.all_genres))
				for genre in target:
					encoded_target[self.genre_indices[genre]] = 1
				return encoded_target

			return tf.convert_to_tensor(np.asarray(list(map(func_map, batch_y))))

	def set_tokenizer(self):
		return BertTokenizer.from_pretrained('bert-base-uncased')

if __name__ == "__main__":
	train_generator = BertDataGenerator.from_directory('../../MovieSummaries', 
													validation_split = 0.2,
													subset = 'training',
													batch_size = 32)
	for train_batch in train_generator:
		print(train_batch)
		# break

	print(len(train_generator))

	valid_generator = BertDataGenerator.from_directory('../../MovieSummaries', 
													validation_split = 0.2,
													subset = 'validation',
													batch_size = 32)



	for valid_batch in valid_generator:
		print(valid_batch)
		# break

	print(len(valid_generator))





