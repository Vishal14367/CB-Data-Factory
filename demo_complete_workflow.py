"""
Demo script to test complete E2E workflow (Phases 1-5).

This script demonstrates the full Codebasics Data Factory pipeline:
1. Research & Problem Statement
2. Schema Generation & Validation
3. Preview Generation
4. Full Generation with Reports
5. Download Package

Usage:
    python demo_complete_workflow.py
"""

import requests
import time
import json
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000"
OUTPUT_DIR = Path("demo_output")
OUTPUT_DIR.mkdir(exist_ok=True)


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_status(message, success=True):
    """Print status message with indicator."""
    symbol = "✓" if success else "✗"
    print(f"{symbol} {message}")


def wait_for_completion(session_id, endpoint, status_field="status",
                       target_status="completed", max_wait=300):
    """Poll endpoint until completion or timeout."""
    start_time = time.time()
    last_message = ""

    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                data = response.json()

                # Check for progress updates
                if "progress" in data:
                    progress = data["progress"]
                    message = f"{progress.get('stage', 'unknown')}: {progress.get('message', '')}"
                    if message != last_message:
                        print(f"   {progress.get('percent', 0):.0f}% - {message}")
                        last_message = message

                # Check completion
                status = data.get(status_field)
                if status == target_status:
                    return data
                elif status == "failed":
                    print_status(f"Failed: {data.get('error', 'Unknown error')}", False)
                    return None

        except Exception as e:
            print(f"   Error polling: {e}")

        time.sleep(2)

    print_status(f"Timeout waiting for {target_status}", False)
    return None


