"""All text of the site lives here. Edit this file, then run `python tools/build.py`."""

SITE_URL = "https://ftharir.github.io"

# Address of the form service, e.g. "https://formspree.io/f/xxxxxxxx" (see README).
# While it is empty, the contact form opens the visitor's e-mail app instead.
CONTACT_FORM_ENDPOINT = ""

PROFILE = {
    "name": "Fatemeh Harirforoush",
    "short": "Fatemeh Harir",
    "role": "AI Software Engineer · Machine Learning Engineer",
    "location": "Tehran, Iran",
    "email": "fatemeh.harirforoush04@gmail.com",
    "github": "https://github.com/ftharir",
    "linkedin": "https://www.linkedin.com/in/fatemeh-harirforoush-01a15927b/",
    "tagline": "AI systems, from messy data to a working product.",
    "summary": (
        "Computer Engineering graduate and AI Software Engineer who builds end-to-end intelligent systems: "
        "machine-learning and deep-learning models, backend architectures and data pipelines. "
        "Research and engineering experience in Transformers, large language models, computer vision, "
        "speech processing and applied machine learning."
    ),
    "values": ["tidy datasets", "honest evaluation", "clean code"],
}

# filter pills on the projects page: (key, label)
AREAS = [
    ("cv", "Computer vision", "pink"),
    ("data", "Data analysis", "peach"),
    ("ml", "Machine learning", "lav"),
    ("backend", "Backend", "green"),
    ("speech", "Speech & LLM", "sky"),
    ("research", "Research", "butter"),
]

