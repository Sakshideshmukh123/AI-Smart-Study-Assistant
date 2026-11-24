"""
Script to generate realistic sample university PDF documents:
- Syllabus (Machine Learning & Data Science)
- Faculty Lecture Notes
- 3 Past Year Question Papers (2022, 2023, 2024) with overlapping high-frequency questions
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


def create_pdf(filename, title, subtitle, content_blocks):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=2.2*cm,
        rightMargin=2.2*cm,
        topMargin=2.0*cm,
        bottomMargin=2.0*cm
    )

    ss = getSampleStyleSheet()
    brand_blue = colors.HexColor("#0284C7")
    slate_dark = colors.HexColor("#0F172A")
    slate_muted = colors.HexColor("#64748B")

    title_st = ParagraphStyle("DocTitle", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=18, textColor=brand_blue, leading=22)
    sub_st = ParagraphStyle("DocSub", parent=ss["Normal"], fontName="Helvetica", fontSize=10, textColor=slate_muted, leading=14)
    h2_st = ParagraphStyle("DocH2", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, textColor=slate_dark, spaceBefore=12, spaceAfter=6)
    body_st = ParagraphStyle("DocBody", parent=ss["Normal"], fontName="Helvetica", fontSize=10, textColor=slate_dark, leading=15, spaceAfter=4)
    bullet_st = ParagraphStyle("DocBullet", parent=ss["Normal"], fontName="Helvetica", fontSize=10, textColor=slate_dark, leading=15, leftIndent=15, firstLineIndent=-10, spaceAfter=3)

    story = []
    # Header table
    hdr_data = [[
        Paragraph(f"<b>{title}</b>", title_st),
        Paragraph(subtitle, sub_st)
    ]]
    t = Table(hdr_data, colWidths=[12*cm, 5*cm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(HRFlowable(width="100%", thickness=1.5, color=brand_blue, spaceAfter=14))

    for block_type, text in content_blocks:
        if block_type == "h2":
            story.append(Paragraph(f"<b>{text}</b>", h2_st))
        elif block_type == "p":
            story.append(Paragraph(text, body_st))
        elif block_type == "bullet":
            story.append(Paragraph(f"• {text}", bullet_st))
        elif block_type == "space":
            story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    print(f"Generated: {filename}")


def main():
    out_dir = "sample_data"

    # 1. Syllabus PDF
    create_pdf(
        os.path.join(out_dir, "Syllabus_Machine_Learning.pdf"),
        "University Curriculum: Machine Learning (CS-701)",
        "Department of Computer Science & Engineering<br/>Academic Session 2024-2025",
        [
            ("h2", "Course Overview & Objectives"),
            ("p", "This course introduces fundamental paradigms in Machine Learning, Statistical Learning Theory, and Model Evaluation. Students will learn core supervised, unsupervised, and reinforcement algorithms along with practical evaluation metrics."),
            ("space", ""),
            ("h2", "Unit 1: Foundations of Learning"),
            ("bullet", "Introduction to Machine Learning: Supervised, Unsupervised, Semi-supervised, and Reinforcement Learning paradigms."),
            ("bullet", "Inductive bias, PAC learnability, Occam's razor, and Bias-Variance tradeoff."),
            ("bullet", "Linear Regression, Cost functions, Gradient Descent algorithms (Batch, Stochastic, Mini-batch)."),
            ("space", ""),
            ("h2", "Unit 2: Classification Algorithms"),
            ("bullet", "Logistic Regression, Binary and Multiclass classification, Maximum Likelihood Estimation."),
            ("bullet", "Decision Trees: ID3, C4.5, CART, Entropy, Information Gain, and Gini Index. Overfitting and tree pruning."),
            ("bullet", "Support Vector Machines (SVM): Hyperplanes, Margin optimization, Soft-margin SVM, and Kernel trick."),
            ("space", ""),
            ("h2", "Unit 3: Unsupervised Learning & Clustering"),
            ("bullet", "Clustering: K-Means algorithm, Elbow method, Silhouette score, and Hierarchical clustering."),
            ("bullet", "Dimensionality Reduction: Principal Component Analysis (PCA) and Eigenvalue decomposition."),
            ("space", ""),
            ("h2", "Unit 4: Model Evaluation & Ensemble Learning"),
            ("bullet", "Evaluation Metrics: Confusion matrix, Precision, Recall, F1-Score, ROC-AUC curve."),
            ("bullet", "Ensemble methods: Bagging, Random Forests, Boosting (AdaBoost, XGBoost)."),
        ]
    )

    # 2. Faculty Notes PDF
    create_pdf(
        os.path.join(out_dir, "Faculty_Notes_Machine_Learning.pdf"),
        "Faculty Lecture Notes: Core ML Modules",
        "Prof. R. K. Sharma | CSE Dept.<br/>Reference Study Material",
        [
            ("h2", "Module 1: Supervised vs Unsupervised Learning"),
            ("p", "Supervised learning algorithms infer a function from labeled training data consisting of input-output pairs. Examples include Linear Regression, Support Vector Machines, and Decision Trees. In contrast, Unsupervised Learning discovers hidden structures or patterns within unlabeled data, such as K-Means clustering and PCA."),
            ("space", ""),
            ("h2", "Module 2: Bias-Variance Decomposition & Overfitting"),
            ("p", "The prediction error of any statistical model comprises Bias, Variance, and Irreducible Noise. High bias leads to underfitting (the model fails to capture underlying patterns). High variance leads to overfitting (the model memorizes noise in training data). Regularization techniques such as L1 (Lasso) and L2 (Ridge) constrain model weights to mitigate variance."),
            ("space", ""),
            ("h2", "Module 3: Decision Trees and Information Gain"),
            ("p", "Decision tree algorithms choose the attribute that maximizes Information Gain at each node. Entropy H(S) measures the impurity of set S. For a binary target, Entropy = -p*log2(p) - (1-p)*log2(1-p). Pruning eliminates subtrees with low statistical significance."),
            ("space", ""),
            ("h2", "Module 4: K-Means Clustering Algorithm"),
            ("p", "K-Means is an iterative centroid-based clustering algorithm. Steps: 1) Initialize K cluster centroids randomly. 2) Assign each data point to its nearest centroid using Euclidean distance. 3) Recompute centroid coordinates as the mean of assigned points. 4) Repeat steps 2-3 until convergence."),
        ]
    )

    # 3. PYQ Paper 2022
    create_pdf(
        os.path.join(out_dir, "PYQ_Paper_May_2022.pdf"),
        "Semester Examination May 2022",
        "Subject: Machine Learning (CS-701)<br/>Max Marks: 100 | Time: 3 Hours",
        [
            ("h2", "Section A (Compulsory Questions)"),
            ("p", "Q1. Explain the difference between Supervised and Unsupervised Learning with suitable examples."),
            ("p", "Q2. Define overfitting and underfitting. How does regularization help in mitigating overfitting?"),
            ("p", "Q3. Explain the working principle of the K-Means clustering algorithm."),
            ("space", ""),
            ("h2", "Section B (Descriptive Questions)"),
            ("p", "Q4. Describe Decision Tree induction. How are Entropy and Information Gain calculated in ID3?"),
            ("p", "Q5. Derive the cost function for Linear Regression and explain Gradient Descent optimization."),
            ("p", "Q6. Explain the concept of Confusion Matrix, Precision, Recall, and F1-Score with equations."),
        ]
    )

    # 4. PYQ Paper 2023 (Repeats Q1, Q2, Q3 with slight variation)
    create_pdf(
        os.path.join(out_dir, "PYQ_Paper_Dec_2023.pdf"),
        "Semester Examination Dec 2023",
        "Subject: Machine Learning (CS-701)<br/>Max Marks: 100 | Time: 3 Hours",
        [
            ("h2", "Section A (Compulsory Questions)"),
            ("p", "Q1. Differentiate between Supervised and Unsupervised Learning paradigms."),
            ("p", "Q2. Explain the working of K-Means clustering algorithm. Mention its limitations."),
            ("p", "Q3. What is Support Vector Machine (SVM)? Explain maximum margin hyperplane."),
            ("space", ""),
            ("h2", "Section B (Descriptive Questions)"),
            ("p", "Q4. Define overfitting and explain how L1 and L2 regularization prevent it."),
            ("p", "Q5. Describe Random Forest ensemble and explain how bagging reduces variance."),
            ("p", "Q6. What is Principal Component Analysis (PCA)? State its applications in dimensionality reduction."),
        ]
    )

    # 5. PYQ Paper 2024 (Repeats Q1 and Q2 again!)
    create_pdf(
        os.path.join(out_dir, "PYQ_Paper_May_2024.pdf"),
        "Semester Examination May 2024",
        "Subject: Machine Learning (CS-701)<br/>Max Marks: 100 | Time: 3 Hours",
        [
            ("h2", "Section A (Compulsory Questions)"),
            ("p", "Q1. Explain the difference between Supervised and Unsupervised Learning with real-world use cases."),
            ("p", "Q2. Explain the step-by-step algorithm of K-Means clustering with an example."),
            ("p", "Q3. Differentiate between Bagging and Boosting in Ensemble Learning."),
            ("space", ""),
            ("h2", "Section B (Descriptive Questions)"),
            ("p", "Q4. How is Information Gain computed in Decision Trees? Explain with formula."),
            ("p", "Q5. Explain ROC curve and AUC metric for binary classification models."),
            ("p", "Q6. Define bias-variance tradeoff and illustrate with diagrams."),
        ]
    )


if __name__ == "__main__":
    main()
