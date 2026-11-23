import numpy as np
import cv2
from medmnist import BloodMNIST
from sklearn.metrics import roc_auc_score

def calculate_dpq_isometry(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    
    C = cv2.bilateralFilter(gray, d=3, sigmaColor=75, sigmaSpace=75)
    C = np.maximum(C, 1e-5)
    
    K = (gray - C) * 5.0
    
    A = ((C + K) ** 2) / (4 * C)
    B = ((C - K) ** 2) / (4 * C)
    
    isometry = np.minimum(A, B) / (np.maximum(A, B) + 1e-8)
    
    return -np.mean(isometry)

if __name__ == "__main__":
    print("Loading BloodMNIST dataset...")
    test_data = BloodMNIST(split='test', download=True, size=28)
    images = test_data.imgs
    labels = test_data.labels.flatten()
    
    mask = (labels == 4) | (labels == 3)
    images = images[mask]
    labels_bin = np.where(labels[mask] == 4, 0, 1)
    
    print("Calculating DPQ metrics...")
    features = [calculate_dpq_isometry(img) for img in images]
    
    auc = roc_auc_score(labels_bin, features)
    print(f"Final Result - ROC-AUC: {auc:.4f}")
