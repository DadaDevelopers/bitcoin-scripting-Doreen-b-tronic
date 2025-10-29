[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/1neRm4kC)
# assignment-4
Bitcoin Scripting


Assignment A

Given this script:

OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG

Tasks:

Break down each opcode's purpose

Create a diagram showing data flow

Identify what happens if signature verification fails

Explain the security benefits of hash verification



Assignment B

Implement a Hashed Time-Lock Contract for atomic swap between Alice and Bob:

Alice can claim with secret preimage within 21 minutes

Bob gets refund after 21 minutes

Tasks:

Complete the HTLC script

Create claiming transaction script

Create refund transaction script

Test with sample hash and timeout
