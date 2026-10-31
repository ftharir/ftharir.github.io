"""Hand-made Persian pieces: texts that are not whole numbered lines (parts of composite strings),
headline fragments with inline markup (FA_HTML) and technical names that stay in English (KEEP)."""

FA_UI = {
    "Sharif Setup": "شریف ستاپ",
    "LLM service": "سرویس LLM",
    "ML platform": "پلتفرم ML",
    "Speech": "گفتار",
    "Sole author": "نویسنده‌ی تنها",
}

# exact inner HTML of an element -> Persian inner HTML (word order differs, so it is not translated piece by piece)
FA_HTML = {
    "About <em>me</em>": "<em>درباره‌ی</em> من",
    "Professional <em>experience</em>": "<em>تجربه‌ی</em> حرفه‌ای",
    "Research &amp; <em>academic</em> work": "<em>پژوهش</em> و کار علمی",
    "Selected <em>projects</em>": "<em>پروژه‌های</em> منتخب",
    "Technical <em>skills</em>": "<em>مهارت‌های</em> فنی",
    "Let's <em>talk</em>": "<em>بیایید</em> حرف بزنیم",
}

KEEP = {
    "github.com/ftharir", "LinkedIn", "fatemeh.harirforoush04@gmail.com", "Python", "PyTorch", "TensorFlow", "scikit-learn",
    "pandas", "OpenCV", "FastAPI", "PostgreSQL", "Docker", "Git", "LLMs", "Pydantic", "Streamlit", "SQLAlchemy", "YOLOv5",
    "ResNet18", "Grad-CAM", "VoiceLedger", "aiogram", "Docker Compose", "REST APIs", "Redis", "Faster Whisper", "Power BI",
    "SQL", "CNN", "RNN", "GAN", "PINNs", "RAG", "RDKit", "MoleculeNet", "PVD", "fMRI", "pytest", "SVM", "ML", "DL", "XAI",
    "GitHub", "Jupyter", "Alembic", "Bale API", "ONNX", "LabelMe", "CTC loss", "CRNN", "matplotlib", "Excel",
}
