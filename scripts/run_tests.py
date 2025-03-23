#!/usr/bin/env python3
"""
Kjører alle tester for Space Invaders-prosjektet.
Dette skriptet kjører testene med coverage-rapportering om tilgjengelig.
"""
import sys
import os
import subprocess

# Finn prosjektmappe
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_dir)

def run_tests_with_coverage():
    """Kjør tester med coverage hvis tilgjengelig"""
    try:
        import coverage
        cov = coverage.Coverage(
            source=['src'],
            omit=[
                '*/test*',
                '*/run_tests.py',
                '*/__pycache__/*',
                '*/__main__.py'
            ]
        )
        cov.start()
        
        # Importer og kjør testene
        from src.run_tests import run_tests
        success = run_tests()
        
        cov.stop()
        cov.save()
        
        print("\nCoverage Rapport:")
        cov.report()
        
        # Generer HTML-rapport
        cov.html_report(directory=os.path.join(project_dir, 'htmlcov'))
        print(f"\nHTML-rapport generert i {os.path.join(project_dir, 'htmlcov')}")
        
        return success
    except ImportError:
        print("Coverage-pakken er ikke installert. Kjører tester uten coverage-rapport.")
        return run_tests_without_coverage()

def run_tests_without_coverage():
    """Kjør tester uten coverage"""
    from src.run_tests import run_tests
    return run_tests()

if __name__ == "__main__":
    print("=" * 70)
    print("Kjører Space Invaders-tester")
    print("=" * 70)
    
    # Sjekk om vi kjører med coverage-flagg
    use_coverage = len(sys.argv) > 1 and sys.argv[1] == '--coverage'
    
    if use_coverage:
        success = run_tests_with_coverage()
    else:
        success = run_tests_without_coverage()
    
    print("\nInformasjon:")
    print("  - For å kjøre med coverage-rapport: python scripts/run_tests.py --coverage")
    print("  - For å installere coverage: pip install coverage")
    
    sys.exit(0 if success else 1) 