PROJECTS = [
    {
        "slug": "industrial-gauge-localization", "gallery": "one",
        "title": "Industrial gauge localization",
        "repo": "industrial-gauge-localization",
        "color": "pink", "areas": ["cv"], "label": "Computer vision",
        "metric": "mAP@0.5 0.995",
        "summary": "YOLOv5 finds analog pressure gauges in video, trained on 435 hand-annotated frames.",
        "lead": "A real-time object detector that locates analog pressure gauges in industrial video, built from raw footage to a trained, exported and documented model.",
        "facts": [("0.995", "mAP@0.5"), ("0.978", "mAP@0.5:0.95"), ("435", "annotated frames"), ("YOLOv5s", "model")],
        "tech": ["Python", "YOLOv5", "PyTorch", "OpenCV", "LabelMe", "ONNX"],
        "problem": "Gauges have to be found in the frame before anything can be read from them. The footage was raw video without labels, so the whole pipeline had to be built: annotation, training, evaluation and inference.",
        "built": [
            "Annotated 435 frames by hand with LabelMe (four annotation sets, two passes) and converted them to YOLO format.",
            "Trained a YOLOv5s detector and exported it to PyTorch and ONNX weights.",
            "Compared it against a classical computer-vision baseline and tested on unseen videos.",
            "Wrote a data audit (it found that the original train and validation folders overlapped, so a fresh 348 / 87 split was made) and documented a model card and a dataset card.",
        ],
        "results": [
            "mAP@0.5 of 0.995 and mAP@0.5:0.95 of 0.978 on the validation split.",
            "The validation set (87 of 435 frames) is a random split of continuous video, so near-duplicates of training frames land in validation: the scores describe the same recordings, not new cameras. The audit also found that the original train and validation folders overlapped, so they were discarded. The repository states all of this openly.",
        ],
        "images": [("industrial-gauge-localization/results/demo/yolo_detection_result.gif", "gauge-detection.gif", "The detector running on video."),
                   ("industrial-gauge-localization/results/figures/08_classical_cv_overview.png", "classical-cv.webp", "Classical computer-vision baseline compared with the detector.")],
    },
    {
        "slug": "cost-allocation-data-analysis",
        "title": "Cost allocation data analysis",
        "repo": "cost-allocation-data-analysis",
        "color": "peach", "areas": ["data"], "label": "Data analysis",
        "metric": "30 tests",
        "summary": "Messy Excel sources become one clean, allocated dataset that feeds a Power BI dashboard.",
        "lead": "A Python data pipeline that automates a monthly cost allocation: several Excel sources in, a validated and allocated reporting dataset out.",
        "facts": [("57", "rows in the final report"), ("30", "automated tests"), ("8", "figures"), ("6", "tables")],
        "tech": ["Python", "pandas", "Power BI", "pytest", "Excel"],
        "problem": "Costs arrived in several Excel files with inconsistent layouts, and the allocation between companies (direct and shared costs, headcount) was done by hand every month.",
        "built": [
            "Validation and cleaning of every source, with a data-quality report of the issues found.",
            "Aggregation and allocation logic, covered by 30 pytest tests.",
            "A final reporting dataset for Power BI and a reconciliation from raw to final totals.",
            "Documentation in English and Persian, including three business rules that were decided but not yet implemented.",
        ],
        "results": [
            "A 57-row final report that reconciles with the raw sources.",
            "Eight figures and six tables describing costs per company, per month and per category, shared cost versus headcount, and data-quality issues.",
        ],
        "images": [("cost-allocation-data-analysis/reports/figures/01_cost_per_company_and_month.png", "cost-per-company.webp", "Direct and shared costs per company and month."),
                   ("cost-allocation-data-analysis/reports/figures/08_raw_to_final_reconciliation.png", "reconciliation.webp", "Reconciliation from the raw sources to the final report.")],
    },
    {
        "slug": "pharmacogenomics-ml-data-analysis",
        "title": "Pharmacogenomics data analysis",
        "repo": "pharmacogenomics-ml-data-analysis",
        "color": "peach", "areas": ["data", "ml"], "label": "Data analysis · ML",
        "metric": "leakage found and fixed",
        "summary": "Predicting the effect of a genetic variant on a drug with an SVM, including an audit that removed data leakage.",
        "lead": "Exploration and classification of 4,698 reported links between genetic variants and drugs, where an honest score mattered more than a high one.",
        "facts": [("4,698", "variant–drug records"), ("12", "imbalanced classes"), ("59.3% → 42.2%", "score after fixing leakage"), ("34.5%", "most-frequent baseline")],
        "tech": ["Python", "scikit-learn", "SVM", "pandas", "matplotlib"],
        "problem": "Each row says what a variant does to a drug (for example increased efficacy or decreased dosage). The task is to predict that effect from the variant, gene, drug and consequence, with twelve classes and heavy imbalance.",
        "built": [
            "Exploratory analysis: class balance, duplicates, conflicting reports, which genes and drugs matter.",
            "A leakage audit that removed exact duplicates (4,698 to 3,295 rows) and fitted all encodings on the training split only.",
            "A linear and a tuned RBF SVM compared with a most-frequent-class baseline.",
        ],
        "results": [
            "The first run reported 59.3%; after removing the leakage the honest accuracy is 42.2% (weighted F1 0.42, macro F1 0.29) against a 34.5% baseline.",
            "The project documents each fix and the score after it, so the drop is explained rather than hidden.",
        ],
        "images": [("pharmacogenomics-ml-data-analysis/reports/figures/05_score_after_each_fix.png", "score-after-fixes.webp", "How the score changes after each fix."),
                   ("pharmacogenomics-ml-data-analysis/reports/figures/06_confusion_matrix_final.png", "confusion-matrix.webp", "Confusion matrix of the final model.")],
    },
    {
        "slug": "explainable-skin-disease-classification", "gallery": "one",
        "title": "Explainable skin disease classification",
        "repo": "explainable-skin-disease-classification",
        "color": "pink", "areas": ["cv", "ml"], "label": "Computer vision · XAI",
        "metric": "macro-F1 0.80",
        "summary": "ResNet18 classifies five facial skin conditions and Grad-CAM shows why; includes a Streamlit demo.",
        "lead": "Bachelor thesis: classify five facial skin conditions from a photo and make the decision inspectable with Grad-CAM heatmaps.",
        "facts": [("80.0%", "test accuracy"), ("0.797", "macro F1"), ("185", "test images"), ("5", "classes")],
        "tech": ["Python", "PyTorch", "ResNet18", "Grad-CAM", "Streamlit", "Transfer learning"],
        "problem": "Medical-image models are only useful if people can see what they look at. With a small dataset (375 training images) the model also overfits quickly, so evaluation and error analysis matter.",
        "built": [
            "Transfer learning with a fine-tuned ResNet18 on five classes: acne, actinic keratosis, basal cell carcinoma, eczema and rosacea.",
            "Grad-CAM explanations, including a comparison of layer3 and layer4.",
            "A Streamlit demo that shows the prediction, the class probabilities and the heatmap.",
            "A model card, a dataset card, an error gallery and the thesis in English and Persian.",
        ],
        "results": [
            "80.0% accuracy and macro F1 0.797 on a held-out test set of 185 images (37 per class).",
            "Actinic keratosis is the hardest class (recall 62%); the model tends to answer basal cell carcinoma when unsure. This is a research project, not a medical device.",
        ],
        "images": [("explainable-skin-disease-classification/docs/gradcam_examples.png", "gradcam.webp", "Grad-CAM: the regions that drive each prediction."),
                   ("explainable-skin-disease-classification/docs/confusion_matrix.png", "confusion.webp", "Confusion matrix on the 185 test images."),
                   ("explainable-skin-disease-classification/docs/demo.png", "demo.webp", "The Streamlit demo.")],
    },
    {
        "slug": "voiceledger",
        "title": "VoiceLedger",
        "repo": "VoiceLedger",
        "color": "sky", "areas": ["speech", "backend"], "label": "Speech · Backend",
        "metric": "Persian speech-to-text",
        "summary": "A Bale bot and REST API that turn spoken work reports into a searchable knowledge base.",
        "lead": "Freelance project: an AI-powered organizational knowledge assistant. A member sends a voice message, the system transcribes it to Persian text and stores it for retrieval.",
        "facts": [("Faster Whisper", "local Persian STT"), ("FastAPI", "REST API"), ("PostgreSQL", "knowledge base"), ("Docker", "deployment")],
        "tech": ["Python", "FastAPI", "PostgreSQL", "SQLAlchemy", "Docker", "Faster Whisper", "Bale API"],
        "problem": "In many organizations daily reports are given verbally and then lost. The goal was to capture them in a messenger people already use and make them searchable.",
        "built": [
            "The backend from scratch: database design, user management with admin approval, voice processing and automated report workflows.",
            "A local Persian speech-to-text pipeline with Faster Whisper, run in a worker thread so the bot is never blocked.",
            "One database commit that saves the transcript, completes the report and creates the knowledge entry.",
            "Docker-based deployment and an API ready for semantic search and RAG extensions.",
        ],
        "results": [
            "A working bot and REST API, documented with architecture, data model and API reference.",
        ],
        "flow": ["Voice message in Bale", "Approved user?", "Download audio", "Faster Whisper (Persian)", "PostgreSQL knowledge base", "Reply with text and tracking ID"],
        "images": [],
    },
    {
        "slug": "ctc-captcha-recognition",
        "title": "Captcha recognition",
        "repo": "ctc-captcha-recognition",
        "color": "lav", "areas": ["cv", "ml"], "label": "Computer vision · DL",
        "metric": "99.1% exact match",
        "summary": "A CNN + bidirectional GRU trained with CTC loss reads 5-character captchas end to end.",
        "lead": "Reads whole captcha images and outputs the text, without segmenting characters. A course project that was rebuilt with a corrected training and evaluation pipeline.",
        "facts": [("99.07%", "exact match on test"), ("99.81%", "character accuracy"), ("107", "held-out test images"), ("25 min", "training time")],
        "tech": ["Python", "PyTorch", "CRNN", "CTC loss", "pytest"],
        "problem": "Captcha text is distorted and touching, so segmenting characters is brittle. CTC lets the network read the whole image directly.",
        "built": [
            "A CNN and bidirectional GRU network trained with CTC loss.",
            "An 80/10/10 split with a fixed seed, so the test set is never used for training or model selection.",
            "Training, evaluation and prediction scripts, unit tests and per-epoch history.",
        ],
        "results": [
            "106 of 107 test captchas exactly right (99.07%); the only error missed the first character.",
            "With 107 test images the 95% confidence interval is roughly 94.9% to 99.8%, so the point estimate is not more precise than that.",
        ],
        "images": [("ctc-captcha-recognition/results/sample_predictions.png", "predictions.webp", "Sample predictions."),
                   ("ctc-captcha-recognition/results/training_curves.png", "training-curves.webp", "Training curves; the first epochs are the plateau typical for CTC models.")],
    },
    {
        "slug": "ml-playbook",
        "title": "ML Playbook",
        "repo": "ml-playbook",
        "color": "butter", "areas": ["ml", "data"], "label": "Machine learning",
        "metric": "6 case studies",
        "summary": "Six end-to-end case studies, each with the original notebook and a more rigorous follow-up analysis.",
        "lead": "Classification, regression, NLP and computer vision, written while learning and then revisited with proper evaluation.",
        "facts": [("6", "case studies"), ("97.9%", "breast-cancer accuracy"), ("94.0%", "spam recall"), ("0.832", "housing R²")],
        "tech": ["Python", "scikit-learn", "TensorFlow / Keras", "pandas", "Jupyter"],
        "problem": "Early notebooks often report a single accuracy number. The playbook keeps them as they were and adds the evaluation they were missing.",
        "built": [
            "Six projects: breast cancer, heart disease, SMS spam, housing prices, hot dog CNN and helmet detection.",
            "For each one an analysis notebook with several models, cross-validation, fixed seeds, leak-free preprocessing and error analysis.",
            "A README per project that states the original and the follow-up result side by side.",
        ],
        "results": [
            "Breast cancer: accuracy 94.1% to 97.9%, malignant recall 91% to 98.5%.",
            "SMS spam: spam recall 70% to 94.0%, F1 0.962. Housing: R² 0.822 to 0.832.",
            "Heart disease and helmet detection are reported with their weaknesses (for example 16% recall for riders without a helmet).",
        ],
        "images": [],
        "table": [("Breast cancer", "94.1% accuracy", "97.9% accuracy; malignant recall 98.5%"),
                  ("Heart disease risk", "86% training accuracy only", "CV ROC-AUC 0.723; CHD recall 5% to 60%"),
                  ("SMS spam", "96% accuracy, 70% spam recall", "Spam recall 94.0%, F1 0.962"),
                  ("Housing prices", "R² 0.822", "R² 0.832, RMSE about $46.9k"),
                  ("Hot dog CNN", "Log inside the notebook", "73% validation accuracy at epoch 18"),
                  ("Helmet detection", "62.5% test accuracy", "69.1% vs 67.1% majority baseline")],
    },
    {
        "slug": "telegram-services-platform",
        "title": "Telegram services platform",
        "repo": "telegram-services-platform",
        "color": "green", "areas": ["backend"], "label": "Backend",
        "metric": "39 tests",
        "summary": "An async Telegram marketplace bot with a coin wallet, order lifecycle and an external SMM API.",
        "lead": "Freelance project: a scalable Telegram-based service marketplace with user management, digital service ordering and automated workflows.",
        "facts": [("aiogram 3", "bot"), ("FastAPI", "web service"), ("39", "automated tests"), ("4", "database tables")],
        "tech": ["Python", "aiogram", "FastAPI", "PostgreSQL", "SQLAlchemy", "Redis", "Alembic", "Docker"],
        "problem": "Users order digital services inside Telegram and pay with coins. Money, orders and an external provider have to stay consistent even when the provider fails.",
        "built": [
            "An asynchronous backend: wallet with atomic credit and debit, transaction history, orders with a tracking code and an idempotency key.",
            "A RapidSeen API client, a background job that checks open orders, and proportional refunds for partial and canceled orders with double-refund protection.",
            "Bilingual (Persian and English) bot flows: ordering, order tracking, forced channel join, user registration.",
            "Alembic migrations, health endpoints, Docker Compose, and a test suite that runs against a fresh database.",
        ],
        "results": [
            "39 tests pass against a fresh PostgreSQL database; the decisions behind the refund and cancel rules are written down in the repository.",
            "The ordering flows are covered by unit tests but have not yet been run end to end against a live provider account.",
        ],
        "flow": ["Telegram user", "Handlers", "Services (wallet, orders)", "Repositories", "PostgreSQL", "RapidSeen API"],
        "images": [],
    },
    {
        "slug": "moleculenet-3d-structure-study",
        "title": "MoleculeNet 3D structure study",
        "repo": "moleculenet-3d-structure-study",
        "color": "lav", "areas": ["research", "ml", "data"], "label": "Research",
        "metric": "3 structure types",
        "summary": "RDKit 3D structures for BACE, BBBP and ClinTox, and how the structure type affects property prediction.",
        "lead": "A lab research task: build several kinds of 3D structure for molecules so that a structure-based model can be evaluated on each of them.",
        "facts": [("3", "datasets"), ("3", "structure types"), ("5,046", "molecules processed"), ("PVD", "reference model")],
        "tech": ["Python", "RDKit", "scikit-learn", "pandas", "Jupyter"],
        "problem": "Models that predict molecular properties from 3D structure are tested on accurately computed geometries, but everyday datasets only have SMILES strings. How much does the generated structure matter?",
        "built": [
            "Approximate (embedding), UFF-optimised and flat graph (z = 0) structures for BACE, BBBP and ClinTox, exported as SDF.",
            "A failure report: invalid SMILES, molecules that cannot be embedded, and UFF optimisations that do not converge.",
            "A Random Forest comparison of the structure types against a no-coordinates baseline (scaffold and random split, five seeds).",
        ],
        "results": [
            "The three structure types are statistically hard to tell apart in this proxy experiment, and the no-coordinates baseline is the best model in every task.",
            "The PVD model itself (pre-training via denoising) was not run; the repository explains the idea and the steps to continue.",
        ],
        "images": [("moleculenet-3d-structure-study/docs/images/example_three_structures.png", "three-structures.webp", "One molecule as approximate, UFF-optimised and flat structure."),
                   ("moleculenet-3d-structure-study/docs/images/model_comparison_roc_auc.png", "roc-auc.webp", "ROC-AUC for each structure type and split.")],
    },
]

