# { "Depends": "py-genlayer:test" }

import json
from genlayer import *


class PatentVerifier(gl.Contract):

    owner: Address
    patent_counter: u256
    patent_data: DynArray[str]
    user_inventions: DynArray[str]
    field_index: DynArray[str]

    def __init__(self, owner_address: str):
        self.owner = Address(owner_address)
        self.patent_counter = u256(0)

    @gl.public.view
    def get_patent(self, patent_id: str) -> str:
        title = self._get(patent_id, "title")
        if not title:
            return "Patent not found"
        return (
            f"ID: {patent_id} | "
            f"Title: {title} | "
            f"Submitter: {self._get(patent_id, 'submitter')} | "
            f"Status: {self._get(patent_id, 'status')} | "
            f"Originality Score: {self._get(patent_id, 'originality_score')}/100 | "
            f"Patentable: {self._get(patent_id, 'patentable')} | "
            f"Novelty: {self._get(patent_id, 'novelty')} | "
            f"Non Obviousness: {self._get(patent_id, 'non_obviousness')} | "
            f"Industrial Application: {self._get(patent_id, 'industrial_application')} | "
            f"Technical Field: {self._get(patent_id, 'technical_field')} | "
            f"Similar Patents: {self._get(patent_id, 'similar_patents')} | "
            f"Recommendations: {self._get(patent_id, 'recommendations')} | "
            f"Summary: {self._get(patent_id, 'summary')} | "
            f"Submissions: {self._get(patent_id, 'submission_count')}"
        )

    @gl.public.view
    def get_patent_count(self) -> u256:
        return self.patent_counter

    @gl.public.view
    def get_my_inventions(self, user_address: str) -> str:
        ids = []
        for i in range(len(self.user_inventions)):
            entry = self.user_inventions[i]
            parts = entry.split(":")
            if len(parts) == 2 and parts[0].lower() == user_address.lower():
                ids.append(parts[1])
        if not ids:
            return "No inventions found for this user"
        return f"User {user_address[:10]}... has {len(ids)} invention(s): {','.join(ids)}"

    @gl.public.view
    def get_patents_by_field(self, technical_field: str) -> str:
        ids = []
        for i in range(len(self.field_index)):
            entry = self.field_index[i]
            parts = entry.split(":", 1)
            if len(parts) == 2 and technical_field.lower() in parts[0].lower():
                ids.append(parts[1])
        if not ids:
            return f"No patents found in field: {technical_field}"
        return f"Field '{technical_field}' has {len(ids)} patent(s): {','.join(ids)}"

    @gl.public.view
    def get_summary(self) -> str:
        total = int(self.patent_counter)
        verified = 0
        likely = 0
        possible = 0
        unlikely = 0
        avg_score = 0
        total_score = 0
        for i in range(total):
            pid = str(i)
            status = self._get(pid, "status")
            if status == "verified":
                verified += 1
                patentable = self._get(pid, "patentable")
                if patentable == "LIKELY":
                    likely += 1
                elif patentable == "POSSIBLE":
                    possible += 1
                elif patentable == "UNLIKELY":
                    unlikely += 1
                score_str = self._get(pid, "originality_score")
                if score_str.isdigit():
                    total_score += int(score_str)
        if verified > 0:
            avg_score = total_score // verified
        return (
            f"GenLayer AI Patent Verifier - Global Stats\n"
            f"Total Inventions Submitted: {total}\n"
            f"Total Verified: {verified}\n"
            f"Likely Patentable: {likely}\n"
            f"Possible: {possible}\n"
            f"Unlikely: {unlikely}\n"
            f"Average Originality Score: {avg_score}/100"
        )

    @gl.public.write
    def submit_invention(
        self,
        title: str,
        invention_description: str,
        technical_field: str,
        prior_art_url: str,
    ) -> str:
        assert len(title) >= 5, "Title too short"
        assert len(invention_description) >= 50, "Invention description too short, provide at least 50 characters"
        assert len(technical_field) >= 5, "Technical field too short"
        assert len(prior_art_url) >= 10, "Prior art URL too short"

        patent_id = str(int(self.patent_counter))
        caller = str(gl.message.sender_address)

        self._set(patent_id, "title", title)
        self._set(patent_id, "description", invention_description[:1500])
        self._set(patent_id, "technical_field", technical_field)
        self._set(patent_id, "prior_art_url", prior_art_url)
        self._set(patent_id, "submitter", caller)
        self._set(patent_id, "status", "pending")
        self._set(patent_id, "originality_score", "0")
        self._set(patent_id, "patentable", "")
        self._set(patent_id, "novelty", "")
        self._set(patent_id, "non_obviousness", "")
        self._set(patent_id, "industrial_application", "")
        self._set(patent_id, "similar_patents", "")
        self._set(patent_id, "recommendations", "")
        self._set(patent_id, "summary", "")
        self._set(patent_id, "submission_count", "1")

        self.user_inventions.append(f"{caller}:{patent_id}")
        self.field_index.append(f"{technical_field}:{patent_id}")
        self.patent_counter = u256(int(self.patent_counter) + 1)

        return f"Invention {patent_id} submitted for patent verification: {title}"

    @gl.public.write
    def resubmit_invention(
        self,
        patent_id: str,
        improved_description: str,
        new_prior_art_url: str,
    ) -> str:
        existing_status = self._get(patent_id, "status")
        assert existing_status == "verified", "Patent must be already verified to be resubmitted"

        caller = str(gl.message.sender_address)
        original_submitter = self._get(patent_id, "submitter")
        assert caller.lower() == original_submitter.lower(), "Only the original submitter can resubmit"

        patentable = self._get(patent_id, "patentable")
        assert patentable in ("POSSIBLE", "UNLIKELY"), "Only POSSIBLE or UNLIKELY patents can be resubmitted"

        assert len(improved_description) >= 50, "Improved description too short"
        assert len(new_prior_art_url) >= 10, "Prior art URL too short"

        submission_count = int(self._get(patent_id, "submission_count") or "1")

        self._set(patent_id, "description", improved_description[:1500])
        self._set(patent_id, "prior_art_url", new_prior_art_url)
        self._set(patent_id, "status", "pending")
        self._set(patent_id, "originality_score", "0")
        self._set(patent_id, "patentable", "")
        self._set(patent_id, "novelty", "")
        self._set(patent_id, "non_obviousness", "")
        self._set(patent_id, "industrial_application", "")
        self._set(patent_id, "similar_patents", "")
        self._set(patent_id, "recommendations", "")
        self._set(patent_id, "summary", "")
        self._set(patent_id, "submission_count", str(submission_count + 1))

        return f"Invention {patent_id} resubmitted with improved evidence. Call verify_patent to re-evaluate. (Submission #{submission_count + 1})"

    @gl.public.write
    def verify_patent(self, patent_id: str) -> str:
        assert self._get(patent_id, "status") == "pending", "Patent verification is not pending"

        title = self._get(patent_id, "title")
        description = self._get(patent_id, "description")
        technical_field = self._get(patent_id, "technical_field")
        prior_art_url = self._get(patent_id, "prior_art_url")

        def leader_fn():
            web_data = ""
            try:
                response = gl.nondet.web.get(prior_art_url)
                raw = response.body.decode("utf-8")
                web_data = raw[:4000]
            except Exception:
                web_data = "Could not fetch prior art content."

            prompt = f"""You are an expert patent examiner specializing in evaluating
the patentability of inventions according to international patent law standards.

Your task is to analyze whether the invention below meets the three core requirements
for patentability and identify any similar prior art that might affect its originality.

Invention Title: {title}
Technical Field: {technical_field}
Invention Description: {description}

Prior Art Search Source from {prior_art_url}:
{web_data}

Evaluate the invention against these three patentability requirements:

REQUIREMENT 1 - NOVELTY
The invention must be new and not previously disclosed in any public document worldwide.
Question: Is this invention sufficiently different from anything in the prior art provided?

REQUIREMENT 2 - NON OBVIOUSNESS (INVENTIVE STEP)
The invention must not be obvious to a person skilled in the technical field.
Question: Would a skilled engineer or scientist in this field consider this an inventive leap or just a routine improvement?

REQUIREMENT 3 - INDUSTRIAL APPLICATION
The invention must be useful and capable of being made or used in industry.
Question: Can this invention be manufactured, used, or commercialized in a real industry?

For each requirement assign a status using these criteria:
PASS means the invention clearly meets this requirement.
PARTIAL means there are some concerns but the requirement could be met with adjustments.
FAIL means the invention does not meet this requirement.

Also assign an overall originality score from 0 to 100 where:
0 to 30 means the invention is not patentable in its current form.
31 to 70 means the invention has potential but needs significant refinement.
71 to 100 means the invention is likely patentable.

Respond ONLY with this JSON:
{{
  "originality_score": 75,
  "patentable": "LIKELY",
  "novelty": "PASS",
  "non_obviousness": "PARTIAL",
  "industrial_application": "PASS",
  "similar_patents": "one sentence describing the most similar prior art found",
  "recommendations": "one sentence with the most important change to strengthen the patent application",
  "summary": "two sentences summarizing the patentability assessment and main concerns"
}}

originality_score is an integer 0 to 100.
patentable must be exactly LIKELY, POSSIBLE, or UNLIKELY.
Each requirement status must be exactly PASS, PARTIAL, or FAIL.
No extra text."""

            result = gl.nondet.exec_prompt(prompt)
            clean = result.strip().replace("```json", "").replace("```", "").strip()
            data = json.loads(clean)

            originality_score = int(data.get("originality_score", 50))
            patentable = data.get("patentable", "POSSIBLE")
            novelty = data.get("novelty", "PARTIAL")
            non_obviousness = data.get("non_obviousness", "PARTIAL")
            industrial_application = data.get("industrial_application", "PARTIAL")
            similar_patents = data.get("similar_patents", "")
            recommendations = data.get("recommendations", "")
            summary = data.get("summary", "")

            originality_score = max(0, min(100, originality_score))
            valid_statuses = ("PASS", "PARTIAL", "FAIL")
            if novelty not in valid_statuses:
                novelty = "PARTIAL"
            if non_obviousness not in valid_statuses:
                non_obviousness = "PARTIAL"
            if industrial_application not in valid_statuses:
                industrial_application = "PARTIAL"
            if patentable not in ("LIKELY", "POSSIBLE", "UNLIKELY"):
                if originality_score >= 71:
                    patentable = "LIKELY"
                elif originality_score >= 31:
                    patentable = "POSSIBLE"
                else:
                    patentable = "UNLIKELY"

            return json.dumps({
                "originality_score": originality_score,
                "patentable": patentable,
                "novelty": novelty,
                "non_obviousness": non_obviousness,
                "industrial_application": industrial_application,
                "similar_patents": similar_patents,
                "recommendations": recommendations,
                "summary": summary
            }, sort_keys=True)

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False
            try:
                validator_raw = leader_fn()
                leader_data = json.loads(leader_result.calldata)
                validator_data = json.loads(validator_raw)
                if leader_data["patentable"] != validator_data["patentable"]:
                    return False
                return abs(leader_data["originality_score"] - validator_data["originality_score"]) <= 15
            except Exception:
                return False

        raw = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        data = json.loads(raw)

        self._set(patent_id, "status", "verified")
        self._set(patent_id, "originality_score", str(data["originality_score"]))
        self._set(patent_id, "patentable", data["patentable"])
        self._set(patent_id, "novelty", data["novelty"])
        self._set(patent_id, "non_obviousness", data["non_obviousness"])
        self._set(patent_id, "industrial_application", data["industrial_application"])
        self._set(patent_id, "similar_patents", data["similar_patents"])
        self._set(patent_id, "recommendations", data["recommendations"])
        self._set(patent_id, "summary", data["summary"])

        return (
            f"Patent verification {patent_id} complete. "
            f"Originality Score: {data['originality_score']}/100. "
            f"Patentable: {data['patentable']}. "
            f"Novelty: {data['novelty']} | "
            f"Non Obviousness: {data['non_obviousness']} | "
            f"Industrial Application: {data['industrial_application']}. "
            f"Similar Patents: {data['similar_patents']}. "
            f"Recommendations: {data['recommendations']}. "
            f"{data['summary']}"
        )

    def _get(self, patent_id: str, field: str) -> str:
        key = f"{patent_id}_{field}:"
        for i in range(len(self.patent_data)):
            if self.patent_data[i].startswith(key):
                return self.patent_data[i][len(key):]
        return ""

    def _set(self, patent_id: str, field: str, value: str) -> None:
        key = f"{patent_id}_{field}:"
        for i in range(len(self.patent_data)):
            if self.patent_data[i].startswith(key):
                self.patent_data[i] = f"{key}{value}"
                return
        self.patent_data.append(f"{key}{value}")
