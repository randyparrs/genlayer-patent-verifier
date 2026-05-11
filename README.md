# GenLayer AI Patent Verifier

A decentralized patent originality verifier where AI validators evaluate inventions against the three core requirements of international patent law and search for similar prior art. Built on GenLayer.

## What is this

Before filing a patent application most inventors spend thousands of dollars on a patentability search to determine if their invention is actually new and patentable. The process can take weeks, the results are subjective, and you have to trust a single firm or expert. I built this to explore whether AI validators on GenLayer could perform a structured patentability assessment that lives onchain, verified by multiple independent validators before being committed.

The interesting part is that the AI evaluates the invention against the same three legal requirements that real patent examiners use, fetches prior art from a public source, and produces a verdict that anyone can verify on the blockchain.

## Why GenLayer

A traditional AI like ChatGPT can give you a similar analysis, but with three critical differences. First, a single AI can hallucinate or make mistakes that you never detect. With GenLayer multiple AI validators must reach consensus on both the verdict and the originality score within a tolerance before the result is accepted. Second, the analysis lives onchain with timestamp and signature, so you can prove later that you verified your invention before filing or before pitching to investors. Third, the trust is decentralized: you do not have to believe a single company or expert, anyone can audit the validators.

## How it works

You submit an invention by providing the title, a detailed description, the technical field, and a URL pointing to prior art. The contract fetches the prior art content and AI validators evaluate the invention against three core patentability requirements.

The first requirement is Novelty: the invention must be new and not previously disclosed in any public document worldwide. The second is Non Obviousness: the invention must not be obvious to a person skilled in the technical field. The third is Industrial Application: the invention must be useful and capable of being made or used in industry.

Each requirement gets its own status of PASS, PARTIAL, or FAIL along with an overall originality score from 0 to 100. The AI also identifies the most similar prior art found, recommends specific changes to strengthen the patent claims, and produces a summary of the assessment. Multiple validators independently evaluate the same invention and must agree on both the patentability verdict and the originality score within a tolerance of 15 points before the result is committed onchain.

## Contract functions

submit_invention takes a title, an invention description of at least 50 characters, the technical field, and a URL pointing to prior art for comparison.

verify_patent takes a patent id and triggers the AI patentability evaluation through Optimistic Democracy consensus.

resubmit_invention takes a patent id, an improved description, and a new prior art URL. Only the original submitter can resubmit, and only POSSIBLE or UNLIKELY inventions can be resubmitted. The contract tracks how many times each invention has been resubmitted.

get_patent shows the full result of a verification including originality score, patentability verdict, individual status for each requirement, similar patents identified, recommendations, and summary.

get_my_inventions takes a user address and returns all the invention IDs that user has submitted.

get_patents_by_field takes a technical field string and returns all the inventions registered in that field.

get_summary returns global statistics including total inventions, total verified, distribution between LIKELY, POSSIBLE, and UNLIKELY, and the average originality score across all verified patents.

## Real-world use cases

A startup wants to verify originality before spending 50 thousand dollars on a patent attorney. They use Patent Verifier first to get a structured opinion from multiple AI validators with onchain evidence of when the verification happened.

An investor wants to validate that a portfolio company actually verified its inventions before claiming patent protection. They can audit the onchain records themselves without trusting the company.

A patent marketplace needs a neutral originality score for inventions being bought or sold. Both buyer and seller can verify the same onchain result without trusting a centralized authority.

A university research group wants to prove date and content of their innovations before publication or filing. Every verification on Patent Verifier is timestamped and signed.

## Test results

Tested with multiple inventions to validate the contract works across different technical fields.

A wireless solar powered water purification system returned an originality score of 55 with a POSSIBLE verdict. Novelty PASS, Non Obviousness PARTIAL, Industrial Application PASS. The AI identified that commercially available active solar water purifiers combining photovoltaic panels, rechargeable batteries, UV LED modules, and ceramic filtration already exist in the prior art. The recommendation was to refine the patent claims toward a novel technical integration such as an adaptive energy management algorithm or a uniquely configured hybrid filtration chamber with unexpected synergistic effects.

A smart beehive health monitor with solar power and machine learning returned an originality score of 78 with a LIKELY verdict. The AI correctly identified that combining thermal sensors, acoustic analysis, weight tracking, LoRa transmission, and predictive ML for swarming events represents a genuine inventive step over existing standalone beehive monitors.

A modular vertical farming pod returned a POSSIBLE verdict because the combination of LED grow lights, hydroponics, and AI climate control, while well executed, was deemed too close to existing vertical farming patents. The recommendation pointed toward more specific algorithmic innovations.

## How to run it

Go to GenLayer Studio at https://studio.genlayer.com and create a new file called patent_verifier.py. Paste the contract code and set execution mode to Normal Full Consensus. Deploy with your wallet address as owner_address.

Follow this order and wait for FINALIZED at each step. Run get_summary first to see initial stats, then submit_invention with the invention details, then get_patent to confirm it is pending, then verify_patent to trigger the AI evaluation, then get_patent again to see the full result with all three patentability requirements analyzed.

For best results provide a detailed invention description of at least 200 characters and use a URL that returns plain text or simple HTML content for the prior art search.

Note: the contract in this repository uses the Address type in the constructor as required by genvm-lint. When deploying in GenLayer Studio use a version that receives str in the constructor and converts internally with Address(owner_address), since Studio requires primitive types to parse the contract schema correctly.

## Live frontend

A complete frontend dApp is deployed at https://patent-verifier-frontend.vercel.app with the following features.

Verify tab to submit and analyze new inventions. How it works section explaining the six step verification process. My Profile tab showing your wallet, your portfolio of submitted inventions, and personal statistics. Explore tab to search verified patents by technical field. Stats tab showing real time global statistics from the network. Resubmit tab to improve POSSIBLE or UNLIKELY inventions with better evidence.

## Resources

GenLayer Docs at https://docs.genlayer.com

Optimistic Democracy at https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy

Equivalence Principle at https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy/equivalence-principle

GenLayer Studio at https://studio.genlayer.com

Discord at https://discord.gg/8Jm4v89VAu