EXPERIENCE = [
    {
        "role": "AI Software Engineering Intern · Project Owner",
        "org": "Sharif Setup — Generative AI startup",
        "period": "August 2026 – present", "kind": "12-week internship", "color": "sky",
        "bullets": [
            "Owned the end-to-end development of an AI-powered data labeling platform: system design, application structure, database schema, authentication and core workflows, through to deployment.",
            "Built a Streamlit multimodal annotation platform for ASR, OCR and vehicle attribute recognition, with AI-based pseudo-labeling, human-in-the-loop correction and quality control.",
            "Implemented project and dataset management, standardized data pipelines and machine-learning workflows for vehicle attribute recognition: dataset preparation, fine-tuning, evaluation and inference.",
        ],
        "tech": ["Python", "Streamlit", "PostgreSQL", "SQLAlchemy", "Docker Compose", "PyTorch", "Computer vision"],
    },
    {
        "role": "Freelance AI software engineer",
        "org": "Independent projects",
        "period": "Selected freelance work", "kind": "freelance", "color": "green",
        "bullets": [
            "VoiceLedger: an AI-powered organizational knowledge assistant that collects voice reports through a Bale bot, with a Persian speech-to-text pipeline.",
            "Telegram services platform: an asynchronous service marketplace with wallet, orders and an external API.",
            "Cost allocation prototype: a Python pipeline from several Excel sources to Power BI reporting datasets.",
        ],
        "tech": ["FastAPI", "PostgreSQL", "Redis", "Docker", "Faster Whisper", "pandas", "Power BI"],
    },
    {
        "role": "Data Scientist Bootcamp trainee",
        "org": "Fanap",
        "period": "December 2023 – September 2024", "kind": "bootcamp", "color": "peach",
        "bullets": [
            "Selected through Quera's Hafez competition for Fanap's Data Scientist Bootcamp.",
            "Hands-on work in Python, SQL, machine learning and deep learning; ranked among the top participants and worked with CNNs, RNNs, GANs and Transformers.",
        ],
        "tech": ["Python", "SQL", "CNN", "RNN", "GAN", "Transformers"],
    },
]

