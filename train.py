import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix

# =========================
# CONFIG
# =========================
CONFIG = {
    "dataset_dir": "dataset",
    "model_save_dir": "model",
    "img_size": (300, 300),
    "batch_size": 16,

    "val_split": 0.2,
    "seed": 42,

    "epochs_frozen": 25,
    "epochs_finetune": 20,

    "lr_frozen": 1e-3,
    "lr_finetune": 1e-5,

    "dropout": 0.4,
    "label_smoothing": 0.05,
}
IMG_H, IMG_W = CONFIG["img_size"]

# =========================
# DATA GENERATOR
# =========================
def build_generators(dataset_dir):

    def sharpen(img):
        return np.clip(img * 1.2, 0, 255)

    train_aug = ImageDataGenerator(
        rescale=1./255,
        validation_split=CONFIG["val_split"],

        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.15,
        horizontal_flip=True,

        brightness_range=[0.9, 1.1],
        preprocessing_function=sharpen
    )

    val_aug = ImageDataGenerator(
        rescale=1./255,
        validation_split=CONFIG["val_split"]
    )

    train_gen = train_aug.flow_from_directory(
        dataset_dir,
        target_size=CONFIG["img_size"],
        batch_size=CONFIG["batch_size"],
        class_mode="categorical",
        subset="training",
        seed=CONFIG["seed"]
    )

    val_gen = val_aug.flow_from_directory(
        dataset_dir,
        target_size=CONFIG["img_size"],
        batch_size=CONFIG["batch_size"],
        class_mode="categorical",
        subset="validation",
        seed=CONFIG["seed"]
    )

    class_names = list(train_gen.class_indices.keys())
    return train_gen, val_gen, class_names, len(class_names)

# =========================
# CLASS WEIGHTS
# =========================
def get_class_weights(train_gen):
    labels = train_gen.classes
    classes = np.unique(labels)
    weights = compute_class_weight('balanced', classes=classes, y=labels)
    return {i: float(w) for i, w in enumerate(weights)}

# =========================
# MODEL
# =========================
def build_model(n_classes):

    base_model = EfficientNetB3(
        include_top=False,
        weights='imagenet',
        input_shape=(IMG_H, IMG_W, 3)
    )

    base_model.trainable = False

    inputs = keras.Input(shape=(IMG_H, IMG_W, 3))
    x = base_model(inputs, training=False)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(CONFIG["dropout"])(x)

    outputs = layers.Dense(n_classes, activation='softmax')(x)

    model = Model(inputs, outputs)
    return model, base_model

# =========================
# COMPILE
# =========================
def compile_model(model, lr):
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr),
        loss=keras.losses.CategoricalCrossentropy(
            label_smoothing=CONFIG["label_smoothing"]
        ),
        metrics=["accuracy"]
    )

# =========================
# CALLBACKS
# =========================
def get_callbacks(name):
    return [
        ModelCheckpoint(
            f"model/{name}.keras",
            monitor="val_accuracy",
            save_best_only=True,
            save_weights_only=True,
              verbose=1
        ),
         EarlyStopping(patience=5, restore_best_weights=True),
        ReduceLROnPlateau(patience=3)
    ]
# =========================
# MAIN
# =========================
def main():

    train_gen, val_gen, class_names, n_classes = build_generators(CONFIG["dataset_dir"])

    # ✅ CLASS WEIGHTS
    class_weights = get_class_weights(train_gen)

    model, base_model = build_model(n_classes)
    compile_model(model, CONFIG["lr_frozen"])

    # =====================
    # PHASE 1
    # =====================
    h1 = model.fit(
        train_gen,
        epochs=CONFIG["epochs_frozen"],
        validation_data=val_gen,
        class_weight=class_weights,
        callbacks=get_callbacks("phase1"),
        verbose=1
    )

    # =====================
    # PHASE 2 (FINE-TUNE)
    # =====================
    """
    base_model.trainable = True

    for layer in base_model.layers[:-30]:
        layer.trainable = False

    compile_model(model, CONFIG["lr_finetune"])

    h2 = model.fit(
        train_gen,
        epochs=CONFIG["epochs_frozen"] + CONFIG["epochs_finetune"],
        initial_epoch=len(h1.history["accuracy"]),
        validation_data=val_gen,
        class_weight=class_weights,
        callbacks=get_callbacks("phase2"),
        verbose=1
    )
    """

    # =====================
    # EVALUATION
    # =====================
    val_gen.reset()
    preds = model.predict(val_gen)
    y_pred = np.argmax(preds, axis=1)
    y_true = val_gen.classes

    print(classification_report(y_true, y_pred, target_names=class_names))

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10,8))
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=class_names, yticklabels=class_names)
    plt.savefig("model/confusion_matrix.png")

    # =====================
    # SAVE MODEL
    # =====================
    model.save("model/firstmodel.keras")

    print("\n✅ Training Completed Successfully!")

# =========================
if __name__ == "__main__":
    main()
