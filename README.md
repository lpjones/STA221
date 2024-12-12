# STA221 Final Project - Deepfake CT Scan Detection

The rise of deepfake technology poses significant challenges to the integrity of
medical imaging systems, particularly in lung cancer diagnostics. Manipulated CT
scans can mislead radiologists and AI systems, introducing false abnormalities or
removing real ones. These tampered images have profound implications, ranging
from misdiagnoses that lead to unnecessary treatments or delayed care to broader
issues such as insurance fraud and targeted cyberattacks. This project addresses
the urgent need for robust detection mechanisms capable of identifying such
manipulations.
We propose a machine learning-based framework designed to detect tampered CT
scans with high accuracy and interpretability. Utilizing the Lung Image Database
Consortium dataset, we generated a balanced set of authentic and manipulated
scans using a CT-GAN model. By injecting realistic synthetic nodules into healthy
scans, we created a reliable training dataset. The models evaluated include classical
machine learning approaches such as Support Vector Machines (SVM) and Random
Forest, as well as deep learning architectures like VGG16, ResNet, and DenseNet.
Results demonstrate that deep learning models outperform classical methods,
achieving up to 95.4% accuracy and 0.95 ROC-AUC. Techniques such as data
augmentation and negative space reduction further enhanced model performance.
Additionally, interpretability tools like Grad-CAM were employed to highlight
regions influencing model predictions, fostering trust among clinicians. By devel-
oping a scalable and interpretable solution, this work contributes to safeguarding
patient safety, enhancing diagnostic reliability, and mitigating risks associated with
deepfake manipulations in healthcare.