RESEARCH = [
    {
        "role": "AI Researcher — LLMs, Transformers and scientific applications",
        "org": "Sharif Center for Information Systems and Data Science",
        "period": "March 2025 – June 2026", "color": "lav",
        "bullets": [
            "Research on predictive maintenance for industrial systems with Transformers, contrastive learning, physics-informed neural networks and diffusion models, for battery and bearing health monitoring.",
            "Resulted in a manuscript submitted to a Q1 journal, currently under review.",
        ],
        "tech": ["Transformers", "Contrastive learning", "PINNs", "Diffusion models"],
    },
    {
        "role": "Research Assistant — Computer vision",
        "org": "Sharif University of Technology lab",
        "period": "June 2024 – February 2025", "color": "pink",
        "bullets": [
            "Deep-learning computer-vision solutions for quadcopter platforms: object detection, tracking and visual recognition.",
        ],
        "tech": ["Object detection", "Tracking", "Deep learning"],
    },
    {
        "role": "Research task — 3D molecular structures",
        "org": "Sharif University of Technology lab",
        "period": "mid-2024", "color": "butter",
        "bullets": [
            "Generated approximate, UFF-optimised and flat graph 3D structures for the BACE, BBBP and ClinTox datasets, so that a structure-based model (PVD, pre-training via denoising) can be evaluated on each of them.",
            "Published as the MoleculeNet 3D structure study, with a failure analysis and a small comparison experiment.",
        ],
        "tech": ["RDKit", "MoleculeNet", "PVD", "Force fields"],
        "link": "/projects/moleculenet-3d-structure-study/",
    },
    {
        "role": "Research Assistant — Neuroimaging and computer vision",
        "org": "School of AI, Sharif University of Technology",
        "period": "July 2024 – January 2025", "color": "green",
        "bullets": [
            "Machine-learning and deep-learning models for mental-state estimation from fMRI data, exploring functional connectivity analysis and graph neural networks.",
        ],
        "tech": ["fMRI", "Graph neural networks", "Functional connectivity"],
    },
]

