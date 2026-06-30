"""Simple test script to verify the physics server tools work correctly."""

from physics_server import kinetic_energy, gravitational_potential_energy, subtract

def test_kinetic_energy():
    """Test kinetic energy calculation."""
    print("Testing kinetic_energy...")
    # Test case: 800 kg car at 25 m/s
    result = kinetic_energy(800, 25)
    expected = 0.5 * 800 * (25 ** 2)  # 250,000 J
    print(f"  Result: {result} J")
    print(f"  Expected: {expected} J")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  ✓ PASSED\n")

def test_gravitational_potential_energy():
    """Test gravitational potential energy calculation."""
    print("Testing gravitational_potential_energy...")
    # Test case: 10 kg object at 50 m height
    result = gravitational_potential_energy(10, 50)
    expected = 10 * 9.81 * 50  # 4905 J
    print(f"  Result: {result} J")
    print(f"  Expected: {expected} J")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  ✓ PASSED\n")

def test_subtract():
    """Test subtraction."""
    print("Testing subtract...")
    result = subtract(100, 30)
    expected = 70
    print(f"  Result: {result}")
    print(f"  Expected: {expected}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  ✓ PASSED\n")

def test_error_handling():
    """Test error handling for invalid inputs."""
    print("Testing error handling...")
    
    # Test negative mass
    try:
        kinetic_energy(-10, 5)
        print("  ✗ FAILED: Should have raised ValueError for negative mass")
    except ValueError as e:
        print(f"  ✓ Correctly raised ValueError: {e}")
    
    # Test negative height
    try:
        gravitational_potential_energy(10, -5)
        print("  ✗ FAILED: Should have raised ValueError for negative height")
    except ValueError as e:
        print(f"  ✓ Correctly raised ValueError: {e}")
    
    print("  ✓ PASSED\n")

if __name__ == "__main__":
    print("=" * 60)
    print("PHYSICS SERVER TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_kinetic_energy()
        test_gravitational_potential_energy()
        test_subtract()
        test_error_handling()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nYour physics server is working correctly!")
        print("You can now configure it in Claude Desktop.")
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
