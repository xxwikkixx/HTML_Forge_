from __future__ import absolute_import, division, print_function

import pathlib
import random

import tensorflow as tf
import matplotlib.pyplot as plt
from keras.engine.saving import save_model

debug = True
tf.enable_eager_execution()
print(tf.VERSION)
data_root = pathlib.Path("dataset/")
all_image_paths = list()


def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize_images(image, [192, 192])
    image /= 255.0  # normalize to [0,1] range
    return image


def load_and_preprocess_image(path):
    image = tf.read_file(path)
    return preprocess_image(image)


if debug:
    print("==============================================")
    print("Output all folders: ")
    for item in data_root.iterdir():
        print("------->", item)
        print("|")
    print("==============================================")

# String Builder for all image paths
all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]
# Shuufle before all image paths
random.shuffle(all_image_paths)

image_count = len(all_image_paths)
if debug: print("TOTAL IMAGES:", image_count)

# Relate Training Tag that defined in the Tag.txt File
attributions = (data_root / "Tags.txt").read_text(encoding="utf8").splitlines()[4:]
attributions = [line.split(' ,') for line in attributions]
attributions = dict(attributions)

print("This is all the files relate to the  Tag:\n", attributions)

# NOTE!!!! Make sure you cd into dataset dir, and run this command in your terminal:
# Delete github hidden file
# find . -name '.DS_Store' -type f -delete

label_names = sorted(item.name for item in data_root.glob('*/') if (item.is_dir() and item != ".DS_Store"))
print(label_names)
label_to_index = dict((name, index) for index, name in enumerate(label_names))
print(label_to_index)

all_image_labels = [label_to_index[pathlib.Path(path).parent.name]
                    for path in all_image_paths]

print("First 10 labels indices: ", all_image_labels[:10])

img_path = all_image_paths[0]
print(img_path)

img_raw = tf.read_file(img_path)
print(repr(img_raw)[:100] + "...")

img_tensor = tf.image.decode_image(img_raw)

print(img_tensor.shape)
print(img_tensor.dtype)

img_final = tf.image.resize_images(img_tensor, [192, 192])
img_final = img_final / 255.0
print(img_final.shape)
print(img_final.numpy().min())
print(img_final.numpy().max())

image_path = all_image_paths[0]
label = all_image_labels[0]


def caption_image(image_path):
    image_rel = pathlib.Path(image_path).relative_to(data_root)
    return "Block Image ".join(attributions[str(image_rel)])


plt.imshow(load_and_preprocess_image(img_path))
plt.grid(False)
# plt.xlabel(caption_image(img_path))
plt.title(label_names[label].title())
# plt.show()
path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)

print('shape: ', repr(path_ds.output_shapes))
print('type: ', path_ds.output_types)
print()
print(path_ds)

image_ds = path_ds.map(load_and_preprocess_image)

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 8))
for n, image in enumerate(image_ds.take(4)):
    plt.subplot(2, 2, n + 1)
    plt.imshow(image)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

# types: tf.string
label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))

for label in label_ds.take(10):
    print(label_names[label.numpy()])

image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))

print('image shape: ', image_label_ds.output_shapes[0])
print('label shape: ', image_label_ds.output_shapes[1])
print('types: ', image_label_ds.output_types)
print()
print(image_label_ds)

ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))


# The tuples are unpacked into the positional arguments of the mapped function
def load_and_preprocess_from_path_label(path, label):
    return load_and_preprocess_image(path), label


image_label_ds = ds.map(load_and_preprocess_from_path_label)
print(image_label_ds)

BATCH_SIZE = 32

# Setting a shuffle buffer size as large as the dataset ensures that the data is
# completely shuffled.
ds = image_label_ds.apply(
    tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = ds.batch(BATCH_SIZE)
# ds = ds.prefetch(buffer_size=AUTOTUNE)
print(ds)

print("This is mobile net")


def change_range(image, label):
    return 2 * image - 1, label


print(all_image_paths)
print(all_image_labels)

# mobile_net = tf.keras.applications.mobilenet(input_shape=(192, 192, 3), include_top=False)
# mobile_net.trainable = False
#
keras_ds = ds.map(change_range)
image_batch, label_batch = next(iter(keras_ds))

model = tf.keras.Sequential([
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(len(label_names))])

logit_batch = model(image_batch).numpy()

print("min logit:", logit_batch.min())
print("max logit:", logit_batch.max())
# print()
#
print("Shape:", logit_batch.shape)

from keras.models import save_model, load_model

# save_model(model, "temp.h5")
# del model
# saved_model = load_model('my_model.h5', compile=False)
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              compile=False)

# model = models.Sequential()
# model.add(layers.Conv2D(32, (3, 3), activation='relu',input_shape=(150, 150, 3)))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(128, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(128, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Flatten())
# model.add(layers.Dropout(0.5))  #Dropout for regularization
# model.add(layers.Dense(512, activation='relu'))
# model.add(layers.Dense(1, activation='sigmoid'))  #Sigmoid function at the end because we have just two classes
#
#
# #Lets see our model
# model.summary()


# tf.keras.applications.mobilenet_v2.MobileNetV2(input_shape=(192, 192, 3), include_top=False)
