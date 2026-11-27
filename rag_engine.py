"""
EcoPantry AI - Retrieval-Augmented Generation (RAG) Engine
Integrates vector retrieval, document chunking, and similarity search
over authoritative food safety, shelf-life, and zero-waste culinary databases.

Resilient architecture: Uses scikit-learn when available, with an automatic
zero-dependency pure-Python TF-IDF vector engine fallback.
"""
import os
import re
import math
from collections import Counter
from typing import List, Dict, Any

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Authoritative Grounding Knowledge Base
DEFAULT_KNOWLEDGE_BASE = [
    {
        "id": "USDA_001",
        "title": "USDA Food Safety - Danger Zone & Bacterial Growth",
        "category": "Food Safety",
        "source": "USDA FSIS Guidelines",
        "content": (
            "The Temperature Danger Zone is between 40°F (4.4°C) and 140°F (60°C). "
            "Bacteria grow most rapidly in this range, doubling in number in as little as 20 minutes. "
            "Perishable food should never be left at room temperature for more than 2 hours (or 1 hour if the temperature is above 90°F / 32°C). "
            "Reheating food to boiling cannot neutralize heat-stable enterotoxins produced by Staphylococcus aureus or emetic toxins from Bacillus cereus. "
            "If perishable food was left out overnight, it must be discarded immediately."
        )
    },
    {
        "id": "USDA_002",
        "title": "USDA FoodKeeper - Refrigerated Shelf-Life of Meats & Poultry",
        "category": "Shelf Life",
        "source": "USDA FoodKeeper Database",
        "content": (
            "Cooked poultry, pork, beef, and stews remain safe in the refrigerator (at or below 40°F / 4°C) for 3 to 4 days. "
            "Raw ground meats and poultry must be cooked or frozen within 1 to 2 days of purchase. "
            "Freezing at 0°F (-18°C) keeps food safe indefinitely by arresting bacterial reproduction, though quality and texture are best preserved when consumed within 3 to 6 months."
        )
    },
    {
        "id": "USDA_003",
        "title": "Dairy, Eggs, and Cheese Preservation Standards",
        "category": "Shelf Life",
        "source": "USDA / FDA Regulatory Guide",
        "content": (
            "Raw whole eggs in their shell can be stored in the refrigerator for 3 to 5 weeks past purchase. "
            "Hard cheeses (Cheddar, Parmesan) can safely be preserved for 3 to 4 weeks after opening; surface mold on hard cheese may be cut off with a 1-inch perimeter around and below the mold. "
            "Soft cheeses (ricotta, cream cheese, cottage cheese) and yogurt contaminated with mold must be discarded completely due to root hyphae penetration."
        )
    },
    {
        "id": "SCRAP_001",
        "title": "Zero-Waste Allium & Vegetable Stock Extraction",
        "category": "Zero-Waste Cooking",
        "source": "Sustainable Kitchen Codex",
        "content": (
            "Vegetable scraps including onion skins, leek greens, garlic trimmings, carrot peels, and herb stems can be accumulated in a freezer bag. "
            "When full, simmer scraps with water, whole peppercorns, and bay leaves for 45 to 60 minutes to extract a nutrient-dense, golden vegetable stock. "
            "Avoid adding brassicas (broccoli, cabbage, cauliflower) as prolonged simmering creates bitter sulfurous off-notes."
        )
    },
    {
        "id": "SCRAP_002",
        "title": "Stale Bread and Herb Preservation Techniques",
        "category": "Zero-Waste Cooking",
        "source": "Culinary Science Handbook",
        "content": (
            "Stale bread is preserved by dehydrating into artisan garlic croutons or pulsing into fine breadcrumbs stored in an airtight freezer jar. "
            "Wilting leafy herbs (parsley, cilantro, dill, basil) can be finely minced and frozen inside olive oil trays, preventing enzymatic oxidation and browning. "
            "Alternatively, blend wilting herbs with oil, garlic, and vinegar to create chimichurri or herbaceous pestos."
        )
    },
    {
        "id": "CHEM_001",
        "title": "Chemistry-Safe Culinary Substitutions",
        "category": "Substitutions",
        "source": "Food Chemistry & Culinary Ratios",
        "content": (
            "Buttermilk substitute: Combine 1 cup whole milk with 1 tablespoon lemon juice or white vinegar; let rest 5 minutes for lactic curdling. "
            "Egg substitute in baking: Replace 1 egg with 1/4 cup unsweetened applesauce, 1/2 mashed ripe banana, or 1 tbsp ground flaxseed mixed with 3 tbsp water. "
            "Heavy cream substitute for sauces: Whisk 3/4 cup milk with 1/4 cup melted unsalted butter. "
            "Cornstarch substitute for thickening: Use 2 tablespoons of all-purpose flour per 1 tablespoon of cornstarch, simmering for 2 minutes to cook out raw starch flavor."
        )
    }
]

