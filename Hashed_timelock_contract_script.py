import hashlib
import time

# -----------------------------
# 1. Complete HTLC Script (Locking Logic)
# -----------------------------
class HTLC:
    def __init__(self, secret_hash, alice_key, bob_key, timeout_seconds):
        self.secret_hash = secret_hash
        self.alice_key = alice_key
        self.bob_key = bob_key
        self.timeout = time.time() + timeout_seconds
        self.funded = False
        self.claimed_by = None

    def fund(self):
        self.funded = True
        print("HTLC funded by Bob")

# -----------------------------
# 2. Claiming Transaction Script (Alice Branch)
# -----------------------------
def claim(htlc, secret, alice_signature):
    if not htlc.funded:
        print("Contract not funded yet")
        return False

    # Verify secret preimage
    h160 = hashlib.new('ripemd160', hashlib.sha256(secret.encode()).digest()).hexdigest()
    if h160 != htlc.secret_hash:
        print("Secret preimage does not match expected hash")
        return False

    # Verify "signature"
    if alice_signature != htlc.alice_key:
        print("Invalid Alice signature")
        return False

    # Check timeout
    if time.time() > htlc.timeout:
        print("Timeout elapsed: Alice cannot claim, Bob can refund")
        return False

    htlc.claimed_by = "Alice"
    print("Alice successfully claimed the funds!")
    return True

# -----------------------------
# 3. Refund Transaction Script (Bob Branch)
# -----------------------------
def refund(htlc, bob_signature):
    if not htlc.funded:
        print("Contract not funded yet")
        return False

    # Check timeout
    if time.time() < htlc.timeout:
        print("Timeout not reached yet: Bob cannot refund")
        return False

    # Verify "signature"
    if bob_signature != htlc.bob_key:
        print("Invalid Bob signature")
        return False

    htlc.claimed_by = "Bob"
    print("Bob refunded the funds!")
    return True

# -----------------------------
# 4. Test Simulation
# -----------------------------
if __name__ == "__main__":
    # Alice/Bob keys (simplified)
    alice_key = "AliceSecretKey"
    bob_key = "BobSecretKey"

    # Secret and its hash
    secret = "mysecret123"
    secret_hash = hashlib.new('ripemd160', hashlib.sha256(secret.encode()).digest()).hexdigest()
    print("HASH160(secret):", secret_hash)

    # Timeout: 21 minutes = 1260 seconds
    timeout_seconds = 1260
    htlc = HTLC(secret_hash, alice_key, bob_key, timeout_seconds)
    htlc.fund()

    # -----------------------------
    # Simulate Alice interaction
    alice_provides_secret = True   # Change to False to simulate no secret

    if alice_provides_secret:
        print("\nAlice provides a secret preimage...")
        alice_secret_input = "mysecret123"  # Change to test wrong preimage
        success = claim(htlc, alice_secret_input, alice_key)

        if not success:
            print("Alice could not claim the funds, waiting for timeout for Bob refund...")
            # Simulate 21 minutes elapsed
            htlc.timeout = time.time() - 1
            refund(htlc, bob_key)

    else:
        print("\nAlice does not provide the secret preimage. Waiting for timeout for Bob...")
        # Simulate 21 minutes elapsed
        htlc.timeout = time.time() - 1
        refund(htlc, bob_key)

    # -----------------------------
    # Final state
    print("\n=== Final state ===")
    if htlc.claimed_by:
        print(f"Funds claimed by: {htlc.claimed_by}")
    else:
        print("Funds are still locked")

