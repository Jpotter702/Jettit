#!/usr/bin/env python3
"""
Test script for Phase 2: Data Collection & Storage
Tests RedditHarbor integration and database storage functionality.
"""

import asyncio
import os
from dotenv import load_dotenv
from services.reddit_collector import reddit_collector

# Load environment variables
load_dotenv()

async def test_phase2_integration():
    """Test the Phase 2 implementation."""
    
    print("🧪 Testing Phase 2: Data Collection & Storage...")
    
    # Check if Reddit credentials are available
    if not os.getenv("REDDIT_CLIENT_ID") or not os.getenv("REDDIT_CLIENT_SECRET"):
        print("⚠️  Reddit credentials not found in environment variables.")
        print("   Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in your .env file.")
        print("   Skipping RedditHarbor integration test.")
        return
    
    print("✅ Reddit credentials found.")
    
    # Test 1: Start a collection job
    print("\n1. Testing RedditHarbor collection job...")
    try:
        result = await reddit_collector.start_collection_job(
            subreddit="programming",
            sort_type="hot",
            post_limit=5,  # Small limit for testing
            include_comments=True,
            anonymize_users=True
        )
        
        print(f"   ✅ Job created: {result}")
        job_id = result["job_id"]
        
    except Exception as e:
        print(f"   ❌ Job creation failed: {e}")
        return
    
    # Test 2: Check job status
    print("\n2. Testing job status tracking...")
    try:
        status = await reddit_collector.get_job_status(job_id)
        print(f"   ✅ Job status: {status['status']}")
        print(f"   📊 Progress: {status.get('progress', 0)}%")
        print(f"   📈 Collected: {status.get('collected_posts', 0)}/{status.get('total_posts', 0)} posts")
        
    except Exception as e:
        print(f"   ❌ Status check failed: {e}")
    
    # Test 3: Wait for completion and check data
    print("\n3. Waiting for collection to complete...")
    max_wait = 60  # Wait up to 60 seconds
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            status = await reddit_collector.get_job_status(job_id)
            if status["status"] == "completed":
                print("   ✅ Collection completed!")
                break
            elif status["status"] == "failed":
                print(f"   ❌ Collection failed: {status.get('error_message', 'Unknown error')}")
                break
            else:
                print(f"   ⏳ Status: {status['status']}, Progress: {status.get('progress', 0)}%")
                await asyncio.sleep(5)  # Wait 5 seconds before checking again
                wait_time += 5
        except Exception as e:
            print(f"   ❌ Status check failed: {e}")
            break
    
    # Test 4: Retrieve collected data
    print("\n4. Testing data retrieval...")
    try:
        data = await reddit_collector.get_collected_data(job_id=job_id)
        print(f"   ✅ Retrieved {len(data['data'])} submissions")
        print(f"   📊 Total available: {data['total']}")
        
        if data['data']:
            print("   📝 Sample submission:")
            sample = data['data'][0]
            print(f"      Title: {sample['title'][:50]}...")
            print(f"      Score: {sample['score']}")
            print(f"      Author: {sample['author'] or 'Anonymous'}")
        
    except Exception as e:
        print(f"   ❌ Data retrieval failed: {e}")
    
    print("\n🎉 Phase 2 testing completed!")
    
    # Test 5: List jobs
    print("\n5. Testing job listing...")
    try:
        jobs = await reddit_collector.list_jobs(limit=5)
        print(f"   ✅ Retrieved {len(jobs['jobs'])} jobs")
        print(f"   📊 Total jobs: {jobs['total']}")
        
        if jobs['jobs']:
            print("   📝 Sample job:")
            sample_job = jobs['jobs'][0]
            print(f"      Subreddit: r/{sample_job['subreddit']}")
            print(f"      Status: {sample_job['status']}")
            print(f"      Progress: {sample_job['progress']}%")
        
    except Exception as e:
        print(f"   ❌ Job listing failed: {e}")
    
    # Test 6: Get statistics
    print("\n6. Testing statistics...")
    try:
        stats = await reddit_collector.get_job_statistics()
        print(f"   ✅ Retrieved statistics")
        print(f"   📊 Total jobs: {stats['jobs']['total']}")
        print(f"   📈 Total submissions: {stats['data']['total_submissions']}")
        print(f"   💬 Total comments: {stats['data']['total_comments']}")
        
        if stats['top_subreddits']:
            print("   🏆 Top subreddits:")
            for subreddit in stats['top_subreddits'][:3]:
                print(f"      r/{subreddit['subreddit']}: {subreddit['job_count']} jobs")
        
    except Exception as e:
        print(f"   ❌ Statistics failed: {e}")
    
    print("\n🎉 Enhanced Phase 2 testing completed!")

if __name__ == "__main__":
    asyncio.run(test_phase2_integration()) 