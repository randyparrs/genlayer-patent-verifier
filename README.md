# GenLayer AI Patent Verifier

A decentralized patent originality verifier where AI validators evaluate inventions against the three core requirements of international patent law and search for similar prior art. Built on GenLayer Testnet Bradbury.

## What is this

Before filing a patent application most inventors spend thousands of dollars on a patentability search to find out if their invention is actually new and patentable. The process can take weeks and the results are subjective. I built this to explore whether AI validators on GenLayer could perform a structured patentability assessment that lives onchain, verified by multiple independent validators before being committed.

The interesting part is that the AI evaluates the invention against the same three legal requirements that real patent examiners use, fetches prior art from a public source, and produces a verdict that anyone can verify on the blockchain.

## How it works

You submit an invention by providing the title, a detailed description, the technical field, and a URL pointing to prior art for comparison. The contract fetches the prior art content and an AI patent examiner evaluates the invention against three core patentability requirements.

The first requirement is Novelty, which means the invention must be new and not previously disclosed in any public document worldwide. The second is Non Obviousness, which means the invention must not be obvious to a person skilled in the technical field. The third is Industrial Application, which means the invention must be useful and capable of being made or used in industry.

Each requirement gets its own status of PASS, PARTIAL, or FAIL along with an overall originality score from 0 to 100. The AI also identifies the most similar prior art found, recommends specific changes to strengthen the patent claims, and produces a summary of the assessment. Multiple validators independently evaluate the same invention and must agree on both the patentability verdict and the originality score within a tolerance of 15 points before the result is committed onchain.

## Functions

submit_invention takes a title, an invention description of at least 50 characters, the technical field, and a URL pointing to prior art for comparison.

verify_patent takes a patent id and triggers the AI patentability evaluation through Optimistic Democracy consensus.

get_patent shows the full result including originality score, patentability verdict, individual status for novelty, non obviousness, and industrial application, similar patents identified, recommendations for strengthening the application, and a summary of the assessment.

get_summary shows the total number of patent verifications performed.

## Test results

Tested the verifier with a wireless solar powered water purification system that combines solar panels with UV LED sterilization and ceramic filtration. The AI returned an originality score of 55 out of 100 with a POSSIBLE patentability verdict. The category breakdown was Novelty PASS, Non Obviousness PARTIAL, and Industrial Application PASS.

The AI correctly identified that commercially available active solar water purifiers combining photovoltaic panels, rechargeable batteries, and multi-stage ceramic or UV filtration already exist in the prior art. The recommendation was to refine the patent claims to emphasize a novel technical integration such as an adaptive energy management algorithm or a uniquely configured hybrid filtration UV chamber that produces unexpected synergistic effects.

The summary correctly noted that while the invention satisfies industrial application and demonstrates novelty over passive solar disinfection methods, the straightforward combination of known components struggles to meet the non obviousness requirement. This is exactly the kind of advice a patent attorney would give to strengthen the application before filing.

## How to run it

Go to GenLayer Studio at https://studio.genlayer.com and create a new file called patent_verifier.py. Paste the contract code and set execution mode to Normal Full Consensus. Deploy with your address as owner_address.

Follow this order and wait for FINALIZED at each step. Run get_summary first, then submit_invention with the invention details, then get_patent to confirm it is pending, then verify_patent to trigger the AI evaluation, then get_patent again to see the full result with all three patentability requirements analyzed.

For best results provide a detailed invention description of at least 200 characters and use a URL that returns plain text or simple HTML content for the prior art search.

Note: the contract in this repository uses the Address type in the constructor as required by genvm-lint. When deploying in GenLayer Studio use a version that receives str in the constructor and converts internally with Address(owner_address) since Studio requires primitive types to parse the contract schema correctly.

## Resources

GenLayer Docs at https://docs.genlayer.com

Optimistic Democracy at https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy

Equivalence Principle at https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy/equivalence-principle

GenLayer Studio at https://studio.genlayer.com

Discord at https://discord.gg/8Jm4v89VAu