def demo_complete_workflow():
    """Run complete E2E workflow demonstration."""

    print_section("CODEBASICS DATA FACTORY - COMPLETE E2E WORKFLOW DEMO")

    session_id = None

    try:
        # ============================================================================
        # PHASE 1: RESEARCH & PROBLEM STATEMENT
        # ============================================================================

        print_section("PHASE 1: Research & Problem Statement")

        # 1A: Conduct Research
        print("Step 1A: Conducting domain research...")

        input_data = {
            "domain": "E-commerce",
            "function": "Customer Analytics",
            "problem_statement": "An online retail company wants to analyze customer behavior, purchase patterns, and retention rates to improve marketing strategies and customer lifetime value.",
            "skill_level": "Intermediate",
            "dataset_size": 5000,
            "data_structure": "Normalized",
            "primary_questions": "What are the key customer segments? How do purchase patterns vary by region? What factors influence customer retention?"
        }

        response = requests.post(f"{BASE_URL}/api/challenge/phase1/research", json=input_data)

        if response.status_code == 200:
            data = response.json()
            session_id = data["session_id"]
            print_status(f"Research completed - Session ID: {session_id}")
            print(f"   Found {len(data['research']['sources'])} sources")
            print(f"   Identified {len(data['research']['identified_kpis'])} KPIs")
        else:
            print_status("Research failed", False)
            return

        time.sleep(1)

        # 1B: Generate Problem Statement
        print("\nStep 1B: Generating problem statement with brand characters...")

        response = requests.post(
            f"{BASE_URL}/api/challenge/phase1/generate-problem",
            params={"session_id": session_id},
            json=input_data
        )

        if response.status_code == 200:
            data = response.json()
            problem = data["problem_statement"]
            print_status("Problem statement generated")
            print(f"   Title: {problem['title']}")
            print(f"   Company: {problem['company_name']}")
            print(f"   Questions: {len(problem['analytical_questions'])}")

            # Save problem statement
            with open(OUTPUT_DIR / "problem_statement.json", "w") as f:
                json.dump(problem, f, indent=2)
        else:
            print_status("Problem generation failed", False)
            return

        time.sleep(1)

        # 1C: Approve Problem
        print("\nStep 1C: Approving problem statement...")

        response = requests.post(
            f"{BASE_URL}/api/challenge/phase1/approve",
            params={"session_id": session_id}
        )

        if response.status_code == 200:
            print_status("Phase 1 approved - Ready for Phase 2")
        else:
            print_status("Approval failed", False)
            return

        # ============================================================================
        # PHASE 2: SCHEMA GENERATION & VALIDATION
        # ============================================================================

        print_section("PHASE 2: Schema Generation & Validation")

        # 2A: Generate Schema
        print("Step 2A: Generating database schema...")

        response = requests.post(
            f"{BASE_URL}/api/challenge/phase2/generate-schema",
            params={"session_id": session_id}
        )

        if response.status_code == 200:
            data = response.json()
            schema = data["schema"]
            validation = data["validation"]

            print_status(f"Schema generated - Validation Score: {validation['validation_score']:.1f}/10")
            print(f"   Tables: {len(schema['tables'])}")
            print(f"   Relationships: {len(schema['relationships'])}")
            print(f"   Can answer all questions: {validation['can_answer_all']}")

            # Save schema
            with open(OUTPUT_DIR / "schema.json", "w") as f:
                json.dump(schema, f, indent=2)
        else:
            print_status("Schema generation failed", False)
            return

        time.sleep(1)

        # 2B: Approve Schema
        print("\nStep 2B: Approving schema...")

        response = requests.post(
            f"{BASE_URL}/api/challenge/phase2/approve",
            params={"session_id": session_id}
        )

        if response.status_code == 200:
            print_status("Phase 2 approved - Ready for Phase 3")
        else:
            print_status("Approval failed", False)
            return

        # ============================================================================
        # PHASE 3: PREVIEW GENERATION
        # ============================================================================

        print_section("PHASE 3: Preview Generation")

        # 3A: Generate Preview
        print("Step 3A: Generating preview data (30 rows per table)...")

        response = requests.post(
            f"{BASE_URL}/api/challenge/phase3/generate-preview",
            params={"session_id": session_id}
        )

        if response.status_code == 200:
            data = response.json()
            preview_data = data["preview_data"]
            validation = data["validation"]

            print_status(f"Preview generated - Quality Score: {validation['quality_score']:.1f}/10")
            print(f"   FK Integrity: {'Passed' if validation['fk_integrity_passed'] else 'Failed'}")
            print(f"   Tables with preview:")
            for table in preview_data:
                print(f"      - {table['table_name']}: {table['row_count']} rows, {table['column_count']} columns")

            # Save preview
            with open(OUTPUT_DIR / "preview_data.json", "w") as f:
                json.dump(preview_data, f, indent=2)
        else:
            print_status("Preview generation failed", False)
            return

        time.sleep(1)

        # 3B: Approve Preview
        print("\nStep 3B: Approving preview...")

        response = requests.post(
            f"{BASE_URL}/api/challenge/phase3/approve",
            params={"session_id": session_id}
        )

        if response.status_code == 200:
            print_status("Phase 3 approved - Ready for Phase 4")
        else:
            print_status("Approval failed", False)
            return

        # ============================================================================
        # PHASE 4: FULL GENERATION WITH REPORTS
        # ============================================================================

        print_section("PHASE 4: Full Generation with Reports")

        # 4A: Start Full Generation
        print("Step 4A: Starting full dataset generation (5,000 rows)...")

        response = requests.post(
            f"{BASE_URL}/api/challenge/phase4/generate-full",
            params={"session_id": session_id},
            json={"dataset_size": 5000}
        )

        if response.status_code == 200:
            print_status("Full generation started")
            print("   This may take 30-60 seconds...")
            print("   Polling for progress...\n")
        else:
            print_status("Generation start failed", False)
            return

        # 4B: Wait for completion
        result = wait_for_completion(
            session_id,
            f"/api/challenge/phase4/status/{session_id}",
            status_field="status",
            target_status="completed",
            max_wait=300
        )

        if result:
            qa_results = result.get("qa_results", {})
            print_status(f"Generation completed - Quality Score: {qa_results.get('overall_score', 0):.1f}/10")
            print(f"   Status: {qa_results.get('status', 'Unknown')}")
            print(f"   Category Scores:")
            for cat, score in qa_results.get('category_scores', {}).items():
                print(f"      - {cat}: {score:.1f}")
        else:
            print_status("Generation failed or timed out", False)
            return

        # ============================================================================
        # PHASE 5: DOWNLOAD PACKAGE
        # ============================================================================

        print_section("PHASE 5: Download Package")

        # 5A: Prepare Package
        print("Step 5A: Preparing download package...")

        response = requests.get(f"{BASE_URL}/api/challenge/phase5/prepare/{session_id}")

        if response.status_code == 200:
            data = response.json()
            package = data["package"]

            print_status("Package prepared successfully")
            print(f"   CSV files: {len(package['csv_files'])}")
            print(f"   PDF report: {package['pdf_report']}")
            print(f"   Excel report: {package['excel_report']}")
            print(f"   Data dictionary: {package['data_dictionary']}")
            print(f"   README: {package['readme']}")
        else:
            print_status("Package preparation failed", False)
            return

        time.sleep(1)

        # 5B: Download ZIP
        print("\nStep 5B: Downloading complete package...")

        response = requests.get(f"{BASE_URL}/api/challenge/phase5/download/{session_id}")

        if response.status_code == 200:
            output_file = OUTPUT_DIR / f"challenge_{session_id}.zip"
            with open(output_file, "wb") as f:
                f.write(response.content)

            file_size = output_file.stat().st_size / (1024 * 1024)  # MB
            print_status(f"Package downloaded: {output_file}")
            print(f"   File size: {file_size:.2f} MB")
        else:
            print_status("Download failed", False)
            return

        # ============================================================================
        # WORKFLOW COMPLETE
        # ============================================================================

        print_section("WORKFLOW COMPLETE")

        print("✓ All phases completed successfully!")
        print(f"\nSession ID: {session_id}")
        print(f"Output directory: {OUTPUT_DIR.absolute()}")
        print("\nGenerated files:")
        print(f"  - problem_statement.json")
        print(f"  - schema.json")
        print(f"  - preview_data.json")
        print(f"  - challenge_{session_id}.zip")

        # Get comprehensive status
        print("\nFinal session status:")
        response = requests.get(f"{BASE_URL}/api/challenge/session/{session_id}")
        if response.status_code == 200:
            status = response.json()
            print(json.dumps(status["phase_status"], indent=2))

        print("\n" + "=" * 80)
        print("Demo completed successfully!")
        print("=" * 80 + "\n")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("Error: Server is not responding correctly")
            print("Please start the server with: python backend/src/main.py")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server")
        print("Please start the server with: python backend/src/main.py")
        exit(1)

    # Run demo
    demo_complete_workflow()
