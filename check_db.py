"""
Script to check Firebase database connection and list collections
"""

import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase service account key
CREDENTIALS_PATH = 'hospital-web-assist-firebase-adminsdk-fbsvc-2b1b4cd8dd.json'

def check_database():
    """Check Firebase connection and list collections"""

    try:
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            print("✓ Firebase initialized successfully")

        # Get Firestore client
        db = firestore.client()
        print("✓ Firestore client created successfully")

        # Try to list collections
        print("\n--- Checking Collections ---")
        collections = db.collections()
        collection_names = []

        for collection in collections:
            collection_names.append(collection.id)
            print(f"  Found collection: {collection.id}")

        if not collection_names:
            print("  No collections found in database")
        else:
            print(f"  Total collections: {len(collection_names)}")

        # Check if 'testing' collection exists
        testing_ref = db.collection('testing')
        docs = testing_ref.stream()

        doc_count = 0
        print("\n--- Checking 'testing' collection ---")
        for doc in docs:
            doc_count += 1
            data = doc.to_dict()
            print(f"  Document ID: {doc.id}")
            print(f"  Data: {data}")
            print("  ---")

        if doc_count == 0:
            print("  No documents found in 'testing' collection")
        else:
            print(f"  Total documents in 'testing': {doc_count}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        print(f"  Type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = check_database()
    if success:
        print("\n✅ Database check completed successfully!")
    else:
        print("\n❌ Database check failed!")
        exit(1)