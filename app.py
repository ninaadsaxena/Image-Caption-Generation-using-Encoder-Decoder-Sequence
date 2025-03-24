from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Add
import numpy as np
import pickle

app = Flask(__name__)

# Load the InceptionV3 model pre-trained on ImageNet and remove the last layer
model = InceptionV3(weights='imagenet')
model_new = Model(model.input, model.layers[-2].output)

# Function to preprocess the image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.inception_v3.preprocess_input(x)
    return x

# Function to encode the image
def encode_image(img):
    img = preprocess_image(img)
    feature_vector = model_new.predict(img)
    feature_vector = np.reshape(feature_vector, feature_vector.shape[1])
    return feature_vector

# Load the tokenizer
with open("tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)

# Load the word-to-index and index-to-word mappings
with open("word_to_index.pickle", "rb") as handle:
    word_to_index = pickle.load(handle)

with open("index_to_word.pickle", "rb") as handle:
    index_to_word = pickle.load(handle)

# Maximum length of the caption
max_length = 34

# Define the Encoder-Decoder model
def define_model(vocab_size, max_length):
    # Feature extractor model
    inputs1 = tf.keras.Input(shape=(2048,))
    fe1 = Dense(256, activation='relu')(inputs1)
    fe2 = tf.keras.layers.RepeatVector(max_length)(fe1)

    # Sequence model
    inputs2 = tf.keras.Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = LSTM(256, return_sequences=True)(se1)
    se3 = LSTM(256, return_sequences=True)(se2)

    # Decoder model
    decoder1 = Add()([fe2, se3])
    decoder2 = LSTM(512, return_sequences=False)(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    # Tie it together [image, seq] [word]
    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

# Load the model
model = define_model(vocab_size=len(word_to_index) + 1, max_length=max_length)
model.load_weights('model_weights.h5')

# Generate caption for an image
def generate_caption(photo):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = [word_to_index[w] for w in in_text.split() if w in word_to_index]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = index_to_word[yhat]
        in_text += ' ' + word
        if word == 'endseq':
            break
    final_caption = in_text.split()[1:-1]
    final_caption = ' '.join(final_caption)
    return final_caption

@app.route('/generate_caption', methods=['POST'])
def caption_image():
    file = request.files['image']
    img_path = 'temp_img.jpg'
    file.save(img_path)
    photo = encode_image(img_path)
    photo = photo.reshape((1, 2048))
    caption = generate_caption(photo)
    return jsonify({'caption': caption})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
