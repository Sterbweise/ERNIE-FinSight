"""
Simple test script to verify the API is working correctly
Usage: python test_api.py
"""

import requests
import time
import sys

API_BASE = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/health")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Health check passed: {data}")
        
        if not data.get("ernie_configured"):
            print("⚠ Warning: ERNIE is not configured. Check your NOVITA_API_KEY in .env")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_upload(pdf_path=None):
    """Test file upload endpoint"""
    if not pdf_path:
        print("\nSkipping upload test (no PDF file provided)")
        print("To test upload, run: python test_api.py path/to/whitepaper.pdf")
        return True
    
    print(f"\nTesting file upload with: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': (pdf_path, f, 'application/pdf')}
            response = requests.post(f"{API_BASE}/api/upload", files=files)
            response.raise_for_status()
            data = response.json()
            print(f"✓ Upload successful: {data}")
            
            task_id = data.get('task_id')
            if task_id:
                return test_status_and_result(task_id)
            
            return True
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return False

def test_status_and_result(task_id):
    """Test status and result endpoints"""
    print(f"\nTesting status endpoint for task: {task_id}")
    
    max_attempts = 60  # Wait up to 2 minutes
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get(f"{API_BASE}/api/status/{task_id}")
            response.raise_for_status()
            data = response.json()
            
            status = data.get('status')
            progress = data.get('progress', 0)
            
            print(f"  Status: {status} ({progress}%)")
            
            if status == 'completed':
                print("✓ Processing completed!")
                return test_result(task_id)
            elif status == 'failed':
                print(f"✗ Processing failed: {data.get('message')}")
                return False
            
            time.sleep(2)
            attempt += 1
            
        except Exception as e:
            print(f"✗ Status check failed: {e}")
            return False
    
    print("✗ Timeout waiting for processing to complete")
    return False

def test_result(task_id):
    """Test result endpoint"""
    print(f"\nTesting result endpoint for task: {task_id}")
    try:
        response = requests.get(f"{API_BASE}/api/result/{task_id}")
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'completed' and data.get('result'):
            result = data['result']
            print("✓ Result retrieved successfully!")
            print(f"\n  Project Name: {result.get('project_name')}")
            print(f"  Executive Summary: {result.get('executive_summary', '')[:100]}...")
            print(f"  Value Props: {len(result.get('key_value_propositions', []))}")
            print(f"  Use Cases: {len(result.get('use_cases', []))}")
            print(f"  Risk Factors: {len(result.get('risk_factors', []))}")
            return True
        else:
            print(f"✗ No result available: {data}")
            return False
            
    except Exception as e:
        print(f"✗ Result retrieval failed: {e}")
        return False

def main():
    print("=" * 60)
    print("  ERNIE FinSight API Test")
    print("=" * 60)
    print()
    
    # Test health
    if not test_health():
        print("\n❌ Health check failed. Make sure:")
        print("  1. Backend server is running (python main.py)")
        print("  2. NOVITA_API_KEY is set in backend/.env")
        sys.exit(1)
    
    # Test upload if PDF provided
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not test_upload(pdf_path):
        print("\n❌ Upload test failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("  ✓ All tests passed!")
    print("=" * 60)

if __name__ == "__main__":
    main()