PUBLICATIONS = [
    {
        "title": "From Predictive Maintenance to Prescriptive: A Survey of Retrieval-Augmented Generation-Driven Systems for End-to-End Maintenance Decision-Making",
        "status": "Submitted to a Q1 journal, under review, 2026.",
    }
]

SKILLS = [
    ("Programming and software engineering", "peach", ["Python", "Java", "SQL", "FastAPI", "REST APIs", "Object-oriented programming", "Git", "Linux"]),
    ("Machine learning and deep learning", "lav", ["scikit-learn", "PyTorch", "TensorFlow", "Neural networks", "CNNs", "RNNs", "LSTM", "Transformers", "Transfer learning", "GANs", "Diffusion models", "Model evaluation"]),
    ("LLMs and generative AI", "sky", ["Large language models", "Prompt engineering", "Retrieval-augmented generation (RAG)", "Hugging Face Transformers"]),
    ("Computer vision", "pink", ["OpenCV", "Image processing", "Object detection", "Object tracking", "YOLO", "Medical image analysis"]),
    ("Data engineering and analytics", "butter", ["pandas", "NumPy", "SciPy", "Data processing", "Data cleaning", "Data validation", "Power BI"]),
    ("Backend, databases and deployment", "green", ["PostgreSQL", "SQLAlchemy", "Redis", "Docker", "Docker Compose", "Streamlit"]),
    ("AI research", "lav", ["Contrastive learning", "Explainable AI (XAI)", "Graph neural networks", "Physics-informed neural networks"]),
]

