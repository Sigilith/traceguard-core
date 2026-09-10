from boundary_reference_implementation import run_conformance_suite, BRI_MANIFEST

if __name__ == "__main__":
    run_conformance_suite()
    print(f"[*] BRI Manifest Loaded: {BRI_MANIFEST['name']} v{BRI_MANIFEST['version']}")
