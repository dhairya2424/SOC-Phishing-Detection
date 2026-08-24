import joblib
import os


MODEL_INPUT_PATH = "D:\\rf.pkl"       # change if needed
MODEL_OUTPUT_PATH = "models_new\\rf_model_compressed.pkl"


def prune_random_forest(model, keep_trees=80):
    if hasattr(model, "estimators_"):
        original = len(model.estimators_)
        model.estimators_ = model.estimators_[:keep_trees]
        model.n_estimators = keep_trees
        print(f"🌲 Trees reduced: {original} → {keep_trees}")
    return model


def compress_model():
    print("📥 Loading model...")

    model = joblib.load(MODEL_INPUT_PATH)

    print("✂️ Pruning model...")
    model = prune_random_forest(model, keep_trees=80)

    print("📦 Compressing and saving...")
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_OUTPUT_PATH, compress=("xz", 6))

    size = os.path.getsize(MODEL_OUTPUT_PATH) / (1024 * 1024)

    print("✅ Compression Done")
    print(f"📦 Final Size: {size:.2f} MB")


if __name__ == "__main__":
    compress_model()