EDUCATION = [
    {"title": "B.Sc. in Computer Engineering", "org": "Science and Research University, Tehran", "period": "September 2022 – September 2026", "color": "peach",
     "text": "Bachelor thesis: explainable deep learning for facial skin-lesion classification."},
    {"title": "Academic coursework (auditing student)", "org": "Sharif University of Technology, Tehran", "period": "alongside the degree", "color": "lav",
     "text": "Audited advanced AI and machine-learning courses."},
    {"title": "Associate degree in Mathematical Physics", "org": "Sampad Tizhooshan Farzanegan 2, Ahwaz", "period": "September 2019 – June 2022", "color": "green",
     "text": ""},
]

ABOUT_PARAGRAPHS = [
    "I am a Computer Engineering graduate and AI software engineer. What I enjoy most is the whole path of a project: understanding messy data, building a model, wrapping it in software that other people can use, and then checking honestly whether it works.",
    "My research and engineering work covers Transformers and large language models, computer vision, speech processing and applied machine learning. In research I have worked on predictive maintenance for industrial systems (a manuscript is under review at a Q1 journal), on computer vision for quadcopters and on neuroimaging with graph neural networks. In engineering I have built a data labeling platform, a Persian voice-report assistant and an asynchronous Telegram service platform.",
    "I care about evaluation that does not flatter the model: leakage checks, held-out test sets, baselines and error analysis. Several of my projects document exactly where a first, higher score turned out to be wrong.",
]
