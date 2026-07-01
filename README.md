# 🧪 Aqueous Solubility Prediction using Machine Learning

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Regression-orange?logo=scikitlearn)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter)

</p>

Predicting the **aqueous solubility (logS)** of small molecules using molecular descriptors and classical machine learning algorithms. This project implements an end-to-end regression pipeline using the **Delaney ESOL dataset**, comparing a **Linear Regression** model with a **Random Forest Regressor**.

---

## 📌 Project Highlights

* Built an end-to-end regression pipeline using Scikit-learn
* Trained and compared **Linear Regression** and **Random Forest Regressor**
* Evaluated model performance using **Mean Squared Error (MSE)** and **R² Score**
* Visualized prediction performance using regression analysis
* Demonstrated that simpler models can outperform more complex models on low-dimensional datasets

---

## 🧬 Why Predict Solubility?

Aqueous solubility is one of the most important physicochemical properties in **drug discovery**.

Many promising drug candidates fail because they dissolve poorly in water, reducing their bioavailability. Experimental measurement of solubility is expensive and time-consuming, making computational prediction an important task in **cheminformatics**.

This project reproduces the classical **Delaney (ESOL)** approach by predicting molecular solubility directly from easily computed molecular descriptors.

---

## 📂 Dataset

### Source

The project uses the **Delaney Solubility Dataset**, which contains molecular descriptors and experimentally measured aqueous solubility values (`logS`) for small organic molecules.

### Dataset Summary

| Property            | Value                         |
| ------------------- | ----------------------------- |
| **Samples**         | 1,144 molecules               |
| **Task**            | Regression                    |
| **Target Variable** | **logS (Aqueous Solubility)** |

### Molecular Descriptors Used

| Feature                | Description                         |
| ---------------------- | ----------------------------------- |
| **MolLogP**            | Octanol/Water partition coefficient |
| **MolWt**              | Molecular Weight                    |
| **NumRotatableBonds**  | Number of rotatable bonds           |
| **AromaticProportion** | Fraction of aromatic atoms          |

These descriptors can be calculated directly from molecular structures without laboratory experiments, making them suitable for rapid computational screening.

---

## ⚙️ Machine Learning Workflow

```text
Load Dataset
      │
      ▼
Data Preprocessing
      │
      ▼
Feature Selection
      │
      ▼
Train-Test Split (80:20)
      │
      ▼
─────────────────────────────────
│                               │
▼                               ▼
Linear Regression        Random Forest
│                               │
──────────────┬──────────────────
              ▼
      Model Evaluation
              │
              ▼
        MSE • R² Score
```

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Jupyter Notebook

---

## 📈 Results

| Model                   | Training MSE | Training R² |  Test MSE |   Test R² |
| ----------------------- | -----------: | ----------: | --------: | --------: |
| **Linear Regression**   |    **1.008** |   **0.765** | **1.021** | **0.789** |
| Random Forest Regressor |        1.028 |       0.760 |     1.408 |     0.709 |

### Key Findings

* **Linear Regression achieved the best predictive performance** on both the training and testing datasets.
* The close agreement between training and testing metrics indicates **good generalization** with minimal evidence of overfitting.
* The shallow Random Forest (`max_depth=2`) produced lower predictive performance, demonstrating that **simpler models can outperform more complex models** when the relationship between features and target is approximately linear.

### Conclusion

Linear Regression outperformed the constrained Random Forest model, achieving a **Test R² of 0.789** while maintaining consistent performance on unseen data. The results show that simpler regression models can be highly effective for predicting molecular solubility when using a small set of informative molecular descriptors.

---

## 📁 Repository Structure

```text
molecular-solubility-prediction/
│
├── data/
│   └── delaney_solubility_with_descriptors.csv
│
├── notebook/
│   └── solubility.ipynb
│
└── README.md
```

---

## 👨‍💻 Collaborators

- **Debashis Kar** (www.linkedin.com/in/debashis-kar-0b033830a)
- **Divyom Srivastava** (https://www.linkedin.com/in/divyom-srivastava-260b95342/)

⭐ If you found this project useful, consider giving it a star!
