"""
database/crud.py
Generic CRUD operations for all MongoDB collections.
Provides a consistent interface for all database operations.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from pymongo.collection import Collection
from database.connection import get_collection


def to_object_id(id_str: str) -> Optional[ObjectId]:
    """Convert string to ObjectId, returns None if invalid."""
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError):
        return None


def serialize_doc(doc: Optional[Dict]) -> Optional[Dict]:
    """Convert MongoDB document to JSON-serializable dict."""
    if doc is None:
        return None
    result = {}
    for key, value in doc.items():
        if key == "_id":
            result["id"] = str(value)
        elif isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, list):
            result[key] = [serialize_doc(v) if isinstance(v, dict) else v for v in value]
        elif isinstance(value, dict):
            result[key] = serialize_doc(value)
        else:
            result[key] = value
    return result


def serialize_docs(docs: List[Dict]) -> List[Dict]:
    """Serialize a list of documents."""
    return [serialize_doc(doc) for doc in docs]


# ==========================================
# Generic CRUD Functions
# ==========================================

def create_one(collection_name: str, data: Dict) -> Dict:
    """Insert a single document and return it with its ID."""
    col = get_collection(collection_name)
    now = datetime.utcnow()
    data.setdefault("created_at", now)
    data.setdefault("updated_at", now)
    result = col.insert_one(data)
    data["_id"] = result.inserted_id
    return serialize_doc(data)


def find_one(collection_name: str, query: Dict, projection: Optional[Dict] = None) -> Optional[Dict]:
    """Find a single document matching the query."""
    col = get_collection(collection_name)
    doc = col.find_one(query, projection)
    return serialize_doc(doc)


def find_by_id(collection_name: str, doc_id: str) -> Optional[Dict]:
    """Find a document by its string ID."""
    oid = to_object_id(doc_id)
    if oid is None:
        return None
    return find_one(collection_name, {"_id": oid})


def find_many(
    collection_name: str,
    query: Dict,
    projection: Optional[Dict] = None,
    sort: Optional[List[Tuple]] = None,
    skip: int = 0,
    limit: int = 20
) -> List[Dict]:
    """Find multiple documents with optional sorting and pagination."""
    col = get_collection(collection_name)
    cursor = col.find(query, projection)
    if sort:
        cursor = cursor.sort(sort)
    if skip:
        cursor = cursor.skip(skip)
    if limit:
        cursor = cursor.limit(limit)
    return serialize_docs(list(cursor))


def count_documents(collection_name: str, query: Dict) -> int:
    """Count documents matching a query."""
    col = get_collection(collection_name)
    return col.count_documents(query)


def update_one(collection_name: str, query: Dict, update_data: Dict, upsert: bool = False) -> Optional[Dict]:
    """Update a single document and return the updated version."""
    col = get_collection(collection_name)
    update_data["updated_at"] = datetime.utcnow()
    result = col.find_one_and_update(
        query,
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
        upsert=upsert
    )
    return serialize_doc(result)


def update_by_id(collection_name: str, doc_id: str, update_data: Dict) -> Optional[Dict]:
    """Update a document by its string ID."""
    oid = to_object_id(doc_id)
    if oid is None:
        return None
    return update_one(collection_name, {"_id": oid}, update_data)


def delete_one(collection_name: str, query: Dict) -> bool:
    """Delete a single document. Returns True if deleted."""
    col = get_collection(collection_name)
    result = col.delete_one(query)
    return result.deleted_count > 0


def delete_by_id(collection_name: str, doc_id: str) -> bool:
    """Delete a document by its string ID."""
    oid = to_object_id(doc_id)
    if oid is None:
        return False
    return delete_one(collection_name, {"_id": oid})


def aggregate(collection_name: str, pipeline: List[Dict]) -> List[Dict]:
    """Run an aggregation pipeline on a collection."""
    col = get_collection(collection_name)
    return serialize_docs(list(col.aggregate(pipeline)))


def bulk_insert(collection_name: str, documents: List[Dict]) -> List[str]:
    """Insert multiple documents and return their IDs."""
    col = get_collection(collection_name)
    now = datetime.utcnow()
    for doc in documents:
        doc.setdefault("created_at", now)
        doc.setdefault("updated_at", now)
    result = col.insert_many(documents)
    return [str(oid) for oid in result.inserted_ids]


# ==========================================
# Collection-Specific Helpers
# ==========================================

def find_user_by_email(email: str) -> Optional[Dict]:
    """Find a user by email, including password hash."""
    col = get_collection("users")
    doc = col.find_one({"email": email.lower().strip()})
    return serialize_doc(doc)


def find_user_by_id(user_id: str) -> Optional[Dict]:
    """Find user by ID without password hash."""
    oid = to_object_id(user_id)
    if not oid:
        return None
    col = get_collection("users")
    doc = col.find_one({"_id": oid}, {"password_hash": 0})
    return serialize_doc(doc)


def get_user_resumes(user_id: str, skip: int = 0, limit: int = 10) -> Tuple[List[Dict], int]:
    """Get paginated list of resumes for a user."""
    oid = to_object_id(user_id)
    if not oid:
        return [], 0
    query = {"user_id": oid}
    total = count_documents("resumes", query)
    resumes = find_many(
        "resumes", query,
        sort=[("created_at", -1)],
        skip=skip, limit=limit
    )
    return resumes, total


def get_resume_with_analysis(resume_id: str) -> Dict:
    """Get a resume along with its analysis data."""
    oid = to_object_id(resume_id)
    if not oid:
        return {}
    pipeline = [
        {"$match": {"_id": oid}},
        {
            "$lookup": {
                "from": "analysis",
                "localField": "_id",
                "foreignField": "resume_id",
                "as": "analysis"
            }
        },
        {
            "$lookup": {
                "from": "career_prediction",
                "localField": "_id",
                "foreignField": "resume_id",
                "as": "career_prediction"
            }
        },
        {
            "$addFields": {
                "analysis": {"$arrayElemAt": ["$analysis", 0]},
                "career_prediction": {"$arrayElemAt": ["$career_prediction", 0]}
            }
        }
    ]
    results = aggregate("resumes", pipeline)
    return results[0] if results else {}
