import numpy as np
from scipy import ndimage as ndi
from tqdm import tqdm
from skimage.transform import resize

from steps.base import BaseTransformer


class BuildingLabeler(BaseTransformer):
    def transform(self, images):
        labeled_images = []
        for i, image in enumerate(images):
            labeled_image = label(image)
            labeled_images.append(labeled_image)
        return {'labeled_images': labeled_images}


class Resizer(BaseTransformer):
    def transform(self, images, target_sizes):
        resized_images = []
        for image, target_size in tqdm(zip(images, target_sizes)):
            n_channels = image.shape[0]
            resized_image = resize(image, [n_channels, ] + target_size, mode='constant')
            resized_images.append(resized_image)
        return {'resized_images': resized_images}


class CategoryAssigner(BaseTransformer):
    def transform(self, images):
        categorized_images = []
        for image in tqdm(images):
            categorized_images.append(categorize_image(image))
        return {'categorized_images': categorized_images}


def label(mask):
    labeled, nr_true = ndi.label(mask)
    return labeled


def label_multichannel_image(mask):
    labeled_channels = []
    for channel in mask:
        labeled_channels.append(label(channel))
    labeled_image = np.stack(labeled_channels)
    return labeled_image


def label(mask):
    labeled, nr_true = ndi.label(mask)
    return labeled


def categorize_image(image):
    return np.argmax(image, axis=0)