# =====================================================================
# Pure-Python TF-IDF Engine Fallback (Zero-Dependency)
# =====================================================================
STOPWORDS = {
    'the', 'and', 'is', 'in', 'it', 'to', 'of', 'for', 'with', 'on', 'at', 
    'by', 'from', 'an', 'be', 'this', 'that', 'or', 'as', 'are', 'was', 
    'can', 'if', 'not', 'but', 'into', 'when', 'all', 'more', 'than'
}

def _tokenize(text: str) -> List[str]:
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    return [w for w in words if w not in STOPWORDS]

class PurePythonTfidfEngine:
    def __init__(self):
        self.doc_vectors = []
        self.idf = {}

    def fit_transform(self, corpus: List[str]):
        tokenized_docs = [_tokenize(doc) for doc in corpus]
        N = len(tokenized_docs)
        
        # Calculate Document Frequency
        df = Counter()
        for doc in tokenized_docs:
            for word in set(doc):
                df[word] += 1
                
        # Calculate Smooth IDF: log(1 + N / (1 + df)) + 1
        self.idf = {word: math.log(1.0 + (N / (1.0 + freq))) + 1.0 for word, freq in df.items()}
        
        # Compute Document TF-IDF vectors
        self.doc_vectors = [self._vectorize(doc) for doc in tokenized_docs]

    def _vectorize(self, tokens: List[str]) -> Dict[str, float]:
        if not tokens:
            return {}
        tf = Counter(tokens)
        total = len(tokens)
        vec = {word: (count / total) * self.idf.get(word, 1.0) for word, count in tf.items()}
        # Normalize L2
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm > 0:
            vec = {k: v / norm for k, v in vec.items()}
        return vec

    def compute_similarity(self, query: str) -> List[float]:
        q_vec = self._vectorize(_tokenize(query))
        if not q_vec:
            return [0.0] * len(self.doc_vectors)
        
        scores = []
        for d_vec in self.doc_vectors:
            # Dot product of normalized vectors = Cosine Similarity
            score = sum(q_vec[term] * d_vec[term] for term in q_vec if term in d_vec)
            scores.append(score)
        return scores

# =====================================================================
# Main RAG Engine
# =====================================================================
class RAGEngine:
    def __init__(self):
        self.documents = list(DEFAULT_KNOWLEDGE_BASE)
        self.sklearn_active = SKLEARN_AVAILABLE
        if self.sklearn_active:
            self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            self.tfidf_matrix = None
        else:
            self.pure_engine = PurePythonTfidfEngine()
        self._rebuild_index()

    def _rebuild_index(self):
        """Builds or refreshes the vector index over the document corpus."""
        corpus = [f"{doc['title']} {doc['category']} {doc['content']}" for doc in self.documents]
        if self.sklearn_active:
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        else:
            self.pure_engine.fit_transform(corpus)

    def add_custom_document(self, title: str, content: str, category: str = "User Document", source: str = "Uploaded File") -> str:
        """Chunks and indexes an uploaded user document into the vector database."""
        chunks = [c.strip() for c in re.split(r'\n\s*\n', content) if len(c.strip()) > 40]
        if not chunks:
            chunks = [content.strip()]
        
        added_ids = []
        for i, chunk in enumerate(chunks):
            doc_id = f"USER_{len(self.documents) + 1}_{i}"
            doc_entry = {
                "id": doc_id,
                "title": f"{title} (Part {i+1})",
                "category": category,
                "source": source,
                "content": chunk
            }
            self.documents.append(doc_entry)
            added_ids.append(doc_id)

        self._rebuild_index()
        return f"Successfully indexed {len(chunks)} knowledge chunk(s) from '{title}'."

    def retrieve(self, query: str, top_k: int = 2, threshold: float = 0.05) -> List[Dict[str, Any]]:
        """
        Executes semantic cosine similarity vector search.
        Returns top-k matching documents passing relevance threshold.
        """
        if self.sklearn_active:
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            top_indices = np.argsort(similarities)[::-1]
        else:
            similarities = self.pure_engine.compute_similarity(query)
            top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= threshold and len(results) < top_k:
                matched_doc = dict(self.documents[idx])
                matched_doc["relevance_score"] = round(score, 3)
                results.append(matched_doc)
                
        return results

    def format_retrieval_context(self, query: str, top_k: int = 2) -> tuple[str, List[Dict[str, Any]]]:
        """
        Retrieves top documents and formats them into an authoritative context block
        for direct grounding into the LLM prompt.
        """
        retrieved_docs = self.retrieve(query, top_k=top_k)
        if not retrieved_docs:
            return "", []

        context_lines = ["[AUTHORITATIVE RETRIEVED KNOWLEDGE - RAG CONTEXT]:"]
        for i, doc in enumerate(retrieved_docs, start=1):
            context_lines.append(
                f"--- Source [{i}]: {doc['title']} (Source: {doc['source']}, Score: {doc['relevance_score']}) ---\n"
                f"{doc['content']}\n"
            )
        context_lines.append("[MANDATE]: Ground your answer strictly on the facts from the retrieved sources above whenever applicable.\n")
        return "\n".join(context_lines), retrieved_docs
