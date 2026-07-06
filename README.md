**Hybrid Traffic Density Prediction using Greenshields Model and Fuzzy Logic**

This project presents a **Hybrid Traffic Density Prediction System** that integrates the **Greenshields Traffic Flow Model** with a **Fuzzy Inference System (FIS)** to estimate traffic density more effectively.

---

**Features**

- Import and preprocess traffic data
- Remove missing and invalid values
- Estimate traffic density using the Greenshields model
- Predict density using a Fuzzy Inference System
- Generate hybrid predictions by combining both models
- Gaussian membership functions
- Rule-based fuzzy inference
- Performance evaluation using regression metrics
- Traffic density classification (Low, Medium, High)
- Confusion Matrix and Accuracy calculation
- Interactive console-based prediction
- Scatter plot visualization

---

**Technologies Used**

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-Fuzzy
- Scikit-Learn

---

**Dataset**

The project uses a sample traffic dataset stored inside the **dataset** folder.

The dataset contains:

- Space Mean Speed
- Traffic Flow

---

**System Workflow**

**Step 1: Load the Dataset**

The traffic dataset is imported using the Pandas library.

**Step 2: Data Preprocessing**

The dataset is cleaned by:

- Removing missing values
- Removing invalid speed and flow values
- Computing the actual traffic density

Formula:

```text
Traffic Density = Traffic Flow / Space Mean Speed
```

**Step 3: Greenshields Traffic Model**

```text
Density = Kj × (1 − Speed / Vf)
```

where:

- **Vf** = Free-flow speed
- **Kj** = Jam density

**Step 4: Fuzzy Inference System**

**Inputs**

- Space Mean Speed
- Traffic Flow

**Output**

- Traffic Density

Gaussian Membership Functions:

**Speed**

- Low
- Medium
- High

**Traffic Flow**

- Low
- Medium
- High

**Traffic Density**

- Low
- Medium
- High

**Step 5: Fuzzy Rule Base**

The model uses **9 fuzzy rules**.

Example rules:

- High Speed + Low Flow → Low Density
- High Speed + High Flow → Medium Density
- Medium Speed + High Flow → High Density
- Low Speed + Medium Flow → High Density
- Low Speed + High Flow → High Density

**Step 6: Hybrid Prediction**

The final prediction combines:

- Greenshields Density
- Fuzzy Density

using a ratio-based weighting mechanism.

**Step 7: Performance Evaluation**

**Regression Metrics**

- RMSE
- MAE
- R² Score

**Classification Metrics**

- Accuracy
- Error Rate
- Confusion Matrix

**Step 8: Visualization**

The project compares:

- Actual Traffic Density
- Greenshields Prediction
- Hybrid Prediction

using scatter plots.

---

**Sample Outputs**

**Evaluation Metrics**

![Evaluation](c:\Users\anwik\Downloads\evaluation.png)

**Traffic Density Prediction**

![Prediction](c:\Users\anwik\Downloads\prediction.png)

**Scatter Plot**

![Graph](c:\Users\anwik\Downloads\graph.png)

---

**Project Structure**

```text
Hybrid-Traffic-Density-Prediction
│
├── dataset
│   └── traffic_small.csv
│
├── screenshots
│   ├── evaluation.png
│   ├── prediction.png
│   └── graph.png
│
├── main.py
├── requirements.txt
└── README.md
```

---

**Installation**

Clone the repository:

```bash
git clone https://github.com/anwikamothukuri/Hybrid-Traffic-Density-Prediction.git
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

---

**Future Enhancements**

- Develop a Streamlit web application
- Integrate real-time traffic data
- Compare with machine learning models
- Optimize fuzzy rules using evolutionary algorithms
- Extend the model for multi-road traffic analysis

---

**Author**

**Mothukuri Anwika**

B.Tech Computer Science Engineering

VIT-AP University

GitHub: https://github.com/anwikamothukuri